#!/usr/bin/env python

import csv
import re
import sys


def parse_clippings(clippings_text):
    clippings = []
    snippets = re.split(r'==========\n', clippings_text)
    for snippet in snippets:
        lines = snippet.split('\n')
        if len(lines) >= 3:
            book_title = lines[0]
            meta_info = lines[1]
            match = re.search(
                r'- Your\s+(\w+)\s+on\s+(Location|page)\s+(\d+)-?(\d+)?\s+\|\s+Added\s+on\s+(.+)', meta_info)
            if match:
                clip_type = match.group(1)
                location_type = match.group(2)
                location_start = int(match.group(3))
                location_end = int(match.group(4)) if match.group(4) else None
                added_date = match.group(5)
                content = lines[3]
                clippings.append({'bookTitle': book_title,
                                  'clipping_type': clip_type,
                                  'location_start': location_start,
                                  'location_end': location_end,
                                  'location_type': location_type,
                                  'content': content,
                                  'addedDate': added_date
                                  })
            else:
                match = re.search(
                    r'- Ihre?\s+(\w+)\s+\w+\s+(\w+)\s+(\d+)-?(\d+)?\s+\|\s+Hinzugefügt\s+am\s+(.+)', meta_info)
                if match:
                    clip_type = {"Markierung": "Highlight",
                                 "Lesezeichen": "Bookmark"}[match.group(1)]
                    location_type = {"Position": "Location",
                                     "Seite": "page"}[match.group(2)]
                    location_start = int(match.group(3))
                    location_end = int(match.group(
                        4)) if match.group(4) else None
                    added_date = match.group(5)
                    content = lines[3]
                    clippings.append({'bookTitle': book_title,
                                      'clipping_type': clip_type,
                                      'location_start': location_start,
                                      'location_end': location_end,
                                      'location_type': location_type,
                                      'content': content,
                                      'addedDate': added_date
                                      })

    return clippings


def write_csv(clippings):
    writer = csv.DictWriter(sys.stdout, fieldnames=['bookTitle', 'clipping_type', 'location_type',
                            'location_start', 'location_end', 'content', 'addedDate'], quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for clipping in clippings:
        writer.writerow(clipping)


def main():
    if len(sys.argv) > 1:
        clippings_file = sys.argv[1]
        with open(clippings_file, 'r', encoding='utf-8') as file:
            clippings_text = file.read()
    else:
        clippings_text = sys.stdin.read()

    clippings = parse_clippings(clippings_text)
    write_csv(clippings)


if __name__ == "__main__":
    main()
