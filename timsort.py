from typing import TypeVar


from state import *
from src.binary_insertion_sort import binary_insertion_sort
from src.count_run_and_make_asc import count_run_and_make_asc
from src.constants import *


T = TypeVar('T')


def __min_run(n: int) -> int:
    """Returns the min run len `k` for a array of size `n`."""

    assert n > 0

    # count how many bits are set to one before `n >= MIN_MERGE`
    # each iteration the last bit of `n` is consumed
    # parity = 1 if count is odd else 0
    parity = 0
    while n >= MIN_MERGE:
        parity |= n & 1
        n >>= 1

    # adds the value remaining at `n` and the parity
    # if `n` was a power of 2, will return `MIN_MERGE / 2`
    # else will return a number `K`, `MIN_MERGE / 2 <= K <= MIN_MERGE`,
    # such that `n / k` is close to, but strictly less than, an exact power of 2
    return n + parity


def timsort(a: list[T]) -> list[T]:
    assert a != None

    hi = len(a)
    if hi <= 1:
        return a  # [] and [X] are trivially sorted

    if hi < MIN_MERGE:
        # do a mergeless mini timsort

        # finds if the array starts with a sorted section
        # we can skip a section of the array by starting
        # the binary insetion sort after the sorted section
        sorted_end_index = count_run_and_make_asc(a, 0, hi)

        return binary_insertion_sort(a, 0, hi, sorted_end_index)

    # state for the current sort
    # this will include the tmp storage
    # run pointers
    # settings
    # and some convenience methods to apply changes based on the state on the array
    tst = TimsortState(a, hi)
    min_run = __min_run(hi)

    lo = 0
    remaining = hi
    while True:

        run_len = count_run_and_make_asc(a, lo, hi)

        # if run is too small, extend it
        if run_len < min_run:
            # force to the end of the list if remaining is smaller then min_run
            forced_size = remaining if remaining <= min_run else min_run

            # start at the next_run_len
            binary_insertion_sort(a, lo, lo + forced_size, lo + run_len)
            run_len = forced_size

        tst.push_run(base=lo, len=run_len)
        tst.merge_collapse()

        lo += run_len
        remaining -= run_len

        if remaining == 0:
            break

    assert lo == hi
    tst.merge_force_collapse()
    assert tst.stack_size == 1

    return a
