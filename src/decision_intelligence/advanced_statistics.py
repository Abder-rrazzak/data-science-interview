"""Advanced inference and regression diagnostics on synthetic/public data."""
from __future__ import annotations
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss


def _numeric(values, minimum=3):
    a = np.asarray(values, dtype=float)
    if a.ndim != 1 or len(a) < minimum or not np.isfinite(a).all():
        raise ValueError(f"Expected at least {minimum} finite 1-D observations")
    return a


def one_way_anova(groups: dict[str, list[float] | np.ndarray]) -> dict:
    """Classical one-way ANOVA; requires independent errors and equal group variances."""
    if len(groups) < 2:
        raise ValueError('At least two groups required')
    samples = [_numeric(v) for v in groups.values()]
    if any(np.var(a, ddof=1) == 0 for a in samples):
        raise ValueError('Each group must have nonzero variance')
    result = stats.f_oneway(*samples)
    grand = np.concatenate(samples).mean()
    between = sum(len(a) * (a.mean() - grand)**2 for a in samples)
    total = sum(((a - grand)**2).sum() for a in samples)
    return {'f_statistic': float(result.statistic), 'p_value': float(result.pvalue),
            'eta_squared': float(between / total), 'group_sizes': {k: len(v) for k,v in groups.items()},
            'assumptions': 'Independent observations, approximately normal residuals, equal variances'}


def chi_square_independence(table) -> dict:
    """Pearson chi-square association test; check expected counts before interpreting."""
    a = np.asarray(table, dtype=float)
    if a.ndim != 2 or min(a.shape) < 2 or not np.isfinite(a).all() or (a < 0).any() or not np.all(a == np.floor(a)):
        raise ValueError('Expected a 2D contingency table of nonnegative integer counts')
    if np.any(a.sum(axis=0) == 0) or np.any(a.sum(axis=1) == 0):
        raise ValueError('Empty row or column')
    chi2, p, dof, expected = stats.chi2_contingency(a, correction=False)
    n = a.sum()
    v = np.sqrt(chi2 / (n * min(a.shape[0]-1, a.shape[1]-1)))
    return {'chi_square': float(chi2), 'p_value': float(p), 'dof': int(dof),
            'min_expected': float(expected.min()), 'expected_below_5': int((expected < 5).sum()),
            'cramers_v': float(v), 'warning': 'Small expected counts: consider exact/Monte Carlo alternative' if (expected < 5).any() else None}


def multiple_ols(X, y, feature_names=None) -> dict:
    """OLS using matrix algebra, standard errors, VIF and Breusch-Pagan LM test.

    Inference relies on independent errors, correct specification and appropriate variance assumptions.
    """
    x = np.asarray(X, dtype=float)
    target = _numeric(y, 5)
    if x.ndim != 2 or x.shape[0] != len(target) or not np.isfinite(x).all():
        raise ValueError('X must be finite 2-D and match y rows')
    n,k = x.shape
    if n <= k+1 or k < 1:
        raise ValueError('Require n > predictors + intercept and >=1 predictor')
    design = np.column_stack([np.ones(n), x])
    if np.linalg.matrix_rank(design) != k+1:
        raise ValueError('Design matrix is rank deficient')
    names = list(feature_names) if feature_names is not None else [f'x{i+1}' for i in range(k)]
    if len(names) != k:
        raise ValueError('Feature names length mismatch')
    beta = np.linalg.lstsq(design, target, rcond=None)[0]
    fitted = design @ beta
    residual = target - fitted
    rss = residual @ residual
    tss = ((target-target.mean())**2).sum()
    dof = n-k-1
    sigma2 = rss/dof
    cov = sigma2 * np.linalg.inv(design.T@design)
    se = np.sqrt(np.diag(cov))
    tvals = np.divide(beta,se,out=np.full_like(beta,np.nan),where=se>0)
    pvals = 2*stats.t.sf(np.abs(tvals),dof)
    vif = {}
    for i,name in enumerate(names):
        other = np.delete(x,i,axis=1)
        z = np.column_stack([np.ones(n),other])
        ri = x[:,i]-z@np.linalg.lstsq(z,x[:,i],rcond=None)[0]
        ti = ((x[:,i]-x[:,i].mean())**2).sum()
        vif[name] = float(ti/(ri@ri)) if ri@ri>1e-12 else float('inf')
    # Breusch-Pagan auxiliary regression of squared residuals on original predictors.
    sq = residual**2
    aux = design@np.linalg.lstsq(design,sq,rcond=None)[0]
    denom = ((sq-sq.mean())**2).sum()
    r2_aux = max(0., 1-((sq-aux)**2).sum()/denom) if denom>0 else 0.
    bp_lm = n*r2_aux
    return {'coefficients': dict(zip(['intercept']+names,map(float,beta))),
            'standard_errors': dict(zip(['intercept']+names,map(float,se))),
            'p_values': dict(zip(['intercept']+names,map(float,pvals))),
            'r_squared': float(1-rss/tss) if tss>0 else float('nan'),
            'adjusted_r_squared': float(1-(rss/dof)/(tss/(n-1))) if tss>0 else float('nan'),
            'rmse': float(np.sqrt(np.mean(residual**2))), 'vif': vif,
            'breusch_pagan_lm': float(bp_lm), 'breusch_pagan_p_value': float(stats.chi2.sf(bp_lm,k)),
            'n': n, 'residuals': residual.tolist(), 'fitted': fitted.tolist(),
            'caveat': 'Coefficient p-values assume homoscedastic independent errors; association does not prove causality.'}


def logistic_regression_demo(X,y,seed=42) -> dict:
    """Fit an illustrative logistic classifier and report in-sample metrics (NOT test metrics)."""
    x = np.asarray(X,dtype=float)
    target = np.asarray(y)
    if x.ndim!=2 or x.shape[0]!=len(target) or not np.isfinite(x).all() or set(np.unique(target))!={0,1}:
        raise ValueError('Finite X and binary y with both classes required')
    if min(np.bincount(target.astype(int)))<3:
        raise ValueError('At least three samples per class')
    model = LogisticRegression(max_iter=1000,random_state=seed)
    model.fit(x,target)
    probabilities = model.predict_proba(x)[:,1]
    return {'coefficients': model.coef_[0].tolist(), 'intercept': float(model.intercept_[0]),
            'train_auc': float(roc_auc_score(target,probabilities)),
            'train_log_loss': float(log_loss(target,probabilities)),
            'warning': 'Training metrics are optimistic. Use holdout/cross-validation for evaluation; scale and encode inside a Pipeline.'}
