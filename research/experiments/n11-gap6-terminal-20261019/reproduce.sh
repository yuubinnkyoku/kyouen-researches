#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
CXX="${CXX:-g++}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
"$CXX" -O3 -std=c++20 verify_s10_direct.cpp -o "$TMP/verify_s10"
"$TMP/verify_s10" s10-probe19-input.txt "$TMP/s10-recomputed.tsv"
diff -u s10-probe19-results.tsv "$TMP/s10-recomputed.tsv"
"$TMP/verify_s10" s8-new-all-s10.txt "$TMP/s8-boundary-recomputed.tsv"
diff -u s8-new-all-s10-results.tsv "$TMP/s8-boundary-recomputed.tsv"
python3 verify_gap6_terminal.py
