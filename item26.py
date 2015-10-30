# Item 26: Use Multiple Inheritance Only for Mix-in Utility Classes
import json

# Multiple Inheritance should be avoided in general. An exception to this are so-called mix-ins, i.e. classes that
# only define a set of methods, but have no own instance attributes and no need for an __init__ constructor to be
# called.
# Suppose e.g. you want to write the functionality to convert an object to a dictionary representation that can be
# serialized. Since this can be useful for different classes, it's worth to make it generic:


class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse(dict)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

# This mix-in can easily be used e.g. in a binary tree class to create a dict representation of it:
class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinaryTree(10,
                  left = BinaryTree(7, right=BinaryTree(9)),
                  right = BinaryTree(13, left=BinaryTree(11)))
print(tree.to_dict())

# {'value': 10,
# 'right': {'value': 13, 'right': None, 'left': {'value': 11, 'right': None, 'left': None}},
# 'left': {'value': 7, 'right': {'value': 9, 'right': None, 'left': None}, 'left': None}}

# Of course, the behavior of the mix-in functions can be overriden in the child classes. Suppose e.g. you want to
# subclass BinaryTree and want the subclass to hold a reference to its parent. This circular reference would cause
# the to_dict method to enter an infinite loop:
class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

# The solution is to override to_dict to not traverse the parent:
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value  # Prevent cycles
        else:
            return super()._traverse(key, value)

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right =  BinaryTreeWithParent(9, parent=root.left)
print(root.to_dict())

# {'left': {'left': None, 'value': 7, 'right': {'left': None, 'value': 9, 'right': None, 'parent': 7}, 'parent': 10},
# 'value': 10,
# 'right': None,
# 'parent': None}

# Any class that has an attribute of type BinaryTreeWithParent now also works with ToDictMixin:
class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubTree('foobar', root.left.right)
print(my_tree.to_dict())

# {'name': 'foobar', 'tree_with_parent': {'parent': 7, 'right': None, 'value': 9, 'left': None}}


# One class can use multiple mix-ins. Suppose you also want to be able to serialize to a JSON representation, you could
# write the following class:
class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())

# Note that the class defines an instance method and a class method. The class method is responsible for creating an
# object from given data while the instance method converts an object to a JSON representation. In this implementation
# JsonMixin requires the child classes to have a to_dict method and __init__ constructor which takes keyword arguments.
# Example using a class that represents part of a datacenter topology:
class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [
            Machine(**kwargs) for kwargs in machines]

class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports, speed):
        self.ports = ports
        self.speed = speed

class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores, ram, disk):
        self.cores = cores
        self.ram = ram
        self.disk = disk

serialized = """{
    "switch": {"ports":5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 4, "ram": 16e9, "disk": 1e12},
        {"cores": 2, "ram": 4e9, "disk": 500e9}
        ]
    }"""
deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)


