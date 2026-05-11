# Modulo(k, p) constructs an object representing k modulo p,
# with p required to be a prime integer.
#
# A PrimeError exception is raised if:
# - p is not an integer;
# - p is less than 2;
# - p is not prime.
#
# An IntError exception is raised if k is not an integer.
#
# On success, the object stores:
# - modulus = p;
# - k = the unique remainder of k modulo p in the range
#   0 to p - 1.
#
# A ModuloError exception is raised when an arithmetic operation
# is attempted with an invalid operand, namely:
# - the operand is not a Modulo object;
# - the operand is a Modulo object, but with a different modulus.
#
# For Modulo objects x and y with the same modulus:
# - x + y returns a new Modulo object representing the sum;
# - x * y returns a new Modulo object representing the product;
# - x += y updates x in place to represent the sum, and returns x;
# - x *= y updates x in place to represent the product, and returns x.
#
# repr(Modulo(k, p)) returns:
#   Modulo(r, p)
# where r is the stored remainder.
#
# str(Modulo(k, p)) returns:
#   r (mod p)
# where r is the stored remainder.
#
# Note: This exercise is intentionally designed to illustrate that
# Python lets special methods such as __add__, __iadd__, __mul__,
# and __imul__ be implemented explicitly, so that operators can be
# given user-defined behaviour.


# COMPLETE THE CODE FOR EXERCISE 8.2 BY:
# - ADDING A CLASS DERIVED FROM EXCEPTION;
# - ADDING METHODS TO THE Modulo CLASS.
