#!/bin/bash

# Define the directory and the placeholder image HTML
directory="notebooks"
placeholder='<img align="center" height="auto" width="50%" src="../../jdaviz_placeholder_new.png">'

cp jdaviz_placeholder_new.png _build/html/

# Use find to search for HTML files and process them with sed
find "$directory" -type f -name "*.html" | while read -r file; do
    sed -i "/vnd.jupyter.widget-view+json/c\\$placeholder" "$file"
done

# Remove original tag
find _build/html/notebooks -name "*.html" | xargs -I {} sed -i '/vnd.jupyter.widget-state+json/d' {}

