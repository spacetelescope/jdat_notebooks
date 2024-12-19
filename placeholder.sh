#!/bin/bash

# Copy the placeholder image to the required directory
cp jdaviz_placeholder_new.png _build/html

# Directory to search within
ROOT_DIR="_build/html"

# Line to search for
SEARCH_STRING="vnd.jupyter.widget-view+json"

# Replacement line
REPLACEMENT_STRING='<img style="display: block; margin: auto; width: 50%;" src="../../../jdaviz_placeholder_new.png">'

# Function to replace lines in a file
replace_lines_in_file() {
    local file=$1
    if grep -q "$SEARCH_STRING" "$file"; then
        sed -i "s|.*$SEARCH_STRING.*|$REPLACEMENT_STRING|g" "$file"
    fi
}

# Export the function to use it with find
export -f replace_lines_in_file
export SEARCH_STRING
export REPLACEMENT_STRING

# Search for all HTML files and replace lines
find "$ROOT_DIR" -type f -name "*.html" -exec bash -c 'replace_lines_in_file "$0"' {} \;

echo "Replacement complete."
