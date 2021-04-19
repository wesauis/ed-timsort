from typing import TypeVar


T = TypeVar('T')


def __binary_loc_search(it: list[T], item: T, low: int, high: int) -> int:
    """Searches the right index to place a value."""

    # recursion stop case
    if low >= high:
        if item > it[low]:
            # place item after low_item
            return low + 1

        # place item at low_item
        return low

    mid = int((low + high) / 2)

    # stable part, that keeps the same elements at the same order
    # + economizes a recursion and shift :)
    if item == it[mid]:
        return mid + 1

    elif item > it[mid]:
        return __binary_loc_search(it, item, mid + 1, high)
    else:
        return __binary_loc_search(it, item, low, mid - 1)


def binary_insertion_sort(it: list[T], lo: int, hi: int, start: int) -> list[T]:
    """Sorts a array by searching the right place for every item.

    This is a worst case O(n^2) algorithm
    But only uses O(log n) comparisons by finding the index with a binary search
    """

    if (start <= lo):
        # ignores the first element because it is already sorted
        start = lo + 1

    # starts at the second element because the first has no items before it
    for index in range(start, hi):
        item = it[index]

        # searches the place to put the item
        # a binary search in a 64 item array will be done in a max of 6 steps
        # and makes the shift faster, reducing the number of comparisons
        loc = __binary_loc_search(it, item, lo, index - 1)

        # opens space for item
        while loc < index:
            it[index] = it[index - 1]
            index -= 1

        it[loc] = item

    return it
