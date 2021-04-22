from timsort import timsort
from utils.asserts import assert_has_all, assert_sorted
from utils.randomplus import randarray
from nose2.tools import params
from random import randint


@params(
    *(map(lambda _: randarray(randint(48, 256)), [None] * randint(3, 12)))
)
def test_is_sorting(to_sort: list[int]):
    sorted = timsort(to_sort)

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
    test_is_sorting(to_sort)
