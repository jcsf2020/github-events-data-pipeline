-- latest run timestamp
SELECT MAX(run_ts) AS latest_run_ts
FROM pipeline_run_log;
-- runs by status
SELECT status,
    COUNT(*) AS runs
FROM pipeline_run_log
GROUP BY status;
-- run history
SELECT run_id,
    run_ts,
    partition_path,
    records_ingested,
    status
FROM pipeline_run_log
ORDER BY run_ts DESC;