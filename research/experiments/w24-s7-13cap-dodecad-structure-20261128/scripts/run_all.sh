#!/usr/bin/env bash
# run_all.sh — full reproduction of this experiment (Git Bash, gcc, python 3).
# Heavy stage (grundy_fullcheck) runs at most 4 parallel processes.
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"
cd "$REPO"
EXP=research/experiments/w24-s7-13cap-dodecad-structure-20261128
BOARD=research/experiments/design-kyouen-witt-20261125/output/board_w24.txt
PY=${PY:-python}

mkdir -p "$EXP/output" "$EXP/build"
gcc -O2 -Wall -o "$EXP/build/gen_structure.exe" "$EXP/scripts/gen_structure.c"
gcc -O2 -Wall -o "$EXP/build/grundy_fullcheck.exe" "$EXP/scripts/grundy_fullcheck.c"

echo "== stage 1: Golay span, dodecads, 13-cap enumeration, incidence, 66/12 split =="
"$EXP/build/gen_structure.exe" "$BOARD" \
  "$EXP/output/golay_weights.txt" "$EXP/output/caps13.txt" "$EXP/output/d11.txt" \
  "$EXP/output/nond11_masks.bin" "$EXP/output/stage1_summary.json"

( cd "$EXP/output" && sha256sum golay_weights.txt caps13.txt d11.txt nond11_masks.bin > hashes.txt )

echo "== python cross-check (independent re-derivation) =="
"$PY" -I "$EXP/scripts/check_golay.py" "$BOARD" \
  "$EXP/output/golay_weights.txt" "$EXP/output/caps13.txt" "$EXP/output/d11.txt" \
  "$EXP/output/nond11_masks.bin" "$EXP/output/hashes.txt" "$EXP/output/crosscheck.json"

echo "== stage 2 probe (2000 masks, timing) =="
"$EXP/build/grundy_fullcheck.exe" "$BOARD" "$EXP/output/caps13.txt" "$EXP/output/d11.txt" \
  "$EXP/output/nond11_masks.bin" 0 1 2000 0 "$EXP/output/probe.json"

echo "== stage 2 full sweep: all 2,040,192 non-d11 11-subsets, 4 parallel parts =="
for i in 0 1 2 3; do
  "$EXP/build/grundy_fullcheck.exe" "$BOARD" "$EXP/output/caps13.txt" "$EXP/output/d11.txt" \
    "$EXP/output/nond11_masks.bin" "$i" 4 0 0 "$EXP/output/grundy_part$i.json" &
done
wait

echo "== merge =="
"$PY" -I "$EXP/scripts/merge_results.py" "$EXP/output"
echo "done: $EXP/output/structure_summary.json"
