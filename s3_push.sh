#!/bin/bash

JSON_DIR="json"
S3_BUCKET="s3://voter-list-2002/malegaon/"

# Exit if json folder doesn't exist
if [ ! -d "$JSON_DIR" ]; then
    echo "❌ JSON directory not found: $JSON_DIR"
    exit 1
fi

# Upload files in sorted order (ls -ltr)
for file in $(ls -1tr "$JSON_DIR"/*.json 2>/dev/null); do
    echo "⬆ Uploading: $file"
    aws s3 cp "$file" "$S3_BUCKET"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to upload: $file"
        exit 1
    fi
done

echo "✔ All JSON files uploaded successfully!"
