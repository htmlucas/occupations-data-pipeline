import pandas as pd
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
CBO_FILE = BASE_DIR / "data" / "raw" / "cbo.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


keyword = 'all'
csv_name = "occupations_processed.csv"

if len(sys.argv) > 1 and sys.argv[1] == '--search':
    if len(sys.argv) > 2:
        keyword = sys.argv[2]

df = pd.read_csv(CBO_FILE, encoding='utf-8')

# Tratamentos

new_df = df.drop_duplicates() #removendo dados duplicados
new_df = new_df.drop_duplicates(subset = ['cod_cbo']) # removendo cbos duplicados
new_df = new_df.dropna(subset=['nom_cbo']) # removendo dados nulos de nomes

cbo_counts = df['cod_cbo'].value_counts()

print('Registros recebidos', len(df))
print('Linhas duplicadas encontradas', df.duplicated().sum())
print('Cbos unicos duplicados:', len(cbo_counts[cbo_counts > 1]))
print('Registros sem nome:', df['nom_cbo'].isna().sum())
print('Registros após limpeza:', len(new_df))
print('Registros descartados:', len(df) - len(new_df))

# Filtrando por uma palavra-chave

if keyword != 'all':
    new_df = new_df[new_df['nom_cbo'].str.contains(keyword, na= False, case = False)]
    csv_name = "occupations_"+keyword+"_processed.csv"

print('Registros após filtro:', len(new_df))

# Salvando os dados tratados em outro arquivo
output_file = PROCESSED_DIR / csv_name
new_df.to_csv(output_file,index = False)
print('Arquivo salvo em:',output_file)