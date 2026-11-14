#!/usr/bin/env python3
"""Assemble class2-lane-warm-band-hygiene-certificates-20261115.json.

Warm band hygiene batch: extraction + BigInt independent verification for the
remaining uncertified WIN7 roots of the my-lane bands that the batch-1 warm
multiband push and the parallel-lane pushes left open (62a bits 1/89, 63a bits
11/109, 71b bit-1 == 61d bit-22 cross-child duplicate). Frontier numbers are
unchanged by this batch (all roots were already WIN7-anchored by their sweep
receipts); this closes certificate gaps only.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
WARM = HERE / 'warm'
REPO_OUT = 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output'

ABSENCE = {
    ('class2-lane-cost62a', 1): ['research/log/2026-11-14-n11-class2-cost62a-partial-raw-audit.md',
                                 f'{REPO_OUT}/class2-lane-cost62a-sweep-20261114.json'],
    ('class2-lane-cost62a', 89): [f'{REPO_OUT}/class2-lane-cost62a-sweep-20261114.json'],
    ('class2-lane-cost63a', 11): [f'{REPO_OUT}/class2-lane-cost63a-sweep-20261114.json'],
    ('class2-lane-cost63a', 109): [f'{REPO_OUT}/class2-lane-cost63a-sweep-20261114.json'],
    ('class2-lane-cost71b', 1): [f'{REPO_OUT}/scripts/recompute_frontier_cost71b_20261115.py',
                                 f'{REPO_OUT}/class2-lane-cost71b-sweep-20261115.json',
                                 f'{REPO_OUT}/class2-lane-cost61d-inflight-20261114.json',
                                 f'{REPO_OUT}/class2-lane-cost61d-sweep-20261114.json',
                                 f'{REPO_OUT}/class-frontier-cost71b-recompute-20261115.json'],
}
NOTES = {
    ('class2-lane-cost62a', 1): 'closes the last two open cost-62a WIN7 bits (with bit-89 below); '
                                'the 62a band is now fully certified: 11/11 WIN7 bits have published '
                                'certificates (bit 11 original + bits 32/66/86/95/105/109/112/118 in '
                                'the batch-1 warm multiband push + bits 1/89 here)',
    ('class2-lane-cost62a', 89): 'with bit-1 above, completes the cost-62a band certificate coverage '
                                '(11/11)',
    ('class2-lane-cost63a', 11): 'cost-63a moves to 8/10 certified (119 + batch-1 bits '
                                 '2/15/28/100/118 + bits 11/109 here); the remaining bits 96/97 are '
                                 'claimed by the parallel warm-multiband batch-2 lane',
    ('class2-lane-cost63a', 109): 'with bit-11 above, cost-63a reaches 8/10 certificate coverage; '
                                 'bits 96/97 remain with the parallel lane',
    ('class2-lane-cost71b', 1): 'closes the first item of the parallel-lane cost-71b '
                                'remaining_win7_bits list [1,14,32,74,94,117]; together with the '
                                'batch-1 warm multiband bits 14/32 and the parallel-lane bits '
                                '109/21/105, cost-71b is 6/9 certified (74/94/117 remain)',
}
CANON = {
    ('class2-lane-cost61d', 22): 'byte-identical independent re-extraction of the same root as the '
                                'cost-71b bit-1 certificate above (cross-child duplicate listing; '
                                'md5 0c241e6759fdddd9605bdb4f63e19d3c matches): positive duplicate '
                                'cross-check between two child-lane listings; the certificate is '
                                'pushed once under class2-lane-cost71b-certificates/ and serves both '
                                'listings; cost-61d moves to 5/14 certified (30/74/94 original, 119 '
                                'batch-1, 22 here)',
}

records = json.loads((WARM / 'warm_records.json').read_text())
assert len(records) == 6

entries = []
for r in records:
    band, bit = r['band'], r['bit']
    repo_dir = f'{REPO_OUT}/{band}-certificates'
    name = f'bit{bit}-root-{r["root_hex"]}.cert'
    whole = WARM / f'{band}-bit{bit}-root-{r["root_hex"]}.cert'
    whole_md5 = hashlib.md5(whole.read_bytes()).hexdigest()
    assert whole_md5 == r['md5']
    e = dict(r)
    e['selection'] = 'warm band hygiene: remaining uncertified WIN7 roots of the my-lane bands ' \
                     '(coordinator marginal_in_manifest=4, mim=0: no frontier number changes)'
    if r['bytes'] > 1_835_000:
        p1 = Path(str(whole) + '.part1of2')
        p2 = Path(str(whole) + '.part2of2')
        assert hashlib.md5(p1.read_bytes() + p2.read_bytes()).hexdigest() == whole_md5
        e['file'] = f'{repo_dir}/{name}.part1of2 + .part2of2'
        e['storage'] = {
            'layout': 'part1of2/part2of2 (line-boundary split; repo convention for >1.75 MB certificates)',
            'part1': {'path': f'{repo_dir}/{name}.part1of2', 'bytes': p1.stat().st_size,
                      'md5': hashlib.md5(p1.read_bytes()).hexdigest()},
            'part2': {'path': f'{repo_dir}/{name}.part2of2', 'bytes': p2.stat().st_size,
                      'md5': hashlib.md5(p2.read_bytes()).hexdigest()},
            'concat_md5_equals_whole': True,
        }
    else:
        e['file'] = f'{repo_dir}/{name}'
        e['storage'] = {'layout': 'single file'}
    if (band, bit) in CANON:
        e['file'] = f'{REPO_OUT}/class2-lane-cost71b-certificates/bit1-root-{r["root_hex"]}.cert'
        e['storage'] = {'layout': 'single file (canonical push under cost-71b; see the 71b bit-1 entry)'}
        e['canonical_note'] = CANON[(band, bit)]
    else:
        e['root_absence_check'] = {
            'method': 'GitHub code search over yuubinnkyoku/kyouen-researches for the quoted root '
                      'hex (2026-11-14 UTC, before the certificate push)',
            'repo_search_hits': len(ABSENCE[(band, bit)]),
            'hit_paths': ABSENCE[(band, bit)],
            'prior_certificate_hits': 0,
            'note': 'every hit is a sweep/inflight/audit/recompute record or a log markdown '
                    'listing the root; no certificate file predating this batch contained the '
                    'root hex',
        }
        e['coverage_note'] = NOTES[(band, bit)]
    e['bigint_independent_audit'] = ('WIN7 certificate independently verified by '
                                     'verify_win7_certificate_bigint_independent.mjs (BigInt 3x3 '
                                     'cofactor expansion, no solver/cache/repo-verifier import): '
                                     'root stones=7, rows sorted unique, all sub-roots passed, '
                                     'union 0/0 (per-extraction assert in the pipeline)')
    e['push_note'] = 'full paged-read push; remote md5 verified byte-exact after landing'
    entries.append(e)

manifest = {
    'schema': 'class2-lane-warm-band-hygiene-certificates-v1',
    'generated_utc': '2026-11-14T20:40:00Z',
    'lane': 'class2-lane (11x11 class-2 long-term lane, warm band hygiene batch 2026-11-15)',
    'baseline_frontier': 'class-frontier-warm-multiband-recompute-20261115.json '
                         '(1109 / 6738 / 531295 / 5008 / 395018)',
    'extraction': 'warm_rebuild_pipeline_20261115.py process() (repo-verbatim '
                  'class4_child1_cert_extractor_exact.ts, blind extraction, FBS=1<<20, fbt_drops=0, '
                  'rows LC_ALL=C sorted-unique)',
    'independent_verification': 'scripts/verify_win7_certificate_bigint_independent.mjs run on '
                                'every certificate after extraction; all asserts passed (root '
                                'stones/mobility vs legal_candidates.py, sub_roots==mobility all '
                                'PASS, strategy/consumed union 0/0 both directions, terminal range '
                                'within 13..17, rows sorted strictly ascending unique)',
    'frontier_effect': 'none: marginal=4, mim=0; every root here was already WIN7-anchored by its '
                       'band sweep receipt, so no secured/coverage/frontier number changes; this '
                       'batch closes certificate gaps and resume-priority items only',
    'records': entries,
    'unknown_status': '11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4: '
                      'UNKNOWN. All WIN7 certificates prove only individual 7-stone roots within '
                      'depth 10.',
}
(OUT / 'class2-lane-warm-band-hygiene-certificates-20261115.json').write_text(json.dumps(manifest, indent=1) + '\n')
print('written class2-lane-warm-band-hygiene-certificates-20261115.json with', len(entries), 'records')
for e in entries:
    print(e['band'], e['bit'], e['rows'], e['storage']['layout'], e['md5'])
