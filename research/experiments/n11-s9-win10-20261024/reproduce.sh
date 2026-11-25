#!/usr/bin/env bash
set -euo pipefail
D=research/experiments/n11-s9-win10-20261024
CPP=research/experiments/n11-four-s8-joint-terminal52-20261023/verify_s10_direct.cpp
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
python3 "$D/verify.py" --emit-s10 "$T/s10.keys"
c++ -O3 -std=c++17 "$CPP" -o "$T/check_s10"
"$T/check_s10" "$T/s10.keys" "$T/cpp.tsv"
python3 "$D/verify.py" --check --cpp-tsv "$T/cpp.tsv"
python3 - "$T/cpp.tsv" "$T/tampered.tsv" <<'PY'
import sys
from pathlib import Path
lines = Path(sys.argv[1]).read_text().splitlines()
lines[0] = lines[0].replace(' WIN ', ' LOSS ', 1)
Path(sys.argv[2]).write_text('\n'.join(lines) + '\n')
PY
if python3 "$D/verify.py" --check --cpp-tsv "$T/tampered.tsv" >/dev/null 2>&1; then
  echo 'FAIL: tampered verdict accepted' >&2
  exit 1
fi
echo 'PASS altered WIN verdict rejected; standard 11x11 empty=UNKNOWN'
