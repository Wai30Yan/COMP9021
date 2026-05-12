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
class PrimeError(Exception):
    pass

class Prime:
    used_primes = set()

    def __init__(self, n):
        if not isinstance(n, int) or self.prime_check(n) == False or n < 2:
            raise PrimeError(f"{n} is not a prime number\n")
        if n in self.used_primes:
            raise PrimeError(f"We have seen {n} before\n")
        if self.prime_check(n):
            self.used_primes.add(n)

    def prime_check(self, n):
        for i in range(2, int(sqrt(n))+1):
            if n % i == 0:
                return False
        return True
    
    @classmethod
    def reset(self):
        self.used_primes.clear()
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
