#!/usr/bin/env python3
"""Depth-10 probe driver for the 28-root refuted-excluded cover witness (epoch-2 rebuild).

For each 7-stone root in the witness list (selected in K1033's cover resolve, certificate
receipts K1035/K1036 for three of them):
  bit   = max stone bit of the root
  child = root ^ (1 << bit)   (6-stone, canonical orientation)
Run runner v17: --child child --bits bit --depth 10 --cap 30000000 --andclose {1,0}
Verdict lines: [pilot control (loss=false, nodes=3402), probe result].
Saves verdicts/<root>.andclose<mode>.json (both lines) - resumable.
Node counts are deterministic; verdict = loss across both orders.
"""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.abspath(__file__))
ROOTS = [
    '00000000000000003800000008001021',
    '0000000000000000380000000b080000',
    '00000000000000003800280009000000',
    '00000000000000083800000048100000',
    '00000000000000801202000000840200',
    '00000000000000801202000000880400',
    '00000000000000801202000001040100',
    '00000000000000801202000011000400',
    '00000000000000801202000020101000',
    '00000000000000801202010001080000',
    '00000000000000801202040000900000',
    '00000000000000801202050000001000',
    '00000000000000801202060001000000',
    '000000000000008012020a0000001000',
    '00000000000000801212000001001000',
    '00000000000000801222000000801000',
    '00000000000000805202080001000000',
    '00000000000000909002000080100000',
    '00000000000020a09002000080000000',
    '00000000000040889002000000100000',
    '00000000010000809003000080000000',
    '00000000010004003800000008002000',
    '00000000020000801222000000100000',
    '00000000040000801202000080100000',
    '00000000040000801202000120000000',
    '0000000a000000003800000008100000',
    '00000010000000801202000000000404',
    '00000010000000801202000100000100',
]
VERDICTS = os.path.join(BASE, 'verdicts28')
RUNNER = os.path.join(BASE, 'scripts', 'class4_child1_runner_v17.ts')
os.makedirs(VERDICTS, exist_ok=True)

def maxbit(h):
    m = int(h, 16); b = -1
    while m:
        b += 1; m >>= 1
    return b

def main():
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 200.0
    assert len(ROOTS) == 28, len(ROOTS)
    for rh, expect_child, expect_bit in [
        ('00000000000000821082000000042000', '00000000000000021082000000042000', 71),
        ('00000000000000821082000000420000', '00000000000000021082000000420000', 71),
    ]:
        b = maxbit(rh); child = f'{(int(rh,16) ^ (1<<b)):032x}'
        assert child == expect_child and b == expect_bit, (rh, b, child)
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
    with ThreadPoolExecutor(max_workers=4) as ex:
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
