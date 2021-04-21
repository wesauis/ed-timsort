from math import ceil, log2
from typing import TypeVar

from src.constants import *
from src.gallop import gallop_left, gallop_right


T = TypeVar('T')


def __tmp_len(n: int) -> int:
    """Returns the recommended tmp array size for a array of size `n`.

    If the `n` is too small, the size will be `n / 2`.
    Else the returned size will be `TMP_STORAGE_LEN`
    """

    if len < 2 * TMP_STORAGE_LEN:
        return n // 2
    else:
        return TMP_STORAGE_LEN


def __stack_len(n: int) -> int:
    """Returns the length for the run stack based on the length `n`
    of the array."""

    if n < 120:
        return 5

    if n < 1542:
        return 10

    if n < 119151:
        return 24

    return 49


def __min_run(n: int) -> int:
    """Returns the min run len `k` for a array of size `n`."""

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


def __next_smallest_power(n: int):
    """Returns the smallest power of 2 > `n`."""

    return 2 ** ceil(log2(n))


class TimsortState:
    def __init__(self, a: list[T], _len: int):
        self.a = a

        # galop mode settings
        # this variable will change over time
        # and could be so large that galop mode is not used anymore
        # on the current sort
        self.min_galop: int = MIN_GALOP

        # temp storage for merges, may be increased if necessary
        self.tmp_len: int = __tmp_len(_len)
        self.tmp_base: int = 0
        self.tmp: list[T] = [None] * self.tmp_len

        # stack for runs
        # run is a piece of the array that is already sorted
        self.stack_len: int = __stack_len(_len)
        self.run_base: list[int] = [0] * self.stack_len
        self.run_len: list[int] = [0] * self.stack_len

        self.min_run: int = __min_run(_len)

    def push_run(self, base: int, len: int):
        self.run_base[self.stack_len] = base
        self.run_len[self.stack_len] = len
        self.stack_len += 1

    def merge_collapse(self):
        """Merge runs and keep the stack at a ratio like a
        'Fibonacci Sequence' on descending order.

        Only consecutive runs will be merged

        More at:
            - https://hg.python.org/cpython/file/tip/Objects/listsort.txt#l330
        """

        while self.stack_len > 1:
            pivot = self.stack_len - 2

            # Consider the stack as having the lengths: A, B, C, D
            # if
            #     3+ runs on the stack and B <= C + D
            # or
            #     4+ runs on the stack and A <= C + B
            if pivot > 0 and self.run_len[pivot - 1] <= self.run_len[pivot] + self.run_len[pivot + 1] or \
               pivot > 1 and self.run_len[pivot - 2] <= self.run_len[pivot] + self.run_len[pivot - 1]:

                # if B < D
                if self.run_len[pivot - 1] < self.run_len[pivot + 1]:
                    pivot -= 1

            # else if C > B, no merges needed
            elif pivot < 0 or self.run_len[pivot] > self.run_len[pivot + 1]:
                break

            self.merge_at(pivot)

    def merge_force_collapse(self):
        while self.stack_len > 1:
            # ensure descending len
            pivot = self.stack_len - 2
            if pivot > 0 and self.run_len[pivot - 1] < self.run_len[pivot + 1]:
                pivot -= 1

            self.merge_at(pivot)

    def merge_at(self, pivot: int):
        base1 = self.run_base[pivot]
        base2 = self.run_base[pivot + 1]
        len1 = self.run_len[pivot]
        len2 = self.run_len[pivot + 1]

        # save new len
        self.run_len[pivot] = len1 + len2

        # if pivot == 3rd-last run slide index over
        # in this case pivot + 1 is the consumed run
        if pivot == self.stack_len - 3:
            self.run_base[pivot + 1] = self.run_base[pivot + 2]
            self.run_len[pivot + 1] = self.run_len[pivot + 2]

        # consume last run on stack
        self.stack_len -= 1

        # index for the first element of r2 at r1
        r2_base_r1 = gallop_right(self.a[base2], self.a, base1, len1, 0)

        base1 += r2_base_r1
        len1 -= r2_base_r1

        if len1 == 0:
            return

        # index for the last element of r1 at r2
        len2 = gallop_left(self.a[base1 + len1 - 1],
                           self.a, base2, len2, len2 - 1)

        if len2 == 0:
            return

        # merge remaining runs, using tmp array with min(len1, len2) elements
        if len1 <= len2:
            self.merge_lo(base1, len1, base2, len2)
        else:
            self.merge_hi(base1, len1, base2, len2)

    def merge_lo(self, base1: int, len1: int, base2: int, len2: int):
        # https://github.com/AdoptOpenJDK/openjdk-jdk11/blob/master/src/java.base/share/classes/java/util/TimSort.java#L685
        pass

    def merge_hi(self, base1: int, len1: int, base2: int, len2: int):
        pass

    def ensure_tmp_capacity(self, min_capacity: int) -> list[T]:
        """Ensures that the external array tmp has at least the specified
        number of elements, increasing its size if necessary. The size
        increases exponentially to ensure amortized linear time complexity."""

        if self.tmp_len < min_capacity:
            new_len = min(
                __next_smallest_power(min_capacity),
                len(self.a) // 2)

            self.tmp = [None] * new_len
            self.tmp_base = 0
            self.tmp_len = new_len

        return self.tmp
