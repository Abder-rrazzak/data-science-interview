def solve(values):
    import numpy as np
    if len(values) < 4: return []
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    if iqr == 0: return []
    return [i for i, v in enumerate(values) if v < q1 - 1.5 * iqr or v > q3 + 1.5 * iqr]
