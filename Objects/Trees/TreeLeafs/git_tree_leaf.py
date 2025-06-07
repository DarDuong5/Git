class GitTreeLeaf:
    def __init__(self, mode: bytes, path: str, sha: str):
        self.mode = mode
        self.path = path
        self.sha = sha

