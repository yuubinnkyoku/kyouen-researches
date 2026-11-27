#!/bin/bash
# Part EV tamper battery. Order per protocol: pin-assert -> backup -> tamper
# -> pre-assert -> audit(expect rc1 + named gate) -> restore -> restore-assert.
set -u
cd "$(dirname "$0")"
LOG=tamper.log
log(){ echo "$(date -u +%FT%TZ) $*" >> $LOG; }
say(){ echo "$*"; log "$*"; }

run_audit(){ python3 scripts/audit_gate.py > /dev/null 2>&1; }

# ---- T1: audit ROWS pin (expected nodes) tampered 3549602 -> 3549603
say "T1-START break audit ROWS pin b018 nodes 3549602->3549603"
A=scripts/audit_gate.py
pin1=$(sha256sum $A | cut -d' ' -f1); say "T1 pin-assert audit_gate.py sha256=$pin1"
cp $A /tmp/ev_t1.audit.bak
sed -i 's/60,15000000,1,3549602/60,15000000,1,3549603/' $A
pre1=$(sha256sum $A | cut -d' ' -f1)
say "T1 pre-assert tampered sha256=$pre1 (differs: $([ "$pin1" != "$pre1" ] && echo yes || echo NO))"
run_audit; rc=$?
say "T1 audit rc=$rc (expected 1)"
grep -o '"G3"[^}]*"status": "FAIL"' output/audit_gate.json | head -1 > /dev/null
python3 - <<'PY'
import json
d=json.load(open('output/audit_gate.json'))
g3=d['gates']['G3']; print("T1 G3 status:",g3.get('status'),"| fail keys:",g3.get('fail') or g3.get('rows_failed') or 'see json')
out={'t1':{'g3':g3}}
json.dump(out,open('t1_result.json','w'))
PY
cp /tmp/ev_t1.audit.bak $A
rest1=$(sha256sum $A | cut -d' ' -f1)
say "T1 restore-assert sha256=$rest1 (byte-identical: $([ "$rest1" == "$pin1" ] && echo yes || echo NO))"

# ---- T2: raw d002.p1.out nodes 5359994 -> 5359995
say "T2-START break raw d002.p1 nodes 5359994->5359995"
R=output/raw/d002.p1.out
pin2=$(sha256sum $R | cut -d' ' -f1); say "T2 pin-assert d002.p1.out sha256=$pin2"
cp $R /tmp/ev_t2.raw.bak
sed -i 's/,15000000,1,5359994/,15000000,1,5359995/' $R
pre2=$(sha256sum $R | cut -d' ' -f1)
say "T2 pre-assert tampered sha256=$pre2 (differs: $([ "$pin2" != "$pre2" ] && echo yes || echo NO))"
run_audit; rc=$?
say "T2 audit rc=$rc (expected 1)"
python3 - <<'PY'
import json
d=json.load(open('output/audit_gate.json'))
g2=d['gates']['G2']; g3=d['gates']['G3']
print("T2 G2 status:",g2.get('status'),"G3 status:",g3.get('status'))
PY
cp /tmp/ev_t2.raw.bak $R
rest2=$(sha256sum $R | cut -d' ' -f1)
say "T2 restore-assert sha256=$rest2 (byte-identical: $([ "$rest2" == "$pin2" ] && echo yes || echo NO))"

# ---- T3: phantom GATE-PASS line in gate-status.log
say "T3-START append phantom GATE-PASS line to gate-status.log"
S=output/gate-status.log
pin3=$(sha256sum $S | cut -d' ' -f1); say "T3 pin-assert gate-status.log sha256=$pin3"
cp $S /tmp/ev_t3.status.bak
echo "2026-11-26T00:00:00Z PHANTOM-KEY GATE-PASS 60,15000000,1,3549602 (fabricated)" >> $S
pre3=$(sha256sum $S | cut -d' ' -f1)
say "T3 pre-assert tampered sha256=$pre3 (differs: $([ "$pin3" != "$pre3" ] && echo yes || echo NO))"
run_audit; rc=$?
say "T3 audit rc=$rc (expected 1)"
python3 - <<'PY'
import json
d=json.load(open('output/audit_gate.json'))
g4=d['gates']['G4']; print("T3 G4:",g4)
PY
cp /tmp/ev_t3.status.bak $S
rest3=$(sha256sum $S | cut -d' ' -f1)
say "T3 restore-assert sha256=$rest3 (byte-identical: $([ "$rest3" == "$pin3" ] && echo yes || echo NO))"

# ---- clean control
run_audit; rc=$?
say "CLEAN-CONTROL audit rc=$rc (expected 0)"
say "BATTERY-END"
