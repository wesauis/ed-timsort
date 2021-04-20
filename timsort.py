from typing import TypeVar
from src.binary_insertion_sort import binary_insertion_sort
from src.settings import MIN_MERGE, MIN_GALOP, TMP_STORAGE_LEN


T = TypeVar('T')


def create_tmp_for(it_len: int) -> list[T]:
    """Creates a array to be used as temporary storage for merges.

    If the array size is too small,
    the temp array will have half of the size of the array to be sorted

    Otherwise the size of the temp array will have the size defined by
    TMP_STORAGE_LEN
    """

    if len < 2 * TMP_STORAGE_LEN:
        it_len = int(it_len / 2)
    else:
        it_len = TMP_STORAGE_LEN

    return [None] * it_len


def stack_size_for(it_len: int) -> int:
    """Returns the length for the run stack based on the it_len
    of the array been sorted."""

    if it_len < 120:
        return 5

    if it_len < 1542:
        return 10

    if it_len < 119151:
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


def min_run_for(n: int) -> int:
    """Returns the min run len `k` for a array of size `n`."""

    # count how many bits are set to one before `n >= MIN_MERGE`
    # parity = 1 if count is odd else 0
    parity = 0
    while n >= MIN_MERGE:
        parity |= n & 1
        n >>= 1

    # adds the value remaining at `n` and the parity
    # if `n` was a power of 2, will return `MIN_MERGE / 2`
    # else will return a number `K`, `MIN_MERGE / 2 <= K <= MIN_MERGE`,
    # such that `n/k` is close to, but strictly less than, an exact power of 2
    return n + parity


# def merge(pivot: int, stack_size: int, run_bases: list[])

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
    tmp_base: int = 0
    tmp_len: int = len(tmp)

    # stack for runs
    # run is a piece of the array that is already sorted
    stack_size: int = stack_size_for(_len)
    run_base: list[int] = [0] * stack_size
    run_len: list[int] = [0] * stack_size

    min_run: int = min_run_for(_len)

    lo = 0
    while lo < _len:

        run_len = count_run_and_make_asc(it, lo, _len)

        # if run is too small, extend it
        if run_len < min_run:
            # force to the end of the list if remaining is smaller then min_run
            remaining = _len - lo
            forced_size = remaining if remaining <= min_run else min_run

            # start at the next_run_len
            binary_insertion_sort(it, lo, lo + forced_size, lo + run_len)
            run_len = forced_size

        # push run to pending stack
        run_base[stack_size] = lo
        run_len[stack_size] = run_len
        stack_size += 1

        # merge runs on the stack
        # to keep stability only consecutive runs are merged
        #
        # the algorith try to keep the run_lengths growing at
        # a ratio, when reading from right to left, that grows
        # at least as fast as the fibonacci numbers
        #
        # how it works:
        # https://hg.python.org/cpython/file/tip/Objects/listsort.txt#l330
        while stack_size > 1:
            n = stack_size - 2

            # Consider the stack as having the lengths: A, B, C, D
            # if
            #     3+ runs on the stack and B <= C + D
            # or
            #     4+ runs on the stack and A <= C + B
            if n > 0 and run_len[n - 1] <= run_len[n] + run_len[n + 1] or \
               n > 1 and run_len[n - 2] <= run_len[n] + run_len[n - 1]:

                # if B < D
                if run_len[n - 1] < run_len[n + 1]:
                    n -= 1

            # C > B, no merges needed
            elif n < 0 or run_len[n] > run_len[n + 1]:
                break

            # functionfy - merge_at
            pivot = n

            base0 = run_base[pivot]
            base1 = run_base[pivot + 1]
            len0 = run_len[pivot]
            len1 = run_len[pivot + 1]

            # save new len
            run_len[pivot] = len0 + len1

            # if pivot == 3rd-last run slide index over
            # in this case pivot + 1 is the consumed run
            if pivot == stack_size - 3:
                run_base[pivot + 1] = run_base[pivot + 2]
                run_len[pivot + 1] = run_len[pivot + 2]

            # consume last run on stack
            stack_size -= 1

            # 500

        # https://github.com/AdoptOpenJDK/openjdk-jdk11/blob/master/src/java.base/share/classes/java/util/TimSort.java

    return it
