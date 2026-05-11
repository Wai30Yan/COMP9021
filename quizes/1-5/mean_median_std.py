from random import seed, randint
import sys
from statistics import mean, median, pstdev

# Prompts the user for an integer to provide as argument to the
# seed() function.
try:
    arg_for_seed = int(input('Feed the seed with an integer: '))
except ValueError:
    print('Input is not an integer, giving up.')
    sys.exit()   
# Prompts the user a strictly positive number, nb_of_elements.
try:
    nb_of_elements = int(input('How many elements do you want to generate? '))
except ValueError:
    print('Input is not an integer, giving up.')
    sys.exit()
if nb_of_elements <= 0:
    print('Input should be strictly positive, giving up.')
    sys.exit()
seed(arg_for_seed)
# Generates a list of nb_of_elements random integers between -50 and 50.
L = [randint(-50, 50) for _ in range(nb_of_elements)]
# Prints out the list.
print('\nThe list is:' , L)
print()

if len(L) == 1:
    print(f'The mean is {float(L[0]):.2f}.\n'
          f'The median is {float(L[0]):.2f}.\n'
          'The standard deviation is 0.00.\n')
    
    print('Confirming with functions from the statistics module:')
    print(f'The mean is {mean(L):.2f}.\n'
        f'The median is {median(L):.2f}.\n'
        f'The standard deviation is {pstdev(L):.2f}.')
    
else:
        mean_value = sum(L) / len(L)
        sorted_L = sorted(L)
        median_value = (sorted_L[len(L) // 2] + sorted_L[-(len(L) // 2 + 1)]) / 2
        variance = sum((x - mean_value) ** 2 for x in L) / len(L)
        std_dev = variance ** 0.5

        mean_of_L = mean(L)
        median_of_L = median(L)
        std_dev_of_L = pstdev(L)
    
        print(f'The mean is {mean_value:.2f}.\n'
            f'The median is {median_value:.2f}.\n'
            f'The standard deviation is {std_dev:.2f}.')
    
        print('Confirming with functions from the statistics module:')
        print(f'The mean is {mean_of_L:.2f}.\n'
            f'The median is {median_of_L:.2f}.\n'
            f'The standard deviation is {std_dev_of_L:.2f}.')

# The mean is -1.00.\n
# The median is -1.00.\n
# The standard deviation is 0.00.\n
# \n
# Confirming with functions from the statistics module:\n
# The mean is -1.00.\n
# The median is -1.00.\n
# The standard deviation is 0.00.\n'