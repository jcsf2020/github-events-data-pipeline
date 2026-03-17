CREATE EXTERNAL TABLE IF NOT EXISTS pipeline_run_log (
    run_id string,
    run_ts string,
    partition_path string,
    records_ingested bigint,
    status string,
    error_message string
) ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe' WITH SERDEPROPERTIES ('ignore.malformed.json' = 'true') STORED AS TEXTFILE LOCATION 's3://joaofonseca-data-platform/metadata/run_logs' TBLPROPERTIES ('has_encrypted_data' = 'false');