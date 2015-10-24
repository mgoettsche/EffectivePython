# Item 20: Use None and Docstrings to Specify Dynamic Default Arguments
from datetime import datetime
import json
from time import sleep

# Suppose you want to write a function for logging messages where by default the messages are printed together
# with the current time. An approach one might try is the following:
def log(message, when=datetime.now()):
    print('%s: %s' % (when, message))

log('Hi there!')
sleep(0.1)
log('Hi again!')

# 2015-10-23 12:13:09.019511: Hi there!
# 2015-10-23 12:13:09.019511: Hi again!

# Contrary to what one might expect, the timestamps are the same. This is because the datetime.now() call is executed
# only once when the module loads, so all calls to the log function will have the same timestamp.
# The convention for such cases is to give such an argument the default of None and document its actual behavior
# in the docstring.
def log(message, when=None):
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occured.
            Defaults to the present time.
    """
    when = datetime.now() if when is None else when
    print('%s: %s' % (when, message))

log('Hi there!')
sleep(0.1)
log('Hi again!')

# 2015-10-23 13:39:34.573864: Hi there!
# 2015-10-23 13:39:34.674155: Hi again!

# When arguments are mutable, using None is especially important. Suppose you want to return an empty dictionary
# when the input to the function was invalid:
def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

# This will behave very surprisingly:
foo = decode('bad data')
foo['stuff'] = 5
bar = decode('bad data')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)

# Foo: {'stuff': 5, 'meep': 1}
# Bar: {'stuff': 5, 'meep': 1}

# In fact, both are the same dictionaries instead of two different ones with one key each. This can be fixed by
# setting the default for default to None.
def decode(data, default=None):
    if default is None:
        default = {}
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('bad data')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)

# Foo: {'stuff': 5}
# Bar: {'meep': 1}


