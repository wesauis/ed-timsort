from timsort import binary_insertion_sort
from utils.asserts import assert_has_all, assert_sorted
from utils.randomplus import randarray
from nose2.tools import params


SIZE = 63


@params(
    randarray(SIZE),
    randarray(SIZE),
    randarray(SIZE),
    randarray(SIZE),
    randarray(SIZE),
    randarray(SIZE),
)
def test_insertion_sort(to_sort: list[int]):
    """Tests if the array is been sorted"""

    sorted = binary_insertion_sort(to_sort, 0, len(to_sort), 0)

    assert_sorted(sorted)
    assert_has_all(to_sort, sorted)


@params(
    randarray(0),
    randarray(1),
    randarray(2),
    randarray(3),
    randarray(4),
)
def test_works_with_small_arrays(to_sort: list[int]):
    test_insertion_sort(to_sort)
