# Item 15: Know How Closures Interact with Variable Scope

# Suppose you want to sort a list of numbers and prioritize based on the group to which they belong.
# This can be done by passing a helper function (key) to sort which leads to sort returning the items
# from the group first. E.g:

def sort_priority(numbers, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)

# There are three things to note here:
# - helper as a so-called closure can access variables from the scope within which it is defined, in this case
# it uses this to access the group set.
# - Functions are first-class objects and can therefore (besides e.g. assigning them to variables, using them in
# if statements etc.) be passed as a parameter to a function. In this case, helper is passed to sort.
# - Python compares tuples based on their index, so tuples (0, x) come before (1, x).

# Suppose you also want to know whether the sorted numbers were from separate groups at all to act accordingly.
# A wrong way to try this using a flag is the following:

def sort_priority2(numbers, group):
    found = False           # Scope: 'sort_priority2'
    def helper(x):
        if x in group:
            found = True    # Scope: 'helper'
            return(0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

# This won't work, because in the scope of helper, found is regarded as a new variable instead of assigning
# a new value to sort_priority2's found variable. This is referred to as the "scoping bug", because it is
# surprising to newcomers, however it is well intended as to prevent pollution of the containing module.

# A working alternative is to declare the variable as nonlocal in the helper function. This will look for the
# variable in the enclosing scope in an assignment, but unlike global not traverse up to the global namespace
# as to avoid pollution of globals.

def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1,x)
    numbers.sort(key=helper)
    return found


# Similar to the advice to avoid global variables, the use of nonlocal should be restricted to very simple functions
# as it can become hard to follow the side effects of nonlocal in more complex code. So, in more complicated
# situations a wrapper class is a better solution:
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True


# Important: The nonlocal keyword does not exist in Python 2. Here, an ugly work-around is to use a list instead, i.e.
# found = [False] in the declaration and found[0] = True in the assignment. The reason this works is that found[0] is
# a reference to a variable, which will look not only in the current's function scope, but traverse up and find it
# in the enclosing function. Therefore, no new variable is created, but a new value assigned to the existing found.