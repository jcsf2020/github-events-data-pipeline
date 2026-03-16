from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "joaofonseca",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="github_events_ingestion",
    description="Ingest GitHub public events into S3 raw layer",
    default_args=default_args,
    start_date=datetime(2026, 3, 16),
    schedule="@daily",
    catchup=False,
    tags=["github", "ingestion", "s3"],
) as dag:
    ingest_github_events = BashOperator(
        task_id="ingest_github_events",
        bash_command="cd /opt/airflow && python -m ingestion.github_api_ingestion",
    )

    validate_run_log_contract = BashOperator(
        task_id="validate_run_log_contract",
        bash_command="cd /opt/airflow && python -m validation.validate_run_log sample_run_log.json",
    )

    run_monitoring_check = BashOperator(
        task_id="run_monitoring_check",
        bash_command="echo 'Running monitoring check for GitHub events pipeline'",
    )

    ingest_github_events >> validate_run_log_contract >> run_monitoring_check
