# Ingestion Contract

## Purpose

This document freezes the current behavior of the GitHub events ingestion pipeline before refactoring.

## Source

- Source system: GitHub Public Events API
- Endpoint: `https://api.github.com/events`
- Method: `GET`
- Response format: JSON array of event objects

## Ingestion Script

- Script path: `ingestion/github_api_ingestion.py`

## Raw Output Contract

- Bucket: `joaofonseca-data-platform`
- Prefix: `raw/github_events`
- File pattern:

```text
raw/github_events/year=YYYY/month=MM/day=DD/events_YYYYMMDD_HHMMSS.json
```

- Storage format: newline-delimited JSON
- Partitioning strategy: ingestion date (year/month/day)

## Run Metadata Contract

- Prefix: metadata/run_logs
- File pattern:

metadata/run_logs/run_YYYYMMDD_HHMMSS.json

Fields written:

- run_id
- run_ts
- partition_path
- records_ingested
- status
- error_message

## Success Behavior

On successful execution the pipeline:

1. Calls the GitHub events endpoint
2. Receives a JSON array of events
3. Writes newline-delimited JSON to S3 raw storage
4. Writes a SUCCESS run log to S3 metadata storage

## Failure Behavior

On failure the pipeline:

1. Writes a FAILED run log to S3 metadata storage
2. Sets partition_path to null
3. Sets records_ingested to 0
4. Stores the exception message in error_message
5. Re-raises the exception

## Current Invariants

- Raw event payload is stored without schema enforcement
- S3 partitioning is based on ingestion date
- Run metadata is written for both success and failure
- Bucket and prefixes are currently hardcoded in the script

## Current Limitations

- No HTTP timeout configured
- No retry logic
- No schema validation
- No deduplication
- No external configuration file
- No orchestration layer

## Notes

This contract freezes the ingestion behavior before refactoring the pipeline architecture.
