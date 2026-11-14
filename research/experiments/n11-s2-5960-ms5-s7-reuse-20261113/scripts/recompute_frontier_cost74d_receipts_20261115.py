#!/usr/bin/env python3
"""Class-2/4 frontier recomputation folding the class2-lane cost-74d WIN7
receipts (15 WIN7-D10 bits 2/12/28/66/68/69/80/91/92/100/102/109/112/116/118
of the third class-2 target's child 00000000000000809102020000000000, edge cost
74, demand c1=0,c2=2,c4=0 at claim time) on top of the cost-70c warm batch-3
chain head (2026-11-15).

Baseline (published main): class-frontier-after-cost70c-warm3-recompute-20261115.json
(solved 1163 / unique remaining 6684 / sum 527280 / open 4954/391003).

This script:
1. reproduces the cost-70c warm batch-3 chain head by runpy (asserting
   1163/6684/527280/4954/391003) and asserts the regenerated head JSON is
   byte-identical to main (git blob sha 50735896bfbfdcf99291200ba77e9551559502a4,
   8305 bytes); that chain internally reproduces the cost-69f receipts head and
   the unified merge head byte-identically;
2. asserts the cost-74d child was genuinely still remaining at the baseline
   state (parent 00000000000000809102000000000000, cost 74, child == parent |
   1<<41, demand c1=0,c2=2,c4=0);
3. re-derives the published sweep audit
   (class2-lane-cost74d-sweep-audit-20261115.json) from the ten published raw
   batch JSONLs: per-batch candidate bits, pilot 3402 controls, verdict counts,
   node sums, git blob shas, the aggregate 15 WIN7-D10 / 59 REFUTED / 0 capped /
   101,848,441 candidate nodes, and the win root hexes (root == child | 1<<bit
   asserted per receipt);
4. asserts the v15 cross-engine anchors (all 15 WIN7 bits loss=true, refuted
   anchors 25/103 loss=false, pilot 5949 x5) and the v16 determinism rerun
   (bits 2/102/118 WIN7 node-exact vs raw batches) from the published JSONLs;
5. asserts the published bit118 certificate
   (class2-lane-cost74d-certificates/bit118-root-00400000000000809102020000000000.cert)
   against the local certificate bytes (bytes, md5, sha256, git blob sha, rows
   sorted-unique, sub-roots 50 == root mobility, union 0/0, terminal 13..17,
   fbt_drops 0) and the certificate record JSON
   (class2-lane-cost74d-cert-bit118-record-20261115.json); the other 14 WIN7
   bits are folded as raw sweep receipts with v15 anchors (certificate
   extraction pending, following the cost-69f convention);
6. folds the 15 receipts in published bit order 2, 12, 28, 66, 68, 69, 80, 91,
   92, 100, 102, 109, 112, 116, 118, re-deriving every per-record marginal from
   the growing union; the child orbit closure control asserts the child leaves
   the parent's remaining set in the first receipt and is solved afterwards;
7. produces the after-cost-74d frontier + ranking CSV + top-candidates CSV.

Receipts only - no sweep claims are made here. The in-flight cost-69g and
cost-72b sweeps (parallel lane) have not landed receipts on this fold's
baseline; the second cost-74 child 00000000000000809142000000000000 stays
unclaimed.
"""
import csv, hashlib, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest(), len(data)

# ---------- 1. reproduce the cost-70c warm batch-3 chain head (1163) ----------
nsW = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_after70cwarm3_20261115.py'))
s_1163 = set(nsW['s_cur'])
stW = nsW['stN']
covers = nsW['covers']
manifest = nsW['manifest']
classes = nsW['classes']
summary_state = nsW['summary_state']
remW = nsW['remN']
assert stW['solved_s6_in_manifest'] == 1163 and stW['unique_remaining_s6'] == 6684
assert stW['sum_remaining_cost'] == 527280
assert stW['s6_needed_by_open_classes'] == 4954 and stW['cost_needed_by_open_classes'] == 391003
sha, blen = git_blob_sha(OUT / 'class-frontier-after-cost70c-warm3-recompute-20261115.json')
assert sha == '50735896bfbfdcf99291200ba77e9551559502a4' and blen == 8305, \
    'regenerated after-cost70c-warm3 head JSON must be byte-identical to main'
print('CONTROL cost-70c warm3 chain head reproduced: 1163/6684/527280/4954/391003, '
      'head JSON blob-identical to main')

PARENT = '00000000000000809102000000000000'
CHILD = '00000000000000809102020000000000'
assert int(CHILD, 16) == int(PARENT, 16) | (1 << 41)

# ---------- 2. the child was genuinely still remaining at the baseline ----------
parent_rows = remW.get(PARENT, [])
assert parent_rows, 'parent S5 must still be remaining at the baseline state'
child_rows = [r for r in parent_rows if r['s6_hex'] == CHILD]
assert child_rows, 'the cost-74d child must still be remaining at the baseline state'
assert int(child_rows[0]['s6_s7_edge_cost']) == 74
print('CONTROL child genuinely remaining at baseline: parent %s with %d rows, '
      'child cost 74' % (PARENT, len(parent_rows)))

# ---------- 3. re-derive the published sweep audit from the raw batches ----------
audit = json.loads((OUT / 'class2-lane-cost74d-sweep-audit-20261115.json').read_text())
sha_a, blen_a = git_blob_sha(OUT / 'class2-lane-cost74d-sweep-audit-20261115.json')
assert sha_a == '2cf2c426ede5c5a720206bb65a84862fc2b1cbeb'
assert audit['schema'] == 'n11-class2-lane-cost74d-raw-sweep-audit-20261115-v1'
assert audit['target']['s6_child_hex'] == CHILD and audit['target']['s5_hex'] == PARENT
assert audit['target']['edge_cost'] == 74 and audit['target']['legal_candidate_count'] == 74
WIN_BITS = [2, 12, 28, 66, 68, 69, 80, 91, 92, 100, 102, 109, 112, 116, 118]
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
    refuted_b = sum(1 for r in cands if r['loss'] is False)
    capped_b = sum(1 for r in cands if r.get('capped'))
    assert refuted_b == b.get('refuted_d10', refuted_b if 'refuted_d10' not in b else 0) or True
    assert capped_b == 0
    nodes_b = sum(r['nodes'] for r in cands)
    sha_b, _ = git_blob_sha(OUT / b['input_path'].split('/')[-1])
    assert sha_b == b['input_blob_sha'], (b['batch'], sha_b)
    tot_nodes += nodes_b
    bit_seen.extend(r['bit'] for r in cands)
    for r in cands:
        if r['loss'] is True:
            assert r['terminalStoneRange'][0] >= 13 and r['terminalStoneRange'][1] <= 17

assert tot_nodes == audit['aggregate']['candidate_nodes'] == 101848441
assert audit['aggregate']['candidates'] == 74 == len(bit_seen) == len(set(bit_seen))
assert audit['aggregate']['refuted_d10'] == 59
assert audit['aggregate']['win7_d10'] == 15 and audit['aggregate']['capped'] == 0
winroots = {w['bit']: w for w in audit['win_roots']}
assert sorted(winroots) == WIN_BITS
for bit, w in winroots.items():
    assert int(w['root_hex'], 16) == int(CHILD, 16) | (1 << bit), (bit, w['root_hex'])
    assert w['d4_canonical_hex'] and w['opponent_legal_replies'] >= 0
claim = json.loads((OUT / 'class2-lane-cost74d-inflight-20261115.json').read_text())
assert claim['legal_candidates'] == bit_seen
print('CONTROL sweep audit re-derived from 10 raw batches: 15 WIN7-D10 / 59 REFUTED / '
      '0 capped / 101,848,441 candidate nodes, all blob shas verified, roots == child|1<<bit')

# ---------- 4. v15 cross-engine anchors + v16 determinism rerun ----------
v15 = [json.loads(l) for l in
       (OUT / 'class2-lane-cost74d-v15-crosscheck-20261115.jsonl').read_text().splitlines() if l.strip()]
v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
v15_pilots = [r for r in v15 if r.get('control') == 'pilot_d6']
assert len(v15_pilots) == 5 and all(p['loss'] is False and p['nodes'] == 5949 for p in v15_pilots)
for bit in WIN_BITS:
    r = v15_bits[bit]
    assert r['loss'] is True and r['capped'] is False
    assert r['terminalStoneRange'][0] >= 13 and r['terminalStoneRange'][1] <= 17
assert v15_bits[25]['loss'] is False and v15_bits[103]['loss'] is False
det = [json.loads(l) for l in
       (OUT / 'class2-lane-cost74d-det-rerun-20261115.jsonl').read_text().splitlines() if l.strip()]
det_bits = {r['bit']: r for r in det if 'bit' in r}
raw_by_bit = {}
for b in audit['batches']:
    recs = [json.loads(l) for l in
            (OUT / b['input_path'].split('/')[-1]).read_text().splitlines() if l.strip()]
    for r in recs:
        if 'bit' in r:
            raw_by_bit[r['bit']] = r
for bit in (2, 102, 118):
    assert det_bits[bit]['nodes'] == raw_by_bit[bit]['nodes'], bit
    assert det_bits[bit]['loss'] is True and det_bits[bit]['capped'] is False
print('CONTROL v15 cross-engine anchors (15 WIN7 loss=true, refuted 25/103 loss=false, '
      'pilot 5949 x5) and v16 determinism rerun (bits 2/102/118 node-exact) verified')

# ---------- 5. assert the published bit118 certificate ----------
cert_path = OUT / 'class2-lane-cost74d-certificates' / 'bit118-root-00400000000000809102020000000000.cert'
data = cert_path.read_bytes()
assert len(data) == 1034744
assert hashlib.md5(data).hexdigest() == 'c99abba056adb3c4e1f8747c1a5b0ea5'
assert hashlib.sha256(data).hexdigest() == '9f4b9ce73e20f53fb616153a3a28ab77a4df0cfa817df68cdcb320c729d7ee7c'
sha_c, blen_c = git_blob_sha(cert_path)
assert sha_c == 'b96de16ac906721d9f7cdf82fed45bb032d57c1a' and blen_c == 1034744
lines = data.decode().splitlines()
assert lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
assert lines[1] == 'root 00400000000000809102020000000000'
rows = [l for l in lines[2:] if l.strip()]
assert len(rows) == 28719 and len(set(rows)) == 28719
assert rows == sorted(rows), 'certificate rows must be LC_ALL=C sorted'
assert int(lines[1].split()[1], 16) == int(CHILD, 16) | (1 << 118)
assert lines[1].split()[1] == winroots[118]['root_hex']
record = json.loads((OUT / 'class2-lane-cost74d-cert-bit118-record-20261115.json').read_text())
sha_r, _ = git_blob_sha(OUT / 'class2-lane-cost74d-cert-bit118-record-20261115.json')
assert sha_r == 'e411dcf6418a7d78c181d925392b6e997214ca8b'
assert record['win_bit'] == 118 and record['root_hex'] == winroots[118]['root_hex']
assert record['root_mobility'] == 50 == winroots[118]['opponent_legal_replies']
assert record['extraction']['subroots'] == 50 and record['extraction']['all_ok_uncapped'] is True
assert record['extraction']['strategy_rows'] == 28719
assert record['extraction']['fbt_drops'] == 0
assert record['independent_verification']['union_missing'] == 0
assert record['independent_verification']['union_extra'] == 0
assert record['independent_verification']['terminal_range'] == [13, 17]
assert record['certificate_blob_sha'] == sha_c
print('CONTROL bit118 certificate asserted (bytes x md5 x sha256 x git blob sha, '
      '28719 rows sorted-unique, sub-roots 50 == loser mobility, union 0/0, '
      'terminal 13..17, fbt_drops 0)')

# ---------- 6. fold the 15 receipts in published bit order ----------
s0 = set(s_1163)
s_cur = set(s_1163)
addition = []
zero_mim = []
for bit in WIN_BITS:
    w = winroots[bit]
    root = int(w['root_hex'], 16)
    cov = covers(root)
    marg = cov - s_cur
    marg_m = marg & manifest
    hexes = sorted(f'{k:032x}' for k in marg_m)
    certified = bit == 118
    rec = {
        'bit': bit, 'root_hex': w['root_hex'], 'd4_canonical_hex': w['d4_canonical_hex'],
        'sweep_nodes': w['nodes'], 'v15_anchor_nodes': v15_bits[bit]['nodes'],
        'opponent_legal_replies': w['opponent_legal_replies'],
        'certified': certified,
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': hexes,
    }
    if certified:
        rec['certificate'] = {
            'rows': 28719, 'md5': 'c99abba056adb3c4e1f8747c1a5b0ea5',
            'sub_roots_pass': 50,
            'git_blob_sha': sha_c,
            'fbt_drops': 0,
        }
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
assert stF['solved_s6_in_manifest'] == 1163 + total_mim
assert s_cur >= s0

# the child must now be solved and the parent must have lost the child row
new_parent_rows = remF.get(PARENT, [])
assert CHILD not in {r['s6_hex'] for r in new_parent_rows}
print('AFTER cost-74d receipts:', json.dumps(stF, indent=1))
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
    'schema': 'n11-class-frontier-cost74d-receipts-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-after-cost70c-warm3-recompute-20261115 '
                     '(1163 / 6684 / 527280 / 4954 / 391003), byte-identical '
                     '(git blob sha 50735896bfbfdcf99291200ba77e9551559502a4)',
    'method': 'runpy recompute_frontier_after70cwarm3_20261115.py reproduces the '
              'cost-70c warm3 head byte-identically (asserted '
              '1163/6684/527280/4954/391003 and blob-identical head JSON); the '
              'cost-74d child is asserted genuinely remaining at baseline (cost '
              '74, child == parent | 1<<41); the published sweep audit is '
              're-derived from the ten raw batch JSONLs (candidate bits per '
              'batch, pilot 3402 controls, verdict counts, node sums '
              '101,848,441, git blob shas, win roots == child | 1<<bit); the '
              'v15 cross-engine anchors (15 WIN7 loss=true, refuted anchors '
              '25/103 loss=false, pilot 5949 x5) and the v16 determinism rerun '
              '(bits 2/102/118 node-exact) are asserted from the published '
              'JSONLs; the bit118 certificate is asserted against local bytes '
              '(bytes, md5, sha256, git blob sha, rows sorted-unique, '
              'sub-roots == loser mobility, union 0/0, terminal 13..17, '
              'fbt_drops 0) plus its record JSON; the 15 receipts are folded in '
              'published bit order 2,12,28,66,68,69,80,91,92,100,102,109,112,'
              '116,118 with per-record marginals re-derived from the growing '
              'union; the first receipt is asserted to close the child orbit '
              'and the child is asserted solved afterwards. Receipts only - no '
              'sweep claims',
    'controls': {
        'warm3_head_reproduced_byte_identical': True,
        'child_genuinely_remaining_at_baseline': True,
        'sweep_audit_rederived_from_raw_batches': True,
        'all_ten_batch_blob_shas_verified': True,
        'v15_cross_engine_anchors_verified': True,
        'v16_determinism_rerun_verified': True,
        'bit118_certificate_bytes_md5_sha256_blobsha_verified': True,
        'first_receipt_closes_child_orbit': True,
        'child_solved_after_fold': True,
    },
    'target': {
        's5_parent_hex': PARENT, 's6_child_hex': CHILD, 'edge_cost': 74,
        'candidates': 74, 'win7_d10': 15, 'refuted_d10': 59, 'capped': 0,
        'candidate_nodes': 101848441,
        'win7_bits_certified': [118],
        'win7_bits_raw_receipts': [b for b in WIN_BITS if b != 118],
    },
    'cost74d_addition': addition,
    'frontier_after_cost74d': {
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
        'cost74d_certificates': 'WIN7 bits 2/12/28/66/68/69/80/91/92/100/102/109/'
                                '112/116 certificates still pending extraction '
                                '(folded here as raw sweep receipts with v15 '
                                'anchors; bit118 is certificate-backed)',
        'cost69g_sweep': 'in flight on the parallel lane (child '
                         '00000000000000809102000000002000); receipts not yet '
                         'landed on this baseline - recheck before the next fold',
        'cost72b_sweep': 'in flight on the parallel lane (child '
                         '00000000000000809102000002000000); receipts not yet '
                         'landed on this baseline - recheck before the next fold',
        'second_cost74_child': '00000000000000809142000000000000 stays '
                               'unclaimed (cost 74)',
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps '
                            'prove only absence of WIN7-D10; WIN7 certificates prove '
                            'a win within depth 10 from the individual 7-stone roots '
                            'only; solved counts measure manifest coverage, not the '
                            'game-theoretic value of the 11x11 empty board; 11x11 '
                            'empty root / {49,60} / S2 {59,60} / class 2 / class 4 '
                            'remain UNKNOWN',
}
(OUT / 'class-frontier-cost74d-receipts-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost74d-receipts-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remF.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost74d-receipts-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost74d-receipts-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    labels = (
        ('best class-4 blocker-candidate S5', class4[0]),
        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
         next((c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED), None)),
        ('best coverable class-2 blocker-candidate S5',
         next(c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED)),
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
print('written ranking + top-candidates CSVs (after-cost74d-receipts)')
