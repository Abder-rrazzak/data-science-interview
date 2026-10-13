"""Reproducible statistical inference on public or synthetic measurements."""
from __future__ import annotations

import numpy as np
from scipy import stats


def _sample(values, min_size: int = 2) -> np.ndarray:
    """Validate one-dimensional finite numeric observations without silent deletion."""
    a = np.asarray(values, dtype=float)
    if a.ndim != 1 or len(a) < min_size or not np.isfinite(a).all():
        raise ValueError(f"Expected >= {min_size} finite numeric observations in 1D")
    return a


def describe(values) -> dict:
    """Descriptive statistics; sample variance uses ddof=1."""
    x = _sample(values)
    return {"n": int(x.size), "mean": float(x.mean()), "median": float(np.median(x)),
            "sample_std": float(x.std(ddof=1)), "q25": float(np.quantile(x, .25)),
            "q75": float(np.quantile(x, .75))}


def mean_confidence_interval(values, confidence: float = .95) -> dict:
    """Two-sided Student-t CI for mean of independent observations."""
    x = _sample(values)
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    se = x.std(ddof=1) / np.sqrt(x.size)
    margin = stats.t.ppf((1 + confidence) / 2, x.size - 1) * se
    return {"estimate": float(x.mean()), "lower": float(x.mean() - margin),
            "upper": float(x.mean() + margin), "confidence": confidence,
            "method": "Student-t mean CI; assumes independent observations"}


def welch_test(x, y, alpha: float = .05) -> dict:
    """Two-sided unequal-variance t-test with Welch-Satterthwaite CI."""
    a, b = _sample(x), _sample(y)
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    if va + vb == 0:
        raise ValueError("Both samples have zero variance")
    dof = (va + vb)**2 / (va**2 / (len(a) - 1) + vb**2 / (len(b) - 1))
    diff = a.mean() - b.mean()
    margin = stats.t.ppf(1 - alpha / 2, dof) * np.sqrt(va + vb)
    p = stats.ttest_ind(a, b, equal_var=False).pvalue
    return {"mean_difference": float(diff), "p_value": float(p),
            "ci_lower": float(diff - margin), "ci_upper": float(diff + margin),
            "degrees_of_freedom": float(dof), "reject_null": bool(p < alpha),
            "method": "Welch independent-samples t-test"}


def paired_test(before, after) -> dict:
    """Paired t-test; observations must be aligned by subject."""
    a, b = _sample(before), _sample(after)
    if len(a) != len(b):
        raise ValueError("Paired samples must have equal length")
    differences = b - a
    if differences.std(ddof=1) == 0:
        raise ValueError("Paired differences have zero variance")
    t, p = stats.ttest_rel(b, a)
    return {"mean_change": float(differences.mean()), "t_statistic": float(t),
            "p_value": float(p), "n_pairs": int(len(a))}


def bootstrap_mean_ci(values, confidence: float = .95, n_resamples: int = 3000,
                      seed: int = 42) -> dict:
    """Percentile bootstrap CI; independent identically distributed sample assumption."""
    x = _sample(values)
    if not 0 < confidence < 1 or n_resamples < 100:
        raise ValueError("Invalid confidence or n_resamples (<100)")
    rng = np.random.default_rng(seed)
    means = np.empty(n_resamples)
    for i in range(n_resamples):
        means[i] = rng.choice(x, size=len(x), replace=True).mean()
    low, high = np.quantile(means, [(1-confidence)/2, (1+confidence)/2])
    return {"estimate": float(x.mean()), "lower": float(low), "upper": float(high),
            "n_resamples": n_resamples, "seed": seed}


def permutation_mean_test(x, y, n_resamples: int = 4000, seed: int = 42) -> dict:
    """Two-sided randomization test of mean difference under exchangeability."""
    a, b = _sample(x), _sample(y)
    if n_resamples < 100:
        raise ValueError("n_resamples must be >= 100")
    observed = abs(a.mean() - b.mean())
    pool = np.concatenate([a, b])
    rng = np.random.default_rng(seed)
    extreme = 0
    for _ in range(n_resamples):
        perm = rng.permutation(pool)
        extreme += abs(perm[:len(a)].mean() - perm[len(a):].mean()) >= observed - 1e-12
    return {"observed_abs_difference": float(observed),
            "p_value": float((extreme + 1) / (n_resamples + 1)),
            "n_resamples": n_resamples, "seed": seed}


def linear_regression_diagnostics(x, y) -> dict:
    """Simple OLS regression and residual diagnostics; association not causation."""
    a, b = _sample(x, 3), _sample(y, 3)
    if len(a) != len(b) or a.std() == 0:
        raise ValueError("Equal length and nonconstant predictor required")
    fit = stats.linregress(a, b)
    residual = b - (fit.intercept + fit.slope * a)
    return {"slope": float(fit.slope), "intercept": float(fit.intercept),
            "r_squared": float(fit.rvalue**2), "p_value_slope": float(fit.pvalue),
            "residual_rmse": float(np.sqrt(np.mean(residual**2))),
            "n": int(len(a))}


def monte_carlo_sum_uncertainty(means, stds, n_simulations: int = 10000,
                                seed: int = 42) -> dict:
    """Independent normal-input sum model; assumptions are illustrative."""
    mu, sigma = _sample(means), _sample(stds)
    if len(mu) != len(sigma) or (sigma < 0).any() or n_simulations < 100:
        raise ValueError("Means/stds must match; stds nonnegative; simulations >=100")
    rng = np.random.default_rng(seed)
    draws = rng.normal(mu, sigma, size=(n_simulations, len(mu))).sum(axis=1)
    low, high = np.quantile(draws, [.025, .975])
    return {"mean": float(draws.mean()), "lower_95": float(low),
            "upper_95": float(high), "seed": seed, "n_simulations": n_simulations}
