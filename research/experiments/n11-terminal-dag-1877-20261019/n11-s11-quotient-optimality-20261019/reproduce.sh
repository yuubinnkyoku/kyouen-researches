#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
python3 n11-s11-dual-branch-optimality-20261019/compact_proof184_342.py
python3 verify_quotient_optimality.py
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
g++ -O3 -std=c++17 n11-s11-dual-branch-optimality-20261019/verify_s11_direct.cpp -o "$TMP/verify_s11"
"$TMP/verify_s11" n11-s11-dual-branch-optimality-20261019/all_s11_candidates.txt "$TMP/recomputed.tsv"
cmp "$TMP/recomputed.tsv" n11-s11-dual-branch-optimality-20261019/all_s11_cpp.tsv
printf 'PASS full C++ direct-board 4,522-candidate audit\n'
if [[ "${1:-}" == '--full-python' ]]; then
    python3 verify_quotient_optimality.py --full-python
fi
