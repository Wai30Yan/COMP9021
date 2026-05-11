from exercise_8_6 import *

L = CircularTuple([3, 8, 14, 19])
print(len(L))
# Indices modulo the length of L
print(L[-20], L[-11], L[-5], L[-2], L[2], L[5], L[11], L[20], sep=', ')
try:
    L[2] = 0
except CircularTupleError as e:
    print(e)
