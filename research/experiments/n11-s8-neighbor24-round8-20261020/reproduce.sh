#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS >/dev/null
python3 verify_proof.py proof24_optimized.tsv
python3 verify_s7.py
python3 verify_loss4_optimal.py
python3 mutation_tests.py
: "${CXX:=g++}"
"$CXX" -O2 -std=c++20 -DNDEBUG verify_s10_direct.cpp -o /tmp/n11-round8-verify10-$$
trap 'rm -f /tmp/n11-round8-verify10-$$ /tmp/n11-round8-cpp-$$.tsv' EXIT
/tmp/n11-round8-verify10-$$ proof_s10_leaves.txt /tmp/n11-round8-cpp-$$.tsv
cmp proof_s10_cpp.tsv /tmp/n11-round8-cpp-$$.tsv
if [[ "${FULL:-0}" == 1 ]]; then
  /tmp/n11-round8-verify10-$$ all_s10.txt /tmp/n11-round8-cpp-$$.tsv
  cmp all_s10_cpp.tsv /tmp/n11-round8-cpp-$$.tsv
fi
if [[ "${PY_FULL:-0}" == 1 ]]; then
  python3 verify_all_s10.py 0 3975
fi
printf '%s\n' 'PASS reproducible round8 terminal-only proof and 41-leaf optimality'
