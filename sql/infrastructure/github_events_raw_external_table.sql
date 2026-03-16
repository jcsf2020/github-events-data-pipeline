CREATE EXTERNAL TABLE IF NOT EXISTS github_events_raw (event string) PARTITIONED BY (
    year string,
    month string,
    day string
) ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe' WITH SERDEPROPERTIES ('ignore.malformed.json' = 'true') STORED AS TEXTFILE LOCATION 's3://joaofonseca-data-platform/raw/github_events/' TBLPROPERTIES ('has_encrypted_data' = 'false');