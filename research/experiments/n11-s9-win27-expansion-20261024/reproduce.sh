#!/usr/bin/env bash
set -euo pipefail
D=research/experiments/n11-s9-win27-expansion-20261024
CPP=research/experiments/n11-four-s8-joint-terminal52-20261023/verify_s10_direct.cpp
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
python3 "$D/verify.py" --emit-s10 "$T/s10.keys"
c++ -O3 -std=c++17 "$CPP" -o "$T/terminal"
"$T/terminal" "$T/s10.keys" "$T/s10.tsv"
python3 "$D/verify.py" --check --cpp-tsv "$T/s10.tsv"
# A fabricated opposite verdict must not be accepted as a certificate.
python3 - "$T/s10.tsv" "$T/bad.tsv" <<'PY'
import sys
from pathlib import Path
s=Path(sys.argv[1]).read_text().splitlines()
s[0]=s[0].replace(' WIN ', ' LOSS ', 1)
Path(sys.argv[2]).write_text('\n'.join(s)+'\n')
PY
if python3 "$D/verify.py" --check --cpp-tsv "$T/bad.tsv" >/dev/null 2>&1; then
  echo 'FAIL: mutated verdict accepted' >&2
  exit 1
fi
echo 'PASS mutated verdict rejected; empty=UNKNOWN'
