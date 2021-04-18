from typing import Iterable
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
def test_insertion_sort(it: Iterable):
    """Tests if the array is been sorted"""

    sorted = binary_insertion_sort(it)

    assert_sorted(sorted)
    assert_has_all(it, sorted)
