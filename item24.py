# Item 24: Use @classmethod Polymorphism to Construct Objects Generically
import os
from threading import Thread

# Like other object-oriented languages, Python supports polymorphism, i.e. that different classes in a hierarchy
# provide their own version of a method.
# Suppose you want to write an implementation of the MapReduce pattern and need a class to represent input data:


class InputData(object):
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

# And similarly you want to write a worker class to be subclassed:
class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

# A concrete class for counting the number of lines could look like this:
class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        count = data.count('\n')

    def reduce(self, other):
        self.result += other.result

# What is still lacking is an orchestrating component that constructs and creates the different objects. A simple
# approach would be to use a helper functions:
def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

# Basic thread-level parallelism can be achieved using threads:
def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result

# Finally, these functions can be connected using a further helper function:
def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

# This can now be used like this:
from tempfile import TemporaryDirectory

def write_test_files(tmpdir):
    # ...
    pass

with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    result = mapreduce(tmpdir)

print('There are', result, 'lines')


# The problem with this approach is that the mapreduce function is not generic at all. If you want to use another
# InputData or Worker subclass, all helper functions need to be rewritten.
# Thus, we need a generic way to create objects. Because Python only allows one constructor per class, overloading it
# is not an option here and would require each subclass to implement one. The best way to solve this is to use
# @classmethod (class-level) # polymorphism, which applies to the whole class instead of constructed objects. E.g:
class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError

# Subclasses use the config argument to actually create the inputs:
class PathInputData(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

# Similarly for the worker class:
class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):  # Class polymorphism
            workers.append(cls(input_data))
        return workers

# LineCountWorker can be adapted to this by simply changing the parent class:
class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        count = data.count('\n')

    def reduce(self, other):
        self.result += other.result

# Now we can rewrite the mapreduce function to be completely generic:
def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

# Now the usage example can be rewritten like this:
with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    config = {'data_dir': tmpdir}
    result = mapreduce(LineCountWorker, PathInputData, config)

