# Returns a generator that yields the successive rows of
# Pascal's triangle, starting with the first row [1].
#
# Each yielded value is a list of integers. After yielding
# a row L, the next row is obtained by placing 1 at both
# ends of a new list and, between them, inserting the sums
# of each pair of consecutive elements of L.
#
# Thus the first rows yielded are:
# [1]
# [1, 1]
# [1, 2, 1]
# [1, 3, 3, 1]
# ...
#
# The generator yields infinitely many rows.

def f2():
    current_row = [1]
    while True:
        yield current_row
        
        next_row = [1]
        for i in range(len(current_row) - 1):
            new_element = current_row[i] + current_row[i+1]
            next_row.append(new_element)
        next_row.append(1)
        
        current_row = next_row


I = f2()
print(next(I))
print(next(I))
print(next(I))
print(next(I))
print(next(I))
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
