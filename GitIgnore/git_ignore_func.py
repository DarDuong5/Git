from typing import TYPE_CHECKING, Optional
import os

from GitIgnore.Ignore.git_ignore import GitIgnore

if TYPE_CHECKING:
    from GitRepo.git_repository import GitRepository

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

    # TODO: - Check existence of global file
    #       - .gitignore files in the index