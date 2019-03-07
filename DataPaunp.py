from functools import reduce

def _to_byte(i, length=1, byteorder="little"):
    return i.to_bytes(length,byteorder)

def _double_if_equal(a, b):
    if a == b:
        return a + b
    else:
        return a

def _join_bytes(byte_list):
    return reduce(
        lambda acc, cur: acc + cur,
        byte_list,
        b''
    )

def _escape(data, escaped_byte):
    return _join_bytes(
        list(
            map(lambda x: _double_if_equal(_to_byte(x), escaped_byte), 
                data)
        )
    )

BYTE_STARTING = _to_byte(128)
BYTE_ENDING = _to_byte(127)

class DataPaunp:
    def __init__(self, byte_start=BYTE_STARTING, byte_ending=BYTE_ENDING):
        assert byte_start!= byte_ending
        self.byte_start=byte_start
        self.byte_ending=byte_ending
        
    def pack(self, data):
        return BYTE_STARTING \
            + _escape(_escape(data, self.byte_start), self.byte_ending) \
            + BYTE_ENDING
            
    def unpack(self, data):
        def all_equal(a,b,c):
            return a == c and b == c
        unpacked_data = [b'']
        payload = data[1:-1]
        i = 0
        while i < len(payload):
            byte_cur = _to_byte(payload[i])
            if i != len(payload) - 1:
                byte_next = _to_byte(payload[i+1])
                if all_equal(byte_cur, byte_next, self.byte_start) \
                    or all_equal(byte_cur, byte_next, self.byte_ending):
                    i += 1
                elif byte_cur == self.byte_ending:
                    print(i)
                    i += 2
                    unpacked_data.append(b'')
                    continue
            unpacked_data[-1] += byte_cur
            i += 1
        return unpacked_data