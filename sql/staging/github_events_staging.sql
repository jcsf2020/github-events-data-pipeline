CREATE OR REPLACE VIEW github_events_partitioned_staging AS
SELECT
    id,
    type,
    actor.login AS actor_login,
    repo.name AS repo_name,
    created_at,
    year,
    month,
    day
FROM github_events_partitioned;
