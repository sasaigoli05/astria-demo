#!/usr/bin/env bash
# Render every scene to MP4 with htmlrec (npm i -g htmlrec).
# Run from this folder:  bash record.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out

echo "→ 01-mortality (14s)"
hrec render scenes/01-mortality.html -o out/01-mortality.mp4 -d 14 -f 60 --width 1920 --height 1080
echo "→ 02-chronic (8s)"
hrec render scenes/02-chronic.html -o out/02-chronic.mp4 -d 8 -f 60 --width 1920 --height 1080
echo "→ 03-ownership (22s)"
hrec render scenes/03-ownership.html -o out/03-ownership.mp4 -d 22 -f 60 --width 1920 --height 1080
echo "→ 04-astria (12s)"
hrec render scenes/04-astria.html -o out/04-astria.mp4 -d 12 -f 60 --width 1920 --height 1080
echo "→ 05-argo (22s)"
hrec render scenes/05-argo.html -o out/05-argo.mp4 -d 22 -f 60 --width 1920 --height 1080
echo "→ 06-id (18s)"
hrec render scenes/06-id.html -o out/06-id.mp4 -d 18 -f 60 --width 1920 --height 1080
echo "→ 07-evidence (14s)"
hrec render scenes/07-evidence.html -o out/07-evidence.mp4 -d 14 -f 60 --width 1920 --height 1080
echo "→ 08-promoter (20s)"
hrec render scenes/08-promoter.html -o out/08-promoter.mp4 -d 20 -f 60 --width 1920 --height 1080
echo "→ 09-network (14s)"
hrec render scenes/09-network.html -o out/09-network.mp4 -d 14 -f 60 --width 1920 --height 1080
echo "→ 10-implementation (20s)"
hrec render scenes/10-implementation.html -o out/10-implementation.mp4 -d 20 -f 60 --width 1920 --height 1080
echo "→ 11-outcome (12s)"
hrec render scenes/11-outcome.html -o out/11-outcome.mp4 -d 12 -f 60 --width 1920 --height 1080
echo "→ 12-map (20s)"
hrec render scenes/12-map.html -o out/12-map.mp4 -d 20 -f 60 --width 1920 --height 1080
echo "→ 13-pathway (16s)"
hrec render scenes/13-pathway.html -o out/13-pathway.mp4 -d 16 -f 60 --width 1920 --height 1080
echo "→ 14-close (18s)"
hrec render scenes/14-close.html -o out/14-close.mp4 -d 18 -f 60 --width 1920 --height 1080

echo "Done. MP4s are in ./out"
