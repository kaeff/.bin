#!/bin/bash

for file in *; do
    if [ -f "$file" ]; then
        timestamp=$(stat -f "%m" "$file") # get the last modified timestamp in seconds
        date=$(date -u -r "$timestamp" "+%Y%m%d") # convert timestamp to YYYYMMDD format
        new_filename="$date"_"$file" # create the new filename with the prefix
        mv "$file" "$new_filename" # rename the file
    fi
done
