from solution import solve

def test_example():
    assert list(solve(list(range(5)), 2)) == [[0, 1], [2, 3], [4]]
