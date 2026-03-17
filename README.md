# GitHub Events Data Pipeline

Cloud-based data engineering project built with **Python**, **AWS S3**, **Amazon Athena**, **AWS Glue Catalog**, **Apache Airflow**, **Pytest**, and **GitHub Actions**.

## Overview

This project implements a production-oriented ingestion and analytics pattern for semi-structured GitHub public events data:

- ingest GitHub public events through a hardened Python client
- store raw event data in Amazon S3
- partition raw data by `year/month/day`
- write run metadata to S3 for operational visibility
- validate and monitor the latest pipeline run through Airflow tasks
- expose partitioned raw data in Athena through external tables
- model staging, core, and mart-style analytical views in Athena

This repository is positioned as the **ingestion + reliability + orchestration** pillar of a wider data engineering portfolio.

## Architecture

See the pipeline diagram in:

`architecture/pipeline-diagram.md`

## Current Stack

- **Python** for ingestion, validation, and monitoring scripts
- **Amazon S3** for raw data lake storage and run metadata
- **Amazon Athena** for queryable external tables and analytical views
- **AWS Glue Catalog** for table and view metadata
- **Airflow DAG** for orchestration
- **Pytest** for Python tests
- **GitHub Actions** for CI

## Data Flow

```text
GitHub public events API
    ↓
Python ingestion
    ↓
S3 raw layer
    ├─ raw/github_events/year=YYYY/month=MM/day=DD/
    └─ metadata/run_logs/
    ↓
Athena external tables
    ├─ github_events_partitioned
    └─ pipeline_run_log
    ↓
Athena views
    ├─ github_events_partitioned_staging
    ├─ github_events_partitioned_core
    └─ mart_events_by_type / partitioned marts
    ↓
Airflow DAG
    ├─ ingest_github_events
    ├─ validate_run_log_contract
    └─ run_monitoring_check
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
- uploads raw event data to S3
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

The DAG now uses Airflow TaskFlow-style tasks rather than shelling out through `BashOperator`.

### 5. Athena / SQL layer

The project includes deployed Athena objects for:

- `github_events_partitioned` external table over partitioned raw S3 data
- `pipeline_run_log` external table over S3 run metadata
- `github_events_partitioned_staging` view for structural flattening
- `github_events_partitioned_core` view for typed analytical fields
- `mart_events_by_type` and partitioned mart variants for aggregation

The repository also contains SQL files under:

- `sql/infrastructure`
- `sql/staging`
- `sql/core`
- `sql/marts`
- `sql/tests`

## Skills Demonstrated

- Python-based API ingestion
- S3 raw zone design
- Hive-style partitioning
- Run metadata logging
- Retry / timeout / request error handling
- Airflow orchestration with TaskFlow API
- Athena external tables and views
- AWS Glue Catalog integration
- Python unit testing with mocks
- GitHub Actions CI
- Layered SQL project structure

## Current Status

Implemented and working:

- real ingestion from GitHub public events API
- partitioned S3 raw storage
- run metadata logging to S3
- externalized ingestion configuration
- hardened HTTP ingestion behavior
- Python tests for config, API behavior, validation, and monitoring
- GitHub Actions workflow for pytest, ruff, and DAG import validation
- Airflow DAG with ingest, validate, and monitor tasks
- Athena external tables for raw events and pipeline run logs
- Athena staging, core, and mart views over the ingested data

## Known Limitations

- Python test coverage is still partial
- No Terraform / IaC yet
- No deduplication or idempotency strategy yet
- Monitoring checks latest status and row count, but does not yet enforce a freshness SLA window
- Repository SQL coverage is still being aligned with every live Athena mart object

## Roadmap

Next high-value improvements:

- improve Python test coverage for ingestion and validation layers
- add repository SQL files for all live partitioned mart variants
- add minimal infrastructure-as-code for AWS resources
- implement a clear deduplication strategy in the analytical layer
- add freshness/SLA validation to monitoring

## Purpose

This project is designed to strengthen a portfolio for **Data Engineer**, **Analytics Engineer**, and **AWS-oriented pipeline / platform** roles by demonstrating ingestion, operational reliability, orchestration, and queryable Athena-based analytical modeling over live cloud data.
