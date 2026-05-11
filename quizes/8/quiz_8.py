# Written by *** for COMP9021

# Models intervals and collections of intervals on the real line.
#
# Your implementation should:
# - validate interval consistency,
# - represent objects in a human-readable form, and
# - determine whether a given interval is fully covered by a collection
#   of intervals.
#
# The following classes must be implemented:
# - Interval(a, b)
#   Represents the closed interval [a, b].
# - IntervalCollection(*intervals)
#   Represents a collection of pairwise disjoint closed intervals.
#
# Validation rules
#
# - Interval:
#   Both arguments must be real numbers (integers or floats),
#   and must satisfy a <= b.
#   Boolean values are not considered valid.
#   Otherwise, raise an IntervalError with message:
#       Cannot create an Interval: invalid endpoints
#
# - IntervalCollection:
#   Every argument must be an Interval object.
#   No two intervals in the collection are allowed to overlap
#   or even touch (that is, share an endpoint).
#   Otherwise, raise an IntervalCollectionError with message:
#       Cannot create an IntervalCollection: invalid intervals
#
# Special methods
#
# - __repr__() and __str__() are implemented for both classes.
#
# - Interval objects can be compared using comparison operators,
#   thanks to the __eq__() and __lt__() special methods.
#   They are ordered by increasing left endpoint; in the case of equal
#   left endpoints, the right endpoint is used to break ties.
#   Note that, in a valid IntervalCollection, no two intervals share
#   the same left endpoint.
#
# - For IntervalCollection, the "in" operator is implemented
#   thanks to the __contains__() special method:
#       interval in collection
#   returns True if interval is fully covered by the collection,
#   and False otherwise.
#   If the left-hand side of "in" is not an Interval object, then
#   False is returned.
#
# Methods
#
# - If interval_1 and interval_2 denote Interval objects, then
#   interval_1.overlaps(interval_2)
#   returns True if the two intervals overlap or touch,
#   and False otherwise.
#
# - If interval_1 and interval_2 denote Interval objects, then
#   interval_1.merge(interval_2)
#   returns the smallest interval containing both intervals,
#   provided they overlap or touch.
#   Otherwise, an IntervalError is raised with message:
#       Cannot merge non-overlapping intervals
#
# - If collection denotes an IntervalCollection object, then
#   collection.total_length()
#   returns the sum of the lengths of all intervals in the collection.
#
# - If collection denotes an IntervalCollection object, then
#   collection.add_interval(interval)
#   adds interval to the collection, merging with all overlapping
#   or touching intervals if needed, so that the collection remains
#   normalised.
#   An IntervalCollectionError is raised with message:
#       Cannot create an IntervalCollection: invalid intervals
#   if the argument is not an Interval object.
#
# Notes
#
# - A collection is always stored in normalised form:
#   intervals are sorted by increasing left endpoint, and no two stored
#   intervals overlap or touch.
#
# - A one-point interval [a, a] has length 0.
#
# - You can assume that comparisons only involve Interval objects.
#
# - You can assume that IntervalCollection() is always called
#   with at least one argument.


from numbers import Real
from functools import total_ordering


# DEFINE AN EXCEPTION CLASS
class IntervalError(Exception):
    def __init__(self, message):
        super().__init__(message)

@total_ordering
class Interval:
    def __init__(self, a, b):
        # if not isinstance(a, Real) or not isinstance(b, Real) or a > b:
        if not (isinstance(a, Real) and not isinstance(a, bool)) or not (isinstance(b, Real) and not isinstance(b, bool)) or a > b:
            raise IntervalError("Cannot create an Interval: invalid endpoints")
        
        self.a = a
        self.b = b

    def __str__(self):
        return f"[{self.a}, {self.b}]"

    def __repr__(self):
        return f"Interval({self.a}, {self.b})"
    
    def __eq__(self, other):
        if self.a == other.a and self.b == other.b:
            return True
        return False
    
    def __lt__(self, other):
        if self.a == other.a:
            return self.b < other.b
        return self.a < other.a
    
    def overlaps(self, other):
        if self.a <= other.b and other.a <= self.b:
            return True
        return False
    
    def merge(self, other):
        if self.overlaps(other):
            return Interval(min(self.a, other.a), max(self.b, other.b))
        else:
            raise IntervalError("Cannot merge non-overlapping intervals")

    def length(self):
        return self.b - self.a
    # REPLACE PASS ABOVE WITH YOUR CODE


# DEFINE ANOTHER EXCEPTION CLASS
class IntervalCollectionError(Exception):
    def __init__(self, message):
        super().__init__(message)

class IntervalCollection:
    def __init__(self, *intervals):
        self.intervals = []
        for interval in intervals:
            if not isinstance(interval, Interval):
                raise IntervalCollectionError("Cannot create an IntervalCollection: invalid intervals")
        
        sorted_input = sorted(intervals)
        for i in range(len(sorted_input) - 1):
            if sorted_input[i].overlaps(sorted_input[i+1]):
                raise IntervalCollectionError("Cannot create an IntervalCollection: invalid intervals")
        
        self.intervals = sorted_input

    def add_interval(self, interval):
        if not isinstance(interval, Interval):
            raise IntervalCollectionError("Cannot create an IntervalCollection: invalid intervals")
        new_intervals = []
        for existing_interval in self.intervals:
            if existing_interval.overlaps(interval):
                interval = interval.merge(existing_interval)
            else:
                new_intervals.append(existing_interval)
        
        new_intervals.append(interval)
        self.intervals = sorted(new_intervals)

    def __str__(self):
        return "Interval collection made of: " + ", ".join(str(interval) for interval in self.intervals)
    
    def __repr__(self):        
        return "IntervalCollection(" + ", ".join(repr(interval) for interval in self.intervals) + ")"
        
    def __contains__(self, interval):
        if not isinstance(interval, Interval):
            return False
        
        for existing_interval in self.intervals:
            if existing_interval.a <= interval.a and existing_interval.b >= interval.b:
                return True
        return False
    
    def total_length(self):
        total = 0
        for interval in self.intervals:
            total += interval.b - interval.a
        return total
    
if __name__ == "__main__":
    interval_1 = Interval(1, 3)
    interval_2 = Interval(3, 4)
    interval_3 = Interval(5, 6)
    collection = IntervalCollection(interval_1, interval_2)
    collection.add_interval(interval_2)
    print(collection)