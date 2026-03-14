-- total rows
SELECT COUNT(*) AS total_rows
FROM github_events_partitioned_core;
-- null checks
SELECT COUNT(*) AS total_rows,
    COUNT(event_id) AS non_null_event_id,
    COUNT(event_type) AS non_null_event_type,
    COUNT(event_ts) AS non_null_event_ts
FROM github_events_partitioned_core;
-- duplicate event_id check
SELECT event_id,
    COUNT(*) AS occurrences
FROM github_events_partitioned_core
GROUP BY event_id
HAVING COUNT(*) > 1;
-- freshness check
SELECT MAX(event_ts) AS latest_event_ts
FROM github_events_partitioned_core;