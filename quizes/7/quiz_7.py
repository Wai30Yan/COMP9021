# Written by *** for COMP9021
#
# Prompts the user for a seed, a dimension dim, and an upper bound N.
#
# Randomly fills a grid of size dim × dim with numbers between 0 and N,
# and computes:
# - the maximum number of cells in a path such that consecutive cells
#   contain numbers whose values differ by exactly 1;
# - the number of such longest paths.
#
# A path is obtained by repeatedly moving in the grid one step diagonally:
# north-west, north-east, south-west, or south-east.
#
# No cell can be visited more than once in a path.
#
# Two paths that are the reverse of each other are considered
# to be the same path and are counted only once.

import sys
from random import seed, randint


def display_grid():
    for row in grid:
        print(' '.join(f'{e:{len(str(upper_bound))}}' for e in row)) 

def length_and_number_of_longest_paths():

    if not grid or not grid[0]:
        return 0, 0
    
    all_paths = []

    def get_paths(r, c, current_path, visited):
        found_neighbours = False
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < dim and 0 <= nc < dim and (nr, nc) not in visited:
                if abs(grid[nr][nc] - grid[r][c]) == 1:
                    found_neighbours = True
                    visited.add((nr, nc))
                    get_paths(nr, nc, current_path + [(nr, nc)], visited)
                    visited.remove((nr, nc))

        if not found_neighbours:
            path_tuple = tuple(current_path)
            reversed_path = tuple(reversed(current_path))
            if reversed_path < path_tuple:
                all_paths.append(reversed_path)
            else:
                all_paths.append(path_tuple)

    for r in range(dim):
        for c in range(dim):
            get_paths(r, c, [(r,c)], {(r,c)})

    if not all_paths:
        return 0, 0
    
    max_len = max(len(p) for p in all_paths)

    longest_unique_paths = {p for p in all_paths if len(p) == max_len}
    return max_len, len(longest_unique_paths)
    # REPLACE THE RETURN STATEMENT ABOVE

# POSSIBLY DEFINE OTHER FUNCTIONS

try:
    for_seed, dim, upper_bound =\
        (abs(int(x)) for x in input('Enter three integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[randint(0, upper_bound) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()

max_length, nb_of_paths_of_max_length = length_and_number_of_longest_paths()
print('The longest paths made up of adjacent diagonal cells')
print('    with values differing by 1 contain', max_length,
      max_length == 1 and 'cell.' or 'cells.'
     )
if nb_of_paths_of_max_length == 1:
    print('There is one such path.')
else:
    print('There are', nb_of_paths_of_max_length, 'such paths.')