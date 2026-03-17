from datetime import datetime, timedelta

from airflow.sdk import dag, task


DEFAULT_ARGS = {
    "owner": "joaofonseca",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="github_events_ingestion",
    description="Ingest GitHub public events into S3 raw layer",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 3, 16),
    schedule="@daily",
    catchup=False,
    tags=["github", "ingestion", "s3"],
)
def github_events_pipeline():
    @task(execution_timeout=timedelta(minutes=10))
    def ingest_github_events():
        from ingestion.github_api_ingestion import main

        main()

    @task(execution_timeout=timedelta(minutes=5))
    def validate_run_log_contract():
        from validation.validate_run_log import main

        main()

    @task(execution_timeout=timedelta(minutes=5))
    def run_monitoring_check():
        from monitoring.check_latest_run import main

        main()

    ingest = ingest_github_events()
    validate = validate_run_log_contract()
    monitor = run_monitoring_check()

    ingest >> validate >> monitor


dag = github_events_pipeline()
