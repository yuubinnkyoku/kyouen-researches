#!/usr/bin/env python3
"""Assemble class2-lane-cost68d-win7-certificates-20261115.json.

Merges the 7 warm/cost68d_records_{a,b}.json entries (extraction + BigInt
independent verification receipts from cost68d_cert_pipeline_20261115.py) with
the v15 cross-engine anchors and the v16 sweep node counts, and records the
pushed storage layout (single file, or part1of2/part2of2 line-boundary split
for >1.75 MB certificates).
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
WARM = HERE / 'warm'
REPO_CERT_DIR = ('research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/'
                 'class2-lane-cost68d-certificates')

records = json.loads((WARM / 'cost68d_records_a.json').read_text()) + \
    json.loads((WARM / 'cost68d_records_b.json').read_text())
assert len(records) == 7 and {r['bit'] for r in records} == {18, 26, 29, 34, 47, 103, 108}

v15 = {}
for line in (OUT / 'class2-lane-cost68d-v15-crosscheck-20261115.jsonl').read_text().splitlines():
    r = json.loads(line)
    if 'bit' in r:
        assert r['loss'] is True and r['capped'] is False
        v15[r['bit']] = r['nodes']
assert set(v15) == {18, 26, 29, 34, 47, 103, 108}

sweep = json.loads((OUT / 'class2-lane-cost68d-sweep-20261115.json').read_text())
v16_nodes = {int(k): v for k, v in sweep['win7_root_nodes'].items()}

certs = []
for r in sorted(records, key=lambda x: x['bit']):
    bit = r['bit']
    name = f"class2-lane-cost68d-bit{bit}-root-{r['root_hex']}.cert"
    whole = WARM / name
    whole_md5 = hashlib.md5(whole.read_bytes()).hexdigest()
    assert whole_md5 == r['md5'], (bit, whole_md5, r['md5'])
    entry = {
        'bit': bit,
        'root_hex': r['root_hex'],
        'verdict': 'WIN7',
        'rows': r['rows'],
        'extraction_nodes': r['extraction_nodes'],
        'extraction': r['extraction'],
        'selection': f"ordered by ascending v16 sweep nodes ({v16_nodes[bit]:,})",
        'rows_sorted_unique': r['rows_sorted_unique'],
        'root_check': r['root_check'],
        'sub_roots_verified': r['sub_roots_verified'],
        'sub_roots_pass': r['sub_roots_pass'],
        'union_missing': r['union_missing'],
        'union_extra': r['union_extra'],
        'terminal_range': r['terminal_range'],
        'visited_states_across_subroots': r['visited_states_across_subroots'],
        'winner_states': r['winner_states'],
        'loser_states': r['loser_states'],
        'loser_reply_edges': r['loser_reply_edges'],
        'terminal_count': r['terminal_count'],
        'md5': r['md5'],
        'sha256': r['sha256'],
        'bytes': r['bytes'],
        'extraction_ms': r['extraction_ms'],
    }
    if r["bytes"] > 1_835_000:
        p1 = WARM / f'{name}.part1of2'
        p2 = WARM / f'{name}.part2of2'
        joined = hashlib.md5((p1.read_bytes() + p2.read_bytes())).hexdigest()
        assert joined == whole_md5, (bit, joined)
        entry['file'] = f'{REPO_CERT_DIR}/{name}.part1of2 + .part2of2'
        entry['storage'] = {
            'layout': 'part1of2/part2of2 (line-boundary split; repo convention for >1.75 MB certificates)',
            'part1': {'path': f'{REPO_CERT_DIR}/{name}.part1of2',
                      'bytes': p1.stat().st_size,
                      'md5': hashlib.md5(p1.read_bytes()).hexdigest()},
            'part2': {'path': f'{REPO_CERT_DIR}/{name}.part2of2',
                      'bytes': p2.stat().st_size,
                      'md5': hashlib.md5(p2.read_bytes()).hexdigest()},
            'concat_md5_equals_whole': True,
        }
    else:
        entry['file'] = f'{REPO_CERT_DIR}/{name}'
        entry['storage'] = {'layout': 'single file'}
    entry['v15_crosscheck_verdict'] = f"loss=true at {v15[bit]:,} nodes (v15 anchor)"
    entry['v16_search_nodes'] = v16_nodes[bit]
    entry['root_not_among_existing'] = True
    entry['root_absence_check'] = ('GitHub code search over yuubinnkyoku/kyouen-researches for the '
                                   'root hex (2026-11-14 UTC, before the certificate push): 0 hits')
    entry['bigint_independent_audit'] = ('WIN7 certificate independently verified by '
                                         'verify_win7_certificate_bigint_independent.mjs (BigInt 3x3 '
                                         'cofactor expansion, no solver/cache/repo-verifier import): '
                                         'root stones=7, rows sorted unique, all sub-roots passed, '
                                         'union 0/0 (per-extraction assert in the pipeline)')
    entry['push_note'] = 'full paged-read push; remote md5 verified byte-exact after landing'
    certs.append(entry)

manifest = {
    'session': 'class2-lane cost-68d WIN7 certificates (long-term lane execution, 2026-11-15 JST)',
    'child_hex': '00000000000000809122000000000000',
    's5_parent_hex': '00000000000000809102000000000000',
    'certificates': certs,
    'v15_crosscheck': {
        'win7_anchors': 'all 7 WIN7 bits loss=true on the v15 runner (class2_child1_runner pilot '
                        'd6 control 5,949 nodes in both invocations; '
                        'class2-lane-cost68d-v15-crosscheck-20261115.jsonl)',
        'refuted_anchors': 'bits 0/120/13 loss=false on the v15 runner, covering the lightest, '
                           'a mid, and the heaviest REFUTED candidate '
                           '(class2-lane-cost68d-v15-refuted-anchor-20261115.jsonl)',
    },
    'pipeline': 'cost68d_cert_pipeline_20261115.py (repo-verbatim warm_rebuild_pipeline process(): '
                'blind extraction, FBS=1<<20, fbt_drops=0, rows LC_ALL=C sorted-unique, BigInt '
                'independent verification with all asserts)',
    'unknown_status': '11x11 empty board: UNKNOWN. All WIN7 certificates prove only individual '
                      '7-stone roots within depth 10.',
}
(OUT / 'class2-lane-cost68d-win7-certificates-20261115.json').write_text(json.dumps(manifest, indent=1) + '\n')
print('written class2-lane-cost68d-win7-certificates-20261115.json with', len(certs), 'certificates')
for c in certs:
    print(c['bit'], c['rows'], c['storage']['layout'], c['md5'])
