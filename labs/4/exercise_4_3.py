# L is an increasing list of integers.
#
# As long as there exists an element of L
# that is neither the first nor the last element
# and is equal to the average of its two neighbors,
# removes the leftmost such element.
#
# Returns L after all such removals have been performed.

def f3(L):
    # INSERT YOUR CODE HERE
    if len(L) < 3: return L
    i = 1

    while i < len(L)-1:
        y = L[i-1] + L[i+1]
        if 2 * L[i] == y:
            L.pop(i)
            i = 1
        else:
            i += 1

    return L
