# L is a nonempty list of lists of integers forming a square,
# i and j are integers between 1 and the size of the square,
# and major is a Boolean.
#
# Returns the sum of the elements on the diagonal passing
# through position (i, j): the major diagonal (NW-SE direction)
# if major is True, and the minor diagonal (SW-NE direction)
# otherwise.
#
# Illustration for a square of size 5:
#           j
#       1 2 3 4 5
#    1  . . . . .
#    2  . . . . .
#  i 3  . . . . .
#    4  . . . . .
#    5  . . . . .

#   1 2
# 1 1 2
# 2 3 4


def f2(L, i, j, major=True):
    total_sum = 0
    r_start, c_start = i - 1, j - 1
    target = r_start - c_start if major else r_start + c_start
    for r in range(len(L)):
        for c in range(len(L)):
            if major:
                if r - c == target:
                    total_sum += L[r][c]
            else:
                if r + c == target:
                    total_sum += L[r][c]
    return total_sum
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
