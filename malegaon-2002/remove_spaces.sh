#!/bin/bash

PDF_DIR="pdfs"

for file in "$PDF_DIR"/*.pdf; do
    # Get the original filename
    base=$(basename "$file")
    
    # Remove spaces only (keep hyphens, numbers, dots, etc.)
    new_base=$(echo "$base" | tr -d ' ')
    
    # Rename only if the name actually changes
    if [ "$base" != "$new_base" ]; then
        echo "Renaming: $base -> $new_base"
        mv "$PDF_DIR/$base" "$PDF_DIR/$new_base"
    fi
done

echo "Spaces removed from filenames."

