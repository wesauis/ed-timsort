from random import randint


def randarray(size: int, a: int = -128, b: int = 128) -> list[int]:
    """Return random list of desidered size containing integers
    in range [a, b], including both end points."""

    it = [0] * size

    for index in range(size):
        it[index] = randint(a, b)

    return it
