#!/usr/bin/env python3
# Receipt fold of the four resolve6 "windfall" WIN7-D10 certificates
# (thirteenth..sixteenth receipts; class2-lane-cost65h child at bits
# 40/43/99/118) into the five-parent S6 frontier chain.
#
# The frontier/base chain is reconstructed from the pinned published blobs
# (worklist -> ledger/globalFold -> cost78c/79c -> first -> second/third ->
# fourth -> fifth/sixth -> seventh -> eighth -> ninth-twelfth), then the four
# certificate-backed receipts are applied to the published post-ninth-twelfth
# state (open 6,213 rows / cost 492,021; five-parent residual target 78).
#
# Certificate inputs are the K1066 published, triple-verified certificates
# (verification record SHA-256 a3ca1b3d...); this machine re-checks certificate
# bytes, root geometry, legal-move counts, covered-row sets, and every chain
# count fail-closed before writing the fold record.
#
# Bookkeeping only: REFUTED-D10 is not a LOSS proof; no game value near the
# empty board is asserted. 11x11 empty board / two-stone roots remain UNKNOWN.
#
# W-relative input path -> published repo path map:
#   inputs/worklist.csv          research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv
#   inputs/ledger.json           research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json
#   inputs/globalFold.json       research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-receipt-harvest-global-fold-20261118.json
#   inputs/previousCostFold.json research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78c-79c-receipts-recompute-20261118.json
#   inputs/firstFoldTarball.tar.gz  research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/first-win7-root-evidence-20261119.tar.gz
#   inputs/census.json          research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json
#   inputs/audit.json           research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-cover-cost16-five-parent-independent-audit-20261118.json
#   ex48/output/secondThirdFold.json  research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/second-third-win7-root-receipt-fold-20261119.json
#   fold4rec/fold4.json         research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/output/fourth-win7-root-receipt-fold-20261119.json
#   fold56rec/fold56.json       research/experiments/n11-head1410-fifth-sixth-win7-receipt-fold-20261119/output/fifth-sixth-win7-root-receipt-fold-20261119.json
#   foldv2/output/seventh-win7-receipt-fold-20261119.json   research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/seventh-win7-receipt-fold-20261119.json
#   foldv2/output/eighth-win7-receipt-fold-20261119.json    research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/eighth-win7-receipt-fold-20261119.json
#   fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json  research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/ninth-twelfth-win7-receipt-fold-20261119.json
#   resolve6/output/post-saturation-full-cache-join-resolve6-20261120.json  research/experiments/n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json
#   windfall4pub/output/windfall4-cert-triple-verification-20261120.json  research/experiments/n11-residual78-windfall4-cert-extract-20261120/output/windfall4-cert-triple-verification-20261120.json
#   windfall4pub/certs/win7-root-<raw>-20261120.n11  research/experiments/n11-residual78-windfall4-cert-extract-20261120/certs/win7-root-<raw>-20261120.n11
#   fold_fourth_fifth_sixth.py  research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/fold_fourth_fifth_sixth.py (geometry part 1 only, pinned by blob sha)
#
# Usage: python3 fold_thirteenth_sixteenth.py
import json, sys, hashlib, tarfile, csv

W = '/home/user/work/n11windfall'
OUT = 'fold13/output/thirteenth-sixteenth-win7-receipt-fold-20261120.json'

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
 'windfall4pub/output/windfall4-cert-triple-verification-20261120.json': 'a3ca1b3dfd2fcdbd28fc88a6f993c4ff5ad81ee92d4a22800ff2f6477c476feb',
}
CERTS = [
 ('thirteenth', 40, '00000000000000803202010000001000'),
 ('fourteenth', 43, '00000000000000803202080000001000'),
 ('fifteenth', 99, '00000008000000803202000000001000'),
 ('sixteenth', 118, '00400000000000803202000000001000'),
]

for k, s in PINS.items():
    need(blob_sha(f'{W}/{k}') == s, f'input blob mismatch {k}')
for k, s in PIN256.items():
    need(sha256_of(k) == s, f'input sha256 mismatch {k}')
for _name, _bit, raw in CERTS:
    need(len(open(f'{W}/windfall4pub/certs/win7-root-{raw}-20261120.n11', 'rb').read()) > 0, f'missing cert {raw}')
print('all', len(PINS) + len(PIN256) + len(CERTS), 'input pins verified')

# ---------- legal move machinery (verbatim published source, part 1) ----------
legal_moves_of_src = open(f'{W}/fold_fourth_fifth_sixth.py').read().split('# ---------- pinned inputs')[0]
_ns = {}; exec(legal_moves_of_src, _ns); legal_moves_of = _ns['legal_moves_of']

# ---------- frontier reconstruction chain ----------
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
fa23 = stf['frontier_after']
need(fa23['unique_remaining_s6'] == 6229 and fa23['sum_remaining_cost'] == 493184
     and fa23['solved_s6_in_manifest'] == 1619 and fa23['parent_row_incidence'] == 11859, 'second-third frontier crosscheck')
fold4rec = load('fold4rec/fold4.json')
need(fold4rec['status'] == 'fold-complete' and fold4rec['schema'] == 'n11-five-parent-fourth-win7-receipt-fold-20261119-v1', 'fold4 record gate')
rows4 = [x['row_hex'] for x in fold4rec['new_receipt_coverage']['rows']]
open3 = {h: v for h, v in open2.items() if h not in set(rows4)}
fa4 = fold4rec['frontier_after']
need(len(open3) == 6226 and sum(v[0] for v in open3.values()) == 492970, 'fourth-fold frontier')
need(fa4['solved_s6_in_manifest'] == 1622 and fa4['parent_row_incidence'] == 11855 and fa4['remaining_s5_orbits'] == 173, 'fold4 frontier_after gate')
fold56rec = load('fold56rec/fold56.json')
need(fold56rec['status'] == 'fold-complete' and fold56rec['schema'] == 'n11-five-parent-fifth-sixth-win7-receipt-fold-20261119-v1', 'fold56 record gate')
rows56 = [x['row_hex'] for x in fold56rec['new_receipt_coverage']['rows']]
open4 = {h: v for h, v in open3.items() if h not in set(rows56)}
need(len(open4) == 6224 and sum(v[0] for v in open4.values()) == 492830, 'fifth-sixth-fold frontier')
fa56 = fold56rec['frontier_after']
need(fa56['solved_s6_in_manifest'] == 1624 and fa56['parent_row_incidence'] == 11852, 'fold56 frontier_after gate')
fold7 = load('foldv2/output/seventh-win7-receipt-fold-20261119.json')
need(fold7['status'] == 'fold-complete' and fold7['receipt_count'] == 1, 'fold7 gate')
rows7 = []
for rr in fold7['receipts']: rows7.extend(rr['covered_s6_rows'])
open5 = {h: v for h, v in open4.items() if h not in set(rows7)}
need(len(open5) == 6223 and sum(v[0] for v in open5.values()) == 492762, 'seventh-fold frontier')
need(fold7['frontier_after']['solved_s6_in_manifest'] == 1625 and fold7['frontier_after']['parent_row_incidence'] == 11850, 'fold7 frontier_after gate')
fold8 = load('foldv2/output/eighth-win7-receipt-fold-20261119.json')
need(fold8['status'] == 'fold-complete' and fold8['receipt_count'] == 1, 'fold8 gate')
rows8 = []
for rr in fold8['receipts']: rows8.extend(rr['covered_s6_rows'])
openCur = {h: v for h, v in open5.items() if h not in set(rows8)}
need(len(openCur) == 6222 and sum(v[0] for v in openCur.values()) == 492688, 'eighth-fold frontier (must match published 6222/492688)')
fa8 = fold8['frontier_after']
need(fa8['solved_s6_in_manifest'] == 1626 and fa8['parent_row_incidence'] == 11848 and fa8['s6_needed_by_open_classes'] == 4517
     and fa8['cost_needed_by_open_classes'] == 358189, 'fold8 frontier_after gate')
print('frontier chain verified: 6259/495507 -> 6240/493965 -> 6236/493703 -> 6229/493184 -> ... -> 6222/492688')

# ---------- census / parent machinery ----------
census = load('inputs/census.json')
parents = {p['hex']: p for p in census['open_s5_census']}
parents_int = {int(h, 16): h for h in parents}
need(len(parents) > 0, 'census parents loaded')
print('census parents:', len(parents))

_rowp_cache = {}
def row_parents_hex(h):
    if h in _rowp_cache: return _rowp_cache[h]
    mask = int(h, 16); ps = set()
    bl = bits_of(mask)
    for q in bl:
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
need(tf9['receipt_count'] == 4 and len(tf9['receipts']) == 4, 'fold9 receipts count')
rows9 = []
for rr in tf9['receipts']:
    need(len(rr['covered_s6_rows']) >= 1, 'fold9 receipt closes nothing')
    rows9.extend(rr['covered_s6_rows'])
need(len(rows9) == len(set(rows9)), 'fold9 receipt rows unique')
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
need(sum(inc.values()) == fa9['parent_row_incidence'] == 11826, 'pre-windfall incidence 11826, got %d' % sum(inc.values()))
needed9 = [h for h in openCur9 if demand(h)['c1'] == 0]
need(len(needed9) == fa9['s6_needed_by_open_classes'], 'fa9 s6_needed recomputed')
need(sum(openCur9[h][0] for h in needed9) == fa9['cost_needed_by_open_classes'], 'fa9 cost_needed recomputed')
need(sum(1 for v in inc.values() if v > 0) == fa9['remaining_s5_orbits'], 'fa9 remaining_s5_orbits recomputed')
print('post-ninth-twelfth frontier verified: 6213/492021, solved_s6 1635, incidence 11826')

# ---------- target machinery ----------
audit = load('inputs/audit.json')
need(audit['all_pass'] is True and audit['check_count'] == 23 and audit['derived']['maximum_root_span'] == 2, 'independent audit gate')
targetRows112 = sorted(set(r for x in audit['derived']['witness_pairs'] for r in x['rows']))
need(len(targetRows112) == 112, 'target rows 112')
tf9t = tf9['five_parent_target_after']
need(tf9t['closed_target_rows_total'] == 34, 'fold9 closed target 34')
residual78 = tf9t['residual_row_hex_after']
need(len(residual78) == 78 and len(set(residual78)) == 78, 'residual 78 unique')
need(residual78 == sorted(residual78), 'residual 78 sorted')
residualSet = set(residual78)
need(all(h in set(targetRows112) for h in residual78), 'residual subset of target union')
need(len(set(targetRows112) - residualSet) == 34, 'closed target complement 34')

# ---------- resolve6 windfall evidence ----------
r6 = load('resolve6/output/post-saturation-full-cache-join-resolve6-20261120.json')
need('resolve6' in str(r6.get('schema', '')), 'resolve6 schema')
vstats = r6['verdict_join']['stats']
need(vstats['win_refuted_conflicts'] == 0, 'resolve6 join conflict-free')
need(vstats['canonical_roots_judged'] == 7493 and vstats['win_roots'] == 786 and vstats['refuted_roots'] == 6707, 'resolve6 judged universe')
need(r6['base_state']['residual_row_hex'] == residual78, 'resolve6 base residual 78 matches fold9 residual')
ev = r6['checks'][11]['detail']['evidence']
need(len(ev) == 4, 'resolve6 windfall evidence 4')
ev_by_bit = {x['engine_entries'][0]['bit']: x for x in ev}
need(sorted(ev_by_bit) == [40, 43, 99, 118], 'windfall bits')
for bit, x in ev_by_bit.items():
    need(x['d4_canonical'] is True and x['popcount'] == 7 and x['unsafe_quadruples'] == 0, 'windfall evidence geometry bit %d' % bit)
    e = x['engine_entries'][0]
    need(e['child_hex'] == '00000000000000803202000000001000', 'windfall lane child (cost65h) bit %d' % bit)
    rawline = e['raw_provenance'][0]['bit_line']
    need(rawline['loss'] is True and rawline['capped'] is False and rawline['andclose'] is True
         and rawline['terminalStoneRange'] == [13, 17], 'raw bit line gate bit %d' % bit)
    pc = e['raw_provenance'][0]['pilot_control_line']
    need(pc['loss'] is False and pc['control'] == 'pilot_d6' and pc['nodes'] == 3402, 'pilot control gate bit %d' % bit)
    need(len(x['covered_residual_rows']) == 1 and x['covered_residual_rows'][0] in residualSet, 'windfall covered row in residual 78 (bit %d)' % bit)
wf_rows = sorted(r for _b, x in sorted(ev_by_bit.items()) for r in x['covered_residual_rows'])
need(len(wf_rows) == 4 and len(set(wf_rows)) == 4, 'windfall rows 4 distinct')
wc = r6['resolve']['win_cover_detail']
need(wc['win_cover_hits'] == 4 and wc['rows_covered_by_pending_win'] == wf_rows, 'win_cover_detail crosscheck')
print('resolve6 windfall evidence verified: 4 roots, 4 residual rows, join conflict-free')

# ---------- K1066 published certificate records ----------
w4 = load('windfall4pub/output/windfall4-cert-triple-verification-20261120.json')
need(w4['status'] == 'windfall-4-WIN7-roots-certificate-backed-pending-fold', 'K1066 record status')
need(all(c['pass'] is True for c in w4['checks']) and len(w4['checks']) == 50, 'K1066 record all 50 gates pass')
def evres_nodes(evb, bit):
    return evb[bit]['engine_entries'][0]['raw_provenance'][0]['bit_line']['nodes']

w4_by_bit = {x['bit']: x for x in w4['roots']}
need(sorted(w4_by_bit) == [40, 43, 99, 118], 'K1066 roots bits')
for name, bit, raw in CERTS:
    x = w4_by_bit[bit]
    need(x['raw_root_hex'] == raw, 'K1066 raw root bit %d' % bit)
    need(canon_hex(int(raw, 16)) == x['canonical_root_hex'], 'K1066 canonical mapping bit %d' % bit)
    need(x['canonical_root_hex'] == ev_by_bit[bit]['root'], 'K1066 canonical == resolve6 evidence root bit %d' % bit)
    cert_path = 'windfall4pub/certs/win7-root-%s-20261120.n11' % raw
    cert_bytes = open(f'{W}/{cert_path}', 'rb').read()
    need(hashlib.sha256(cert_bytes).hexdigest() == x['certificate']['sha256'], 'cert bytes sha256 bit %d' % bit)
    need(x['certificate']['bytes'] == len(cert_bytes), 'cert bytes length bit %d' % bit)
    ex = x['extraction']
    need(ex['fbt_drops'] == 0 and ex['fatal'] is None and ex['rerun_byte_identical'] is True
         and ex['terminal_range'] == [13, 17] and ex['kill_table'] == 'empty (blind, pref=null)', 'extraction gate bit %d' % bit)
    need(ex['nodes_run1'] == ex['nodes_rerun'], 'extraction node rerun identity bit %d' % bit)
    bv = x['bigint_independent_verification']
    need(bv['verdict'] == 'WIN7 certificate independently verified' and bv['root_safe'] is True
         and bv['root_hex'] == raw and bv['root_mobility'] == ex['moves']
         and bv['root_stones'] == 7 and bv['subroots_passed'] == ex['moves']
         and bv['union_missing'] == 0 and bv['union_extra'] == 0
         and bv['strategy_rows'] == ex['rows'] and bv['terminal_range'] == [13, 17]
         and bv['rows_sorted_unique'] is True and bv['consumed_winner_rows'] == ex['rows'], 'bigint gate bit %d' % bit)
    ts = x['ts_verify_bit7_win7_cert']
    need(ts['root_check']['stones'] == 7 and ts['root_check']['loserMobility'] == ex['moves']
         and ts['subroots_verified'] == ex['moves'] and ts['union_audit']['exact_union'] is True
         and ts['union_audit']['missing'] == 0 and ts['union_audit']['extra'] == 0
         and ts['union_audit']['consumed_unique'] == ex['rows'] and ts['union_audit']['certificate_rows'] == ex['rows'], 'ts bareiss gate bit %d' % bit)
    pp = x['python_bareiss_replay']
    need(pp['root_loser_mobility'] == ex['moves'] and pp['root_stones'] == 7
         and pp['consumed_rows'] == ex['rows'] and pp['strategy_rows'] == ex['rows']
         and pp['union_missing'] == 0 and pp['union_extra'] == 0
         and pp['subroots_passed'] == ex['moves']
         and pp['terminal_stone_range'] == [13, 15, 17], 'python bareiss gate bit %d' % bit)
    need(x['covered_residual_rows'] == ev_by_bit[bit]['covered_residual_rows'], 'K1066 covered rows == resolve6 bit %d' % bit)
    rv = x['runner_v16_fresh_crosscheck']
    need(rv['loss'] is True and rv['capped'] is False and rv['andclose'] is True
         and rv['terminalStoneRange'] == [13, 17]
         and rv['nodes'] == evres_nodes(ev_by_bit, bit), 'runner v16 node-exact gate bit %d' % bit)
    mask = int(x['canonical_root_hex'], 16)
    need(popcount(mask) == 7 and canon_hex(mask) == x['canonical_root_hex'], 'canonical root geometry bit %d' % bit)
    need(unsafe_quadruples(mask) == 0, 'canonical root unsafe quadruples bit %d' % bit)
    lmv = legal_moves_of(mask)
    need(len(lmv) == ex['moves'], 'legal move count rederivation bit %d' % bit)
    cert_lines = cert_bytes.decode().splitlines()
    need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS', 'cert header bit %d' % bit)
    need(cert_lines[1] == 'root ' + raw, 'cert root line bit %d' % bit)
    need(len(cert_lines) - 2 == ex['rows'], 'cert rows bit %d' % bit)
print('K1066 certificate records verified: 50/50 gates, bytes sha256, headers, geometry, legal moves')

# ---------- apply the four windfall receipts ----------
receipts = []; totalClosed = []; proc_notes = []
for name, bit, raw in CERTS:
    x = w4_by_bit[bit]
    canon_root = x['canonical_root_hex']
    mask = int(canon_root, 16)
    rootRows = root_row_set(canon_root, openCur9)
    need(len(rootRows) >= 1, name + ' closes no row')
    for h in rootRows:
        need(h in openCur9, name + ' row not open: ' + h)
        need(h not in totalClosed, name + ' row closed twice: ' + h)
    targetRows_new = sorted(h for h in rootRows if h in residualSet)
    need(targetRows_new == x['covered_residual_rows'], name + ' independent covered-row join mismatch')
    extra_rows = [h for h in rootRows if h not in residualSet]
    closedCost = sum(openCur9[h][0] for h in rootRows)
    deltas = {}
    for h in rootRows:
        for p in row_parents_hex(h): deltas[p] = deltas.get(p, 0) + 1
    pdeltas = []
    for p in sorted(deltas):
        before = inc[p]; after = before - deltas[p]
        pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'], 'rows_before': before, 'rows_closed': deltas[p], 'rows_after': after})
    for h in rootRows:
        del openCur9[h]
        for p in row_parents_hex(h): inc[p] -= 1
    ex = x['extraction']; bv = x['bigint_independent_verification']
    ts = x['ts_verify_bit7_win7_cert']; pp = x['python_bareiss_replay']
    rv = x['runner_v16_fresh_crosscheck']
    receipts.append({
      'root': canon_root,
      'raw_root_hex': raw,
      'receipt': name,
      'lane_bit': bit,
      'lane_child_hex': '00000000000000803202000000001000',
      'raw_root_is_d4_canonical': raw == canon_root,
      'legal_next_moves': ex['moves'],
      'covered_s6_rows': rootRows,
      'covered_five_parent_target_rows': targetRows_new,
      'extra_s6_rows_not_in_target': extra_rows,
      'unique_strategy_rows': ex['rows'],
      'extraction_nodes': ex['nodes_run1'],
      'extraction_rerun_byte_identical': True,
      'closed_edge_cost': closedCost,
      'certificate_sha256': x['certificate']['sha256'],
      'certificate_bytes': x['certificate']['bytes'],
      'affected_parents': len(pdeltas),
      'parent_deltas': pdeltas,
      'extraction': {'engine': 'class4_child1_cert_extractor_exact_ms23 (repo-verbatim; blind, empty kill table; fbt_drops 0; terminal range [13,17])',
                     'lane_provenance': {'raw_batch_file': ev_by_bit[bit]['engine_entries'][0]['raw_provenance'][0]['file'],
                                         'raw_nodes': evres_nodes(ev_by_bit, bit),
                                         'pilot_d6_control': {'nodes': 3402, 'loss': False}}},
      'independent_verification': {
        'bigint_3x3': {'subroots_passed': ex['moves'], 'union_missing': 0, 'union_extra': 0,
                       'visited_states': bv['visited_states_across_subroots'], 'terminal_count': bv['terminal_count'],
                       'loser_reply_edges': bv['loser_reply_edges'], 'terminal_range': bv['terminal_range']},
        'ts_bareiss_4x4': {'subroots': ts['subroots_verified'], 'union_missing': 0, 'union_extra': 0,
                           'consumed_unique': ts['union_audit']['consumed_unique']},
        'python_exact_bareiss_full_replay': {'subroots_passed': pp['subroots_passed'], 'consumed_rows': pp['consumed_rows'],
                                             'visited_winner_states': pp['visited_winner_states'],
                                             'terminal_stone_range': pp['terminal_stone_range']},
        'runner_v16_fresh_crosscheck': {'nodes': rv['nodes'], 'loss': True, 'capped': False},
        'cross_method_state_flow_equal': True,
        'certificate_union_exact': True,
        'source_record': 'research/experiments/n11-residual78-windfall4-cert-extract-20261120 (K1066; verification record SHA-256 a3ca1b3d...)',
      },
    })
    totalClosed.extend(rootRows)
    proc_notes.append('%s (bit %d) root %s: closed %d S6 rows (%d target rows; %d extra), cost %d' % (
        name, bit, canon_root, len(rootRows), len(targetRows_new), len(extra_rows), closedCost))
    print('  %s: bit %d closed %d rows, target %d, extra %d, cost %d' % (
        name, bit, len(rootRows), len(targetRows_new), len(extra_rows), closedCost))

# frontier after
needed_rows = [h for h in openCur9 if demand(h)['c1'] == 0]
frontier_after = {
  'solved_s6_in_manifest': 1635 + len(totalClosed),
  'remaining_s5_orbits': sum(1 for v in inc.values() if v > 0),
  'unique_remaining_s6': len(openCur9),
  'sum_remaining_cost': sum(v[0] for v in openCur9.values()),
  's6_needed_by_open_classes': len(needed_rows),
  'cost_needed_by_open_classes': sum(openCur9[h][0] for h in needed_rows),
  'parent_row_incidence': sum(inc.values()),
}
# five-parent target accounting
newTargetAll = set()
for r in receipts: newTargetAll |= set(r['covered_five_parent_target_rows'])
need(len(newTargetAll) == 4, 'new target rows total 4, got %d' % len(newTargetAll))
closedAllNew = 34 + len(newTargetAll)
residualAfter = sorted(residualSet - newTargetAll)
need(len(residualAfter) == 74, 'residual target rows 74, got %d' % len(residualAfter))

# live witness plan impact (observation only)
wf_plan = r6['witness_full']
impact = {'unaffected': 0, 'one_of_two_rows_closed': 0, 'both_rows_closed': 0}
for w in wf_plan:
    closed_here = sum(1 for h in w['rows'] if h in newTargetAll)
    if closed_here == 0: impact['unaffected'] += 1
    elif closed_here == 1: impact['one_of_two_rows_closed'] += 1
    else: impact['both_rows_closed'] += 1

def coverage_rows(receipts, wl, totalClosed):
    row_receipt = {}
    for r in receipts:
        for h in r['covered_s6_rows']: row_receipt[h] = r['root']
    rr_out = []
    for h in sorted(totalClosed):
        rr_out.append({'row_hex': h, 'cost': wl[h][0], 'category': wl[h][1], 'demand': demand(h),
                       'parents': sorted(row_parents_hex(h)), 'receipt': {'root': row_receipt[h], 'verdict': 'WIN7-D10'}})
    return rr_out

result = {
  'schema': 'n11-windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120-v1',
  'date': '2026-11-20', 'status': 'fold-complete',
  'source_main_head_before': '5ee7d7c79dc827957ab3c8bb8b2f30d1dd8760b3',
  'previous_fold': {'record': 'fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json (git blob 5b1a30f9b56230382d502aa66ea89d3083b16dd2; n11-stranded86-add-one-stone-expansion-d10-sweep-20261119)',
                    'frontier_after': fa9},
  'certificate_source': {
    'record': 'research/experiments/n11-residual78-windfall4-cert-extract-20261120 (K1066)',
    'verification_sha256': 'a3ca1b3dfd2fcdbd28fc88a6f993c4ff5ad81ee92d4a22800ff2f6477c476feb',
    'certificates_sha256': {raw: sha256_of('windfall4pub/certs/win7-root-%s-20261120.n11' % raw) for _n, _b, raw in CERTS},
    'note': 'Certificates are published at the raw (child|1<<bit) root lines; bits 99/118 raw roots are D4 images of their canonical roots and the mapping is gate-verified. Fold covered-row sets are computed at the canonical root and are representation-invariant under D4.',
  },
  'source_blob_pins': dict(PINS),
  'source_sha256_pins': dict(PIN256),
  'receipt_count': 4, 'receipts': receipts, 'processing_notes': proc_notes,
  'frontier_before': fa9,
  'frontier_after': frontier_after,
  'new_receipt_coverage': {
    'unique_s6_rows': len(totalClosed),
    'closed_edge_cost': sum(r['closed_edge_cost'] for r in receipts),
    'rows': coverage_rows(receipts, wl, totalClosed),
  },
  'parent_closure': {
    'fully_closed_parent_count': len(set(p['parent_hex'] for r in receipts for p in r['parent_deltas'] if p['rows_after'] == 0)),
    'affected_unique_parents': len(set(p['parent_hex'] for r in receipts for p in r['parent_deltas'])),
  },
  'five_parent_target_after': {
    'framework': 'five-parent target union (112 rows; 34 closed through the twelfth receipt, %d through the sixteenth)' % closedAllNew,
    'closed_target_rows_total': closedAllNew,
    'residual_target_rows': len(residualAfter),
    'residual_row_hex_after': residualAfter,
  },
  'witness_plan_impact': {
    'live_plan': '39-root maximum-matching depth-10 witness plan over the 78 residual rows (resolve6; K1059 v17 pilot_d6 cap 30M orderings convention)',
    'note': 'Observation only. The live plan covered all 78 rows and remains a conditional sweep plan, not certificates.',
    'after_windfall_closure': impact,
  },
  'verdict_join_summary': {
    'windfall_roots': [r['root'] for r in receipts],
    'join_basis': 'resolve6 published full-universe cache join (judged 7,493 canonical roots; win 786 / refuted 6,707; win/refuted conflicts 0)',
    'receipt_roots_are': 'certificate-backed WIN7-D10 (K1066 triple verification: TS Bareiss 4x4 sub-root decomposition, pure-python exact Bareiss full replay, BigInt 3x3 independent verification; plus runner v16 node-exact fresh re-solve of all four raw bit lines)',
    'join_limitation': 'bookkeeping join over published pinned records only; no new engine sweep was run in this fold',
  },
  'controls': {
    'base_frontier_recomputed': True,
    'chain_frontiers_recomputed_each_step': True,
    'post_ninth_twelfth_frontier_matches_published_6213_492021': True,
    'fold9_receipt_rows_were_open_and_unique_prior_state': True,
    'receipt_rows_rederived_from_d4_images_and_canonical_frontier': True,
    'receipt_target_rows_match_resolve6_evidence_and_published_records': True,
    'all_receipt_rows_were_open_before_their_receipt': True,
    'receipts_disjoint': True,
    'legal_move_counts_independently_rederived': True,
    'certificates_sha256_verified_against_published_record': True,
    'k1066_all_50_gates_pass_rechecked': True,
    'bigint_independent_verification_pass_three_methods': True,
    'runner_v16_fresh_node_exact_reproduction_pass_all_four': True,
    'win_loss_conflict_scan_against_published_verdict_universe': True,
  },
  'interpretation_guard': [
    'WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone roots of these receipts.',
    'The receipts close their S6 rows in the frontier but prove nothing about the empty board or any two-stone root.',
    'REFUTED-D10 witnesses (of the sweep43 era and the resolve6 joins) are NOT LOSS proofs.',
    'The remaining residual five-parent target rows (74) and the 39-root live witness plan are a conditional depth-10 sweep plan, not certificates.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
  ],
}
with open(f'{W}/{OUT}', 'w') as f:
    json.dump(result, f, indent=1); f.write('\n')
print(json.dumps({'status': result['status'], 'frontier_after': frontier_after,
                  'closed_target_rows_total': closedAllNew, 'residual_target_rows': len(residualAfter),
                  'witness_plan_impact': impact, 'output': OUT}, indent=1))
