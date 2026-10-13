import argparse
import json
from pathlib import Path
import pandas as pd
from decision_intelligence.analysis import compare_regions
from decision_intelligence.model import score_anomalies

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="data/generated/events.csv")
    p.add_argument("--output", default="artifacts/analysis.json")
    args = p.parse_args()
    df = pd.read_csv(args.input)
    report = compare_regions(df)
    report["anomalies_detected"] = int(score_anomalies(df).is_anomaly.sum())
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
