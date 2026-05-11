# L is a nonempty list of integers and n is an integer ≥ len(L).
#
# Given an integer e and a list A, let e × A denote the list obtained
# by multiplying every element of A by e.
#
# Define a sequence of lists (Bₖ) for k ≥ 0 by
#     B₀ = L
#     Bₖ = 2 × Bₖ₋₁   for k ≥ 1.
#
# Returns the list consisting of the first n elements of
#     B₀ + B₁ + B₂ + B₃ + ⋯

def f2(L: list, n):
    # INSERT YOUR CODE HERE
    result = L
    current_block = L
    while len(result) < n:
        current_block = [i * 2 for i in current_block]
        result.extend(current_block)
    return result

print(f2([1], 14))