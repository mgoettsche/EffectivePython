# Item 29: Use Plain Attributes Instead of Get and Set Methods

# Python beginners may be tempted to implement getters and setters as known from other languages, e.g:
class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

# These can be used as usually:
r0 = OldResistor(50e3)
print('Before: %5r' % r0.get_ohms())
r0.set_ohms(10e3)
print('After:  %5r' % r0.get_ohms())

# Before: 50000.0
# After:  10000.0

# While this encapsulation helps in achieving the well-known goals of validation etc., this way of implementing
# attribut access is not Pythonic. In the beginning, you should design your class simply with public attributes:
class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3
r1.ohms += 5e3

# If you later decide that you need custom behavior when an attribute is get/set, use the @property decorator and
# implement both methods:
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

r2 = VoltageResistance(1e3)
print('Before: %5r amps' % r2.current)
r2.voltage = 10
print('After:  %5r amps' % r2.current)

# Before:     0 amps
# After:   0.01 amps

# This can also be used not only to update other attributes' values, but to perform validity checks on the attribute
# itself:
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms

r3 = BoundedResistance(1e3)
# r3.ohms = 0  # ValueError: 0.000000 ohms must be > 0

# foo = BoundedResistance(-5)  # ValueError: 0.000000 ohms must be > 0

# Using @property attributes from parent classes can even be marked immutable:
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms

r4 = FixedResistance(1e3)
# r4.ohms = 2e3  # AttributeError: Can't set attribute

# When using @property, you should not set other attributes in getter methods as this leads to bizarre behavior:
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms

r7 = MysteriousResistor(10)
r7.current = 0.01
print('Before: %5r' % r7.voltage)
r7.ohms
print('After:  %5r' % r7.voltage)

# Before:     0
# After:    0.1

# @property methods should thus have no side effects and not perform complex operations, because users will expect them
# to be fast just like normal attribute access.