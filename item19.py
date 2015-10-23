# Item 19: Provide Optional Behavior with Keyword Arguments

# Like in most languages, arguments in Python can be passed by position:
def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6

# Positional arguments can also be called with keywords, i.e. the name of the arguments, as long as all positional
# arguments are specified. E.g.:
remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)

# Positional arguments must be specified before keyword arguments:
remainder(number=20, 7)     # SyntaxError: non-keyword arg after keyword arg

# Each argument can only be specified once:
remainder(20, number=7)     # TypeError: remainder() got multiple values for argument 'number'

# The first advantage of keywords arguments is that they make the code easier to read, because you don't need to know
# the function definition to know which argument is which.
# A second advantage is that they can have default values specified. This allows to enable additional capabilities while
# providing good default behavior at the same time.

# Example: Compute the rate of a fluid flowing into a vat. If the vat is on a scale, you can use the weight and time
# difference between two measurements to calculate the flow rate.
def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print('%.3f kg per second' % flow)

# Usually, the user will want to know the flow per second. However sometimes other time scales might be interesting.
# This functionality can be added using a third parameter called period:
def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period

# But this requires the user to include the parameter in the function call every time:
flow_per_second = flow_rate(weight_diff, time_diff, 1)

# This can be made less noisy by giving period a default value:
def flow_rate(weight_diff, time_diff, period=1):
     return (weight_diff / time_diff) * period

flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)

# A third advantage is that keyword parameters allow to extend the function's parameters without having to migrate
# the function calls. In this example, the flow_rate function is modified to calculate other units than kilograms:
def flow_rate(weight_diff, time_diff, period=1, units_per_kg=2.2):
    return ((weight_diff / units_per_kg) / time_diff) * period

# The remaining problem is that the optional arguments can be passed as positional arguments, making it unclear
# what their values correspond to, e.g:
pounds_per_hours = flow_rate(weight_diff, time_diff, 3600, 2.2)

# The best practice is to specify optional arguments via their keyword and never pass them as positional arguments.


