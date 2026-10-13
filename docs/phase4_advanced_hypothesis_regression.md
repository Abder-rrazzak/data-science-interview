# Phase 4 — Advanced Hypothesis Testing & Regression

All exercises use **synthetic observations**. None supports real security or operational claims.

## Run

```powershell
.\.venv\Scripts\python.exe scripts/run_advanced_statistics.py
.\.venv\Scripts\python.exe -m pytest -q
```

## 1. One-way ANOVA

**Question:** Do three groups have equal population means? Null hypothesis: all group means are equal. The F statistic compares between-group to within-group variability. ANOVA assumes independent observations, approximately normal errors and homogeneous variances. If variances differ, use Welch's ANOVA (not implemented here). A significant F test does not identify which groups differ: post-hoc tests with multiplicity correction are needed. Eta-squared is an effect-size measure, not a p-value.

## 2. Chi-square independence

**Question:** Are two categorical variables associated? Pearson chi-square compares observed to expected contingency-table counts. Small expected counts can invalidate asymptotic inference; consider Fisher's exact test for 2×2 tables. Cramér's V quantifies association strength. Association is not causation.

## 3. Multiple linear regression

Model: `y = β0 + β1*x1 + ... + βk*xk + ε`.

- Inspect residual-vs-fitted plots for misspecification and changing variance.
- Check multicollinearity with VIF; high VIF means unstable coefficient estimates.
- Breusch–Pagan tests whether residual variance is related to predictors; the provided LM implementation is educational, not a replacement for a comprehensive diagnostics library.
- Classical standard errors require appropriate assumptions; robust standard errors can be preferable with heteroscedasticity.
- A coefficient represents a *conditional association*, not proof of causation.
- R² is not a generalization score; evaluate on independent data.

## 4. Logistic regression

Use for binary outcomes. The log-odds are linear in the features. Predicted probabilities should be checked for calibration. **The demonstration intentionally reports training metrics only**; do not present them as held-out performance. In real work, use a train/validation/test split, a preprocessing Pipeline and leakage checks.

## 5. Interview drills

1. **ANOVA vs t-test?** ANOVA is an omnibus test for more than two groups; avoid multiple unadjusted t-tests.
2. **When is a chi-square test unreliable?** Sparse expected counts, dependence between observations, or non-count input.
3. **How do you detect multicollinearity?** Inspect design rank, predictor correlations and VIF; consider domain-informed feature removal or regularization.
4. **What does heteroscedasticity change?** Ordinary OLS coefficient estimates may remain unbiased under exogeneity, but classical standard errors and tests can be invalid.
5. **Why is a low p-value not enough?** Effect size, uncertainty, multiple testing, sampling design and practical relevance matter.
6. **How to explain logistic coefficients?** A one-unit feature increase changes log-odds by β holding others fixed; the odds ratio is `exp(β)`.
7. **Correlation vs causation?** Observational associations may reflect confounding, reverse causality or selection; causal claims require defensible identification.
8. **What if observations are repeated per unit?** Independence is violated; consider clustered standard errors or mixed-effects models.

## Practice tasks

- Change group variances and explain why classical ANOVA may fail.
- Create a sparse contingency table and inspect the warning.
- Make two predictors nearly collinear and compare VIF and coefficient stability.
- Add heteroscedastic noise to the regression example and inspect Breusch–Pagan p-value.
- Split logistic data into train and test; compare train vs held-out AUC and calibration.

## Boundaries

This phase does not yet implement post-hoc comparisons, robust OLS confidence intervals, mixed-effects models, or formal causal inference. Those are future enhancements.
