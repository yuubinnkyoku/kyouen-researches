#!/bin/bash
set -u
cd "$(dirname "$0")"
LOG=tamper.log
say(){ echo "$*"; echo "$(date -u +%FT%TZ) $*" >> $LOG; }
run_audit(){ python3 scripts/audit_gate.py > /dev/null 2>&1; }

# ---- T1 re-check: capture FAIL gate names
say "T1-RECHECK-START (capture fail gate names; same tamper, same order)"
A=scripts/audit_gate.py
pin1=$(sha256sum $A | cut -d' ' -f1)
[ "$pin1" == "cfbba26494c2f7eaf0802ce5bb35439a1e6a9a254b7098ac24ec49960778d1cb" ] && say "T1 pin-assert restored sha256=$pin1 OK" || { say "T1 pin-assert MISMATCH $pin1"; exit 2; }
cp $A /tmp/ev_t1b.audit.bak
sed -i 's/60,15000000,1,3549602/60,15000000,1,3549603/' $A
say "T1 pre-assert tampered sha256=$(sha256sum $A | cut -d' ' -f1) (differs: $([ "$(sha256sum $A|cut -d' ' -f1)" != "$pin1" ] && echo yes || echo NO))"
run_audit; rc=$?
say "T1 recheck audit rc=$rc (expected 1)"
python3 - <<'PY' >> $LOG
import json
d=json.load(open('output/audit_gate.json'))
fails=[k for k,v in d['gates'].items() if v.get('status')=='FAIL']
print('T1-RECHECK FAIL gates:', fails)
for k in fails: print('  ',k,'detail:',d['gates'][k].get('detail'))
json.dump({'fail_gates':fails},open('t1_result.json','w'))
PY
cp /tmp/ev_t1b.audit.bak $A
rest1=$(sha256sum $A | cut -d' ' -f1)
say "T1 restore-assert sha256=$rest1 (byte-identical: $([ "$rest1" == "$pin1" ] && echo yes || echo NO))"

# ---- T2 re-check
say "T2-RECHECK-START (capture fail gate names; same tamper, same order)"
R=output/raw/d002.p1.out
pin2=$(sha256sum $R | cut -d' ' -f1)
[ "$pin2" == "32d2378d1b42c26d32af504a068b83e5e24954fafbc6071fff16b71d7d3a95c7" ] && say "T2 pin-assert restored sha256=$pin2 OK" || { say "T2 pin-assert MISMATCH $pin2"; exit 2; }
cp $R /tmp/ev_t2b.raw.bak
sed -i 's/,15000000,1,5359994/,15000000,1,5359995/' $R
say "T2 pre-assert tampered sha256=$(sha256sum $R | cut -d' ' -f1) (differs: $([ "$(sha256sum $R|cut -d' ' -f1)" != "$pin2" ] && echo yes || echo NO))"
run_audit; rc=$?
say "T2 recheck audit rc=$rc (expected 1)"
python3 - <<'PY' >> $LOG
import json
d=json.load(open('output/audit_gate.json'))
fails=[k for k,v in d['gates'].items() if v.get('status')=='FAIL']
print('T2-RECHECK FAIL gates:', fails)
for k in fails: print('  ',k,'detail:',d['gates'][k].get('detail'))
json.dump({'fail_gates':fails},open('t2_result.json','w'))
PY
cp /tmp/ev_t2b.raw.bak $R
rest2=$(sha256sum $R | cut -d' ' -f1)
say "T2 restore-assert sha256=$rest2 (byte-identical: $([ "$rest2" == "$pin2" ] && echo yes || echo NO))"

run_audit; say "CLEAN-CONTROL-2 audit rc=$?"
say "BATTERY-RECHECK-END"
