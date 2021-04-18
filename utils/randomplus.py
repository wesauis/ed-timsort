from random import randint
from typing import Iterable


def randarray(size: int, a: int = -128, b: int = 127) -> Iterable[int]:
    """Return random iterable of desidered size containing integers in range [a, b], including both end points."""

    it = [0] * size

    for index in range(size):
        it[index] = randint(a, b)

    return it
