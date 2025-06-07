import sys
from typing import TYPE_CHECKING, BinaryIO, Optional
from blinker import Namespace

from Libraries.Arguments.args import *
from GitRepo.git_repository import GitRepository
from Objects.Trees.git_tree import GitTree
from Objects.object_funcs import *

if TYPE_CHECKING:
    from Objects.git_object import GitObject

def cmd_init(args: argparse.Namespace) -> None:
    repo = GitRepository.repo_create(args.path)
    print(f"Initialized empty Git repository in {repo.gitdir}")

def find(args: argparse.Namespace) -> None:
    try:
        repo: 'GitRepository' = GitRepository.repo_find(args.path)
        print(f"Git repository found at: {repo.worktree}")
    except Exception as e:
        print(f"Error: {e}")

def cmd_cat_file(args: argparse.Namespace) -> None:
    repo: 'GitRepository' = GitRepository.repo_find()
    cat_file(repo, args.object, object_type=args.type.encode())

def cat_file(repo: 'GitRepository', obj: str, object_type: Optional[bytes] = None) -> None:
    obj = object_read(repo, object_find(repo, obj, object_type=object_type))
    sys.stdout.buffer.write(obj.serialize())

def object_find(repo: 'GitRepository', name: str, object_type: 'GitObject' = None, follow: bool = True):
    return name

def cmd_hash_object(args: argparse.Namespace) -> None:
    if args.write:
        repo: 'GitRepository' = GitRepository.repo_find()
    else:
        repo = None

    with open(args.path, "rb") as file_desc:
        sha = object_hash(file_desc, args.type.encode(), repo)
        print(sha)

def object_hash(file_desc: BinaryIO, object_type: bytes, repo: 'GitRepository' = None):
    data = file_desc.read()

    match object_type:
        case b'commit': obj=GitCommit(data)
        case b'tree': obj=GitTree(data)
        # case b'tag': obj=GitTag(data)
        case b'blob': obj=GitBlob(data)
        case _: raise Exception(f"Unknown type {object_type}!")

    return object_write(obj, repo)

def cmd_log(args: Namespace) -> None:
    repo: 'GitRepository' = GitRepository.repo_find()
    print("digraph wyaglog{")
    print("  node[shape=rect]")
    log_graphviz(repo, object_find(repo, args.commit), set())
    print("}")

def log_graphviz(repo: 'GitRepository', sha: str, seen: set) -> None:
    if sha in seen:
        return
    seen.add(sha)

    commit = object_read(repo, sha)
    message = commit.kvlm[None].decode("utf8").strip()
    message = message.replace("\\", "\\\\")
    message = message.replace("\"", "\\\"")

    if "\n" in message:
        message = message[:message.index("\n")]

    print(f"  c_{sha} [label=\"{sha[0:7]}: {message}\"]")
    assert commit.object_type == b"commit"

    if not b'parent' in commit.kvlm.keys():
        return
    
    parents = commit.kvlm[b'parent']

    if type(parents) != list:
        parents = [parents]

    for p in parents:
        p = p.decode("ascii")
        print(f"  c_{sha} -> c_{p};")
        log_graphviz(repo, p, seen)
