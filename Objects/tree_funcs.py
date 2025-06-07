from typing import TYPE_CHECKING

from Objects.Trees.TreeLeafs.git_tree_leaf import GitTreeLeaf

if TYPE_CHECKING:
    from Objects.git_object import GitObject

def tree_parse_one(raw: bytes, start: int = 0) -> tuple[int, 'GitTreeLeaf']:
    space_index: int = raw.find(b' ', start)
    assert space_index-start == 5 or space_index-start == 6

    mode: bytes = raw[start:space_index]
    if len(mode) == 5:
        mode = b'0' + mode

    null_index: int = raw.find(b'\x00', space_index)

    path: bytes = raw[space_index+1:null_index]

    raw_sha: int = int.from_bytes(raw[null_index+1:null_index+21], "big")

    sha: str = format(raw_sha, "040x")

    return null_index+21, GitTreeLeaf(mode, path.decode("utf8"), sha)

def tree_parse(raw: bytes) -> list['GitTreeLeaf']:
    pos: int = 0
    max: int = len(raw)
    ret: list['GitTreeLeaf'] = []
    while pos < max:
        pos, data = tree_parse_one(raw, data)
        ret.append(data)
    
    return ret

def tree_leaf_sort_key(leaf: 'GitTreeLeaf') -> str:
    return leaf.path+'/' if not leaf.path.startswith(b'10') else leaf.path

def tree_serialize(obj: list['GitObject']) -> bytes:
    obj.items.sort(key=tree_leaf_sort_key)
    ret = b''
    for i in obj.items:
        ret += i.mode
        ret += b' '
        ret += i.path.encode("utf8")
        ret += b"\x00"
        sha += int(i.sha, 16)
        ret += sha.to_bytes(20, byteorder="big")
    return ret
