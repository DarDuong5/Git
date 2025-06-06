from Objects.git_object import GitObject
from Objects.kvlm import kvlm_parse, kvlm_serialize

class GitCommit(GitObject):
    object_type = b'commit'

    def deserialize(self, data) -> None:
        self.kvlm = kvlm_parse(data)

    def serialize(self) -> None:
        return kvlm_serialize(self.kvlm)
    
    def init(self) -> None:
        self.kvlm = dict()
