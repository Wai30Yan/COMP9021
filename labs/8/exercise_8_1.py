# Prime(p) constructs a Prime object from p, provided that p is
# a prime integer that has not already been used.
#
# A PrimeError exception is raised if:
# - p is not an integer;
# - p is less than 2;
# - p is not prime;
# - p has already been used in a successful call to Prime(...)
#   since the most recent call to Prime.reset().
#
# Prime.reset() clears the set of previously used prime numbers.
#
# Note: The class is intentionally written in a slightly unconventional way
# to illustrate how Python handles methods and class-level state.

from math import sqrt

# DEFINE A CLASS THAT DERIVES FROM EXCEPTION

class Prime:
    pass
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
