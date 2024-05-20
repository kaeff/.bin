#! /usr/bin/env python3

import argparse
import os
import re
from datetime import datetime


def input_to_python(date_input):
    return date_input \
        .replace('YYYY', '%Y') \
        .replace('YY', '%y') \
        .replace('MM', '%m') \
        .replace('DD', '%d')


def input_to_regex(date_input):
    return re.compile(
        date_input
        .replace('YYYY', r'\d{4}')
        .replace('YY', r'\d{2}')
        .replace('MM', r'\d{2}')
        .replace('DD', r'\d{2}')
    )


def convert_date_format(filename, old_format, new_format):
    """
    Converts the date format in a filename from old_format to new_format.

    Args:
        filename (str): The filename to be converted.
        old_format (str): The current date format in the filename.
        new_format (str): The desired date format in the filename.

    Returns:
        str: The new filename with the date format converted.
    """
    old_regex = input_to_regex(old_format)
    match = re.match(old_regex, filename)
    if match:
        old_date_found = match.group(0)
        try:
            date_obj = datetime.strptime(
                old_date_found, input_to_python(old_format))
            date_obj_str = datetime.strftime(
                date_obj, input_to_python(old_format))
            if old_date_found != date_obj_str:
                raise ValueError('Date format does not match input format.')
        except ValueError:
            print(f"Error: {old_regex} does not match the format {
                  input_to_python(old_format)}. Skipping file {filename}.")
            return filename

        new_date_str = datetime.strftime(date_obj, input_to_python(new_format))
        new_filename = filename.replace(old_date_found, new_date_str, 1)
        return new_filename

    return filename


def get_renamings(directory_path, old_format, new_format):
    renamings = {}
    for filename in os.listdir(directory_path):
        new_filename = convert_date_format(filename, old_format, new_format)
        if new_filename != filename:
            renamings[filename] = new_filename
    return renamings


def apply_renamings(directory_path, renamings):
    """
    Applies the renamings to the files in the specified directory.

    Args:
        directory_path (str): The path to the directory
             containing the files to be renamed.
        renamings (dict): A dictionary of renamings to be made,
             mapping old filenames to new filenames.

    Returns:
        None
    """
    for old_filename, new_filename in renamings.items():
        old_path = os.path.join(directory_path, old_filename)
        new_path = os.path.join(directory_path, new_filename)
        os.rename(old_path, new_path)


def rename_files_in_directory(directory_path, old_format, new_format,
                              ask_for_consent=True):
    """
    Renames all files in a directory whose filename starts with the expected
        date pattern.

    Args:
        directory_path (str): The path to the directory containing the files
             to be renamed.
        old_format (str): The current date format in the filename.
        new_format (str): The desired date format in the filename.
        ask_for_consent (bool): If False, skips user input prompt and renames
             files directly.

    Returns:
        None
    """
    print("Renaming matching files in directory: " +
          str(directory_path))
    renamings = get_renamings(directory_path, old_format, new_format)
    if not renamings:
        print("No files to rename.")
        return

    print("Renaming the following files:")
    for old_filename, new_filename in renamings.items():
        print(f"{old_filename} -> {new_filename}")

    if ask_for_consent:
        confirmation = input(
            "Do you want to proceed with the renaming? (Y/N) ").strip().lower()
        if confirmation != 'y':
            print("Renaming aborted.")
            return

    apply_renamings(directory_path, renamings)

    print("Renaming complete.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Rename files with date format in filename.')
    parser.add_argument('old_format', metavar='old_format', type=str,
                        help='the current date format in the filename')
    parser.add_argument('new_format', metavar='new_format', type=str,
                        help='the desired date format in the filename')
    args = parser.parse_args()

    directory_path = os.path.abspath(os.path.curdir)
    old_format = args.old_format
    new_format = args.new_format

    rename_files_in_directory(directory_path, old_format, new_format)
