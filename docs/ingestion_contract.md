# Ingestion Contract

## Purpose

This document defines the current behavior of the GitHub events ingestion pipeline.

## Source

- Source system: GitHub Public Events API
- Endpoint: `https://api.github.com/events`
- Method: `GET`
- Response format: JSON array of event objects

## Ingestion Modules

- Source module: `ingestion/github_api.py`
- Ingestion entrypoint: `ingestion/github_api_ingestion.py`
- Run logging module: `ingestion/run_logger.py`
- Config module: `ingestion/config.py`

## Raw Output Contract

- Bucket: `joaofonseca-data-platform`
- Prefix: `raw/github_events`
- File pattern:

```text
raw/github_events/year=YYYY/month=MM/day=DD/events_YYYYMMDD_HHMMSS.json
```

## Raw File Format

- Output format: newline-delimited JSON
- One GitHub event per line
- Raw payload stored without schema enforcement

## Run Metadata Contract

Run metadata is written to:

```text
metadata/run_logs/run_YYYYMMDD_HHMMSS.json
```

Each run log contains:

- `run_id`
- `run_ts`
- `partition_path`
- `records_ingested`
- `status`
- `error_message`

## Success Behavior

On success the pipeline:

1. Calls the GitHub public events API
2. Receives a JSON array of events
3. Writes newline-delimited JSON to S3 raw storage
4. Writes a `SUCCESS` run log to S3 metadata storage

## Failure Behavior

On failure the pipeline:

1. Writes a `FAILED` run log to S3 metadata storage
2. Sets `partition_path` to `null`
3. Sets `records_ingested` to `0`
4. Stores the exception message in `error_message`
5. Re-raises the exception

## Current Reliability Controls

The source access layer includes:

- HTTP timeout
- retry for transient `500`, `502`, `503`, and `504` responses
- explicit request exception handling

## Current Invariants

- S3 partitioning is based on ingestion date
- Run metadata is written for both success and failure
- Configuration is externalized through `config.py`
- Validation and monitoring scripts read the latest run log from S3

## Current Limitations

- No deduplication strategy
- No idempotency strategy
- No Athena external table DDL yet
- No partition sync / projection layer yet
- Airflow orchestration still uses `BashOperator`

## Notes

This contract reflects the implemented ingestion behavior currently present in the repository.
