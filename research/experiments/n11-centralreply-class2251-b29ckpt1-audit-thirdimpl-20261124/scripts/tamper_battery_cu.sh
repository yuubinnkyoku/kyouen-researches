#!/bin/bash
# tamper_battery_cu.sh -- Part CU tamper battery against audit_cu.py.
# Constructs sandbox-local copies of the frozen post-run kit, applies one
# pre-registered mutation per case, runs the audit copy, and asserts rc=1
# PLUS the pre-registered first-failing gate name. Any battery deviation is
# itself a failure. Appends the full record to output/tamper-battery.txt and
# exits 0 only if every case is captured and the untouched control passes.
#
# Pre-registered cases (declared in the Part CU declaration note BEFORE any
# solver ran; gate names follow the audit implementation order):
#   T1 replica ab002.p1 nodes 3662776 -> 3662777       expect replica-ab002-det-pair
#   T2 third target ab005.b expansions +1             expect third-target-ab005-det-pair
#   T3 third target ab009 a+b result 2 -> 1 (both)    expect third-target-ab009-verdict-agree
#   T4 replica ab012.p2 '# replay_done' line removed   expect replica-ab012-done
#   T5 published source raw ab013.p2 nodes +1         expect pin-all-73
#   T6 canonical cache: insert fake adopted row        expect pin-all-73
#   T7 anchor l1a.a expansions 7660602 -> 7661602      expect anchor-l1a-a-expansions
#   CONTROL untouched copy                             expect rc=0 ALL GATES PASS
set -u
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
BATT="$ROOT/output/tamper-battery.txt"
: > "$BATT"
FROZEN="$ROOT/../tamper-frozen"
fail() { echo "BATTERY FAIL: $1" | tee -a "$BATT"; exit 1; }

snapshot() {  # snapshot <case-name>
  local dst="$ROOT/../tamper-$1"
  rm -rf "$dst"; cp -a "$FROZEN" "$dst"; echo "$dst"
}

run_case() {  # run_case <case-name> <expected-first-gate>
  local name="$1" expect="$2"
  local out rc first
  out="$(cd "$ROOT/../tamper-$name" && python3 scripts/audit_cu.py 2>&1)"; rc=$?
  first="$(echo "$out" | grep -o 'GATE FAILED: [^ ]+' | head -1 | cut -d' ' -f3-)"
  echo "CASE $name rc=$rc first_gate=${first:-<none>} expected=$expect" >> "$BATT"
  echo "$out" | sed 's/^/    /' >> "$BATT"
  [ "$rc" -eq 1 ] || fail "$name expected rc=1 got rc=$rc"
  [ "$first" = "$expect" ] || fail "$name expected gate '$expect' got '$first'"
}

# T1: replica determinism-layer corruption
d="$(snapshot t1)"; sed -i 's/replay,0,5,97,0,15000000,2,3662776,/replay,0,5,97,0,15000000,2,3662777,/' "$d/output/raw/ab002.p1.out"
echo "TAMPER-T1 replica ab002.p1 nodes 3662776->3662777" >> "$BATT"; run_case t1 "replica-ab002-det-pair"

# T2: third-impl target b-run expansion corruption
d="$(snapshot t2)"
python3 - "$d/output/targets/ab005.b.out" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read().replace("third,ab005b,5,96,96,2,", "third,ab005b,5,96,96,2,")
lines = s.split("\n")
for i, l in enumerate(lines):
    if l.startswith("third,ab005b,"):
        f = l.split(","); f[6] = str(int(f[6]) + 1); lines[i] = ",".join(f)
open(p, "w").write("\n".join(lines))
EOF
echo "TAMPER-T2 third ab005.b expansions +1" >> "$BATT"; run_case t2 "third-target-ab005-det-pair"

# T3: third-impl verdict flip on BOTH runs (det-pair survives; agreement gate fires)
d="$(snapshot t3)"; for tag in a b; do
python3 - "$d/output/targets/ab009.$tag.out" <<'EOF'
import sys
p = sys.argv[1]
lines = open(p).read().split("\n")
for i, l in enumerate(lines):
    if l.startswith("third,ab009"):
        f = l.split(","); f[5] = "1"; lines[i] = ",".join(f)
open(p, "w").write("\n".join(lines))
EOF
done
echo "TAMPER-T3 third ab009 a+b result 2->1" >> "$BATT"; run_case t3 "third-target-ab009-verdict-agree"

# T4: replica truncated-fragment corruption (terminal line removed)
d="$(snapshot t4)"; grep -v '# replay_done' "$d/output/raw/ab012.p2.out" > "$d/output/raw/ab012.p2.out.tmp" && mv "$d/output/raw/ab012.p2.out.tmp" "$d/output/raw/ab012.p2.out"
echo "TAMPER-T4 replica ab012.p2 replay_done removed" >> "$BATT"; run_case t4 "replica-ab012-done"

# T5: published-source corruption (pin layer must fire first)
d="$(snapshot t5)"; sed -i 's/replay,0,5,87,0,15000000,2,2284195,/replay,0,5,87,0,15000000,2,2284196,/' "$d/sources/raw/ab013.p2.out"
echo "TAMPER-T5 published source ab013.p2 nodes +1" >> "$BATT"; run_case t5 "pin-all-73"

# T6: canonical-cache corruption (verdict-consumption forgery; pin layer first)
d="$(snapshot t6)"; printf 's5verdict,1155314042043105281,0,5,2,4265342\n' >> "$d/sources/canonical-cache-co-merged-b28loss7.cache"
echo "TAMPER-T6 canonical cache fake adopted row appended" >> "$BATT"; run_case t6 "pin-all-73"

# T7: anchor semantic corruption
d="$(snapshot t7)"; python3 - "$d/output/anchors/l1a.a.out" <<'EOF'
import sys
p = sys.argv[1]
lines = open(p).read().split("\n")
for i, l in enumerate(lines):
    if l.startswith("third,l1aa,"):
        f = l.split(","); f[6] = "7661602"; lines[i] = ",".join(f)
open(p, "w").write("\n".join(lines))
EOF
echo "TAMPER-T7 anchor l1a.a expansions 7660602->7661602" >> "$BATT"; run_case t7 "anchor-l1a-a-expansions"

# CONTROL: untouched copy must pass everything
d="$(snapshot control)"; out="$(cd "$d" && python3 scripts/audit_cu.py 2>&1)"; rc=$?
echo "CASE control rc=$rc expected rc=0" >> "$BATT"; echo "$out" | sed 's/^/    /' >> "$BATT"
[ "$rc" -eq 0 ] || fail "control copy must pass, got rc=$rc"

echo "BATTERY COMPLETE: 7/7 tamper cases captured at pre-registered gates + control PASS" >> "$BATT"
echo "BATTERY COMPLETE: 7/7 captured + control PASS"
