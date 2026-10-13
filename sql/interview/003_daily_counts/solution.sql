SELECT CAST(timestamp AS DATE) AS day, COUNT(*) AS n FROM events GROUP BY day ORDER BY day;
