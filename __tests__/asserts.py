from typing import Iterable


def assert_sorted(it: Iterable) -> bool:
    for index in range(1, len(it)):
        assert it[index - 1] <= it[index]
