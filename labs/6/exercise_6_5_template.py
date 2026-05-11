# L is a list of lists of integers.
#
# Prints a rectangle of coloured squares of the same shape as L,
# with the square at position (i, j) determined by the sign of
# the sum of all elements in row i and column j, counting the
# element at (i, j) only once:
# - blue if the sum is 0,
# - green if the sum is positive,
# - red if the sum is negative.
#
# The argument L may be modified by the function.
#
# For example, the entry -3 corresponds to a blue square
# in the 3 × 5 rectangle below.
#
#   .  .  2  .  .
#   2  0 -3  7 -4
#   .  . -4  .  .
#
# np.sign() and np.sum() are useful.
# The axis argument of np.sum() is useful.

import numpy as np

def f5(L):
    pass
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
