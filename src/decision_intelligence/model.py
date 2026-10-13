"""Simple reproducible anomaly baseline; no threat inference."""
import pandas as pd
from sklearn.ensemble import IsolationForest

def score_anomalies(df: pd.DataFrame, contamination: float = 0.05, seed: int = 42) -> pd.DataFrame:
    if not 0 < contamination <= 0.5:
        raise ValueError("contamination must be in (0, 0.5]")
    if df["measurement"].isna().any():
        raise ValueError("measurement contains missing values")
    model = IsolationForest(contamination=contamination, random_state=seed)
    output = df.copy()
    values = output[["measurement"]]
    output["anomaly_score"] = -model.fit(values).score_samples(values)
    output["is_anomaly"] = model.predict(values) == -1
    return output
