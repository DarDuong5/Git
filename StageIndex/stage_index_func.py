import math
import os
from time import ctime

from GitRepo.git_repository import GitRepository
from StageIndex.GitIndex.git_index import GitIndex
from StageIndex.IndexEntry.git_index_entry import GitIndexEntry

def index_read(repo: 'GitRepository') -> 'GitIndex':
    index_file: str = GitRepository.repo_file(repo, "index")
    if not os.path.exists(index_file):
        return GitIndex()
    
    with open(index_file, 'rb') as f:
        raw: bytes = f.read()

    header: bytes = raw[:12]
    signature: bytes = header[:4]
    assert signature == b"DIRC" # Stands for "DirCache"

    version: int = int.from_bytes(header[4:8], "big")
    assert version == 2 # Bootgit only supports index file version 2
    count: int = int.from_bytes(header[8:12], "big")

    entries: list = []
    content: bytes = raw[12:]
    idx: int = 0
    for i in range(0, count):
        ctime_s = int.from_bytes(content[idx:idx+4], "big")
        ctime_ns = int.from_bytes(content[idx+4:idx+8], "big")
        mtime_s = int.from_bytes(content[idx+8:idx+12], "big")
        mtime_ns = int.from_bytes(content[idx+12:idx+16], "big")
        dev = int.from_bytes(content[idx+16:idx+20], "big")
        ino = int.from_bytes(content[idx+20:idx+24], "big")
        unused = int.from_bytes(content[idx+24:idx+26], "big")
        assert 0 == unused

        mode = int.from_bytes(content[idx+26:idx+28], "big")
        mode_type = mode >> 12
        assert mode_type in [0b1000, 0b1010, 0b1110]

        mode_perms = mode & 0b0000000111111111
        uid = int.from_bytes(content[idx+28:idx+32], "big")
        gid = int.from_bytes(content[idx+32:idx+36], "big")
        fsize = int.from_bytes(content[idx+36:idx+40], "big")
        sha = format(int.from_bytes(content[idx+40:idx+60], "big"), "040x")
        flags = int.from_bytes(content[idx+60:idx+62], "big")
        flag_assume_valid = (flags & 0b1000000000000000) != 0
        flag_extended = (flags & 0b0100000000000000) != 0
        assert not flag_extended

        flag_stage = flags & 0b0011000000000000
        name_length = flags & 0b0000111111111111
        idx += 62
        if name_length < 0xFFF:
            assert content[idx+name_length] == 0x00
            raw_name = content[idx:idx+name_length]
            idx += name_length + 1
        else:
            print(f"Notice: Name is 0x{name_length:X} bytes long.")
            null_idx = content.find(b"\x00", idx+ 0xFFF)
            raw_name = content[idx:null_idx]
            idx = null_idx + 1
        
        name = raw_name.decode("utf8")

        idx = 8 * math.ceil(idx/8)

        entries.append(GitIndexEntry(ctime=(ctime_s, ctime_ns),
                                    mtime=(mtime_s, mtime_ns),
                                    dev=dev,
                                    ino=ino,
                                    mode_type=mode_type,
                                    mode_perms=mode_perms,
                                    uid=uid,
                                    gid=gid,
                                    fsize=fsize,
                                    sha=sha,
                                    flag_assume_valid=flag_assume_valid,
                                    flag_stage=flag_stage,
                                    name=name))
        
    return GitIndex(version=version, entries=entries)

# Signature: GitRepository, GitIndex -> None
# Purpose: Serializes all of the Git entries back into binary.
def index_write(repo: 'GitRepository', index: 'GitIndex') -> None:
    with open(GitRepository.repo_find(repo, "index"), "wb") as f:
        f.write(b'DIRC')
        f.write(index.version.to_bytes(4, "big"))
        f.write(len(index.entries).to_bytes(4, "big"))

        idx: int = 0
        for entry in index.entries:
            f.write(entry.ctime[0].to_bytes(4, "big"))
            f.write(entry.ctime[1].to_bytes(4, "big"))
            f.write(entry.mtime[0].to_bytes(4, "big"))
            f.write(entry.mtime[1].to_bytes(4, "big"))
            f.write(entry.dev.to_bytes(4, "big"))
            f.write(entry.dev.to_bytes(4, "big"))

            mode = (entry.mode_type << 12) | entry.mode_perms
            f.write(mode.to_bytes(4, "big"))

            f.write(entry.uid.to_bytes(4, "big"))
            f.write(entry.gid.to_bytes(4, "big"))

            f.write(entry.fsize.to_bytes(4, "big"))
            f.write(int(entry.sha, 16).to_bytes(20, "big"))

            flag_assume_valid = 0x1 << 15 if entry.flag_assume_valid else 0

            name_bytes = entry.name.encode("utf8")
            bytes_len = len(name_bytes)
            if bytes_len >= 0xFFF:
                name_length = 0xFFF
            else:
                name_length = bytes_len
            
            f.write((flag_assume_valid | entry.flag_stage | name_length).to_bytes(2, "big"))

            f.write(name_bytes)
            f.write((0).to_bytes(1, "big"))

            idx += 62 + len(name_bytes) + 1
            if idx % 8 != 0:
                pad = 8 - (idx % 8)
                f.write((0).to_bytes(pad, "big"))
                idx += pad

