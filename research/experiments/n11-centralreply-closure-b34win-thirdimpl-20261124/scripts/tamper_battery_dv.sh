#!/bin/bash
# tamper_battery_dv.sh <kit-root> <workdir> -- pre-registered corruption battery
# for the Part DU-b fail-closed audit (audit_dv.py). Each variant is applied to
# a FROZEN COPY of the kit (the battery never mutates the given kit-root);
# the audit must exit rc=1 at exactly the pre-registered gate. CONTROL runs the
# untouched copy and must rc=0. Pre-registered variants (declaration note):
#   T1  replica ag001.p1 nodes +1                -> replica-ag001-det-pair
#   T2  third target ag002.b expansions +1       -> target-ag002-det-pair
#   T3  third target ag001 a+b result 1->2       -> target-ag001-verdict-agree
#   T4  replica ag001.p2 replay_done removed     -> replica-ag001-done
#   T5  sources raw ag002.p2 nodes +1            -> published-ag002-det-pair
#   T6  canonical cache fake WIN adoption append -> unadopted-pin-canonical-cache
#       (the cache byte-pin gate fires first; rowcount would also fail)
#   T7  anchor l1a.a expansions +10000           -> anchor-l1a-a-expansions
#   T8  negative ng1 declared 88->89             -> neg-ng1-failclosed
#   T9  rules-gate.txt mismatches 0->3           -> rules-gate-tbl-mismatch0
#   T10 val-gate host at2m-...946 nodes +1       -> valgate-at2m-s5-1152921504606851072-536870946-node-exact
#   CONTROL (no mutation)                       -> rc=0
# Any rc/gate deviation from this table is a battery FAILURE (exit 1).
set -u
KIT="$1"; WORK="$2"
[ -d "$KIT" ] || { echo "battery: kit-root missing: $KIT"; exit 2; }
mkdir -p "$WORK"
rm -rf "$WORK"/t* "$WORK"/control
printf 'T1 replica-ag001-det-pair\nT2 target-ag002-det-pair\nT3 target-ag001-verdict-agree\nT4 replica-ag001-done\nT5 published-ag002-det-pair\nT6 unadopted-pin-canonical-cache\nT7 anchor-l1a-a-expansions\nT8 neg-ng1-failclosed\nT9 rules-gate-tbl-mismatch0\nT10 valgate-at2m-s5-1152921504606851072-536870946-node-exact\n' > "$WORK/expected-gates.txt"

frozen() { # $1=case name; echoes the copy root
  local c="$1"
  [ -d "$WORK/$c" ] || cp -r "$KIT" "$WORK/$c"
  echo "$WORK/$c"
}

run_case() { # $1=case name, $2=expected gate ("-" for control rc=0)
  local c="$1" want="$2" root rc got
  root=$(frozen "$c")
  ( cd "$root" && python3 scripts/audit_dv.py > "$WORK/$c.audit-stdout.txt" 2>&1 )
  rc=$?
  got=$(grep -oE "GATE FAILED: [A-Za-z0-9_.-]+" "$WORK/$c.audit-stdout.txt" | head -1 | cut -d" " -f3)
  if [ "$want" = "-" ]; then
    if [ "$rc" -eq 0 ] && grep -q "ALL .* GATES PASS" "$WORK/$c.audit-stdout.txt"; then
      echo "TAMPER $c: CONTROL rc=0 ALL-PASS (as pre-registered)"
    else
      echo "TAMPER $c: CONTROL-UNEXPECTED rc=$rc"; return 1
    fi
  else
    if [ "$rc" -eq 1 ] && [ "$got" = "$want" ]; then
      echo "TAMPER $c: rc=1 gate=$got (as pre-registered)"
    else
      echo "TAMPER $c: UNEXPECTED rc=$rc got=${got:-none} want=$want"; return 1
    fi
  fi
}

fail=0
# T1
root=$(frozen t1); sed -i 's/replay,0,5,85,0,15000000,1,9149084/replay,0,5,85,0,15000000,1,9149085/' "$root/output/raw/ag001.p1.out" || fail=1
run_case t1 replica-ag001-det-pair || fail=1
# T2 (generic: increment the b-line expansions field by 1, whatever its value;
#     first run used a synthetic-kit placeholder constant 7777000 and detected
#     no drift on the real kit -> buggy record preserved in
#     output/tamper-battery-t2-buggy-record.txt, corrected to a generic
#     mutation, disclosed in the B-commit message)
root=$(frozen t2)
python3 -c "import sys; p=sys.argv[1]; l=open(p).read().rstrip('\n').split(','); assert l[5]=='1' and l[11]=='clean', 'unexpected shape'; l[6]=str(int(l[6])+1); open(p,'w').write(','.join(l)+'\n')" "$root/output/targets/ag002.b.out" || fail=1
run_case t2 target-ag002-det-pair || fail=1
# T3
root=$(frozen t3); sed -i 's/third,ag001a,5,85,85,1,/third,ag001a,5,85,85,2,/;s/third,ag001b,5,85,85,1,/third,ag001b,5,85,85,2,/' "$root/output/targets/ag001.a.out" "$root/output/targets/ag001.b.out" || fail=1
run_case t3 target-ag001-verdict-agree || fail=1
# T4
root=$(frozen t4); sed -i '/^# replay_done rows=1/d' "$root/output/raw/ag001.p2.out" || fail=1
run_case t4 replica-ag001-done || fail=1
# T5
root=$(frozen t5); sed -i 's/replay,0,5,88,0,15000000,1,4893014/replay,0,5,88,0,15000000,1,4893015/' "$root/sources/raw/ag002.p2.out" || fail=1
run_case t5 published-ag002-det-pair || fail=1
# T6
root=$(frozen t6); printf 's5verdict,1152921505747697664,1032,5,1,9149084\n' >> "$root/sources/canonical-cache-973bcd19.cache" || fail=1
run_case t6 unadopted-pin-canonical-cache || fail=1
# T7
root=$(frozen t7); sed -i 's/,7660602,/,7661602,/' "$root/output/anchors/l1a.a.out" || fail=1
run_case t7 anchor-l1a-a-expansions || fail=1
# T8
root=$(frozen t8); sed -i 's/declared=88/declared=89/' "$root/output/negative/ng1.a.out" || fail=1
run_case t8 neg-ng1-failclosed || fail=1
# T9
root=$(frozen t9); sed -i 's/mismatches 0/mismatches 3/' "$root/output/rules-gate.txt" || fail=1
run_case t9 rules-gate-tbl-mismatch0 || fail=1
# T10
root=$(frozen t10); sed -i 's/2000000,0,2000000/2000000,0,2000001/' "$root/val-gate/at2m-s5-1152921504606851072-536870946.dv-host.out" || fail=1
run_case t10 valgate-at2m-s5-1152921504606851072-536870946-node-exact || fail=1
# CONTROL
run_case control - || fail=1

if [ "$fail" -eq 0 ]; then
  echo "TAMPER-BATTERY 10/10 pre-registered gates + control rc=0: PASS"
  exit 0
fi
echo "TAMPER-BATTERY: FAIL"
exit 1
