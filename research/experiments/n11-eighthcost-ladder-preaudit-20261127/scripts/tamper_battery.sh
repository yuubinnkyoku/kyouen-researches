#!/bin/bash
# Eighth-cost ladder pre-audit tamper battery (4 modes) - runs on a SCRATCH COPY
# of the kit, never on the published bytes. Every mode must make the audit FAIL
# (rc=1) on the expected gates; the clean control must return rc=0 with the
# clean output byte-identical to the official run.
set -u
AUDIT="${1:?usage: tamper_battery.sh <audit.py> <clean-kit-dir> <head-cache> <scratch-dir> <official-output>}"
CLEAN="${2:?}"
HEADC="${3:?}"
SCRATCH="${4:?}"
OFFICIAL="${5:?}"
rm -rf "$SCRATCH"
mkdir -p "$SCRATCH"
cp -r "$CLEAN" "$SCRATCH/kit"
cp "$AUDIT" "$SCRATCH/audit_eighth_ladder.py"
cd "$SCRATCH" || exit 2
{
python3 - <<'EOF'
import hashlib, pathlib, subprocess, sys
def run():
    return subprocess.run(['python3', 'audit_eighth_ladder.py', 'kit', 'kit/head.cache', 'tamper_out.json'], capture_output=True, text=True)
def fails(r):
    return [l.split()[1] for l in r.stdout.splitlines() if l.startswith('FAIL')]
res = {}
r0 = run()
if r0.returncode != 0:
    print('CLEAN-PRE FAIL', fails(r0)); sys.exit(1)
clean_out = pathlib.Path('tamper_out.json').read_bytes()

# T1: raw at15m-run1 k01 nodes edit (kit byte tamper)
p = pathlib.Path('kit/output/raw/at15m-run1/k01.out.csv'); o = p.read_text()
p.write_text(o.replace(',1,8514427,', ',1,8514426,'))
r = run(); res['T1'] = (r.returncode, fails(r))
p.write_text(o)

# T2: phantom k02 15M raw added to the tree ONLY (manifest untouched)
d = pathlib.Path('kit/output/raw/at15m-run1'); d.mkdir(exist_ok=True)
src = pathlib.Path('kit/output/raw/at2m-run1/k02.out.csv').read_text()
phantom = src.replace(',0,2000000,', ',0,15000000,')
(d / 'k02.out.csv').write_text(phantom)
r = run(); res['T2'] = (r.returncode, fails(r))
(d / 'k02.out.csv').unlink()

# T3: phantom k02 15M raw added to the tree AND the manifest (full forgery)
(d / 'k02.out.csv').write_text(phantom)
m = pathlib.Path('kit/MANIFEST-raw-sha256.txt'); mo = m.read_text()
sha = hashlib.sha256(phantom.encode()).hexdigest()
m.write_text(mo + "%s %d output/raw/at15m-run1/k02.out.csv\n" % (sha, len(phantom)))
r = run(); res['T3'] = (r.returncode, fails(r))
(d / 'k02.out.csv').unlink(); m.write_text(mo)

# T4: batch-summary ledger byte flip
b = pathlib.Path('kit/output/batch-summary.json'); bo = b.read_text()
b.write_text(bo.replace('"resolved_exact_win": 1', '"resolved_exact_win": 2'))
r = run(); res['T4'] = (r.returncode, fails(r))
b.write_text(bo)

r = run(); res['CLEAN-POST'] = (r.returncode, pathlib.Path('tamper_out.json').read_bytes() == clean_out)
ok = (res['T1'][0] == 1 and any('P1:manifest-sha-all' in f or 'P3:k01:at15m-pair-identity' in f or 'P2:k01:at15m-win' in f for f in res['T1'][1])
      and res['T2'][0] == 1 and any('P1:raw-tree==manifest' in f for f in res['T2'][1])
      and res['T3'][0] == 1 and any('P1:manifest-at15m-only-k01' in f or 'P5:no-post-win-15m-starts' in f for f in res['T3'][1])
      and res['T4'][0] == 1 and any('P0:batch-summary-sha' in f for f in res['T4'][1])
      and res['CLEAN-POST'][0] == 0 and res['CLEAN-POST'][1])
for k, v in res.items(): print(k, v[0], v[1] if isinstance(v[1], list) else v[1])
print('BATTERY', 'FAIL-CLOSED-ALL-4 + CLEAN' if ok else 'INCOMPLETE')
sys.exit(0 if ok else 1)
EOF
} | tee tamper-battery-stdout.log
rc=${PIPESTATUS[0]}
echo "battery rc=$rc"
exit "$rc"
