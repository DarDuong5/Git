from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from GitRepo.git_repository import GitRepository

class GitObject(ABC):
    def __init__(self, data: Optional[bytes] = None):
        if data != None:
            self.deserialize(data)
        else:
            self.init()

    @abstractmethod
    def serialize(self, repo: 'GitRepository') -> bytes:
        raise Exception("Unimplemented!")
    
    @abstractmethod
    def deserialize(self, data: bytes) -> None:
        raise Exception("Unimplemented!")
    
    def init(self):
        pass