SELECT region, AVG(measurement) AS avg_measurement, DENSE_RANK() OVER (ORDER BY AVG(measurement) DESC) AS rnk FROM events GROUP BY region;
