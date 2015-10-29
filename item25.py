# Item 25: Initialize Parent Classes with super

# The old way to initialize parent class from a child class is a direct call to __init__:
class MyBaseClass(object):
    def __init__(self, value):
        self.value = value

def MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)

# For simple hierarchies this approach is fine, but for more complex ones it can break.
# First: Multiple Inheritance (which in general should be avoided, see item #26)
# Here, the call order is important, e.g.:
class TimesTwo(object):
    def __init__(self):
        self.value *= 2

class PlusFive(object):
    def __init__(self):
        self.value += 5

# First ordering variant:
class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

foo = OneWay(5)
print('First ordering is (5 * 2) + 5 =', foo.value)

# First ordering is (5 * 2) + 5 = 15

# Second ordering variant:
class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

bar = AnotherWay(5)
print('Second ordering still is', bar.value)

# Second ordering still is 15

# Despite the different order in the parent class list (but the same order in calls to __init__), the initialization
# is in the same order as before and thus does not match the expected result.

# Second: Diamond Inheritance (i.e. subclass with two superclasses that share a superclass)
class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5

class PlusTwo(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2

class ThisWay(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)

foo = ThisWay(5)
print('Should be (5 * 5) + 2 = 27 but is', foo.value)

# Should be (5 * 5) + 2 = 27 but is 7
# What happens here is that the constructor for MyBaseClass is called twice, (re)setting it to 5 each time.

# To solve such problems, Python 2.2:
# 1. Introduced the super() built-in function
# 2. Introduced the method-resolution order (MRO) that standardizes the order of superclass initializations and
# ensures that common superclasses constructors are executed only once in diamond hierarchies.

# < Skip Python 2 Example >

# Python 3 fixes problems with the Python 2 approach, making it less verbose and less error-prone (by removing the
# need to specify the current's class name in the call to the superclass).
# Small usage example:
class Explicit(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)

class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)

assert Explicit(10).value == Implicit(10).value

# To summarize: Parent classes should always be initialized using super() to make the code shorter. Python's
# method-resolution order ensures correct initialization in complex hierarchies. 