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
class IntError(Exception):
    pass

class PrimeError(Exception):
    pass

class Modulo:
    r, p = 0, 0

    def __init__(self, k, p):
        if not isinstance(k, int):
            raise IntError(f"{k} is not an integer")
        if not isinstance(p, int) or p < 2 or self.prime_check(p) == False:
            raise PrimeError(f"{p} is not a prime number")
        self.p = p
        self.r = k % p

    def prime_check(self, n):
        for i in range(2, int(sqrt(n))+1):
            if n % i == 0:
                return False
        return True
    
    def __repr__(self):
        return f"Modulo({self.r}, {self.p})"
    
    def __str__(self):
        return f"{self.r} (mod {self.p})"
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
