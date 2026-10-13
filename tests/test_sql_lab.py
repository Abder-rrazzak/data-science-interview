from pathlib import Path
import pytest
duckdb = pytest.importorskip("duckdb")
import pytest
from decision_intelligence.data import generate_events

ROOT = Path(__file__).resolve().parents[1]
QUERIES = sorted((ROOT / "sql" / "interview").glob("*/solution.sql"))

@pytest.mark.parametrize("query_file", QUERIES, ids=lambda p: p.parent.name)
def test_sql_solution(query_file):
    with duckdb.connect(":memory:") as con:
        con.register("events_frame", generate_events(400, seed=7))
        con.execute("CREATE VIEW events AS SELECT * FROM events_frame")
        result = con.execute(query_file.read_text(encoding="utf-8")).fetchdf()
        assert len(result) > 0
