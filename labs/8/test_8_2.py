from exercise_8_2 import *

try:
    Modulo(4, 1)
except PrimeError as e:
    # 1 is not a prime number
    print(e)
try:
    # 2.0 is not a prime number
    Modulo(4, 2.0)
except PrimeError as e:
    print(e)
try:
    Modulo({0}, 7)
except IntError as e:
    # {0} is not an integer
    print(e)
x = Modulo(6, 11)
print(repr(x))
print(x)
y = Modulo(11, 7)
print(repr(y))
print(y)
z = Modulo(-100, 29)
print(repr(z))
print(z)
