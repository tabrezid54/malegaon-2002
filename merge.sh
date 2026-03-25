#!/bin/bash

JSON_DIR="json"       # folder with your JSON files
OUTPUT="malegaon.json"

# Start a new array
echo "[" > $OUTPUT

# Loop through files
first=true
for f in $JSON_DIR/*.json; do
  if [ "$first" = true ]; then
    jq -c '.[]' "$f" >> $OUTPUT
    first=false
  else
    echo "," >> $OUTPUT
    jq -c '.[]' "$f" >> $OUTPUT
  fi
done

# Close the array
echo "]" >> $OUTPUT

echo "✅ Appended $(ls $JSON_DIR/*.json | wc -l) files into $OUTPUT"

