def solve(values, size):
    if size < 1: raise ValueError("size must be positive")
    for start in range(0, len(values), size):
        yield values[start:start+size]
