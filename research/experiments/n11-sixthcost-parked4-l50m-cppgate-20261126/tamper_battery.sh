#!/bin/bash
# Part SM (parked4 L50M WIN rows) tamper battery. Order per protocol: pin-assert -> backup -> tamper
# -> pre-assert -> audit(expect rc1 + named gate) -> restore -> restore-assert.
set -u
cd "$(dirname "$0")"
LOG=tamper.log
log(){ echo "$(date -u +%FT%TZ) $*" >> $LOG; }
say(){ echo "$*"; log "$*"; }

run_audit(){ python3 scripts/audit_gate.py > /dev/null 2>&1; }

# ---- T1: audit ROWS pin (expected nodes) tampered 16402480 -> 16402481
say "T1-START break audit ROWS pin k13 nodes 16402480->16402481"
A=scripts/audit_gate.py
pin1=$(sha256sum $A | cut -d' ' -f1); say "T1 pin-assert audit_gate.py sha256=$pin1"
cp $A /tmp/sm_t1.audit.bak
sed -i 's/95,50000000,1,16402480/95,50000000,1,16402481/' $A
pre1=$(sha256sum $A | cut -d' ' -f1)
say "T1 pre-assert tampered sha256=$pre1 (differs: $([ "$pin1" != "$pre1" ] && echo yes || echo NO))"
run_audit; rc=$?
say "T1 audit rc=$rc (expected 1)"
grep -o '"G3:k13": {"status": "FAIL"' output/audit_gate.json | head -1 > /dev/null
python3 - <<'PY'
import json
d=json.load(open('output/audit_gate.json'))
g3=d['gates']['G3:k13']; print("T1 G3:k13 status:",g3.get('status'),"| detail:",g3.get('detail'))
out={'t1':{'g3_k13':g3}}
json.dump(out,open('t1_result.json','w'))
PY
cp /tmp/sm_t1.audit.bak $A
rest1=$(sha256sum $A | cut -d' ' -f1)
say "T1 restore-assert sha256=$rest1 (byte-identical: $([ "$rest1" == "$pin1" ] && echo yes || echo NO))"

# ---- T2: raw k13.p1.out nodes 16402480 -> 16402481
say "T2-START break raw k13.p1 nodes 16402480->16402481"
R=output/raw/k13.p1.out
pin2=$(sha256sum $R | cut -d' ' -f1); say "T2 pin-assert k13.p1.out sha256=$pin2"
cp $R /tmp/sm_t2.raw.bak
sed -i 's/,50000000,1,16402480/,50000000,1,16402481/' $R
pre2=$(sha256sum $R | cut -d' ' -f1)
say "T2 pre-assert tampered sha256=$pre2 (differs: $([ "$pin2" != "$pre2" ] && echo yes || echo NO))"
run_audit; rc=$?
say "T2 audit rc=$rc (expected 1)"
python3 - <<'PY'
import json
d=json.load(open('output/audit_gate.json'))
g2=d['gates']['G2:k13']; g3=d['gates']['G3:k13']
print("T2 G2:k13 status:",g2.get('status'),"G3 status:",g3.get('status'))
PY
cp /tmp/sm_t2.raw.bak $R
rest2=$(sha256sum $R | cut -d' ' -f1)
say "T2 restore-assert sha256=$rest2 (byte-identical: $([ "$rest2" == "$pin2" ] && echo yes || echo NO))"

# ---- T3: phantom GATE-PASS line in gate-status.log
say "T3-START append phantom GATE-PASS line to gate-status.log"
S=output/gate-status.log
pin3=$(sha256sum $S | cut -d' ' -f1); say "T3 pin-assert gate-status.log sha256=$pin3"
cp $S /tmp/sm_t3.status.bak
echo "2026-11-26T00:00:00Z PHANTOM-KEY GATE-PASS 95,50000000,1,16402480 (fabricated)" >> $S
pre3=$(sha256sum $S | cut -d' ' -f1)
say "T3 pre-assert tampered sha256=$pre3 (differs: $([ "$pin3" != "$pre3" ] && echo yes || echo NO))"
run_audit; rc=$?
say "T3 audit rc=$rc (expected 1)"
python3 - <<'PY'
import json
d=json.load(open('output/audit_gate.json'))
g4=d['gates']['G4']; print("T3 G4:",g4)
PY
cp /tmp/sm_t3.status.bak $S
rest3=$(sha256sum $S | cut -d' ' -f1)
say "T3 restore-assert sha256=$rest3 (byte-identical: $([ "$rest3" == "$pin3" ] && echo yes || echo NO))"

# ---- clean control
run_audit; rc=$?
say "CLEAN-CONTROL audit rc=$rc (expected 0)"
say "BATTERY-END"
