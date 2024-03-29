#! /usr/bin/env python3

import os
import sys
import argparse
from datetime import datetime
import piexif

def get_creation_time(file_name):
    if sys.platform == 'darwin':  # macOS
        stat = os.stat(file_name)
        return stat.st_birthtime
    else:
        return os.path.getctime(file_name)

def write_exif_creation_date(file_name, creation_date):
    formatted_creation_date = creation_date.strftime("%Y:%m:%d %H:%M:%S")
    exif_dict = {"Exif": {piexif.ExifIFD.DateTimeOriginal: formatted_creation_date}}
    exif_bytes = piexif.dump(exif_dict)
    try:
        piexif.insert(exif_bytes, file_name)
        print(f"Creation date added to EXIF information of '{file_name}'")
    except Exception as e:
        print(f"Failed to write creation date to EXIF information of '{file_name}': {e}")

def rename_files(files, datetime_format, dry_run):
    for file_name in files:
        if not os.path.exists(file_name):
            print(f"File '{file_name}' not found.")
            continue

        creation_time = get_creation_time(file_name)
        creation_date = datetime.fromtimestamp(creation_time)
        formatted_time = creation_date.strftime(datetime_format)
        file_name_parts = os.path.splitext(file_name)
        new_file_name = f"{formatted_time}{file_name_parts[1]}"

        if dry_run:
            print(f"Rename '{file_name}' to '{new_file_name}' (Dry run)")
        else:
            try:
                os.rename(file_name, new_file_name)
                print(f"Renamed '{file_name}' to '{new_file_name}'")
                if file_name_parts[1].lower() in ('.jpg', '.jpeg'):
                    write_exif_creation_date(new_file_name, creation_date)
            except Exception as e:
                print(f"Failed to rename '{file_name}': {e}")

def main():
    parser = argparse.ArgumentParser(description="Rename files using creation date")
    parser.add_argument("files", nargs="+", help="List of files to rename")
    parser.add_argument("-df", "--datetime-format", default="%Y-%m-%d_%H-%M-%S",
                        help="Datetime format to use for renaming (default: %(default)s)")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force renaming without dry run")
    args = parser.parse_args()

    if args.force:
        rename_files(args.files, args.datetime_format, dry_run=False)
    else:
        rename_files(args.files, args.datetime_format, dry_run=True)

if __name__ == "__main__":
    main()

