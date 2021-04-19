from typing import TypeVar
from src.binary_insertion_sort import binary_insertion_sort
from src.settings import MIN_MERGE, MIN_GALOP, TMP_STORAGE_LEN


T = TypeVar('T')


def create_tmp_for(_len: int) -> list[T]:
    """Creates a iterable to be used as temporary storage for merges.

    If the iterable size is too small,
    the temp iterable will have half of the size of the iterable to be sorted

    Otherwise the size of the temp iterable will have the size defined by TMP_STORAGE_LEN
    """

    if len < 2 * TMP_STORAGE_LEN:
        _len = int(_len / 2)
    else:
        _len = TMP_STORAGE_LEN

    return [None] * _len


def stack_size_for(_len: int) -> int:
    """Returns the length for the run stack based on the len of iterable been sorted."""

    if _len < 120:
        return 5

    if _len < 1542:
        return 10

    if _len < 119151:
        return 24

    return 49


def count_run_and_make_asc(it: list[T], lo: int, hi: int) -> int:
    """Finds a sequence of ordered values, make it ascending and
    returns the lenght of the run."""

    # end index of the run
    run_hi = lo + 1
    if run_hi == hi:
        return 1

    # is ascending if it[lo] <= it[lo + 1]
    is_ascending = it[lo] <= it[run_hi]
    run_hi += 1

    if is_ascending:
        while run_hi < hi and it[lo] <= it[run_hi]:
            run_hi += 1

    else:
        while run_hi < hi and it[lo] > it[run_hi]:
            run_hi += 1

        # reverses the section
        it[lo:run_hi] = it[lo:run_hi][::-1]

    return run_hi - lo


def timsort(it: list[T]) -> list[T]:
    _len = len(it)

    if _len < MIN_MERGE:
        # do a mergeless mini timsort

        # finds if the array starts with a sorted section
        # we can skip a section of the array by starting
        # the binary insetion sort after the sorted section
        sorted_end_index = count_run_and_make_asc(it, 0, _len)

        return binary_insertion_sort(it, 0, _len, sorted_end_index)

    # galop mode settings
    # this variable will change over time
    # and could be so large that galop mode is not used anymore
    # on the current sort
    min_galop: int = MIN_GALOP

    # temp storage for merges, may be increased if necessary
    tmp: list[T] = create_tmp_for(_len)
    tmp_base_index: int = 0
    tmp_len: int = len(tmp)

    # stack for runs
    # run is a piece of the array that is already sorted
    stack_size: int = stack_size_for(_len)
    run_base_index: list[int] = [0] * stack_size
    run_len: list[int] = [0] * stack_size

    return it
