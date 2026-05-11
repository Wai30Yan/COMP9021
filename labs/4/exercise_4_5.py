# All arguments, if any, are integers.
#
# Returns a list whose i-th element is a pair consisting of
# (L[i], L[-i-1]) and (L[-i-1], L[i]),
# where L is the sequence of arguments.

def f5(*L):
    result = []
    for i, num1 in enumerate(L):
        num2 = L[-i-1]
        t = ((num1, num2), (num2, num1))
        result.append(t)
    return result
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
