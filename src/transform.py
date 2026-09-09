

def transform_occupations(df):
    required_columns = ['CODIO', 'TITULO']
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(f'Colunas obrigatórias ausentes: {missing_columns}')

    new_occupations = df.dropna(subset=['TITULO'])

    return new_occupations