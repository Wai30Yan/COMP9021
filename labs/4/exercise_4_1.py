# n is an integer ≥ 1.
#
# For each integer i from n down to 1,
# print the sequence obtained by repeatedly dividing i by 2
# and taking the floor of the result at each step.
#
# The sequence starts with i and stops before the value would become 0.
#
# Each integer is printed in a field
# whose width is equal to the number of digits of n plus 1.
# Each sequence is printed on its own line.
#
# The output is printed, not returned.

def f1(n):
    while n >= 1:
        
        i = n
        s = f"{i:>2}"

        while i > 1:
            i = i // 2
            s = s + f"{i:>2}"
        print(s)
        n -= 1
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
