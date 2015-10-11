# Item 4: Write Helper Functions Instead of Complex Expressions

# Example: Parse parameters of an URL.

from urllib.parse import parse_qs
my_values = parse_qs('red=5&blue=0&green=',
                     keep_blank_values=True)
print(repr(my_values))

# Suppose you want to print the URL parameters' values
print('Red:     ', my_values.get('red'))
print('Green:    ', my_values.get('green'))
print('Opacity:   ', my_values.get('opacity'))

# Red:      ['5']
# Green:     ['']
# Opacity:    None

# Now, empty values should default to 0 instead of '' or None. What is the best way to achieve this?
# First option is to provide a default parameter to the get function and check for its return value:
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print('Red:     %r' % red)
print('Green:   %r' % green)
print('Opacity: %r' % opacity)

# Red:     '5'
# Green:   0
# Opacity: 0

# Yet, this code is difficult to read, especially if you want the values as ints:
red = int(my_values.get('red', [''])[0] or 0)
green = int(my_values.get('green', [''])[0] or 0)
opacity = int(my_values.get('opacity', [''])[0] or 0)

# A better way would be to at least split this into two expressions, second being a ternary one, e.g.:
red = my_values.get('red', [''])
red = int(red[0]) if red[0] else 0

# However, if you use this logic more often, a helper function is a better choice:
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found:
        found = found[0]
    else:
        found = default
    return found

# Which can be used like:
red = get_first_int(my_values, 'red')

# Helper functions improve readability of the code compared to complex expressions. 





