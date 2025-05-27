import argparse
import configparser
from datetime import datetime
import grp, pwd
from fnmatch import fnmatch
import hashlib
from math import ceil
import os
import re
import sys
import zlib
from Libraries.Objects.GitRepository import GitRepository

argparser = argparse.ArgumentParser(description="Hello, welcome to Wyag!")
argsubparsers: argparse.ArgumentParser = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True 

argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")
argsp.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repository.")

def cmd_init(args):
    repo = GitRepository.repo_create(args.path)
    print(f"Initialized empty Git repository in {repo.gitdir}")

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "init":            cmd_init(args)
        case _:                 print("Invalid command.")


if __name__ == "__main__":
    main()

