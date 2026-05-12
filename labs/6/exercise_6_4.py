# n is an integer ≥ 1 and black_centre is a Boolean.
#
# Prints an n × n square made of alternating concentric
# layers of black and white squares, with the colour of
# the central layer determined by black_centre.
#
# np.full() is useful.

import numpy as np

# POSSIBLY DEFINE A FUNCTION

def f4(n, black_centre=True):
    max_L = (n - 1) // 2
    map = np.full((n,n), ' ')
    for L in range(max_L + 1):
        if black_centre:
            if(max_L - L) % 2 == 0:
                char = "⬛"
                map[L, L : n-L] = char
                map[n-1-L, L : n-L] = char
                map[L : n-L ,L] = char
                map[L : n - L, n-1-L] = char
            else: 
                char = "⬜"
                map[L, L : n-L] = char
                map[n-1-L, L : n-L] = char
                map[L : n-L ,L] = char
                map[L : n - L, n-1-L] = char
        else:
            if(max_L - L) % 2 == 0:
                char = "⬜"
                map[L, L : n-L] = char
                map[n-1-L, L : n-L] = char
                map[L : n-L ,L] = char
                map[L : n - L, n-1-L] = char
            else:
                char = "⬛"
                map[L, L : n-L] = char
                map[n-1-L, L : n-L] = char
                map[L : n-L ,L] = char
                map[L : n - L, n-1-L] = char
    
    for m in map:
        for c in m:
            print(c, end='')
        print()
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE

print(f4(4, True))


# s = 'hello world'
# l = []
# for i in s:
#     if i is not ' ':
#         l.append(i)
# print(l)