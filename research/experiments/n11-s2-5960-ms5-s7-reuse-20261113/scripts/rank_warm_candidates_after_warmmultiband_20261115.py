#!/usr/bin/env python3
"""Rank all still-uncertified WIN7-D10 warm candidates of the class2-lane
sweeps against the after-warm-multiband frontier (solved 1109 / unique
remaining 6738 / sum 531295 / open 5008/395018, canonical chain head
class-frontier-warm-multiband-recompute-20261115.json, 2026-11-15).

Same coordinator logic as rank_warm_candidates_20261115.py, but the baseline
is the post-35-receipt state: the bits certified by the warm multiband batch
(cost-61d bit-119, 61e bits 4/102, 61f bit-102, 62a bits 32/66/86/95/105/109/
112/118, 63a bits 2/15/28/100/118, 64b bits 8/33/102, 65e bits 7/26/29/32/33/
42/94/105/106/111/114/116, 71b bits 14/32, 72 bit-52) are removed from the
candidate pool, their roots are added to the certified set, and every marginal
is re-derived against the 1109 solved set. This is the coordinator instrument
for the next warm batch.

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

# ---------- 1. reproduce the after-warm-multiband frontier (1109) ----------
nsW = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_warm_multiband_20261115.py'))
s_cur = nsW['s_cur']
manifest = nsW['manifest']
covers = nsW['covers']
stW = nsW['stW']
assert stW['solved_s6_in_manifest'] == 1109 and stW['unique_remaining_s6'] == 6738
assert stW['sum_remaining_cost'] == 531295
assert stW['s6_needed_by_open_classes'] == 5008 and stW['cost_needed_by_open_classes'] == 395018
print('CONTROL after-warm-multiband baseline reproduced: 1109/6738/531295/5008/395018')

# ---------- 2. every published WIN7 root (already certified) ----------
certified_roots = set()


def add_roots(rec, certified_roots):
    n0 = len(certified_roots)
    if isinstance(rec, dict):
        if rec.get('verdict', 'WIN7') == 'WIN7' and 'root_hex' in rec:
            certified_roots.add(rec['root_hex'])
        for k, v in rec.items():
            if k in ('certificates', 'warm_certificates', 'records') and isinstance(v, list):
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
warm_bits_closed = {}
for name in WARM_RECORDS:
    rec = json.loads((OUT / name).read_text())
    add_roots(rec, certified_roots)
    band = name.split('-warm-')[0]
    warm_bits_closed[band] = [c['bit'] for c in rec.get('certificates', [])
                              if c.get('verdict', 'WIN7') == 'WIN7']
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

# the 35 warm multiband receipts (records list)
multiband = json.loads((OUT / 'class2-lane-warm-multiband-certificates-20261115.json').read_text())
multiband_bits = {}
for r in multiband['records']:
    certified_roots.add(r['root_hex'])
    multiband_bits.setdefault(r['band'], []).append(r['bit'])
print(f'CONTROL published WIN7 roots collected: {len(certified_roots)}')

# ---------- 3. the candidate pool (unverified WIN7 bits per sweep) ----------
WARM_COVERED = {}
for name, band in [
    ('class2-lane-cost60b-sweep-20261114.json', 'class2-lane-cost60b'),
    ('class2-lane-cost63e-sweep-20261114.json', 'class2-lane-cost63e'),
    ('class2-lane-cost65g-sweep-20261114.json', 'class2-lane-cost65g'),
]:
    WARM_COVERED[name] = warm_bits_closed.get(band, [])
# warm multiband: the sweep record names differ in date suffix, match by band prefix
for sweep_name in glob.glob(str(OUT / 'class2-lane-cost*-sweep-*.json')):
    band = Path(sweep_name).name.split('-sweep-')[0]
    if band in multiband_bits:
        WARM_COVERED[Path(sweep_name).name] = (
            WARM_COVERED.get(Path(sweep_name).name, []) + multiband_bits[band])

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
    greedy.append({
        'root_hex': r['root_hex'],
        'entries': r['entries'],
        'fold_gain_in_manifest': gain,
        'uncovered_outside_manifest': len((cov - grown) - manifest),
        'marginal_manifest_hexes': r['marginal_manifest_hexes'],
    })
    grown |= cov
    remaining.remove(r)
    if len(greedy) >= 40:
        break

total_manifest_gain = sum(g['fold_gain_in_manifest'] for g in greedy)

result = {
    'schema': 'n11-class2-lane-warm-candidate-ranking-after-warm-multiband-20261115-v1',
    'date': '2026-11-15',
    'baseline': 'class-frontier-warm-multiband-recompute-20261115.json '
                '(solved 1109 / unique remaining 6738 / sum 531295 / open 5008/395018)',
    'published_win7_roots': len(certified_roots),
    'n_candidate_roots': len(rows),
    'n_candidate_roots_already_certified': sum(1 for r in rows if r['root_already_certified']),
    'n_uncertified_candidate_roots': sum(1 for r in rows if not r['root_already_certified']),
    'ranking_top': rows[:40],
    'greedy_fold_order': greedy,
    'greedy_total_in_manifest_gain': total_manifest_gain,
    'interpretation_guard': 'bookkeeping over published records; marginals are '
                            'derived from root parent-lift orbits and the current '
                            'solved set only; no new certificate is created here; '
                            '11x11 empty root / {49,60} / S2 {59,60} / class 2 / '
                            'class 4 remain UNKNOWN',
}
(OUT / 'class2-lane-warm-candidate-ranking-after-warm-multiband-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class2-lane-warm-candidate-ranking-after-warm-multiband-20261115.json')
print(f'uncertified candidate roots: {result["n_uncertified_candidate_roots"]}')
print(f'greedy total in-manifest gain: {total_manifest_gain}')
for g in greedy[:5]:
    print(f"  {g['root_hex']} gain={g['fold_gain_in_manifest']} "
          f"outside={g['uncovered_outside_manifest']} {','.join(g['entries'])}")
