from Objects.git_object import GitObject

class GitBlob(GitObject):
    object_type = b'blob'

    def serialize(self) -> bytes:
        return self.blobdata
    
    def deserialize(self, data: bytes) -> None:
        self.blobdata: bytes = data