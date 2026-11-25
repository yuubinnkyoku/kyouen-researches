#!/usr/bin/env python3
"""Rank all still-uncertified WIN7-D10 warm candidates of the class2-lane
sweeps against the after-warm-multiband chain head (solved 1109 / unique
remaining 6738 / sum 531295 / open 5008/395018, canonical chain head
class-frontier-warm-multiband-recompute-20261115.json, 2026-11-15).

Successor of rank_warm_candidates_20261115.py (which ranked against the
after-cost-75b frontier 1049 and drove the 35-certificate warm multiband
batch): this v2 re-derives per-candidate marginals against the current 1109
solved set, excluding every root/band already certified by the warm rebuild
records (cost-60b/63e/65g) and the warm multiband records (35 receipts).

Parallel-lane bands (cost-65h/67b/68c, plus the in-flight cost-65j sweep)
are ranked for visibility but excluded from the greedy selection.

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

# ---------- 1. reproduce the after-warm-multiband chain head (1109) ----------
nsW = runpy.run_path(str(HERE / 'scripts' /
                         'recompute_frontier_warm_multiband_20261115.py'))
s_head = nsW['s_cur']
manifest = nsW['manifest']
covers = nsW['covers']
stW = nsW['stW']
assert stW['solved_s6_in_manifest'] == 1109 and stW['unique_remaining_s6'] == 6738
assert stW['sum_remaining_cost'] == 531295
assert stW['s6_needed_by_open_classes'] == 5008 and stW['cost_needed_by_open_classes'] == 395018
print('CONTROL after-warm-multiband chain head reproduced: '
      '1109/6738/531295/5008/395018')

# ---------- 2. every published WIN7 root (already certified) ----------
certified_roots = set()
covered_bits = {}  # band -> [bits with published certificates]


def add_roots(rec, certified_roots):
    if not isinstance(rec, dict):
        return
    if 'root_hex' in rec and rec.get('verdict', 'WIN7') == 'WIN7':
        certified_roots.add(rec['root_hex'])
    for k, v in rec.items():
        if k in ('certificates', 'warm_certificates', 'records') and isinstance(v, list):
            for c in v:
                if isinstance(c, dict) and c.get('verdict', 'WIN7') == 'WIN7' \
                        and 'root_hex' in c:
                    certified_roots.add(c['root_hex'])
                    covered_bits.setdefault(c.get('band'), []).append(c['bit'])


WARM_RECORDS = [
    'class2-lane-cost60b-warm-certificates-20261115.json',
    'class2-lane-cost63e-warm-certificates-20261114.json',
    'class2-lane-cost65g-warm-certificates-20261114.json',
    'class2-lane-warm-multiband-certificates-20261115.json',
]
for name in WARM_RECORDS:
    rec = json.loads((OUT / name).read_text())
    add_roots(rec, certified_roots)
for name in sorted(glob.glob(str(OUT / '*win7-certificates*.json'))):
    rec = json.loads(Path(name).read_text())
    add_roots(rec, certified_roots)
for name in sorted(glob.glob(str(OUT / '*certificates-verified.json'))):
    rec = json.loads(Path(name).read_text())
    add_roots(rec, certified_roots)
for name in ('class4-batch3-bit37-certificate.json',):
    rec = json.loads((OUT / name).read_text())
    if 'root_hex' in rec:
        certified_roots.add(rec['root_hex'])
print(f'CONTROL published WIN7 roots collected: {len(certified_roots)}')

# ---------- 3. the candidate pool (unverified WIN7 bits per sweep) ----------
PARALLEL_BANDS = {
    'class2-lane-cost65h': 'active parallel-lane band (sweep by the parallel lane; '
                           'certificates bits 7/109/24 published by them)',
    'class2-lane-cost67b': 'active parallel-lane band',
    'class2-lane-cost68c': 'active parallel-lane band',
}
candidates = []
for name in sorted(glob.glob(str(OUT / 'class2-lane-cost*-sweep-*.json'))):
    rec = json.loads(Path(name).read_text())
    unv = rec.get('unverified_win7_bits')
    if not unv:
        continue
    band = Path(name).name.split('-sweep-')[0]
    wb = rec.get('win7_bits') or []
    wr = rec.get('win7_roots') or []
    assert len(wb) == len(wr), name
    roots = dict(zip(wb, wr))
    skip = set(covered_bits.get(band, []))
    for bit in unv:
        if bit in skip:
            continue
        root_hex = roots[bit]
        candidates.append({
            'sweep': Path(name).name,
            'band': band,
            'child_hex': rec['s6_child_hex'],
            'bit': bit,
            'root_hex': root_hex,
            'root_already_certified': root_hex in certified_roots,
            'parallel_lane_band': band in PARALLEL_BANDS,
        })
# the cost-72 record (bit-111 certified, bit-52 now certified by the multiband)
rec72 = json.loads((OUT / 'class2-lane-cost72-win7-certificates-20261115.json').read_text())
for bit in rec72['unverified_win7_bits']:
    if bit in covered_bits.get('class2-lane-cost72', []):
        continue
    candidates.append({
        'sweep': 'class2-lane-cost72-win7-certificates-20261115.json',
        'band': 'class2-lane-cost72',
        'child_hex': rec72['child_s6_hex'],
        'bit': bit,
        'root_hex': format(int(rec72['child_s6_hex'], 16) | (1 << bit), '032x'),
        'root_already_certified': False,
        'parallel_lane_band': False,
    })

# ---------- 4. marginals against the current solved set ----------
by_root = {}
for c in candidates:
    by_root.setdefault(c['root_hex'], []).append(c)

rows = []
for root_hex, group in by_root.items():
    cov = covers(int(root_hex, 16))
    marg = cov - s_head
    marg_m = marg & manifest
    rows.append({
        'root_hex': root_hex,
        'entries': [f"{g['band']} bit-{g['bit']}" for g in group],
        'bands': sorted(set(g['band'] for g in group)),
        'child_hexes': sorted(set(g['child_hex'] for g in group)),
        'bits': sorted(g['bit'] for g in group),
        'root_already_certified': any(g['root_already_certified'] for g in group),
        'parallel_lane_band': any(g['parallel_lane_band'] for g in group),
        'n_entries': len(group),
        'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    })
rows.sort(key=lambda r: (-r['marginal_in_manifest'], -r['marginal'],
                         r['root_hex']))

# ---------- 5. greedy fold order over selectable (own-lane) roots ----------
greedy = []
grown = set(s_head)
remaining = [r for r in rows
             if not r['root_already_certified'] and not r['parallel_lane_band']]
while remaining and len(greedy) < 60:
    best = None
    for r in remaining:
        cov = covers(int(r['root_hex'], 16))
        gain = len((cov - grown) & manifest)
        if best is None or gain > best[0] or (gain == best[0] and
                                              (r['marginal_in_manifest'],
                                               r['root_hex']) > (best[1]['marginal_in_manifest'],
                                                                 best[1]['root_hex'])):
            best = (gain, r, cov)
    gain, r, cov = best
    if gain == 0 and r['marginal'] == 0:
        # nothing with any uncovered orbit remains; keep only if gain>0
        remaining.remove(r)
        continue
    greedy.append({
        'root_hex': r['root_hex'],
        'entries': r['entries'],
        'fold_gain_in_manifest': gain,
        'uncovered_outside_manifest': len((cov - grown) - manifest),
    })
    grown |= cov
    remaining.remove(r)

total_manifest_gain = sum(g['fold_gain_in_manifest'] for g in greedy)
n_parallel_rows = sum(1 for r in rows if r['parallel_lane_band'] and
                     not r['root_already_certified'])

result = {
    'schema': 'n11-class2-lane-warm-candidate-ranking2-20261115-v1',
    'date': '2026-11-15',
    'baseline': 'class-frontier-warm-multiband-recompute-20261115.json '
                '(solved 1109 / unique remaining 6738 / sum 531295 / open '
                '5008/395018)',
    'published_win7_roots': len(certified_roots),
    'n_candidate_roots': len(rows),
    'n_candidate_roots_already_certified': sum(1 for r in rows if r['root_already_certified']),
    'n_parallel_lane_candidate_roots_uncertified': n_parallel_rows,
    'ranking_top': rows[:60],
    'greedy_fold_order': greedy,
    'greedy_total_in_manifest_gain': total_manifest_gain,
    'interpretation_guard': 'bookkeeping over published records; marginals are '
                            'derived from root parent-lift orbits and the current '
                            'solved set only; no new certificate is created here; '
                            'parallel-lane bands (65h/67b/68c + in-flight 65j) are '
                            'excluded from the greedy selection; 11x11 empty root / '
                            '{49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class2-lane-warm-candidate-ranking2-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class2-lane-warm-candidate-ranking2-20261115.json')
print('candidates:', len(rows), 'already-certified roots:',
      sum(1 for r in rows if r['root_already_certified']))
print('parallel-lane uncertified roots (excluded from selection):', n_parallel_rows)
print('greedy total in-manifest gain over own-lane uncertified roots:',
      total_manifest_gain)
for g in greedy[:25]:
    print(f"  {g['fold_gain_in_manifest']:2d}  {g['root_hex']}  {g['entries']}")
