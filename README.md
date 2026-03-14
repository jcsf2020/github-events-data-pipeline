# GitHub Events Data Pipeline

Cloud-based data engineering project built with **AWS S3**, **Athena**, **SQL**, and a layered lakehouse-style architecture.

## Overview

This project demonstrates how to ingest semi-structured event data into an AWS data lake and transform it into analytics-ready datasets using a layered approach:

- **Raw** → original JSON event data stored in S3
- **Staging** → flattened fields from nested JSON
- **Core** → normalized types and business-friendly naming
- **Mart** → analytical aggregations ready for reporting

## Architecture

See the pipeline diagram in:

`architecture/pipeline-diagram.md`

## Current Stack

- **Amazon S3** for raw data lake storage
- **Amazon Athena** for SQL querying and transformations
- **AWS Glue Data Catalog / Athena metadata**
- **SQL views** for staging, core and mart layers

## Data Flow

```text
GitHub event JSON
    ↓
S3 raw layer
    ↓
Athena external table
    ↓
staging view
    ↓
core view
    ↓
analytics mart
```

## Implemented Layers

### 1. Raw layer

Source data stored as JSON in S3.

Example location:

`s3://joaofonseca-data-platform/raw/github_events/`

### 2. Staging layer

Flattened nested JSON fields such as:

- `actor.login` → `actor_login`
- `repo.name` → `repo_name`

### 3. Core layer

Normalized and typed fields:

- `event_id`
- `event_type`
- `actor_login`
- `repo_name`
- `event_ts`

### 4. Mart layer

Analytical aggregation example:

- `mart_events_by_type`

## Example SQL Pattern

```sql
SELECT
    event_type,
    COUNT(*) AS total_events
FROM github_events_core
GROUP BY event_type;
```

## Skills Demonstrated

- Data lake architecture
- Schema-on-read querying
- JSON flattening in SQL
- Type normalization
- Layered analytical modeling
- AWS-based cloud data workflows

## Roadmap

Planned next steps:

- Python ingestion pipeline from GitHub API
- Partitioned S3 layout
- Data quality checks
- Automated ingestion workflow
- Portfolio-ready documentation and screenshots

## Purpose

This project is designed to strengthen a portfolio for **Data Engineer** and **Analytics Engineer** roles by demonstrating practical cloud data engineering patterns used in modern data platforms.
