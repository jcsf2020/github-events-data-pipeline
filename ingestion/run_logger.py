import json
import boto3


def log_success(bucket, run_id, run_ts, partition_path, records_ingested):
    s3 = boto3.client("s3")

    run_log = {
        "run_id": run_id,
        "run_ts": run_ts,
        "partition_path": partition_path,
        "records_ingested": records_ingested,
        "status": "SUCCESS",
        "error_message": None,
    }

    s3.put_object(
        Bucket=bucket,
        Key=f"metadata/run_logs/run_{run_id}.json",
        Body=json.dumps(run_log),
    )


def log_failure(bucket, run_id, run_ts, error_message):
    s3 = boto3.client("s3")

    failed_log = {
        "run_id": run_id,
        "run_ts": run_ts,
        "partition_path": None,
        "records_ingested": 0,
        "status": "FAILED",
        "error_message": str(error_message),
    }

    s3.put_object(
        Bucket=bucket,
        Key=f"metadata/run_logs/run_{run_id}.json",
        Body=json.dumps(failed_log),
    )
