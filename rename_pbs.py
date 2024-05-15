#! /usr/bin/env python3

import sys
import re
import os
import argparse
from pdfminer.high_level import extract_text

def find_month(input_string):
    months = {
        "ENE": "01",
        "FEB": "02",
        "MAR": "03",
        "ABR": "04",
        "MAI": "05",
        "JUN": "06",
        "JUL": "07",
        "AGO": "08",
        "SEP": "09",
        "OCT": "10",
        "NOV": "11",
        "DIC": "12"
    }

    pattern = r'\bMENS \d{2} (' + '|'.join(months.keys()) + r') (\d{2})\b'
    match = re.search(pattern, input_string)
    if match:
        month = months[match.group(1)]
        year = match.group(2)
        return f"{year}-{month}"
    else:
        return None

def find_rsu(input_string):
    pattern = r'\bRSU (\d{2})/20(\d{2})\b'
    match = re.search(pattern, input_string)
    if match:
        month = match.group(1)
        year = match.group(2)
        return f"{year}-{month} RSU"
    else:
        return None


def rename_file(input_file, result, force):
    if result:
        new_name = f"{result} {input_file}"
        if force:
            os.rename(input_file, new_name)
            print(f"Renamed file to: {new_name}")
        else:
            print(f"Dry run: Would rename file to: {new_name}")
    else:
        print("No match found, file not renamed.")

def main():
    parser = argparse.ArgumentParser(description='Rename PDF files based on content')
    parser.add_argument('input_file', help='Input PDF file to process')
    parser.add_argument('--force', '-f', action='store_true', help='Force renaming (otherwise, perform dry run)')
    args = parser.parse_args()

    input_file = args.input_file

    try:
        text = extract_text(input_file)
        result = find_month(text)
        if not result:
            result = find_rsu(text)
        rename_file(input_file, result, args.force)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

