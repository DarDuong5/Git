import sys

from Libraries.Commands.cmd import *

def main(argv: list[str] = sys.argv[1:]) -> None:
    args = argparser.parse_args(argv)
    match args.command:
        case "init":            cmd_init(args)
        case "find":            find(args)
        case "cat-file":        cmd_cat_file(args)
        case "hash-object":     cmd_hash_object(args)
        case "log":             cmd_log(args)
        case _:                 print("Invalid command.")

if __name__ == "__main__":
    main()

