from creation_data.creation_test_data_cache import creation_data
import struct
import random

def only_insert():
    data = creation_data(1)
    result = b''
    for coder in data:
        key, value = coder

        key_bytes = key.encode()
        value_bytes = value.encode()

        key_length = len(key_bytes)
        key_length_with_flag = key_length | 0x80000000
        value_length = len(value_bytes)

        header1 = struct.pack('>I', key_length_with_flag)
        header2 = struct.pack('>I', value_length)


        result += header1 + header2 + key_bytes + value_bytes
    return result

def only_select():
    data = creation_data(1)
    result = b''
    for coder in data:
        key, value = coder

        key_bytes = key.encode()

        key_length = len(key_bytes)

        header = struct.pack('>I', key_length)

        result += header + key_bytes

    return result

def insert_or_select():
    data = creation_data(1)
    result = b''
    for coder in data:
        key, value = coder

        key_bytes = key.encode()
        value_bytes = value.encode()

        key_length = len(key_bytes)
        value_length = len(value_bytes)

        rand = random.randint(0,1)
        if rand == 0:
            header = struct.pack('>I', key_length)
            result += header + key_bytes
        else:
            key_length_with_flag = key_length | 0x80000000
            header = struct.pack('>II', key_length_with_flag, value_length)
            result += header + key_bytes + value_bytes
    return result

def speed_test_data():
    data = creation_data(1)
    result = b''

    key, value = data[0]

    key_bytes = key.encode()
    value_bytes = value.encode()

    key_length = len(key_bytes)
    key_length_with_flag = key_length | 0x80000000
    value_length = len(value_bytes)

    header = struct.pack('>II', key_length_with_flag, value_length)
    result += header + key_bytes + value_bytes

    key, value = data[1]

    key_bytes = key.encode()
    key_length = len(key_bytes)

    header = struct.pack('>I', key_length)
    result += header + key_bytes

    for coder in data[2:-2]:
        key, value = coder

        key_bytes = key.encode()
        value_bytes = value.encode()

        key_length = len(key_bytes)
        value_length = len(value_bytes)

        header = struct.pack('>II', key_length, value_length)

        result += header + key_bytes + value_bytes

    key, value = data[-1]

    key_bytes = key.encode()
    key_length = len(key_bytes)

    header = struct.pack('>I', key_length)
    result += header + key_bytes

    return result
'''
flag = (key_length_with_flag & 0x80000000) >> 31  # Считать старший бит (0 или 1)
key_length = key_length_with_flag & 0x7FFFFFFF 

'''