"""Run reproducible synthetic examples from the Phase 3 statistics laboratory."""
import json
import numpy as np
from decision_intelligence.statistics_lab import (
    describe, mean_confidence_interval, welch_test, paired_test,
    bootstrap_mean_ci, permutation_mean_test, linear_regression_diagnostics,
    monte_carlo_sum_uncertainty,
)

def main():
    rng = np.random.default_rng(2026)
    a = rng.normal(50, 10, 100)
    b = rng.normal(53, 12, 110)
    baseline = rng.normal(20, 3, 60)
    followup = baseline + rng.normal(1.5, 2, 60)
    outputs = {
        "descriptive": describe(a), "mean_ci": mean_confidence_interval(a),
        "welch": welch_test(a, b), "paired": paired_test(baseline, followup),
        "bootstrap": bootstrap_mean_ci(a),
        "permutation": permutation_mean_test(a, b),
        "regression": linear_regression_diagnostics(np.arange(30), np.arange(30) * 1.5 + rng.normal(0, 3, 30)),
        "monte_carlo": monte_carlo_sum_uncertainty([20, 30, 15], [2, 4, 3]),
    }
    print(json.dumps(outputs, indent=2))

if __name__ == "__main__":
    main()
