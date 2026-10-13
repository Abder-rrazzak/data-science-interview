def solve(values, k):
    if k < 0: raise ValueError("k must be nonnegative")
    return sorted(set(values), reverse=True)[:k]
