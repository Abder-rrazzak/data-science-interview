# Phase 5 — Experimental Design & A/B Testing

All demonstrations use **synthetic data**. The estimand in the simulated experiment is the difference in mean outcomes between randomized groups. A statistically significant result does not necessarily imply a meaningful operational improvement.

## 1. Randomization

Use `random_assignment(n, seed=...)` for complete randomization. Use `stratified_assignment(strata)` to balance assignments within prespecified groups. Randomization protects against systematic baseline differences *in expectation*, not in every finite sample. Verify allocation and report attrition/noncompliance.

## 2. Sample size and power

`sample_size_two_means(effect, std, alpha=.05, power=.8)` returns an approximate per-arm sample size under independent observations, common SD and a two-sided normal test. Set the minimum detectable effect **before** the experiment. The approximation is not suitable for clustered data without a design-effect adjustment.

## 3. A/B test

`ab_test(treatment, control)` computes the mean difference, Welch t-test, confidence interval and Cohen's d. Welch's test allows unequal variances. Check independence, selection, outliers and missingness. For nonrandomized comparisons, the observed difference is an association, not a causal estimate.

## 4. Confounding and balance

`standardized_mean_difference()` measures covariate imbalance. Confounding arises when a third variable influences both exposure and outcome. Random assignment reduces confounding; observational adjustment alone cannot guarantee causal identification.

## 5. Multiple testing

`adjust_pvalues(..., method='bonferroni'|'holm'|'fdr_bh')` implements three corrections. Bonferroni and Holm control family-wise error under their standard conditions; Benjamini–Hochberg controls false discovery rate under independence or suitable positive dependence assumptions. Pre-register primary endpoints where possible.

## 6. Practical significance

Specify the minimum effect that would change a decision, implementation cost, confidence interval, and operational constraints. Never equate p < .05 with mission impact.

## Run (Windows PowerShell)

```powershell
.\.venv\Scripts\python.exe scripts/run_experimental_design.py
.\.venv\Scripts\python.exe -m pytest tests/test_experimental_design.py -q
```

## Interview practice

**Q1: How do you design an experiment?** Define the decision, unit of randomization, primary outcome, minimum detectable effect, assignment mechanism, power, duration, exclusion rules, and analysis plan before collecting outcomes.

**Q2: What is a confounder?** A variable influencing both exposure and outcome, creating a potentially misleading association. Random assignment is a strong preventive design strategy.

**Q3: Why stratify?** To ensure reasonable allocation balance within important predefined subgroups and potentially improve precision.

**Q4: What is statistical power?** The probability of rejecting a false null hypothesis for a specified alternative, assuming the model and design assumptions hold.

**Q5: Why use Welch rather than Student's t-test?** Welch does not require equal population variances and accommodates unequal group sizes.

**Q6: Why correct for multiple tests?** Repeating tests raises the chance of false discoveries; choose error control appropriate to the analysis goal.

**Q7: A p-value is small but effect is tiny. What next?** Compare the confidence interval to a pre-specified practical threshold, costs, and possible harms; do not rely on p-value alone.

**Q8: What threatens experiment validity?** Contamination, attrition, noncompliance, instrumentation changes, peeking without sequential correction, and clustered dependence.

## Guided exercise

1. Generate a randomized 500-unit experiment with true simulated effect 0.4.
2. Repeat across several random seeds; compare confidence intervals and p-values.
3. Increase the sample size and observe interval width.
4. Simulate four exploratory outcomes and compare unadjusted, Holm and BH results.
5. Draft a five-sentence executive recommendation acknowledging uncertainty.
