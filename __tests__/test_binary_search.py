from math import ceil, log2
from typing import Callable
from binary_search import binary_search


def test_performance():
  """Test if worst performance is less or equal O(log n)

  The test will try to search all numbers on a list of size 1_000_000
  """

  class Value:
    def __init__(self, integer: int, on_eq: Callable):
      self.integer = integer
      self.on_eq = on_eq

    def __eq__(self, other):
      self.on_eq()
      return self.integer == other.integer

    def __lt__(self, other):
      return self.integer < other.integer

    def __str__(self) -> str:
      return f'Value({self.integer})'

  class Counter:
    count = 0

    def reset(self):
      self.count = 0

    def increment(self):
      self.count += 1

  iters = Counter()

  values = [Value(n, iters.increment) for n in range(1_000_000)]

  max_iters = ceil(log2(1_000_000))

  for item in values:
    iters.reset()

    # Check if item was found
    index = binary_search(values, item)
    assert index != -1, f'Not found: {item}'
    assert item.integer == values[index].integer, f'Incorrect index: {index}'

    # Check if took too long
    assert iters.count <= max_iters, f'Max iterations exceeded: {iters} of {max_iters}'
