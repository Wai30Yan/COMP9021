from exercise_8_3 import *

x = Modulo(6, 11)
try:
    x + 20
except ModuloError as e:
    # 20 is not a Modulo object
    print(e)
try:
    y = Modulo(20, 13)
    z = x + y
except ModuloError as e:
    # 6 (mod 11) and 7 (mod 13) do not have the same modulus
    print(e)
print('\nTesting addition\n')
y = Modulo(20, 11)
z = x + y
print(x, y, z, sep='; ')
y = Modulo(20, 11)
x += y
print(x, y, sep='; ')
print('\nTesting mutiplication\n')
y = Modulo(-30, 11)
z = x * y
print(x, y, z, sep='; ')
y = Modulo(-30, 11)
x *= y
print(x, y, sep='; ')
