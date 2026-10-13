def solve(dates, start, end):
    import pandas as pd
    present = set(pd.to_datetime(dates).normalize())
    return [d.strftime("%Y-%m-%d") for d in pd.date_range(start, end) if d not in present]
