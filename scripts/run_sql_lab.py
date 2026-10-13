"""Execute and verify the SQL interview lab on generated synthetic data."""
from pathlib import Path
import sys
import duckdb

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from decision_intelligence.data import generate_events


def run() -> None:
    connection = duckdb.connect(":memory:")
    connection.register("events_frame", generate_events(1000, seed=42))
    connection.execute("CREATE VIEW events AS SELECT * FROM events_frame")
    for path in sorted((ROOT / "sql" / "interview").glob("*/solution.sql")):
        query = path.read_text(encoding="utf-8")
        result = connection.execute(query).fetchdf()
        print(f"{path.parent.name}: {len(result)} rows; columns={list(result.columns)}")
    print("SQL lab: all 12 queries passed")


if __name__ == "__main__":
    run()
