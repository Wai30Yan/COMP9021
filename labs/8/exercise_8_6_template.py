# CircularTuple(L) constructs an object behaving like a sequence
# whose elements are those of L, but indexed in a circular way.
#
# The object supports the sequence protocol:
# - len(CircularTuple(L)) returns the length of L;
# - indexing is defined for all integers i, with:
#     CircularTuple(L)[i] == L[i mod n],
#   where n is the length of L.
#
# In particular, both positive and negative indices are accepted,
# and are interpreted modulo the length of L.
#
# The object is not mutable:
# - any attempt to assign to an index raises a CircularTupleError
#   exception.
#
# Note 1: By inheriting from collections.abc.Sequence and defining
# __len__() and __getitem__(), the class automatically gains the
# full behaviour of a sequence (such as iteration).
#
# Note 2: Although the class is called CircularTuple, it wraps a
# list and only enforces immutability by raising an exception in
# __setitem__; Python does not enforce true immutability.

from collections.abc import Sequence

# DEFINE A CLASS CircularTupleError THAT DERIVES FROM EXCEPTION

class CircularTuple(Sequence):
    pass
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
