#!/usr/bin/env bash
set -euo pipefail
D=research/experiments/n11-s10-joint-cache-20261024
S9=research/experiments/n11-s9-win29-lift-20261023
S52=research/experiments/n11-four-s8-shared-tt-20261023
CERT=research/experiments/n11-four-s8-joint-terminal52-20261023
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
python3 "$S9/verify.py" --emit-s10 "$T/s10.keys"
sha256sum "$T/s10.keys"
c++ -O3 -std=c++17 "$D/verify_joint.cpp" -o "$T/joint"
for mode in 0 1; do
  "$T/joint" "$T/s10.keys" "$S9/schedule734-compact.txt" "$S52/adaptive52-schedule.tsv" "$CERT/selected52.keys" "$mode"
done
python3 "$D/verify_joint.py"
# Negative control: an invalid schedule number must fail, not be silently ignored.
cp "$S9/schedule734-compact.txt" "$T/bad-schedule.txt"
python3 - "$T/bad-schedule.txt" <<'PY'
import sys
from pathlib import Path
p=Path(sys.argv[1]); s=''.join(p.read_text().split()); p.write_text('ff'+s[2:]+'\n')
PY
if "$T/joint" "$T/s10.keys" "$T/bad-schedule.txt" "$S52/adaptive52-schedule.tsv" "$CERT/selected52.keys" 0 >/dev/null 2>&1; then
  echo 'FAIL: bad schedule accepted' >&2
  exit 1
fi
echo 'PASS invalid schedule rejected; empty=UNKNOWN'
