from Objects.git_object import GitObject
from Objects.tree_func import *

class GitTree(GitObject):
    object_type = b'tree'

    def deserialize(self, data):
        self.items = tree_parse(data)

    def serialize(self):
        return tree_serialize(self)

    def init(self):
        self.items = list()