#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
D="$ROOT/research/experiments/n11-four-s8-shared-tt-20261023"
P="$ROOT/research/experiments/n11-four-s8-joint-terminal52-20261023"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
c++ -O3 -std=c++17 -Wall -Wextra "$D/adaptive52.cpp" -o "$TMP/adaptive52"
python3 "$P/verify_global.py" --skip-terminal
"$TMP/adaptive52" plan "$P/selected52.keys" "$D/adaptive52-weights.txt" "$TMP/schedule.tsv" | grep -q 'PASS command=plan roots=52 states=6563 lookups=10944 hits=4381 children=10892'
cmp "$D/adaptive52-schedule.tsv" "$TMP/schedule.tsv"
"$TMP/adaptive52" verify "$P/selected52.keys" "$D/adaptive52-schedule.tsv" | grep -q 'PASS command=verify roots=52 states=6563 lookups=10944 hits=4381 children=10892'
python3 "$D/verify_adaptive52.py" "$P/selected52.keys" "$D/adaptive52-schedule.tsv"
# Negative control: a wrong first root must be rejected by both independent verifiers.
sed '1s/^000800/000900/' "$D/adaptive52-schedule.tsv" > "$TMP/bad-schedule.tsv"
if "$TMP/adaptive52" verify "$P/selected52.keys" "$TMP/bad-schedule.tsv" > /dev/null 2>&1; then
  echo 'ERROR: C++ accepted mutated schedule' >&2; exit 1
fi
if python3 "$D/verify_adaptive52.py" "$P/selected52.keys" "$TMP/bad-schedule.tsv" > /dev/null 2>&1; then
  echo 'ERROR: Python accepted mutated schedule' >&2; exit 1
fi
echo 'PASS: adaptive52 schedule replay, independent geometry, and negative control'
