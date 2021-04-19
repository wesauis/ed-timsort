def assert_sorted(it: list):
    """Asserts if the array is sorted at ascending order."""

    try:
        for index in range(1, len(it)):
            assert it[index - 1] <= it[index]

    except AssertionError:
        assert False, {
            "message": "Unsorted",
            "it": it
        }


def assert_has_all(it0: list, it1: list):
    """Asserts if it1 has all items that it0 have and have the same size."""

    for item0 in it0:
        assert next((True for item1 in it1 if item0 == item1), False), {
            "message": "item not present",
            "item": item0
        }

    assert len(it0) == len(it1), {
        "message": "Diferent sizes",
        "it0": it0,
        "it1": it1
    }
