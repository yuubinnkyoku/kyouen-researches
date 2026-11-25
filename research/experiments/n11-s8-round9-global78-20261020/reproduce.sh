#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS >/dev/null
python3 verify_proof.py round9_proof_optimized.tsv
FULL=0 python3 verify_loss6_global.py
python3 verify_s7_s6.py
python3 mutation_tests.py
python3 test_merge_s10.py
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
: "${CXX:=g++}"
"$CXX" -O2 -std=c++20 -DNDEBUG verify_s10_direct.cpp -o "$TMPDIR/check10"
"$TMPDIR/check10" round9_opt_leaves.txt "$TMPDIR/opt.tsv"
cmp round9_opt_cpp.tsv "$TMPDIR/opt.tsv"
"$TMPDIR/check10" loss6_all_s10.txt "$TMPDIR/boundary.tsv"
cmp loss6_all_s10_cpp.tsv "$TMPDIR/boundary.tsv"
"$TMPDIR/check10" round9_new_s10_keys.txt "$TMPDIR/new.tsv"
cmp round9_new_s10_cpp.tsv "$TMPDIR/new.tsv"
python3 - <<'PYVERIFY'
from pathlib import Path
a=[x.split("\t")[:3] for x in Path("round9_new_s10.tsv").read_text().splitlines()]
b=[x.split("\t")[:3] for x in Path("round9_new_s10_cpp.tsv").read_text().splitlines()]
assert len(a)==len(b)==285 and a==b
print("PASS all 285 new S10 C++/Python agreement")
PYVERIFY
if [[ "${FULL:-0}" == 1 ]]; then python3 verify_cpp_python.py; fi
python3 merge_s10.py "$TMPDIR/merged.tsv"
cmp merged_s10_9739.tsv "$TMPDIR/merged.tsv"
# Four disjoint independent Python minimax passes, modest shared-server parallelism.
if [[ "${FULL:-0}" == 1 ]]; then
pids=()
for r in '0 365' '365 730' '730 1095' '1095 1461'; do
  (python3 verify_loss6_boundary.py $r > "$TMPDIR/py_${r// /_}.log" 2>&1) &
  pids+=("$!")
done
for pid in "${pids[@]}"; do wait "$pid"; done
cat "$TMPDIR"/py_*.log
fi
if [[ "${FULL_PRIOR:-0}" == 1 ]]; then
  pids=()
  for r in '0 1000' '1000 2000' '2000 3000' '3000 3975'; do
    (python3 verify_round8_s10.py $r > "$TMPDIR/prior_${r// /_}.log" 2>&1) &
    pids+=("$!")
  done
  for pid in "${pids[@]}"; do wait "$pid"; done
  cat "$TMPDIR"/prior_*.log
fi
echo 'PASS all 22-root proofs and global 78-leaf optimum; UNKNOWN empty-board outcome'
