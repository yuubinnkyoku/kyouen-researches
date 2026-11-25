#!/usr/bin/env bash
# Independent verification orchestrator for one cost-72d WIN7 certificate (2026-11-17).
# Usage: verify_cost72d_one.sh <bit> <root_hex> <cert_file>
# Runs verify_bit7_win7_cert.ts root-check + all sub-roots in batches, accumulates the
# consumed winner-state union and compares it with the certificate row set.
set -u
BIT="$1"; ROOT="$2"; CERT="$3"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
SCR="$HERE/scripts"
WORK="$HERE/output/class2-lane-cost72d-certificates"
CONS="$WORK/bit${BIT}-consumed.txt"
rm -f "$CONS"
MOVES=$(python3 "$SCR/legal_candidates.py" "$ROOT" | tail -1)
IFS=',' read -ra ARR <<< "$MOVES"
N=${#ARR[@]}
echo "bit $BIT root $ROOT moves $N cert $CERT"
RC=$(node --experimental-strip-types "$SCR/verify_bit7_win7_cert.ts" --cert "$CERT" --root "$ROOT" --root-check --subroots "")
echo "rootcheck: $RC"
echo "$RC" > "$WORK/bit${BIT}-rootcheck.json"
B=8
FAIL=0
: > "$WORK/bit${BIT}-subroots.jsonl"
for ((i=0; i<N; i+=B)); do
  BATCH=("${ARR[@]:i:B}")
  SUB=$(IFS=,; echo "${BATCH[*]}")
  OUT=$(node --experimental-strip-types "$SCR/verify_bit7_win7_cert.ts" --cert "$CERT" --root "$ROOT" --subroots "$SUB" --consumed-out "$CONS") || { echo "SUBROOT BATCH FAIL at $SUB"; FAIL=1; break; }
  echo "$OUT" >> "$WORK/bit${BIT}-subroots.jsonl"
  echo "batch $SUB ok"
done
[ "$FAIL" -eq 0 ] || { echo "VERIFICATION FAILED bit $BIT"; exit 1; }
sort -u "$CONS" > "$WORK/bit${BIT}-consumed-sorted.txt"
tail -n +3 "$CERT" | cut -d' ' -f1 > "$WORK/bit${BIT}-certkeys.txt"
MISS=$(comm -23 "$WORK/bit${BIT}-certkeys.txt" "$WORK/bit${BIT}-consumed-sorted.txt" | wc -l)
EXTRA=$(comm -13 "$WORK/bit${BIT}-certkeys.txt" "$WORK/bit${BIT}-consumed-sorted.txt" | wc -l)
NC=$(wc -l < "$WORK/bit${BIT}-consumed-sorted.txt")
NK=$(wc -l < "$WORK/bit${BIT}-certkeys.txt")
echo "bit $BIT: certrows $NK consumed $NC union_missing $MISS union_extra $EXTRA"
