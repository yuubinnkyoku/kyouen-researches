#!/bin/bash
# Eighth-cost k01 WIN row tamper battery (k01 quadruple, 3 modes) - runs on a
# SCRATCH COPY of the kit, never on the published bytes. Every mode must make
# the audit FAIL (rc=1); the restore must be byte-identical; the clean control
# must return rc=0. K01_HEAD must point at the canonical head cache (G6).
set -u
SCRATCH="${1:?usage: tamper_battery.sh <scratch-kit-dir> <clean-kit-dir> <head-cache>}"
CLEAN="${2:?}"
HEADC="${3:?}"
rm -rf "$SCRATCH"
cp -r "$CLEAN" "$SCRATCH"
cd "$SCRATCH" || exit 2
{
K01_HEAD="$HEADC" python3 - <<'EOF'
import subprocess, pathlib, sys
def run(): return subprocess.run(['python3','scripts/audit_gate.py'],capture_output=True,text=True)
r0=run()
if r0.returncode!=0: print('CLEAN-PRE FAIL'); sys.exit(1)
res={}
# T1: audit expected pin flip (k01 nodes)
src=pathlib.Path('scripts/audit_gate.py'); orig=src.read_text()
t1=orig.replace('84,15000000,1,8514427','84,15000000,1,8514428')
src.write_text(t1); r=run()
res['T1']=(r.returncode,[l.split(' (')[0] for l in r.stdout.splitlines() if l.startswith('FAIL')])
src.write_text(orig)
# T2: raw k01.p1 edit (nodes)
p=pathlib.Path('output/raw/k01.p1.out'); o=p.read_text()
p.write_text(o.replace(',1,8514427,',',1,8514426,'))
r=run(); res['T2']=(r.returncode,[l.split(' (')[0] for l in r.stdout.splitlines() if l.startswith('FAIL')])
p.write_text(o)
# T3: phantom GATE-PASS line
s=pathlib.Path('output/gate-status.log'); so=s.read_text()
s.write_text(so+'2026-11-27T00:00:00Z k99 GATE-PASS 1,1,1,1 (phantom)\n')
r=run(); res['T3']=(r.returncode,[l.split(' (')[0] for l in r.stdout.splitlines() if l.startswith('FAIL')])
s.write_text(so)
r=run(); res['CLEAN-POST']=(r.returncode,[r.stdout.splitlines()[0] if r.stdout else ''])
ok = (res['T1'][0]==1 and any('G3:k01' in f for f in res['T1'][1])
      and res['T2'][0]==1 and any('G2:k01' in f for f in res['T2'][1]) and any('G3:k01' in f for f in res['T2'][1])
      and res['T3'][0]==1 and any('G4' in f for f in res['T3'][1])
      and res['CLEAN-POST'][0]==0)
for k,v in res.items(): print(k, v[0], v[1])
print('BATTERY', 'FAIL-CLOSED-ALL-3 + CLEAN' if ok else 'INCOMPLETE')
sys.exit(0 if ok else 1)
EOF
} | tee tamper-battery-stdout.log
rc=${PIPESTATUS[0]}
echo "battery rc=$rc"
exit "$rc"
