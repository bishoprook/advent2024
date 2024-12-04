from itertools import islice
import collections

# Slight tweak from more_itertools. This will continue iterating when the
# window reaches the end, with one less element each time.
def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG EFG FG G ()
    iterator = iter(iterable)
    window = collections.deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)
    while len(window) > 0:
        window.popleft()
        yield tuple(window)
