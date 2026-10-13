from solution import solve

def test_example():
    assert solve([("A", 2), ("B", 5), ("A", 4)]) == {"A": 3.0, "B": 5.0}
