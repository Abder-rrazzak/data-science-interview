# SQL 005 — Top 3 busiest days per region

Dataset: `events(event_id, timestamp, region, measurement, source_id)` from `scripts/generate_data.py`.

Write a DuckDB-compatible query. Compare your result with `solution.sql`.

**Performance note:** filtering early, choosing appropriate partitions and inspecting `EXPLAIN` matter at scale.
