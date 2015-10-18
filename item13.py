# Item 13: Take Advantage of Each Block in try/except/else/finally

import json

# Use try/finally when the exception should be propagated up, but cleanup code should be executed before, e.g.:
handle = open('/tmp/somefile.txt')
try:
    data = handle.read()
finally:
    handle.close()

# In this example, it is important to open the handle before the try block to make sure that the close operation
# does not cause an IOError in the finally block.

# Use try/except/else to make clear which exceptions are propagated up and which are handled by your code, e.g.:
def load_json_key(data, key):
    try:
        result_dict = json.loads(data)
    except ValueError as e:
        raise KeyError from e
    else:
        return result_dict[key]

# If the JSON is not valid, the except block will catch and handle it. If they key lookup fails, the resulting
# exception is propagated up and not handled by the method.


# An all-together-example. Read description from a file, process and update it.
# try: Read and process
# except: Handle exceptions
# else: Update file, let unhandled exceptions propagate
# finally: Closes file handle
UNDEFINED = object()

def divide_json(path):
    handle = open(path)             # May raise IOError
    try:
        data = handle.read()        # May raise UnicodeDecodeError
        op = json.loads(data)       # May raise ValueError
        value = (
            op['numerator'] /
            op['denominaor'])       # May raise ZeroDivisionError
    except ZeroDivisionError as e:
        return UNDEFINED
    else:
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)        # May raise IOError
        return value
    finally:
        handle.close()              # Always runs, even if else throws an exception


