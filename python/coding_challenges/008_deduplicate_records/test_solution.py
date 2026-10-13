from solution import solve

def test_example():
    assert solve([{"id": 1, "v": 3}, {"id": 1, "v": 4}, {"id": 2, "v": 5}]) == [{"id": 1, "v": 3}, {"id": 2, "v": 5}]
