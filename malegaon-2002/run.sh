#!/bin/bash

PDF_DIR="pdf"
JSON_DIR="json"
PY_SCRIPT="script.py"

mkdir -p "$JSON_DIR"

# Process PDFs in ls -ltr order (oldest first)
for file in $(ls -1tr "$PDF_DIR"/*.pdf 2>/dev/null); do
    base=$(basename "$file")
    filename="${base%.pdf}"

    echo "Processing $base ..."
    python3 "$PY_SCRIPT" -i "$file" -o "$JSON_DIR/$filename.json"
done

echo "---------------------------"
echo "All PDFs processed."
