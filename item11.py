# Item 11: Use zip to Process Iterators in Parallel

# Suppose you have two related lists
names = ['Cecilia', 'Lise', 'Marie']
letters = [len(n) for n in names]

# One way to iterate over both lists is to iterate over the length of the first. The following is an example for
# this and looks for the name with the maximum length:
longest_name = None
max_letters = 0

for i in range(len(names)):
    count = letters[i]
    if count > max_letters:
        longest_name = names[i]
        max_letters = count

print(longest_name)

# This however is visually noisy, using enumerate (as in item 10) improves this slightly as it removes one
# indexing operation:
for i, name in enumerate(names):
    count = letters[i]
    if count > max_letters:
        longest_name = name
        max_letters = count

# Using the built-in zip function, which wraps iterators together, this can be expressed more clearly:
for name, count in zip(names, letters):
    if count > max_letters:
        longest_name = name
        max_letters = count

# One caveat is that zip will only return values until one iterator is exhausted, so if there are still items
# in the other list, these won't be returned.
names.append('Rosalind')
for name, count in zip(names, letters):
    print(name)  # will only print until 'Marie'

#  In such cases, itertool's zip_longest may be considered as an alternative.