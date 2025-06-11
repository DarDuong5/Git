class GitIndex:
    def __init__(self, version: int = 2, entries: list = None):
        if entries is None:
            entries = []
        
        self.version = version
        self.entries = entries