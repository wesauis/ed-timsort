from math import log2, ceil
from typing import Iterable, TypeVar


T = TypeVar('T')


def binary_search(array: Iterable[T], target: T, start: int = 0, end: int = None) -> int:
    """Pesquisa um valor no array.

    Este algoritimo espera que o array seja previamente ordenado.

    Argumentos:
        - array : um array com elementos que possam ser comparados
        - target: valor que se deseja encontrar no vetor
        - start : min index to search
        - end   : max index to search

    Retorna:
        a posição em que `target` está no `array`, senão `-1`
    """

    _len = len(array)
    if (_len <= 0): return -1

    if end == None: end = _len - 1

    for _ in range(ceil(log2(_len))):
        mid = int((start + end) / 2)
        value = array[mid]

        if value == target:
          return mid

        elif value < target:
          start = mid + 1

        else:
          end = mid - 1

    return -1
