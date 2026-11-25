#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
HERE=research/experiments/n11-s9-loss12-frontier-20261024
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
c++ -O3 -std=c++17 research/experiments/n11-s7-terminal-loss12-20261024/verify_s10_cpp.cpp -o "$TMP/s10check"
"$TMP/s10check" "$HERE/s10-loss12.keys" > "$TMP/recomputed.tsv"
diff -u "$HERE/s10-loss12-cpp.tsv" "$TMP/recomputed.tsv"
python "$HERE/verify.py" --cpp-tsv "$TMP/recomputed.tsv"
python "$HERE/audit.py"
sed '1s/ LOSS / WIN /' "$TMP/recomputed.tsv" > "$TMP/tampered.tsv"
if python "$HERE/verify.py" --cpp-tsv "$TMP/tampered.tsv" > "$TMP/tamper.log" 2>&1; then
  echo 'FAIL: altered C++ verdict was accepted' >&2
  exit 1
fi
printf 'PASS: tampered verdict rejected; empty=UNKNOWN\n'
