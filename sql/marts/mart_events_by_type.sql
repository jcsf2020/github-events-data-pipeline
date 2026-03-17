CREATE OR REPLACE VIEW mart_events_by_type AS
SELECT event_type,
    COUNT(*) AS total_events
FROM github_events_partitioned_core
GROUP BY event_type;