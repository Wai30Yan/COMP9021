# L is a list of lists of integers
#
# Returns a pair (F, R) where F is the sorted list of all
# integers in L, and R is a list of lists obtained by
# partitioning F into sublists whose lengths match those
# of the corresponding sublists in L.
#
# The argument L must not be modified by the function.

def f1(L):
    sorted_list = []
    length_of_list = []
    for sublist in L:
        length_of_list.append(len(sublist))
        for i in sublist:
            sorted_list.append(i)

    sorted_list.sort()
    idx = 0
    sublist = []
    for length in length_of_list:
        sublist.append(sorted_list[idx:idx+length])
        idx += length

    return (sorted_list, sublist)
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
L = [[]]
print(f1(L))
# L = [[4, 10, -19, 11, 15], [6, -7, 16, 9], [6, 12, 12],[-19, -8, 6, 18, 12]]; print(f1(L))
