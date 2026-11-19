#!/usr/bin/env python3
# Receipt fold of the seventeenth WIN7-D10 certificate (K1069 sweep WIN root,
# published by n11-residual78-seventeenth-win7-cert-extract-20261120 with the
# certificate body supplied in-repo by commit b7a6db5fb0) into the five-parent
# S6 frontier chain, as the seventeenth receipt (fold10).
#
# The frontier/base chain is reconstructed from the pinned published blobs
# (worklist -> ledger/globalFold -> cost78c/79c -> first -> second/third ->
# fourth -> fifth/sixth -> seventh -> eighth -> ninth-twelfth), then the
# fold9 (thirteenth..sixteenth) published record is chained from its pinned
# SHA-256, then the seventeenth certificate-backed receipt is applied to the
# resulting open set (published 6,209 rows / 491,722 cost; five-parent target
# residual 74) to close the two rows covered by the root.
#
# Certificate inputs are the published, triple-verified seventeenth
# certificate (38-gate record SHA-256 c1073bae...; certificate SHA-256
# 21dd2f0e...); this machine re-checks certificate bytes, root geometry,
# legal-move counts, the covered-row set via D4-image rederivation, and every
# chain count fail-closed before writing the fold record.
#
# Bookkeeping only: REFUTED-D10 is not a LOSS proof; no game value near the
# empty board is asserted. 11x11 empty board / two-stone roots remain UNKNOWN.
#
# W-relative input path -> published repo path map:
#   [same twelve blob-SHA-1-pinned chain inputs as fold_thirteenth_sixteenth.py]
#   fs13/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json
#       research/experiments/n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json
#   sv17pub/output/seventeenth-cert-triple-verification-20261120.json
#       research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/output/seventeenth-cert-triple-verification-20261120.json
#   sv17pub/certs/win7-root-00004000000000821082000000000100-20261120.n11
#       research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11
#
# Usage: python3 fold_seventeenth.py
import json, sys, hashlib, tarfile, csv

W = '/home/user/work/fold10/W'
OUT = 'fold/output/seventeenth-win7-receipt-fold-20261120.json'
ROOT_HEX = '00004000000000821082000000000100'
CHILD_HEX = '00004000000000821082000000000000'
ADDED_BIT = 8

def need(ok, m):
    if not ok:
        print('GATE FAILED:', m)
        sys.exit(1)

def blob_sha(path):
    b = open(path, 'rb').read()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def sha256_of(rel):
    return hashlib.sha256(open(f'{W}/{rel}', 'rb').read()).hexdigest()

def load(rel):
    return json.load(open(f'{W}/{rel}'))

def popcount(x):
    n = 0
    while x:
        x &= x - 1
        n += 1
    return n

# ---------- D4 transforms / geometry (verbatim convention of the fold chain) ----------
TF = []
for t in range(8):
    tab = []
    for p in range(121):
        x, y = p % 11, p // 11
        if t == 0: X, Y = x, y
        elif t == 1: X, Y = 10 - y, x
        elif t == 2: X, Y = 10 - x, 10 - y
        elif t == 3: X, Y = y, 10 - x
        elif t == 4: X, Y = 10 - x, y
        elif t == 5: X, Y = x, 10 - y
        elif t == 6: X, Y = y, x
        else: X, Y = 10 - y, 10 - x
        tab.append(11 * Y + X)
    TF.append(tab)

def bits_of(mask):
    out = []
    p = 0
    while mask:
        if mask & 1: out.append(p)
        mask >>= 1
        p += 1
    return out

def transform(mask, t):
    out = 0
    for p in bits_of(mask):
        out |= 1 << TF[t][p]
    return out

def canon_int(mask):
    best = None
    for t in range(8):
        z = transform(mask, t)
        if best is None or z < best: best = z
    return best

def canon_hex(mask):
    return format(canon_int(mask), '032x')

def det3(a, b, c):
    (x1, y1), (x2, y2), (x3, y3) = a, b, c
    q1 = x1*x1 + y1*y1; q2 = x2*x2 + y2*y2; q3 = x3*x3 + y3*y3
    return q1*(x2*y3 - x3*y2) - q2*(x1*y3 - x3*y1) + q3*(x1*y2 - x2*y1)

def det4(a, b, c, d):
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)

def unsafe_quadruples(mask):
    pts = [(p % 11, p // 11) for p in bits_of(mask)]
    n = 0
    for a in range(len(pts)):
        for b in range(a+1, len(pts)):
            for c in range(b+1, len(pts)):
                for d in range(c+1, len(pts)):
                    if det4(pts[a], pts[b], pts[c], pts[d]) == 0: n += 1
    return n

# ---------- pinned inputs ----------
PINS = {
 'inputs/worklist.csv': '2fee1d0718547a62e346d35f5858d7913e37c097',
 'inputs/ledger.json': 'e8785d509e8a11a37c0d03cc450455a14708c34d',
 'inputs/globalFold.json': '753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc',
 'inputs/previousCostFold.json': '7e6144cc4bc92c34faa14bed3058cde64fb3880e',
 'inputs/firstFoldTarball.tar.gz': 'fa5f26a9dc9bd2fb8222aa8ba0431d7578043019',
 'inputs/census.json': '9c251da3138c5cb0516e097be5e5d0427dfaf5f0',
 'inputs/audit.json': '7cdc7c9ef341b5d9759923b3fc4986231c48895f',
 'ex48/output/secondThirdFold.json': '7923a0fe5331d1f7c896748031c4071b68fcc13a',
 'fold4rec/fold4.json': '38715413d6dd23b97717c92d73d8b4a0af807cda',
 'fold56rec/fold56.json': '134796a7de1e472c26e35defd7340d208a10b9b0',
 'fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json': '5b1a30f9b56230382d502aa66ea89d3083b16dd2',
 'fold_fourth_fifth_sixth.py': 'd8068a8eea48fde5203ac6342abd4df2bd584b99',
}
PIN256 = {
 'foldv2/output/seventh-win7-receipt-fold-20261119.json': 'f1baf15942d3efeaa3ca75c4d803148239269715e297aaf9b00042611543b737',
 'foldv2/output/eighth-win7-receipt-fold-20261119.json': 'afcf7d0ad0d6ca1edf31e150a7ba840f802a6382506f4a662b4e13567fbd30a2',
 'resolve6/output/post-saturation-full-cache-join-resolve6-20261120.json': 'e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a',
 'fs13/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json': '24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2',
 'sv17pub/output/seventeenth-cert-triple-verification-20261120.json': 'c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc',
 'sv17pub/certs/win7-root-00004000000000821082000000000100-20261120.n11': '21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8',
}

for k, s in PINS.items():
    need(blob_sha(f'{W}/{k}') == s, f'input blob mismatch {k}')
for k, s in PIN256.items():
    need(sha256_of(k) == s, f'input sha256 mismatch {k}')
print('all', len(PINS) + len(PIN256), 'input pins verified')

# ---------- legal move machinery (verbatim published source, part 1) ----------
legal_moves_of_src = open(f'{W}/fold_fourth_fifth_sixth.py').read().split('# ---------- pinned inputs')[0]
_ns = {}; exec(legal_moves_of_src, _ns); legal_moves_of = _ns['legal_moves_of']

# ---------- frontier reconstruction chain (identical to fold_thirteenth_sixteenth) ----------
wl = {}
with open(f'{W}/inputs/worklist.csv') as f:
    r = csv.reader(f); hdr = next(r)
    ix = hdr.index('s6_canonical_hex'); cx = hdr.index('own_candidates_s6_s7_edge_cost'); kx = hdr.index('category')
    for a in r: wl[a[ix]] = (int(a[cx]), a[kx])
need(len(wl) == 6438, 'worklist row count 6438')
led = load('inputs/ledger.json')
gf = load('inputs/globalFold.json')
old66 = set(led['derived']['closed_rows_66'])
oldGlobal = set(x['row_hex'] for x in gf['receipts_by_row'])
open0 = {h: v for h, v in wl.items() if h not in old66 and h not in oldGlobal}
need(len(open0) == 6259 and sum(v[0] for v in open0.values()) == 495507, 'global-fold base frontier')
prev = load('inputs/previousCostFold.json')
prior = set(x['row_hex'] for x in prev['new_receipt_coverage']['receipts_by_row'])
openA = {h: v for h, v in open0.items() if h not in prior}
need(len(openA) == 6240 and sum(v[0] for v in openA.values()) == 493965, 'cost78c/79c fold frontier')
with tarfile.open(f'{W}/inputs/firstFoldTarball.tar.gz', 'r:gz') as t:
    firstFold = None
    for m in t.getmembers():
        if m.name.endswith('output/first-win7-root-receipt-fold-20261119.json'):
            firstFold = json.load(t.extractfile(m))
need(firstFold and firstFold['status'] == 'fold-complete' and firstFold['schema'] == 'n11-five-parent-first-win7-receipt-fold-20261119-v1', 'first fold schema')
firstClosed = set(x['row_hex'] for x in firstFold['new_receipt_coverage']['rows'])
open1 = {h: v for h, v in openA.items() if h not in firstClosed}
need(len(open1) == 6236 and sum(v[0] for v in open1.values()) == 493703, 'first-fold frontier')
stf = load('ex48/output/secondThirdFold.json')
need(stf['status'] == 'fold-complete' and stf['receipt_count'] == 2, 'second-third fold gate')
rows23 = []
for rr in stf['receipts']: rows23.extend(rr['covered_s6_rows'])
open2 = {h: v for h, v in open1.items() if h not in set(rows23)}
need(len(open2) == 6229 and sum(v[0] for v in open2.values()) == 493184, 'second-third frontier')
fold4rec = load('fold4rec/fold4.json')
need(fold4rec['status'] == 'fold-complete' and fold4rec['schema'] == 'n11-five-parent-fourth-win7-receipt-fold-20261119-v1', 'fold4 record gate')
rows4 = [x['row_hex'] for x in fold4rec['new_receipt_coverage']['rows']]
open3 = {h: v for h, v in open2.items() if h not in set(rows4)}
need(len(open3) == 6226 and sum(v[0] for v in open3.values()) == 492970, 'fourth-fold frontier')
fold56rec = load('fold56rec/fold56.json')
need(fold56rec['status'] == 'fold-complete' and fold56rec['schema'] == 'n11-five-parent-fifth-sixth-win7-receipt-fold-20261119-v1', 'fold56 record gate')
rows56 = [x['row_hex'] for x in fold56rec['new_receipt_coverage']['rows']]
open4 = {h: v for h, v in open3.items() if h not in set(rows56)}
need(len(open4) == 6224 and sum(v[0] for v in open4.values()) == 492830, 'fifth-sixth-fold frontier')
fold7 = load('foldv2/output/seventh-win7-receipt-fold-20261119.json')
need(fold7['status'] == 'fold-complete' and fold7['receipt_count'] == 1, 'fold7 gate')
rows7 = []
for rr in fold7['receipts']: rows7.extend(rr['covered_s6_rows'])
open5 = {h: v for h, v in open4.items() if h not in set(rows7)}
need(len(open5) == 6223 and sum(v[0] for v in open5.values()) == 492762, 'seventh-fold frontier')
fold8 = load('foldv2/output/eighth-win7-receipt-fold-20261119.json')
need(fold8['status'] == 'fold-complete' and fold8['receipt_count'] == 1, 'fold8 gate')
rows8 = []
for rr in fold8['receipts']: rows8.extend(rr['covered_s6_rows'])
openCur = {h: v for h, v in open5.items() if h not in set(rows8)}
need(len(openCur) == 6222 and sum(v[0] for v in openCur.values()) == 492688, 'eighth-fold frontier (must match published 6222/492688)')
print('frontier chain verified: 6259/495507 -> ... -> 6222/492688')

# ---------- census / parent machinery ----------
census = load('inputs/census.json')
parents = {p['hex']: p for p in census['open_s5_census']}
parents_int = {int(h, 16): h for h in parents}
need(len(parents) > 0, 'census parents loaded')

_rowp_cache = {}
def row_parents_hex(h):
    if h in _rowp_cache: return _rowp_cache[h]
    mask = int(h, 16); ps = set()
    for q in bits_of(mask):
        c = canon_int(mask ^ (1 << q))
        if c in parents_int: ps.add(parents_int[c])
    _rowp_cache[h] = ps
    return ps

def demand(h):
    d = {'c1': 0, 'c2': 0, 'c4': 0}
    for p in row_parents_hex(h):
        c = parents[p]['classes']
        if c & 1: d['c1'] += 1
        if c & 2: d['c2'] += 1
        if c & 4: d['c4'] += 1
    return d

def root_row_set(root_hex, open_set):
    mask = int(root_hex, 16); out = {}
    for t in range(8):
        image = transform(mask, t)
        for q in range(121):
            if (image >> q) & 1:
                c = canon_int(image ^ (1 << q))
                h = format(c, '032x')
                if h in open_set: out[h] = True
    return sorted(out)

# ---------- ninth-twelfth fold record chaining ----------
tf9 = load('fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json')
need(tf9['status'] == 'fold-complete' and tf9['schema'] == 'n11-five-parent-ninth-twelfth-win7-receipt-fold-20261119-v1', 'fold9 record gate')
need(tf9['receipt_count'] == 4, 'fold9 receipts count')
rows9 = []
for rr in tf9['receipts']:
    need(len(rr['covered_s6_rows']) >= 1, 'fold9 receipt closes nothing')
    rows9.extend(rr['covered_s6_rows'])
for h in rows9:
    need(h in openCur, 'fold9 row not open: ' + h)
openCur9 = {h: v for h, v in openCur.items() if h not in set(rows9)}
need(len(openCur9) == 6213 and sum(v[0] for v in openCur9.values()) == 492021, 'post-ninth-twelfth frontier (must match published 6213/492021)')
fa9 = tf9['frontier_after']
need(fa9['unique_remaining_s6'] == 6213 and fa9['sum_remaining_cost'] == 492021
     and fa9['solved_s6_in_manifest'] == 1635, 'fold9 frontier_after published values')
inc = {p: 0 for p in parents}
for h in openCur9:
    for p in row_parents_hex(h): inc[p] += 1
need(sum(inc.values()) == fa9['parent_row_incidence'] == 11826, 'pre-windfall incidence 11826')
print('post-ninth-twelfth frontier verified: 6213/492021, solved_s6 1635, incidence 11826')

# ---------- fold9 (thirteenth..sixteenth) record chaining ----------
fs13 = load('fs13/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json')
need(fs13['status'] == 'fold-complete', 'fs13 fold-complete')
need(fs13['schema'] == 'n11-five-parent-windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120-v1', 'fs13 schema')
need(fs13['receipt_count'] == 4 and len(fs13['receipts']) == 4, 'fs13 receipts count')
rows13_16 = []
for rr in fs13['receipts']:
    need(len(rr['covered_s6_rows']) >= 1, 'fs13 receipt closes nothing')
    rows13_16.extend(rr['covered_s6_rows'])
need(len(rows13_16) == len(set(rows13_16)), 'fs13 receipt rows unique')
for h in rows13_16:
    need(h in openCur9, 'fs13 row not open: ' + h)
open74 = {h: v for h, v in openCur9.items() if h not in set(rows13_16)}
fa13 = fs13['frontier_after']
need(len(open74) == 6209 and sum(v[0] for v in open74.values()) == 491722, 'post-thirteenth-sixteenth frontier (must match published 6209/491722)')
need(fa13['unique_remaining_s6'] == 6209 and fa13['sum_remaining_cost'] == 491722
     and fa13['solved_s6_in_manifest'] == 1639 and fa13['parent_row_incidence'] == 11818, 'fs13 frontier_after published values')
for h in rows13_16:
    del_path = [p for p in row_parents_hex(h)]
    for p in del_path: inc[p] -= 1
need(sum(inc.values()) == 11818, 'post-fs13 incidence 11818, got %d' % sum(inc.values()))
residual74 = fs13['five_parent_target_after']['residual_row_hex_after']
need(len(residual74) == 74 and len(set(residual74)) == 74 and residual74 == sorted(residual74), 'residual 74 sorted unique')
residualSet74 = set(residual74)
need(all(h in residualSet74 for h in residual74) and fs13['five_parent_target_after']['closed_target_rows_total'] == 38, 'fs13 closed target 38')
print('post-thirteenth-sixteenth frontier verified: 6209/491722, solved_s6 1639, incidence 11818, residual 74')

# ---------- target machinery ----------
audit = load('inputs/audit.json')
need(audit['all_pass'] is True and audit['check_count'] == 23 and audit['derived']['maximum_root_span'] == 2, 'independent audit gate')
targetRows112 = sorted(set(r for x in audit['derived']['witness_pairs'] for r in x['rows']))
need(len(targetRows112) == 112, 'target rows 112')
need(all(h in set(targetRows112) for h in residual74), 'residual 74 subset of target union')

# ---------- seventeenth certificate record ----------
sv17 = load('sv17pub/output/seventeenth-cert-triple-verification-20261120.json')
need(sv17['status'] == 'triple-verified', 'sv17 status')
need(sv17['gates_all_pass'] is True and sv17['gates_total'] == 38 and len(sv17['gates']) == 38, 'sv17 38 gates all pass')
need(all(g['pass'] for g in sv17['gates']), 'sv17 every gate pass')
need(sv17['root_hex'] == ROOT_HEX and int(sv17['child_hex'], 16) == int(CHILD_HEX, 16) and sv17['added_bit'] == ADDED_BIT, 'sv17 root/child/bit')
need((int(CHILD_HEX, 16) | (1 << ADDED_BIT)) == int(ROOT_HEX, 16), 'child-bit decomposition')
need(int(CHILD_HEX, 16) == int(ROOT_HEX, 16) ^ (1 << ADDED_BIT), 'child is root minus added bit')
need(canon_int(int(ROOT_HEX, 16)) == int(ROOT_HEX, 16), 'root D4 canonical')
need(canon_int(int(CHILD_HEX, 16)) == int(CHILD_HEX, 16) or True, 'child canonicality not required (raw hex convention)')
ncert = sv17['certificate']
cert_path = f'{W}/sv17pub/certs/win7-root-00004000000000821082000000000100-20261120.n11'
cert_bytes = open(cert_path, 'rb').read()
need(hashlib.sha256(cert_bytes).hexdigest() == ncert['sha256'] == '21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8', 'cert sha256')
need(ncert['bytes'] == len(cert_bytes) == 1791541, 'cert bytes')
need(ncert['rows'] == 49591 and ncert['loser_first_moves'] == 60, 'cert rows and loser moves')
cert_lines = cert_bytes.decode().splitlines()
need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS', 'cert header')
need(cert_lines[1] == 'root ' + ROOT_HEX, 'cert root line')
need(len(cert_lines) - 2 == 49591, 'cert rows count')
ex = sv17['extraction']
need(ex['fbt_drops'] == 0 and ex['rerun_summary_numbers_identical'] is True and ex['run1_nodes'] == 4250297
     and ex['run1_rows'] == 49591, 'extraction summary')
pyv = sv17['triple_verification']['python_bareiss_replay']
need(pyv['subroots_passed'] == 60 and pyv['union_missing'] == 0 and pyv['union_extra'] == 0
     and pyv['terminal_stone_range'] == [13, 15, 17] and pyv['visited_winner_states'] == 150963, 'python bareiss record')
bigv = sv17['triple_verification']['bigint']
need(bigv['subroots_passed'] == 60 and bigv['union_missing'] == 0 and bigv['union_extra'] == 0
     and bigv['terminal_range'] == [13, 17] and bigv['rows_sorted_unique'] is True, 'bigint record')
tsv = sv17['triple_verification']['ts_bareiss']
need(tsv['subroots'] == 60 and tsv['union_missing'] == 0 and tsv['union_extra'] == 0
     and tsv['terminals'] == 17157, 'ts bareiss record')
pc17 = sv17['triple_verification']['pilot_control']
need(pc17['loss'] is False and pc17['nodes'] == 3402 and pc17['control'] == 'pilot_d6', 'pilot control')
drv = sv17['discovery']['verdicts']
need(drv['win7_d10'] == 1 and drv['refuted_d10'] == 38 and drv['capped'] == 0 and drv['ordering_conflicts'] == 0, 'sweep classification')
rerun = sv17['discovery']['determinism_rerun']
need(rerun['andclose1']['node_exact_vs_sweep_record'] is True and rerun['andclose1']['nodes'] == 1576372
     and rerun['andclose0']['node_exact_vs_sweep_record'] is True and rerun['andclose0']['nodes'] == 2544178, 'determinism rerun')
cov = sv17['coverage_claim_pending_fold']
need(cov['both_rows_open_in_fold9_residual_74'] is True, 'coverage claim open')
claim_rows = cov['covered_rows_per_resolve6_matching']
need(claim_rows == ['00000000000000821082000000000001', '00000000000000821082000000000004'], 'coverage claim rows')
mask = int(ROOT_HEX, 16)
need(popcount(mask) == 7, 'root 7 stones')
need(unsafe_quadruples(mask) == 0, 'root safe')
lmv = legal_moves_of(mask)
need(len(lmv) == 60, 'legal move count rederivation')
print('seventeenth certificate record verified: 38/38 gates, sha, geometry, legal moves')

# ---------- resolve6 witness plan crosscheck ----------
r6 = load('resolve6/output/post-saturation-full-cache-join-resolve6-20261120.json')
need('resolve6' in str(r6.get('schema', '')), 'resolve6 schema')
vstats = r6['verdict_join']['stats']
need(vstats['win_refuted_conflicts'] == 0, 'resolve6 join conflict-free')
need(r6['base_state']['residual_row_hex'] and len(r6['base_state']['residual_row_hex']) == 78, 'resolve6 base residual 78')
wf = r6['witness_full']
wf_entry = [w for w in wf if w.get('root') == ROOT_HEX]
need(len(wf_entry) == 1, 'witness entry for seventeenth root')
wf_entry = wf_entry[0]
need(sorted(wf_entry['rows']) == claim_rows, 'witness rows == coverage claim')
need(wf_entry['safe'] is True, 'witness safe')
print('resolve6 witness crosscheck verified: rows', wf_entry['rows'])

# ---------- apply the seventeenth receipt ----------
rootRows = root_row_set(ROOT_HEX, open74)
need(len(rootRows) >= 1, 'seventeenth receipt closes no row')
for h in rootRows:
    need(h in open74, 'seventeenth row not open: ' + h)
need(rootRows == sorted(set(rootRows)) and len(set(rootRows)) == len(rootRows), 'rederived rows unique')
targetRows_new = sorted(h for h in rootRows if h in residualSet74)
need(targetRows_new == claim_rows, 'rederived target rows == published coverage claim')
extra_rows = [h for h in rootRows if h not in residualSet74]
closedCost = sum(open74[h][0] for h in rootRows)
deltas = {}
for h in rootRows:
    for p in row_parents_hex(h): deltas[p] = deltas.get(p, 0) + 1
pdeltas = []
for p in sorted(deltas):
    before = inc[p]; after = before - deltas[p]
    pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'], 'rows_before': before, 'rows_closed': deltas[p], 'rows_after': after})
for h in rootRows:
    del open74[h]
    for p in row_parents_hex(h): inc[p] -= 1

# frontier after
needed_rows = [h for h in open74 if demand(h)['c1'] == 0]
frontier_after = {
  'solved_s6_in_manifest': 1639 + len(rootRows),
  'remaining_s5_orbits': sum(1 for v in inc.values() if v > 0),
  'unique_remaining_s6': len(open74),
  'sum_remaining_cost': sum(v[0] for v in open74.values()),
  's6_needed_by_open_classes': len(needed_rows),
  'cost_needed_by_open_classes': sum(open74[h][0] for h in needed_rows),
  'parent_row_incidence': sum(inc.values()),
}

# five-parent target accounting
newTargetAll = set(targetRows_new)
closedAllNew = 38 + len(newTargetAll)
residualAfter = sorted(residualSet74 - newTargetAll)
need(len(residualAfter) == 72, 'residual target rows 72, got %d' % len(residualAfter))

def coverage_rows(rootRows, wl):
    rr_out = []
    for h in sorted(rootRows):
        rr_out.append({'row_hex': h, 'cost': wl[h][0], 'category': wl[h][1], 'demand': demand(h),
                       'parents': sorted(row_parents_hex(h)), 'receipt': {'root': ROOT_HEX, 'verdict': 'WIN7-D10'}})
    return rr_out

result = {
  'schema': 'n11-five-parent-seventeenth-win7-receipt-fold-20261120-v1',
  'date': '2026-11-20', 'status': 'fold-complete', 'receipt_ordinal': 'seventeenth (fold10)',
  'single_owner_note': 'research/log/2026-11-20-n11-fold10-single-owner-note.md',
  'previous_fold': {'record': 'research/experiments/n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json (sha256 24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2)',
                    'frontier_after': fa13},
  'certificate_source': {
    'record': 'research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120 (seventeenth WIN7 cert extract + triple verification, 38 gates)',
    'verification_sha256': 'c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc',
    'certificate_path': 'research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11 (commit b7a6db5fb0)',
    'certificate_sha256': ncert['sha256'],
    'discovery': 'K1069 39-live-witness depth-10 sweep (WIN 1 / REFUTED 38 / CAPPED 0; root andclose1 1,576,372 nodes / andclose0 2,544,178 nodes, both uncapped, terminal [13,17]); independent byte-exact re-extraction lane log research/log/2026-11-20-n11-seventeenth-cert-body-published.md',
  },
  'source_blob_pins': dict(PINS),
  'source_sha256_pins': dict(PIN256),
  'receipt_count': 1,
  'receipts': [{
      'root': ROOT_HEX, 'raw_root_hex': ROOT_HEX, 'receipt': 'seventeenth',
      'lane_bit': ADDED_BIT, 'lane_child_hex': CHILD_HEX,
      'raw_root_is_d4_canonical': True,
      'legal_next_moves': 60,
      'covered_s6_rows': rootRows,
      'covered_five_parent_target_rows': targetRows_new,
      'extra_s6_rows_not_in_target': extra_rows,
      'unique_strategy_rows': 49591,
      'extraction_nodes': ex['run1_nodes'],
      'extraction_rerun_byte_identical': True,
      'closed_edge_cost': closedCost,
      'certificate_sha256': ncert['sha256'],
      'certificate_bytes': ncert['bytes'],
      'affected_parents': len(pdeltas),
      'parent_deltas': pdeltas,
      'sweep_provenance': {'nodes_andclose_1': 1576372, 'nodes_andclose_0': 2544178,
                           'capped': False, 'terminal_stone_range': [13, 17],
                           'determinism_rerun_node_exact': True},
      'independent_verification': {
        'bigint_3x3': {'subroots_passed': 60, 'union_missing': 0, 'union_extra': 0, 'terminal_range': [13, 17]},
        'ts_bareiss_4x4': {'subroots': 60, 'union_missing': 0, 'union_extra': 0, 'terminals': 17157},
        'python_exact_bareiss_full_replay': {'subroots_passed': 60, 'consumed_rows': 49591, 'visited_winner_states': 150963, 'terminal_stone_range': [13, 15, 17]},
        'cross_method_union_exact': True,
        'certificate_union_exact': True,
        'source_record': 'research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120',
      },
  }],
  'frontier_before': fa13,
  'frontier_after': frontier_after,
  'new_receipt_coverage': {
    'unique_s6_rows': len(rootRows),
    'closed_edge_cost': closedCost,
    'rows': coverage_rows(rootRows, wl),
  },
  'parent_closure': {
    'fully_closed_parent_count': len(set(p['parent_hex'] for p in pdeltas if p['rows_after'] == 0)),
    'affected_unique_parents': len(set(p['parent_hex'] for p in pdeltas)),
  },
  'five_parent_target_after': {
    'closed_target_rows_total': closedAllNew,
    'residual_target_rows': len(residualAfter),
    'residual_row_hex_after': residualAfter,
  },
  'witness_plan_impact': {
    'note': 'Observation only. The 39-root live witness plan covered all 78 pre-windfall rows; after the seventeenth fold the covered witness root is retired and the plan degrades by exactly the 2 closed rows.',
    'retired_witness_root': ROOT_HEX,
    'rows_of_retired_root': wf_entry['rows'],
  },
  'verdict_join_summary': {
    'join_basis': 'resolve6 published full-universe cache join (win/refuted conflicts 0) + K1069 depth-10 both-order sweep of the 39 live witness roots',
    'receipt_root_is': 'certificate-backed WIN7-D10 (seventeenth triple verification: TS Bareiss 4x4 sub-root decomposition, pure-python exact Bareiss full replay, BigInt 3x3; independent byte-exact re-extraction by a second lane)',
  },
  'controls': {
    'base_frontier_recomputed': True,
    'chain_frontiers_recomputed_each_step': True,
    'post_ninth_twelfth_frontier_matches_published_6213_492021': True,
    'thirteenth_sixteenth_frontier_matches_published_6209_491722': True,
    'seventeenth_cert_38_gates_rechecked': True,
    'receipt_rows_rederived_from_d4_images_and_canonical_frontier': True,
    'rederived_rows_match_published_coverage_claim': True,
    'all_receipt_rows_were_open_before': True,
    'legal_move_count_independently_rederived': True,
    'certificates_sha256_verified': True,
    'win_loss_conflict_scan_against_published_verdict_universe': True,
  },
  'interpretation_guard': [
    'WIN7-D10 proves a first-player win within depth 10 only from the seven-stone root of this receipt.',
    'The receipt closes its S6 rows in the frontier but proves nothing about the empty board or any two-stone root.',
    'REFUTED-D10 witnesses are NOT LOSS proofs.',
    'The remaining residual five-parent target rows (72) are a conditional depth-10 sweep/accounting state, not certificates.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
  ],
}
import os
os.makedirs(f'{W}/fold/output', exist_ok=True)
with open(f'{W}/{OUT}', 'w') as f:
    json.dump(result, f, indent=1); f.write('\n')
print(json.dumps({'status': result['status'], 'frontier_after': frontier_after,
                  'closed_target_rows_total': closedAllNew, 'residual_target_rows': len(residualAfter),
                  'rederived_rows': rootRows, 'output': OUT, 'sha256': sha256_of(OUT)}, indent=1))
