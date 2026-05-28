# Execution Evidence

## Status

**Evidence baseline: partial.**

Local and CI validation is confirmed. Live AWS execution evidence has not yet been
documented in this repository.

---

## What is proven

| Evidence item | Current status |
|---|---|
| Python tests pass | Confirmed — `pytest -q tests` runs in CI and locally |
| GitHub Actions CI workflow exists | Confirmed — `.github/workflows/python-tests.yml` |
| ruff linting passes | Confirmed — `ruff check .` runs in CI |
| Python compilation passes | Confirmed — `compileall ingestion monitoring validation orchestration` runs in CI |
| Airflow DAG import validation passes | Confirmed — `python -c "from orchestration.github_events_dag import dag"` runs in CI |
| Airflow DAG uses TaskFlow API | Confirmed — `orchestration/github_events_dag.py` uses `@dag` / `@task` from `airflow.sdk` |

---

## What is not yet evidenced

| Evidence item | Current status | How to prove later |
|---|---|---|
| Live S3 write proof | Not documented | Run pipeline locally or on EC2; capture S3 object path or `aws s3 ls` output |
| Athena query output | Not documented | Run `SELECT` against `github_events_partitioned`; export CSV or screenshot |
| Glue Catalog table registration | Not documented | Screenshot Glue Console table list or `aws glue get-table` output |
| Airflow scheduled DAG run | Not documented | Screenshot Airflow UI DAG run grid or export `dag_run` table row |
| Run log JSON artifact | Not documented | Copy a `metadata/run_logs/run_YYYYMMDD_HHMMSS.json` with bucket name redacted |
| CI run link | Partial | CI runs on pushes to `main` and `feat/**`; link a passing run URL once available |

---

## Suggested future evidence artifacts

The following artifacts would fully close the evidence gap without exposing secrets:

1. **S3 object path sample** — e.g. `raw/github_events/year=2026/month=05/day=28/events_20260528_120000.json` (bucket name can be redacted)
2. **Run log JSON sample** — the `metadata/run_logs/run_*.json` payload with `status: SUCCESS` and a real `records_ingested` count
3. **Athena query output** — a `SELECT COUNT(*), event_type FROM github_events_partitioned_core GROUP BY event_type` result exported as CSV or screenshot
4. **Airflow DAG run screenshot** — the DAG run grid showing three green tasks: `ingest_github_events`, `validate_run_log_contract`, `run_monitoring_check`
5. **GitHub Actions passing run link** — a URL to a green CI run on the `main` branch

---

## Safety notes

- No AWS commands were run to produce this document.
- No secrets, credentials, or bucket contents are included.
- Evidence claims above are based on code inspection only.
