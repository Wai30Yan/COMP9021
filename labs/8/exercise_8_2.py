# Modulo(k, p) constructs the residue class of k modulo p.
#
# A PrimeError exception is raised if:
# - p is not an integer;
# - p is less than 2;
# - p is not prime.
#
# An IntError exception is raised if:
# - k is not an integer.
#
# If construction succeeds:
# - the modulus is p;
# - the stored value is the remainder of k upon division by p,
#   so it is always one of 0, 1, ..., p - 1.
#
# repr(Modulo(k, p)) returns:
#   Modulo(r, p)
# where r is the stored remainder.
#
# str(Modulo(k, p)) returns:
#   r (mod p)
# where r is the stored remainder.

from math import sqrt

# DEFINE TWO CLASSES THAT DERIVE FROM EXCEPTION

class Modulo:
    pass
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
