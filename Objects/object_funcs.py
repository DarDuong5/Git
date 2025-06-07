from typing import TYPE_CHECKING, Optional
import os
import zlib
import hashlib

from Objects.Blobs.git_blob import GitBlob
from Objects.Commits.git_commit import GitCommit
from Objects.Trees.git_tree import GitTree
from GitRepo.git_repository import GitRepository

if TYPE_CHECKING:
    from git_object import GitObject

def object_read(repo: 'GitRepository', sha: str) -> Optional['GitObject']:
    """Read object sha from Git repository repo. 
    Return a GitObject whose exact type depends on the object."""

    path: str = GitRepository.repo_file(repo, "objects", sha[0:2], sha[2:])

    if not os.path.isfile(path):
        return None

    with open(path, "rb") as f:
        raw: bytes = zlib.decompress(f.read())

        space_index: int = raw.find(b' ') 
        object_type: bytes = raw[0:space_index] 

        null_index: int = raw.find(b'\x00', space_index) 
        size: int = int(raw[space_index:null_index].decode("ascii")) 
        if size != len(raw) - null_index - 1:
            raise Exception(f"Malformed object {sha}: bad length")
        
        match object_type:
            case b'commit': c=GitCommit
            case b'tree': c=GitTree
            # case b'tag': c=GitTag
            case b'blob': c=GitBlob
            case _:
                raise Exception(f"Unknown type {object_type.decode('ascii')} for object {sha}")
            
        return c(raw[null_index + 1:])

def object_write(obj: 'GitObject', repo: 'GitRepository' = None) -> str:
    data: bytes = obj.serialize()
    result: bytes = obj.object_type + b' ' + str(len(data)).encode() + b'\x00' + data
    sha: str = hashlib.sha1(result).hexdigest()
    
    if repo:
        path: str = GitRepository.repo_file(repo, "objects", sha[0:2], sha[2:], mkdir=True)

        if not os.path.exists(path):
            with open(path, 'wb') as f:
                f.write(zlib.compress(result))
    
    return sha

