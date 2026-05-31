#!/usr/bin/env bash
# Delete all rendered Manim videos to force a fresh re-render on next run.
set -euo pipefail

MEDIA_DIR="$(dirname "$0")/media/videos"

if [ ! -d "$MEDIA_DIR" ]; then
    echo "No media/videos directory found — nothing to clear."
    exit 0
fi

echo "Clearing rendered videos in $MEDIA_DIR ..."
find "$MEDIA_DIR" -name "*.mp4" -delete
echo "Done."
