from exercise_8_5 import *

print('Testing a polygon')
print()
# Printed out as a side effect of following statement:
# I am a polygon
x = Polygon(((-3.3, 3.0), (-2.3, 5.1), (0.2, 3.4), (3.2, 5.3),
             (5.0, 2.8), (2.8, -1.8), (1.7, 0.7), (-2.6, -4.1),
             (-5.7, -2.0), (-0.3, 0.7)
            )
           )
print(x.nb_of_vertices)
# Printed out as a side effect of following statement:
# Computed using the shoelace formula
print(round(x.area(), 3))
print()
print('Testing a rectangle')
print()
# Printed out as a side effect of following statement:
# I am a polygon
# More precisely, I am a rectangle
y = Rectangle(((5.5, -2.8), (5.5, 4.4), (-3.6, 4.4), (-3.6, -2.8)))
print(y.nb_of_vertices)
# Printed out as a side effect of following statement:
# I could compute it more easily, but well, I leave it to Polygon...
# Computed using the shoelace formula
print(round(y.area(), 3))
print()
print('Testing a square')
print()
# Printed out as a side effect of following statement:
# I am a polygon
# More precisely, I am a rectangle
# Even more precisely, I am a square
z = Square(((-3.5, 3.5), (3.5, 3.5), (3.5, -3.5), (-3.5, -3.5)))
print(z.nb_of_vertices)
# Printed out as a side effect of following statement:
# I compute it myself!
print(round(z.area(), 3))