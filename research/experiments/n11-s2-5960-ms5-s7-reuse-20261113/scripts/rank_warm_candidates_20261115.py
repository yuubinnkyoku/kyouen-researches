#!/usr/bin/env python3
"""Rank all still-uncertified WIN7-D10 warm candidates of the class2-lane
sweeps against the after-cost-75b frontier (solved 1049 / unique remaining
6798 / sum 535812 / open 5068/399535, canonical chain head
class-frontier-cost75b-recompute-20261115.json, 2026-11-15).

Purpose: the coordinator picks which warm certificate to build next. A WIN7-D10
candidate only advances the global frontier when at least one of the 7
parent-lift orbits of its root lies in the MS5 manifest and is not yet in the
solved set. This script re-derives, for every unverified candidate of every
published sweep record (minus the bits already covered by the warm rebuild
records of cost-60b / cost-63e / cost-65g, minus roots that already have a
published certificate), the per-candidate marginal against the current solved
set, then reports a greedy fold order (marginals re-derived from the growing
union) with the total expected in-manifest gain. It also measures the fold
value of the published-but-unfolded cost-72 bit-111 partial receipt.

This is bookkeeping over published records only. It certifies nothing: a warm
candidate remains a search result until a certificate is extracted, verified
and published. 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4
remain UNKNOWN.
"""
import glob
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-75b frontier (1049) ----------
ns75 = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost75b_20261115.py'))
s_cur = ns75['s_cur']
manifest = ns75['manifest']
covers = ns75['covers']
st75 = ns75['st75']
assert st75['solved_s6_in_manifest'] == 1049 and st75['unique_remaining_s6'] == 6798
assert st75['sum_remaining_cost'] == 535812
assert st75['s6_needed_by_open_classes'] == 5068 and st75['cost_needed_by_open_classes'] == 399535
print('CONTROL after-cost-75b baseline reproduced: 1049/6798/535812/5068/399535')

# ---------- 2. every published WIN7 root (already certified) ----------
certified_roots = set()


def add_roots(rec, certified_roots):
    n0 = len(certified_roots)
    if isinstance(rec, dict):
        if 'root_hex' in rec and rec.get('verdict', 'WIN7') == 'WIN7':
            certified_roots.add(rec['root_hex'])
        if rec.get('verdict') == 'WIN7' and 'root_hex' in rec:
            certified_roots.add(rec['root_hex'])
        for k, v in rec.items():
            if k in ('certificates', 'warm_certificates') and isinstance(v, list):
                for c in v:
                    if isinstance(c, dict):
                        if c.get('verdict', 'WIN7') == 'WIN7' and 'root_hex' in c:
                            certified_roots.add(c['root_hex'])
    return len(certified_roots) - n0


WARM_RECORDS = [
    'class2-lane-cost60b-warm-certificates-20261115.json',
    'class2-lane-cost63e-warm-certificates-20261114.json',
    'class2-lane-cost65g-warm-certificates-20261114.json',
]
for name in WARM_RECORDS:
    rec = json.loads((OUT / name).read_text())
    add_roots(rec, certified_roots)
    # the warm records themselves enumerate the bits they closed
warm_bits_closed = {}
for name in WARM_RECORDS:
    rec = json.loads((OUT / name).read_text())
    band = name.split('-warm-')[0]
    warm_bits_closed[band] = [c['bit'] for c in rec.get('certificates', [])
                              if c.get('verdict', 'WIN7') == 'WIN7']
# every *win7-certificates*.json record (bits with published certificates)
for name in sorted(glob.glob(str(OUT / '*win7-certificates*.json'))):
    rec = json.loads(Path(name).read_text())
    add_roots(rec, certified_roots)
# the class4-batch and verified- records read by the chain root
for name in sorted(glob.glob(str(OUT / '*certificates-verified.json'))):
    rec = json.loads(Path(name).read_text())
    add_roots(rec, certified_roots)
for name in ('class4-batch3-bit37-certificate.json',):
    rec = json.loads((OUT / name).read_text())
    if 'root_hex' in rec:
        certified_roots.add(rec['root_hex'])
print(f'CONTROL published WIN7 roots collected: {len(certified_roots)}')

# ---------- 3. the candidate pool (unverified WIN7 bits per sweep) ----------
WARM_COVERED = {
    'class2-lane-cost60b-sweep-20261114.json': warm_bits_closed.get('class2-lane-cost60b', []),
    'class2-lane-cost63e-sweep-20261114.json': warm_bits_closed.get('class2-lane-cost63e', []),
    'class2-lane-cost65g-sweep-20261114.json': warm_bits_closed.get('class2-lane-cost65g', []),
}

candidates = []
for name in sorted(glob.glob(str(OUT / 'class2-lane-cost*-sweep-*.json'))):
    rec = json.loads(Path(name).read_text())
    unv = rec.get('unverified_win7_bits')
    if not unv:
        continue
    wb = rec.get('win7_bits') or []
    wr = rec.get('win7_roots') or []
    assert len(wb) == len(wr), name
    roots = dict(zip(wb, wr))
    skip = set(WARM_COVERED.get(Path(name).name, []))
    for bit in unv:
        if bit in skip:
            continue
        root_hex = roots[bit]
        candidates.append({
            'sweep': Path(name).name,
            'band': Path(name).name.split('-sweep-')[0],
            'child_hex': rec['s6_child_hex'],
            'bit': bit,
            'root_hex': root_hex,
            'root_already_certified': root_hex in certified_roots,
        })
# the cost-72 sweep has no completed sweep record; its partial receipt record
# enumerates the two WIN7-D10 bits (bit-111 certified, bit-52 uncertified)
rec72 = json.loads((OUT / 'class2-lane-cost72-win7-certificates-20261115.json').read_text())
for bit in rec72['unverified_win7_bits']:
    candidates.append({
        'sweep': 'class2-lane-cost72-win7-certificates-20261115.json',
        'band': 'class2-lane-cost72',
        'child_hex': rec72['child_s6_hex'],
        'bit': bit,
        'root_hex': format(int(rec72['child_s6_hex'], 16) | (1 << bit), '032x'),
        'root_already_certified': False,
    })

# ---------- 4. marginals against the current solved set ----------
by_root = {}
for c in candidates:
    by_root.setdefault(c['root_hex'], []).append(c)

rows = []
for root_hex, group in by_root.items():
    cov = covers(int(root_hex, 16))
    marg = cov - s_cur
    marg_m = marg & manifest
    rows.append({
        'root_hex': root_hex,
        'entries': [f"{g['band']} bit-{g['bit']}" for g in group],
        'root_already_certified': group[0]['root_already_certified'],
        'n_entries': len(group),
        'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    })
rows.sort(key=lambda r: (-r['marginal_in_manifest'], -r['marginal'],
                         r['root_hex']))

# ---------- 5. greedy fold order over uncertified roots ----------
greedy = []
grown = set(s_cur)
remaining = [r for r in rows if not r['root_already_certified']]
while True:
    best = None
    for r in remaining:
        cov = covers(int(r['root_hex'], 16))
        gain = len((cov - grown) & manifest)
        if best is None or gain > best[0] or (gain == best[0] and
                                              (r['marginal_in_manifest'],
                                               r['root_hex']) > (best[1]['marginal_in_manifest'],
                                                                 best[1]['root_hex'])):
            best = (gain, r, cov)
    if best is None:
        break
    gain, r, cov = best
    if gain == 0 and r['marginal'] == 0:
        # nothing left with any uncovered orbit at all
        pass
    greedy.append({
        'root_hex': r['root_hex'],
        'entries': r['entries'],
        'fold_gain_in_manifest': gain,
        'uncovered_outside_manifest': len((cov - grown) - manifest),
    })
    grown |= cov
    remaining.remove(r)
    if len(greedy) >= 40:
        break

total_manifest_gain = sum(g['fold_gain_in_manifest'] for g in greedy)

# ---------- 6. the published-but-unfolded cost-72 bit-111 receipt ----------
bit111_root = rec72['certificate']['root_hex']
cov111 = covers(int(bit111_root, 16))
marg111 = cov111 - s_cur
marg111_m = marg111 & manifest

result = {
    'schema': 'n11-class2-lane-warm-candidate-ranking-20261115-v1',
    'date': '2026-11-15',
    'baseline': 'class-frontier-cost75b-recompute-20261115.json '
                '(solved 1049 / unique remaining 6798 / sum 535812 / open 5068/399535)',
    'published_win7_roots': len(certified_roots),
    'n_candidate_roots': len(rows),
    'n_candidate_roots_already_certified': sum(1 for r in rows if r['root_already_certified']),
    'cost72_bit111_receipt_unfolded': {
        'root_hex': bit111_root,
        'marginal': len(marg111),
        'marginal_in_manifest': len(marg111_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg111_m),
    },
    'ranking_top': rows[:40],
    'greedy_fold_order': greedy,
    'greedy_total_in_manifest_gain': total_manifest_gain,
    'interpretation_guard': 'bookkeeping over published records; marginals are '
                            'derived from root parent-lift orbits and the current '
                            'solved set only; no new certificate is created here; '
                            '11x11 empty root / {49,60} / S2 {59,60} / class 2 / '
                            'class 4 remain UNKNOWN',
}
(OUT / 'class2-lane-warm-candidate-ranking-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class2-lane-warm-candidate-ranking-20261115.json')
print('candidates:', len(rows), 'already-certified roots:',
      sum(1 for r in rows if r['root_already_certified']))
print('cost72 bit111 (published, unfolded) marginal_in_manifest:',
      len(marg111_m), sorted(f'{k:032x}' for k in marg111_m))
print('greedy total in-manifest gain over uncertified roots:',
      total_manifest_gain)
for g in greedy[:20]:
    print(f"  {g['fold_gain_in_manifest']:2d}  {g['root_hex']}  {g['entries']}")
