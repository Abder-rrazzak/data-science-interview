# Phase 3 — Statistics & Statistical Inference Lab

All examples are **synthetic**. Run `python scripts/run_statistics_lab.py` from an installed environment.

## What is implemented

| Technique | Function | Question it answers | Critical assumptions |
|---|---|---|---|
| Descriptive statistics | `describe` | What does the sample look like? | Sample SD uses `ddof=1` |
| Student-t CI | `mean_confidence_interval` | What range is plausible for a population mean? | Independent observations; approximate normality of sample mean |
| Welch t-test | `welch_test` | Do independent groups differ in their means? | Independent groups; does not assume equal variance |
| Paired t-test | `paired_test` | Did matched units change? | Matched observations; approximately normal differences |
| Percentile bootstrap | `bootstrap_mean_ci` | How variable is the sample mean? | IID sample; naive bootstrap is not for autocorrelated series |
| Permutation test | `permutation_mean_test` | Is the observed difference unusual under label exchangeability? | Exchangeability under the null |
| Simple OLS | `linear_regression_diagnostics` | What is the linear association? | Regression assumptions needed for inference; association != causation |
| Monte Carlo | `monte_carlo_sum_uncertainty` | How does input uncertainty propagate? | Independent normally distributed inputs |

## Guided practice

1. Generate 100 measurements in group A and 100 in group B, fixing a random seed.
2. Describe each group, inspect outliers, and draw histograms.
3. State H0 and H1 **before** running the Welch test.
4. Calculate the mean difference, p-value and 95% CI. Interpret effect size separately from statistical significance.
5. Repeat the analysis using the permutation test; explain why its assumptions differ.
6. Bootstrap a mean CI; compare it with the t interval. Do not interpret either as the probability that the fixed parameter lies in the observed interval.
7. Generate paired before/after measurements and explain why the paired test is more appropriate than treating them as independent.
8. Fit a linear regression and examine residuals before making any predictive claim.
9. Propagate measurement uncertainty through an additive Monte Carlo model; vary one input standard deviation.
10. Write a 100-word executive memo that distinguishes estimate, uncertainty, limitations and next steps.

## Interview prompts with concise model answers

**Q: What does a p-value mean?** Under the specified null model, it is the probability of observing a statistic at least as extreme as the one observed. It is not the probability that H0 is true.

**Q: When use Welch rather than Student's pooled t-test?** Welch allows unequal group variances and is a sound default for two independent means; still verify independence and sampling assumptions.

**Q: What is the difference between confidence and prediction intervals?** A confidence interval concerns a population parameter or conditional mean; a prediction interval concerns a future observation and is typically wider.

**Q: Why isn't significance sufficient?** With enough observations, trivial effects can be statistically significant. Report effect magnitude, interval, costs and practical importance.

**Q: How would you handle repeated measures?** Respect pairing or within-unit dependence using paired tests, mixed models, cluster-aware inference, or appropriate resampling.

**Q: How do you quantify uncertainty?** Distinguish sampling, measurement, parameter and model uncertainty. Use CIs, bootstrap, sensitivity analysis or simulation as appropriate; make assumptions explicit.

## Self-check

Run `python -m pytest tests/test_statistics_lab.py -q` and `python scripts/run_statistics_lab.py`. Verify actual outputs rather than copying hard-coded numerical claims.

## Not yet included

Full power/sample-size planning, multivariate regression diagnostics, randomized experimental design and Bayesian posterior modeling are planned for subsequent phases.
