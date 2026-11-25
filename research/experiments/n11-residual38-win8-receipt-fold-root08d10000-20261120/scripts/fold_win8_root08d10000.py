# Receipt fold (fold20, twenty-seventh receipt) of the WIN8-D10 certificate of root
# 00000000000000003800000008d10000 (K1121: extraction + triple verification, 19-gate
# record sha256 0088ebab...; certificate sha256 8513e366..., 28,328 rows / 1,026,202
# bytes; the 50-mobility 3-claim WIN8 candidate of the K1091 sweep with uncapped
# probes 564695/673870; extracted and published by the parallel lane) into the five-parent
# S6 frontier chain -- the tenth WIN8 receipt fold, executed under the adopted
# FOLD_PREVERIFIED_CHAIN rerun-gate redesign (adoption note
# research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md): this machine
# re-runs only its immediate predecessor (the published fold19 machine, executed
# PRISTINE in an isolated W copy -- no preverified patch is needed, because the
# published fold19 machine already carries the PREVERIFIED switch and its default
# full run internally re-runs the published fold18 machine as the marker-reversible
# preverified copy -- and is verified byte-identical to the published fold19 record
# sha256 c02d9a54...), and verifies fold10..fold18 upstream by SHA pins plus the full
# frontier chain recomputation, giving the open set 6,152 rows / 487,418 cost,
# solved S6 1,696, parent incidence 11,711 and the residual-41 five-parent target
# (published fold19 values).  The WIN8 receipt of root 08d10000 is then applied:
# the covered S6 rows of the root are rederived geometrically by two independent
# methods -- (A) the fold-chain convention of 8 D4 images with C(8,2) two-stone
# removals (224 operations) and (B) the refsolve coverage_of82 convention of the
# C(8,6)=28 six-stone subsets of the root -- whose canonical row sets must be equal
# (D4-equivariance) and whose intersection with the open frontier is the receipt
# closure.
#
# All chain and certificate inputs are fail-closed SHA-pinned.  Bookkeeping
# only: WIN8-D10 proves only the game tree of the eight-stone root; REFUTED-D10
# is not a LOSS proof; no game value near the empty board is asserted.
# 11x11 empty board / two-stone roots remain UNKNOWN.
#
# W-relative input path -> published repo path map (identical chain inputs as the
# published fold19 machine, plus):
#   fold19/output/win8-root1009000-receipt-fold-20261120.json
#       research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/output/win8-root1009000-receipt-fold-20261120.json
#   fold_win8_root1009000.py (published fold19 machine; sha256-pinned)
#       research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/fold_win8_root1009000.py
#   k1121/output/win8-cert-extract-verification-20261120.json
#       research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/output/win8-cert-extract-verification-20261120.json
#   k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11
#       research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/certs/win8-root-00000000000000003800000008d10000-20261120.n11
#
# Usage: python3 fold_win8_root08d10000.py  (env FOLD20_W overrides the W root)
import json, sys, os, hashlib, tarfile, csv
from itertools import combinations

PREVERIFIED = os.environ.get('FOLD_PREVERIFIED_CHAIN', '') == '1'
PIN_F19_MACHINE_SHA256 = '51442d96341fcffc17d9cb72e36946cb68cd97100abaa6939b27e0d6a20949e8'

W = os.environ.get('FOLD20_W', '/home/user/work/W20')
OUT = 'fold20/output/win8-root08d10000-receipt-fold-20261120.json'
ROOT_HEX = '00000000000000003800000008d10000'
CERT_RELPATH = 'k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11'

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
 'fold11/output/win8-root8003180-receipt-fold-20261120.json': 'd7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e',
 'k1106/output/win8-cert-extract-verification-20261120.json': '0bd2dd10c1d5b735a04f31425003c635d80266e4c03a6bef0fdff212d499408f',
 'k1106/certs/win8-root-00000000000000003800000008005021-20261120.n11': '69f32661d80ae0887ecf385cb690e0d4300c5ad28686ec42fc83e93da79ac6f5',
 'fold12/output/win8-root8005021-receipt-fold-20261120.json': '0f73795ce71aec83ba4a9f1b97a530891f3e6d1c807bfa47c9fbb88a1b33f5bd',
 'k1108/output/win8-cert-extract-verification-20261120.json': '2e453a76fc3168b8eb2e5c224d4a271eea0839eb5256d51fd9c02eb54bb1f648',
 'k1108/certs/win8-root-00000000000000003800000009840004-20261120.n11': '5b114b9e739b7a0a300434afb7ec5326564fc54b0d234df5e3d61abc44541143',
 'fold13/output/win8-root9840004-receipt-fold-20261120.json': 'c2bf80511e816306bbb8dcf4efb450214234f020c513386c3b3a82045f71e9ae',
 'k1109/output/win8-cert-extract-verification-20261120.json': '00836a6e859c780e2204b1aea427eefc044f0d4c5a6b8e8c33505a57fa950bb4',
 'k1109/certs/win8-root-00000000000000909002200080100000-20261120.n11': 'b8a15f9aac5e5f802f85459318247cb20bc983e3b2372167917ba8138cbc7a54',
 'fold14/output/win8-root9090022-receipt-fold-20261120.json': 'ed3159fdb8cf2dd8884beb845cd4ef776cbc8b4b7b442d568d895cd930a13f71',
 'k1114/output/win8-cert-extract-verification-20261120.json': 'ab8cd535c14637c150c02ceeb688b335eb2da9dc1c5778b6a7c05a1a0906f67e',
 'k1114/certs/win8-root-00000000012000003800080009000000-20261120.n11': '5a1359033325e918cf5d9cd2d60ff63fc2fd45e30b926e79330560a7a3a23c4c',
 'fold15/output/win8-root120000038-receipt-fold-20261120.json': 'bae2b3c182da6b0b06be530604f43d1bfa3bf008190860dad6d27f2b9c285aef',
 'k1113/output/win8-cert-extract-verification-20261120.json': 'b8c264e671b9e26fa9caf8cd2454f75b13c992d548e2d5ed0b02f2bec75c5236',
 'k1113/certs/win8-root-00000000010000889002000080100000-20261120.n11': '105e1e2ad59f4f6baa85f37dde7306b98fc96d2164edf5b5d12205b1c71e2bc4',
 'fold16/output/win8-root8890020-receipt-fold-20261120.json': 'edd552588e265ada1cf015b4359584288cca3f18686c0fc8ca1536b6458b969b',
 'k1117/output/win8-cert-extract-verification-20261120.json': '3d97ac6d90e239638b019c95218f0051b432ccdcc6dd2d25e805dcbab11024d9',
 'k1117/certs/win8-root-00000000000000801202000022081000-20261120.n11': 'f62f6704a0d9a1366d333529dd9e742813fe87814f3857a00406d6cfc87f3c8f',
 'fold17/output/win8-root22081000-receipt-fold-20261120.json': '1175244d1da269b1851d5298a824b12a6ed445edc99307acc9c0fefd803bd674',
 'k1120/output/win8-cert-extract-verification-20261120.json': 'ea6f1945c5a8ff359b93336a0a5d4e29035928447503e2bf2f0d13277174b516',
 'k1120/certs/win8-root-00000000000000801202000000901010-20261120.n11': 'd6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1',
 'fold18/output/win8-root00901010-receipt-fold-20261120.json': '18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026',
 'k1119/output/win8-cert-extract-verification-20261120.json': '4696ce1475fd3313c6bb46ebf553e48db4eff2d7182edb0f2b8015258fd17100',
 'k1119/certs/win8-root-00000000000000801212000001009000-20261120.n11': 'b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c',
 'fold19/output/win8-root1009000-receipt-fold-20261120.json': 'c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae',
 'k1121/output/win8-cert-extract-verification-20261120.json': '0088ebab040a29e608c987fb8ae866abf59253d60455b0d2ca6b6ef963170940',
 'k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11': '8513e36613c2676fb82816f47a1ecdda674264eedb9c583dae2616346f4000d2',
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

# ---------- fold11 (eighteenth, WIN8 root 8003180) record chaining ----------
f11 = load('fold11/output/win8-root8003180-receipt-fold-20261120.json')
need(sha256_of('fold11/output/win8-root8003180-receipt-fold-20261120.json') == PIN256['fold11/output/win8-root8003180-receipt-fold-20261120.json'], 'fold11 record sha256')
need(f11['schema'] == 'n11-five-parent-win8-root8003180-receipt-fold-20261120-v1', 'fold11 schema')
need(f11['status'] == 'fold-complete', 'fold11 fold-complete')
need(f11['receipt_count'] == 1 and len(f11['receipts']) == 1, 'fold11 receipt count')
rc11 = f11['receipts'][0]
rows11 = list(rc11['covered_s6_rows'])
need(len(rows11) == len(set(rows11)) == 5, 'fold11 covered rows unique 5')
for h in rows11:
    need(h in open72, 'fold11 row not open: ' + h)
open68 = {h: v for h, v in open72.items() if h not in set(rows11)}
fa11 = f11['frontier_after']
need(len(open68) == 6201 and sum(v[0] for v in open68.values()) == 491110, 'post-fold11 frontier (must match published 6201/491110)')
need(fa11['unique_remaining_s6'] == 6201 and fa11['sum_remaining_cost'] == 491110
     and fa11['solved_s6_in_manifest'] == 1647 and fa11['parent_row_incidence'] == 11803
     and fa11['s6_needed_by_open_classes'] == 4504 and fa11['cost_needed_by_open_classes'] == 357196, 'fold11 frontier_after published values')
for rec_row in f11['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold11 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows11, 'fold11 coverage row among covered')
need(rc11['closed_edge_cost'] == sum(wl[h][0] for h in rows11), 'fold11 closed edge cost recomputed')
for h in rows11:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11803 == fa11['parent_row_incidence'], 'post-fold11 incidence 11803, got %d' % sum(inc.values()))
targetRows11 = list(rc11['covered_five_parent_target_rows'])
need(set(targetRows11) <= residualSet72 and len(targetRows11) == 4, 'fold11 target rows subset of residual72; exactly 4')
extra11 = [h for h in rows11 if h not in residualSet72]
need(extra11 == rc11['extra_s6_rows_not_in_target'], 'fold11 extra rows recorded')
residual68 = f11['five_parent_target_after']['residual_row_hex_after']
need(len(residual68) == 68 and len(set(residual68)) == 68 and residual68 == sorted(residual68), 'residual 68 sorted unique')
need(sorted(residualSet72 - set(targetRows11)) == residual68, 'residual68 == residual72 minus fold11 target rows')
need(f11['five_parent_target_after']['closed_target_rows_total'] == 44, 'fold11 closed target 44')
residualSet68 = set(residual68)
need(all(h in open68 for h in residual68), 'residual68 rows open in frontier')
print('post-fold11 frontier verified: 6201/491110, solved_s6 1647, incidence 11803, residual 68')

# (rerun gate of the fold11 machine removed: adopted single-predecessor rerun design; fold11 record remains SHA-pinned and its chain step recomputed below)

# ---------- fold12 (nineteenth, WIN8 root 8005021) record chaining ----------
f12 = load('fold12/output/win8-root8005021-receipt-fold-20261120.json')
need(sha256_of('fold12/output/win8-root8005021-receipt-fold-20261120.json') == PIN256['fold12/output/win8-root8005021-receipt-fold-20261120.json'], 'fold12 record sha256')
need(f12['schema'] == 'n11-five-parent-win8-root8005021-receipt-fold-20261120-v1', 'fold12 schema')
need(f12['status'] == 'fold-complete', 'fold12 fold-complete')
need(f12['receipt_count'] == 1 and len(f12['receipts']) == 1, 'fold12 receipt count')
rc12 = f12['receipts'][0]
rows12 = list(rc12['covered_s6_rows'])
need(len(rows12) == len(set(rows12)) == 8, 'fold12 covered rows unique 8')
for h in rows12:
    need(h in open68, 'fold12 row not open: ' + h)
open65 = {h: v for h, v in open68.items() if h not in set(rows12)}
fa12 = f12['frontier_after']
need(len(open65) == 6193 and sum(v[0] for v in open65.values()) == 490526, 'post-fold12 frontier (must match published 6193/490526)')
need(fa12['unique_remaining_s6'] == 6193 and fa12['sum_remaining_cost'] == 490526
     and fa12['solved_s6_in_manifest'] == 1655 and fa12['parent_row_incidence'] == 11790
     and fa12['s6_needed_by_open_classes'] == 4501 and fa12['cost_needed_by_open_classes'] == 356974, 'fold12 frontier_after published values')
for rec_row in f12['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold12 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows12, 'fold12 coverage row among covered')
need(rc12['closed_edge_cost'] == sum(wl[h][0] for h in rows12), 'fold12 closed edge cost recomputed')
for h in rows12:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11790 == fa12['parent_row_incidence'], 'post-fold12 incidence 11790, got %d' % sum(inc.values()))
targetRows12 = list(rc12['covered_five_parent_target_rows'])
need(set(targetRows12) <= residualSet68 and len(targetRows12) == 3, 'fold12 target rows subset of residual68; exactly 3')
extra12 = [h for h in rows12 if h not in residualSet68]
need(extra12 == rc12['extra_s6_rows_not_in_target'], 'fold12 extra rows recorded')
residual65 = f12['five_parent_target_after']['residual_row_hex_after']
need(len(residual65) == 65 and len(set(residual65)) == 65 and residual65 == sorted(residual65), 'residual 65 sorted unique')
need(sorted(residualSet68 - set(targetRows12)) == residual65, 'residual65 == residual68 minus fold12 target rows')
need(f12['five_parent_target_after']['closed_target_rows_total'] == 47, 'fold12 closed target 47')
residualSet65 = set(residual65)
need(all(h in open65 for h in residual65), 'residual65 rows open in frontier')
print('post-fold12 frontier verified: 6193/490526, solved_s6 1655, incidence 11790, residual 65')

# (rerun gate of the fold12 machine removed: adopted single-predecessor rerun design; fold12 record remains SHA-pinned and its chain step recomputed below)

# ---------- fold13 (twentieth, WIN8 root 9840004) record chaining ----------
f13 = load('fold13/output/win8-root9840004-receipt-fold-20261120.json')
need(sha256_of('fold13/output/win8-root9840004-receipt-fold-20261120.json') == PIN256['fold13/output/win8-root9840004-receipt-fold-20261120.json'], 'fold13 record sha256')
need(f13['schema'] == 'n11-five-parent-win8-root9840004-receipt-fold-20261120-v1', 'fold13 schema')
need(f13['status'] == 'fold-complete', 'fold13 fold-complete')
need(f13['receipt_count'] == 1 and len(f13['receipts']) == 1, 'fold13 receipt count')
rc13 = f13['receipts'][0]
rows13 = list(rc13['covered_s6_rows'])
need(len(rows13) == len(set(rows13)) == 9, 'fold13 covered rows unique 9')
for h in rows13:
    need(h in open65, 'fold13 row not open: ' + h)
open62 = {h: v for h, v in open65.items() if h not in set(rows13)}
fa13 = f13['frontier_after']
need(len(open62) == 6184 and sum(v[0] for v in open62.values()) == 489813, 'post-fold13 frontier (must match published 6184/489813)')
need(fa13['unique_remaining_s6'] == 6184 and fa13['sum_remaining_cost'] == 489813
     and fa13['solved_s6_in_manifest'] == 1664 and fa13['parent_row_incidence'] == 11775
     and fa13['s6_needed_by_open_classes'] == 4492 and fa13['cost_needed_by_open_classes'] == 356261, 'fold13 frontier_after published values')
for rec_row in f13['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold13 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows13, 'fold13 coverage row among covered')
need(rc13['closed_edge_cost'] == sum(wl[h][0] for h in rows13), 'fold13 closed edge cost recomputed')
for h in rows13:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11775 == fa13['parent_row_incidence'], 'post-fold13 incidence 11775, got %d' % sum(inc.values()))
targetRows13 = list(rc13['covered_five_parent_target_rows'])
need(set(targetRows13) <= residualSet65 and len(targetRows13) == 3, 'fold13 target rows subset of residual65; exactly 3')
extra13 = [h for h in rows13 if h not in residualSet65]
need(extra13 == rc13['extra_s6_rows_not_in_target'], 'fold13 extra rows recorded')
residual62 = f13['five_parent_target_after']['residual_row_hex_after']
need(len(residual62) == 62 and len(set(residual62)) == 62 and residual62 == sorted(residual62), 'residual 62 sorted unique')
need(sorted(residualSet65 - set(targetRows13)) == residual62, 'residual62 == residual65 minus fold13 target rows')
need(f13['five_parent_target_after']['closed_target_rows_total'] == 50, 'fold13 closed target 50')
residualSet62 = set(residual62)
need(all(h in open62 for h in residual62), 'residual62 rows open in frontier')
print('post-fold13 frontier verified: 6184/489813, solved_s6 1664, incidence 11775, residual 62')

# (rerun gate of the fold13 machine removed: adopted single-predecessor rerun design; fold13 record remains SHA-pinned and its chain step recomputed below)


# ---------- fold14 (twenty-first, WIN8 root 9090022) record chaining ----------
f14 = load('fold14/output/win8-root9090022-receipt-fold-20261120.json')
need(sha256_of('fold14/output/win8-root9090022-receipt-fold-20261120.json') == PIN256['fold14/output/win8-root9090022-receipt-fold-20261120.json'], 'fold14 record sha256')
need(f14['schema'] == 'n11-five-parent-win8-root9090022-receipt-fold-20261120-v1', 'fold14 schema')
need(f14['status'] == 'fold-complete', 'fold14 fold-complete')
need(f14['receipt_count'] == 1 and len(f14['receipts']) == 1, 'fold14 receipt count')
rc14 = f14['receipts'][0]
rows14 = list(rc14['covered_s6_rows'])
need(len(rows14) == len(set(rows14)) == 5, 'fold14 covered rows unique 5')
for h in rows14:
    need(h in open62, 'fold14 row not open: ' + h)
open58 = {h: v for h, v in open62.items() if h not in set(rows14)}
fa14 = f14['frontier_after']
need(len(open58) == 6179 and sum(v[0] for v in open58.values()) == 489440, 'post-fold14 frontier (must match published 6179/489440)')
need(fa14['unique_remaining_s6'] == 6179 and fa14['sum_remaining_cost'] == 489440
     and fa14['solved_s6_in_manifest'] == 1669 and fa14['parent_row_incidence'] == 11765
     and fa14['s6_needed_by_open_classes'] == 4487 and fa14['cost_needed_by_open_classes'] == 355888, 'fold14 frontier_after published values')
for rec_row in f14['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold14 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows14, 'fold14 coverage row among covered')
need(rc14['closed_edge_cost'] == sum(wl[h][0] for h in rows14), 'fold14 closed edge cost recomputed')
for h in rows14:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11765 == fa14['parent_row_incidence'], 'post-fold14 incidence 11765, got %d' % sum(inc.values()))
targetRows14 = list(rc14['covered_five_parent_target_rows'])
need(set(targetRows14) <= residualSet62 and len(targetRows14) == 4, 'fold14 target rows subset of residual62; exactly 4')
extra14 = [h for h in rows14 if h not in residualSet62]
need(extra14 == rc14['extra_s6_rows_not_in_target'], 'fold14 extra rows recorded')
residual58 = f14['five_parent_target_after']['residual_row_hex_after']
need(len(residual58) == 58 and len(set(residual58)) == 58 and residual58 == sorted(residual58), 'residual 58 sorted unique')
need(sorted(residualSet62 - set(targetRows14)) == residual58, 'residual58 == residual62 minus fold14 target rows')
need(f14['five_parent_target_after']['closed_target_rows_total'] == 54, 'fold14 closed target 54')
residualSet58 = set(residual58)
need(all(h in open58 for h in residual58), 'residual58 rows open in frontier')
print('post-fold14 frontier verified: 6179/489440, solved_s6 1669, incidence 11765, residual 58')

# (rerun gate of the fold14 machine removed: adopted single-predecessor rerun design; fold14 record remains SHA-pinned and its chain step recomputed below)


# ---------- fold15 (twenty-second, WIN8 root 120000038) record chaining ----------
f15 = load('fold15/output/win8-root120000038-receipt-fold-20261120.json')
need(sha256_of('fold15/output/win8-root120000038-receipt-fold-20261120.json') == PIN256['fold15/output/win8-root120000038-receipt-fold-20261120.json'], 'fold15 record sha256')
need(f15['schema'] == 'n11-five-parent-win8-root120000038-receipt-fold-20261120-v1', 'fold15 schema')
need(f15['status'] == 'fold-complete', 'fold15 fold-complete')
need(f15['receipt_count'] == 1 and len(f15['receipts']) == 1, 'fold15 receipt count')
rc15 = f15['receipts'][0]
rows15 = list(rc15['covered_s6_rows'])
need(len(rows15) == len(set(rows15)) == 6, 'fold15 covered rows unique 6')
for h in rows15:
    need(h in open58, 'fold15 row not open: ' + h)
open55 = {h: v for h, v in open58.items() if h not in set(rows15)}
fa15 = f15['frontier_after']
need(len(open55) == 6173 and sum(v[0] for v in open55.values()) == 488954, 'post-fold15 frontier (must match published 6173/488954)')
need(fa15['unique_remaining_s6'] == 6173 and fa15['sum_remaining_cost'] == 488954
     and fa15['solved_s6_in_manifest'] == 1675 and fa15['parent_row_incidence'] == 11753
     and fa15['s6_needed_by_open_classes'] == 4481 and fa15['cost_needed_by_open_classes'] == 355402, 'fold15 frontier_after published values')
for rec_row in f15['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold15 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows15, 'fold15 coverage row among covered')
need(rc15['closed_edge_cost'] == sum(wl[h][0] for h in rows15), 'fold15 closed edge cost recomputed')
for h in rows15:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11753 == fa15['parent_row_incidence'], 'post-fold15 incidence 11753, got %d' % sum(inc.values()))
targetRows15 = list(rc15['covered_five_parent_target_rows'])
need(set(targetRows15) <= residualSet58 and len(targetRows15) == 3, 'fold15 target rows subset of residual58; exactly 3')
extra15 = [h for h in rows15 if h not in residualSet58]
need(extra15 == rc15['extra_s6_rows_not_in_target'], 'fold15 extra rows recorded')
residual55 = f15['five_parent_target_after']['residual_row_hex_after']
need(len(residual55) == 55 and len(set(residual55)) == 55 and residual55 == sorted(residual55), 'residual 55 sorted unique')
need(sorted(residualSet58 - set(targetRows15)) == residual55, 'residual55 == residual58 minus fold15 target rows')
need(f15['five_parent_target_after']['closed_target_rows_total'] == 57, 'fold15 closed target 57')
residualSet55 = set(residual55)
need(all(h in open55 for h in residual55), 'residual55 rows open in frontier')
print('post-fold15 frontier verified: 6173/488954, solved_s6 1675, incidence 11753, residual 55')

# (rerun gate of the fold15 machine removed: adopted single-predecessor rerun design; fold15 record remains SHA-pinned and its chain step recomputed below)


# ---------- fold16 (twenty-third, WIN8 root 8890020) record chaining ----------
f16 = load('fold16/output/win8-root8890020-receipt-fold-20261120.json')
need(sha256_of('fold16/output/win8-root8890020-receipt-fold-20261120.json') == PIN256['fold16/output/win8-root8890020-receipt-fold-20261120.json'], 'fold16 record sha256')
need(f16['schema'] == 'n11-five-parent-win8-root8890020-receipt-fold-20261120-v1', 'fold16 schema')
need(f16['status'] == 'fold-complete', 'fold16 fold-complete')
need(f16['receipt_count'] == 1 and len(f16['receipts']) == 1, 'fold16 receipt count')
rc16 = f16['receipts'][0]
rows16 = list(rc16['covered_s6_rows'])
need(len(rows16) == len(set(rows16)) == 5, 'fold16 covered rows unique 5')
for h in rows16:
    need(h in open55, 'fold16 row not open: ' + h)
open51 = {h: v for h, v in open55.items() if h not in set(rows16)}
fa16 = f16['frontier_after']
need(len(open51) == 6168 and sum(v[0] for v in open51.values()) == 488575, 'post-fold16 frontier (must match published 6168/488575)')
need(fa16['unique_remaining_s6'] == 6168 and fa16['sum_remaining_cost'] == 488575
     and fa16['solved_s6_in_manifest'] == 1680 and fa16['parent_row_incidence'] == 11743
     and fa16['s6_needed_by_open_classes'] == 4476 and fa16['cost_needed_by_open_classes'] == 355023, 'fold16 frontier_after published values')
for rec_row in f16['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold16 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows16, 'fold16 coverage row among covered')
need(rc16['closed_edge_cost'] == sum(wl[h][0] for h in rows16), 'fold16 closed edge cost recomputed')
for h in rows16:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11743 == fa16['parent_row_incidence'], 'post-fold16 incidence 11743, got %d' % sum(inc.values()))
targetRows16 = list(rc16['covered_five_parent_target_rows'])
need(set(targetRows16) <= residualSet55 and len(targetRows16) == 4, 'fold16 target rows subset of residual55; exactly 4')
extra16 = [h for h in rows16 if h not in residualSet55]
need(extra16 == rc16['extra_s6_rows_not_in_target'], 'fold16 extra rows recorded')
residual51 = f16['five_parent_target_after']['residual_row_hex_after']
need(len(residual51) == 51 and len(set(residual51)) == 51 and residual51 == sorted(residual51), 'residual 51 sorted unique')
need(sorted(residualSet55 - set(targetRows16)) == residual51, 'residual51 == residual55 minus fold16 target rows')
need(f16['five_parent_target_after']['closed_target_rows_total'] == 61, 'fold16 closed target 61')
residualSet51 = set(residual51)
need(all(h in open51 for h in residual51), 'residual51 rows open in frontier')
print('post-fold16 frontier verified: 6168/488575, solved_s6 1680, incidence 11743, residual 51')

# (rerun gate of the fold16 machine removed: adopted single-predecessor rerun design; fold16 record remains SHA-pinned and its chain step recomputed below)

# ---------- fold17 (twenty-fourth, WIN8 root 22081000) record chaining ----------
f17 = load('fold17/output/win8-root22081000-receipt-fold-20261120.json')
need(sha256_of('fold17/output/win8-root22081000-receipt-fold-20261120.json') == PIN256['fold17/output/win8-root22081000-receipt-fold-20261120.json'], 'fold17 record sha256')
need(f17['schema'] == 'n11-five-parent-win8-root22081000-receipt-fold-20261120-v1', 'fold17 schema')
need(f17['status'] == 'fold-complete', 'fold17 fold-complete')
need(f17['receipt_count'] == 1 and len(f17['receipts']) == 1, 'fold17 receipt count')
rc17 = f17['receipts'][0]
rows17 = list(rc17['covered_s6_rows'])
need(len(rows17) == len(set(rows17)) == 7, 'fold17 covered rows unique 7')
for h in rows17:
    need(h in open51, 'fold17 row not open: ' + h)
open48 = {h: v for h, v in open51.items() if h not in set(rows17)}
fa17 = f17['frontier_after']
need(len(open48) == 6161 and sum(v[0] for v in open48.values()) == 488094, 'post-fold17 frontier (must match published 6161/488094)')
need(fa17['unique_remaining_s6'] == 6161 and fa17['sum_remaining_cost'] == 488094
     and fa17['solved_s6_in_manifest'] == 1687 and fa17['parent_row_incidence'] == 11729
     and fa17['s6_needed_by_open_classes'] == 4469 and fa17['cost_needed_by_open_classes'] == 354542, 'fold17 frontier_after published values')
for rec_row in f17['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold17 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows17, 'fold17 coverage row among covered')
need(rc17['closed_edge_cost'] == sum(wl[h][0] for h in rows17), 'fold17 closed edge cost recomputed')
for h in rows17:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11729 == fa17['parent_row_incidence'], 'post-fold17 incidence 11729, got %d' % sum(inc.values()))
targetRows17 = list(rc17['covered_five_parent_target_rows'])
need(set(targetRows17) <= residualSet51 and len(targetRows17) == 3, 'fold17 target rows subset of residual51; exactly 3')
extra17 = [h for h in rows17 if h not in residualSet55]
need(extra17 == rc17['extra_s6_rows_not_in_target'], 'fold17 extra rows recorded')
residual48 = f17['five_parent_target_after']['residual_row_hex_after']
need(len(residual48) == 48 and len(set(residual48)) == 48 and residual48 == sorted(residual48), 'residual 48 sorted unique')
need(sorted(residualSet51 - set(targetRows17)) == residual48, 'residual48 == residual51 minus fold17 target rows')
need(f17['five_parent_target_after']['closed_target_rows_total'] == 64, 'fold17 closed target 64')
residualSet48 = set(residual48)
need(all(h in open48 for h in residual48), 'residual48 rows open in frontier')
print('post-fold17 frontier verified: 6161/488094, solved_s6 1687, incidence 11729, residual 48')

# ---------- fold18 (twenty-fifth, WIN8 root 00901010) record chaining ----------
f18 = load('fold18/output/win8-root00901010-receipt-fold-20261120.json')
need(sha256_of('fold18/output/win8-root00901010-receipt-fold-20261120.json') == PIN256['fold18/output/win8-root00901010-receipt-fold-20261120.json'], 'fold18 record sha256')
need(f18['schema'] == 'n11-five-parent-win8-root00901010-receipt-fold-20261120-v1', 'fold18 schema')
need(f18['status'] == 'fold-complete', 'fold18 fold-complete')
need(f18['receipt_count'] == 1 and len(f18['receipts']) == 1, 'fold18 receipt count')
rc18 = f18['receipts'][0]
rows18 = list(rc18['covered_s6_rows'])
need(len(rows18) == len(set(rows18)) == 4, 'fold18 covered rows unique 4')
for h in rows18:
    need(h in open48, 'fold18 row not open: ' + h)
open45 = {h: v for h, v in open48.items() if h not in set(rows18)}
fa18 = f18['frontier_after']
need(len(open45) == 6157 and sum(v[0] for v in open45.values()) == 487800, 'post-fold18 frontier (must match published 6157/487800)')
need(fa18['unique_remaining_s6'] == 6157 and fa18['sum_remaining_cost'] == 487800
     and fa18['solved_s6_in_manifest'] == 1691 and fa18['parent_row_incidence'] == 11721
     and fa18['s6_needed_by_open_classes'] == 4465 and fa18['cost_needed_by_open_classes'] == 354248, 'fold18 frontier_after published values')
for rec_row in f18['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold18 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows18, 'fold18 coverage row among covered')
need(rc18['closed_edge_cost'] == sum(wl[h][0] for h in rows18), 'fold18 closed edge cost recomputed')
for h in rows18:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11721 == fa18['parent_row_incidence'], 'post-fold18 incidence 11721, got %d' % sum(inc.values()))
targetRows18 = list(rc18['covered_five_parent_target_rows'])
need(set(targetRows18) <= residualSet48 and len(targetRows18) == 3, 'fold18 target rows subset of residual48; exactly 3')
extra18 = [h for h in rows18 if h not in residualSet48]
need(extra18 == rc18['extra_s6_rows_not_in_target'], 'fold18 extra rows recorded')
residual45 = f18['five_parent_target_after']['residual_row_hex_after']
need(len(residual45) == 45 and len(set(residual45)) == 45 and residual45 == sorted(residual45), 'residual 45 sorted unique')
need(sorted(residualSet48 - set(targetRows18)) == residual45, 'residual45 == residual48 minus fold18 target rows')
need(f18['five_parent_target_after']['closed_target_rows_total'] == 67, 'fold18 closed target 67')
residualSet45 = set(residual45)
need(all(h in open45 for h in residual45), 'residual45 rows open in frontier')
print('post-fold18 frontier verified: 6157/487800, solved_s6 1691, incidence 11721, residual 45')


# ---------- fold19 (twenty-sixth, WIN8 root 1009000) record chaining ----------
f19 = load('fold19/output/win8-root1009000-receipt-fold-20261120.json')
need(sha256_of('fold19/output/win8-root1009000-receipt-fold-20261120.json') == PIN256['fold19/output/win8-root1009000-receipt-fold-20261120.json'], 'fold19 record sha256')
need(f19['schema'] == 'n11-five-parent-win8-root1009000-receipt-fold-20261120-v1', 'fold19 schema')
need(f19['status'] == 'fold-complete', 'fold19 fold-complete')
need(f19['receipt_count'] == 1 and len(f19['receipts']) == 1, 'fold19 receipt count')
rc19 = f19['receipts'][0]
rows19 = list(rc19['covered_s6_rows'])
need(len(rows19) == len(set(rows19)) == 5, 'fold19 covered rows unique 5')
for h in rows19:
    need(h in open45, 'fold19 row not open: ' + h)
open41 = {h: v for h, v in open45.items() if h not in set(rows19)}
fa19 = f19['frontier_after']
need(len(open41) == 6152 and sum(v[0] for v in open41.values()) == 487418, 'post-fold19 frontier (must match published 6152/487418)')
need(fa19['unique_remaining_s6'] == 6152 and fa19['sum_remaining_cost'] == 487418
     and fa19['solved_s6_in_manifest'] == 1696 and fa19['parent_row_incidence'] == 11711
     and fa19['s6_needed_by_open_classes'] == 4460 and fa19['cost_needed_by_open_classes'] == 353866, 'fold19 frontier_after published values')
for rec_row in f19['new_receipt_coverage']['rows']:
    need(rec_row['cost'] == wl[rec_row['row_hex']][0], 'fold19 recorded cost matches worklist')
    need(rec_row['row_hex'] in rows19, 'fold19 coverage row among covered')
need(rc19['closed_edge_cost'] == sum(wl[h][0] for h in rows19), 'fold19 closed edge cost recomputed')
for h in rows19:
    for p in row_parents_hex(h): inc[p] -= 1
need(sum(inc.values()) == 11711 == fa19['parent_row_incidence'], 'post-fold19 incidence 11711, got %d' % sum(inc.values()))
targetRows19 = list(rc19['covered_five_parent_target_rows'])
need(set(targetRows19) <= residualSet45 and len(targetRows19) == 4, 'fold19 target rows subset of residual45; exactly 4')
extra19 = [h for h in rows19 if h not in residualSet45]
need(extra19 == rc19['extra_s6_rows_not_in_target'], 'fold19 extra rows recorded')
residual41 = f19['five_parent_target_after']['residual_row_hex_after']
need(len(residual41) == 41 and len(set(residual41)) == 41 and residual41 == sorted(residual41), 'residual 41 sorted unique')
need(sorted(residualSet45 - set(targetRows19)) == residual41, 'residual41 == residual45 minus fold19 target rows')
need(f19['five_parent_target_after']['closed_target_rows_total'] == 71, 'fold19 closed target 71')
residualSet41 = set(residual41)
need(all(h in open41 for h in residual41), 'residual41 rows open in frontier')
print('post-fold19 frontier verified: 6152/487418, solved_s6 1696, incidence 11711, residual 41')

# ---------- fold19 machine rerun (published machine pristine; single rerun gate) ----------
# Adopted rerun-gate redesign: this machine freshly re-runs ONLY its immediate
# predecessor.  The published fold19 machine is executed PRISTINE (no preverified
# patch is needed: the published fold19 machine already carries the PREVERIFIED
# switch of the adopted redesign, and its default full run is a short gate that
# internally re-runs the published fold18 machine as the marker-reversible
# preverified copy, re-verifying the reverse patch) in an isolated W copy; it keeps
# every input pin, the full frontier chain recomputation, the fold18 preverified
# rerun gate, the K1119 19-gate block, the K1097 crosscheck and the receipt
# application, so its output must be byte-identical to the published fold19 record.
# When THIS machine is the rerun target of fold21, FOLD_PREVERIFIED_CHAIN=1
# skips this gate and upstream verification is via SHA pins + chain recomputation.
if not PREVERIFIED:
    import shutil, subprocess
    _pub19 = open(f'{W}/fold_win8_root1009000.py', 'rb').read()
    need(hashlib.sha256(_pub19).hexdigest() == PIN_F19_MACHINE_SHA256, 'published fold19 machine sha256 pin')
    W19X = W + '-rerun-root-f19'
    if os.path.isdir(W19X): shutil.rmtree(W19X)
    shutil.copytree(W, W19X)
    _env19 = dict(os.environ); _env19['FOLD19_W'] = W19X
    _rr19 = subprocess.run([sys.executable, W19X + '/fold_win8_root1009000.py'], env=_env19, capture_output=True, text=True)
    need(_rr19.returncode == 0, 'fold19 machine pristine rerun failed: ' + _rr19.stderr[-600:])
    _rerun19_sha = hashlib.sha256(open(W19X + '/fold19/output/win8-root1009000-receipt-fold-20261120.json', 'rb').read()).hexdigest()
    need(_rerun19_sha == PIN256['fold19/output/win8-root1009000-receipt-fold-20261120.json'], 'fold19 pristine rerun byte mismatch vs published record')
    shutil.rmtree(W19X)
    print('fold19 machine pristine rerun verified: stdout ends ' + _rr19.stdout.strip().splitlines()[-1][:80])
else:
    print('FOLD_PREVERIFIED_CHAIN=1: fold19 machine rerun gate skipped; upstream via SHA pins + chain recomputation')


# (rerun gate of the fold17 machine removed: adopted single-predecessor rerun design; fold17 record remains SHA-pinned and its chain step recomputed below)

# ---------- k1121 certificate record (19 gates) ----------
k1121 = load('k1121/output/win8-cert-extract-verification-20261120.json')
need(k1121['schema'] == 'win8-cert-extract-verification-v1', 'k1121 schema')
need(k1121['all_gates_pass'] is True and k1121['gate_count'] == 19 and len(k1121['gates']) == 19, 'k1121 gate count')
need(all(g['passed'] for g in k1121['gates']), 'k1121 every gate passed')
need(k1121['root'] == ROOT_HEX, 'k1121 root hex')
gate01 = [g for g in k1121['gates'] if g['gate'] == 'g01_k1091_master_sha256_pin'][0]
need(gate01['detail'] == 'edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25', 'k1121 k1091 master sha pin')
gate07 = [g for g in k1121['gates'] if g['gate'] == 'g07_k1091_root_claimed_coverage_3rows']
need(len(gate07) == 1, 'g07 present')
CLAIM = sorted(gate07[0]['detail'])
need(len(CLAIM) == 3, 'k1121 claim rows are 3')
need(CLAIM == sorted(k1121['recorded']['k1091_claimed_coverage_rows']), 'k1121 claim rows consistent')
gate05 = [g for g in k1121['gates'] if g['gate'] == 'g05_root_mobility_50'][0]
need(gate05['detail'] == 50 and gate05['passed'] is True, 'k1121 mobility 50')
gate08 = [g for g in k1121['gates'] if g['gate'] == 'g08_probe_reproduction_matches_k1091'][0]
need(gate08['detail'] == {'pilot_d6': 4, 'reproduced': {'andclose0': 2, 'andclose1': 2}}, 'k1121 probe reproduction detail')
gate06 = [g for g in k1121['gates'] if g['gate'] == 'g06_k1091_root_probes_win_uncapped'][0]
need(gate06['detail']['andclose1']['capped'] is False and gate06['detail']['andclose1']['loss'] is True and gate06['detail']['andclose1']['nodes'] == 564695
     and gate06['detail']['andclose0']['capped'] is False and gate06['detail']['andclose0']['loss'] is True and gate06['detail']['andclose0']['nodes'] == 673870
     and gate06['detail']['andclose0']['terminalStoneRange'] == [14, 18] and gate06['detail']['andclose1']['terminalStoneRange'] == [14, 18],
     'k1121 uncapped probes 564695/673870 with terminal range [14,18]')
gate13 = [g for g in k1121['gates'] if g['gate'] == 'g13_node_accounting_chunk_vs_single'][0]
need(gate13['detail'] == {'a1_chunk_total_nodes': 2428240, 'b_single_process_nodes': 1748509}, 'k1121 extraction node accounting')
gate16 = [g for g in k1121['gates'] if g['gate'] == 'g16_third_method_traversal_pass'][0]
need(gate16['detail']['missing'] == 0 and gate16['detail']['extra'] == 0 and gate16['detail']['failure'] is None, 'k1121 third-method zero miss/extra')
gate19 = [g for g in k1121['gates'] if g['gate'] == 'g19_k1097_refsolve_footprint_match'][0]
need(len(gate19['detail']['claimed']) == 3 and sorted(gate19['detail']['claimed']) == CLAIM, 'k1121 g19 footprint claimed == CLAIM (3 rows)')
need(gate19['detail']['k1097_sha256'] == PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'], 'k1121 g19 k1097 sha pin')
cert_recd = k1121['recorded']['certificate']
cert_bytes = open(f'{W}/{CERT_RELPATH}', 'rb').read()
need(hashlib.sha256(cert_bytes).hexdigest() == cert_recd['sha256'] == PIN256[CERT_RELPATH], 'k1121 cert sha256')
need(cert_recd['bytes'] == len(cert_bytes) == 1026202, 'k1121 cert bytes')
need(cert_recd['rows'] == 28328, 'k1121 cert rows')
cert_lines = cert_bytes.decode().splitlines()
need(cert_lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'k1121 cert header')
need(cert_lines[1] == 'root ' + ROOT_HEX, 'k1121 cert root line')
need(len(cert_lines) - 2 == 28328, 'k1121 cert row count')
data_rows = cert_lines[2:]
need(all(len(x.split(' ')) == 2 and len(x.split(' ')[0]) == 32 for x in data_rows), 'k1121 cert row format')
need(data_rows == sorted(data_rows) and len(set(data_rows)) == len(data_rows), 'k1121 cert rows sorted unique')
tm = k1121['recorded']['third_method']
need(tm['root_first_moves'] == 50 and tm['terminal_count'] == 15513 and tm['terminal_range'] == [14, 18]
     and tm['visited_states'] == 83544 and tm['winner_states'] == 53570 and tm['loser_states'] == 14461
     and tm['loser_reply_edges'] == 72930, 'k1121 third-method aggregate')

# ---------- k1121 geometry independent rederivation ----------
mask = int(ROOT_HEX, 16)
need(popcount(mask) == 8, 'root 8 stones')
need(unsafe_quadruples(mask) == 0, 'root safe')
need(canon_int(mask) == mask, 'root D4 canonical')
lmv = legal_moves_of(mask)
need(len(lmv) == 50, 'root legal move count rederivation 50')
print('k1121 certificate record verified: 19/19 gates, sha, header, geometry, mobility 50')

# ---------- K1097 refsolve claim crosscheck ----------
k1097 = load('k1097/output/safe8-refuted50-refsolve-20261120.json')
need(k1097['status'] == 'refsolve-computed', 'k1097 status')
need(len(k1097['gates']) == 27 and all(g['ok'] for g in k1097['gates']), 'k1097 gates all ok')
foot = k1097['win16_intrinsic_footprints']
need(ROOT_HEX in foot, 'k1097 footprint has root')
need(foot[ROOT_HEX]['intrinsic_equals_claimed'] is True, 'root intrinsic == claimed')
need(sorted(foot[ROOT_HEX]['claimed']) == CLAIM, 'footprint claimed == K1086/K1113 claim')
need(sorted(foot[ROOT_HEX]['intrinsic']) == CLAIM, 'footprint intrinsic == K1086/K1113 claim')
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
need(all(h in residualSet41 for h in CLAIM), 'claim rows inside residual41')
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
closedHistorical |= set(rows11) | set(rows12) | set(rows13)
closedHistorical |= set(rows14)
closedHistorical |= set(rows15)
closedHistorical |= set(rows16)
closedHistorical |= set(rows17)
closedHistorical |= set(rows18)
closedHistorical |= set(rows19)
row_class = {}
for h in sorted(rootB):
    if h in open41: row_class[h] = 'open-frontier'
    elif h in closedHistorical: row_class[h] = 'closed-before-this-receipt'
    elif h in wl: row_class[h] = 'worklist-but-not-open'   # impossible if chain is exact
    else: row_class[h] = 'not-in-worklist'
for h, cls in row_class.items():
    need(cls != 'worklist-but-not-open', 'chain inconsistency on row ' + h)

rootRows = sorted(h for h in rootA if h in open41)
need(len(rootRows) >= 1, 'WIN8 receipt closes no open row')
need(rootRows == sorted(set(rootRows)), 'rederived rows unique')
targetRows_new = sorted(h for h in rootRows if h in residualSet41)
need(targetRows_new == CLAIM, 'rederived target rows == published claim')
extra_rows = [h for h in rootRows if h not in residualSet41]
closedCost = sum(open41[h][0] for h in rootRows)

# apply the receipt
deltas = {}
for h in rootRows:
    for p in row_parents_hex(h): deltas[p] = deltas.get(p, 0) + 1
pdeltas = []
for p in sorted(deltas):
    before = inc[p]; after = before - deltas[p]
    pdeltas.append({'parent_hex': p, 'classes': parents[p]['classes'], 'rows_before': before, 'rows_closed': deltas[p], 'rows_after': after})
for h in rootRows:
    del open41[h]
    for p in row_parents_hex(h): inc[p] -= 1

# frontier after
needed_rows = [h for h in open41 if demand(h)['c1'] == 0]
frontier_after = {
  'solved_s6_in_manifest': 1696 + len(rootRows),
  'remaining_s5_orbits': sum(1 for v in inc.values() if v > 0),
  'unique_remaining_s6': len(open41),
  'sum_remaining_cost': sum(v[0] for v in open41.values()),
  's6_needed_by_open_classes': len(needed_rows),
  'cost_needed_by_open_classes': sum(open41[h][0] for h in needed_rows),
  'parent_row_incidence': sum(inc.values()),
}

# five-parent target accounting
newTargetAll = set(targetRows_new)
closedAllNew = 71 + len(newTargetAll)
residualAfter = sorted(residualSet41 - newTargetAll)
need(len(residualAfter) == 41 - len(targetRows_new), 'residual accounting')

def coverage_rows(rootRows, wl):
    rr_out = []
    for h in sorted(rootRows):
        rr_out.append({'row_hex': h, 'cost': wl[h][0], 'category': wl[h][1], 'demand': demand(h),
                       'parents': sorted(row_parents_hex(h)), 'receipt': {'root': ROOT_HEX, 'verdict': 'WIN8-D10'}})
    return rr_out

result = {
  'schema': 'n11-five-parent-win8-root08d10000-receipt-fold-20261120-v1',
  'date': '2026-11-20', 'status': 'fold-complete', 'receipt_ordinal': 'twenty-seventh (fold20, tenth WIN8 receipt fold)',
  'single_owner_note': 'research/log/2026-11-20-n11-fold20-win8-root08d10000-single-owner-note.md',
  'previous_fold': {'record': 'research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/output/win8-root1009000-receipt-fold-20261120.json (sha256 c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae)',
                    'frontier_after': fa19},
  'certificate_source': {
    'record': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120 (K1121: WIN8 root certificate extract + triple verification, 19 gates; 50-mobility 3-claim WIN8 candidate of the K1091 sweep with uncapped probes 564695/673870; published by the parallel lane)',
    'verification_sha256': PIN256['k1121/output/win8-cert-extract-verification-20261120.json'],
    'certificate_path': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/certs/win8-root-00000000000000003800000008d10000-20261120.n11',
    'certificate_sha256': cert_recd['sha256'],
    'k1091_probes_record': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/output/.input-k1091.json (K1091 alternate-15-roots d10 sweep record; sha256 edd7ac84...; claimed coverage 3 rows, pinned by K1121 g01/g07)',
    'claims_record': 'research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json (K1097; sha256 ' + PIN256['k1097/output/safe8-refuted50-refsolve-20261120.json'] + '; win16_intrinsic_footprints: intrinsic == claimed == 3 rows)',
  },
  'source_blob_pins': dict(PINS),
  'source_sha256_pins': dict(PIN256),
  'receipt_count': 1,
  'receipts': [{
      'root': ROOT_HEX, 'raw_root_hex': ROOT_HEX, 'receipt': 'twenty-seventh',
      'stones': 8, 'verdict': 'WIN8-D10',
      'legal_next_moves': 50,
      'covered_s6_rows': rootRows,
      'covered_five_parent_target_rows': targetRows_new,
      'extra_s6_rows_not_in_target': extra_rows,
      'unique_strategy_rows': 28328,
      'certificate_sha256': cert_recd['sha256'],
      'certificate_bytes': cert_recd['bytes'],
      'closed_edge_cost': closedCost,
      'affected_parents': len(pdeltas),
      'parent_deltas': pdeltas,
      'independent_verification': {
        'extraction_and_triple': {'gates': 19, 'all_pass': True,
          'methods': ['extraction self-check A1/A2/B byte-identical', 'BigInt 3x3 cofactor', 'Bareiss 4x4', 'python third-method exact traversal'],
          'third_method_aggregates': tm},
        'coverage_geometry_two_methods': {'d4_images_two_stone_removals_ops': opsA, 'c86_subsets': 28,
          'canonical_row_sets_equal': True, 'canonical_rows': sorted(rootB)},
        'cross_method_union_exact': True,
        'source_record': 'research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120',
      },
  }],
  'frontier_before': fa19,
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
    'note': 'Observation only. The K1086 probe classified 7 WIN8-D10 candidates (claims 4+4+4+3+3+3+2 = 23 rows) inside the K1097 plan (16 candidates, 49 rows, exactly-once partition) with 9 alternative roots (residual 23 rows). Fold11 retired root 8003180 (4 claimed rows), fold12 retired root 8005021 (3 claimed rows), fold13 retired root 9840004 (3 claimed rows), fold14 retired root 9090022 (4 claimed rows), fold15 retired root 120000038 (3 claimed rows), fold16 retired root 8890020 (4 claimed rows), fold17 retired root 22081000 (3 claimed rows), fold18 retired root 00901010 (3 claimed rows) and fold19 retired root 1009000 (4 claimed rows); this receipt closes the 3 claimed rows of root 08d10000 (a K1091-sweep WIN candidate inside the same K1097 footprint plan); the remaining 6 WIN8 candidates keep 49-4-3-3-4-3-4-3-3-4-3 = 15 claimed rows, the residual-23 alternative sweep plan is untouched: its rows are disjoint from every WIN16 claim, machine-checked.',
    'retired_win_candidate_root': ROOT_HEX,
    'rows_of_retired_root': CLAIM,
    'retired_root_predecessor': '00000000000000801212000001009000',
    'win16_candidates_remaining': 6,
    'win16_claimed_rows_remaining': 15,
    'residual23_untouched': True,
  },
  'verdict_join_summary': {
    'join_basis': 'published fold19 chain frontier (single fresh rerun gate: the published fold19 machine executed pristine in an isolated W copy, byte-identical to the published fold19 record; the fold18 preverified rerun, its reverse-patch preverification and the K1120 gate block re-run transitively inside it; fold10..fold18 upstream verified by SHA-256 pins and the full frontier chain recomputation per the adopted rerun-gate redesign) + K1121 triple-verified WIN8 certificate + K1091 claims and K1097 refsolve coverage footprints',
    'receipt_root_is': 'certificate-backed WIN8-D10 (K1121: extraction self-check + BigInt 3x3 + Bareiss 4x4 + python third-method; independently re-audited 19-gate record)',
  },
  'controls': {
    'base_frontier_recomputed': True,
    'chain_frontiers_recomputed_each_step': True,
    'fold10_record_chained_and_published_values_matched': True,
    'fold10_frontier_6206_491497_recomputed_from_worklist': True,
    'post_fold10_incidence_11810_recomputed': True,
    'fold11_record_chained_and_published_values_matched': True,
    'fold11_frontier_6201_491110_recomputed_from_worklist': True,
    'post_fold11_incidence_11803_recomputed': True,
    'fold12_record_chained_and_published_values_matched': True,
    'fold12_frontier_6193_490526_recomputed_from_worklist': True,
    'post_fold12_incidence_11790_recomputed': True,
    'fold13_record_chained_and_published_values_matched': True,
    'fold13_frontier_6184_489813_recomputed_from_worklist': True,
    'post_fold13_incidence_11775_recomputed': True,
    'fold14_record_chained_and_published_values_matched': True,
    'fold14_frontier_6179_489440_recomputed_from_worklist': True,
    'post_fold14_incidence_11765_recomputed': True,
    'fold15_record_chained_and_published_values_matched': True,
    'fold15_frontier_6173_488954_recomputed_from_worklist': True,
    'post_fold15_incidence_11753_recomputed': True,
    'fold16_record_chained_and_published_values_matched': True,
    'fold16_frontier_6168_488575_recomputed_from_worklist': True,
    'post_fold16_incidence_11743_recomputed': True,
    'fold17_record_chained_and_published_values_matched': True,
    'fold17_frontier_6161_488094_recomputed_from_worklist': True,
    'post_fold17_incidence_11729_recomputed': True,
    'fold18_record_chained_and_published_values_matched': True,
    'fold18_frontier_6157_487800_recomputed_from_worklist': True,
    'post_fold18_incidence_11721_recomputed': True,
    'fold19_record_chained_and_published_values_matched': True,
    'fold19_frontier_6152_487418_recomputed_from_worklist': True,
    'post_fold19_incidence_11711_recomputed': True,
    'fold10_record_sha256_pin_verified': True,
    'fold11_record_sha256_pin_verified': True,
    'fold12_record_sha256_pin_verified': True,
    'fold13_record_sha256_pin_verified': True,
    'fold14_record_sha256_pin_verified': True,
    'fold15_record_sha256_pin_verified': True,
    'fold16_record_sha256_pin_verified': True,
    'fold17_record_sha256_pin_verified': True,
    'fold18_record_sha256_pin_verified': True,
    'fold19_record_sha256_pin_verified': True,
    'rerun_gate_redesign_adopted_single_predecessor_rerun': True,
    'fold11_through_fold17_machine_recursive_reruns_replaced_by_sha_pins_and_chain_recomputation': True,
    'fold19_machine_pristine_rerun_byte_identical': True,
    'fold18_preverified_rerun_and_reverse_patch_rechecked_transitively_inside_fold19_rerun': True,
    'all_chain_input_pins_verified_upfront': True,
    'k1121_cert_19_gates_rechecked_and_bytes_verified': True,
    'k1120_cert_gates_rechecked_inside_preverified_fold18_rerun': True,
    'k1119_cert_gates_rechecked_inside_fold19_pristine_rerun': True,
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
os.makedirs(f'{W}/fold20/output', exist_ok=True)
with open(f'{W}/{OUT}', 'w') as f:
    json.dump(result, f, indent=1); f.write('\n')
print(json.dumps({'status': result['status'], 'frontier_after': frontier_after,
                  'closed_target_rows_total': closedAllNew, 'residual_target_rows': len(residualAfter),
                  'rederived_rows': rootRows, 'target_rows': targetRows_new, 'extra_rows': extra_rows,
                  'output': OUT, 'sha256': sha256_of(OUT)}, indent=1))
