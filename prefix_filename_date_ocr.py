#! /usr/bin/env python3

from argparse import ArgumentParser, BooleanOptionalAction
import os
import glob
import re
from pdfminer.high_level import extract_text
from dateutil import parser


# Map German month names to English
MONTH_MAP = {
    "Januar": "January",
    "Februar": "February",
    "März": "March",
    "April": "April",
    "Mai": "May",
    "Juni": "June",
    "Juli": "July",
    "August": "August",
    "September": "September",
    "Oktober": "October",
    "November": "November",
    "Dezember": "December"
}


def translate_month_names(text):
    # Replace German month names with English
    for month in MONTH_MAP:
        text = text.replace(month, MONTH_MAP[month])
    return text


def filter_for_date(text):
    date_text = ""
    pattern='([0-9]{2})[\.-]([0-9]{2})[\.-]([0-9]{2,4})'
    pattern_long='([0-9]{2})\.([a-zA-Z]+)\.([0-9]{4})'

    match = re.search(pattern, text)
    if match:
        date_text = match.group(0)
    else:
        match = re.search(pattern_long, text)
        if match:
            date_text = match.group(0)
    return date_text


def extract_date(text):
    # Translate German month names to English

    text = filter_for_date(text)
    text = translate_month_names(text)

    # Parse date using dateutil with fuzzy=True
    try:
        date = parser.parse(text, fuzzy=True, dayfirst=True, yearfirst=True)
        # Format date in German format
        formatted_date = date.strftime("%Y%m%d")
        return formatted_date
    except ValueError:
        return None


def get_new_filename(pdf_file):
    # Extract text from PDF
    text = extract_text(pdf_file)

    # Extract date from text
    date = extract_date(text)

    # Rename file with prefix and date
    if date:
        new_file_name = f"{date}_{pdf_file}"
    else:
        new_file_name = pdf_file

    return new_file_name


def prefix_filename_date_ocr(force):
    # Get all PDF files in current directory
    pdf_files = glob.glob("*.PDF") + glob.glob("*.pdf")

    for pdf_file in pdf_files:
        # Get new file name
        new_file_name = get_new_filename(pdf_file)

        # Rename file
        # os.rename(pdf_file, new_file_name)
        if force:
            os.rename(pdf_file, new_file_name)
            print ("Renamed: " + new_file_name)
        else:
            print(pdf_file + " -> " + new_file_name)

        

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--force", action=BooleanOptionalAction, help="Actually rename files")
    args = arg_parser.parse_args()

    if not args.force:
        print("DRY RUN - no files will be renamed. Call script with argument --force to rename files")
        print()

    prefix_filename_date_ocr(args.force)
