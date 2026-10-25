#!/usr/bin/env bash
set -euo pipefail
D=research/experiments/n11-s9-terminal-neighbor-20261025
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
c++ -std=c++17 -O2 -Wall -Wextra research/experiments/n11-s7-terminal-loss12-20261024/verify_s10_cpp.cpp -o "$T/check"
"$T/check" "$D/s10-win18.keys" > "$T/cpp.tsv"
python3 "$D/verify.py" --cpp-tsv "$T/cpp.tsv" --negative
