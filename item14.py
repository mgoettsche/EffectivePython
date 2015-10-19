# Item 14: Prefer Exceptions to Returning None

# Sometimes in writing methods, a special meaning is assigned to None as a return value, e.g.:
def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return None

# The return value can be interpreted accordingly:
result = divide(2, 0)
if result is None:
    print('Invalid inputs')

# However, this can introduce ambiguity. Suppose you look only for False equivalents instead of only Nones:
result = divide(0, 2)
if not result:
    print('Invalid Inputs!')  # This is wrong, should be 0

# A workaround would be to return a tuple instead, where the first value indicates a failure and the second
# contains the result:
def divide(a, b):
    try:
        return True, a/b
    except ZeroDivisionError:
        return False, None

# However, callers may ignore the first part and miss the error. A better way is to raise an exception and
# have the caller deal with it. This, of course, should be documented. E.g:
def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

# Now, the caller checks for an exception and if there is none, the return value must be good:
try:
    result = divide(5, 2)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)

