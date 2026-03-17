from unittest.mock import patch

import pytest

from monitoring.check_latest_run import main


def test_check_latest_run_module_imports():
    assert callable(main)


@patch("monitoring.check_latest_run.load_latest_run_log")
def test_check_latest_run_main_passes_on_success(mock_load_latest_run_log, capsys):
    mock_load_latest_run_log.return_value = (
        "metadata/run_logs/run_20260316_015326.json",
        {
            "run_id": "20260316_015326",
            "run_ts": "2026-03-16T01:53:26+00:00",
            "partition_path": "raw/github_events/year=2026/month=03/day=16/events_20260316_015326.json",
            "records_ingested": 30,
            "status": "SUCCESS",
            "error_message": None,
        },
    )

    main()

    captured = capsys.readouterr()
    assert "Monitoring check passed for s3://" in captured.out


@patch("monitoring.check_latest_run.load_latest_run_log")
def test_check_latest_run_main_raises_on_failed_status(mock_load_latest_run_log):
    mock_load_latest_run_log.return_value = (
        "metadata/run_logs/run_20260316_015326.json",
        {
            "run_id": "20260316_015326",
            "run_ts": "2026-03-16T01:53:26+00:00",
            "partition_path": None,
            "records_ingested": 0,
            "status": "FAILED",
            "error_message": "boom",
        },
    )

    with pytest.raises(ValueError, match="Latest run status is not SUCCESS"):
        main()


@patch("monitoring.check_latest_run.load_latest_run_log")
def test_check_latest_run_main_raises_on_zero_records(mock_load_latest_run_log):
    mock_load_latest_run_log.return_value = (
        "metadata/run_logs/run_20260316_015326.json",
        {
            "run_id": "20260316_015326",
            "run_ts": "2026-03-16T01:53:26+00:00",
            "partition_path": "raw/github_events/year=2026/month=03/day=16/events_20260316_015326.json",
            "records_ingested": 0,
            "status": "SUCCESS",
            "error_message": None,
        },
    )

    with pytest.raises(ValueError, match="Latest run has no ingested records"):
        main()
