from typing import TypeVar


T = TypeVar('T')


def count_run_and_make_asc(a: list[T], lo: int, hi: int) -> int:
    """Finds a sequence of ordered values, make it ascending and
    returns the lenght of the run."""

    # end index of the run
    run_hi = lo + 1
    if run_hi >= hi:
        return 1

    # is ascending if it[lo] <= it[lo + 1]
    is_ascending = a[lo] <= a[run_hi]
    run_hi += 1

    if is_ascending:
        while run_hi < hi and a[run_hi - 1] <= a[run_hi]:
            run_hi += 1

    else:
        while run_hi < hi and a[run_hi - 1] > a[run_hi]:
            run_hi += 1

        # reverses the section
        a[lo:run_hi] = a[lo:run_hi][::-1]

    return run_hi - lo
