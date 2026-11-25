#!/usr/bin/env python3
"""compare_verify.py MYROOT PUBROOT: byte-level field comparison of second-environment
fresh re-runs (MYROOT/output/raw) vs published batch-38 evidence (PUBROOT/output/raw).
Comparison unit: the 'replay,' line, all fields EXCEPT wall_s (field 9, operational info,
excluded from determinism comparison per published precedent) + '# forbidden quadruples'
header + '# replay_done' terminal marker. rc=0 iff every published regular .out for a key
present in MYROOT matches (missing keys are reported as MY-RUN-MISSING and counted bad)."""
import re, os, sys
MY, PUB = sys.argv[1], sys.argv[2]
def line_of(p):
    t = open(p, 'rb').read().decode()
    m = re.search(r'^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)$', t, re.M)
    fq = re.search(r'# forbidden quadruples: (\d+)', t)
    done = '# replay_done rows=' in t
    return (m.groups() if m else None, fq.group(1) if fq else None, done)
bad = 0; rows = []; n = 0
for k in sorted(os.listdir(PUB)):
    if '.truncated.' in k or not k.endswith('.out'):
        continue
    n += 1
    kid, p = k.rsplit('.', 2)[0], k.rsplit('.', 2)[1]
    my, pub = f'{MY}/{kid}.{p}.out', f'{PUB}/{k}'
    if not os.path.exists(my):
        rows.append((kid, p, 'MY-RUN-MISSING', '', '')); bad += 1; continue
    (mf, mfw, md) = line_of(my); (pf, pfw, pd) = line_of(pub)
    if mf is None or pf is None or not md or not pd:
        rows.append((kid, p, 'STRUCT-DIFF', '', '')); bad += 1; continue
    same = (mf[:7] == pf[:7]) and (mf[8:] == pf[8:]) and mfw == pfw  # wall_s = index 7 excluded
    rows.append((kid, p, 'OK' if same else 'FIELDDIFF', ','.join(mf[4:7]), ','.join(pf[4:7])))
    if not same:
        bad += 1
        rows[-1] = (kid, p, 'FIELDDIFF', 'mine=' + ','.join(mf), 'pub=' + ','.join(pf))
print(f"{'key':7} {'pass':4} {'verdict':13} {'mine(bud,res,nodes)':30} published")
for r in rows:
    print(f"{r[0]:7} {r[1]:4} {r[2]:13} {r[3]:30} {r[4]}")
print(f"TOTAL pairs={len(rows)} bad={bad}")
sys.exit(1 if bad else 0)
