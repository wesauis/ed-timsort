from timsort import timsort
from utils.asserts import assert_has_all, assert_sorted
from utils.randomplus import randarray
from random import randint


def test_is_sorting():
    for to_sort in map(
        lambda _: randarray(randint(48, 256)),
        [None] * randint(3, 12)
    ):
        sorted = timsort(to_sort)

        assert_sorted(sorted)
        assert_has_all(to_sort, sorted)


def test_works_with_small_arrays():
    for to_sort in (
        randarray(0),
        randarray(1),
        randarray(2),
        randarray(3),
        randarray(4)
    ):
        sorted = timsort(to_sort)

        assert_sorted(sorted)
        assert_has_all(to_sort, sorted)
