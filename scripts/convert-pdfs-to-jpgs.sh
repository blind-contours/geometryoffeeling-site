#!/bin/bash
# Convert all final_series PDFs to JPGs for the website.
# Uses macOS sips: 1800px wide, JPEG quality 92.
# Output: public/prints/{series}/{piece}.jpg

set -e

BASE_DIR="mathematical_affect"
OUT_BASE="public/prints"

converted=0
errors=0

for series_dir in "$BASE_DIR"/*/final_series; do
    [ -d "$series_dir" ] || continue
    series=$(basename "$(dirname "$series_dir")")
    out_dir="$OUT_BASE/$series"
    mkdir -p "$out_dir"

    for pdf in "$series_dir"/*.pdf; do
        [ -f "$pdf" ] || continue
        name=$(basename "$pdf" .pdf)
        jpg="$out_dir/$name.jpg"

        if sips -s format jpeg -s formatOptions 92 --resampleWidth 1800 "$pdf" --out "$jpg" > /dev/null 2>&1; then
            converted=$((converted + 1))
        else
            echo "  ERROR: $pdf"
            errors=$((errors + 1))
        fi
    done
    echo "  $series: done"
done

echo ""
echo "Converted $converted PDFs to JPGs ($errors errors)"
