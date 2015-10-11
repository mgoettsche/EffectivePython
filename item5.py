# Item 5: Know How to Slice Sequences

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('First Four:', a[:4])
print('Last Four:', a[-4:])
print('Middle two:', a[3:-3])

# Starting 0 is not necessary:
assert a[0:5] == a[:5]

# Neither is end:
assert a[5:] == a[5:len(a)]

# Some examples
a           # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
a[:5]       # ['a', 'b', 'c', 'd', 'e']
a[:-1]      # ['a', 'b', 'c', 'd', 'e', 'f', 'g']
a[4:]       # ['e', 'f', 'g', 'h']
a[-3:]      # ['f', 'g', 'h']
a[2:5]      # ['c', 'd', 'e']
a[2:-1]     # ['c', 'd', 'e', 'f', 'g']
a[-3:-1]    # ['f', 'g']

# Exceeding the boundaries causes no exceptions:
first_twenty_items = a[:20] # == a
last_twenty_items = a[-20:] # == a

# Slicing can be used in assignments one way or the other:
b, c = a[:2]  # b='a', c='b'
a[3:6] = 'i'  # ['a', 'b', 'c', 'i', 'g', 'h'] - 'd' replaced, 'e' and 'f' missing
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
a[3:6] = ['i', 'i', 'i']  # ['a', 'b', 'c', 'i', 'i', 'i', 'g', 'h'] - all three placed with 'i'

# Without boundaries, slicing returns the original sequence
assert a == a[:]
