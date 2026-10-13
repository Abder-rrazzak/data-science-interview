WITH scored AS (SELECT *, AVG(measurement) OVER (PARTITION BY region) AS region_mean FROM events) SELECT event_id, region, measurement FROM scored WHERE measurement > region_mean;
