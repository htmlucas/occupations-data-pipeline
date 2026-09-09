

def export_csv(df, output_path):
    df.to_csv(
        output_path,
        index = False
    )

def export_parquet(df, output_path):
    df.to_parquet(
        output_path,
        index = False,
        engine = 'pyarrow',
        compression = 'snappy'
    )