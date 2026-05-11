# L is a list of lists of integers forming a square
# with even side length, and half is one of
# 'top', 'bottom', 'left' or 'right'.
#
# Returns a new list of lists obtained from L by possibly
# swapping diagonally opposite elements so that, for each
# such pair, the element in the specified half of the square
# is at least equal to the other one.
#
# For instance, ! and ? are diagonally oppposite in:
#
# ! . . .
# . . . .
# . . . .
# . . . ?
#
# The integer at location ! should be at least equal to
# the integer at location ? iff half is 'top' or 'left';
# otherwise, they should be swapped.
#
# For another example, ! and ? are diagonally oppposite in:
#
# . . . .
# . . ! .
# . ? . .
# . . . .
#
# The integer at location ! should be at least equal to
# the integer at location ? iff half is 'top' or 'right';
# otherwise, they should be swapped.
#
# The argument L must not be modified by the function.

def f3(L, half='top'):
    N = len(L)

    res = [row[:] for row in L]

    for r in range(N // 2):
        for c in range(N):
            r_opp = N - 1 - r
            c_opp = N - 1 - c
            partner = L[r_opp][c_opp]
    return []
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
