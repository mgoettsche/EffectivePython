# Item 23: Accept Functions for Simple Interfaces Instead of Classes
from collections import defaultdict

# The behavior of many of Python's built-in functions can be modified by passing them a function. This works because
# functions are first-class objects so they can be passed around and referenced like other objects. For example,
# the sort function takes a key argument to determine the sort order:

names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=lambda x: len(x))
print(names)

# ['Plato', 'Socrates', 'Aristotle', 'Archimedes']

# These so-called hooks are called during the execution of the function. For example, the defaultdict class calls a
# user-supplied function every time a missing key is accessed to ask it for the corresponding default value. If you
# want to log such accesses and return 0, it can be done like this:
def log_missing():
    print('Key added')
    return 0

current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]

result = defaultdict(log_missing, current)
print('Before', dict(result))
for key, amount in increments:
    result[key] += amount

print('After', dict(result))

# Before {'blue': 3, 'green': 12}
# Key added
# Key added
# After {'blue': 20, 'red': 5, 'orange': 9, 'green': 12}

# Supplying functions this way makes it easy to separate side effects from deterministic behavior and facilitates
# replacing the function. Suppose you now want to just count the number of failed accesses. Using a stateful closure
# (see item 15) this can be done like this:

def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count  # Stateful closure
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount
    return result, added_count

result, count = increment_with_report(current, increments)
assert count == 2

# However, the problem with this closure-based approach is that it is harder to read than the stateless function
# example. A class that encapsulates the state makes the code easier to understand:
class CountMissing(object):
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0

# Thanks to functions being first-class objects, with this modification you can still reference the method directly
# and pass it to defaultdict:
counter = CountMissing()
result = defaultdict(counter.missing, current)  # Method ref

for key, amount in increments:
    result[key] += amount

assert counter.added == 2

# Though this is better to read than the increment_with_report function, one problem remains: In isolation it is
# unclear what the purpose of the class is. Without seeing it in context with the defaultdict, it is a mystery and
# you don't know who is reponsible for calling the missing() function. This can be solved by replacing missing() with
# the __call__ special function that allows an object to be called like a function.
class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
assert callable(counter)

result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount

assert counter.added == 2

# This is clearer than the CountMissing class. By looking at the __call__ method the reader knows that the class
# is supposed to be used as a function somewhere and provides hint that the class will act as a stateful closure.
# For a function like defaultdict it makes no difference whether you pass it a normal function or a callable class.
# To summarize, a function interface can be satisfied via different ways from an anonymous lambda function to a class
# depending on the needs.
