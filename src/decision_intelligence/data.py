"""Reproducible, entirely synthetic event and observation datasets."""
from pathlib import Path
import numpy as np
import pandas as pd

def generate_events(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    if n < 1:
        raise ValueError("n must be positive")
    rng = np.random.default_rng(seed)
    regions = rng.choice(["North", "South", "East", "West"], size=n)
    baseline = np.select([regions == "North", regions == "South", regions == "East"], [48, 55, 43], default=51)
    values = np.maximum(0, rng.normal(baseline, 9, n))
    return pd.DataFrame({
        "event_id": np.arange(1, n + 1),
        "timestamp": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
        "region": regions,
        "measurement": values.round(3),
        "source_id": rng.choice(["sensor_a", "sensor_b", "report_c"], size=n),
    }).sort_values(["timestamp", "event_id"]).reset_index(drop=True)

def save_events(path: str | Path, n: int = 1000, seed: int = 42) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    generate_events(n, seed).to_csv(destination, index=False)
    return destination
