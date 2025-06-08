import sys
from typing import TYPE_CHECKING, BinaryIO, Optional
from blinker import Namespace

from Libraries.Arguments.args import *
from GitRepo.git_repository import GitRepository
from Objects.Trees.git_tree import GitTree
from Objects.object_funcs import *
from Refs.ref_funcs import *

if TYPE_CHECKING:
    from Objects.git_object import GitObject

# ------------------------------------------------[init]--------------------------------------------------

def cmd_init(args: argparse.Namespace) -> None:
    repo = GitRepository.repo_create(args.path)
    print(f"Initialized empty Git repository in {repo.gitdir}")

def find(args: argparse.Namespace) -> None:
    try:
        repo: 'GitRepository' = GitRepository.repo_find(args.path)
        print(f"Git repository found at: {repo.worktree}")
    except Exception as e:
        print(f"Error: {e}")

# ------------------------------------------------[cat-file]--------------------------------------------------

def cmd_cat_file(args: argparse.Namespace) -> None:
    repo: 'GitRepository' = GitRepository.repo_find()
    cat_file(repo, args.object, object_type=args.type.encode())

def cat_file(repo: 'GitRepository', obj: str, object_type: Optional[bytes] = None) -> None:
    obj = object_read(repo, object_find(repo, obj, object_type=object_type))
    sys.stdout.buffer.write(obj.serialize())

def object_find(repo: 'GitRepository', name: str, object_type: 'GitObject' = None, follow: bool = True) -> str:
    return name

# # ------------------------------------------------[hash-object]--------------------------------------------------

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

# ------------------------------------------------[log]--------------------------------------------------

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

# ------------------------------------------------[ls-tree]--------------------------------------------------

def cmd_ls_tree(args: Namespace) -> None:
    repo: 'GitRepository' = GitRepository.repo_find()
    ls_tree(repo, args.tree, args.recursive)

def ls_tree(repo: 'GitRepository', ref, recursive=None, prefix="") -> None:
    sha: str = object_find(repo, ref, object_type=b"tree")
    obj: Optional['GitObject'] = object_read(repo, sha)
    for item in obj.items:
        if len(item.mode) == 5:
            type = item.mode[0:1]
        else:
            type = item.mode[0:2]
    
        match type:
            case b'04': type = "tree"
            case b'10': type = "blob" #regular file
            case b'12': type = "blob" #symlink; blob contents is link target
            case b'16': type = "commit" #submodule
            case _: raise Exception(f"Weird tree leaf mode: {item.mode}")

        if not (recursive and type == 'tree'):
            print(f"{'0'*(6-len(item.mode)) + item.mode.decode('ascii')} {type} {item.sha}\t{os.path.join(prefix, item.path)}")
        else:
            ls_tree(repo, item.sha, recursive, os.path.join(prefix, item.path))

# ------------------------------------------------[checkout]--------------------------------------------------

def cmd_checkout(args: Namespace) -> None:
    repo: 'GitRepository' = GitRepository.repo_find()

    obj: Optional[GitObject] = object_read(repo, object_find(repo, args.commit))

    if obj.object_type == b'commit':
        obj = object_read(repo, obj.kvlm[b'tree'].decode("ascii"))
    
    if os.path.exists(args.path):
        if not os.path.isdir(args.path):
            raise Exception(f"Not a directory {args.path}!")
        if os.listdir(args.path):
            raise Exception(f"Not empty {args.path}!")
    else:
        os.makedirs(args.path)

    tree_checkout(repo, obj, os.path.realpath(args.path))

def tree_checkout(repo: 'GitRepository', tree, path: str) -> None:
    for item in tree.items:
        obj: Optional['GitObject'] = object_read(repo, item.sha)
        dest: str = os.path.join(path, item.path)

        if obj.object_type == b'tree':
            os.mkdir(dest)
            tree_checkout(repo, obj, dest)
        elif obj.object_type == b'blob':
            with open(dest, 'wb') as f:
                f.write(obj.blobdata)

# ------------------------------------------------[show-ref]--------------------------------------------------

# def cmd_show_ref(args: Namespace) -> None:
#     repo: 'GitRepository' = GitRepository.repo_find()
#     refs: dict[str, Optional[dict[]]] = ref_list(repo)