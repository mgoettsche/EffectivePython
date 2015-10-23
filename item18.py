# Item 18: Reduce Visual Noise with Variable Positional Arguments

# Suppose you want to write a function for logging debug information with a message and optional list of values:
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, values_str))

log('My numbers are', [1, 2])
log('Hi there', [])

# Having to pass an empty list if there are no values is noisy. It is possible to make the parameter optional by
# turning it into a so-called star argument:
def log(message, *values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, values_str))

log('My numbers are', [1, 2])
log('Hi there')     # Much better

# If you already have a list that you want to pass as values parameter, it can be done like this:
favorites = [7, 33, 99]
log('Favorite colors', *favorites)

# There are two problems with accepting positional arguments.
# First: Python will turn the arguments into a tuple. If you pass an iterator, it will iterate over it until it is
# exhausted and pass the values as a list. This produces the same memory shortage problem that we have seen in e.g.
# item 16. hus, positional arguments are best suited for cases where you know that the number of variable arguments is
# small.
def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = my_generator()
my_func(*it)

# (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

# Second problem: Adding positional argument to the function requires migrating every caller. If you add a positional
# argument in front, all calls that are not migrated for this change will break. Example:

def log(sequence, message, *values):
    if not values:
        print('%s: %s' % (sequence, message))
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s: %s' % (sequence, message, values_str))

log(1, 'Favorites', 7, 33)      # New usage is OK
log('Favorite numbers', 7, 33)  # Old usage breaks

# In the second call, 7 is mistakenly treated as the message. Bugs like these are hard to trace as they don't cause
# an exception.

# To summarize, *args should be used to function usage convenient to use and easy to read, but you have to be
# cautious when adding new positional arguments or passing generators.
