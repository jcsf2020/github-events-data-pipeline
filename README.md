# GitHub Events Data Pipeline

Cloud-based data engineering project built with **Python**, **AWS S3**, **Athena-oriented storage patterns**, **Airflow**, **Pytest**, and **GitHub Actions**.

## Overview

This project demonstrates a production-style ingestion and orchestration pattern for semi-structured event data:

- ingest GitHub public events through a hardened Python client
- store newline-delimited JSON in an S3 raw layer
- partition raw data by `year/month/day`
- write run metadata to S3 for operational visibility
- validate and monitor the latest pipeline run through Airflow tasks
- prepare SQL layers for staging, core, and mart-style analytics modeling

This repository is positioned as the **ingestion + reliability + orchestration** pillar of a wider data engineering portfolio.

## Architecture

See the pipeline diagram in:

`architecture/pipeline-diagram.md`

## Current Stack

- **Python** for ingestion, validation, and monitoring scripts
- **Amazon S3** for raw data lake storage and run metadata
- **Amazon Athena / AWS Glue-oriented patterns** for downstream SQL querying
- **Airflow DAG** for orchestration
- **Pytest** for Python tests
- **GitHub Actions** for CI

## Data Flow

```text
GitHub public events API
    ↓
Python ingestion
    ↓
S3 raw layer (newline-delimited JSON)
    ↓
S3 run log metadata
    ↓
Airflow DAG
    ├─ ingest
    ├─ validate latest S3 run log
    └─ monitor latest S3 run status
```

## Implemented Components

### 1. Source layer

GitHub public events API accessed through a Python source module with:

- request timeout
- retry for transient `5xx` errors
- explicit request exception handling

### 2. Ingestion layer

The ingestion pipeline:

- fetches GitHub public events
- uploads newline-delimited JSON to S3
- writes partitioned raw files using:
  - `year=YYYY`
  - `month=MM`
  - `day=DD`
- writes run metadata to `metadata/run_logs/`

### 3. Validation and monitoring layer

The project includes Python scripts that:

- validate the latest run log stored in S3
- check latest pipeline run status and ingested record count

### 4. Orchestration layer

The Airflow DAG orchestrates three tasks:

- `ingest_github_events`
- `validate_run_log_contract`
- `run_monitoring_check`

### 5. SQL layer

The repository includes SQL directories for:

- `staging`
- `core`
- `marts`
- `tests`

These provide the foundation for the Athena-side transformation story.

## Skills Demonstrated

- Python-based API ingestion
- S3 raw zone design
- Hive-style partitioning
- Run metadata logging
- Retry / timeout / request error handling
- Basic Airflow orchestration
- Python unit testing with mocks
- GitHub Actions CI
- Layered SQL project structure

## Current Status

Implemented today:

- real ingestion from GitHub public events API
- partitioned S3 raw storage
- run metadata logging to S3
- externalized ingestion configuration
- hardened HTTP ingestion behavior
- Python tests for config and API behavior
- GitHub Actions workflow for pytest
- Airflow DAG with ingest, validate, and monitor tasks
- validation and monitoring scripts backed by real S3 run logs

## Known Limitations

- Airflow still uses `BashOperator`
- Athena external table DDL is not yet implemented
- SQL layers are present but not yet wired into an executable Athena workflow
- Python test coverage is still partial
- No Terraform / IaC yet
- No deduplication or idempotency strategy yet

## Roadmap

Next high-value improvements:

- improve Python test coverage for ingestion and validation layers
- add Athena external table DDL and partition management story
- strengthen CI with linting and DAG validation
- improve Airflow implementation beyond the current BashOperator pattern
- add minimal infrastructure-as-code for AWS resources

## Purpose

This project is designed to strengthen a portfolio for **Data Engineer**, **Analytics Engineer**, and **AWS-oriented pipeline / platform** roles by demonstrating ingestion, operational reliability, and orchestration patterns used in real data platforms.
