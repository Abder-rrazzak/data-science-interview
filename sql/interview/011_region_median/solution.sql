SELECT region, MEDIAN(measurement) AS median_measurement FROM events GROUP BY region ORDER BY region;
