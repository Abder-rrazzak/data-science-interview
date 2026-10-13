def solve(records):
    seen, result = set(), []
    for row in records:
        if row["id"] not in seen:
            seen.add(row["id"])
            result.append(row)
    return result
