import pytest

from validation.validate_run_log import validate_run_log


def test_validate_run_log_accepts_valid_success_payload():
    run_log = {
        "run_id": "20260316_015326",
        "run_ts": "2026-03-16T01:53:26+00:00",
        "partition_path": "raw/github_events/year=2026/month=03/day=16/events_20260316_015326.json",
        "records_ingested": 30,
        "status": "SUCCESS",
        "error_message": None,
    }

    validate_run_log(run_log)


def test_validate_run_log_raises_when_required_field_is_missing():
    run_log = {
        "run_id": "20260316_015326",
        "run_ts": "2026-03-16T01:53:26+00:00",
        "partition_path": "raw/github_events/year=2026/month=03/day=16/events_20260316_015326.json",
        "records_ingested": 30,
        "status": "SUCCESS",
    }

    with pytest.raises(ValueError, match="Missing required fields"):
        validate_run_log(run_log)


def test_validate_run_log_raises_when_status_is_not_success():
    run_log = {
        "run_id": "20260316_015326",
        "run_ts": "2026-03-16T01:53:26+00:00",
        "partition_path": None,
        "records_ingested": 0,
        "status": "FAILED",
        "error_message": "boom",
    }

    with pytest.raises(ValueError, match="Run log status must be SUCCESS"):
        validate_run_log(run_log)
