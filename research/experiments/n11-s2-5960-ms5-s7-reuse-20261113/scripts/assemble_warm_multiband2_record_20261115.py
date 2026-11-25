#!/usr/bin/env python3
"""Assemble class2-lane-warm-multiband2-certificates-20261115.json from the 31
rebuilt warm records (second warm multiband batch), per-root absence scan
results, and remote storage info (whole vs part1of2/part2of2 layout)."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
WARM = HERE / 'warm'

records = json.loads(Path('/tmp/warm2_records_ordered.json').read_text())
OUT_BASE = ('research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output')

SPLIT = {  # certificates > 1.75 MB (repo convention: line-boundary part split)
    'class2-lane-cost65e-bit120-root-01000000000000809102000000800000',
    'class2-lane-cost71b-bit94-root-00000000400000803202000000400000',
    'class2-lane-cost64b-bit92-root-00000000100000803202000000100000',
    'class2-lane-cost71b-bit74-root-00000000000004803202000000400000',
    'class2-lane-cost64b-bit43-root-00000000000000803202080000100000',
}

entries = []
for e in records:
    key = f"{e['band']}-bit{e['bit']}-root-{e['root_hex']}"
    local = WARM / f'{key}.cert'
    assert hashlib.md5(local.read_bytes()).hexdigest() == e['md5'], key
    repo_dir = f"{OUT_BASE}/{e['band']}-certificates"
    fname = f"bit{e['bit']}-root-{e['root_hex']}.cert"
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
        'method': 'local full-repo rg -F scan of the 3631e7ba main tree (research/ + '
                  'results/ + docs/ + root README + Kyouen/rust/cpp/scripts) for each '
                  'quoted root hex before extraction (2026-11-14 UTC), cross-checked '
                  'against the record-based certified-root set of '
                  'rank_warm_candidates2_20261115.py',
        'repo_scan_hits': 'sweep/inflight/ranking record JSONs only (root listings)',
        'prior_certificate_hits': 0,
        'note': 'no certificate file or certificate record predating this batch '
                'contained any of these 31 root hexes; the 31 roots and their '
                'marginal manifest parents were also cross-checked against the '
                'published LOSS7 evidence (loss7 certificate manifests, loss7 JSON '
                'manifests, 274-key central49 terminal LOSS7 parent-lift manifest): '
                'zero hits, zero WIN/LOSS conflicts',
    }
    entry['pushed'] = '2026-11-15'
    entries.append(entry)

doc = {
    'schema': 'class2-lane-warm-multiband2-certificates-v1',
    'generated_utc': '2026-11-14T20:00:00Z',
    'lane': 'class2-lane (11x11 class-2 long-term lane, warm multiband batch 2, 2026-11-15)',
    'baseline_frontier': 'class-frontier-warm-multiband-recompute-20261115.json (1109 / 6738 / 531295 / 5008 / 395018)',
    'candidate_ranking': 'class2-lane-warm-candidate-ranking2-20261115.json (coordinator v2: marginal_in_manifest greedy over uncertified WIN7 roots of the own-lane bands against the 1109 chain head)',
    'extraction': 'warm_rebuild_pipeline2_20261115.py, two disjoint-target workers (repo-verbatim class4_child1_cert_extractor_exact.ts, blind extraction, FBS=1<<20, fbt_drops=0, rows LC_ALL=C sorted-unique)',
    'independent_verification': 'scripts/verify_win7_certificate_bigint_independent.mjs re-run 2026-11-14 UTC on every certificate after extraction; all asserts passed (root stones/mobility vs legal_candidates.py, sub_roots==mobility all PASS, strategy/consumed union 0/0 both directions, terminal range within 13..17, rows sorted strictly ascending unique)',
    'selection_note': 'the greedy total in-manifest gain over own-lane uncertified roots against 1109 is 37; this batch takes the 31 non-cost-70c gain-1 candidates (cost-70c is a parallel-lane band; its six gain-1 candidates and all gain-0 candidates are deferred). Includes the cost-71b remaining WIN7 bits 74/94/117 (bit 1 = cost-61d bit-22 root has zero in-manifest marginal against 1109 and is deferred). No 65h/67b/68c/65j candidates were touched',
    'records': entries,
}

out = HERE / 'output' / 'class2-lane-warm-multiband2-certificates-20261115.json'
out.write_text(json.dumps(doc, indent=1) + '\n')
print('written', out, out.stat().st_size, 'bytes,', len(entries), 'entries')
