# Returns a generator that, whenever advanced, prints the
# next frame of an endlessly repeating 4-step animation.
#
# The successive frames printed are:
#
#  /\
# /  \
#
# ----
#
# \  /
#  \/
#
#  ||
#  ||
#
# After the fourth frame, the animation starts again from
# the first one.

def f1():
    while True:
        print(" /\\")
        print("/  \\")
        yield 
        print('----')
        yield 
        print('\\  /')
        print(' \\/')

        yield 
        print(' ||')
        print(' ||')
        yield
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE

f1()
