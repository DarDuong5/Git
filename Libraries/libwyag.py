import sys

from GitRepo.git_repository import GitRepository
from Libraries.Arguments.args import *
from Objects.object_funcs import object_read, object_write
from Objects.git_blob import GitBlob

def cmd_init(args) -> None:
    repo = GitRepository.repo_create(args.path)
    print(f"Initialized empty Git repository in {repo.gitdir}")

def find(args: str) -> None:
    try:
        repo: 'GitRepository' = GitRepository.repo_find(args.path)
        print(f"Git repository found at: {repo.worktree}")
    except Exception as e:
        print(f"Error: {e}")

def cmd_cat_file(args) -> None:
    repo: 'GitRepository' = GitRepository.repo_find()
    cat_file(repo, args.object, object_type=args.type.encode())

def cat_file(repo, obj, object_type=None) -> None:
    obj = object_read(repo, object_find(repo, obj, object_type=object_type))
    sys.stdout.buffer.write(obj.serialize())

def object_find(repo, name, object_type=None, follow=True):
    return name

def cmd_hash_object(args) -> None:
    if args.write:
        repo: 'GitRepository' = GitRepository.repo_find()
    else:
        repo = None

    with open(args.path, "rb") as fd:
        sha = object_hash(fd, args.type.encode(), repo)
        print(sha)

def object_hash(fd, fmt, repo=None):
    data = fd.read()

    match fmt:
        # case b'commit': obj=GitCommit(data)
        # case b'tree': obj=GitTree(data)
        # case b'tag': obj=GitTag(data)
        case b'blob': obj=GitBlob(data)
        case _: raise Exception(f"Unknown type {fmt}!")

    return object_write(obj, repo)


def main(argv=sys.argv[1:]) -> None:
    args = argparser.parse_args(argv)
    match args.command:
        case "init":            cmd_init(args)
        case "find":            find(args)
        case "cat-file":        cmd_cat_file(args)
        case "hash-object":     cmd_hash_object(args)
        case _:                 print("Invalid command.")

if __name__ == "__main__":
    main()

