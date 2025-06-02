from git_object import GitObject

class GitBlob(GitObject):
    fmt = b'blob'

    def serialize(self) -> bytes:
        return self.blobdata
    
    def deserialize(self, data: bytes) -> None:
        self.blobdata: bytes = data