"""Phase 6: reproducible uncertainty quantification using synthetic/public inputs.

Intervals have different meanings: confidence intervals estimate a population
parameter; prediction intervals describe a future observation; credible intervals
summarize posterior probability under a specified Bayesian model.
"""
from __future__ import annotations
import numpy as np
from scipy import stats


def bootstrap_mean_ci(values, confidence=.95, resamples=4000, seed=42):
    """Percentile bootstrap CI for the population mean (iid observations)."""
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or len(x) < 2 or not np.isfinite(x).all():
        raise ValueError('values must be a finite 1-D array with >=2 observations')
    if not 0 < confidence < 1 or resamples < 100:
        raise ValueError('confidence must be (0,1); resamples >= 100')
    rng = np.random.default_rng(seed)
    # Chunk to bound memory for large datasets.
    means = np.empty(resamples)
    for start in range(0, resamples, 250):
        end = min(start + 250, resamples)
        means[start:end] = rng.choice(x, size=(end-start, len(x)), replace=True).mean(axis=1)
    alpha = (1-confidence)/2
    lo, hi = np.quantile(means, [alpha, 1-alpha])
    return {'estimate':float(x.mean()),'lower':float(lo),'upper':float(hi),
            'confidence':confidence,'method':'iid percentile bootstrap'}


def linear_prediction_interval(x, y, x_new, confidence=.95):
    """OLS mean-response CI and individual-observation PI, with intercept.

    Assumes independent, homoscedastic Gaussian residuals and linear mean.
    """
    x, y = np.asarray(x,dtype=float), np.asarray(y,dtype=float)
    xn = np.atleast_1d(np.asarray(x_new,dtype=float))
    if x.ndim != 1 or y.ndim != 1 or len(x)!=len(y) or len(x)<3:
        raise ValueError('x and y must be equal-length 1-D arrays, n>=3')
    if not (np.isfinite(x).all() and np.isfinite(y).all() and np.isfinite(xn).all()):
        raise ValueError('inputs must be finite')
    if not 0 < confidence < 1 or np.var(x)==0:
        raise ValueError('invalid confidence or constant predictor')
    X=np.column_stack((np.ones(len(x)),x))
    Xn=np.column_stack((np.ones(len(xn)),xn))
    beta=np.linalg.lstsq(X,y,rcond=None)[0]
    residual=y-X@beta
    s2=float(residual@residual/(len(x)-2))
    cov=np.linalg.inv(X.T@X)
    h=np.einsum('ij,jk,ik->i',Xn,cov,Xn)
    predicted=Xn@beta
    t=stats.t.ppf((1+confidence)/2,df=len(x)-2)
    mean_margin=t*np.sqrt(s2*h)
    pred_margin=t*np.sqrt(s2*(1+h))
    return {'predicted':predicted.tolist(),
            'mean_ci_lower':(predicted-mean_margin).tolist(),
            'mean_ci_upper':(predicted+mean_margin).tolist(),
            'prediction_lower':(predicted-pred_margin).tolist(),
            'prediction_upper':(predicted+pred_margin).tolist(),
            'residual_std':float(np.sqrt(s2)),'confidence':confidence}


def beta_binomial_posterior(successes, trials, prior_a=1., prior_b=1., credibility=.95):
    """Conjugate Beta posterior for iid Bernoulli observations."""
    if not (isinstance(successes,(int,np.integer)) and isinstance(trials,(int,np.integer)) and 0<=successes<=trials):
        raise ValueError('successes and trials must be integers with 0<=successes<=trials')
    if min(prior_a,prior_b)<=0 or not 0<credibility<1:
        raise ValueError('prior parameters must be positive; credibility in (0,1)')
    a=prior_a+successes; b=prior_b+trials-successes
    lo,hi=stats.beta.ppf([(1-credibility)/2,(1+credibility)/2],a,b)
    return {'posterior_mean':float(a/(a+b)),'credible_lower':float(lo),
            'credible_upper':float(hi),'posterior_alpha':float(a),
            'posterior_beta':float(b),'credibility':credibility}


def correlated_monte_carlo(means, stds, correlation, weights, draws=20000, seed=42):
    """Propagate correlated Gaussian measurement uncertainty to weighted sum."""
    m=np.asarray(means,dtype=float); s=np.asarray(stds,dtype=float)
    c=np.asarray(correlation,dtype=float); w=np.asarray(weights,dtype=float)
    n=len(m)
    if n==0 or any(v.shape!=(n,) for v in (s,w)) or c.shape!=(n,n):
        raise ValueError('dimension mismatch')
    if not (np.isfinite(m).all() and np.isfinite(s).all() and np.isfinite(c).all() and np.isfinite(w).all()):
        raise ValueError('all inputs must be finite')
    if (s<0).any() or not np.allclose(c,c.T,atol=1e-10) or not np.allclose(np.diag(c),1):
        raise ValueError('stds must be nonnegative; correlation must be symmetric with unit diagonal')
    if np.linalg.eigvalsh(c).min() < -1e-10 or draws<100:
        raise ValueError('correlation must be positive semidefinite; draws>=100')
    cov=np.outer(s,s)*c
    rng=np.random.default_rng(seed)
    samples=rng.multivariate_normal(m,cov,size=draws,check_valid='raise')@w
    return {'mean':float(samples.mean()),'std':float(samples.std(ddof=1)),
            'p05':float(np.quantile(samples,.05)),'p50':float(np.median(samples)),
            'p95':float(np.quantile(samples,.95)),
            'analytical_mean':float(w@m),'analytical_std':float(np.sqrt(w@cov@w)),
            'draws':draws}


def one_at_a_time_sensitivity(base, ranges, model):
    """One-at-a-time sensitivity; ranges maps parameter -> (low, high)."""
    baseline=float(model(**base))
    output=[]
    for name,(low,high) in ranges.items():
        if name not in base or low>high:
            raise ValueError(f'invalid range for {name}')
        low_args={**base,name:low}; high_args={**base,name:high}
        low_y=float(model(**low_args)); high_y=float(model(**high_args))
        output.append({'parameter':name,'low_output':low_y,'high_output':high_y,
                       'swing':abs(high_y-low_y)})
    return {'baseline':baseline,'parameters':sorted(output,key=lambda r:r['swing'],reverse=True),
            'warning':'One-at-a-time ignores interactions and parameter dependence.'}


def compare_decisions(outcomes, probabilities, loss_fraction=.1):
    """Compare scenario payoffs: expected payoff and lower-tail expected payoff.

    outcomes maps action to one payoff per scenario; probabilities sum to 1.
    lower_tail_payoff is the probability-weighted mean of worst loss_fraction outcomes.
    """
    p=np.asarray(probabilities,dtype=float)
    if p.ndim!=1 or len(p)==0 or not np.isfinite(p).all() or (p<0).any() or not np.isclose(p.sum(),1):
        raise ValueError('probabilities must be nonnegative and sum to 1')
    if not 0<loss_fraction<=1:
        raise ValueError('loss_fraction must be in (0,1]')
    results={}
    for action,values in outcomes.items():
        v=np.asarray(values,dtype=float)
        if v.shape!=p.shape or not np.isfinite(v).all():
            raise ValueError(f'invalid payoffs for {action}')
        order=np.argsort(v); remaining=loss_fraction; weighted=0.
        for i in order:
            take=min(remaining,float(p[i])); weighted+=take*float(v[i]); remaining-=take
            if remaining<=1e-12: break
        results[action]={'expected_payoff':float(p@v),
                         'lower_tail_payoff':float(weighted/loss_fraction)}
    return results
