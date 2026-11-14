#!/usr/bin/env python3
"""Extract stones from a saved kissat raw log (SAT), dual-verify
(census-free JS sat.js verifyConfig + verify_witness.py Python Fraction),
save witness JSON, and append a record line to output/results.jsonl.

Usage: extract_verify.py w m q tag rawlog.kissat.txt --mode=deficient|rowfixed --rowY=Y [--conflicts=N]
Reads the 'p cnf' header size and encoding params from the log itself.
"""
import json, re, subprocess, sys, pathlib, argparse

DIR = pathlib.Path(__file__).resolve().parent.parent

p = argparse.ArgumentParser()
p.add_argument('w', type=int); p.add_argument('m', type=int); p.add_argument('q', type=int)
p.add_argument('tag'); p.add_argument('log')
p.add_argument('--mode', default='deficient')
p.add_argument('--rowY', type=int, default=None)
p.add_argument('--lex', default='')
p.add_argument('--note', default='')
a = p.parse_args()

raw = open(a.log).read()
status = 'SAT' if 's SATISFIABLE' in raw else ('UNSAT' if 's UNSATISFIABLE' in raw else 'UNKNOWN')
conf = int((re.search(r'c conflicts:\s+(\d+)', raw) or [0, 0])[1])
deci = int((re.search(r'c decisions:\s+(\d+)', raw) or [0, 0])[1])
hdr = re.search(r"parsed 'p cnf (\d+) (\d+)'", raw)
nv, ncl = (int(hdr.group(1)), int(hdr.group(2))) if hdr else (None, None)
assert status == 'SAT', f'log is {status}, need SAT'

lits = []
for l in raw.split('\n'):
    if l.startswith('v '):
        lits += [int(t) for t in l[2:].split()]
pos = set(v for v in lits if v > 0)
stones = [[x, y] for y in range(a.w) for x in range(a.m) if (y * a.m + x + 1) in pos]
rows = [sum(1 for s in stones if s[1] == y) for y in range(a.w)]

js = subprocess.run(['node', '-e',
    f'const S=require("{DIR}/scripts/sat.js");'
    f'const st=JSON.parse(require("fs").readFileSync(0));'
    f'console.log(JSON.stringify(S.verifyConfig({a.w},{a.m},{a.q},st)));'],
    input=json.dumps(stones), capture_output=True, text=True)
jsv = json.loads(js.stdout)
py = subprocess.run(['python3', str(DIR / 'scripts/verify_witness.py'), str(a.w), str(a.m), str(a.q)],
                    input=json.dumps(stones), capture_output=True, text=True)
pyv = json.loads(py.stdout)
ok = (jsv.get('ok') is True) and (pyv.get('ok') is True)
print(f'w={a.w} m={a.m} q={a.q} nStones={len(stones)} rows={rows} conflicts={conf} jsOK={jsv.get("ok")} pyOK={pyv.get("ok")}')
assert ok, f'verification failed: js={jsv} py={pyv}'

base = a.log.split('/')[-1].replace('.kissat.txt', '')
json.dump(stones, open(f'{DIR}/output/{base}.witness.json', 'w'))
rec = {'w': a.w, 'm': a.m, 'q': a.q, 'tag': a.tag, 'lex': a.lex.split(',') if a.lex else [],
       'encoding': {'vars': nv, 'clauses': ncl, 'mode': a.mode, 'rowY': a.rowY},
       'solver': 'kissat-4.0.4', 'status': 'SAT', 'conflicts': conf, 'decisions': deci,
       'stones': stones, 'rows': rows, 'nStones': len(stones), 'jsVerify': jsv, 'pyVerify': pyv}
if a.note: rec['note'] = a.note
open(f'{DIR}/output/results.jsonl', 'a').write(json.dumps(rec) + '\n')
print('recorded ->', f'output/{base}.witness.json')
