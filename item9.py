# Item 9: Consider Generator Expressions for Large Comprehensions

# For very large input, list comprehensions that may create an output item for a good proportion of their input
# items, can be very memory-intensive. An example for this is the line-wise reading and counting of line length
# for an enormous input file.
value = [len(x) for x in open('/tmp/somelargefile.txt')]

# To solve this problem, Python offers generator expressions which don't evaluate to a whole new list at once,
# but return an iterator that yields one element at a time. Above example can be rewritten to use a generator
# like the following, basically simply replacing [] with ():
it = (len(x) for x in open('/tmp/somelargefile.txt'))

# Values can be retrieved using the next() call:
next(it)

# One caveat is that the returned iterators are stateful, so they cannot be used more than once (see item 17).
