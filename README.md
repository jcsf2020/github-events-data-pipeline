# GitHub Events Data Pipeline

[![Python Tests](https://github.com/jcsf2020/github-events-data-pipeline/actions/workflows/python-tests.yml/badge.svg)](https://github.com/jcsf2020/github-events-data-pipeline/actions/workflows/python-tests.yml)

A production-oriented portfolio project that implements a layered data engineering pipeline
over the GitHub public events API, using **Python**, **AWS S3**, **Amazon Athena**,
**AWS Glue Catalog**, **Apache Airflow**, **Pytest**, and **GitHub Actions**.

The project demonstrates ingestion reliability, Hive-style partitioned storage, Airflow
TaskFlow orchestration, layered Athena SQL modeling, and a CI-validated test suite — all
designed to reflect real pipeline engineering practices.

---

## Current Evidence Status

| Area | Status |
|---|---|
| Python tests | Passing in CI |
| ruff linting | Passing in CI |
| Python compilation | Passing in CI |
| Airflow DAG import validation | Passing in CI |
| Live S3 / Athena execution | Not yet documented in this repo |
| Terraform / IaC | Not yet implemented |

See [`docs/execution-evidence.md`](docs/execution-evidence.md) for the full evidence baseline
and the gap table with how each item will be closed.

---

## What is implemented

- Hardened Python ingestion client (timeout, retry, error handling)
- Partitioned S3 raw zone (`year=YYYY/month=MM/day=DD`)
- Run metadata logging for operational visibility
- Validation and monitoring modules that read from S3 run logs
- Airflow DAG with three TaskFlow tasks: ingest, validate, monitor
- Athena external tables, staging view, core view, and mart views
- Layered SQL under `sql/` (infrastructure, staging, core, marts, tests)
- `pytest` unit tests for ingestion, validation, and monitoring modules
- GitHub Actions CI running pytest, ruff, compileall, and DAG import validation

## What is not yet proven

- Live AWS execution has not been documented here (no S3 screenshot, no Athena output)
- Terraform / IaC does not exist in this branch
- No deduplication or idempotency strategy is implemented
- Monitoring does not enforce a freshness SLA window
- Python test coverage is partial

---

## Architecture

```text
GitHub public events API
    |
    v
Python ingestion (ingestion/)
    |
    v
S3 raw layer
    |-- raw/github_events/year=YYYY/month=MM/day=DD/
    +-- metadata/run_logs/
    |
    v
Athena external tables
    |-- github_events_partitioned
    +-- pipeline_run_log
    |
    v
Athena views
    |-- github_events_partitioned_staging
    |-- github_events_partitioned_core
    +-- mart_events_by_type / partitioned mart variants
    |
    v
Airflow DAG (orchestration/)
    |-- ingest_github_events
    |-- validate_run_log_contract
    +-- run_monitoring_check
```

Full diagram: [`architecture/pipeline-diagram.md`](architecture/pipeline-diagram.md)

---

## Stack

| Layer | Technology |
|---|---|
| Ingestion | Python, `requests`, `boto3` |
| Storage | Amazon S3 |
| Catalog | AWS Glue Catalog |
| Query | Amazon Athena |
| Orchestration | Apache Airflow (TaskFlow API) |
| Testing | pytest |
| Linting | ruff |
| CI | GitHub Actions |

---

## Setup and Local Validation

**Prerequisites:** Python 3.12, a virtual environment, `uv` or `pip`.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install runtime and dev dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 3. Copy environment config (no real AWS credentials needed for local tests)
cp .env.example .env

# 4. Run tests
python -m pytest -q tests/

# 5. Lint
python -m ruff check .

# 6. Compile Python modules
python -m compileall ingestion monitoring validation orchestration

# 7. Validate Airflow DAG import (requires airflow installed)
pip install apache-airflow
python -c "from orchestration.github_events_dag import dag"
```

Steps 4-7 mirror the GitHub Actions CI workflow exactly.

---

## Evidence Navigation

- [`docs/execution-evidence.md`](docs/execution-evidence.md) — evidence baseline, gap table, and suggested future artifacts
- [`docs/ingestion_contract.md`](docs/ingestion_contract.md) — ingestion behavior contract (S3 paths, run log schema, reliability controls)
- [`architecture/pipeline-diagram.md`](architecture/pipeline-diagram.md) — Mermaid pipeline diagram
- [`.github/workflows/python-tests.yml`](.github/workflows/python-tests.yml) — CI workflow definition

---

## Skills Demonstrated

- Python-based API ingestion with retry, timeout, and error handling
- S3 raw zone design with Hive-style partitioning
- Run metadata logging for pipeline observability
- Airflow orchestration with TaskFlow API
- Athena external tables and multi-layer SQL views
- AWS Glue Catalog integration
- Python unit testing with mocks
- GitHub Actions CI with pytest, ruff, compileall, and DAG import validation
- Layered SQL project structure (staging, core, marts)

---

## Known Limitations

- No Terraform / IaC
- No deduplication or idempotency strategy
- Monitoring does not enforce a freshness SLA window
- Python test coverage is partial
- Live AWS execution evidence not yet documented in this repository

---

## Recommended Next Improvements

1. Document live execution evidence (S3 path, Athena output, Airflow run screenshot)
2. Add minimal Terraform for S3 bucket and Glue table registration
3. Implement a deduplication strategy in the analytical layer
4. Add freshness SLA enforcement to the monitoring check
5. Expand Python test coverage for ingestion and validation layers

---

## Purpose

This project is designed to strengthen a portfolio for **Data Engineer**, **Analytics Engineer**,
and **AWS-oriented pipeline / platform** roles by demonstrating ingestion, operational
reliability, orchestration, and queryable Athena-based analytical modeling.
