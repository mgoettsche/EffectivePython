# Item 21: Enforce Clarity with Keyword-Only Arguments

# Suppose you want to write a safe division function for which the caller can specify how to handle ZeroDivisionError
# and OverflowError exceptions:
def safe_division(number, divisor, ignore_overflow, ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

result = safe_division(1, 10**500, True, False)  # Ignores overflow from division and returns zero
print(result)   # 0.0

result = safe_division(1, 0, False, True)   # Ignores errors from dividing by zero and returns infinity
print(result)   # inf

# The problem with this approach is that it is easy to confuse their positions. By using keyword arguments the
# readability is improved:
def safe_division_b(number, divisor, ignore_overflow=False, ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

safe_division_b(1, 10*500, ignore_overflow=True)
safe_division_b(1, 0, ignore_zero_division=True)

# The problem with this approach is that the arguments are now optional and that they can still be called in a
# positional fashion.
# In Python 3 it is possible to declare arguments keyword-only using the * operator
# so that they cannot be passed as positional arguments:
def safe_division_c(number, divisor, *,
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# Now a call with all arguments positional won't work:
safe_division_c(1, 10*500, True, False)  #  TypeError: safe_division_c() takes 2 positional arguments but 4 were given

# Keyword arguments and their default values work:
safe_division_c(1, 0, ignore_zero_division=True)    # OK

try:
    safe_division_c(1, 0)
except ZeroDivisionError:
    pass    # Expected

# In Python 2, keyword arguments can be enforced with the **kwargs argument which is similar to *args, but accepts
# keyword arguments instead of position arguments. (No code example here because I am more interested in the
# Python 3 way to do things.)
