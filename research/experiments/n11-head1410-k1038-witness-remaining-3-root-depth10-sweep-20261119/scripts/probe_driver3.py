#!/usr/bin/env python3
"""Depth-10 probe driver for the 3 untested K1038 refold witness roots (K1039 follow-up).

K1039 judged 23 of K1038's 26 untested witness roots; these 3 remain untested in
K1038's witness_sweep_plan. Same protocol as K1039: both AND-close orderings,
cap 30M uniform, pilot_d6 control before each probe, resumable per (root, mode).
Roots are the K1038 published D4-canonical 7-stone hex (stones 7, unsafe 0 per
K1038 root_checks).
"""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.abspath(__file__))
ROOTS = [
    '00000000000000403800000008100020',
    '00000000020000801202000100100000',
    '00000000000000889002000080100000',
]
VERDICTS = os.path.join(BASE, 'verdicts3')
RUNNER = os.path.join(BASE, 'scripts', 'class4_child1_runner_v17.ts')
os.makedirs(VERDICTS, exist_ok=True)

def maxbit(h):
    m = int(h, 16); b = -1
    while m:
        b += 1; m >>= 1
    return b

def main():
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 200.0
    for rh in ROOTS:
        assert len(rh) == 32 and bin(int(rh, 16)).count('1') == 7, rh
    todo = []
    for rh in ROOTS:
        for mode in (1, 0):
            out = os.path.join(VERDICTS, f'{rh}.andclose{mode}.json')
            if os.path.exists(out):
                try:
                    d = json.load(open(out))
                    if len(d) == 2 and d[0].get('control') == 'pilot_d6':
                        continue
                except Exception:
                    pass
            todo.append((rh, mode, out))
    todo.sort(key=lambda t: (t[1], ROOTS.index(t[0])))
    print(f'{len(ROOTS)} roots, {len(todo)} probes remaining', flush=True)
    if not todo:
        print('NOTHING_TO_DO'); return
    t_start = time.time()
    def run(t):
        rh, mode, out = t
        b = maxbit(rh); child = f'{(int(rh,16) ^ (1<<b)):032x}'
        jsonl = out + '.raw'
        cmd = ['node', '--experimental-strip-types', RUNNER, '--child', child,
               '--bits', str(b), '--depth', '10', '--cap', '30000000',
               '--andclose', str(mode), '--out', jsonl]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        lines = [l for l in p.stdout.strip().splitlines() if l.strip()]
        if p.returncode != 0 or len(lines) != 2:
            return (rh, mode, 'FAIL', p.returncode, p.stderr[-400:], lines)
        d = [json.loads(l) for l in lines]
        if d[0].get('control') != 'pilot_d6' or d[0]['loss'] is not False or d[0]['nodes'] != 3402:
            return (rh, mode, 'PILOT_FAIL', None, '', lines)
        with open(out, 'w') as f:
            json.dump(d, f, separators=(',', ':'))
        return (rh, mode, 'OK', d[1]['loss'], d[1]['nodes'], d[1]['capped'])
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = []
        for t in todo:
            if time.time() - t_start > budget:
                print('BUDGET_STOP', flush=True); break
            futs.append(ex.submit(run, t))
        for fut in futs:
            r = fut.result()
            print(json.dumps({'root': r[0], 'andclose': r[1], 'status': r[2],
                              'loss': r[3] if len(r) > 3 else None,
                              'nodes': r[4] if len(r) > 4 else None,
                              'capped': r[5] if len(r) > 5 else None}), flush=True)

if __name__ == '__main__':
    main()
