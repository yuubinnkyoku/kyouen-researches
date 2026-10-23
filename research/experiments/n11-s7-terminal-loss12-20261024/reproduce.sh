#!/usr/bin/env bash
set -euo pipefail
D=research/experiments/n11-s7-terminal-loss12-20261024
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
python3 "$D/verify.py" --emit-s10 "$T/s10.keys"
c++ -std=c++17 -O2 -Wall -Wextra "$D/verify_s10_cpp.cpp" -o "$T/verify_s10_cpp"
"$T/verify_s10_cpp" "$T/s10.keys" > "$T/cpp.tsv"
python3 "$D/verify.py" --check --cpp-tsv "$T/cpp.tsv"
python3 - "$T/cpp.tsv" "$T/tampered.tsv" <<'PY'
from pathlib import Path
import sys
lines = Path(sys.argv[1]).read_text().splitlines()
lines[0] = lines[0].replace(' WIN ', ' LOSS ', 1) if ' WIN ' in lines[0] else lines[0].replace(' LOSS ', ' WIN ', 1)
Path(sys.argv[2]).write_text('\n'.join(lines) + '\n')
PY
if python3 "$D/verify.py" --check-cpp-known --cpp-tsv "$T/tampered.tsv" >/dev/null 2>&1; then
    echo 'FAIL: tampered C++ verdict accepted' >&2
    exit 1
fi
python3 - "$D/certificate.json" "$T/tampered.json" <<'PY'
import json
from pathlib import Path
import sys
cert = json.loads(Path(sys.argv[1]).read_text())
cert['s10_loss_cover12'][0] = '0' * 32
Path(sys.argv[2]).write_text(json.dumps(cert))
PY
if python3 "$D/verify.py" --certificate "$T/tampered.json" --emit-s10 "$T/tampered.keys" >/dev/null 2>&1; then
    echo 'FAIL: tampered certificate accepted' >&2
    exit 1
fi
python3 "$D/verify_three_root_minimality.py"
echo 'PASS tampered C++ verdict and certificate rejected; empty=UNKNOWN'
