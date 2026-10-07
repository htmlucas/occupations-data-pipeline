import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone
from transform import transform_occupations
from save_pipeline_run import save_pipeline_run

# Tempos
execution_time = datetime.now()

run_id = execution_time.strftime("%Y-%m-%d_%H-%M-%S")
started_at = datetime.now(timezone.utc)

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
    save_pipeline_run(
        name = "teste_validation",
        status = "FAILED",
        created_at = started_at,
        error_message=str(error),
    )
    raise

# contar quantos cod_cbo distintos aparecem mais de uma vez;
occupations_counts = new_occupations['CODIGO'].value_counts()

occupations_duplicados = occupations_counts[occupations_counts > 1]
print('Occupations distintos duplicados:', len(occupations_duplicados))

finished_at = datetime.now(timezone.utc)

save_pipeline_run(
    name='occupations_pipeline',
    status='SUCCESS',
    started_at=started_at,
    finished_at=finished_at,
    records_received=len(occupations),
    records_processed=len(new_occupations),
    records_discarded=len(occupations) - len(new_occupations),
    created_at=finished_at
)
