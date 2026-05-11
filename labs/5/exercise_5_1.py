# L is a list of integers and n is an integer ≥ 0.
#
# Given an integer e and a list A,
# let e × A denote the list obtained
# by multiplying every element of A by e.
#
# Let L₀ = L.
# For k ≥ 1, define the list Lₖ by
#     Lₖ = Lₖ₋₁ concatenated with (k + 1) × Lₖ₋₁.
#
# Returns Lₙ.

def f1(L, n):
    # INSERT YOUR CODE HERE
    for k in range(1, n+1):
        Lk = [item * (k+1) for item in L]
        L.extend(Lk)
    return L

print(f1([1], 1))
