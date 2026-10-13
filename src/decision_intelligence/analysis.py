"""Transparent statistical inference for a synthetic two-region comparison."""
import numpy as np
import pandas as pd
from scipy import stats

def compare_regions(df: pd.DataFrame, a: str = "North", b: str = "South") -> dict:
    required = {"region", "measurement"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {required - set(df.columns)}")
    x = pd.to_numeric(df.loc[df.region == a, "measurement"], errors="coerce").dropna().to_numpy()
    y = pd.to_numeric(df.loc[df.region == b, "measurement"], errors="coerce").dropna().to_numpy()
    if len(x) < 2 or len(y) < 2:
        raise ValueError("Each region requires at least two valid observations")
    result = stats.ttest_ind(x, y, equal_var=False)
    difference = float(x.mean() - y.mean())
    se = float(np.sqrt(x.var(ddof=1) / len(x) + y.var(ddof=1) / len(y)))
    v1, v2 = x.var(ddof=1) / len(x), y.var(ddof=1) / len(y)
    dof = float((v1 + v2)**2 / (v1**2 / (len(x) - 1) + v2**2 / (len(y) - 1))) if v1 + v2 > 0 else float("inf")
    critical = float(stats.t.ppf(0.975, dof))
    return {"region_a": a, "region_b": b, "n_a": len(x), "n_b": len(y),
            "mean_difference": difference, "p_value": float(result.pvalue),
            "ci95_lower": difference - critical * se, "ci95_upper": difference + critical * se,
            "method": "Welch two-sample t-test; descriptive synthetic example"}
