def solve(values, weights):
    if len(values) != len(weights) or not values or any(w < 0 for w in weights) or sum(weights) <= 0:
        raise ValueError("invalid values or weights")
    return sum(v*w for v,w in zip(values, weights)) / sum(weights)
