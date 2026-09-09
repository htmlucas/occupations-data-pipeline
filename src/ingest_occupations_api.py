import requests
import pandas as pd
from io import StringIO
from pathlib import Path
from datetime import datetime
import json
import time

from export import export_csv, export_parquet
from transform import transform_occupations

# Enquanto o pandas.read_csv() trabalha muito bem recebendo algo que se comporta como um arquivo.
# O StringIO pega a string e cria um objeto que funciona como um arquivo em memória:

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
METADATA_DIR = BASE_DIR / "data" / "metadata"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

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
res = requests.get(url)

# usar response.raise_for_status();
res.raise_for_status()

# converter o JSON em DataFrame
occupations = pd.read_csv(StringIO(res.text), sep = ';')

# salvar a resposta recebida sem modificá-la;
export_csv(occupations,raw_output_file)

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
    "source" : url,
    "requested_at" : datetime.now().isoformat(),
    "status_code": res.status_code,
    "content_type": res.headers.get('Content-Type'),
}

with open(metadata_output_file, 'w', encoding='utf-8' ) as file:
    json.dump(metadata, file, ensure_ascii= False, indent=4)
