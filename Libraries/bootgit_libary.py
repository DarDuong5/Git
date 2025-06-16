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
        case "ls-tree":         cmd_ls_tree(args)
        case "checkout":        cmd_checkout(args)
        case "show-ref":        cmd_show_ref(args)
        case "tag":             cmd_tag(args)
        case "rev-parse":       cmd_rev_parse(args)
        case "ls-files":        cmd_ls_files(args)
        case "check-ignore":    cmd_check_ignore(args)
        case "status":          cmd_status(_=args)
        case "rm":              cmd_status(args)
        case _:                 print("Invalid command.")

if __name__ == "__main__":
    main()

