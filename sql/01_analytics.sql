-- DuckDB-compatible example. Create a view after generating data.
CREATE OR REPLACE VIEW events AS SELECT * FROM read_csv_auto('data/generated/events.csv');
-- 1. Daily counts by region
SELECT region, CAST(timestamp AS DATE) AS day, COUNT(*) AS event_count
FROM events GROUP BY region, day ORDER BY region, day;
-- 2. Top 3 days by activity in each region
WITH daily AS (
  SELECT region, CAST(timestamp AS DATE) AS day, COUNT(*) AS n
  FROM events GROUP BY region, day
), ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY region ORDER BY n DESC, day) AS rn
  FROM daily
)
SELECT region, day, n FROM ranked WHERE rn <= 3 ORDER BY region, rn;
-- 3. Running regional average (observation-order, not 30 calendar days)
SELECT region, timestamp, measurement,
 AVG(measurement) OVER (PARTITION BY region ORDER BY timestamp, event_id
 ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS last_30_observations_mean
FROM events ORDER BY region, timestamp, event_id;
