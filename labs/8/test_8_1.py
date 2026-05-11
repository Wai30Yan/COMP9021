from exercise_8_1 import *

Prime.reset()
try:
    Prime(1)
except PrimeError as e:
    # 1 is not a prime number
    print(e)
try:
    Prime(2.0)
except PrimeError as e:
    # 2.0 is not a prime number
    print(e)
try:
    Prime([1, 2, 3])
except PrimeError as e:
    # [1, 2, 3] is not a prime number
    print(e)
_ = Prime(2)
try:
    Prime(2)
except PrimeError as e:
    # We have seen 2 before
    print(e)
_ = Prime(3)
try:
    Prime(4)
except PrimeError as e:
    # 4 is not a prime number
    print(e)
_ = Prime(5)
_ = Prime(7)
try:
    _ = Prime(2)
except PrimeError as e:
    # We have seen 2 before
    print(e)
_ = Prime(11)
try:
    Prime(5)
except PrimeError as e:
    # We have seen 5 before
    print(e)
Prime.reset()
_ = Prime(2), Prime(3), Prime(5), Prime(7), Prime(11)
