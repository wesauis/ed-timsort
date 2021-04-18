from typing import Iterable
from timsort import insertion_sort
from __tests__.asserts import assert_sorted
from __tests__.randomplus import randarray
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

    assert_sorted(insertion_sort(it))
