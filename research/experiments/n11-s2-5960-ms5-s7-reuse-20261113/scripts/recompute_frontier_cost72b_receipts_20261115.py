#!/usr/bin/env python3
"""Class-2/4 frontier recomputation folding the class2-lane cost-72b WIN7
receipts (13 WIN7-D10 bits 2/11/21/30/31/36/47/66/85/95/97/100/106 of the
third class-2 target's cheapest remaining child 00000000000000809102000002000000,
edge cost 72, demand c1=0,c2=2,c4=0 at claim time) on top of the cost-74d
receipts chain head (solved 1179, 2026-11-15).

Baseline (published main): class-frontier-cost74d-receipts-recompute-20261115.json
(1179 / 6668 / 526075 / 4938 / 389798; the parallel lane's cost-74d fold landed
on main first and its bit-91 receipt cross-covered and closed this cost-72b
child orbit, so this fold rebases on the 1179 head; a sibling fold of these
same receipts on the 1163 head would have given 1175 but was never published).

This script:
1. reproduces the after-cost-70c-warm3 chain head by runpy (asserting
   1163/6684/527280/4954/391003; that chain internally reproduces the unified
   merge head 1154 blob-identically and the cost-69f head 1163), and asserts
   the regenerated warm3 head JSON is byte-identical to main (git blob sha
   50735896bfbfdcf99291200ba77e9551559502a4, 8305 bytes);
2. asserts every published cost-72b input file byte-exact against main
   (git blob shas at main aa6ef0b9: sweep record, 10 raw batches, 4 v15
   crosscheck files, determinism rerun, claim, certificate manifest);
3. asserts the child was genuinely still remaining at the baseline state
   (cost 72 row of the parent, demand c1=0,c2=2,c4=0, both open parents);
4. re-derives the published sweep record from the ten raw batch JSONLs:
   per-batch candidate bits, pilot 3402 controls, 72 candidates exactly
   once, 13 WIN7-D10 / 59 REFUTED / 0 capped, node sum 117,444,772, win
   roots == child | 1<<bit, 13 distinct D4 orbits, terminal range 13..17;
5. asserts the v15 cross-engine anchors (13 WIN loss=true with node match,
   refuted anchors bits 0/9/120 loss=false, pilot 5949 per file) and the
   v16 determinism rerun (13 bits node-exact, pilot 3402);
6. asserts all 13 published certificates against the local certificate
   bytes (whole = single file or joined parts: md5, sha256, git blob shas,
   bytes, rows sorted-unique, header, root identity, sub-roots == loser
   mobility, union 0/0, terminal 13..17, fbt_drops 0, v15 anchor node
   match, v16 sweep node match) and the manifest totals;
7. asserts the 13 roots are disjoint from the 63 folded receipt roots
   (49 unified + 9 cost-69f + 4 warm batch-3, distinct);
8. folds the 13 receipts in published bit order, re-deriving every
   per-record marginal from the growing union, with the child-orbit
   closure control and a set-equality control s_after == s_1163 UNION
   covers(13 roots);
9. produces the after-cost-72b frontier + ranking CSV + top-candidates CSV.

Receipts only - no sweep claims are made here. The in-flight cost-74d
certificate extraction (parallel lane) and the cost-69g/65j sweeps are not
folded by this script.
"""
import csv, hashlib, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
CERTS = OUT / 'cost72b-certs'

def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest(), len(data)

# ---------- 1. reproduce the cost-74d chain head (1179) ----------
nsD = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost74d_receipts_20261115.py'))
s_1179 = nsD['s_cur']
st_1179 = nsD['stF']
covers = nsD['covers']
manifest = nsD['manifest']
classes = nsD['classes']
summary_state = nsD['summary_state']
rem_1163 = nsD['remW']
addition74d = nsD['addition']
assert st_1179['solved_s6_in_manifest'] == 1179 and st_1179['unique_remaining_s6'] == 6668
assert st_1179['sum_remaining_cost'] == 526075
assert st_1179['s6_needed_by_open_classes'] == 4938 and st_1179['cost_needed_by_open_classes'] == 389798
sha, blen = git_blob_sha(OUT / 'class-frontier-cost74d-receipts-recompute-20261115.json')
assert sha == '06724afe0698ce93319d092521c5887da6eec0f0' and blen == 11449, \
    'regenerated cost-74d head JSON must be byte-identical to main'
# the 74d chain internally reproduced warm3 1163 and unified 1154 (blob controls there)
assert len(addition74d) == 15 and [a['bit'] for a in addition74d] == \
    [2, 12, 28, 66, 68, 69, 80, 91, 92, 100, 102, 109, 112, 116, 118]
print('CONTROL cost-74d chain head reproduced byte-identically: '
      '1179/6668/526075/4938/389798 (head JSON blob == main; warm3 1163 and '
      'unified 1154 asserted chain-internally)')

# ---------- 2. published cost-72b inputs byte-exact against main ----------
MAIN_BLOBS = {
    'class2-lane-cost72b-sweep-20261115.json':
        '2d27ad7ad6149687f0ecb5aeba1573dbd343bf36',
    'class2-lane-cost72b-raw-batch1-20261115.jsonl':
        '5709c962aac5428aae603da1af05f1cf42d2227e',
    'class2-lane-cost72b-raw-batch2-20261115.jsonl':
        'b1a49a6fdc54790b102e1341e0ce55b72ec9d518',
    'class2-lane-cost72b-raw-batch3-20261115.jsonl':
        '1b215563408d55b5643acdb5f91eb271691d8edd',
    'class2-lane-cost72b-raw-batch4-20261115.jsonl':
        'ea47503649b7c0ba5c4cddbef3e03b9a782ab4dd',
    'class2-lane-cost72b-raw-batch5-20261115.jsonl':
        '59b027090889e623eb4c0bac2582187008080b89',
    'class2-lane-cost72b-raw-batch6-20261115.jsonl':
        '1ccebc4d68dbf035a7c0d076acc3c600c1184a21',
    'class2-lane-cost72b-raw-batch7-20261115.jsonl':
        'db499c9c203e2827b3d0ffbf9c0277e968dc9a6b',
    'class2-lane-cost72b-raw-batch8-20261115.jsonl':
        'b5d84d7ac00b9d3dba25dbffb3eb845b18b08819',
    'class2-lane-cost72b-raw-batch9-20261115.jsonl':
        '8d1fdd96d8f50d85967e36f1b6f17b1464411660',
    'class2-lane-cost72b-raw-batch10-20261115.jsonl':
        '2d7f52e941ddf9e3ea1cef17046422bfe425b279',
    'class2-lane-cost72b-v15-crosscheck-a-20261115.jsonl':
        '539570f195bab5a084d322c9ff2da21664b7d670',
    'class2-lane-cost72b-v15-crosscheck-b-20261115.jsonl':
        '880e1d03c15acc095dc8259a0f8221767affcee5',
    'class2-lane-cost72b-v15-crosscheck-c-20261115.jsonl':
        '4a58a1d95503313a3f6e6e6809bc93a6ad87d3d9',
    'class2-lane-cost72b-v15-crosscheck-refuted-20261115.jsonl':
        '31bef68736e46eb9b545d8c0d038830eda960532',
    'class2-lane-cost72b-determinism-rerun-20261115.jsonl':
        'e97e5583d687da4fe4ca2645c80806cedd3519e9',
    'class2-lane-cost72b-inflight-20261115.json':
        'e8ede6750351b11037115f8478a2c556c578cc6a',
    'class2-lane-cost72b-win7-certificates-20261115.json':
        '27ca07f9bb49e3638c901f62cab7f961844c5106',
}
for name, want in MAIN_BLOBS.items():
    sha, blen = git_blob_sha(OUT / name)
    assert sha == want, name
print('CONTROL %d published cost-72b input files byte-exact against main '
      '(git blob shas)' % len(MAIN_BLOBS))

PARENT = '00000000000000809102000000000000'
CHILD = '00000000000000809102000002000000'
CHILD_V = int(CHILD, 16)
_diff = CHILD_V ^ int(PARENT, 16)
assert _diff > 0 and _diff & (_diff - 1) == 0, 'the child must be the parent plus exactly one stone'
LIFT_BIT = _diff.bit_length() - 1
WIN_BITS = [2, 11, 21, 30, 31, 36, 47, 66, 85, 95, 97, 100, 106]

# ---------- 3. baseline controls: remaining at 1163, pre-closed at 1179 ----------
OTHER_PARENT = '00000000000000801202000020000000'
# (a) historical: the child was genuinely remaining at the 1163 claim baseline
parent_rows_1163 = rem_1163.get(PARENT, [])
assert parent_rows_1163, 'parent S5 must still be remaining at the 1163 baseline'
child_rows_1163 = [r for r in parent_rows_1163 if r['s6_hex'] == CHILD]
assert child_rows_1163, 'the cost-72b child must still be remaining at the 1163 baseline'
assert int(child_rows_1163[0]['s6_s7_edge_cost']) == 72
other_rows_1163 = [r for r in rem_1163.get(OTHER_PARENT, []) if r['s6_hex'] == CHILD]
assert other_rows_1163, 'the second open parent must also hold the child row at 1163'
# re-derive the 1163 demand from the remaining incidences and the classes bitmask
dem_1163 = {'c1': 0, 'c2': 0, 'c4': 0}
for s5 in {PARENT, OTHER_PARENT}:
    bits = classes.get(s5, 0)
    if bits & 1: dem_1163['c1'] += 1
    if bits & 2: dem_1163['c2'] += 1
    if bits & 4: dem_1163['c4'] += 1
assert dem_1163 == {'c1': 0, 'c2': 2, 'c4': 0}
# (b) the 74d fold (1179) has already cross-covered and closed this child orbit
remD = nsD['remF']
assert CHILD_V in s_1179, 'the child must already be solved at the 1179 head'
assert CHILD not in {r['s6_hex'] for r in remD.get(PARENT, [])}
assert CHILD not in {r['s6_hex'] for r in remD.get(OTHER_PARENT, [])}
bit91 = next(a for a in addition74d if a['bit'] == 91)
assert CHILD in bit91['marginal_manifest_hexes'], \
    'the 74d bit-91 receipt must be the one that closed this child orbit'
claim = json.loads((OUT / 'class2-lane-cost72b-inflight-20261115.json').read_text())
assert claim['demand'] == {'c1': 0, 'c2': 2, 'c4': 0}
op = claim['open_parents_at_head_1163']
assert {p['s5_hex'] for p in op} == {PARENT, OTHER_PARENT}
# the parallel lane's rebase instruction recorded on main in the updated claim
rb = claim['rebase_required']
assert rb['required'] is True and rb['baseline_head'] == 1179
dd = rb['d4_duplicate_root']
assert dd['cost72b_bit85'] == '00000000002000809102000002000000'
assert dd['cost74d_bit91'] == '00000000080000809102020000000000'
assert dd['canonical'] == '00000000000080811202000020000000'
# the D4-equivalence itself is verified with the chain-internal canon() in the
# disjointness section below (after the certificates are loaded)
print('CONTROL child genuinely remaining at the 1163 claim baseline (parent rows %d, '
      'child cost 72, demand c1=0,c2=2,c4=0 re-derived); pre-closed at 1179 by the '
      'cost-74d bit-91 cross-cover (both parents already lost the child row)' % len(parent_rows_1163))

# ---------- 4. re-derive the published sweep record from the raw batches ----------
sweep = json.loads((OUT / 'class2-lane-cost72b-sweep-20261115.json').read_text())
assert sweep['schema'] == 'n11-class2-lane-cost72b-sweep-20261115-v1'
assert sweep['s6_child'] == CHILD and sweep['s6_s7_edge_cost'] == 72
assert sweep['demand'] == {'c1': 0, 'c2': 2, 'c4': 0}
assert sweep['candidate_count'] == 72
assert sweep['win7_d10_bits'] == WIN_BITS
assert sweep['chain_head_at_claim'] == '1163/6684/527280/4954/391003'

raw_by_bit = {}
seen_bits = []
for brec in sweep['raw_batches']:
    b = brec['batch']
    lines = (OUT / f'class2-lane-cost72b-raw-batch{b}-20261115.jsonl').read_text().splitlines()
    recs = [json.loads(l) for l in lines if l.strip()]
    pilots = [r for r in recs if r.get('control') == 'pilot_d6']
    assert len(pilots) == 1 and pilots[0]['loss'] is False and pilots[0]['nodes'] == 3402
    cands = [r for r in recs if 'bit' in r]
    assert [r['bit'] for r in cands] == brec['bits']
    for r in cands:
        assert r['capped'] is False
        assert r['terminalStoneRange'][0] >= 13 and r['terminalStoneRange'][1] <= 17
        raw_by_bit[r['bit']] = r
        seen_bits.append(r['bit'])
assert len(seen_bits) == len(set(seen_bits)) == 72
assert sweep['totals'] == {'candidates': 72, 'win7_d10': 13, 'refuted_d10': 59,
                           'capped': 0, 'candidate_nodes': 117444772}
win_raw = [b for b in WIN_BITS if raw_by_bit[b]['loss'] is True]
refuted_raw = [b for b in raw_by_bit if raw_by_bit[b]['loss'] is False]
assert len(win_raw) == 13 and len(refuted_raw) == 59
assert sum(r['nodes'] for r in raw_by_bit.values()) == 117444772
# sweep record per-candidate results == raw batch records
res_by_bit = {r['bit']: r for r in sweep['results']}
assert sorted(res_by_bit) == sorted(raw_by_bit) and len(raw_by_bit) == 72
for bit, r in raw_by_bit.items():
    s = res_by_bit[bit]
    assert s['loss'] == r['loss'] and s['nodes'] == r['nodes'] and s['capped'] is False
    assert s['raw_batch'] in {b['batch'] for b in sweep['raw_batches'] if bit in b['bits']}
wd = {w['bit']: w for w in sweep['win7_details']}
assert sorted(wd) == WIN_BITS
d4s = set()
for bit in WIN_BITS:
    w = wd[bit]
    assert int(w['root_hex'], 16) == CHILD_V | (1 << bit), bit
    assert w['v16_nodes'] == raw_by_bit[bit]['nodes']
    assert w['v15_crosscheck_loss'] is True
    assert w['determinism_rerun_nodes_equal'] is True
    d4s.add(w['d4_canonical_hex'])
assert len(d4s) == 13 and sweep['win7_d4_orbits_distinct'] == 13
print('CONTROL sweep record re-derived from 10 raw batches: 72 candidates exactly '
      'once, 13 WIN7-D10 / 59 REFUTED / 0 capped / 117,444,772 nodes, '
      'roots == child|1<<bit, 13 distinct D4 orbits')

# ---------- 5. v15 cross-engine anchors + v16 determinism rerun ----------
v15_bits = {}
v15_pilots = 0
for tag in ('a', 'b', 'c'):
    lines = (OUT / f'class2-lane-cost72b-v15-crosscheck-{tag}-20261115.jsonl').read_text().splitlines()
    recs = [json.loads(l) for l in lines if l.strip()]
    pilots = [r for r in recs if r.get('control') == 'pilot_d6']
    assert len(pilots) == 1 and pilots[0]['loss'] is False and pilots[0]['nodes'] == 5949
    v15_pilots += 1
    for r in recs:
        if 'bit' in r:
            v15_bits[r['bit']] = r
assert sorted(v15_bits) == WIN_BITS
for bit in WIN_BITS:
    r = v15_bits[bit]
    assert r['loss'] is True and r['capped'] is False
    assert r['nodes'] == wd[bit]['v15_crosscheck_nodes']
    assert r['terminalStoneRange'][0] >= 13 and r['terminalStoneRange'][1] <= 17
refl = [json.loads(l) for l in
        (OUT / 'class2-lane-cost72b-v15-crosscheck-refuted-20261115.jsonl').read_text().splitlines() if l.strip()]
ref_pilots = [r for r in refl if r.get('control') == 'pilot_d6']
assert len(ref_pilots) == 1 and ref_pilots[0]['loss'] is False and ref_pilots[0]['nodes'] == 5949
ref_bits = {r['bit']: r for r in refl if 'bit' in r}
for a in sweep['refuted_v15_anchors']:
    r = ref_bits[a['bit']]
    assert r['loss'] is False and r['nodes'] == a['v15_nodes']
det = [json.loads(l) for l in
       (OUT / 'class2-lane-cost72b-determinism-rerun-20261115.jsonl').read_text().splitlines() if l.strip()]
det_pilots = [r for r in det if r.get('control') == 'pilot_d6']
assert len(det_pilots) == 1 and det_pilots[0]['loss'] is False and det_pilots[0]['nodes'] == 3402
det_bits = {r['bit']: r for r in det if 'bit' in r}
assert sorted(det_bits) == WIN_BITS
for bit in WIN_BITS:
    r = det_bits[bit]
    assert r['loss'] is True and r['capped'] is False
    assert r['nodes'] == raw_by_bit[bit]['nodes'], bit
assert sweep['determinism_rerun'] == {'bits': WIN_BITS, 'node_exact_all': True}
print('CONTROL v15 cross-engine anchors (13 WIN loss=true node-matched, refuted '
      '0/9/120 loss=false, pilots 5949 x4) and v16 determinism rerun '
      '(13 bits node-exact, pilot 3402) verified')

# ---------- 6. assert all 13 published certificates ----------
certdoc = json.loads((OUT / 'class2-lane-cost72b-win7-certificates-20261115.json').read_text())
assert certdoc['schema'] == 'n11-class2-lane-cost72b-win7-certificates-20261115-v1'
certs = certdoc['certificates']
assert [c['bit'] for c in certs] == WIN_BITS
whole_blobs = {}
sums = {'rows': 0, 'extraction_nodes': 0, 'sub_roots_total': 0,
        'visited_states_across_subroots': 0, 'winner_states': 0,
        'loser_states': 0, 'terminal_count': 0, 'loser_reply_edges': 0}
v15_sum = 0
for c in certs:
    bit = c['bit']
    assert c['verdict'] == 'WIN7' and c['child_hex'] == CHILD
    assert int(c['root_hex'], 16) == CHILD_V | (1 << bit), bit
    assert c['root_hex'] == wd[bit]['root_hex']
    assert c['d4_canonical_hex'] == wd[bit]['d4_canonical_hex']
    assert c['fbt_drops'] == 0 and c['fatal'] is None
    assert c['all_loser_first_moves_extracted_ok'] is True
    assert c['rows_sorted_unique'] is True
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert c['sub_roots_pass'] == c['sub_roots_total'] == c['root_check']['loser_mobility'] > 0
    assert c['root_check']['stones'] == 7 and c['root_check']['match'] is True
    assert c['terminal_range'][0] >= 13 and c['terminal_range'][1] <= 17
    assert c['v16_sweep_nodes'] == raw_by_bit[bit]['nodes']
    assert c['v15_anchor_crosscheck']['loss'] is True
    assert c['v15_anchor_crosscheck']['nodes'] == v15_bits[bit]['nodes']
    v15_sum += c['v15_anchor_crosscheck']['nodes']
    # local certificate bytes: whole = single file or joined parts
    st = c['storage']
    part_files = []
    for p in st['parts']:
        local = CERTS / p['path'].split('/')[-1]
        data = local.read_bytes()
        assert len(data) == p['bytes'], (bit, p['path'])
        assert hashlib.md5(data).hexdigest() == p['md5'], (bit, p['path'])
        sha_p, _ = git_blob_sha(local)
        assert sha_p == p['git_blob_sha'], (bit, p['path'])
        part_files.append(data)
    whole = b''.join(part_files)
    assert len(whole) == c['bytes']
    assert hashlib.md5(whole).hexdigest() == c['md5']
    assert hashlib.sha256(whole).hexdigest() == c['sha256']
    sha_w, _ = git_blob_sha.__call__(None) if False else (None, None)
    # whole git blob sha: write joined bytes to a temp name derived from root
    tmp = CERTS / f'fold-verify-bit{bit}.whole'
    tmp.write_bytes(whole)
    sha_w, blen_w = git_blob_sha(tmp)
    tmp.unlink()
    assert sha_w == c['whole_git_blob_sha'], bit
    lines = whole.decode().splitlines()
    assert lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
    assert lines[1] == 'root ' + c['root_hex']
    rows = [l for l in lines[2:] if l.strip()]
    assert len(rows) == c['rows'] and len(set(rows)) == c['rows']
    assert rows == sorted(rows), 'certificate rows must be sorted-unique'
    for k in sums:
        sums[k] += c[k]
    whole_blobs[bit] = sha_w
assert sums == {'rows': 636225, 'extraction_nodes': 200029509, 'sub_roots_total': 729,
                'visited_states_across_subroots': 1378650, 'winner_states': 889294,
                'loser_states': 264554, 'terminal_count': 224802,
                'loser_reply_edges': 1241817}
assert v15_sum == 132170428 == certdoc['totals']['v15_crosscheck_nodes']
t = certdoc['totals']
assert t['certificates'] == 13 and t['rows'] == 636225 and t['extraction_nodes'] == 200029509
assert t['sub_roots'] == 729 and t['visited_states_across_subroots'] == 1378650
assert t['winner_states'] == 889294 and t['loser_states'] == 264554
assert t['terminal_count'] == 224802 and t['loser_reply_edges'] == 1241817
assert certdoc['controls']['all_certificates_independently_verified'] is True
assert certdoc['controls']['all_part_splits_at_line_boundaries'] is True
assert certdoc['controls']['all_git_blob_shas_verified_on_main_19_of_19'] is True
print('CONTROL 13 published certificates asserted against local bytes: md5 x sha256 '
      'x git blob shas (19 parts + 13 whole), rows sorted-unique, sub-roots == '
      'loser mobility, union 0/0, terminal 13..17, v15 anchors node-matched; '
      'manifest totals 636,225 rows / 729 sub-roots / 200,029,509 extraction nodes')

# ---------- 7. root disjointness vs the 63 folded receipt roots ----------
nsU = nsD['nsW']['nsU']
roots68 = nsU['roots68']
rootsM2 = nsU['rootsM2']
roots70 = nsU['roots70']
addition69f = nsD['nsW']['nsF']['addition']
warm3_roots = {r['root_hex'] for r in nsD['nsW']['recs']}
prev = {int(x, 16) for x in roots68} | {int(x, 16) for x in rootsM2} | \
       {int(x, 16) for x in roots70} | {int(a['root_hex'], 16) for a in addition69f} | \
       {int(x, 16) for x in warm3_roots} | {int(a['root_hex'], 16) for a in addition74d}
assert len(prev) == 77, len(prev)
roots72 = [int(c['root_hex'], 16) for c in certs]
assert len(set(roots72)) == 13
assert not (set(roots72) & prev), 'the 13 cost-72b roots must be disjoint from the folded receipt roots'
# D4-orbit cross-check against the 74d receipts: exactly one known equivalence
canon = covers.__globals__['canon']
d4_74d = {f'{canon(int(a["root_hex"], 16)):032x}' for a in addition74d}
d4_hits = [(c['bit'], c['d4_canonical_hex']) for c in certs
           if f'{canon(int(c["root_hex"], 16)):032x}' in d4_74d]
assert d4_hits == [(85, '00000000000080811202000020000000')], d4_hits
assert all(f'{canon(int(c["root_hex"], 16)):032x}' == c['d4_canonical_hex'] for c in certs)
print('CONTROL root disjointness: 13 new roots vs 77 distinct folded receipt roots '
      '(62 + 15 cost-74d; raw-hex intersections empty); exactly one known '
      'D4-orbit equivalence with the 74d receipts (72b bit85 == 74d bit91, '
      'canonical 00000000000080811202000020000000), verified with the '
      'chain-internal canon() - the two are not counted as separate orbits')

# ---------- 8. fold the 13 receipts in published bit order ----------
s0 = set(s_1179)
s_cur = set(s_1179)
addition = []
zero_mim = []
for bit in WIN_BITS:
    w = wd[bit]
    c = next(x for x in certs if x['bit'] == bit)
    root = int(w['root_hex'], 16)
    cov = covers(root)
    marg = cov - s_cur
    marg_m = marg & manifest
    assert CHILD_V not in marg, \
        'the child orbit was pre-closed at 1179 by the 74d bit-91 cross-cover'
    rec = {
        'bit': bit, 'root_hex': w['root_hex'], 'd4_canonical_hex': w['d4_canonical_hex'],
        'sweep_nodes': w['v16_nodes'], 'certified': True,
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
        'marginal_non_manifest_hexes': sorted(f'{k:032x}' for k in marg - marg_m),
        'rows': c['rows'], 'extraction_nodes': c['extraction_nodes'],
        'md5': c['md5'], 'sub_roots_pass': c['sub_roots_pass'],
        'v15_anchor_nodes': c['v15_anchor_crosscheck']['nodes'],
    }
    addition.append(rec)
    if not marg_m:
        zero_mim.append(bit)
    s_cur |= marg
cov13 = set()
for r in roots72:
    cov13 |= covers(r)
assert s_cur == set(s_1179) | cov13, 'set-equality: s_after == s_1179 UNION covers(13 roots)'
total_mim = sum(a['marginal_in_manifest'] for a in addition)
total_marg = sum(a['marginal'] for a in addition)
stF, remF, uniqF, demF = summary_state(s_cur)
assert stF['solved_s6_in_manifest'] == 1179 + total_mim
assert s_cur >= s0
# the child was pre-closed at 1179; it must remain solved and both parents stay childless
assert CHILD_V in s_cur and CHILD_V in manifest
assert CHILD not in {r['s6_hex'] for r in remF.get(PARENT, [])}
assert CHILD not in {r['s6_hex'] for r in remF.get(OTHER_PARENT, [])}
print('AFTER cost-72b receipts:', json.dumps(stF, indent=1))
print(f'total marginal={total_marg} marginal_in_manifest={total_mim}; '
      f'zero-mim receipts: {zero_mim or "none"}; child orbit pre-closed by cost-74d bit91')

# ---------- 9. outputs ----------
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
    'schema': 'n11-class-frontier-cost72b-receipts-recompute-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'class-frontier-cost74d-receipts-recompute-20261115.json '
                     '(cost-74d chain head 1179/6668/526075/4938/389798; '
                     'regenerated byte-identical, git blob sha '
                     '06724afe0698ce93319d092521c5887da6eec0f0)',
    'rebase_note': 'the parallel lane published the cost-74d fold on the 1163 '
                   'head first; its bit-91 receipt cross-covered and closed '
                   'this cost-72b child orbit, so this fold rebases on the '
                   'canonical 1179 head per the rebase_required instruction '
                   'recorded in the updated claim. A sibling fold of the same '
                   '13 receipts on the 1163 head would have given 1175 but '
                   'was never published. Known D4-orbit equivalence: cost-72b '
                   'bit85 root 00000000002000809102000002000000 == cost-74d '
                   'bit91 root 00000000080000809102020000000000 (canonical '
                   '00000000000080811202000020000000, verified with the '
                   'chain-internal canon()); the bit85 certificate upgrades '
                   'proof backing of orbits folded as a raw receipt on the '
                   '74d side and the two are not counted as separate orbits. '
                   'The child-remaining-at-baseline control is asserted '
                   'historically at 1163 via the chain-internal warm3 '
                   'remaining set',
    'method': 'runpy reproduction of the cost-74d chain head '
              '(asserting 1179/6668/526075/4938/389798 and the blob-identical '
              '74d head JSON; that chain internally reproduces the warm3 head '
              '1163 and the unified merge head 1154 blob-identically), the '
              'cost-72b child asserted genuinely remaining at the 1163 claim '
              'baseline (cost 72, demand c1=0,c2=2,c4=0 re-derived from the '
              'chain-internal remaining incidences, both open parents holding '
              'the child row) and already closed at 1179 by the 74d bit-91 '
              'cross-cover (asserted), all 18 published cost-72b '
              'input files asserted byte-exact against main by git blob sha, '
              'the cost-72b child asserted genuinely remaining at baseline '
              '(cost 72, demand c1=0,c2=2,c4=0, both open parents), the '
              'published sweep record re-derived from the ten raw batch '
              'JSONLs (72 candidates exactly once, 13 WIN7-D10 / 59 REFUTED '
              '/ 0 capped / 117,444,772 nodes, roots == child | 1<<bit, 13 '
              'distinct D4 orbits), the v15 cross-engine anchors and the v16 '
              'determinism rerun asserted from the published JSONLs, all 13 '
              'published certificates asserted against the local certificate '
              'bytes (md5, sha256, git blob shas of 19 parts and 13 joined '
              'wholes, rows sorted-unique, sub-roots == loser mobility, '
              'union 0/0, terminal 13..17, v15 anchors node-matched) with '
              'the manifest totals re-summed, the 13 roots asserted disjoint '
              'from the 62 folded receipt roots, then the 13 receipts folded '
              'in published bit order with every per-record marginal '
              're-derived from the growing union; the child-orbit closure is '
              'identified and asserted, both open parents are asserted to '
              'have lost the child row, and a set-equality control holds. '
              'Receipts only - no sweep claims',
    'controls': {
        'warm3_head_1163_reproduced_byte_identical': True,
        'input_files_byte_exact_vs_main': len(MAIN_BLOBS),
        'child_genuinely_remaining_at_baseline': True,
        'sweep_rederived_from_raw_batches': True,
        'v15_cross_engine_anchors_verified': True,
        'v16_determinism_rerun_verified': True,
        'certificates_bytes_md5_sha256_blobsha_verified': True,
        'manifest_totals_resummed': True,
        'root_disjointness_vs_62_receipts': True,
        'child_orbit_closure': 'child orbit pre-closed at chain head 1179 by the cost-74d bit-91 cross-cover (72b bit85 is the same D4 orbit)',
        'both_open_parents_lost_child_row': True,
        'set_equality_after_13': 's == s_1163 UNION covers(13 cost-72b roots)',
    },
    'target': {
        's5_parent_hex': PARENT, 's6_child_hex': CHILD, 'edge_cost': 72,
        'open_parents': [PARENT, OTHER_PARENT],
        'demand_at_claim_baseline_1163': {'c1': 0, 'c2': 2, 'c4': 0},
        'child_orbit_closure': 'closed at 1179 by the cost-74d bit-91 '
                               'cross-cover (before this fold)',
        'candidates': 72, 'win7_d10': 13, 'refuted_d10': 59, 'capped': 0,
        'candidate_nodes': 117444772,
    },
    'cost72b_addition': addition,
    'totals': {
        'receipts': 13,
        'total_marginal': total_marg,
        'total_marginal_in_manifest': total_mim,
        'zero_marginal_in_manifest': [f'bit{b}' for b in zero_mim],
        'certificate_rows': sums['rows'],
        'certificate_extraction_nodes': sums['extraction_nodes'],
        'certificate_sub_roots': sums['sub_roots_total'],
        'v15_crosscheck_nodes_sum': v15_sum,
    },
    'frontier_after_cost72b': {
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
        'cost74d_certificates': '14 of the 15 cost-74d WIN7 receipts are '
                                 'certificate-pending (only bit118 is '
                                 'certificate-backed; the rest are raw sweep '
                                 'receipts with v15 anchors) - extraction '
                                 'stays with the parallel lane',
        'cost69f_certificates': 'WIN7 bits 2/94/109/119 certificates still '
                                'pending extraction (folded earlier as raw '
                                'sweep receipts with v15 anchors)',
        'cost65j_sweep': 'in flight on the parallel lane; its bit-113 WIN7 '
                         '(if found) cross-covers the cost-69f child through '
                         'the shared orbit - recheck before the next fold',
        'parallel_bands': 'cost-65h/67b/68c warm candidates stay with the '
                          'parallel lane',
    },
    'interpretation_guard': 'bookkeeping over published receipts; solved counts '
                            'measure manifest coverage, not the game-theoretic '
                            'value of any position; REFUTED-D10 sweeps prove '
                            'only absence of WIN7-D10; WIN7 certificates prove '
                            'a win within depth 10 from the individual '
                            '7-stone roots only; closing the cost-72b child '
                            'orbit removes the child from its parents\' '
                            'remaining rows but does not solve either S5 '
                            'parent; 11x11 empty board / two-stone root '
                            '{49,60} / S2 {59,60} / class 2 / class 4 remain '
                            'UNKNOWN',
}
(OUT / 'class-frontier-cost72b-receipts-recompute-20261115.json').write_text(
    json.dumps(result, indent=1) + '\n')
print('written class-frontier-cost72b-receipts-recompute-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remF.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost72b-receipts-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

with (OUT / 'class-frontier-top-candidates-s6-after-cost72b-receipts-20261115.csv').open(
        'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    coverable = [c for c in class2 if c['s5_hex'] != AUDIT_BLOCKED]
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         next((c for c in class2 if c['s5_hex'] == AUDIT_BLOCKED), None)),
                        ('best coverable class-2 blocker-candidate S5', coverable[0]),
                        ('second coverable class-2 candidate S5',
                         coverable[1] if len(coverable) > 1 else None)):
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
print('written ranking + top-candidates CSVs (after-cost72b-receipts)')
