# Item 10: Prefer enumerate Over range

# range is useful for iterating over a set of integers, e.g.:
for i in range(10):
    print(i**2)

# It's possible to iterate directly over a sequence, e.g.:
flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for flavor in flavor_list:
    print('%s is delicious' % flavor)

# If you want to iterate over a list and also know the item's index, sometimes the range function is used:
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print('%d: %s' % (i+1, flavor))

# However, replacing this with enumerate - which returns a lazy generator - makes the code more readable:
for i, flavor in enumerate(flavor_list):
    print('%d: %s' % (i+1, flavor))

# Alternatively, if the counting should start at 1, this can be passed as the second parameter to enumerate:
for i, flavor in enumerate(flavor_list, 1):
    print('%d: %s' % (i, flavor))