SELECT source_id, AVG(measurement) AS mean_measurement FROM events GROUP BY source_id ORDER BY source_id;
