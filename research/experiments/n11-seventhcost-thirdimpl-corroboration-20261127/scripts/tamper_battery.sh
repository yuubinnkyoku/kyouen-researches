#!/usr/bin/env bash
# Part SY tamper battery: scratch copy only, never the published bytes.
set -u
SRC=kit
SCR=scratch-tamper
rm -rf "$SCR"; cp -r "$SRC" "$SCR"
cd "$SCR"
fail() { echo "TAMPER-$1 expected FAIL, got PASS"; exit 1; }
# T1: flip k05 expected_result pin 1 -> 2
python3 - <<'PY'
import json,pathlib
p=pathlib.Path('input/gate-rows.json'); d=json.loads(p.read_text())
d['targets']['k05']['expected_result']='2'
p.write_text(json.dumps(d,indent=1))
PY
python3 scripts/audit_sy.py . > /dev/null 2>&1 && fail T1
echo "T1 FAIL as expected (k05 expected pin flip -> G3)"
cd ..; rm -rf "$SCR"; cp -r "$SRC" "$SCR"; cd "$SCR"
# T2: edit k10.p2 expansions -> cold pair mismatch
python3 - <<'PY'
import pathlib
p=pathlib.Path('output/raw/k10.p2.txt')
t=p.read_text().replace(',15223326,',',15223327,',1)
p.write_text(t)
PY
python3 scripts/audit_sy.py . > /dev/null 2>&1 && fail T2
echo "T2 FAIL as expected (raw expansion edit -> G4)"
cd ..; rm -rf "$SCR"; cp -r "$SRC" "$SCR"; cd "$SCR"
# T3: phantom raw -> count gate
cp output/raw/k42.p1.txt output/raw/k99.p1.txt
python3 scripts/audit_sy.py . > /dev/null 2>&1 && fail T3
echo "T3 FAIL as expected (phantom raw -> G5)"
cd ..; rm -rf "$SCR"
# clean control
python3 "$SRC/scripts/audit_sy.py" "$SRC" > /dev/null 2>&1 && echo "clean control rc=0" || echo "CLEAN CONTROL FAIL"
