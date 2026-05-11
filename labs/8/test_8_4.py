from exercise_8_4 import *

I = Prime()
print(*(next(I) for _ in range(10)), sep=', ')
print()
J = Prime()
print([next(J) for _ in range(10)])
