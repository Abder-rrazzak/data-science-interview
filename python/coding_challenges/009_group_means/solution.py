def solve(rows):
    from collections import defaultdict
    groups = defaultdict(list)
    for group, value in rows: groups[group].append(value)
    return {group: sum(values)/len(values) for group, values in groups.items()}
