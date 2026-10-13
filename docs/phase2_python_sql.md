# Phase 2 — Python, Pandas, NumPy and SQL practice

**Implemented:** 12 Python challenges with starter/solution/tests; 12 executable DuckDB SQL problems; a SQL runner; automated tests. This is an incremental milestone, not the requested 100/150 questions.

## Run locally (PowerShell)

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/run_sql_lab.py
```

## Verification note

The 12 Python reference tests passed in the build environment. DuckDB is not installed in that environment, so SQL integration tests are provided but could not be executed there. Install dependencies locally and run the SQL lab before relying on the results.

## Suggested learning loop

1. Read `python/coding_challenges/001_duplicates/problem.md`.
2. Implement `starter.py` without viewing `solution.py`.
3. Compare with the reference and inspect `test_solution.py`.
4. Read `sql/interview/005_top_three_days/problem.md`, write your SQL, then compare with `solution.sql`.
5. Run `scripts/run_sql_lab.py` to validate all queries.

**Research integrity:** SQL window frame `ROWS BETWEEN 4 PRECEDING` means five observations, not five calendar days. The examples are synthetic; significance testing requires additional statistical assumptions.
