# Item 7: Use List Comprehensions Instead of map and filter

# E.g.
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [x**2 for x in a]

# is preferable to
squares = map(lambda x: x**2, a)

# as creating a lambda function is more visually noisy. Also, it is easier to perform a filtering step, e.g.:
even_squares = [x**2 for x in a if x % 2 == 0]

# is easier to read than
even_squares = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))


# Dictionaries and sets have equivalents for list comprehensions:
chile_ranks = {'ghost': 1, 'habanero': 2, 'cayenne': 3}
rank_dict = {rank: name for name, rank in chile_ranks.items()}  # Reversal of keys/values
chile_len_set = {len(name) for name in rank_dict.values()}  # Lengths of chili names

print(chile_ranks)
print(rank_dict)
print(chile_len_set)
