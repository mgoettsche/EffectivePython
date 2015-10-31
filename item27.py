# Item 27: Prefer Public Attributes Over Private Ones

# There are two types of attribute visibility in Python classes: public and private
class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field

foo = MyObject()
assert foo.public_field == 5
assert foo.get_private_field() == 10

# print(foo.__private_field)  # AttributeError: 'MyObject' object has no attribute '__private_field'

# Private variables cannot be accessed from outside of the class, but classmethods can access them:
class MyOtherObject(object):
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71

# Subclasses can't access a parent's private fields:
class MyParentObject(object):
    def __init__(self):
        self.__private_field = 71

class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field

baz = MyChildObject()
# baz.get_private_field() # AttributeError: 'MyChildObject' object has no attribute '_MyChildObject__private_field'

# However, Python does not strictly prevent access to private fields from the outside, because private variables
# are internally only renamed to prevent them from being accessed. With this knowlege, it is easy to access them
# anyway:
assert baz._MyParentObject__private_field == 71 # No error

print(baz.__dict__)
# {'_MyParentObject__private_field': 71}

# The reasoning for this is Python's motto that "We are all consenting adults here".
# Besides, prefixing a variable with a single underscore is established as a convention to indicate a proteced variable.
# However, many novice Pythoners use private fields to prevent subclasses from making modifications. E.g:
class MyClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)

foo = MyClass(5)
assert foo.get_value() == '5'

# Suppose someone wants to instead return the value as an integer. The user is then forced to access the private
# variable via its "hidden" name:
class MyIntegerSubclass(MyClass):
    def get_value(self):
        return int(self._MyClass__value)

foo = MyIntegerSubclass(5)
assert foo.get_value() == 5

# But this approach is going to break if the class hierarchy changes. Suppose the MyClass class itself has a superclass
# which now holds the private variable:
class MyBaseClass(object):
    def __init__(self, value):
        self.__value = value

class MyClass(MyBaseClass):
    def get_value(self):
        return str(self.__value)

class MyIntegerSubclass(MyClass):
    # ...
    def get_value(self):
        return int(self._MyClass__value)

foo = MyIntegerSubclass(5)
# foo.get_value() #   AttributeError: 'MyIntegerSubclass' object has no attribute '_MyClass__value'


# Instead, it is better to use protected attributes and document them which ones can be subclassed and which ones
# should be left alone. E.g:
class MyClass(object):
    def __init__(self, value):
        # This stores the user-supplied value for the object.
        # It should be coercible to a string. Once assigned for
        # the object it should be treated as immutable.
        self._value = value

# Private attributes should only be considered when there is reason to be worried about naming conflicts with
# subclasses. E.g:
class ApiClass(object):
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # Conflicts

a = Child()
print(a.get(), 'and', a._value, 'should be different')

# hello and hello should be different

# This can especially happen if you use an attribute name that is very common like "value". By making it private, the
# conflict can be resolved:
class ApiClass(object):
    def __init__(self):
        self.__value = 5

    def get(self):
        return self.__value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # OK!

a = Child()
print(a.get(), 'and', a._value, 'are different')

# 5 and hello are different

# To summarize, private variables should only be used to avoid naming conflicts and their privateness is not
# enforced anyway. Protected fields should be documented to guide users what they should and should not do when
# subclassing.