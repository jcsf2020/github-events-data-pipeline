CREATE OR REPLACE VIEW github_events_core AS
SELECT CAST(id AS bigint) AS event_id,
    type AS event_type,
    actor_login,
    repo_name,
    CAST(from_iso8601_timestamp(created_at) AS timestamp) AS event_ts
FROM github_events_staging;