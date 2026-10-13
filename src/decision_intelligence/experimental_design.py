"""Reproducible randomized experiment design and evaluation for synthetic data.

Educational examples: no claim of causal identification without actual random assignment.
"""
from __future__ import annotations
import numpy as np
from scipy import stats
from scipy.stats import norm


def _vector(values, minimum=2):
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or len(x) < minimum or not np.isfinite(x).all():
        raise ValueError(f"Expected >= {minimum} finite one-dimensional values")
    return x


def random_assignment(n: int, treatment_fraction: float = 0.5, seed: int = 42) -> np.ndarray:
    """Complete randomization with a fixed number of treated units."""
    if not isinstance(n, int) or n < 4 or not 0 < treatment_fraction < 1:
        raise ValueError("n must be >=4 and treatment_fraction strictly between 0 and 1")
    k = round(n * treatment_fraction)
    if k < 2 or n-k < 2:
        raise ValueError("Both groups must contain at least two units")
    rng = np.random.default_rng(seed)
    labels = np.zeros(n, dtype=int)
    labels[rng.choice(n, size=k, replace=False)] = 1
    return labels


def stratified_assignment(strata, seed: int = 42) -> np.ndarray:
    """Randomize approximately half within each stratum; require >=4 per stratum."""
    groups = np.asarray(strata)
    if groups.ndim != 1 or len(groups) < 4:
        raise ValueError("Expected one-dimensional strata")
    rng = np.random.default_rng(seed)
    assignment = np.zeros(len(groups), dtype=int)
    for group in np.unique(groups):
        idx = np.flatnonzero(groups == group)
        if len(idx) < 4:
            raise ValueError("Each stratum must have at least four units")
        assignment[rng.choice(idx, size=len(idx)//2, replace=False)] = 1
    return assignment


def sample_size_two_means(effect: float, std: float, alpha: float = .05,
                          power: float = .8, allocation_ratio: float = 1.) -> dict:
    """Normal-approximation sample size for a two-sided, two-arm mean difference.

    allocation_ratio is n_treatment / n_control; assumes common known SD.
    """
    if not np.isfinite([effect,std,alpha,power,allocation_ratio]).all() or effect == 0 or std <= 0 or not 0 < alpha < 1 or not 0 < power < 1 or allocation_ratio <= 0:
        raise ValueError("Invalid effect, SD, alpha, power or allocation ratio")
    z = norm.ppf(1-alpha/2) + norm.ppf(power)
    control = int(np.ceil(z*z*std*std*(1+1/allocation_ratio)/(effect*effect)))
    treated = int(np.ceil(control*allocation_ratio))
    return {'n_control': max(control,2), 'n_treatment': max(treated,2),
            'n_total': max(control,2)+max(treated,2),
            'assumptions': 'Normal approximation, independent observations, common SD, two-sided test; confirm using simulation or exact power.'}


def ab_test(treatment, control, alpha: float = .05) -> dict:
    """Welch test, confidence interval, Cohen d and practical-effect estimate."""
    a,b = _vector(treatment),_vector(control)
    if not 0 < alpha < 1:
        raise ValueError('alpha must lie between 0 and 1')
    va,vb = a.var(ddof=1),b.var(ddof=1)
    if va == 0 and vb == 0:
        raise ValueError('At least one group must have nonzero variance')
    se2 = va/len(a)+vb/len(b)
    dof = se2**2 / ((va/len(a))**2/(len(a)-1)+(vb/len(b))**2/(len(b)-1))
    diff = float(a.mean()-b.mean())
    half = stats.t.ppf(1-alpha/2,dof)*np.sqrt(se2)
    pooled = np.sqrt(((len(a)-1)*va+(len(b)-1)*vb)/(len(a)+len(b)-2))
    return {'difference':diff,'p_value':float(stats.ttest_ind(a,b,equal_var=False).pvalue),
            'confidence_interval':[float(diff-half),float(diff+half)],
            'cohens_d':float(diff/pooled) if pooled>0 else None,
            'n_treatment':len(a),'n_control':len(b),
            'warning':'A low p-value does not establish practical significance; causal interpretation requires valid randomization.'}


def adjust_pvalues(pvalues, method: str = 'holm') -> list[float]:
    """Control familywise error (Bonferroni/Holm) or FDR (Benjamini-Hochberg)."""
    p = _vector(pvalues,1)
    if np.any((p<0)|(p>1)):
        raise ValueError('p-values must be in [0,1]')
    m=len(p)
    if method == 'bonferroni':
        return np.minimum(1,p*m).tolist()
    order=np.argsort(p,kind='stable')
    sorted_p=p[order]
    if method == 'holm':
        adjusted=np.maximum.accumulate(sorted_p*(m-np.arange(m)))
    elif method == 'fdr_bh':
        adjusted=np.minimum.accumulate((sorted_p*m/(np.arange(m)+1))[::-1])[::-1]
    else:
        raise ValueError('method must be bonferroni, holm or fdr_bh')
    result=np.empty(m)
    result[order]=np.minimum(1,adjusted)
    return result.tolist()


def standardized_mean_difference(treatment_covariate, control_covariate) -> float:
    """Baseline covariate balance diagnostic; values near zero indicate balance."""
    a,b=_vector(treatment_covariate),_vector(control_covariate)
    pooled=np.sqrt((a.var(ddof=1)+b.var(ddof=1))/2)
    if pooled == 0:
        return 0. if a.mean()==b.mean() else float('inf')
    return float((a.mean()-b.mean())/pooled)


def simulate_experiment(n: int = 500, effect: float = 0.4, seed: int = 42) -> dict:
    """Illustrative synthetic randomized experiment with reproducible potential outcomes."""
    if not np.isfinite(effect):
        raise ValueError('effect must be finite')
    rng=np.random.default_rng(seed)
    baseline=rng.normal(10,2,size=n)
    assignment=random_assignment(n,seed=seed)
    observed=baseline+effect*assignment+rng.normal(0,1,size=n)
    outcome=ab_test(observed[assignment==1],observed[assignment==0])
    outcome['true_simulated_effect']=effect
    outcome['baseline_smd']=standardized_mean_difference(baseline[assignment==1],baseline[assignment==0])
    return outcome
