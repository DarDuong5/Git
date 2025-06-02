import argparse
import sys
from typing import TYPE_CHECKING
from GitRepo.git_repository import GitRepository

argparser = argparse.ArgumentParser(description="Hello, welcome to Wyag!")
argsubparsers: argparse.ArgumentParser = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True 

argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")
argsp.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repository.")

argsq = argsubparsers.add_parser("find", help="Finds the root starting from the current directory.")
argsq.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to start searching the repository.")

def cmd_init(args) -> None:
    repo = GitRepository.repo_create(args.path)
    print(f"Initialized empty Git repository in {repo.gitdir}")

def find(args: str) -> None:
    try:
        repo: 'GitRepository' = GitRepository.repo_find(args.path)
        print(f"Git repository found at: {repo.worktree}")
    except Exception as e:
        print(f"Error: {e}")

def main(argv=sys.argv[1:]) -> None:
    args = argparser.parse_args(argv)
    match args.command:
        case "init":            cmd_init(args)
        case "find":            find(args)
        case _:                 print("Invalid command.")

if __name__ == "__main__":
    main()

