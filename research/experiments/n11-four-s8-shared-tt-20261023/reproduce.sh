#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
D="$ROOT/research/experiments/n11-four-s8-shared-tt-20261023"
P="$ROOT/research/experiments/n11-four-s8-joint-terminal52-20261023"
BIN=$(mktemp)
trap 'rm -f "$BIN"' EXIT HUP INT TERM
c++ -O3 -std=c++17 -Wall -Wextra "$D/shared52.cpp" -o "$BIN"
python3 "$P/verify_global.py" --skip-terminal
"$BIN" "$P/selected52.keys" 0 reverse
"$BIN" "$P/selected52.keys" 1 reverse
"$BIN" "$P/selected52.keys" 6 reverse separate
"$BIN" "$P/selected52.keys" 6 reverse
python3 "$D/verify_shared52.py" "$P/selected52.keys" reverse separate
python3 "$D/verify_shared52.py" "$P/selected52.keys" reverse
