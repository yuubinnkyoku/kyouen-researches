#!/usr/bin/env bash
set -euo pipefail
D=research/experiments/n11-s9-win29-lift-20261023
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
python3 "$D/verify.py" --emit-s10 "$T/s10.keys"
sha256sum "$T/s10.keys"
c++ -O3 -std=c++17 "$D/verify_schedule734.cpp" -o "$T/verify"
"$T/verify" "$T/s10.keys" "$D/schedule734-compact.txt"
python3 "$D/verify_adaptive734.py" "$D/schedule734-compact.txt"
