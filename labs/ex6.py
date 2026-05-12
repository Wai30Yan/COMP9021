def alternating_parity_sublists(L):
    result = []
    # Loop through every possible starting index
    for i in range(len(L)):
        # For each starting index, try to extend the sublist to the right
        for j in range(i, len(L)):
            # Rule: Single-element sublists alternate trivially
            if j == i:
                result.append(L[i:j+1])
            else:
                # Rule: Check if current element alternates parity with the previous one
                if L[j] % 2 != L[j-1] % 2:
                    result.append(L[i:j+1])
                else:
                    # If parity doesn't alternate, we can't extend this sublist further
                    break
    
    return result

print(alternating_parity_sublists([3,8,5]))