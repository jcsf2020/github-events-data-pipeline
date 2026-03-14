-- Row count
SELECT COUNT(*) AS total_rows
FROM github_events_core;
-- Null checks
SELECT COUNT(*) AS total_rows,
    COUNT(event_id) AS non_null_event_id,
    COUNT(event_type) AS non_null_event_type,
    COUNT(event_ts) AS non_null_event_ts
FROM github_events_core;
-- Duplicate event_id check
SELECT event_id,
    COUNT(*) AS occurrences
FROM github_events_core
GROUP BY event_id
HAVING COUNT(*) > 1;
-- Event type distribution
SELECT event_type,
    COUNT(*) AS total_events
FROM github_events_core
GROUP BY event_type
ORDER BY total_events DESC;