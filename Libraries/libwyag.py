import sys

from GitRepo.git_repository import GitRepository
from Libraries.Arguments.args import *
from Objects.object_funcs import object_read

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

def main(argv=sys.argv[1:]) -> None:
    args = argparser.parse_args(argv)
    match args.command:
        case "init":            cmd_init(args)
        case "find":            find(args)
        case "cat-file":        cmd_cat_file(args)
        case _:                 print("Invalid command.")

if __name__ == "__main__":
    main()

