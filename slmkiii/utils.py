import os
from slmkiii.errors import ErrorUnknownExtension


def file_type(filename):
    _, extension = os.path.splitext(filename)
    if extension in ('.js', '.json'):
        return 'json'
    if extension in ('.syx', '.sysex'):
        return 'sysex'
    raise ErrorUnknownExtension(extension)


def bytes_to_nibbles(data):
    nibbles = [0] * 8
    for ofst in range(8):
        nibbles[ofst] = data >> 4 * (7 - ofst) & 15
    return ''.join([chr(x) for x in nibbles])


def nibbles_to_bytes(data):
    output = 0
    for idx, char in enumerate(data):
        output += ord(char) * pow(16, 7 - idx)
    return (output % 0x100000000) >> 0


def seven_to_eight(data):
    raw = [ord(x) for x in data]
    result = []
    offset = 0
    while offset < len(raw):
        chunk = raw[offset:offset + 8]
        eights = chunk[1:]
        for idx, _ in enumerate(eights):
            eights[idx] += (((chunk[0] & 1 << idx) >> idx) << 7)
        result += eights
        offset += 8
    return ''.join([chr(x) for x in result])


def eight_to_seven(data):
    result = [0] * (1 + len(data) - -(len(data) // 7))
    seven_offset = 0
    eight_offset = 0
    while seven_offset < len(data):
        result[eight_offset] = 0
        for incr in range(7):
            if seven_offset + incr < len(data):
                char = ord(data[seven_offset + incr])
                result[eight_offset + incr + 1] = 127 & char
            sevens = (128 & char) >> 7 - incr
            result[eight_offset] |= sevens
        eight_offset += 8
        seven_offset += 7
    return ''.join([chr(x) for x in result])
