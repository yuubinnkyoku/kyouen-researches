#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
D=research/experiments/n11-s8-frontier-13way-20261024
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT

python3 "$D/verify.py" --emit-s10 "$T/s10.keys"
c++ -std=c++17 -O2 -Wall -Wextra \
  research/experiments/n11-s7-terminal-loss12-20261024/verify_s10_cpp.cpp \
  -o "$T/s10-cpp"
"$T/s10-cpp" "$T/s10.keys" > "$T/s10-cpp.tsv"
python3 "$D/verify.py" --cpp-tsv "$T/s10-cpp.tsv" --s10-manifest "$T/s10.keys"

head -n -1 "$T/s10.keys" > "$T/incomplete.keys"
if python3 "$D/verify.py" --cpp-tsv "$T/s10-cpp.tsv" \
  --s10-manifest "$T/incomplete.keys" >/dev/null 2>&1; then
  echo "FAIL: missing S10 leaf accepted" >&2; exit 1
fi
python3 - "$T/s10-cpp.tsv" "$T/tampered.tsv" <<'PY'
from pathlib import Path
import sys
lines = Path(sys.argv[1]).read_text().splitlines()
if ' WIN ' in lines[0]:
    lines[0] = lines[0].replace(' WIN ', ' LOSS ', 1)
else:
    lines[0] = lines[0].replace(' LOSS ', ' WIN ', 1)
Path(sys.argv[2]).write_text('\n'.join(lines) + '\n')
PY
if python3 "$D/verify.py" --cpp-tsv "$T/tampered.tsv" >/dev/null 2>&1; then
  echo "FAIL: opposite terminal verdict accepted" >&2; exit 1
fi
echo "PASS negative controls; empty=UNKNOWN"
