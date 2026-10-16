#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
g++ -std=c++17 -O3 terminal_triple_index.cpp -o "$tmp/terminal"
"$tmp/terminal" --audit-geometry
"$tmp/terminal" --generate > "$tmp/input.txt"
printf '%s  %s\n' 6f740634c6d89441e8ef379b6d5363cc78b9e7cd67c24b9dd250c0507d57f9b6 "$tmp/input.txt" | sha256sum -c -
N11_GEOMETRY_ROOT_AUDIT=1 "$tmp/terminal" "$tmp/input.txt" "$tmp/out.tsv" 7 2325
printf '%s  %s\n' 94aa731461706e0ca023fc59bd9b475df155f184a92143e8d2ce195e6401aa8b "$tmp/out.tsv" | sha256sum -c -
N11_INCREMENTAL_AUDIT=1 "$tmp/terminal" "$tmp/input.txt" "$tmp/audit.tsv" 7 2325
cmp "$tmp/out.tsv" "$tmp/audit.tsv"
head -n 2324 "$tmp/input.txt" > "$tmp/truncated.txt"
if "$tmp/terminal" "$tmp/truncated.txt" "$tmp/negative.tsv" 7 2325 >/dev/null 2>&1; then echo 'FAIL truncated input accepted' >&2; exit 1; fi
printf '%s\n' ffffffffffffffffffffffffffffffff > "$tmp/invalid.txt"
if "$tmp/terminal" "$tmp/invalid.txt" "$tmp/negative.tsv" 7 1 >/dev/null 2>&1; then echo 'FAIL invalid mask accepted' >&2; exit 1; fi
echo 'PASS: 2,325 roots, geometry, per-state legality, hashes, and negative tests; empty root UNKNOWN'
