# All arguments, if any, are integers.
#
# Let L be the sequence of arguments.
# Returns the list consisting of:
# - the tuple formed by the elements of L followed by them in reverse order;
# - the tuple formed by the elements of L in reverse order followed by them
#   in their original order.

def f6(*L):
    if not L: return []
    # reversed the tuple
    R = L[::-1] 
    return [(L+R), (R+L)]
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
