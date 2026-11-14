#!/usr/bin/env python3
"""Assemble class2-lane-warm-multiband-certificates-20261115.json from the 35
rebuilt warm records, per-root absence search results, and remote storage info
(whole vs part1of2/part2of2 layout)."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
WARM = HERE / 'warm'

records = json.loads((WARM / 'warm_records_all35.json').read_text())
search = {r['root']: r for r in json.loads(Path('/tmp/wr/search_results.json').read_text())}

OUT_BASE = ('research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output')

SPLIT = {  # band-bit-root -> (whole_md5, part bytes)
    'class2-lane-cost63a-bit2-root-00000000000000809102000800000004': None,
    'class2-lane-cost65e-bit94-root-00000000400000809102000000800000': None,
    'class2-lane-cost65e-bit106-root-00000400000000809102000000800000': None,
    'class2-lane-cost61f-bit102-root-00000040000000803202000080000000': None,
    'class2-lane-cost71b-bit14-root-00000000000000803202000000404000': None,
    'class2-lane-cost65e-bit114-root-00040000000000809102000000800000': None,
    'class2-lane-cost71b-bit32-root-00000000000000803202000100400000': None,
    'class2-lane-cost72-bit52-root-00000000000000803212000000000200': None,
}

entries = []
for e in records:
    key = f"{e['band']}-bit{e['bit']}-root-{e['root_hex']}"
    local = WARM / f'{key}.cert'
    assert hashlib.md5(local.read_bytes()).hexdigest() == e['md5'], key
    repo_dir = f"{OUT_BASE}/{e['band']}-certificates"
    fname = f"bit{e['bit']}-root-{e['root_hex']}.cert"
    s = search[e['root_hex']]
    assert all(('.cert' not in p) or p.endswith(('.json', '.md')) for p in s['paths']), (key, s['paths'])
    entry = dict(e)
    if key in SPLIT:
        p1 = WARM / f'{key}.cert.part1of2'
        p2 = WARM / f'{key}.cert.part2of2'
        md51 = hashlib.md5(p1.read_bytes()).hexdigest()
        md52 = hashlib.md5(p2.read_bytes()).hexdigest()
        assert hashlib.md5(p1.read_bytes() + p2.read_bytes()).hexdigest() == e['md5'], key
        entry['file'] = None
        entry['storage'] = {
            'layout': 'part1of2/part2of2 (line-boundary split; repo convention for >1.75 MB certificates)',
            'part1': {'path': f'{repo_dir}/{fname}.part1of2', 'bytes': p1.stat().st_size, 'md5': md51},
            'part2': {'path': f'{repo_dir}/{fname}.part2of2', 'bytes': p2.stat().st_size, 'md5': md52},
            'concat_md5_equals_whole': True,
        }
    else:
        entry['file'] = f'{repo_dir}/{fname}'
        entry['storage'] = {'layout': 'single file'}
    entry['root_absence_check'] = {
        'method': 'GitHub code search over yuubinnkyoku/kyouen-researches for the quoted root hex (2026-11-14 UTC, immediately after the certificate pushes of this batch; index lag means the new files are not yet searchable)',
        'repo_search_hits': s['n'],
        'hit_paths': s['paths'],
        'prior_certificate_hits': 0,
        'note': 'every hit is a sweep/inflight/audit record JSON or a log markdown listing the root; no certificate file predating this batch contained any of these root hexes',
    }
    entry['pushed'] = '2026-11-15'
    entries.append(entry)

doc = {
    'schema': 'class2-lane-warm-multiband-certificates-v1',
    'generated_utc': '2026-11-14T19:30:00Z',
    'lane': 'class2-lane (11x11 class-2 long-term lane, warm multiband batch 2026-11-15)',
    'baseline_frontier': 'class-frontier-cost75b-recompute-20261115.json (1049 / 6798 / 535812 / 5068 / 399535)',
    'candidate_ranking': 'class2-lane-warm-candidate-ranking-20261115.json (coordinator: marginal_in_manifest greedy over uncertified WIN7 roots, my-lane bands only)',
    'extraction': 'warm_rebuild_pipeline_20261115.py (repo-verbatim class4_child1_cert_extractor_exact.ts, blind extraction, FBS=1<<20, fbt_drops=0, rows LC_ALL=C sorted-unique)',
    'independent_verification': 'scripts/verify_win7_certificate_bigint_independent.mjs re-run 2026-11-14 UTC on every certificate after extraction; all asserts passed (root stones/mobility vs legal_candidates.py, sub_roots==mobility all PASS, strategy/consumed union 0/0 both directions, terminal range within 13..17, rows sorted strictly ascending unique)',
    'selection_note': 'cost72 bit-52 was included because the cost-72 sweep owner explicitly deprioritized it ("only when aiming at additional parent coverage"); no 65h/67b/68c (parallel-lane bands) candidates were touched',
    'records': entries,
}

out = WARM / 'class2-lane-warm-multiband-certificates-20261115.json'
out.write_text(json.dumps(doc, indent=1) + '\n')
print('written', out, out.stat().st_size, 'bytes,', len(entries), 'entries')
