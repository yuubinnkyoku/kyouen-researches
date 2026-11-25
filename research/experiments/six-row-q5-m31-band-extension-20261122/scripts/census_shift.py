#!/usr/bin/env python3
"""Placement census (staircase table) for witness band extension without new stones.

For a fixed safe stone configuration S (span = maxx+1 columns, rows 0..w-1),
placing S with x-offset s on a board of width m2 >= s+span gives a
row-deficient maximal safe configuration on the w x m2 board iff every empty
cell of that board is blocked.  Blocking depends only on (S, c) (K0853), so:

  left strip  : columns 0..s-1           -> covered by the shifted config's
                                           old-column coverage scan
  stone span  : columns s..s+span-1      -> idem (maximality at own width)
  right strip : columns s+span .. m2-1   -> covered iff m2 <= free_append_reach

Hence for each offset s the config witnesses at EVERY width in
[s+span, reach_s] (when old coverage is complete), and the per-config band
top by placement is  max over s of reach_s  among complete-coverage offsets.
All placements x-offset 0..(m2-span) are enumerated; this is a COMPLETE
placement census for the config family (mirror placements are the same
config reflected, a separate config the caller may census as well).

Per offset exactly one append_criterion.py call (verbatim published script,
sha256 d08d8fb16a5ed9cae11ba781ff5606c7f07da77c7e6bc934b88b1b3fc59a51d0)
with the requested scan_limit; the caller picks scan_limit ABOVE all target
widths so reach_s saturates.  No float; deterministic.

Usage: python3 census_shift.py <stones.json> w q max_width
  stones.json: either [[x,y],...] or {"stones": [[x,y],...]}
Output: JSON on stdout with the per-offset staircase and the placement band top.
"""
import json, subprocess, sys, os

def load_stones(p):
    d = json.load(open(p))
    if isinstance(d, dict):
        for k in ('stones', 'config', 'witness'):
            if k in d:
                return d[k]
        raise SystemExit(f'no stones key in {p}')
    return d

def main():
    stones_path, w, q, maxw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    scan_limit = maxw + 2
    S = [list(p) for p in load_stones(stones_path)]
    span = max(x for x, _ in S) + 1
    here = os.path.dirname(os.path.abspath(__file__))
    crit = os.path.join(here, 'append_criterion.py')
    table = []
    top = span  # offset 0 width span always covered by definition of census use
    for s in range(0, maxw - span + 1):
        shifted = [[x + s, y] for x, y in S]
        r = subprocess.run(['python3', crit, str(w), str(scan_limit), str(q)],
                           input=json.dumps(shifted), capture_output=True, text=True, check=True)
        j = json.loads(r.stdout.strip())
        reach = j['free_append_reach']
        cov_ok = j['old_uncovered_count'] == 0
        if cov_ok:
            # widths witnessed at this offset: s+span .. min(reach, maxw)
            hi = min(reach, maxw)
            if hi >= s + span and hi > top:
                top = hi
        table.append({'offset': s, 'old_uncovered': j['old_uncovered_count'],
                      'reach': reach, 'first_unblocked': j.get('first_unblocked'),
                      'safe': j['safe'], 'rows': j['rows']})
    print(json.dumps({'path': stones_path, 'w': w, 'q': q, 'span': span,
                      'max_width': maxw,
                      'placement_band_top': top,
                      'raising_widths_m2': sorted({min(t['reach'], maxw) for t in table
                                                    if t['old_uncovered'] == 0 and t['reach'] >= 0}),
                      'table': table}, indent=1))

if __name__ == '__main__':
    main()
