def transform_occupations(df):
    required_columns = ['CODIGO', 'TITULO']
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(f'Colunas obrigatórias ausentes: {missing_columns}')

    if df['CODIGO'].isnull().any() or df['CODIGO'].duplicated().any():
        raise ValueError(f'Codigo não pode ser nulo e deve ser unico')

    if df['TITULO'].isnull().any():
        raise ValueError(f'Titulo não pode estar vazio')

    new_occupations = df.dropna(subset=['TITULO'])

    if new_occupations.empty:
        raise ValueError('Quantidade de registros não pode ser zero')

    return new_occupations
