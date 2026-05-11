# Prime() constructs an iterator that generates the prime numbers
# in increasing order, starting from 2.
#
# The object returned by Prime():
# - is its own iterator, so iter(I) is I;
# - returns 2 the first time next(I) is called;
# - thereafter returns the successive odd prime numbers.
#
# Thus the sequence produced is:
#   2, 3, 5, 7, 11, 13, 17, 19, 23, 29, ...
#
# No exception is raised to stop the iteration: the sequence of
# primes is infinite.
#
# Note 1: This exercise illustrates that an object can be its own
# iterator: __iter__() can return self, provided that __next__()
# is also defined.
#
# Note 2: The current prime being generated is stored as a class
# attribute, so all Prime objects share the same state.

class Prime:
    pass
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
