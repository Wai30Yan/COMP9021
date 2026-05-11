# n is an integer.
#
# Prints an equality expressing n as a sum of distinct powers of 2.
# If n is negative, the equality expresses n as the negative of such a sum.
# For n = 0, the output is "0 = 0".

# The output is printed out, not returned.

def f4(n):
    if n == 0:
        print('0 = 0')
        return
    
    binary = bin(abs(n))
    binary = binary[2:]
    exponent = len(binary)-1
    prefix = '2^'
    s = f'{n} = '
    sign = ' + ' if n > 0 else ' - '
    L = []
    for i in binary:
        if i == '1':
            L.append(prefix + str(exponent))
        exponent -= 1
    
    if n < 0: L[0] = '-' + L[0]
    l = sign.join(i for i in L)
    
    print(s+l)
    #REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE
