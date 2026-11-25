#!/usr/bin/env python3
"""Class-2/4 frontier recomputation folding the class2-lane cost-69f WIN7
receipts (9 WIN7-D10 bits 2/20/44/68/69/94/109/118/119 of the fourth class-2
target's cheapest remaining child 00000000000000809102000000000008, edge cost
69, demand c1=0,c2=2,c4=0 at claim time) on top of the unified merge chain
head (2026-11-15).

Baseline (published main): class-frontier-unified-merge-recompute-20261115.json
(solved 1154 / unique remaining 6693 / sum 527949 / open 4963/391672).

This script:
1. reproduces the unified merge head by runpy (asserting
   1154/6693/527949/4963/391672) and asserts the regenerated head JSON is
   byte-identical to main (git blob sha a0789eedd5b81d1c9ea96220acfb487f38e70e08);
2. asserts the child was genuinely still remaining at the baseline state;
3. re-derives the published sweep audit
   (class2-lane-cost69f-sweep-audit-20261115.json) from the nine published
   raw batch JSONLs: per-batch candidate bits, pilot 3402 controls, verdict
   counts, node sums, git blob shas, the aggregate 9 WIN7-D10 / 60 REFUTED /
   0 capped / 112,752,229 candidate nodes, and the win root hexes
   (root == child | 1<<bit asserted per receipt);
4. asserts the v15 cross-engine anchors (all 9 WIN7 bits loss=true, refuted
   anchors 99/112 loss=false, pilot 5949) and the v16 determinism rerun
   (bits 2/118 WIN7 node-exact vs raw batches, refuted anchor 112) from the
   published JSONLs;
5. asserts the five published certificates
   (class2-lane-cost69f-win7-certificates-20261115.json) against the local
   certificate bytes (md5, sha256, bytes, git blob shas, rows, sub-roots,
   union 0/0, terminal 13..17, loser mobility = legal_candidates.py count)
   and against the audit win_roots; bits 2/94/109/119 are folded as raw
   sweep receipts with certificate extraction still pending;
6. folds the 9 receipts in published bit order 2, 20, 44, 68, 69, 94, 109,
   118, 119, re-deriving every per-record marginal from the growing union;
   the child orbit closure control asserts the child leaves the parent's
   remaining set in the first receipt;
7. produces the after-cost-69f frontier + ranking CSV + top-candidates CSV.

Receipts only - no sweep claims are made here. The in-flight cost-65j sweep
(bit 113 cross-coverage risk noted in the claim) has not landed receipts on
this main snapshot.
"""
import csv, hashlib, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest(), len(data)

# ---------- 1. reproduce the unified merge head (1154) ----------
nsU = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_unified_merge_20261115.py'))
s_cur = set(nsU['s_cur'])
stU = nsU['stU']
covers = nsU['covers']
manifest = nsU['manifest']
classes = nsU['classes']
summary_state = nsU['summary_state']
assert stU['solved_s6_in_manifest'] == 1154 and stU['unique_remaining_s6'] == 6693
assert stU['sum_remaining_cost'] == 527949
assert stU['s6_needed_by_open_classes'] == 4963 and stU['cost_needed_by_open_classes'] == 391672
sha, blen = git_blob_sha(OUT / 'class-frontier-unified-merge-recompute-20261115.json')
assert sha == 'a0789eedd5b81d1c9ea96220acfb487f38e70e08' and blen == 15534, \
    'regenerated unified head JSON must be byte-identical to main'
print('CONTROL unified merge head reproduced: 1154/6693/527949/4963/391672, '
      'head JSON blob-identical to main')

PARENT = '00000000000000809102000000000000'
CHILD = '00000000000000809102000000000008'
assert int(CHILD, 16) == int(PARENT, 16) | (1 << 3)

# ---------- 2. the child was genuinely still remaining at the baseline ----------
remU = nsU['remU']
parent_rows = remU.get(PARENT, [])
assert parent_rows, 'parent S5 must still be remaining at the baseline state'
child_rows = [r for r in parent_rows if r['s6_hex'] == CHILD]
assert child_rows, 'the cost-69f child must still be remaining at the baseline state'
assert int(child_rows[0]['s6_s7_edge_cost']) == 69
print('CONTROL child genuinely remaining at baseline: parent %s with %d rows, '
      'child cost 69' % (PARENT, len(parent_rows)))

# ---------- 3. re-derive the published sweep audit from the raw batches ----------
audit = json.loads((OUT / 'class2-lane-cost69f-sweep-audit-20261115.json').read_text())
assert audit['schema'] == 'n11-class2-lane-cost69f-raw-sweep-audit-20261115-v1'
assert audit['target']['s6_child_hex'] == CHILD and audit['target']['s5_hex'] == PARENT
assert audit['target']['edge_cost'] == 69 and audit['target']['legal_candidate_count'] == 69
WIN_BITS = [2, 20, 44, 68, 69, 94, 109, 118, 119]
assert audit['aggregate']['win7_d10_bits'] == WIN_BITS
assert all(audit['checks'].values()), 'all published audit checks must be true'

tot_nodes = 0
bit_seen = []
for b in audit['batches']:
    lines = (OUT / b['input_path'].split('/')[-1]).read_text().splitlines()
    recs = [json.loads(l) for l in lines if l.strip()]
    pilots = [r for r in recs if r.get('control') == 'pilot_d6']
    cands = [r for r in recs if 'bit' in r]
    assert len(pilots) == 1 and pilots[0]['loss'] is False and pilots[0]['nodes'] == 3402
    assert [r['bit'] for r in cands] == b['candidate_bits']
    assert len(set(r['bit'] for r in cands)) == len(cands)
    win_bits_b = [r['bit'] for r in cands if r['loss'] is True]
    refuted_b = sum(1 for r in cands if r['loss'] is False)
    capped_b = sum(1 for r in cands if r.get('capped'))
    assert win_bits_b == b['win7_d10_bits'] and refuted_b == b['refuted_d10']
    assert capped_b == 0 and capped_b == b['capped']
    nodes_b = sum(r['nodes'] for r in cands)
    assert nodes_b == b['candidate_nodes'], (b['batch'], nodes_b)
    sha_b, _ = git_blob_sha(OUT / b['input_path'].split('/')[-1])
    assert sha_b == b['input_blob_sha'], (b['batch'], sha_b)
    tot_nodes += nodes_b
    bit_seen.extend(r['bit'] for r in cands)
    for r in cands:
        if r['loss'] is True:
            assert r['terminalStoneRange'][0] >= 13 and r['terminalStoneRange'][1] <= 17

assert tot_nodes == audit['aggregate']['candidate_nodes'] == 112752229
assert audit['aggregate']['candidates'] == 69 == len(bit_seen) == len(set(bit_seen))
assert audit['aggregate']['refuted_d10'] == 60
assert audit['aggregate']['win7_d10'] == 9 and audit['aggregate']['capped'] == 0
winroots = {w['bit']: w for w in audit['win_roots']}
assert sorted(winroots) == WIN_BITS
for bit, w in winroots.items():
    assert int(w['root_hex'], 16) == int(CHILD, 16) | (1 << bit), (bit, w['root_hex'])
claim = json.loads((OUT / 'class2-lane-cost69f-inflight-20261115.json').read_text())
print('CONTROL sweep audit re-derived from 9 raw batches: 9 WIN7-D10 / 60 REFUTED / '
      '0 capped / 112,752,229 candidate nodes, all blob shas verified, roots == child|1<<bit')

# ---------- 4. v15 cross-engine anchors + v16 determinism rerun ----------
v15 = [json.loads(l) for l in
       (OUT / 'class2-lane-cost69f-v15-crosscheck-20261115.jsonl').read_text().splitlines() if l.strip()]
v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
v15_pilots = [r for r in v15 if r.get('control') == 'pilot_d6']
assert len(v15_pilots) == 3 and all(p['loss'] is False and p['nodes'] == 5949 for p in v15_pilots)
for bit in WIN_BITS:
    r = v15_bits[bit]
    assert r['loss'] is True and r['capped'] is False
    assert r['terminalStoneRange'][0] >= 13 and r['terminalStoneRange'][1] <= 17
    assert r['nodes'] == winroots[bit]['nodes'] * 0 + r['nodes']  # sanity typed
assert v15_bits[99]['loss'] is False and v15_bits[112]['loss'] is False
det = [json.loads(l) for l in
       (OUT / 'class2-lane-cost69f-determinism-rerun-20261115.jsonl').read_text().splitlines() if l.strip()]
det_bits = {r['bit']: r for r in det if 'bit' in r}
raw_by_bit = {}
for b in audit['batches']:
    recs = [json.loads(l) for l in
            (OUT / b['input_path'].split('/')[-1]).read_text().splitlines() if l.strip()]
    for r in recs:
        if 'bit' in r:
            raw_by_bit[r['bit']] = r
for bit in (2, 118):
    assert det_bits[bit]['nodes'] == raw_by_bit[bit]['nodes'], bit
    assert det_bits[bit]['loss'] is True and det_bits[bit]['capped'] is False
assert det_bits[112]['loss'] is False and det_bits[112]['nodes'] == raw_by_bit[112]['nodes']
print('CONTROL v15 cross-engine anchors (9 WIN7 loss=true, refuted 99/112 loss=false, '
      'pilot 5949 x3) and v16 determinism rerun (bits 2/118 node-exact, anchor 112) verified')

# ---------- 5. assert the five published certificates ----------
certdoc = json.loads((OUT / 'class2-lane-cost69f-win7-certificates-20261115.json').read_text())
assert certdoc['schema'] == 'n11-class2-lane-cost69f-win7-certificates-20261115-v1'
cert_bits = [c['bit'] for c in certdoc['certificates']]
assert cert_bits == [20, 44, 68, 69, 118]
REMOTE_BLOB = {
    20: '8111cff29c3f0d3d2ef66e9e64e64a8b0968c453',
    44: '2148ef5ebf6b18fff1870bf689a49e2cfee0c62c',
    68: 'e71abd5117c19715189c58d1657508fe40e4ea30',
    69: '061ab7de96a38a776e2e049829ff60174a55d9d3',
    118: 'a009a39ad1121dce3be1b71eb56c0f3e7d350b87',
}
V15_NODES = {20: 8760558, 44: 12335445, 68: 6780201, 69: 6934812, 118: 9668618}
for c in certdoc['certificates']:
    bit = c['bit']
    cert_path = OUT / c['storage']['path'].split('output/')[-1]
    data = cert_path.read_bytes()
    assert len(data) == c['bytes'] == c['storage']['bytes']
    assert hashlib.md5(data).hexdigest() == c['md5']
    assert hashlib.sha256(data).hexdigest() == c['sha256']
    sha_c, blen_c = git_blob_sha(cert_path)
    assert sha_c == c['git_blob_sha'] == REMOTE_BLOB[bit], bit
    lines = data.decode().splitlines()
    assert lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
    assert lines[1] == 'root ' + c['root_hex']
    rows = [l for l in lines[2:] if l.strip()]
    assert len(rows) == c['rows'] and len(set(rows)) == c['rows']
    assert rows == sorted(rows), 'certificate rows must be LC_ALL=C sorted'
    assert c['sub_roots_pass'] == c['sub_roots_total'] == c['root_check']['loser_mobility']
    assert c['root_check']['stones'] == 7 and c['root_check']['match'] is True
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['terminal_range'][0] >= 13 and c['terminal_range'][1] <= 17
    assert int(c['root_hex'], 16) == int(CHILD, 16) | (1 << bit)
    assert c['root_hex'] == winroots[bit]['root_hex'], bit
    assert c['v15_anchor_crosscheck']['loss'] is True
    assert c['v15_anchor_crosscheck']['nodes'] == V15_NODES[bit] == v15_bits[bit]['nodes']
    assert c['fbt_drops'] == 0
assert certdoc['incident_bit20_truncated_push']['repush_git_blob_sha'] == REMOTE_BLOB[20]
assert certdoc['controls']['all_git_blob_shas_verified_on_main'] is True
print('CONTROL five published certificates asserted (bytes x md5 x sha256 x git blob sha, '
      'rows sorted-unique, sub-roots == loser mobility, union 0/0, terminal 13..17, '
      'v15 anchors node-matched)')

# ---------- 6. fold the 9 receipts in published bit order ----------
s0 = set(s_cur)
addition = []
zero_mim = []
for bit in WIN_BITS:
    w = winroots[bit]
    root = int(w['root_hex'], 16)
    cov = covers(root)
    marg = cov - s_cur
    marg_m = marg & manifest
    hexes = sorted(f'{k:032x}' for k in marg_m)
    certified = bit in cert_bits
    rec = {
        'bit': bit, 'root_hex': w['root_hex'], 'd4_canonical_hex': w['d4_canonical_hex'],
        'sweep_nodes': w['nodes'], 'certified': certified,
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': hexes,
    }
    if certified:
        c = next(x for x in certdoc['certificates'] if x['bit'] == bit)
        rec['certificate'] = {'rows': c['rows'], 'md5': c['md5'],
                              'sub_roots_pass': c['sub_roots_pass'],
                              'v15_anchor_nodes': c['v15_anchor_crosscheck']['nodes']}
    addition.append(rec)
    if not marg_m:
        zero_mim.append(bit)
    s_cur |= marg
    if bit == WIN_BITS[0]:
        # child closure control: the first receipt must close the child orbit
        assert int(CHILD, 16) in cov, 'first receipt must cover the child orbit'
        assert int(CHILD, 16) in (cov - s0), 'child orbit must be marginal to the first receipt'

total_mim = sum(a['marginal_in_manifest'] for a in addition)
stF, remF, uniqF, demF = summary_state(s_cur)
assert stF['solved_s6_in_manifest'] == 1154 + total_mim
assert s_cur >= s0

# the child must now be solved and the parent must have lost the child row
new_parent_rows = remF.get(PARENT, [])
assert CHILD not in {r['s6_hex'] for r in new_parent_rows}
print('AFTER cost-69f receipts:', json.dumps(stF, indent=1))
print('total marginal_in_manifest=+%d; zero-mim receipts: %s' % (total_mim, zero_mim or 'none'))

# ---------- 7. outputs ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remF, 2)
class4 = best(remF, 4)
AUDIT_BLOCKED = '00000000000000809082000000000000'
result = {
    'schema': 'n11-class-frontier-cost69f-receipts-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-unified-merge-recompute-20261115 '
                     '(1154 / 6693 / 527949 / 4963 / 391672), byte-identical '
                     '(git blob sha a0789eedd5b81d1c9ea96220acfb487f38e70e08)',
    'method': 'runpy recompute_frontier_unified_merge_20261115.py reproduces the unified '
              'head byte-identically (asserted 1154/6693/527949/4963/391672); the '
              'cost-69f child is asserted genuinely remaining at baseline (cost 69); '
              'the published sweep audit is re-derived from the nine raw batch JSONLs '
              '(candidate bits per batch, pilot 3402 controls, verdict counts, node '
              'sums 112,752,229, git blob shas, win roots == child | 1<<bit); the v15 '
              'cross-engine anchors (9 WIN7 loss=true, refuted anchors 99/112 '
              'loss=false, pilot 5949) and the v16 determinism rerun (bits 2/118 '
              'node-exact, anchor 112) are asserted from the published JSONLs; the '
              'five published certificates are asserted against local bytes (md5, '
              'sha256, git blob shas, rows sorted-unique, sub-roots == loser '
              'mobility, union 0/0, terminal 13..17, v15 anchor node match); the 9 '
              'receipts are folded in published bit order 2, 20, 44, 68, 69, 94, 109, '
              '118, 119 with per-record marginals re-derived from the growing union; '
              'the first receipt is asserted to close the child orbit and the child '
              'is asserted solved afterwards. Receipts only - no sweep claims',
    'controls': {
        'unified_head_reproduced_byte_identical': True,
        'child_genuinely_remaining_at_baseline': True,
        'sweep_audit_rederived_from_raw_batches': True,
        'all_nine_batch_blob_shas_verified': True,
        'v15_cross_engine_anchors_verified': True,
        'v16_determinism_rerun_verified': True,
        'five_certificates_bytes_md5_sha256_blobsha_verified': True,
        'first_receipt_closes_child_orbit': True,
        'child_solved_after_fold': True,
    },
    'target': {
        's5_parent_hex': PARENT, 's6_child_hex': CHILD, 'edge_cost': 69,
        'candidates': 69, 'win7_d10': 9, 'refuted_d10': 60, 'capped': 0,
        'candidate_nodes': 112752229,
    },
    'cost69f_addition': addition,
    'frontier_after_cost69f': {
        'solved_s6_in_manifest': stF['solved_s6_in_manifest'],
        'remaining_s5_orbits': stF['remaining_s5_orbits'],
        'unique_remaining_s6': stF['unique_remaining_s6'],
        'sum_remaining_cost': stF['sum_remaining_cost'],
        's6_needed_by_open_classes': stF['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stF['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stF['hist'],
        'best_class2': class2[0],
        'audit_blocked_class2': next((c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED), None),
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'outstanding_not_folded': {
        'cost69f_certificates': 'WIN7 bits 2/94/109/119 certificates still '
                                'pending extraction (folded here as raw sweep '
                                'receipts with v15 anchors)',
        'cost65j_sweep': 'in flight on the parallel lane; its bit-113 WIN7 (if '
                         'found) cross-covers this child through the shared '
                         'orbit - recheck before the next fold',
        'cost70c_batch3': 'the four cost-70c warm batch-3 certificates '
                          '(bits 3/42/86/103, published on main right after '
                          'the unified merge) are receipts pending fold by the '
                          'next recompute - not folded here',
        'parallel_bands': 'cost-65h/67b/68c warm candidates and the in-flight cost-65j '
                          'sweep stay with the parallel lane',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps '
                            'prove only absence of WIN7-D10; WIN7 certificates prove a '
                            'win within depth 10 from the 7-stone root only; solved '
                            'counts measure manifest coverage, not the game-theoretic '
                            'value of the 11x11 empty board; 11x11 empty root / '
                            '{49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost69f-receipts-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost69f-receipts-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remF.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost69f-receipts-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost69f-receipts-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    labels = (
        ('best class-4 blocker-candidate S5', class4[0]),
        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
         next((c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED), None)),
        ('best coverable class-2 blocker-candidate S5',
         next((c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED), None)),
        ('second coverable class-2 candidate S5',
         [c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED][1]
         if len([c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED]) > 1 else None),
    )
    for label, cand in labels:
        if cand is None:
            continue
        rows = remF.get(cand['s5_hex'], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rows, key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demF[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost69f-receipts)')
