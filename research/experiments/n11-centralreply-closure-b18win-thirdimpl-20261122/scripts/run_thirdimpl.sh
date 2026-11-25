#!/bin/bash
# run_thirdimpl.sh <key_id> <runtag> <kind>  -- kind: target|anchor|negative
# One third-implementation solver process per row (1 solver / 1 row / 1 process).
# Result appended to output/status.log. Determinism pairs are (a, b).
#
# lo/hi/legal/stones are taken from the machine-derived input CSV STRINGS
# (input/<key>.input.csv). Never round-trip 121-bit keys through a JS Number:
# JSON.parse -> Number -> String mangles mantissa-precision integers
# (observed: 1297036692683751424 -> "...1400", flipping popcount 5 -> 20).
# The driver independently re-derives the legal count and the stone popcount from
# the board and fails closed on any mismatch (GATE_FAIL), so a mangled key
# cannot run silently.
set -u
KEY="$1"; TAG="$2"; KIND="$3"
cd "$(dirname "$0")/.."
DIR=output/targets; [ "$KIND" = "anchor" ] && DIR=output/anchors; [ "$KIND" = "negative" ] && DIR=output/negative
SRC="input/$KEY.input.csv"
[ -f "$SRC" ] || { echo "RUN key=$KEY MISSING-INPUT" >> output/status.log; exit 48; }
# input CSV shape gate (pure string)
IFS=, read -r C0 C1 STONES LO HI LEGAL R0 R1 R2 R3 R4 R5 <<< "$(cat "$SRC")"
[ "$C0" = "target" ] && [ "$C1" = "0" ] && [ -n "$LO" ] && [ -n "$HI" ] && [ -n "$LEGAL" ] && [ -n "$STONES" ] || { echo "RUN key=$KEY INPUT-SHAPE-FAIL" >> output/status.log; exit 49; }
# key must be declared in rows.json (presence check only; numeric equality is
# audited by scripts/audit.py in exact Python integers)
grep -q "\"key_id\": \"$KEY\"" input/rows.json || { echo "RUN key=$KEY NOT-IN-ROWS" >> output/status.log; exit 50; }
mkdir -p "$DIR"
OUTF="$DIR/$KEY.$TAG.out"
node scripts/third_impl.js "--stones=$STONES" "--legal=$LEGAL" "--lo=$LO" "--hi=$HI" \
  --row="$KEY$TAG" --cap=300000000 --wallcap=240 --memo-power=22 > "$OUTF" 2>&1
RC=$?
echo "RUN key=$KEY tag=$TAG kind=$KIND rc=$RC out=$OUTF $(grep -o '^third,.*' "$OUTF" | head -1)" >> output/status.log
exit $RC
