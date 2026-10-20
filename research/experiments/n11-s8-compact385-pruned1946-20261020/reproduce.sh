#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
python3 audit_pruning.py
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cat selected385.txt <(cut -f1 win_witnesses1561.tsv) | sort -u > "$work/keys.txt"
g++ -O3 -std=c++20 verify_s10_direct.cpp -o "$work/verify_s10"
"$work/verify_s10" "$work/keys.txt" "$work/results.tsv"
python3 check_cpp.py "$work/results.tsv"
g++ -O3 -std=c++20 exact_cover_fast.cpp -o "$work/exact_cover"
python3 core_gap.py --matrix > "$work/core.matrix"
"$work/exact_cover" < "$work/core.matrix"
python3 gen_exact.py 6 > "$work/component6.matrix"
"$work/exact_cover" < "$work/component6.matrix"
printf '1 0 1\n1 0 0\n' | "$work/exact_cover" > "$work/sat.txt" && { echo 'ERROR: accepted SAT matrix as UNSAT'; exit 1; } || test "$?" -eq 2
# A zero-only column must remain usable after all positive rows are covered.
printf '1 1 2\n1 0 0\n0 1 0\n' | "$work/exact_cover" > "$work/sat-zero.txt" && { echo 'ERROR: accepted SAT matrix as UNSAT'; exit 1; } || test "$?" -eq 2
python3 -u verify_compact385.py
python3 -u verify_essential115.py
python3 -u verify_essential100.py
if [[ "${NEGATIVE:-0}" == 1 ]]; then python3 -u mutation_tests.py; fi
