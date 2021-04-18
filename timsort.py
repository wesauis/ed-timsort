from typing import Iterable, TypeVar
from src.binary_search import binary_search


T = TypeVar('T')


def timsort(unsorted: Iterable[T]) -> Iterable[T]:
    if not unsorted or len(unsorted) < 1:
        return unsorted

    pass
