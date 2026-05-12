def consecutive_sublists(L, k):
    if not L or k == 0:
        return [[]]
    result = []
    for i in range(len(L)-k+1):
        sublist = L[i:i+k]
        if sublist not in result:
            result.append(sublist)
    result.sort()
    return result

print(consecutive_sublists([7,7,7,7], 1))