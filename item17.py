# Item 17: Be Defensive When Iterating Over Arguments

# Sometimes you want to iterate over a parameter to a function twice, e.g. to normalize some input. An example
# would be to calculate the share of total visitors each city has.
def normalize(numbers):
    total = sum(numbers)
    result = []
    for number in numbers:
        percent = number * 100 / total
        result.append(percent)
    return result

visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)

# This works well if numbers is passed as a container. However, if you read in the numbers via a generator
# for reasons as described in item 16, the normalize function won't work.
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield line

it = read_visits('/tmp/somefile')
percentages = normalize(it)
print(it)

# The results list will be empty, because the iterator is exhausted after the iteration caused by calling sum.
# What's more, the function will not even throw an error. A way around this is to make a copy of the input at
# the beginning of the normalize function:
def normalize_copy(numbers):
    numbers = list(numbers)     # Copy the iterator
    total = sum(numbers)
    result = []
    for number in numbers:
        percent = number * 100 / total
        result.append(percent)
    return result

# This version will work correctly with an iterator as input. However, this is not a very elegant solution
# as it doubles the memory usage and could cause the program to run out of memory. An ugly work-around is to accept
# a function as input which will return an iterator every time it is called:
def normalize_func(get_iter):
    total = sum(get_iter())     # New iterator
    result = []
    for number in get_iter():
        percent = number * 100 / total
        result.append(percent)
    return result

# With the previously defined read_visits function, a call to normalize_func could look like this:
percentages = normalize_func(lambda path: read_visits(path))

# Still, this is clumsy from the perspective of the user of the function.
# A better way to achieve the same result is to implement a container class that implements the iterator protocol.
# The iterator protocol is how Python handles traversals in for loops etc. in general. A call like for x in foo
# will call iter(foo) to get an iterator for foo (iter in turn will call foo.__iter__). For this to work, foo's
# class must implement the __iter__ method to return an iterator. The for loop can then subsequently call __next__
# to receive the next elements.
# For our case, the wrapper class could look like this:
class ReadVisits(object):
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path):
            for line in f:
                yield int(line)

# This can be passed to the unmodified normalize function:
visits = ReadVisits('/tmp/somefile')
percentages = normalize(visits)

# This works because a new iterator will be created for every loop, in this case for the summation and the iteration
# over each value.

# Finally, we can defend our function against normal iterators to ensure it works correctly:
def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers):              # Must be an iterator!
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for number in numbers:
        percent = number * 100 / total
        result.append(percent)
    return result

# This will work for lists, ReadVisits and generally any object that implements the iterator protocol.

visits = [15, 35, 80]
percentages = normalize(visits)     # No error
visits = ReadVisits('/tmp/somefile')
percentages = normalize(visits)     # No error
it = iter(visits)
percentages = normalize(it)         # TypeError: Must supply a container

# Another take-away of this item is that you can easily implement your own iterable container type by implementing
# the __iter__ method as a generator.
