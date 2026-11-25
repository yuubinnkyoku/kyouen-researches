#!/usr/bin/env bash
set -euo pipefail
D=research/experiments/n11-s9-win20-neighbor-20261024
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
c++ -std=c++17 -O2 -Wall -Wextra \
  research/experiments/n11-s7-terminal-loss12-20261024/verify_s10_cpp.cpp \
  -o "$T/verify_s10_cpp"
"$T/verify_s10_cpp" "$D/s10-win233.keys" > "$T/s10-cpp.tsv"
python3 "$D/verify.py" --cpp-tsv "$T/s10-cpp.tsv" \
  --frozen-win research/experiments/n11-targeted-terminal-lift-20261015/data/lifted_s8_win_51571.txt \
  --frozen-loss research/experiments/n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt
python3 "$D/audit_coverage.py"
head -n -1 "$D/s10-win233.keys" > "$T/missing.keys"
if python3 "$D/verify.py" --cpp-tsv "$T/s10-cpp.tsv" --s10-manifest "$T/missing.keys" >/dev/null 2>&1; then
  echo 'FAIL: missing S10 child accepted' >&2; exit 1
fi
python3 - "$T/s10-cpp.tsv" "$T/tampered.tsv" <<'PY'
from pathlib import Path
import sys
lines = Path(sys.argv[1]).read_text().splitlines()
lines[0] = lines[0].replace(' WIN ', ' LOSS ', 1)
Path(sys.argv[2]).write_text('\n'.join(lines) + '\n')
PY
if python3 "$D/verify.py" --cpp-tsv "$T/tampered.tsv" >/dev/null 2>&1; then
  echo 'FAIL: tampered verdict accepted' >&2; exit 1
fi
echo 'PASS negative controls; empty=UNKNOWN'
