#! /Users/kaeff/.bin/.venv/bin/python3

from argparse import ArgumentParser, BooleanOptionalAction
from datetime import datetime
import os
import glob
import re
from pdfminer.high_level import extract_text
from dateutil import parser
import ocrmypdf


# Map German month names to English
MONTH_GERMAN_TO_ENGLISH = {
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
    for month in MONTH_GERMAN_TO_ENGLISH:
        text = text.replace(month, MONTH_GERMAN_TO_ENGLISH[month])
    return text


def filter_for_date(text):
    date_text = ""
    pattern = '([0-9]{2})[_\\.-]([0-9]{2})[_\\.-]([0-9]{2,4})'
    pattern_long = '([0-9]{2})\\. ?([a-zA-Z]+)[ \\.]([0-9]{4})'

    match = re.search(pattern, text)
    if match:
        date_text = match.group(0)
    else:
        match = re.search(pattern_long, text)
        if match:
            date_text = match.group(0)
    return date_text


def extract_date(text):
    text = filter_for_date(text)
    text = translate_month_names(text)

    # Parse date using dateutil with fuzzy=True
    try:
        return parser.parse(text, fuzzy=True, dayfirst=True, yearfirst=True)
    except ValueError:
        return None


def perform_ocr(pdf_file):
    ocrmypdf.configure_logging(verbosity=-1)
    print("Performing OCR for: " + pdf_file)

    dirname, filename = os.path.split(pdf_file)
    basename, ext = os.path.splitext(filename)
    tmp_pdf_ocred = os.path.join(dirname, basename + ".ocr" + ext)

    if os.path.exists(tmp_pdf_ocred):
        os.remove(tmp_pdf_ocred)

    ocrmypdf.ocr(pdf_file, tmp_pdf_ocred, force_ocr=True)
    text = extract_text(tmp_pdf_ocred)

    os.remove(tmp_pdf_ocred)
    return text


def get_new_filename(pdf_file, print_text):
    # Check if filename contains a date
    date = extract_date(pdf_file)

    # Otherwise, extract text from PDF
    if not date:
        text = extract_text(pdf_file)
        date = extract_date(text)

    # Otherwise, try OCR
    if not date:
        text = perform_ocr(pdf_file)
        date = extract_date(text)

    # Otherwise, use mtime
    if not date:
        # Use last modified timestamp as date
        timestamp = os.path.getmtime(pdf_file)
        date = datetime.fromtimestamp(timestamp).date()

    # Rename file with prefix and date
    if date:
        formatted_date = date.strftime("%Y-%m-%d")
        new_file_name = os.path.join(
            os.path.dirname(pdf_file),
            f"{formatted_date}_{os.path.basename(pdf_file)}")
    else:
        new_file_name = pdf_file

    return new_file_name


def prefix_filename_date_ocr(force, print_text):
    # Get all PDF files in current directory
    pdf_files = glob.glob("*.PDF") + glob.glob("*.pdf")

    for pdf_file in pdf_files:
        # Get new file name
        new_file_name = get_new_filename(pdf_file, print_text)

        # Rename file
        if force:
            os.rename(pdf_file, new_file_name)
            print("Renamed: " + new_file_name)
        else:
            print(pdf_file + " -> " + new_file_name)


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-f", "--force",
        action=BooleanOptionalAction,
        help="Actually rename files")

    arg_parser.add_argument(
        "-t", "--print-text",
        action=BooleanOptionalAction,
        help="Print OCR text for debugging")

    arg_parser.add_argument(
        "files",
        nargs="*",
        default=glob.glob("*.PDF") + glob.glob("*.pdf"),
        help="List of files to prefix"
    )

    args = arg_parser.parse_args()

    if not args.force:
        print("DRY RUN - no files will be renamed. " +
              "Call script with argument --force to rename files")
        print()

    prefix_filename_date_ocr(args.force, args.print_text)


if __name__ == "__main__":
    main()
