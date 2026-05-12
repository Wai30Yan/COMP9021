# L is a list.
#
# Returns a copy of L, unless L can be partitioned into
# consecutive blocks all of the same length greater than 1.
# In that case, the blocks have maximal possible length,
# and the function returns the list of the results obtained
# by applying itself to each block.
#
# The argument L must not be modified.

from math import sqrt

def f4(L):
    # Base case: if list is empty or too short to partition (blocks must be > 1)
    n = len(L)
    if n < 4:  # Smallest possible partitionable list is [x,x,y,y] -> 4 elements
        return list(L)
    
    # Try maximal block lengths first (from n/2 down to 2)
    for i in range(n // 2, 1, -1):
        # 1. Check if the list can be divided into blocks of this size
        if n % i == 0:
            first_block = L[:i]
            
            # 2. Check if EVERY block is identical to the first one
            all_match = True
            for j in range(0, n, i):
                if L[j : j + i] != first_block:
                    all_match = False
                    break
            
            # 3. If they all match, apply f4 to each block recursively
            if all_match:
                return [f4(L[j : j + i]) for j in range(0, n, i)]
                
    # If no valid partition was found after checking all i
    return list(L)
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE



