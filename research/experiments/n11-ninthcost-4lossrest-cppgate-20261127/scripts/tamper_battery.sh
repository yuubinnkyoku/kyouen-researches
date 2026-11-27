#!/bin/bash
# Ninth-cost k08-k11 LOSS row tamper battery (4 modes: expected pin flip
# on the first target, raw nodes edit on the first target, phantom
# GATE-PASS, head byte append) - runs on a SCRATCH COPY of the kit,
# never on the published bytes. Every mode must make the audit FAIL
# (rc=1); each restore must be byte-identical; the clean control must
# return rc=0. N9_HEAD must point at the canonical head cache (G6).
# Disclosed adaptation of the k12 single-row battery (same session
# lineage), pins renamed to the k08 row of the k08-k11 batch.
set -u
SCRATCH="${1:?usage: tamper_battery.sh <scratch-kit-dir> <clean-kit-dir> <head-cache>}"
CLEAN="${2:?}"
HEADC="${3:?}"
rm -rf "$SCRATCH"
cp -r "$CLEAN" "$SCRATCH"
cd "$SCRATCH" || exit 2
{
N9_HEAD="$HEADC" python3 - <<'PYEOF'
import subprocess, pathlib, sys
def run(): return subprocess.run(['python3','scripts/audit_gate.py'],capture_output=True,text=True)
r0=run()
if r0.returncode!=0: print('CLEAN-PRE FAIL'); sys.exit(1)
res={}
def fails(r): return [l.split(' (')[0] for l in r.stdout.splitlines() if l.startswith('FAIL')]
# T1: audit expected pin flip (k08 nodes)
src=pathlib.Path('scripts/audit_gate.py'); orig=src.read_text()
t1=orig.replace('"k08": "98,15000000,2,3306768"','"k08": "98,15000000,2,3306769"')
assert t1!=orig
src.write_text(t1); r=run(); res['T1']=(r.returncode,fails(r))
src.write_text(orig)
# T2: raw k08.p1 edit (nodes)
p=pathlib.Path('output/raw/k08.p1.out'); o=p.read_text()
t2=o.replace(',15000000,2,3306768,',',15000000,2,3306767,')
assert t2!=o
p.write_text(t2); r=run(); res['T2']=(r.returncode,fails(r))
p.write_text(o)
# T3: phantom GATE-PASS line
s=pathlib.Path('output/gate-status.log'); so=s.read_text()
s.write_text(so+'2026-11-27T00:00:00Z k99 GATE-PASS 1,1,1,1 (phantom)\n')
r=run(); res['T3']=(r.returncode,fails(r))
s.write_text(so)
# T4: head byte append (freshness gate)
env=dict(__import__('os').environ)
head=pathlib.Path(env['N9_HEAD']); ho=head.read_bytes()
head.write_bytes(ho+b'# tamper\n')
r=run(); res['T4']=(r.returncode,fails(r))
head.write_bytes(ho)
r=run(); res['CLEAN-POST']=(r.returncode,[r.stdout.splitlines()[0] if r.stdout else ''])
ok = (res['T1'][0]==1 and any('G0:target-expected:k08' in f or 'G3:k08' in f for f in res['T1'][1])
      and res['T2'][0]==1 and any('G2:k08' in f for f in res['T2'][1]) and any('G3:k08' in f for f in res['T2'][1])
      and res['T3'][0]==1 and any('G4' in f for f in res['T3'][1])
      and res['T4'][0]==1 and any('G6' in f for f in res['T4'][1])
      and res['CLEAN-POST'][0]==0)
for k,v in res.items(): print(k, v[0], v[1])
print('BATTERY', 'FAIL-CLOSED-ALL-4 + CLEAN' if ok else 'INCOMPLETE')
sys.exit(0 if ok else 1)
PYEOF
} | tee tamper-battery-stdout.log
rc=${PIPESTATUS[0]}
echo "battery rc=$rc"
exit "$rc"
