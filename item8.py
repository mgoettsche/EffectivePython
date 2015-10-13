# Item 8: Avoid More Than Two Expressions in List Comprehensions

# The following two uses of two expressions in list comprehensions are readable:
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)

squared = [[x**2 for x in row] for row in matrix]
print(squared)

# The following with three is not as much:
my_lists = [
    [[1, 2, 3], [4, 5, 6]]#, ...
]

flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]

# Replacing this with normal loop statements makes it more readable:
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)


# Using conditionals in list comprehensions is fine in cases like this:
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0] # equivalent to b

# In nested comprehensions, however, they harm the readability:
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]
print(filtered)

# The resulting rule of thumb is to avoid more than two expressions in list comprehensions, be it conditions
# or loops. Not following that rule makes it much harder for others to read your code and saving a few lines
# doesn't outweigh this.