#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
D="$ROOT/research/experiments/n11-s9-win29-lift-20261023"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
python3 "$D/verify.py" --emit-s10 "$TMP/s10-734.keys"
c++ -O3 -std=c++17 -Wall -Wextra "$D/shared734.cpp" -o "$TMP/shared734"
"$TMP/shared734" "$TMP/s10-734.keys" 0 1 0 | grep -q 'states=255458 lookups=431861 hits=176403 edges=431127'
"$TMP/shared734" "$TMP/s10-734.keys" 0 1 1 | grep -q 'states=255458 lookups=431861 hits=176403 edges=431127'
"$TMP/shared734" "$TMP/s10-734.keys" 0 1 2 | grep -q 'states=123684 lookups=243473 hits=119789 edges=242739'
"$TMP/shared734" "$TMP/s10-734.keys" 0 1 3 | grep -q 'states=103277 lookups=214928 hits=111651 edges=214194'
"$TMP/shared734" "$TMP/s10-734.keys" 1 7 3 | grep -q 'states=55010 lookups=94068 hits=39058 edges=93334'
python3 "$D/verify_shared734.py" --keys "$TMP/s10-734.keys"
sed '1s/^0/1/' "$TMP/s10-734.keys" > "$TMP/bad.keys"
if "$TMP/shared734" "$TMP/bad.keys" 1 7 3 >/dev/null 2>&1; then
  echo 'ERROR: C++ accepted a corrupt leaf' >&2; exit 1
fi
if python3 "$D/verify_shared734.py" --keys "$TMP/bad.keys" >/dev/null 2>&1; then
  echo 'ERROR: Python accepted a corrupt leaf' >&2; exit 1
fi
echo 'PASS: independent 734-leaf shared-D4 verification and mutation rejection'
