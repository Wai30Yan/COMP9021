# Written by *** for COMP9021

# A prime number p is said to be consecutively representable
# if it can be written as the sum of two or more consecutive
# primes in the sequence of prime numbers.
#
# For instance:
# - 5 = 2 + 3
# - 17 = 2 + 3 + 5 + 7
# - 41 = 2 + 3 + 5 + 7 + 11 + 13
# - 53 = 5 + 7 + 11 + 13 + 17
#
# Write a function primes_as_consecutive_sums(a, b) that:
# - takes two integers a and b with 2 <= a <= b;
# - considers all prime numbers between a and b inclusive;
# - determines which of them can be written as the sum of
#   two or more consecutive primes;
# - for each such prime, keeps a decomposition using the
#   largest possible number of consecutive primes;
# - prints all such primes in increasing order, together
#   with their decomposition;
# - then prints the largest number of consecutive primes used
#   in any such decomposition;
# - and finally prints the prime or primes for which that
#   maximum is achieved, together with their decomposition.
#
# Example:
# primes_as_consecutive_sums(2, 3) prints
#
# There are no such primes between 2 and 3.
#
# Example:
# primes_as_consecutive_sums(2, 50) prints
#
# The following primes between 2 and 50 can be written
# as the sum of consecutive primes:
#
# 5 = 2 + 3
# 17 = 2 + 3 + 5 + 7
# 23 = 5 + 7 + 11
# 31 = 7 + 11 + 13
# 41 = 2 + 3 + 5 + 7 + 11 + 13
#
# The largest number of consecutive primes used is 6.
# It is achieved for:
# 41 = 2 + 3 + 5 + 7 + 11 + 13
#
# In some intervals, that maximum can be achieved by more than one prime.
# In that case, the program should print:
#
# The largest number of consecutive primes used is ...
# It is achieved for the following primes:
# ...
#
# Note:
# In the tests, a and b can be much larger than in the sample examples,
# so a solution that avoids unnecessary work is expected.

from math import sqrt


def sieve_of_primes_up_to(n):
    sieve = [True] * (n + 1)
    for p in range(2, round(sqrt(n)) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return sieve


def primes_as_consecutive_sums(a, b):
    sieve = sieve_of_primes_up_to(b)

    primeList = []
    for idx, isPrime in enumerate(sieve):
        if idx == 0 or idx == 1:
            continue
        if isPrime:
            primeList.append(idx)

    results = {}
    for i in range(len(primeList)):
        curSum = 0
        for j in range(i, len(primeList)):
            curSum += primeList[j]
            
            if curSum > b:
                break
                
            # Check if the sum is a prime within range [a, b]
            # and that at least two numbers (j > i) are used
            if curSum >= a and sieve[curSum] and j > i:
                count = (j - i) + 1 # Number of primes in this sequence
                
                if curSum not in results or count > len(results[curSum]):
                    results[curSum] = primeList[i : j + 1]
    
    if len(results) == 0:
        print(f'There are no such primes between {a} and {b}.')
        return
    
    print(f'The following primes between {a} and {b} can be\nwritten as the sum of consecutive primes:')
    print()

    for key in sorted(results.keys()):
        primes = results.get(key)
        print(f'{key} = ' + ' + '.join(str(primes[i]) for i in range(len(primes))))

    print()
    max_len = max(len(v) for v in results.values())
    # longestLists = [v for v in results.values() if len(v) == max_len]
    longestKeys = [k for k, v in results.items() if len(v) == max_len]
    if len(longestKeys) > 1:
        print(f'The largest number of consecutive primes used is {max_len}.')
        print('It is achieved for the following primes:')
        for key in longestKeys:
            primes = results[key]
            print(f'{key} = ' + ' + '.join(str(primes[i]) for i in range(len(primes))))

    else:
        primes = results[longestKeys[0]]
        print(f'The largest number of consecutive primes used is {len(primes)}.')
        print('It is achieved for:')
        print(f'{longestKeys[0]} = ' + ' + '.join(str(primes[i]) for i in range(len(primes))))


primes_as_consecutive_sums(379, 491)