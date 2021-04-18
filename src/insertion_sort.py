from timsort import binary_search
from typing import Iterable, TypeVar


T = TypeVar('T')


def insertion_sort(it: Iterable[T]) -> Iterable[T]:
    """Sorts a array by searching the right place for every item.

    This is a O(n2) algorithm"""

    # starts at the second element because the first has no items before it
    for index in range(1, len(it)):
        value = it[index]

        # go back into the array until it reaches the
        # start or finds the position to place the value
        ptr = index - 1
        while ptr >= 0 and value < it[ptr]:
            # while the index is not found it keeps moving the items to the right
            it[ptr + 1] = it[ptr]
            ptr -= 1

        it[ptr + 1] = value

    return it
