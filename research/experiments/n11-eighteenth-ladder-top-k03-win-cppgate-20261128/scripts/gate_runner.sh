#!/bin/bash
# Eighteenth ladder-top k03 WIN-row (key 1155173441859489792:131072, class 20421, budget 15000000) C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>
#   key        = input/<key>.input.csv (byte-clone of the published eighteenth escalation kit input)
#   budget     = exact-replay node budget of the row's published probe condition
#   expected   = "legal,budget,result,nodes" pinned from the published raw (SSOT)
# Machine-identical to the published seventeenth k02 gate runner (only this comment block names the eighteenth k03 pillars kit). Two fresh-cold passes (one process per pass, like the
# drive runners). Acceptance: p1 == p2 on (legal,budget,result,nodes); both == expected. FAIL-closed.
set -u
key="$1"; budget="$2"; expected="$3"
dir="$(cd "$(dirname "$0")/.." && pwd)"
bin="${GATE_BIN:?point GATE_BIN at the binary built from the pinned gate source}"
test -x "$bin" || { echo "GATE_BIN not executable: $bin" >&2; exit 2; }
test -f "$dir/input/$key.input.csv" || { echo "missing input/$key.input.csv" >&2; exit 2; }
mkdir -p "$dir/output/raw"
for p in p1 p2; do
  out="$dir/output/raw/$key.$p.out"
  if [ -f "$out" ]; then
    if grep -q "# replay_done" "$out"; then :; else rm -f "$out"; echo "$(date -u +%FT%TZ) $key $p-TRUNCATED-RETRY" >> "$dir/output/gate-status.log"; fi
  fi
  if ! [ -f "$out" ]; then
    "$bin" --n=11 --memo=22 --only=5 --exact-order=count \
      --exact-replay="$dir/input/$key.input.csv" --exact-replay-budget="$budget" > "$out" 2>&1
  fi
  grep -q "# replay_done" "$out" || { echo "$(date -u +%FT%TZ) $key GATE-CRASH $p (no replay_done)" >> "$dir/output/gate-status.log"; echo "GATE-CRASH $key $p"; exit 41; }
done
f1=$(grep "^replay," "$dir/output/raw/$key.p1.out" | cut -d, -f4,6,7,8)
f2=$(grep "^replay," "$dir/output/raw/$key.p2.out" | cut -d, -f4,6,7,8)
if [ -z "$f1" ] || [ -z "$f2" ]; then echo "$(date -u +%FT%TZ) $key GATE-FAIL missing-replay-row" >> "$dir/output/gate-status.log"; echo "GATE-FAIL $key missing replay row"; exit 46; fi
if [ "$f1" != "$f2" ]; then
  echo "$(date -u +%FT%TZ) $key MISMATCH p1=$f1 p2=$f2" >> "$dir/output/gate-status.log"
  echo "HARD-STOP: determinism mismatch on $key"; exit 42
fi
if [ "$f1" != "$expected" ]; then
  echo "$(date -u +%FT%TZ) $key GATE-FAIL p1=$f1 expected=$expected" >> "$dir/output/gate-status.log"
  echo "HARD-STOP: published-row disagreement on $key (C5: no interpretation)"; exit 43
fi
echo "$(date -u +%FT%TZ) $key GATE-PASS $f1 (2-pass determinism + published-raw node-exact)" >> "$dir/output/gate-status.log"
echo "$key GATE-PASS $f1"
exit 0
