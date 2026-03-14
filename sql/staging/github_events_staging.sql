CREATE OR REPLACE VIEW github_events_staging AS
SELECT id,
    type,
    actor.login AS actor_login,
    repo.name AS repo_name,
    created_at
FROM github_events;