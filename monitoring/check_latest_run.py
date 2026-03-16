import json

import boto3

from ingestion.config import S3_BUCKET


RUN_LOG_PREFIX = "metadata/run_logs/"


def load_latest_run_log():
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=RUN_LOG_PREFIX)
    contents = response.get("Contents", [])

    if not contents:
        raise ValueError("No run log files found in S3")

    latest_run_log = max(contents, key=lambda item: item["LastModified"])
    run_log_key = latest_run_log["Key"]

    response = s3.get_object(Bucket=S3_BUCKET, Key=run_log_key)
    run_log = json.loads(response["Body"].read().decode("utf-8"))

    return run_log_key, run_log


def main():
    run_log_key, run_log = load_latest_run_log()

    if run_log["status"] != "SUCCESS":
        raise ValueError(f"Latest run status is not SUCCESS: {run_log['status']}")

    if run_log["records_ingested"] <= 0:
        raise ValueError("Latest run has no ingested records")

    print(f"Monitoring check passed for s3://{S3_BUCKET}/{run_log_key}")


if __name__ == "__main__":
    main()
