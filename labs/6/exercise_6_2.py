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

def f2(L, i, j, major=True):
    total_sum = 0
    r_start, c_start = i - 1, j - 1
    target = abs(i - j) if major else sum(i,j)
    for r in range(len(L)):
        for c in range(len(L)):
            if major:
                if target == r+c+2:
                    total_sum += L[r][c]
            else:
                if target == r-c:
                    pass
    return 0
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
