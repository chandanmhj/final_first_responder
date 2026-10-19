#!/usr/bin/env bash
# Compress videos and images from media/emergencies/ into media/processed/ for fast loading.
# Needs ffmpeg. Videos: H.264 MP4, max 720p, ~1.2 Mbps, no audio, faststart. Images: WebP 1000px wide.
set -euo pipefail
SRC="${1:-media/emergencies}"
DST="${2:-media/processed}"
find "$SRC" -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.mkv' -o -iname '*.webm' \) | while read -r f; do
  rel="${f#$SRC/}"; out="$DST/${rel%.*}.mp4"; mkdir -p "$(dirname "$out")"
  ffmpeg -y -i "$f" -vf "scale='min(1280,iw)':-2" -c:v libx264 -preset slow -crf 28 -maxrate 1200k -bufsize 2400k -an -movflags +faststart "$out"
done
find "$SRC" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) | while read -r f; do
  rel="${f#$SRC/}"; out="$DST/${rel%.*}.webp"; mkdir -p "$(dirname "$out")"
  ffmpeg -y -i "$f" -vf "scale='min(1000,iw)':-2" -quality 80 "$out"
done
echo "Done. Files are in $DST"
