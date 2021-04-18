from math import log2, ceil
from typing import Iterable, TypeVar


T = TypeVar('T')


def binary_search(it: Iterable[T], target: T, low: int = 0, high: int = None) -> int:
    """Searches a value on a iterable, or on a section of it.

    This algorithm expects an sorted iterable.

    Arguments:
        - it     : iterable to be searched on
        - target : desidered value
        - low    : starting index to search, defaults to 0
        - high   : end index to search, defaults to the last index of the iterable

    Returns the index of `target` on the iterable or `-1` if not found
    """

    _len = len(it)
    if (_len <= 0):
        return -1

    if high == None:
        high = _len - 1

    for _ in range(ceil(log2(_len))):
        mid = int((low + high) / 2)
        value = it[mid]

        if value == target:
            return mid

        elif value < target:
            low = mid + 1

        else:
            high = mid - 1

    return -1
