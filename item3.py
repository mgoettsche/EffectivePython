# Item 3: Know the Differences Between bytes, str, and unicode

# Python 3 distinguishes between bytes and str for sequences of characters. bytes are raw 8-bit values, str
# unicode-encoded. # str does not have an # associated binary encoding. In programs that require both representations
# often, it is useful to # have two helper functions to perform the conversion.

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value

if __name__ == '__main__':
    text = "Hello world"
    as_bytes = to_bytes(text)
    print(type(as_bytes))
    as_str = to_str(as_bytes)
    print(type(as_str))

# Further, in Python 3 file handles default to utf-8. It is thus not possible to write binary data.
# To be able to write bytes, open with mode 'wb' instead and read with 'rb'.
