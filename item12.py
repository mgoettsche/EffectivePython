# Item 12: Avoid else blocks after for and while loops

# Python has the unusual feature of allowing else blocks right after loops:
for i in range(3):
    print('Loop: %d' % i)
else:
    print('Else Block')

# Output:
# Loop: 0
# Loop: 1
# Loop: 2
# Else Block

# Contrary to what one might expect, the else block executes every time the loop has completed, even if there were
# no iterations:
for x in []:
    print('Never runs')
else:
    print('For else block')

# Output:
# For else block

# The else block will only then be skipped if the loop is exited early using break, e.g.:
a = 4
b = 9
for i in range(2, min(a, b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')

# Output:
# Testing 2
# Testing 3
# Testing 4
# Coprime

# Using this approach is not recommended. Instead, using a helper function will make the code more readable:
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True

# Alternatively, one can use a result variable:
def coprime2(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime

# Both approaches are much better to understand and thus should be preferred over the for/else construct.


