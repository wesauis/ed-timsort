from typing import TypeVar
from src.binary_insertion_sort import binary_insertion_sort
from src.settings import MIN_MERGE, MIN_GALOP, TMP_STORAGE_LEN


T = TypeVar('T')


class __TimsortState:
    def __init__(self, a: list[T], _len: int):
        self.a = a

        # galop mode settings
        # this variable will change over time
        # and could be so large that galop mode is not used anymore
        # on the current sort
        self.min_galop: int = MIN_GALOP

        # temp storage for merges, may be increased if necessary
        self.tmp_len: int = self.__tmp_len(_len)
        self.tmp_base: int = 0
        self.tmp: list[T] = [None] * self.tmp_len

        # stack for runs
        # run is a piece of the array that is already sorted
        self.stack_len: int = self.__stack_len(_len)
        self.run_base: list[int] = [0] * self.stack_len
        self.run_len: list[int] = [0] * self.stack_len

        self.min_run: int = self.__min_run(_len)

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

    def ensure_tmp_capacity(self, min_capacity: int):
        pass

    @staticmethod
    def __tmp_len(n: int) -> int:
        """Returns the recommended tmp array size for a array of size `n`.

        If the `n` is too small, the size will be `n / 2`.
        Else the returned size will be `TMP_STORAGE_LEN`
        """

        if len < 2 * TMP_STORAGE_LEN:
            return n // 2
        else:
            return TMP_STORAGE_LEN

    @staticmethod
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

    @staticmethod
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


def count_run_and_make_asc(a: list[T], lo: int, hi: int) -> int:
    """Finds a sequence of ordered values, make it ascending and
    returns the lenght of the run."""

    # end index of the run
    run_hi = lo + 1
    if run_hi == hi:
        return 1

    # is ascending if it[lo] <= it[lo + 1]
    is_ascending = a[lo] <= a[run_hi]
    run_hi += 1

    if is_ascending:
        while run_hi < hi and a[lo] <= a[run_hi]:
            run_hi += 1

    else:
        while run_hi < hi and a[lo] > a[run_hi]:
            run_hi += 1

        # reverses the section
        a[lo:run_hi] = a[lo:run_hi][::-1]

    return run_hi - lo


def gallop_left(key: T, a: list[T], base: int, range_len: int, hint: int):
    """Locates the position at which to insert the specified key into the
    specified sorted range; if the range contains an element equal to key,
    returns the index of the leftmost equal element."""

    last_offset = 0
    offset = 1

    # exponential search at the direction of the value
    if key > a[base + hint]:
        # gallop right until `a[base + hint + last_offset] < key <= a[base + hint + offset]`
        max_offset = range_len - hint
        while offset < max_offset and key > a[base + hint + offset]:
            last_offset = offset
            offset = int(offset * 2) + 1

        if offset > max_offset:
            offset = max_offset

        last_offset += hint
        offset += hint

    else:
        # gallop left until `a[base + hint - offset] < key <= a[base + hint - last_offset]`
        max_offset = hint + 1
        while offset < max_offset and key <= a[base + hint + offset]:
            last_offset = offset
            offset = int(offset * 2) + 1

        if offset > max_offset:
            offset = max_offset

        # Make offsets relative to base
        last_offset, offset = hint - offset, hint - last_offset

    # approches the real index of the value
    last_offset += 1
    while last_offset < offset:
        m = last_offset + int((offset - last_offset) / 2)

        if key > a[base + m]:
            last_offset = m + 1  # a[base + m] < key
        else:
            offset = m           # key <= a[base + m]

    return offset


def gallop_right(key: T, a: list[T], base: int, range_len: int, hint: int):
    """Like gallop_left, except that if the range contains an element equal to
    key, gallop_right returns the index after the rightmost equal element."""

    last_offset = 0
    offset = 1

    # exponential search at the direction of the value
    if key < a[base + hint]:
        # gallop right until `a[base + hint + last_offset] < key <= a[base + hint + offset]`
        max_offset = range_len - hint
        while offset < max_offset and key > a[base + hint + offset]:
            last_offset = offset
            offset = int(offset * 2) + 1

        if offset > max_offset:
            offset = max_offset

        last_offset += hint
        offset += hint

    else:
        # gallop left until a[base + hint - offset] < key <= a[base + hint - last_offset]
        max_offset = hint + 1
        while offset < max_offset and key <= a[base + hint + offset]:
            last_offset = offset
            offset = int(offset * 2) + 1

        if offset > max_offset:
            offset = max_offset

        # Make offsets relative to base
        last_offset, offset = hint - offset, hint - last_offset

    # approches the real index of the value
    last_offset += 1
    while last_offset < offset:
        m = last_offset + int((offset - last_offset) / 2)

        if key > a[base + m]:
            last_offset = m + 1  # a[base + m] < key
        else:
            offset = m           # key <= a[base + m]

    return offset


def timsort(a: list[T]) -> list[T]:
    _len = len(a)

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
    tst = __TimsortState(a, _len)

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

    tst.merge_force_collapse()

    return a
