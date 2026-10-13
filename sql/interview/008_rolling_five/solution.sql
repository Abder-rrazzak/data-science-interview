SELECT event_id, region, AVG(measurement) OVER (PARTITION BY region ORDER BY timestamp, event_id ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_mean FROM events;
