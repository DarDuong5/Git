from StageIndex.IndexEntry.git_index_entry import GitIndexEntry

class GitIndex:
    def __init__(self, version: int = 2, entries: list['GitIndexEntry'] = None):
        if entries is None:
            entries = []
        
        self.version = version
        self.entries = entries