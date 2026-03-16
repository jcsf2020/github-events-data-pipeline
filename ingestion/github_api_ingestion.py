import json
from datetime import UTC, datetime

import boto3

from ingestion.config import S3_BUCKET, S3_PREFIX
from ingestion.github_api import fetch_github_events
from ingestion.run_logger import log_failure, log_success


def upload_raw_events(bucket, prefix, data):
    s3 = boto3.client("s3")

    now = datetime.now(UTC)
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    key = f"{prefix}/year={year}/month={month}/day={day}/events_{timestamp}.json"

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body="\n".join(json.dumps(event) for event in data),
    )

    return {
        "run_id": timestamp,
        "run_ts": now.isoformat(),
        "partition_path": key,
        "records_ingested": len(data),
    }


def main():
    now = datetime.now(UTC)
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    try:
        events = fetch_github_events()
        run_metadata = upload_raw_events(S3_BUCKET, S3_PREFIX, events)
        log_success(
            bucket=S3_BUCKET,
            run_id=run_metadata["run_id"],
            run_ts=run_metadata["run_ts"],
            partition_path=run_metadata["partition_path"],
            records_ingested=run_metadata["records_ingested"],
        )
        print(f"Uploaded file to s3://{S3_BUCKET}/{run_metadata['partition_path']}")
    except Exception as exc:
        log_failure(
            bucket=S3_BUCKET,
            run_id=timestamp,
            run_ts=now.isoformat(),
            error_message=exc,
        )
        raise


if __name__ == "__main__":
    main()
