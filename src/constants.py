"""
Minimum sized sequence to be merged.

This constant needs to be a power of two
"""
MIN_MERGE = 32

"""
When we get into galloping mode, we stay there until
both runs win less often than MIN_GALLOP consecutive times.
"""
MIN_GALOP: int = 7

"""
Temporary storage size for not-so-small iterables
"""
TMP_STORAGE_LEN = 256
