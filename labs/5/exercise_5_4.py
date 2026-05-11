# L is a list of integers.
#
# Return a list of lists obtained as follows.
#
# Take as many disjoint pairs of consecutive elements as possible
# simultaneously from the beginning and from the end of L,
# with the same number of pairs taken from each side.
#
# These pairs appear at the beginning and at the end of the result,
# in their original order.
#
# If elements remain in the middle of L after removing these pairs,
# they form a single sublist placed between the two groups of pairs.

def f4(L):
    if not L: return []
    result = []
    k = len(L) // 4
    mid = 0
    for i in range(0, k*2, 2):
        result.append(L[i : i+2])
        mid = i + 2

    if mid != len(L)-(k*2):
        result.append(L[mid: len(L)-(k*2)])
    
    for i in range(len(L)-(k*2), len(L), 2):
        result.append(L[i : i+2])
    return result
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE

print(f4([1, 2, 3, 4, 5]))