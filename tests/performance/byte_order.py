import sys
import struct
import cProfile


value_4byte = b'abcd'
result_4byte = b'dcba'

value_8byte = b'abcdefgh'
result_8byte = b'dcbahgfe'

value_16byte = b'abcdefghijklmnop'
result_16byte = b'dcbahgfelkjiponm'

def byteorder_list_chunks_bytes(data: bytes):
    result = []
    for i in range(0, len(data), 4):
        result.append(data[i:i+4][::-1])
    return b''.join(result)


def byteorder_list_chunks_bytearray(data: bytes):
    result = bytearray()
    for i in range(0, len(data), 4):
        result += data[i:i+4][::-1]
    return result


def byteorder_list_chunks_bytearray_reverse(data: bytes):
    data = bytearray(data)
    result = bytearray()
    for i in range(0, len(data), 4):
        r = data[i:i+4]
        r.reverse()
        result += r
    return result


def byteorder_repack_chunks(data: bytes):
    result = bytearray()
    it = struct.iter_unpack('>L', data)
    for i, in it:
        result += struct.pack('L', i)
    return result


def byteorder_int_chunks(data: bytes):
    result = bytearray()
    for i in range(0, len(data), 4):
        res = int.from_bytes(data[i:i+4], byteorder='big')
        result += res.to_bytes(4, byteorder=sys.byteorder)
    return result


if __name__ == '__main__':
    import timeit

    test_functions = [
        'byteorder_list_chunks_bytes',
        'byteorder_list_chunks_bytearray',
        'byteorder_list_chunks_bytearray_reverse',
        'byteorder_repack_chunks',
        'byteorder_int_chunks',
    ]

    test_sets = [
        '4byte', '8byte', '16byte'
    ]

    for test_function in test_functions:
        for test_set in test_sets:
            text = "{test_function}, {test_set}: {time:.5f} secs"
            setup = '''from __main__ import {test_function} as test_func, value_{test_set} as test_set'''.format(**locals())
            time = timeit.timeit("test_func(test_set)", setup=setup)
            print(text.format(**locals()))

            # Tests for correct value
            fun = globals()[test_function]
            val = globals()['value_'+test_set]
            res = globals()['result_'+test_set]
            if fun(val) != res:
                print("Error, function did'n returned correct value! Expected: '{}', result '{}'".format(fun(val), res))
