import fnmatch
from typing import TYPE_CHECKING, Optional
import os

from GitIgnore.Ignore.git_ignore import GitIgnore
from Objects.object_funcs import object_read
from StageIndex.stage_index_func import index_read

if TYPE_CHECKING:
    from GitRepo.git_repository import GitRepository
    from StageIndex.GitIndex.git_index import GitIndex

def gitignore_parse1(raw: str) -> Optional[tuple[str, bool]]:
    raw = raw.strip()

    if not raw or raw[0] == "#":
        return None
    elif raw[0] == "!":
        return (raw[1:], False)
    elif raw[0] == "\\":
        return (raw[1:], True)
    else:
        return (raw, True)
    
def gitignore_parse(lines: list[str]) -> list[tuple[str, bool]]:
    ret: list[str] = []

    for line in lines:
        parsed = gitignore_parse1(line)
        if parsed:
            ret.append(parsed)

    return ret

def gitignore_read(repo: 'GitRepository') -> 'GitIgnore':
    ret: 'GitIgnore' = GitIgnore(absolute=[], scoped=dict())

    repo_file: str = os.path.join(repo.gitdir, "info/exclude")
    if os.path.exists(repo_file):
        with open(repo_file, "r") as f:
            ret.absolute.append(gitignore_parse(f.readlines()))
    
    if "XDG_CONFIG_HOME" in os.environ:
        config_home: str = os.environ["XDG_CONFIG_HOME"]
    else:
        config_home: str = os.path.expanduser("~/.config")
    global_file: str = os.path.join(config_home, "git/ignore")

    index: 'GitIndex' = index_read(repo)

    for entry in index.entries:
        if entry.name == ".gitignore" or entry.name.endswith("/.gitignore"):
            dir_name = os.path.dirname(entry.name)
            contents = object_read(repo, entry.sha)
            lines = contents.blobdata.decode("utf8").splitlines()
            ret.scoped[dir_name] = gitignore_parse(lines)

    return ret

def check_ignore1(rules: list[tuple[str, bool]], path: str) -> Optional[bool]:
    result: Optional[bool] = None
    for (pattern, value) in rules:
        if fnmatch.fnmatch(path, pattern):
            result = value

    return result

def check_ignored_scoped(rules: dict[str, list[tuple[str, bool]]], path: str) -> Optional[bool]:
    parent: str = os.path.dirname(path)
    while True:
        if parent in rules:
            result: Optional[bool] = check_ignore1(rules[parent], path)
            if result != None:
                return result
        if parent == "":
            break
        parent = os.path.dirname(parent)

    return None

def check_ignored_absolute(rules: list[tuple[str, bool]], path: str) -> bool:
    parent: str = os.path.dirname(path)
    for rule in rules:
        result: Optional[bool] = check_ignore1(rule, path)
        if result != None:
            return result
    
    return False