# Item 6: Avoid Using start, end and stride in a Single Slice

# Using a third parameter it is possible to select every n'th element in a slice operation
a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = a[::2]  # ['red', 'yellow', 'blue']
evens = a[1::2]  # ['orange', 'green', 'purple']

# A common trick to reverse a byte string is the use of -1.
# # This however does not work for unicode characters encoded as UTF-8 strings.
x = b'mongoose'
y = x[::-1]  # b'esoognom'

# While this is easy to understand, other slice operations are harder to understand, especially when all three
# parameters are provided and/or when they are negative:
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
a[2::2]         # ['c', 'e', 'g']
a[-2::-2]       # ['g', 'e', 'c', 'a']
a[-2:2:-2]      # ['g', 'e']
a[2:2:-2]       # []

# Such slice operations should be avoided to maintain readability. A better way is to separate into a slice and
# a stride operation, e.g.:
b = a[::2]      # ['a', 'c', 'e', 'g']
c = b[1:-1]     # ['c', 'e']

# If this method is too costly from a memory or runtime perspective, 'islice' of the package 'itertools' poses
# an alternative that doesn't permit negative start/end/stride values.





