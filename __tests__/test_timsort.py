from timsort import timsort
from nose2.tools import params

@params(list(range(0, 5)))
def test_runs(arr):
  assert timsort(arr)
