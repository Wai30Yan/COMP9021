# Written by *** for COMP9021

# Write a function paren_chunks(s) that takes a string s
# consisting only of the characters '(' and ')'.
#
# A non-empty string t is called a chunk if:
# - t contains the same number of '(' and ')', and
# - in every strict initial segment of t,
#   the number of '(' is strictly greater than
#   the number of ')'.
#
# The string s is intended to be a concatenation of chunks
# (placed next to each other with no extra characters).
#
# If s can be written as a concatenation of chunks, the
# function returns the list of these chunks (from left to right).
#
# Otherwise, the function returns the empty list [].
#
# Example 1:
# For s = '(()())()',
# the function returns ['(()())', '()'].
#
# Example 2:
# For s = '(())',
# the function returns ['(())'].
#
# Example 3:
# For s = '()()()',
# the function returns ['()', '()', '()'].
#
# Example 4:
# For s = ')()',
# the function returns [].
#
# Example 5:
# For s = '())',
# the function returns [].

def paren_chunks(s):
    ans = []
    cur = '' 
    balance = 0
    for c in s:
        cur += c
        if c == '(':
            balance += 1
        else:
            balance -= 1

        if balance < 0:
            return []
        
        if balance == 0:
            ans.append(cur)
            cur = ''
    if balance != 0:
        return []
    return ans

# ------------------------------------------------------------


# Write a function inverse_perm(L) that
# takes a list L of length n consisting of integers.
#
# The list L is intended to represent a mapping
# from {0, 1, ..., n - 1} to itself, where
# each index i is mapped to L[i].
#
# The function checks whether L represents a
# permutation of the set {0, 1, ..., n - 1}.
#
# If it does, the function returns a dictionary
# representing the inverse mapping:
# each element x in {0, 1, ..., n - 1} is
# associated with the unique index i such that
# L[i] == x.
#
# If L does not represent a permutation of
# {0, 1, ..., n - 1}, the function returns
# the empty dictionary {}.
#
# Example 1:
# For L = [2, 0, 1],
# the function returns
# {2: 0, 0: 1, 1: 2}.
#
# Example 2:
# For L = [2, 0, 1, 3, 5, 4],
# the function returns
# {2: 0, 0: 1, 1: 2, 3: 3, 5: 4, 4: 5}.
#
# Example 3:
# For L = [1, 1, 0],
# the function returns
# {}.
#
# Example 4:
# For L = [0, 2, 3],
# the function returns
# {}.

def inverse_perm(L):
    ans = {}
    s = set()
    n = len(L)
    for e in L:
        if e in s:
            return {}
        if e < 0 or e >= n:
            return {}
        s.add(e)

    for idx, num in enumerate(L):
        ans[num] = idx

    return ans


print(inverse_perm([2, 0, 1]) == {2: 0, 0: 1, 1: 2})
print(inverse_perm([2, 0, 1, 3, 5, 4]) == {2: 0, 0: 1, 1: 2, 3: 3, 5: 4, 4: 5})