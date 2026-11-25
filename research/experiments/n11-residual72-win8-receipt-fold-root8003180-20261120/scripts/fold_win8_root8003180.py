#!/usr/bin/env python3
# Receipt fold (fold11, eighteenth receipt) of the WIN8-D10 certificate of root
# 00000000000000003800000008003180 (K1096: extraction + triple verification, 18-gate
# record sha256 ad0d9fb3...; certificate sha256 13931289...) into the five-parent
# S6 frontier chain -- the first WIN8 receipt fold.
#
# The frontier/base chain is reconstructed exactly as in the published
# fold_seventeenth.py machine (worklist -> ledger/globalFold -> cost78c/79c ->
# first -> second/third -> fourth -> fifth/sixth -> seventh -> eighth ->
# ninth-twelfth -> fs13 thirteenth..sixteenth), then the published fold10
# (seventeenth) record is chained from its pinned SHA-256, giving the open set
# 6,206 rows / 491,497 cost, solved S6 1,642, parent incidence 11,810 and the
# residual-72 five-parent target (published fold10 values). The WIN8 receipt is
# then applied: the covered S6 rows of the root are rederived geometrically by
# two independent methods -- (A) the fold-chain convention of 8 D4 images with
# C(8,2) two-stone removals (224 operations) and (B) the refsolve
# coverage_of82 convention of the C(8,6)=28 six-stone subsets of the root --
# whose canonical row sets must be equal (D4-equivariance) and whose
# intersection with the open frontier is the receipt closure.
#
# All chain and certificate inputs are fail-closed SHA-pinned.  Bookkeeping
# only: WIN8-D10 proves only the game tree of the eight-stone root; REFUTED-D10
# is not a LOSS proof; no game value near the empty board is asserted.
# 11x11 empty board / two-stone roots remain UNKNOWN.
#
# W-relative input path -> published repo path map (identical chain inputs as
# fold_seventeenth.py, plus):
#   fold10/output/seventeenth-win7-receipt-fold-20261120.json
#       research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json
#   k1096/output/win8-cert-extract-verification-20261120.json
#       research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/output/win8-cert-extract-verification-20261120.json
#   k1096/certs/win8-root-00000000000000003800000008003180-20261120.n11
#       research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/certs/win8-root-00000000000000003800000008003180-20261120.n11
#   k1097/output/safe8-refuted50-refsolve-20261120.json
#       research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json
#
# Usage: python3 fold_win8_root8003180.py  (env FOLD11_W overrides the W root)
import json, sys, os, hashlib, tarfile, csv
from itertools import combinations

W = os.environ.get('FOLD11_W', '/home/user/work/w8003180fold/W')
OUT = 'fold/output/win8-root8003180-receipt-fold-20261120.json'
ROOT_HEX = '00000000000000003800000008003180'
CERT_RELPATH = 'k1096/certs/win8-root-00000000000000003800000008003180-20261120.n11'

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
 'fold10/output/seventeenth-win7-receipt-fold-20261120.json': 'bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a',
 'k1096/output/win8-cert-extract-verification-20261120.json': 'ad0d9fb3a30edbd76fcb5562ab01f1e7e51781381377a04fa4a195378eb887da',
 'k1096/certs/win8-root-00000000000000003800000008003180-20261120.n11': '1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c',
 'k1097/output/safe8-refuted50-refsolve-20261120.json': '2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40',
}

for k, s in PINS.items():
    need(blob_sha(f'{W}/{k}') == s, f'input blob mismatch {k}')
for k, s in PIN256.items():
    need(sha256_of(k) == s, f'input sha256 mismatch {k}')
print('all', len(PINS) + len(PIN256), 'input pins verified')

# ---------- legal move machinery (verbatim published source, part 1) ----------
legal_moves_of_src = open(f'{W}/fold_fourth_fifth_sixth.py').read().split('# ---------- pinned inputs')[0]
_ns = {}; exec(legal_moves_of_src, _ns); legal_moves_of = _ns['legal_moves_of']

# ---------- frontier reconstruction chain (identical to fold_seventeenth) ----------
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
need(fs13['five_parent_target_after']['closed_target_rows_total'] == 38, 'fs13 closed target 38')

# ---------- target machinery ----------
audit = load('inputs/audit.json')
need(audit['all_pass'] is True and audit['check_count'] == 23 and audit['derived']['maximum_root_span'] == 2, 'independent audit gate')
targetRows112 = sorted(set(r for x in audit['derived']['witness_pairs'] for r in x['rows']))
need(len(targetRows112) == 112, 'target rows 112')
need(all(h in set(targetRows112) for h in residual74), 'residual 74 subset of target union')

# ---------- fold10 (seventeenth) record chaining ----------
f10 = load('fold10/output/seventeenth-win7-receipt-fold-20261120.json')
need(f10['status'] == 'fold-complete', 'fold10 fold-complete')
need(f10['schema'] == 'n11-five-parent-seventeenth-win7-receipt-fold-20261120-v1', 'fold10 schema')
need(f10['receipt_count'] == 1 and len(f10['receipts']) == 1, 'fold10 receipt count')
rc10 = f10['receipts'][0]
rows10 = list(rc10['covered_s6_rows'])
need(len(rows10) == len(set(rows10)) == 3, 'fold10 covered rows unique 3')
for h in rows10:
    need(h in open74, 'fold10 row not open: ' + h)
open72 = {h: v for h, v in open74.items() if h not in set(rows10)}
fa10 = f10['frontier_after']
need(len(open72) == 6206 and sum(v[0] for v in open72.values()) == 491497, 'post-fold10 frontier (must match published 6206/491497)')
need(fa10['unique_remaining_s6'] == 6206 and fa10['sum_remaining_cost'] == 491497
     and fa10['solved_s6_in_manifest'] == 1642 and fa10['parent_row_incidence'] == 11810, 'fold10 frontier_after published values')
for rec_row in f10['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold10 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows10, 'fold10 coverage row among covered')
need(rc10['closed_edge_cost'] == sum(wl[h][0] for h in rows10), 'fold10 closed edge cost recomputed')
for h in rows10:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11810, 'post-fold10 incidence 11810, got %d' % sum(inc.values()))
targetRows10 = list(rc10['covered_five_parent_target_rows'])
need(set(targetRows10) <= residualSet74 and len(targetRows10) == 2, 'fold10 target rows subset of residual74')
extra10 = [h for h in rows10 if h not in residualSet74]
need(extra10 == rc10['extra_s6_rows_not_in_target'], 'fold10 extra rows recorded')
residual72 = f10['five_parent_target_after']['residual_row_hex_after']
need(len(residual72) == 72 and len(set(residual72)) == 72 and residual72 == sorted(residual72), 'residual 72 sorted unique')
need(sorted(residualSet74 - set(targetRows10)) == residual72, 'residual72 == residual74 minus fold10 target rows')
need(f10['five_parent_target_after']['closed_target_rows_total'] == 40, 'fold10 closed target 40')
residualSet72 = set(residual72)
need(all(h in open72 for h in residual72), 'residual72 rows open in frontier')
print('post-fold10 frontier verified: 6206/491497, solved_s6 1642, incidence 11810, residual 72')

# ---------- K1096 certificate record (18 gates) ----------
k1096 = load('k1096/output/win8-cert-extract-verification-20261120.json')
need(k1096['schema'] == 'win8-cert-extract-verification-v1', 'k1096 schema')
need(k1096['all_gates_pass'] is True and k1096['gate_count'] == 18 and len(k1096['gates']) == 18, 'k1096 gate count')
need(all(g['passed'] for g in k1096['gates']), 'k1096 every gate passed')
need(k1096['root'] == ROOT_HEX, 'k1096 root hex')
gate07 = [g for g in k1096['gates'] if g['gate'] == 'g07_k1086_root_claimed_coverage_4rows']
need(len(gate07) == 1, 'g07 present')
CLAIM = sorted(gate07[0]['detail'])
need(CLAIM == sorted(k1096['recorded']['k1086_claimed_coverage_rows']), 'k1096 claim rows consistent')
gate05 = [g for g in k1096['gates'] if g['gate'] == 'g05_root_mobility_53'][0]
need(gate05['detail'] == 53 and gate05['passed'] is True, 'k1096 mobility 53')
cert_recd = k1096['recorded']['certificate']
cert_bytes = open(f'{W}/{CERT_RELPATH}', 'rb').read()
need(hashlib.sha256(cert_bytes).hexdigest() == cert_recd['sha256'] == PIN256[CERT_RELPATH], 'k1096 cert sha256')
need(cert_recd['bytes'] == len(cert_bytes) == 1251923, 'k1096 cert bytes')
need(cert_recd['rows'] == 34529, 'k1096 cert rows')
cert_lines = cert_bytes.decode().splitlines()
need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'k1096 cert header')
need(cert_lines[1] == 'root ' + ROOT_HEX, 'k1096 cert root line')
need(len(cert_lines) - 2 == 34529, 'k1096 cert row count')
data_rows = cert_lines[2:]
need(all(len(x.split(' ')) == 2 and len(x.split(' ')[0]) == 32 for x in data_rows), 'k1096 cert row format')
need(data_rows == sorted(data_rows) and len(set(data_rows)) == len(data_rows), 'k1096 cert rows sorted unique')
tm = k1096['recorded']['third_method']
need(tm['root_first_moves'] == 53 and tm['terminal_count'] == 13364 and tm['terminal_range'] == [14, 18]
     and tm['visited_states'] == 76955 and tm['winner_states'] == 49509 and tm['loser_states'] == 14082
     and tm['loser_reply_edges'] == 67420, 'k1096 third-method aggregate')

# ---------- K1096 geometry independent rederivation ----------
mask = int(ROOT_HEX, 16)
need(popcount(mask) == 8, 'root 8 stones')
need(unsafe_quadruples(mask) == 0, 'root safe')
need(canon_int(mask) == mask, 'root D4 canonical')
lmv = legal_moves_of(mask)
need(len(lmv) == 53, 'root legal move count rederivation 53')
print('K1096 certificate record verified: 18/18 gates, sha, header, geometry, mobility 53')

# ---------- K1097 refsolve claim crosscheck ----------
k1097 = load('k1097/output/safe8-refuted50-refsolve-20261120.json')
need(k1097['status'] == 'refsolve-computed', 'k1097 status')
need(len(k1097['gates']) == 27 and all(g['ok'] for g in k1097['gates']), 'k1097 gates all ok')
foot = k1097['win16_intrinsic_footprints']
need(ROOT_HEX in foot, 'k1097 footprint has root')
need(foot[ROOT_HEX]['intrinsic_equals_claimed'] is True, 'root intrinsic == claimed')
need(sorted(foot[ROOT_HEX]['claimed']) == CLAIM, 'footprint claimed == K1096 claim')
need(sorted(foot[ROOT_HEX]['intrinsic']) == CLAIM, 'footprint intrinsic == K1096 claim')
need(len(foot) == 16, 'win16 footprint count')
all_claims = []
for r in foot:
    need(len(foot[r]['claimed']) == len(set(foot[r]['claimed'])), 'claimed rows unique per root')
    all_claims.extend(foot[r]['claimed'])
need(len(all_claims) == 49 and len(set(all_claims)) == 49, 'win16 claims total 49 distinct')
claim_count = {h: 0 for h in set(all_claims)}
for r in foot:
    for h in foot[r]['claimed']: claim_count[h] += 1
need(all(v == 1 for v in claim_count.values()), 'win16 claims exactly-once partition')
need(all(h in residualSet72 for h in CLAIM), 'claim rows inside residual72')
scope1 = k1097['scope1_refsolve_residual23']
need(ROOT_HEX not in [s['root'] for s in scope1['greedy_selection']], 'root not in residual23 greedy selection')
residual23 = k1097['exclusion']['residual23_rows']
need(sorted(residual23) == residual23 and len(residual23) == 23, 'residual23 sorted')
need(not (set(residual23) & set(all_claims)), 'residual23 disjoint from win16 claims')
need(not (set(residual23) & set(CLAIM)), 'residual23 untouched by this receipt')
print('K1097 refsolve record crosscheck verified: 27 gates, footprint partition, plan untouched')

# ---------- WIN8 receipt geometry: two independent methods ----------
# Method A: fold-chain convention -- 8 D4 images x C(8,2) two-stone removals.
rootA = set()
for t in range(8):
    image = transform(mask, t)
    sb = bits_of(image)
    for b1, b2 in combinations(sb, 2):
        c = canon_int(image ^ (1 << b1) ^ (1 << b2))
        rootA.add(format(c, '032x'))
# Method B: refsolve coverage_of82 convention -- C(8,6)=28 six-stone subsets.
rootB = set()
stones = bits_of(mask)
for six in combinations(stones, 6):
    smask = 0
    for b in six: smask |= 1 << b
    rootB.add(canon_hex(smask))
need(rootA == rootB, 'methods A and B canonical row sets equal (D4 equivariance)')
need(len(rootB) <= 28, 'subset count bound')
opsA = 8 * 28
print('WIN8 receipt geometry verified: method A (%d ops) == method B (%d subsets), %d canonical rows' % (opsA, 28, len(rootB)))

# classification of every canonical row of the root's 6-stone subgeometry
closedHistorical = set()
closedHistorical |= old66 | oldGlobal | prior
closedHistorical |= firstClosed | set(rows23) | set(rows4) | set(rows56)
closedHistorical |= set(rows7) | set(rows8) | set(rows9) | set(rows13_16) | set(rows10)
row_class = {}
for h in sorted(rootB):
    if h in open72: row_class[h] = 'open-frontier'
    elif h in closedHistorical: row_class[h] = 'closed-before-this-receipt'
    elif h in wl: row_class[h] = 'worklist-but-not-open'   # impossible if chain is exact
    else: row_class[h] = 'not-in-worklist'
for h, cls in row_class.items():
    need(cls != 'worklist-but-not-open', 'chain inconsistency on row ' + h)

rootRows = sorted(h for h in rootA if h in open72)
need(len(rootRows) >= 1, 'WIN8 receipt closes no open row')
need(rootRows == sorted(set(rootRows)), 'rederived rows unique')
targetRows_new = sorted(h for h in rootRows if h in residualSet72)
need(targetRows_new == CLAIM, 'rederived target rows == published claim')
extra_rows = [h for h in rootRows if h not in residualSet72]
closedCost = sum(open72[h][0] for h in rootRows)

# apply the receipt
deltas = {}
for h in rootRows:
    for p in row_parents_hex(h): deltas[p] = deltas.get(p, 0) + 1
pdeltas = []
for p in sorted(deltas):
    before = inc[p]; after = before - deltas[p]
    pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'], 'rows_before': before, 'rows_closed': deltas[p], 'rows_after': after})
for h in rootRows:
    del open72[h]
    for p in row_parents_hex(h): inc[p] -= 1

# frontier after
needed_rows = [h for h in open72 if demand(h)['c1'] == 0]
frontier_after = {
  'solved_s6_in_manifest': 1642 + len(rootRows),
  'remaining_s5_orbits': sum(1 for v in inc.values() if v > 0),
  'unique_remaining_s6': len(open72),
  'sum_remaining_cost': sum(v[0] for v in open72.values()),
  's6_needed_by_open_classes': len(needed_rows),
  'cost_needed_by_open_classes': sum(open72[h][0] for h in needed_rows),
  'parent_row_incidence': sum(inc.values()),
}

# five-parent target accounting
newTargetAll = set(targetRows_new)
closedAllNew = 40 + len(newTargetAll)
residualAfter = sorted(residualSet72 - newTargetAll)
need(len(residualAfter) == 72 - len(targetRows_new), 'residual accounting')

def coverage_rows(rootRows, wl):
    rr_out = []
    for h in sorted(rootRows):
        rr_out.append({'row_hex': h, 'cost': wl[h][0], 'category': wl[h][1], 'demand': demand(h),
                       'parents': sorted(row_parents_hex(h)), 'receipt': {'root': ROOT_HEX, 'verdict': 'WIN8-D10'}})
    return rr_out

result = {
  'schema': 'n11-five-parent-win8-root8003180-receipt-fold-20261120-v1',
  'date': '2026-11-20', 'status': 'fold-complete', 'receipt_ordinal': 'eighteenth (fold11, first WIN8 receipt fold)',
  'single_owner_note': 'research/log/2026-11-20-n11-fold11-win8-root8003180-single-owner-note.md',
  'previous_fold': {'record': 'research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json (sha256 bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a)',
                    'frontier_after': fa10},
  'certificate_source': {
    'record': 'research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120 (K1096: WIN8 root certificate extract + triple verification, 18 gates)',
    'verification_sha256': PIN256['k1096/output/win8-cert-extract-verification-20261120.json'],
    'certificate_path': 'research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/certs/win8-root-00000000000000003800000008003180-20261120.n11',
    'certificate_sha256': cert_recd['sha256'],
    'claims_record': 'research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json (K1097; sha256 ' + PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'] + '; win16_intrinsic_footprints: intrinsic == claimed == 4 rows)',
  },
  'source_blob_pins': dict(PINS),
  'source_sha256_pins': dict(PIN256),
  'receipt_count': 1,
  'receipts': [{
      'root': ROOT_HEX, 'raw_root_hex': ROOT_HEX, 'receipt': 'eighteenth',
      'stones': 8, 'verdict': 'WIN8-D10',
      'legal_next_moves': 53,
      'covered_s6_rows': rootRows,
      'covered_five_parent_target_rows': targetRows_new,
      'extra_s6_rows_not_in_target': extra_rows,
      'unique_strategy_rows': 34529,
      'certificate_sha256': cert_recd['sha256'],
      'certificate_bytes': cert_recd['bytes'],
      'closed_edge_cost': closedCost,
      'affected_parents': len(pdeltas),
      'parent_deltas': pdeltas,
      'independent_verification': {
        'extraction_and_triple': {'gates': 18, 'all_pass': True,
          'methods': ['extraction self-check A1/A2/B byte-identical', 'BigInt 3x3 cofactor', 'Bareiss 4x4', 'python third-method exact traversal'],
          'third_method_aggregates': tm},
        'coverage_geometry_two_methods': {'d4_images_two_stone_removals_ops': opsA, 'c86_subsets': 28,
          'canonical_row_sets_equal': True, 'canonical_rows': sorted(rootB)},
        'cross_method_union_exact': True,
        'source_record': 'research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120',
      },
  }],
  'frontier_before': fa10,
  'frontier_after': frontier_after,
  'new_receipt_coverage': {
    'unique_s6_rows': len(rootRows),
    'closed_edge_cost': closedCost,
    'rows': coverage_rows(rootRows, wl),
  },
  'six_stone_subgeometry_classification': {h: row_class[h] for h in sorted(rootB)},
  'parent_closure': {
    'fully_closed_parent_count': len(set(p['parent_hex'] for p in pdeltas if p['rows_after'] == 0)),
    'affected_unique_parents': len(set(p['parent_hex'] for p in pdeltas)),
  },
  'five_parent_target_after': {
    'closed_target_rows_total': closedAllNew,
    'residual_target_rows': len(residualAfter),
    'residual_row_hex_after': residualAfter,
  },
  'win_candidate_plan_impact': {
    'note': 'Observation only. The K1097 plan grouped 16 WIN8-D10 candidates (claims 49 rows, exactly-once partition) with 9 alternative roots (residual 23 rows). This receipt closes the 4 claimed rows of root 8003180; the remaining 15 WIN8 candidates keep 45 claimed rows, the residual-23 alternative sweep plan (depth-10 round 5, separately declared owner) is untouched: its rows are disjoint from every WIN16 claim, machine-checked.',
    'retired_win_candidate_root': ROOT_HEX,
    'rows_of_retired_root': CLAIM,
    'win16_candidates_remaining': 15,
    'win16_claimed_rows_remaining': 45,
    'residual23_untouched': True,
  },
  'verdict_join_summary': {
    'join_basis': 'published fold10 chain frontier (byte-exact rerun of fold_seventeenth.py verified) + K1096 triple-verified WIN8 certificate + K1097 refsolve coverage footprints',
    'receipt_root_is': 'certificate-backed WIN8-D10 (K1096: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 18-gate record)',
  },
  'controls': {
    'base_frontier_recomputed': True,
    'chain_frontiers_recomputed_each_step': True,
    'fold10_rerun_byte_identical_upstream_of_this_fold': True,
    'fold10_frontier_6206_491497_recomputed_from_worklist': True,
    'post_fold10_incidence_11810_recomputed': True,
    'k1096_cert_18_gates_rechecked_and_bytes_verified': True,
    'k1097_refsolve_27_gates_rechecked': True,
    'coverage_rederived_from_d4_images_and_subsets_two_methods': True,
    'rederived_target_rows_match_published_claim': True,
    'all_receipt_rows_were_open_before': True,
    'coverage_of_historical_closed_set_empty': True,
    'win16_claim_partition_exactly_once_rechecked': True,
    'legal_move_count_independently_rederived': True,
    'certificates_sha256_verified': True,
  },
  'interpretation_guard': [
    'WIN8-D10 proves a first-player win within depth 10 only from the eight-stone root of this receipt.',
    'The receipt closes its S6 rows in the frontier through the published two-stone-removal cover convention (refsolve coverage_of82 / K1096 cover semantics); it proves nothing about the empty board or any two-stone root.',
    'The closed rows are a bookkeeping closure of the five-parent depth-10 receipt chain, not a LOSS proof of the rows.',
    'REFUTED-D10 witnesses are NOT LOSS proofs; node counts and solved counts are not win/loss readings.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
  ],
}
os.makedirs(f'{W}/fold/output', exist_ok=True)
with open(f'{W}/{OUT}', 'w') as f:
    json.dump(result, f, indent=1); f.write('\n')
print(json.dumps({'status': result['status'], 'frontier_after': frontier_after,
                  'closed_target_rows_total': closedAllNew, 'residual_target_rows': len(residualAfter),
                  'rederived_rows': rootRows, 'target_rows': targetRows_new, 'extra_rows': extra_rows,
                  'output': OUT, 'sha256': sha256_of(OUT)}, indent=1))
