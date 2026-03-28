#!/bin/bash

output="files.json"

echo "[" > "$output"

files=( *.json )
count=${#files[@]}

for ((i=0; i<count; i++)); do
    if [ $i -lt $((count-1)) ]; then
        echo "  \"${files[$i]}\"," >> "$output"
    else
        echo "  \"${files[$i]}\"" >> "$output"
    fi
done

echo "]" >> "$output"

echo "Created $output"

