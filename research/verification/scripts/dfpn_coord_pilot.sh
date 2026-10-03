#!/bin/bash
# Pilot: run the adaptive coordinator on reply r2=0 for a few classes.
#
# This is the experiment that decides whether "widest coverage first" or
# "fewest unknown s5 first" is the better rule -- currently an
# assumption. Per class it reports coverage size, unknown s5 count before
# the work, the verdict, nodes and wall time.
cd /mnt/d/ghq/build11 || exit 1
OUT=logs/coord
mkdir -p "$OUT"
CACHE=${CACHE:-logs/s5cache/s5_verdicts.csv}
R2=${R2:-0}
MAX=${MAX:-8}
WALL=${WALL:-1500}

rm -f "$OUT/r$R2.txt"
timeout $((WALL + 300)) ./dfpn --n=11 --memo=24 --coord \
  --coord-r2="$R2" --coord-max="$MAX" --coord-wall="$WALL" \
  --s5-cache="$CACHE" > "$OUT/r$R2.txt" 2>&1
echo "rc=$?"
cat "$OUT/r$R2.txt"