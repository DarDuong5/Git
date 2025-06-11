class GitIndexEntry:
    def __init__(self, ctime: tuple[int, int] = None, mtime: tuple[int, int] = None, dev: int = None, ino: int = None,
                mode_type: bytes = None, mode_perms: int = None, uid: int = None, gid: int = None, fsize: int = None, sha: bytes = None,
                flag_assume_valid: int = None, flag_stage: int = None, name: str = None):

        self.ctime = ctime
        self.mtime = mtime
        self.dev = dev
        self.ino = ino
        self.mode_type = mode_type
        self.mode_perms = mode_perms
        self.uid = uid
        self.gid = gid
        self.fsize = fsize
        self.sha = sha
        self.flag_assume_valid = flag_assume_valid
        self.flag_stage = flag_stage
        self.name = name