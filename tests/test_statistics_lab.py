import numpy as np
import pytest
from decision_intelligence.statistics_lab import (
    describe, mean_confidence_interval, welch_test, paired_test,
    bootstrap_mean_ci, permutation_mean_test, linear_regression_diagnostics,
    monte_carlo_sum_uncertainty,
)


def test_describe_sample_sd():
    result = describe([1, 2, 3, 4, 5])
    assert result["n"] == 5
    assert result["mean"] == 3
    assert result["sample_std"] == pytest.approx(np.sqrt(2.5))


def test_mean_ci_contains_mean():
    result = mean_confidence_interval([1, 2, 3, 4, 5])
    assert result["lower"] < 3 < result["upper"]


def test_welch_detects_clear_difference():
    rng = np.random.default_rng(1)
    a, b = rng.normal(0, 1, 200), rng.normal(2, 1, 200)
    result = welch_test(a, b)
    assert result["p_value"] < .001
    assert result["ci_upper"] < 0


def test_welch_rejects_invalid():
    with pytest.raises(ValueError):
        welch_test([1, 1], [2, 2])


def test_paired_detects_improvement():
    rng = np.random.default_rng(2)
    before = rng.normal(5, 1, 80)
    after = before + rng.normal(1, .3, 80)
    assert paired_test(before, after)["p_value"] < .001


def test_paired_length_mismatch():
    with pytest.raises(ValueError):
        paired_test([1, 2], [1, 2, 3])


def test_bootstrap_reproducible():
    x = np.arange(20)
    assert bootstrap_mean_ci(x, seed=10) == bootstrap_mean_ci(x, seed=10)


def test_permutation_detects_difference():
    rng = np.random.default_rng(3)
    a, b = rng.normal(0, 1, 60), rng.normal(3, 1, 60)
    assert permutation_mean_test(a, b, 1000)["p_value"] < .01


def test_regression_known_line():
    x = np.arange(10)
    out = linear_regression_diagnostics(x, 2 * x + 3)
    assert out["slope"] == pytest.approx(2)
    assert out["r_squared"] == pytest.approx(1)


def test_monte_carlo_reproducible():
    a = monte_carlo_sum_uncertainty([5, 10], [1, 2], 500, 7)
    assert a == monte_carlo_sum_uncertainty([5, 10], [1, 2], 500, 7)
    assert a["lower_95"] < 15 < a["upper_95"]


def test_reject_nan():
    with pytest.raises(ValueError):
        describe([1, np.nan, 3])
