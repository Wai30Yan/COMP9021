# n is an integer ≥ 0.
#
# Prints a trace of the recursive computation of fibo(n),
# where fibo(0) = 0, fibo(1) = 1, and for n ≥ 2,
# fibo(n) = fibo(n - 1) + fibo(n - 2).
#
# Each time fibo(k) is computed, a line is printed before
# the computation and a line is printed after the computation.
#
# - The lines corresponding to a call at depth d in the
#   computation are preceded by d tab characters.
# - For each k, the calls to fibo(k) are numbered in the
#   order in which they occur.
#
# The output has the form:
#
# Computation nb 1 of fibo(n)...
#     Computation nb 1 of fibo(n-1)...
#     ...
#     ... computed as ...
# ...
# ... computed as ...
#
# The function returns None.

from collections import defaultdict

def f6(n):
    _f6(n)

def _f6(n):
    return 0
    # ADD ARGUMENTS WITH DEFAULT VALUES IF NEEDED
    # AND REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
