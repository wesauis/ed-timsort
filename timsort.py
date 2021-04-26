from typing import TypeVar


from state import *
from src.binary_insertion_sort import binary_insertion_sort
from src.count_run_and_make_asc import count_run_and_make_asc
from src.constants import *


T = TypeVar('T')


def timsort(a: list[T]) -> list[T]:
    _len = len(a)
    assert a != None

    if _len < MIN_MERGE:
        # do a mergeless mini timsort

        # finds if the array starts with a sorted section
        # we can skip a section of the array by starting
        # the binary insetion sort after the sorted section
        sorted_end_index = count_run_and_make_asc(a, 0, _len)

        return binary_insertion_sort(a, 0, _len, sorted_end_index)

    # state for the current sort
    # this will include the tmp storage
    # run pointers
    # settings
    # and some convenience methods to apply changes based on the state on the array
    tst = TimsortState(a, _len)

    lo = 0
    while lo < _len:

        run_len = count_run_and_make_asc(a, lo, _len)

        # if run is too small, extend it
        if run_len < tst.min_run:
            # force to the end of the list if remaining is smaller then min_run
            remaining = _len - lo
            forced_size = remaining if remaining <= tst.min_run else tst.min_run

            # start at the next_run_len
            binary_insertion_sort(a, lo, lo + forced_size, lo + run_len)
            run_len = forced_size

        tst.push_run(base=lo, len=run_len)
        tst.merge_collapse()

        lo += run_len

    assert lo == _len
    tst.merge_force_collapse()
    assert tst.stack_len == 1

    return a
