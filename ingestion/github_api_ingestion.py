import requests
import json
from datetime import datetime, UTC
import boto3

# GitHub public events endpoint
GITHUB_EVENTS_URL = "https://api.github.com/events"

# S3 configuration
S3_BUCKET = "joaofonseca-data-platform"
S3_PREFIX = "raw/github_events"


def fetch_github_events():
    response = requests.get(GITHUB_EVENTS_URL)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}")

    return response.json()


def upload_to_s3(data):
    s3 = boto3.client("s3")

    now = datetime.now(UTC)
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    key = f"{S3_PREFIX}/year={year}/month={month}/day={day}/events_{timestamp}.json"

    s3.put_object(
        Bucket=S3_BUCKET, Key=key, Body="\n".join(json.dumps(event) for event in data)
    )

    run_log = {
        "run_id": timestamp,
        "run_ts": now.isoformat(),
        "partition_path": key,
        "records_ingested": len(data),
        "status": "SUCCESS",
    }

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"metadata/run_logs/run_{timestamp}.json",
        Body=json.dumps(run_log),
    )

    print(f"Uploaded file to s3://{S3_BUCKET}/{key}")


def main():
    events = fetch_github_events()
    upload_to_s3(events)


if __name__ == "__main__":
    main()
