from database import get_connection

def save_pipeline_run(
    name,
    status,
    created_at,
    started_at=None,
    finished_at=None,
    records_received=None,
    records_processed=None,
    records_discarded=None,
    error_message=None
):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO pipeline_runs (
                    pipeline_name,
                    status,
                    error_message,
                    started_at,
                    finished_at,
                    records_received,
                    records_processed,
                    records_discarded,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    name,
                    status,
                    error_message,
                    started_at,
                    finished_at,
                    records_received,
                    records_processed,
                    records_discarded,
                    created_at
                )
            )