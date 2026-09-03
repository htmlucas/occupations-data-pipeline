import requests
import pandas as pd
from io import StringIO
from pathlib import Path
from datetime import datetime
import json

# Enquanto o pandas.read_csv() trabalha muito bem recebendo algo que se comporta como um arquivo.
# O StringIO pega a string e cria um objeto que funciona como um arquivo em memória:

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
METADATA_DIR = BASE_DIR / "data" / "metadata"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

raw_csv_name = "official_occupations.csv"
processed_csv_name = "official_occupations_processed.csv"
metadata_json_name = "ingestion_metadata.json"

raw_output_file = RAW_DIR / raw_csv_name
processed_output_file = PROCESSED_DIR / processed_csv_name
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
occupations.to_csv(raw_output_file, index = False)

# validar a presença das colunas necessárias;
required_columns = ['CODIGO', 'TITULO']
missing_columns = set(required_columns) - set(occupations.columns)

if missing_columns:
    raise ValueError(f'Colunas obrigatórias ausentes: {missing_columns}')

# contar quantos cod_cbo distintos aparecem mais de uma vez;
occupations_counts = occupations['CODIGO'].value_counts()

occupations_duplicados = occupations_counts[occupations_counts > 1]
print('Occupations distintos duplicados:', len(occupations_duplicados))

# remover registros sem nome da ocupação;
new_occupations = occupations.dropna(subset=['TITULO'])

# gerar um CSV processado;
occupations.to_csv(processed_output_file, index = False)

# informar registros recebidos, descartados e processados.
print('Registros recebidos', len(occupations))
print('Registros descartados:', len(occupations) - len(new_occupations))
print('Registros após limpeza:', len(new_occupations))

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

