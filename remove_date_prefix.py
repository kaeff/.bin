#!/usr/bin/env python3

from argparse import ArgumentParser, BooleanOptionalAction
import os
import re


def main(files, force):
    if not force:
        print("DRY RUN - no files will be renamed. " +
              "Call script with argument --force to rename files")

    newfiles = set()
    for file in files:
        if os.path.isfile(file):
            newfile = re.sub(r'^[0-9_-]*', '', file)
            while newfile in newfiles:
                newfile += " (1)"
            newfiles.add(newfile)

            if force:
                os.rename(file, newfile)
            else:
                print(f'mv "{file}" "{newfile}"')


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-f", "--force",
        action=BooleanOptionalAction,
        help="Actually rename files")

    arg_parser.add_argument(
        "files",
        nargs="*",
        default=os.listdir('.'),
        help="List of files to prefix"
    )

    args = arg_parser.parse_args()

    main(args.files, args.force)
