# Key Value List with Message (used for commit and tags)

def kvlm_parse(raw: bytes, start: int= 0, dct: dict[bytes, bytes] = None) -> None:
    if not dct:
        dct = dict()

    space = raw.find(b' ', start)
    new_line = raw.find(b'\n', start)

    if (space < 0) or (new_line < space):
        assert new_line == start
        dct[None] = raw[start+1:]
        return dct
    
    key = raw[start:space]

    end = start
    while True:
        end = raw.find(b'\n', end+1)
        if raw[end+1] != ord(' '): 
            break
    
    value = raw[space+1:end].replace(b'\n', b'\n')

    if key in dct:
        if type(dct[key]) == list:
            dct[key].append(value)
        else:
            dct[key] = [dct[key], value]
    else:
        dct[key] = value

    return kvlm_parse(raw, start=end+1, dct=dct)

def kvlm_serialize(kvlm: dict[bytes, bytes]) -> bytes:
    ret: bytes = b''

    for k in kvlm.keys():
        if k == None:
            continue
        val = kvlm[k]
        if type(val) != list:
            val = [val]

        for v in val:
            ret += k + b' ' + (v.replace(b'\n', b'\n ')) + b'\n'

    ret += b'\n' + kvlm[None]

    return ret


