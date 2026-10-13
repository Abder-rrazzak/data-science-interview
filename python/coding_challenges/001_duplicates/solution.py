def solve(values):
    seen, repeated, output = set(), set(), []
    for value in values:
        if value in seen and value not in repeated:
            output.append(value)
            repeated.add(value)
        seen.add(value)
    return output
