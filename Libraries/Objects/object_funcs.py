from typing import TYPE_CHECKING
import os
import zlib
import hashlib


if TYPE_CHECKING:
    from GitRepo.git_repository import GitRepository
    from git_object import GitObject

def object_read(repo: 'GitRepository', sha: str) -> 'GitObject':
    """Read object sha from Git repository repo. 
    Return a GitObject whose exact type depends on the object."""

    path: str = GitRepository.repo_file(repo, "objects", sha[0:2], sha[2:])

    if not os.path.isfile(path):
        return None

    with open(path, "rb") as f:
        raw = zlib.decompress(f.read())

        x = raw.find(b' ')
        fmt = raw[0:x]

        y = raw.find(b'\x00', x)
        size = int(raw[x:y].decode("ascii"))
        if size != len(raw) - y - 1:
            raise Exception(f"Malformed object {sha}: bad length")
        
        match fmt:
            # case b'commit': c=GitCommit
            # case b'tree': c=GitTree
            # case b'tag': c=GitTag
            # case b'blob': c=GitBlob
            case _:
                raise Exception(f"Unknown type {fmt.decode("ascii")} for object {sha}")
            
        return c(raw[y + 1:])

def object_write(obj: 'GitObject', repo: 'GitRepository' = None) -> str:
    data = obj.serialize()
    result = obj.fmt + b' ' + str(len(data)).encode() + b'\x00' + data
    sha = hashlib.sha1(result).hexdigest()
    
    if repo:
        path = GitRepository.repo_file(repo, "objects", sha[0:2], sha[2:], mkdir=True)

        if not os.path.exists(path):
            with open(path, 'wb') as f:
                f.write(zlib.compress(result))
    
    return sha

