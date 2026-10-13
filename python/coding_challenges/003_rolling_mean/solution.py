def solve(values, window=3):
    if window < 1: raise ValueError("window must be positive")
    return [sum(values[max(0, i-window+1):i+1]) / len(values[max(0, i-window+1):i+1]) for i in range(len(values))]
