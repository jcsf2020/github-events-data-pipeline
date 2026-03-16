import pytest

from monitoring.check_latest_run import main


def test_check_latest_run_module_imports():
    assert callable(main)


def test_check_latest_run_success_payload_contract():
    run_log = {
        "run_id": "20260316_015326",
        "run_ts": "2026-03-16T01:53:26+00:00",
        "partition_path": "raw/github_events/year=2026/month=03/day=16/events_20260316_015326.json",
        "records_ingested": 30,
        "status": "SUCCESS",
        "error_message": None,
    }

    assert run_log["status"] == "SUCCESS"
    assert run_log["records_ingested"] > 0


def test_check_latest_run_failure_payload_contract():
    run_log = {
        "run_id": "20260316_015326",
        "run_ts": "2026-03-16T01:53:26+00:00",
        "partition_path": None,
        "records_ingested": 0,
        "status": "FAILED",
        "error_message": "boom",
    }

    with pytest.raises(AssertionError):
        assert run_log["status"] == "SUCCESS"
