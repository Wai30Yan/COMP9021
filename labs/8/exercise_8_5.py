# Polygon(points) constructs an object representing a polygon
# whose vertices are given by the sequence points.
#
# points is a sequence of pairs of floating point numbers,
# interpreted as (x, y)-coordinates of the vertices, listed
# in order along the boundary (clockwise or anticlockwise).
#
# On construction:
# - the message 'I am a polygon' is printed;
# - the number of vertices is stored as nb_of_vertices.
#
# Polygon.area() returns the area of the polygon, computed
# using the shoelace formula, and prints:
#   Computed using the shoelace formula
#
# Rectangle(points) constructs a Polygon object that is
# known to be a rectangle.
#
# On construction:
# - the Polygon constructor is first called;
# - then the message 'More precisely, I am a rectangle'
#   is printed.
#
# Rectangle.area() prints:
#   I could compute it more easily, but well, I leave it to Polygon...
# and returns the result of Polygon.area().
#
# Square(points) constructs a Rectangle object that is
# known to be a square.
#
# On construction:
# - the Rectangle constructor is first called;
# - then the message 'Even more precisely, I am a square'
#   is printed.
#
# Square.area() prints:
#   I compute it myself!
# and returns the area computed directly from the side length.
#
# Note 1: This exercise illustrates inheritance and method overriding:
# subclasses can extend the behaviour of their parent class and
# redefine methods such as area().
#
# Note 2: The use of super() shows how a method in a subclass can
# explicitly call the corresponding method in its parent class.
#
# Note 3: Constructors are chained: creating a Square object
# successively calls the constructors of Polygon, Rectangle,
# and Square.

# DEFINE THE Polygon, Rectangle and Square CLASSES
from math import sqrt
class Polygon:
    def __init__(self, points):
        print('I am a polygon')
        self.nb_of_vertices = len(points)
        self.points = points

    def area(self):
        print('Computed using the shoelace formula')
        area_sum = 0
        for i in range(self.nb_of_vertices):
            nxt = (i + 1) % self.nb_of_vertices
            area_sum += (self.points[i][0] * self.points[nxt][1]) - (self.points[nxt][0] * self.points[i][1])
        area_sum = abs(area_sum) / 2
        return area_sum

class Rectangle(Polygon):
    def __init__(self, points):
        super().__init__(points)
        print('More precisely, I am a rectangle')

    def area(self):
        print('I could compute it more easily, but well, I leave it to Polygon...')
        return super().area()

class Square(Rectangle):
    def __init__(self, points):
        super().__init__(points)
        print('Even more precisely, I am a square')
    
    def area(self):
        print('I compute it myself!')
        distance = sqrt((self.points[0][0] - self.points[1][0])**2+(self.points[0][1] - self.points[1][1])**2)
        return distance