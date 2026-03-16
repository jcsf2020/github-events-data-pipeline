import json
from pathlib import Path


REQUIRED_FIELDS = {
    "run_id",
    "run_ts",
    "partition_path",
    "records_ingested",
    "status",
    "error_message",
}


def validate_run_log(run_log):
    missing_fields = REQUIRED_FIELDS - set(run_log.keys())

    if missing_fields:
        raise ValueError(f"Missing required fields: {sorted(missing_fields)}")

    if run_log["status"] != "SUCCESS":
        raise ValueError(f"Run log status must be SUCCESS, got: {run_log['status']}")

    if run_log["records_ingested"] <= 0:
        raise ValueError("Run log records_ingested must be greater than 0")


def main():
    run_log_path = Path("sample_run_log.json")

    with run_log_path.open() as file:
        run_log = json.load(file)

    validate_run_log(run_log)
    print("Run log validation passed")


if __name__ == "__main__":
    main()
