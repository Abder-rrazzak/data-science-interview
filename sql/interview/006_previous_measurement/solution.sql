SELECT event_id, region, measurement, LAG(measurement) OVER (PARTITION BY region ORDER BY timestamp, event_id) AS previous_measurement FROM events;
