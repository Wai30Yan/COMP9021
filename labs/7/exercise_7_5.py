# A special list is a list whose elements are integers or
# special lists.
#
# The argument L is assumed to be a special list.
#
# Returns a dictionary D such that:
# - the keys of D are non-empty tuples of indices;
# - for every key (i_1, ..., i_n) in D, the associated value
#   is the integer reached by starting from L and then
#   successively taking index i_1, then index i_2, ..., then
#   index i_n.
#
# Conversely, every integer occurring in L appears exactly
# once as a value in D, associated with the tuple of indices
# that leads to it.
#
# type() is useful.

def f5(L):
    return {}
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
