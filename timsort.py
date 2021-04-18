from typing import Iterable, TypeVar
from src.binary_search import binary_search
from src.binary_insertion_sort import binary_insertion_sort


T = TypeVar('T')


def timsort(it: Iterable[T]) -> Iterable[T]:
    _len = len(it)

    if _len < 64:
        return binary_insertion_sort(it)

    # min_minrun: int = 32
    # max_minrun: int = 64

    # # min_run: int = random
    # min_galop: int = 7

    return it
