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
