# Phase 6 — Advanced Uncertainty Quantification

All examples use **synthetic** observations. Run `python scripts/run_uncertainty_lab.py` after `pip install -e ".[dev]"`.

## Core concepts and assumptions

| Method | What it quantifies | Key assumption / limitation |
|---|---|---|
| Percentile bootstrap | Sampling uncertainty in a mean | Observations are iid; can under-cover for skewed/small samples |
| OLS mean confidence interval | Uncertainty about conditional expected response | Linear, independent, homoscedastic normal residuals for exact t coverage |
| OLS prediction interval | Uncertainty about an individual future response | Includes irreducible residual variation; typically wider than mean CI |
| Beta-binomial credible interval | Posterior uncertainty in a Bernoulli probability | Prior Beta(a,b) and conditionally iid Bernoulli observations |
| Correlated Monte Carlo | Propagated measurement uncertainty | Input distributions/correlation are specified correctly; Monte Carlo error |
| One-at-a-time sensitivity | Local dependence on individual assumptions | Does not capture interactions or correlations |
| Scenario decision analysis | Expected and lower-tail payoff | Scenario probabilities and payoffs are subjective inputs, not facts |

**Confidence interval vs credible interval:** A frequentist 95% confidence interval is a procedure with 95% long-run coverage under its assumptions. A 95% Bayesian credible interval contains 95% posterior probability conditional on the chosen prior and likelihood. Neither means the model itself is 95% likely to be correct.

**Prediction interval vs confidence interval:** A prediction interval for an individual future observation includes observation noise. A confidence interval for the conditional mean does not.

**Correlated inputs:** Ignoring positive correlation can underestimate total uncertainty. Compare the simulated standard deviation with the analytical formula `sqrt(w.T @ covariance @ w)`.

**Decision analysis:** High expected payoff can conceal a severe downside. Report both expected payoff and lower-tail payoff, plus sensitivity to scenario probabilities. These examples do not estimate real-world threats.

## Guided practice

1. Increase bootstrap resamples from 1,000 to 10,000; compare CI stability over different random seeds. Explain Monte Carlo error versus sampling error.
2. Use `linear_prediction_interval` for points within and beyond the observed x-range. Explain extrapolation risk.
3. Change the Beta prior from `(1,1)` to `(20,20)` with 10 observations, then with 1,000 observations. Describe prior influence.
4. Set correlation to `0`, `0.8`, then `-0.8`; compare analytical and simulated uncertainty.
5. Reverse the scenario probabilities in `compare_decisions`; explain whether the preferred action changes.
6. Add a new uncertain input to the sensitivity model and state why one-at-a-time analysis may miss interactions.

## Senior interview questions and concise model answers

**Q1. How do you quantify uncertainty in an analytical conclusion?** Separate measurement, sampling, parameter, model and scenario uncertainty. Use appropriate intervals, diagnostics, sensitivity checks, and independent validation. State what is not quantified.

**Q2. Confidence interval versus prediction interval?** A CI quantifies uncertainty in the estimated conditional mean; a PI predicts a future observation and includes residual variability.

**Q3. When is bootstrap unreliable?** Very small samples, strong dependence without block resampling, nonrepresentative samples, or nonsmooth statistics can invalidate naive iid percentile bootstrap.

**Q4. What does a Bayesian credible interval mean?** Conditional on the likelihood, prior, and observed data, the posterior probability of the parameter lying in the interval equals the specified credibility level.

**Q5. How would you communicate uncertainty to executives?** Present the central estimate, plausible range, major assumptions, downside scenarios, and which decision remains robust when assumptions change.

**Q6. Why model correlation in Monte Carlo?** Dependence affects the variance of aggregates; independent draws can severely distort the risk estimate.

**Q7. What is a model risk you cannot solve by increasing simulation draws?** Incorrect distributional assumptions, omitted variables, biased inputs, or structural model error.

**Q8. How do you prioritize analyses under uncertain inputs?** Identify decisions that are sensitive to uncertain assumptions and target additional data collection where it has the greatest potential decision value.

## Validation checklist

- Validate sample units, independence, and missingness.
- State exact estimand, coverage/credibility, model assumptions, and sample size.
- Use fixed seeds for reproducibility; vary seeds to assess simulation stability.
- Distinguish statistical from practical importance.
- Never infer causality from descriptive associations alone.
- Do not present synthetic results as actual mission findings.
