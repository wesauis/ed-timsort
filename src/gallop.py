from typing import TypeVar


T = TypeVar('T')


def gallop_left(key: T, a: list[T], base: int, range_len: int, hint: int):
    """Locates the position at which to insert the specified key into the
    specified sorted range; if the range contains an element equal to key,
    returns the index of the leftmost equal element."""

    last_offset = 0
    offset = 1

    # exponential search at the direction of the value
    if key > a[base + hint]:
        # gallop right until `a[base + hint + last_offset] < key <= a[base + hint + offset]`
        max_offset = range_len - hint
        while offset < max_offset and key > a[base + hint + offset]:
            last_offset = offset
            offset = int(offset * 2) + 1

        if offset > max_offset:
            offset = max_offset

        last_offset += hint
        offset += hint

    else:
        # gallop left until `a[base + hint - offset] < key <= a[base + hint - last_offset]`
        max_offset = hint + 1
        while offset < max_offset and key <= a[base + hint + offset]:
            last_offset = offset
            offset = int(offset * 2) + 1

        if offset > max_offset:
            offset = max_offset

        # Make offsets relative to base
        last_offset, offset = hint - offset, hint - last_offset

    # approches the real index of the value
    last_offset += 1
    while last_offset < offset:
        m = last_offset + int((offset - last_offset) / 2)

        if key > a[base + m]:
            last_offset = m + 1  # a[base + m] < key
        else:
            offset = m           # key <= a[base + m]

    return offset


def gallop_right(key: T, a: list[T], base: int, range_len: int, hint: int):
    """Like gallop_left, except that if the range contains an element equal to
    key, gallop_right returns the index after the rightmost equal element."""

    last_offset = 0
    offset = 1

    # exponential search at the direction of the value
    if key < a[base + hint]:
        # gallop right until `a[base + hint + last_offset] < key <= a[base + hint + offset]`
        max_offset = range_len - hint
        while offset < max_offset and key > a[base + hint + offset]:
            last_offset = offset
            offset = int(offset * 2) + 1

        if offset > max_offset:
            offset = max_offset

        last_offset += hint
        offset += hint

    else:
        # gallop left until a[base + hint - offset] < key <= a[base + hint - last_offset]
        max_offset = hint + 1
        while offset < max_offset and key <= a[base + hint + offset]:
            last_offset = offset
            offset = int(offset * 2) + 1

        if offset > max_offset:
            offset = max_offset

        # Make offsets relative to base
        last_offset, offset = hint - offset, hint - last_offset

    # approches the real index of the value
    last_offset += 1
    while last_offset < offset:
        m = last_offset + int((offset - last_offset) / 2)

        if key > a[base + m]:
            last_offset = m + 1  # a[base + m] < key
        else:
            offset = m           # key <= a[base + m]

    return offset
