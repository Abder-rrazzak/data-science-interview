def solve(values):
    import numpy as np
    a = np.asarray(values, dtype=float)
    if not len(a): return []
    std = a.std(ddof=0)
    return (np.zeros(len(a)) if std == 0 else (a-a.mean())/std).tolist()
