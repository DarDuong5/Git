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