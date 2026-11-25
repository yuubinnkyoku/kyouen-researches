#!/usr/bin/env bash
# Extract + verify one cost72d WIN7 certificate (2026-11-17).
# Usage: ev72d.sh <bit>
set -eu
BIT="$1"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
SCR="$HERE/scripts"
WORK="$HERE/output/class2-lane-cost72d-certificates"
CHILD=00000000000000403800000008004000
ROOT=$(python3 - "$CHILD" "$BIT" <<'EOF'
import sys
child = int(sys.argv[1], 16)
print(f"{child | (1 << int(sys.argv[2])):032x}")
EOF
)
CERT="$WORK/n11_s7_${ROOT}.cert"
python3 "$SCR/legal_candidates.py" "$ROOT" | tail -1 > "$WORK/bit${BIT}-moves.txt"
node --experimental-strip-types "$SCR/cert_driver71e.ts" "$CHILD" "$BIT" "$CERT" \
  < "$WORK/bit${BIT}-moves.txt" > "$WORK/bit${BIT}-extract.stdout" 2> "$WORK/bit${BIT}-extract.err"
bash "$SCR/verify_cost72d_one.sh" "$BIT" "$ROOT" "$CERT"
md5sum "$CERT"
echo "EV72D DONE bit $BIT root $ROOT"
