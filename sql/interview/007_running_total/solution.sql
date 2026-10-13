SELECT event_id, region, SUM(measurement) OVER (PARTITION BY region ORDER BY timestamp, event_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total FROM events;
