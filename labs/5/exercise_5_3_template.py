# L is a nonempty list of nonempty lists of nonempty lists of integers,
# and n is an integer ≥ 0.
#
# Returns a pair (A, B) of lists of lists such that:
#   - For each member M of L with len(M) ≥ n, A has one member,
#     namely the list of all strictly positive integers occurring,
#     in order, in those members N of M such that sum(N) > 0.
#
#   - For each member N of each member M of L such that
#     len(M) ≥ n and sum(N) > 0, B has one member, namely
#     the list of the strictly positive integers of N, in order.

def f3(L, n):
    return [], []
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
