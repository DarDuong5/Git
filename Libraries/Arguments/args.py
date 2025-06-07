import argparse

argparser = argparse.ArgumentParser(description="Hello, welcome to Wyag!")
argsubparsers: argparse.ArgumentParser = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True 

argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")
argsp.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repository.")

argsp = argsubparsers.add_parser("find", help="Finds the root starting from the current directory.")
argsp.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to start searching the repository.")

argsp = argsubparsers.add_parser("cat-file", help="Provide content of repository objects.")
argsp.add_argument("type", metavar="type", choices=["blob", "commit", "tag", "tree"], help="Specify the type.")
argsp.add_argument("object", metavar="object", help="The object to display.")

argsp = argsubparsers.add_parser("hash-object", help="Compute object ID and optionally creates a blob from a file.")
argsp.add_argument("-t", metavar="type", dest="type", choices=["blob", "commit", "tag", "tree"], default="blob", help="Specify the type.")
argsp.add_argument("-w", dest="write", action="store_true", help="Actually write the object into the database.")
argsp.add_argument("path", help="Read objects from <file>.")

argsp = argsubparsers.add_parser("log", help="Display history of a given commit.")
argsp.add_argument("commit", default="HEAD", nargs="?", help="Commit to start at.")

argsp = argsubparsers.add_parser("ls-tree", help="Pretty-print a tree object.")
argsp.add_argument("-r", dest="recursive", action="store_true", help="Recurse into subt-trees")
argsp.add_argument("tree", help="A tree-ish object.")
