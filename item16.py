# Item 16: Consider Generators Instead of Returning Lists
from itertools import islice

# Suppose you want to write a function that returns the indexes of every word in a string. Using a list this
# could look like:
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

address = 'Four score and seven years ago...'
result = index_words(address)
print(result)

# There are however two problems with this approach.
# First: Verbosity
# Only about half of the function body is concerned with the actual task. The rest of it creates, populates and returns
# the resulting list. By writing a generator function this becomes much shorter and better to read:
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

# A user might prefer to get a list returned instead. This is easily possible, e.g:
result = list(index_words_iter(address))

# Second: Memory shortage
# If the list of results is too large to fit into memory, the application will crash before returning from the
# function call. With a generator the input can be arbitrarily large. Suppose you want to write a function that
# takes as input a file handle and outputs the word indices one at a time:
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset

with open('/tmp/somefile', 'r') as f:
    it = index_file(f)
    results = islice(it, 0, 3)
    print(list(results))

# Keep in mind that iterators are stateful and can't be reused.
