import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import json
import time
from upload_to_s3 import upload_file
from export import export_csv, export_parquet
from transform import transform_occupations

# Tempos
execution_time = datetime.now()
run_id = execution_time.strftime("%Y-%m-%d_%H-%M-%S")
requested_at = execution_time.isoformat()

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
METADATA_DIR = BASE_DIR / "data" / "metadata"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
S3_BUCKET_NAME  = "occupations-data-pipeline-lucas-2026"

raw_csv_name = "official_occupations.csv"
processed_csv_name = "official_occupations_processed.csv"
processed_parquet_name = "official_occupations_processed.parquet"
metadata_json_name = "ingestion_metadata.json"

raw_output_file = RAW_DIR / raw_csv_name
processed_output_file = PROCESSED_DIR / processed_csv_name
parquet_output_file = PROCESSED_DIR / processed_parquet_name
metadata_output_file = METADATA_DIR / metadata_json_name

# url
url = "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/cbo/servicos/downloads/cbo2002-ocupacao.csv"

# usar requests;
res = requests.get(url, timeout=30)

# usar response.raise_for_status();
res.raise_for_status()

# RAW: guarda exatamente o que veio da fonte
with open(raw_output_file, "wb") as file:
    file.write(res.content)

# PROCESSAMENTO
# A fonte oficial da CBO utiliza uma codificação compatível com Latin-1.
occupations = pd.read_csv(raw_output_file, sep=';',encoding='latin1')

# validar;
try:
    new_occupations = transform_occupations(occupations)
except ValueError as error:
    print(f"Erro na transformação: {error}")
    raise

# contar quantos cod_cbo distintos aparecem mais de uma vez;
occupations_counts = new_occupations['CODIGO'].value_counts()

occupations_duplicados = occupations_counts[occupations_counts > 1]
print('Occupations distintos duplicados:', len(occupations_duplicados))

# gerar um CSV processado;
export_csv(new_occupations, processed_output_file)
occupations_file = Path(processed_output_file)
occupations_file_size = occupations_file.stat().st_size / (1024 ** 2)

# salvar em um arquivo PARQUET
export_parquet(new_occupations, parquet_output_file)

# ler o arquivo CSV processado
inicio = time.perf_counter()
occupations_processed_file = pd.read_csv(processed_output_file, sep = ';')
tempo_csv = time.perf_counter() - inicio

# ler o arquivo PARQUET
inicio = time.perf_counter()
parquet_file = pd.read_parquet(parquet_output_file, engine="pyarrow")
tempo_parquet = time.perf_counter() - inicio

get_parquet_file = Path(parquet_output_file)
parquet_file_size = get_parquet_file.stat().st_size / (1024 ** 2)

# informar registros recebidos, descartados e processados.
print('Registros recebidos', len(occupations))
print('Registros descartados:', len(occupations) - len(new_occupations))
print('Registros após limpeza:', len(new_occupations))

# Comparar os 2 arquivos
print('CSV')
print('Registros:', len(new_occupations))
print('Colunas', len(new_occupations.columns))
print(F"Tamanho: {occupations_file_size:.2f} MB")

print('PARQUET')
print('Registros:', len(parquet_file))
print('Colunas', len(parquet_file.columns))
print(F"Tamanho: {parquet_file_size:.2f} MB")

# Medir tempo de leitura para cada formato
print(f"Tempo de leitura CSV: {tempo_csv:.6f} segundos")
print(f"Tempo de leitura Parquet: {tempo_parquet:.6f} segundos")

# arquivo metadata.json contendo:
# URL consultada;
# data da coleta;
# quantidade recebida;
# quantidade processada;
# quantidade descartada;

metadata = {
    "run_id" : run_id,
    "source" : url,
    "requested_at" : requested_at,
    "status_code": res.status_code,
    "content_type": res.headers.get('Content-Type'),
    "received_quantity": len(occupations),
    "processed_quantity": len(new_occupations),
    "descarted_quantity": len(occupations) - len(new_occupations),
}

with open(metadata_output_file, 'w', encoding='utf-8' ) as file:
    json.dump(metadata, file, ensure_ascii= False, indent=4)

# Enviar arquivos para o Aws S3 Bucket - occupations-data-pipeline-lucas-2026

print('Iniciando o upload pro S3')

# RAW

raw_s3_key = f"raw/{run_id}/{raw_csv_name}"

processed_csv_s3_key = (
    f"processed/{run_id}/{processed_csv_name}"
)

processed_parquet_s3_key = (
    f"processed/{run_id}/{processed_parquet_name}"
)

metadata_s3_key = (
    f"reports/{run_id}/{metadata_json_name}"
)

raw_return = upload_file(
    file_name=str(raw_output_file),
    bucket=S3_BUCKET_NAME,
    object_name=raw_s3_key,
)

print('RAW:',raw_return)

# PROCESSED

processed_return = upload_file(
    file_name=str(processed_output_file),
    bucket=S3_BUCKET_NAME,
    object_name=processed_csv_s3_key,
)

print('PROCESSED:',processed_return)

# PARQUET

parquet_return = upload_file(
    file_name=str(parquet_output_file),
    bucket=S3_BUCKET_NAME,
    object_name=processed_parquet_s3_key,
)

print('PARQUET:', parquet_return)

# Metadata

metadata_return = upload_file(
    file_name=str(metadata_output_file),
    bucket=S3_BUCKET_NAME,
    object_name=metadata_s3_key,
)

print('METADATA:', metadata_return)