#!/usr/bin/env python3
"""Count unblocked cells on a target width M for every pool placement (base ranking).

Uses the exact Fraction blocking predicate of append_criterion.py (imported,
published sha). For each pool config and each x-offset 0..(M-span), counts
empty cells of the w x M board that are not blocked by the placement.
Output: JSON list sorted by unblocked count (best bases first) + stdout.
Usage: unblocked_scan.py M [M2 ...]
"""
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('append_criterion', os.path.join(HERE, 'append_criterion.py'))
ac = importlib.util.module_from_spec(spec)
# append_criterion runs on import? no: it has __main__ guard. import functions only.
src = open(os.path.join(HERE, 'append_criterion.py')).read()
ns = {}
exec(compile(src.replace("if __name__ == '__main__':", "if False:"), 'append_criterion', 'exec'), ns)
canon_line, circle_coeffs = ns['canon_line'], ns['circle_coeffs']

def analyze(w, M, q, S):
    n = len(S)
    maxx = max(x for x, y in S)
    lines = {}
    for i in range(n):
        for j in range(i+1, n):
            k = canon_line(S[i], S[j])
            lines[k] = lines.get(k, 0) + 1
    circles = {}
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                co = circle_coeffs(S[i], S[j], S[k])
                if co is not None:
                    circles[co] = True
    sset = set(map(tuple, S))
    def blocked(c):
        for s in S:
            k = canon_line(c, s)
            if sum(1 for p in S if k[0]*p[0]+k[1]*p[1]+k[2] == 0) >= q-1:
                return True
        for co in circles:
            D, E, F = co
            if c[0]*c[0]+c[1]*c[1]+D*c[0]+E*c[1]+F == 0 and sum(1 for p in S if p[0]*p[0]+p[1]*p[1]+D*p[0]+E*p[1]+F == 0) >= q-1:
                return True
        return False
    unb = []
    for x in range(M):
        for y in range(w):
            c = (x, y)
            if c in sset: continue
            if not blocked(c): unb.append(list(c))
    return unb

def main():
    Ms = [int(a) for a in sys.argv[1:]] or [32]
    pool = json.load(open(os.path.join(KIT, 'pool.json')))
    for M in Ms:
        rows = []
        for c in pool['configs']:
            for off in range(0, M - c['span'] + 1):
                shifted = [(x+off, y) for x, y in c['stones']]
                unb = analyze(6, M, 5, shifted)
                rows.append({'cfg': c['cfg_id'], 'offset': off, 'unblocked': len(unb), 'cells': unb})
        rows.sort(key=lambda r: r['unblocked'])
        with open(os.path.join(KIT, 'unblocked_w%d.json' % M), 'w') as f:
            json.dump(rows, f, indent=1)
        print('== width', M)
        for r in rows[:14]:
            print(r['cfg'], 'off', r['offset'], 'unblocked', r['unblocked'], r['cells'])

main()
