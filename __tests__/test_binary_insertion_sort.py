from timsort import binary_insertion_sort
from utils.asserts import assert_has_all, assert_sorted
from utils.randomplus import randarray
from random import randint


def test_is_sorting():
    for to_sort in map(
        lambda _: randarray(randint(48, 256)),
        [None] * randint(3, 12)
    ):
        sorted = binary_insertion_sort(to_sort, 0, len(to_sort), 0)

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
        sorted = binary_insertion_sort(to_sort, 0, len(to_sort), 0)

        assert_sorted(sorted)
        assert_has_all(to_sort, sorted)
