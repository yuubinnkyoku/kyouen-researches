#!/usr/bin/env python3
"""External second verification of the published fold24 (K1140) WIN8-D10 receipt fold.

Third implementation, written by an external lane. Distinct from both the
published fold24 machine and the publisher's bundled independent auditor:
the D4 transformations, the 4x4 incidence determinant (cofactor expansion),
the parent/row bookkeeping and every frontier statistic are re-derived from
scratch with explicit coordinate maps and no shared helper code.

Reads only:
  - a reconstructed pristine input tree W (61 pinned chain inputs, produced by
    the publisher's reconstruct_inputs.py from its fixed Git reference), and
  - the five published byte artifacts of the fold24 experiment directory.

Fail-closed. Deterministic output: one audit JSON (sorted keys, no timestamps).
No row is closed by this verification and no game-theoretic value is proven.
The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60},
and classes 1/2/4 remain UNKNOWN.

Usage: verify_fold24_external_20261120.py <W_pristine_master> <pub_dir> <out_json>
"""
import csv, hashlib, json, os, shutil, subprocess, sys, tarfile
from itertools import combinations

# ---------------------------------------------------------------- published pins
PUB_RECEIPT_SHA = 'c4ab76d3cb7eba5c1ab8e1830c43d17bf9a771f511b66e7e8573864f3f2402c7'
PUB_MACHINE_SHA = 'f462733dbaa6a958680ce49ff85e056adf8756cc946fa5ac612442f2c47b4fc8'
PUB_AUDIT_SHA = '49f330c6e0f73c0a58fdd9b21c215c38fc3a594d35f1d617b1324468c4a3387b'
PUB_REPROLOG_SHA = 'cb01749a9b52e7ed4392dc2d25cf008e805b0ca17b40a25537680e9d1df0e5b2'
PUB_RECONSTRUCT_SHA = 'f4e1fa8e69b10c07d9eec7f0b798458b0e73a97308bd418b622d1e9542873591'
PUB_BUNDLED_AUDITOR_SHA = 'e0dbebe463a5f0f4e652779905658301d3b9e4b1506e80b581bce673d1f102aa'
PIN_K1091_SWEEP = 'edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25'
PIN_K1091_SWEEP_REL = 'k1091/output/replace15-d10-sweep-20261120.json'
PIN_RUNNER_V17 = 'c132cc6425eee3feaeef1d697dd74f968cfedb59'
PIN_RUNNER_REL = 'k1136/runner_v17.ts'
ROOT_HEX = '00000000000000043800000008180010'
CERT_RELPATH = 'k1136/certs/win8-root-00000000000000043800000008180010-20261120.n11'
K1136_VERIF_REL = 'k1136/output/win8-cert-extract-verification-20261120.json'
K1136_VERIF_SHA = 'd065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c'
K1097_REL = 'k1097/output/safe8-refuted50-refsolve-20261120.json'
FOLD23_REL = 'fold23/output/win8-root208090020004-receipt-fold-20261120.json'
FOLD23_SHA = '04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59'
MACHINE_NAME = 'fold_win8_root438000000818.py'
RECEIPT_RELPATH = 'fold24/output/win8-root438000000818-receipt-fold-20261120.json'
BUNDLED_AUDITOR_NAME = 'verify_fold24_independent.py'
TAMPER_CASES = [('T1-worklist-offset-777', 'inputs/worklist.csv', 777),
                ('T2-k1136-cert-offset-12345', CERT_RELPATH, 12345)]

PINS = { "ex48/output/secondThirdFold.json": "7923a0fe5331d1f7c896748031c4071b68fcc13a", "fold4rec/fold4.json": "38715413d6dd23b97717c92d73d8b4a0af807cda", "fold56rec/fold56.json": "134796a7de1e472c26e35defd7340d208a10b9b0", "fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json": "5b1a30f9b56230382d502aa66ea89d3083b16dd2", "fold_fourth_fifth_sixth.py": "d8068a8eea48fde5203ac6342abd4df2bd584b99", "inputs/audit.json": "7cdc7c9ef341b5d9759923b3fc4986231c48895f", "inputs/census.json": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0", "inputs/firstFoldTarball.tar.gz": "fa5f26a9dc9bd2fb8222aa8ba0431d7578043019", "inputs/globalFold.json": "753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc", "inputs/ledger.json": "e8785d509e8a11a37c0d03cc450455a14708c34d", "inputs/previousCostFold.json": "7e6144cc4bc92c34faa14bed3058cde64fb3880e", "inputs/worklist.csv": "2fee1d0718547a62e346d35f5858d7913e37c097" }
PIN256 = { "fold10/output/seventeenth-win7-receipt-fold-20261120.json": "bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a", "fold11/output/win8-root8003180-receipt-fold-20261120.json": "d7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e", "fold12/output/win8-root8005021-receipt-fold-20261120.json": "0f73795ce71aec83ba4a9f1b97a530891f3e6d1c807bfa47c9fbb88a1b33f5bd", "fold13/output/win8-root9840004-receipt-fold-20261120.json": "c2bf80511e816306bbb8dcf4efb450214234f020c513386c3b3a82045f71e9ae", "fold14/output/win8-root9090022-receipt-fold-20261120.json": "ed3159fdb8cf2dd8884beb845cd4ef776cbc8b4b7b442d568d895cd930a13f71", "fold15/output/win8-root120000038-receipt-fold-20261120.json": "bae2b3c182da6b0b06be530604f43d1bfa3bf008190860dad6d27f2b9c285aef", "fold16/output/win8-root8890020-receipt-fold-20261120.json": "edd552588e265ada1cf015b4359584288cca3f18686c0fc8ca1536b6458b969b", "fold17/output/win8-root22081000-receipt-fold-20261120.json": "1175244d1da269b1851d5298a824b12a6ed445edc99307acc9c0fefd803bd674", "fold18/output/win8-root00901010-receipt-fold-20261120.json": "18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026", "fold19/output/win8-root1009000-receipt-fold-20261120.json": "c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae", "fold20/output/win8-root08d10000-receipt-fold-20261120.json": "76fd255bf16f0e434d15579cf148015bd564929e85910172f0a0ef87015842a2", "fold21/output/win8-root80880200-receipt-fold-20261120.json": "9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39", "fold22/output/win8-root840500-receipt-fold-20261120.json": "f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488", "fold23/output/win8-root208090020004-receipt-fold-20261120.json": "04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59", "foldv2/output/eighth-win7-receipt-fold-20261119.json": "afcf7d0ad0d6ca1edf31e150a7ba840f802a6382506f4a662b4e13567fbd30a2", "foldv2/output/seventh-win7-receipt-fold-20261119.json": "f1baf15942d3efeaa3ca75c4d803148239269715e297aaf9b00042611543b737", "fs13/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json": "24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2", "k1096/certs/win8-root-00000000000000003800000008003180-20261120.n11": "1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c", "k1096/output/win8-cert-extract-verification-20261120.json": "ad0d9fb3a30edbd76fcb5562ab01f1e7e51781381377a04fa4a195378eb887da", "k1097/output/safe8-refuted50-refsolve-20261120.json": "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40", "k1106/certs/win8-root-00000000000000003800000008005021-20261120.n11": "69f32661d80ae0887ecf385cb690e0d4300c5ad28686ec42fc83e93da79ac6f5", "k1106/output/win8-cert-extract-verification-20261120.json": "0bd2dd10c1d5b735a04f31425003c635d80266e4c03a6bef0fdff212d499408f", "k1108/certs/win8-root-00000000000000003800000009840004-20261120.n11": "5b114b9e739b7a0a300434afb7ec5326564fc54b0d234df5e3d61abc44541143", "k1108/output/win8-cert-extract-verification-20261120.json": "2e453a76fc3168b8eb2e5c224d4a271eea0839eb5256d51fd9c02eb54bb1f648", "k1109/certs/win8-root-00000000000000909002200080100000-20261120.n11": "b8a15f9aac5e5f802f85459318247cb20bc983e3b2372167917ba8138cbc7a54", "k1109/output/win8-cert-extract-verification-20261120.json": "00836a6e859c780e2204b1aea427eefc044f0d4c5a6b8e8c33505a57fa950bb4", "k1113/certs/win8-root-00000000010000889002000080100000-20261120.n11": "105e1e2ad59f4f6baa85f37dde7306b98fc96d2164edf5b5d12205b1c71e2bc4", "k1113/output/win8-cert-extract-verification-20261120.json": "b8c264e671b9e26fa9caf8cd2454f75b13c992d548e2d5ed0b02f2bec75c5236", "k1114/certs/win8-root-00000000012000003800080009000000-20261120.n11": "5a1359033325e918cf5d9cd2d60ff63fc2fd45e30b926e79330560a7a3a23c4c", "k1114/output/win8-cert-extract-verification-20261120.json": "ab8cd535c14637c150c02ceeb688b335eb2da9dc1c5778b6a7c05a1a0906f67e", "k1117/certs/win8-root-00000000000000801202000022081000-20261120.n11": "f62f6704a0d9a1366d333529dd9e742813fe87814f3857a00406d6cfc87f3c8f", "k1117/output/win8-cert-extract-verification-20261120.json": "3d97ac6d90e239638b019c95218f0051b432ccdcc6dd2d25e805dcbab11024d9", "k1119/certs/win8-root-00000000000000801212000001009000-20261120.n11": "b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c", "k1119/output/win8-cert-extract-verification-20261120.json": "4696ce1475fd3313c6bb46ebf553e48db4eff2d7182edb0f2b8015258fd17100", "k1120/certs/win8-root-00000000000000801202000000901010-20261120.n11": "d6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1", "k1120/output/win8-cert-extract-verification-20261120.json": "ea6f1945c5a8ff359b93336a0a5d4e29035928447503e2bf2f0d13277174b516", "k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11": "8513e36613c2676fb82816f47a1ecdda674264eedb9c583dae2616346f4000d2", "k1121/output/win8-cert-extract-verification-20261120.json": "0088ebab040a29e608c987fb8ae866abf59253d60455b0d2ca6b6ef963170940", "k1123/certs/win8-root-00000000000020809002000480100000-20261120.n11": "b8145352cc1d8e21247595bdaedcb123c8e34cf0fb476502a561b46a106f701e", "k1123/output/win8-cert-extract-verification-20261120.json": "6ea634c9fdd005626904669e08cb7139e59e78120a0b8c9e1dd48fde0b70ddf0", "k1124/certs/win8-root-00000000000000801202000800880200-20261120.n11": "eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf", "k1124/output/win8-cert-extract-verification-20261120.json": "422e61095e80ee5ea6a52278e2ba52bb18d4ea301cab4c26e1e45d9c9701f172", "k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11": "21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc", "k1125/output/win8-cert-extract-verification-20261120.json": "06c65f7611b7fea17131d5e13b28792aee1b7d723e7b8cdb1cb3b54012282886", "k1136/certs/win8-root-00000000000000043800000008180010-20261120.n11": "dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004", "k1136/output/win8-cert-extract-verification-20261120.json": "d065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c", "resolve6/output/post-saturation-full-cache-join-resolve6-20261120.json": "e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a", "sv17pub/certs/win7-root-00004000000000821082000000000100-20261120.n11": "21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8", "sv17pub/output/seventeenth-cert-triple-verification-20261120.json": "c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc" }

# ---------------------------------------------------------------- gate bookkeeping
GATES = []
def need(ok, name):
    if not ok:
        print('GATE FAILED: ' + name)
        sys.exit(1)
    GATES.append(name)

def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()

def blob_sha_bytes(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

# ---------------------------------------------------------------- fresh geometry
# Explicit D4 coordinate maps on the 11x11 board. Pieces are (x, y); cell index
# is 11*y + x. No table sharing with any published machine.
_D4_KINDS = ['id', 'r90', 'r180', 'r270', 'fx', 'fy', 'd1', 'd2']

def d4_point(kind, x, y):
    if kind == 'id': return (x, y)
    if kind == 'r90': return (10 - y, x)
    if kind == 'r180': return (10 - x, 10 - y)
    if kind == 'r270': return (y, 10 - x)
    if kind == 'fx': return (x, 10 - y)
    if kind == 'fy': return (10 - x, y)
    if kind == 'd1': return (y, x)
    return (10 - y, 10 - x)

_PTMAP = {}
for _k in _D4_KINDS:
    _m = [0] * 121
    for _i in range(121):
        _x, _y = _i % 11, _i // 11
        _m[_i] = 11 * d4_point(_k, _x, _y)[1] + d4_point(_k, _x, _y)[0]
    _PTMAP[_k] = _m

def move_mask(mask, kind):
    out = 0
    m = mask
    bit = 0
    while m:
        if m & 1:
            out |= 1 << _PTMAP[kind][bit]
        m >>= 1
        bit += 1
    return out

def canon_form(mask):
    best = None
    for k in _D4_KINDS:
        z = move_mask(mask, k)
        if best is None or z < best:
            best = z
    return best

def canon_str(mask):
    return format(canon_form(mask), '032x')

def stones_of(mask):
    out = []
    m = mask
    bit = 0
    while m:
        if m & 1:
            out.append(bit)
        m >>= 1
        bit += 1
    return out

def card(mask):
    n = 0
    while mask:
        mask &= mask - 1
        n += 1
    return n

def _det3(p0, p1, p2):
    x0, y0 = p0 % 11, p0 // 11
    x1, y1 = p1 % 11, p1 // 11
    x2, y2 = p2 % 11, p2 // 11
    return (x0 * (y1 - y2) - x1 * (y0 - y2) + x2 * (y0 - y1))

def concircular4(points):
    """Zero of the full 4x4 incidence determinant [x, y, x^2+y^2, 1] over the
    four points, by cofactor expansion along the first row. Zero iff the four
    points are concyclic or collinear (the published unsafe-move criterion)."""
    cols = []
    for p in points:
        x, y = p % 11, p // 11
        cols.append([x, y, x * x + y * y, 1])

    def minor(col):
        rows = []
        for i in (1, 2, 3):
            rows.append([cols[i][c] for c in range(4) if c != col])
        a = rows[0]; b = rows[1]; c = rows[2]
        return (a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0]))
    total = 0
    for col in range(4):
        total += ((-1) ** col) * cols[0][col] * minor(col)
    return total == 0

def unsafe_quads(mask):
    pts = stones_of(mask)
    n = 0
    for quad in combinations(pts, 4):
        if concircular4(quad):
            n += 1
    return n

def legal_move_count(mask):
    """Fresh rederivation of the root mobility convention: an empty cell is a
    legal next move unless it is concircular or collinear with any three stones
    (incidence determinant over all C(k,3) triples)."""
    pts = stones_of(mask)
    occupied = set(pts)
    n = 0
    for d in range(121):
        if d in occupied:
            continue
        ok = True
        for tri in combinations(pts, 3):
            if concircular4(list(tri) + [d]):
                ok = False
                break
        if ok:
            n += 1
    return n

# ---------------------------------------------------------------- chain bookkeeping
SPAN_SAFE = 'no game-theoretic value is claimed anywhere in this verification'

class Bookkeeping:
    """Fresh re-derivation of the whole published fold1..fold23 chain state that
    the fold24 receipt joins, then of the receipt itself. Every step is checked
    against the corresponding published record field."""

    def __init__(self, W):
        self.W = W

    def load(self, rel):
        with open(os.path.join(self.W, rel)) as f:
            return json.load(f)

    def build(self):
        W = self.W
        # -- base worklist
        wl = {}
        with open(os.path.join(W, 'inputs/worklist.csv')) as f:
            r = csv.reader(f)
            hdr = next(r)
            ix = hdr.index('s6_canonical_hex')
            cx = hdr.index('own_candidates_s6_s7_edge_cost')
            kx = hdr.index('category')
            for a in r:
                wl[a[ix]] = (int(a[cx]), a[kx])
        need(len(wl) == 6438, 'C-base-worklist-6438')
        self.wl = wl

        led = self.load('inputs/ledger.json')
        old66 = set(led['derived']['closed_rows_66'])
        gf = self.load('inputs/globalFold.json')
        oldGlobal = set(x['row_hex'] for x in gf['receipts_by_row'])
        open0 = {h: v for h, v in wl.items() if h not in old66 and h not in oldGlobal}
        need(len(open0) == 6259 and sum(v[0] for v in open0.values()) == 495507,
             'C-base-open-global-6259-495507')
        prev = self.load('inputs/previousCostFold.json')
        prior = set(x['row_hex'] for x in prev['new_receipt_coverage']['receipts_by_row'])
        openA = {h: v for h, v in open0.items() if h not in prior}
        need(len(openA) == 6240 and sum(v[0] for v in openA.values()) == 493965,
             'C-base-open-78c79c-6240-493965')
        with tarfile.open(os.path.join(W, 'inputs/firstFoldTarball.tar.gz'), 'r:gz') as t:
            firstFold = None
            for m in t.getmembers():
                if m.name.endswith('output/first-win7-root-receipt-fold-20261119.json'):
                    firstFold = json.load(t.extractfile(m))
        need(firstFold is not None and firstFold['status'] == 'fold-complete', 'C-firstfold-loaded')
        firstClosed = set(x['row_hex'] for x in firstFold['new_receipt_coverage']['rows'])
        open1 = {h: v for h, v in openA.items() if h not in firstClosed}
        need(len(open1) == 6236 and sum(v[0] for v in open1.values()) == 493703,
             'C-open-first-6236-493703')
        stf = self.load('ex48/output/secondThirdFold.json')
        need(stf['status'] == 'fold-complete' and stf['receipt_count'] == 2, 'C-secondthird-gate')
        rows23 = []
        for rr in stf['receipts']:
            rows23.extend(rr['covered_s6_rows'])
        open2 = {h: v for h, v in open1.items() if h not in set(rows23)}
        need(len(open2) == 6229 and sum(v[0] for v in open2.values()) == 493184,
             'C-open-secondthird-6229-493184')
        f4 = self.load('fold4rec/fold4.json')
        need(f4['status'] == 'fold-complete', 'C-fold4-gate')
        rows4 = [x['row_hex'] for x in f4['new_receipt_coverage']['rows']]
        open3 = {h: v for h, v in open2.items() if h not in set(rows4)}
        need(len(open3) == 6226 and sum(v[0] for v in open3.values()) == 492970,
             'C-open-fourth-6226-492970')
        f56 = self.load('fold56rec/fold56.json')
        need(f56['status'] == 'fold-complete', 'C-fold56-gate')
        rows56 = [x['row_hex'] for x in f56['new_receipt_coverage']['rows']]
        open4 = {h: v for h, v in open3.items() if h not in set(rows56)}
        need(len(open4) == 6224 and sum(v[0] for v in open4.values()) == 492830,
             'C-open-fifthsixth-6224-492830')
        f7 = self.load('foldv2/output/seventh-win7-receipt-fold-20261119.json')
        need(f7['status'] == 'fold-complete' and f7['receipt_count'] == 1, 'C-fold7-gate')
        rows7 = []
        for rr in f7['receipts']:
            rows7.extend(rr['covered_s6_rows'])
        open5 = {h: v for h, v in open4.items() if h not in set(rows7)}
        need(len(open5) == 6223 and sum(v[0] for v in open5.values()) == 492762,
             'C-open-seventh-6223-492762')
        f8 = self.load('foldv2/output/eighth-win7-receipt-fold-20261119.json')
        need(f8['status'] == 'fold-complete' and f8['receipt_count'] == 1, 'C-fold8-gate')
        rows8 = []
        for rr in f8['receipts']:
            rows8.extend(rr['covered_s6_rows'])
        open8 = {h: v for h, v in open5.items() if h not in set(rows8)}
        need(len(open8) == 6222 and sum(v[0] for v in open8.values()) == 492688,
             'C-open-eighth-6222-492688')
        closedHis = [old66, oldGlobal, prior, firstClosed, set(rows23), set(rows4), set(rows56), set(rows7), set(rows8)]

        # -- census / parents
        census = self.load('inputs/census.json')
        parents = {p['hex']: p for p in census['open_s5_census']}
        need(len(parents) == 174, 'C-census-parents-174')
        parents_int = {int(h, 16): h for h in parents}
        self.parents = parents
        pcache = {}
        def row_parents(h):
            if h in pcache:
                return pcache[h]
            mask = int(h, 16)
            ps = set()
            for q in stones_of(mask):
                c = canon_form(mask ^ (1 << q))
                if c in parents_int:
                    ps.add(parents_int[c])
            pcache[h] = ps
            return ps
        def demand(h):
            d = {'c1': 0, 'c2': 0, 'c4': 0}
            for p in row_parents(h):
                c = parents[p]['classes']
                if c & 1: d['c1'] += 1
                if c & 2: d['c2'] += 1
                if c & 4: d['c4'] += 1
            return d
        self.row_parents = row_parents
        self.demand = demand

        # -- fold9 (ninth..twelfth)
        tf9 = self.load('fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json')
        need(tf9['status'] == 'fold-complete' and tf9['receipt_count'] == 4, 'C-fold9-gate')
        rows9 = []
        for rr in tf9['receipts']:
            need(len(rr['covered_s6_rows']) >= 1, 'C-fold9-receipt-nonempty')
            rows9.extend(rr['covered_s6_rows'])
        for h in rows9:
            need(h in open8, 'C-fold9-row-open-' + h)
        open9 = {h: v for h, v in open8.items() if h not in set(rows9)}
        need(len(open9) == 6213 and sum(v[0] for v in open9.values()) == 492021,
             'C-open-fold9-6213-492021')
        fa9 = tf9['frontier_after']
        need(fa9['unique_remaining_s6'] == len(open9) and fa9['sum_remaining_cost'] == 492021
             and fa9['solved_s6_in_manifest'] == 1635, 'C-fold9-fa-fields')
        need(fa9.get('unique_remaining_s6', -1) == 6213 or 'unique_remaining_s6' not in fa9, 'C-fold9-fa-shape')
        inc = {p: 0 for p in parents}
        for h in open9:
            for p in row_parents(h):
                inc[p] += 1
        need(sum(inc.values()) == fa9['parent_row_incidence'] == 11826, 'C-fold9-incidence-11826')
        if 'remaining_s5_orbits' in fa9:
            need(fa9['remaining_s5_orbits'] == sum(1 for v in inc.values() if v > 0), 'C-fold9-s5-orbits')
        closedHis.append(set(rows9))
        sol = 1635

        # -- fs13 (thirteenth..sixteenth)
        fs13 = self.load('fs13/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json')
        need(fs13['status'] == 'fold-complete' and fs13['receipt_count'] == 4, 'C-fs13-gate')
        rows1316 = []
        for rr in fs13['receipts']:
            need(len(rr['covered_s6_rows']) >= 1, 'C-fs13-receipt-nonempty')
            rows1316.extend(rr['covered_s6_rows'])
        need(len(rows1316) == len(set(rows1316)), 'C-fs13-rows-unique')
        for h in rows1316:
            need(h in open9, 'C-fs13-row-open-' + h)
        open74 = {h: v for h, v in open9.items() if h not in set(rows1316)}
        need(len(open74) == 6209 and sum(v[0] for v in open74.values()) == 491722,
             'C-open-fs13-6209-491722')
        fa13 = fs13['frontier_after']
        need(fa13['unique_remaining_s6'] == len(open74) and fa13['sum_remaining_cost'] == 491722
             and fa13['solved_s6_in_manifest'] == 1639 and fa13['parent_row_incidence'] == 11818,
             'C-fs13-fa-fields')
        sol = 1639
        for h in rows1316:
            for p in row_parents(h):
                inc[p] -= 1
        need(sum(inc.values()) == 11818, 'C-fs13-incidence-11818')
        if 'remaining_s5_orbits' in fa13:
            need(fa13['remaining_s5_orbits'] == sum(1 for v in inc.values() if v > 0), 'C-fs13-s5-orbits')
        residual74 = fs13['five_parent_target_after']['residual_row_hex_after']
        need(len(residual74) == 74 and residual74 == sorted(set(residual74)), 'C-residual74-sorted')
        need(fs13['five_parent_target_after']['closed_target_rows_total'] == 38, 'C-fs13-closed-38')
        closedHis.append(set(rows1316))

        # -- target machinery
        audit = self.load('inputs/audit.json')
        need(audit['all_pass'] is True and audit['check_count'] == 23, 'C-audit-23-pass')
        need(audit['derived']['maximum_root_span'] == 2, 'C-audit-maxrootspan-2')
        target112 = sorted(set(r for x in audit['derived']['witness_pairs'] for r in x['rows']))
        need(len(target112) == 112, 'C-target-112')
        need(all(h in set(target112) for h in residual74), 'C-residual74-subset-target')
        residualSet = set(residual74)
        closed_total = 38

        # -- fold10..fold23 chain
        # rel, wantN, wantC, wantS, wantInc, wantClosed, wantResidual, wantCovered, wantTarget, wantNeeded, wantNeededCost
        chain = [
            ('fold10/output/seventeenth-win7-receipt-fold-20261120.json', 6206, 491497, 1642, 11810, 40, 72, 3, 2, None, None),
            ('fold11/output/win8-root8003180-receipt-fold-20261120.json', 6201, 491110, 1647, 11803, 44, 68, 5, 4, 4504, 357196),
            ('fold12/output/win8-root8005021-receipt-fold-20261120.json', 6193, 490526, 1655, 11790, 47, 65, 8, 3, 4501, 356974),
            ('fold13/output/win8-root9840004-receipt-fold-20261120.json', 6184, 489813, 1664, 11775, 50, 62, 9, 3, 4492, 356261),
            ('fold14/output/win8-root9090022-receipt-fold-20261120.json', 6179, 489440, 1669, 11765, 54, 58, 5, 4, 4487, 355888),
            ('fold15/output/win8-root120000038-receipt-fold-20261120.json', 6173, 488954, 1675, 11753, 57, 55, 6, 3, 4481, 355402),
            ('fold16/output/win8-root8890020-receipt-fold-20261120.json', 6168, 488575, 1680, 11743, 61, 51, 5, 4, 4476, 355023),
            ('fold17/output/win8-root22081000-receipt-fold-20261120.json', 6161, 488094, 1687, 11729, 64, 48, 7, 3, 4469, 354542),
            ('fold18/output/win8-root00901010-receipt-fold-20261120.json', 6157, 487800, 1691, 11721, 67, 45, 4, 3, 4465, 354248),
            ('fold19/output/win8-root1009000-receipt-fold-20261120.json', 6152, 487418, 1696, 11711, 71, 41, 5, 4, 4460, 353866),
            ('fold20/output/win8-root08d10000-receipt-fold-20261120.json', 6144, 486819, 1704, 11701, 74, 38, 8, 3, 4452, 353267),
            ('fold21/output/win8-root80880200-receipt-fold-20261120.json', 6136, 486243, 1712, 11683, 77, 35, 8, 3, 4444, 352691),
            ('fold22/output/win8-root840500-receipt-fold-20261120.json', 6130, 485759, 1718, 11671, 80, 32, 6, 3, 4438, 352207),
            (FOLD23_REL, 6126, 485438, 1722, 11666, 83, 29, 4, 3, 4434, 351886),
        ]
        cur = open74
        fa_prev = fa13
        for (rel, wantN, wantC, wantS, wantInc, wantClosed, wantRes, wantCov, wantTgt,
             wantNec, wantNecC) in chain:
            tag = rel.split('/')[0]
            rec = self.load(rel)
            need(rec['status'] == 'fold-complete', 'C-' + tag + '-complete')
            need(rec['receipt_count'] == 1 and len(rec['receipts']) == 1, 'C-' + tag + '-single-receipt')
            rc = rec['receipts'][0]
            rows = list(rc['covered_s6_rows'])
            need(len(rows) == len(set(rows)) == wantCov, 'C-' + tag + '-covered-' + str(wantCov))
            for h in rows:
                need(h in cur, 'C-' + tag + '-row-open-' + h)
            extra = [h for h in rows if h not in residualSet]
            need(extra == rc['extra_s6_rows_not_in_target'], 'C-' + tag + '-extra-recorded')
            target_rows = list(rc['covered_five_parent_target_rows'])
            need(len(target_rows) == wantTgt and set(target_rows) <= residualSet,
                 'C-' + tag + '-target-' + str(wantTgt) + '-subset')
            cur = {h: v for h, v in cur.items() if h not in set(rows)}
            need(len(cur) == wantN and sum(v[0] for v in cur.values()) == wantC,
                 'C-' + tag + '-open-' + str(wantN) + '-' + str(wantC))
            fa = rec['frontier_after']
            need(fa['unique_remaining_s6'] == wantN and fa['sum_remaining_cost'] == wantC,
                 'C-' + tag + '-fa-count-cost')
            need(fa['solved_s6_in_manifest'] == wantS == sol + wantCov, 'C-' + tag + '-solved')
            sol = wantS
            if wantNec is not None:
                nec = [h for h in cur if demand(h)['c1'] == 0]
                need(len(nec) == wantNec == fa['s6_needed_by_open_classes'], 'C-' + tag + '-needed')
                need(sum(cur[h][0] for h in nec) == wantNecC == fa['cost_needed_by_open_classes'],
                     'C-' + tag + '-needed-cost')
            elif 's6_needed_by_open_classes' in fa:
                nec = [h for h in cur if demand(h)['c1'] == 0]
                need(len(nec) == fa['s6_needed_by_open_classes']
                     and sum(cur[h][0] for h in nec) == fa['cost_needed_by_open_classes'],
                     'C-' + tag + '-needed-soft')
            if 'remaining_s5_orbits' in fa:
                need(fa['remaining_s5_orbits'] == sum(1 for v in inc.values() if v > 0),
                     'C-' + tag + '-s5-orbits')
            for h in rows:
                for p in row_parents(h):
                    inc[p] -= 1
            need(sum(inc.values()) == wantInc == fa['parent_row_incidence'],
                 'C-' + tag + '-incidence-' + str(wantInc))
            for crr in rec['new_receipt_coverage']['rows']:
                need(crr['cost'] == wl[crr['row_hex']][0], 'C-' + tag + '-cost')
                need(crr['row_hex'] in rows, 'C-' + tag + '-coverage-among-covered')
            need(rc['closed_edge_cost'] == sum(wl[h][0] for h in rows), 'C-' + tag + '-closed-cost')
            residual_next = rec['five_parent_target_after']['residual_row_hex_after']
            need(len(residual_next) == wantRes and residual_next == sorted(set(residual_next)),
                 'C-' + tag + '-residual-' + str(wantRes) + '-sorted')
            need(sorted(residualSet - set(target_rows)) == residual_next, 'C-' + tag + '-residual-evolution')
            need(rec['five_parent_target_after']['closed_target_rows_total'] == wantClosed == closed_total + wantTgt,
                 'C-' + tag + '-closed-target-' + str(wantClosed))
            closed_total = wantClosed
            need(all(h in cur for h in residual_next), 'C-' + tag + '-residual-open')
            residualSet = set(residual_next)
            closedHis.append(set(rows))
            fa_prev = fa

        need(fa_prev['remaining_s5_orbits'] == 173, 'C-fold23-s5-173')
        need(closed_total == 83 and len(residualSet) == 29, 'C-fold23-chain-end')

        self.open29 = cur
        self.residual29 = residualSet
        self.inc = inc
        self.fa23 = fa_prev
        self.closedHistorical = set().union(*closedHis)
        self.closed_total = closed_total
        self.sol = sol
        nec29 = [h for h in cur if demand(h)['c1'] == 0]
        need(len(nec29) == fa_prev['s6_needed_by_open_classes'] == 4434, 'C-fold23-needed-4434')
        need(sum(cur[h][0] for h in nec29) == fa_prev['cost_needed_by_open_classes'] == 351886,
             'C-fold23-needed-cost-351886')
        return self

# ---------------------------------------------------------------- machine plumbing
def run_machine(wdir, iso_home=None, iso_cwd=None, hashseed=None):
    env = dict(os.environ)
    env['FOLD24_W'] = wdir
    env.pop('FOLD_PREVERIFIED_CHAIN', None)
    env.pop('PYTHONHASHSEED', None)
    if iso_home is not None:
        env['HOME'] = iso_home
    if hashseed is not None:
        env['PYTHONHASHSEED'] = hashseed
    cwd = iso_cwd if iso_cwd is not None else os.getcwd()
    p = subprocess.run([sys.executable, os.path.join(wdir, MACHINE_NAME)],
                       env=env, cwd=cwd, capture_output=True, text=True)
    return p

def fresh_copy(master, dest):
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(master, dest)

# ---------------------------------------------------------------- main
def main():
    if len(sys.argv) < 4:
        print('usage: verify_fold24_external_20261120.py <W_pristine_master> <pub_dir> <out_json>')
        return 2
    Wmaster = os.path.abspath(sys.argv[1])
    pubdir = os.path.abspath(sys.argv[2])
    outpath = os.path.abspath(sys.argv[3])
    tag = os.path.splitext(os.path.basename(outpath))[0]
    rroot = os.path.join(os.path.dirname(Wmaster), 'x-' + tag)

    # ---- P-gates: published bytes
    pub_receipt_b = open(os.path.join(pubdir, 'win8-root438000000818-receipt-fold-20261120.json'), 'rb').read()
    pub_machine_b = open(os.path.join(pubdir, MACHINE_NAME), 'rb').read()
    pub_audit_b = open(os.path.join(pubdir, 'independent-audit.json'), 'rb').read()
    pub_repro_b = open(os.path.join(pubdir, 'reproduction.log'), 'rb').read()
    pub_recon_b = open(os.path.join(pubdir, 'reconstruct_inputs.py'), 'rb').read()
    need(sha_bytes(pub_receipt_b) == PUB_RECEIPT_SHA, 'P-receipt-sha256')
    need(sha_bytes(pub_machine_b) == PUB_MACHINE_SHA, 'P-machine-sha256')
    need(sha_bytes(pub_audit_b) == PUB_AUDIT_SHA, 'P-bundled-audit-sha256')
    need(sha_bytes(pub_repro_b) == PUB_REPROLOG_SHA, 'P-reproduction-log-sha256')
    need(sha_bytes(pub_recon_b) == PUB_RECONSTRUCT_SHA, 'P-reconstruct-sha256')
    receipt = json.loads(pub_receipt_b)

    # ---- I-gates: pristine master tree pins
    for rel, want in PINS.items():
        with open(os.path.join(Wmaster, rel), 'rb') as f:
            b = f.read()
        need(blob_sha_bytes(b) == want, 'I-blob-' + rel)
    for rel, want in PIN256.items():
        with open(os.path.join(Wmaster, rel), 'rb') as f:
            b = f.read()
        need(sha_bytes(b) == want, 'I-sha-' + rel)
    with open(os.path.join(Wmaster, PIN_K1091_SWEEP_REL), 'rb') as f:
        need(sha_bytes(f.read()) == PIN_K1091_SWEEP, 'I-k1091-sweep-sha256')
    with open(os.path.join(Wmaster, PIN_RUNNER_REL), 'rb') as f:
        need(blob_sha_bytes(f.read()) == PIN_RUNNER_V17, 'I-runner-v17-git-blob')
    need(not os.path.exists(os.path.join(Wmaster, RECEIPT_RELPATH)), 'I-master-pristine-no-fold24-output')
    with open(os.path.join(Wmaster, MACHINE_NAME), 'rb') as f:
        need(sha_bytes(f.read()) == PUB_MACHINE_SHA, 'I-w-machine-sha256')

    # ---- X-gates: pristine machine re-execution (4 runs)
    if os.path.isdir(rroot):
        shutil.rmtree(rroot)
    os.makedirs(os.path.join(rroot, 'iso-home'))
    os.makedirs(os.path.join(rroot, 'iso-cwd-a'))
    os.makedirs(os.path.join(rroot, 'iso-cwd-b'))
    iso_home = os.path.join(rroot, 'iso-home')
    runs = []
    for name, kw in [('same-env-1', {}), ('same-env-2', {}),
                     ('isolated-cwd-home', {'iso_home': iso_home,
                                            'iso_cwd': os.path.join(rroot, 'iso-cwd-a')}),
                     ('isolated-hashseed-random', {'iso_home': iso_home,
                                                   'iso_cwd': os.path.join(rroot, 'iso-cwd-b'),
                                                   'hashseed': 'random'})]:
        wX = os.path.join(rroot, 'W-' + name)
        fresh_copy(Wmaster, wX)
        pX = run_machine(wX, **kw)
        need(pX.returncode == 0, 'X-' + name + '-rc0')
        need('all 61 input pins verified' in pX.stdout, 'X-' + name + '-pins-line')
        need('fold23 machine pristine rerun verified' in pX.stdout, 'X-' + name + '-chain-rerun')
        need('"status": "fold-complete"' in pX.stdout, 'X-' + name + '-stdout-final')
        with open(os.path.join(wX, RECEIPT_RELPATH), 'rb') as f:
            shaX = sha_bytes(f.read())
        need(shaX == PUB_RECEIPT_SHA, 'X-' + name + '-receipt-byte-identical')
        runs.append({'mode': name, 'rc': 0, 'receipt_sha256': shaX})
        if name == 'same-env-1':
            wA = wX

    # ---- V-gates: published bundled auditor re-execution on run 1's tree
    verifier = os.path.join(pubdir, BUNDLED_AUDITOR_NAME)
    with open(verifier, 'rb') as f:
        need(sha_bytes(f.read()) == PUB_BUNDLED_AUDITOR_SHA, 'V-bundled-auditor-sha256')
    audit_out = os.path.join(wA, 'fold24/output/independent-audit.json')
    if os.path.exists(audit_out):
        os.remove(audit_out)
    pV = subprocess.run([sys.executable, verifier, wA, audit_out],
                         capture_output=True, text=True)
    need(pV.returncode == 0, 'V-bundled-auditor-rc0')
    with open(audit_out, 'rb') as f:
        auditout_b = f.read()
    need(sha_bytes(auditout_b) == PUB_AUDIT_SHA, 'V-bundled-audit-output-byte-identical')
    aud_obj = json.loads(auditout_b)
    need(aud_obj['status'] == 'PASS' and aud_obj['check_count'] == 46, 'V-bundled-audit-46-pass')

    # ---- T-gates: 1-byte XOR tamper, fail-closed
    tamper_results = []
    for name, rel, off in TAMPER_CASES:
        wT = os.path.join(rroot, 'W-' + name)
        fresh_copy(Wmaster, wT)
        fp = os.path.join(wT, rel)
        with open(fp, 'rb') as f:
            b = bytearray(f.read())
        b[off] ^= 0x01
        with open(fp, 'wb') as f:
            f.write(bytes(b))
        pT = run_machine(wT)
        need(pT.returncode != 0, 'T-' + name + '-fail-closed-rc')
        need(not os.path.exists(os.path.join(wT, RECEIPT_RELPATH)), 'T-' + name + '-receipt-unwritten')
        need('GATE FAILED' in (pT.stdout + pT.stderr), 'T-' + name + '-gate-message')
        tamper_results.append({'case': name, 'input': rel, 'offset': off, 'result': 'fail-closed'})

    # ---- E-gates: independent bookkeeping re-derivation vs published receipt record
    bk = Bookkeeping(Wmaster).build()
    need(receipt['schema'] == 'n11-five-parent-win8-root438000000818-receipt-fold-20261120-v1', 'E-schema')
    need(receipt['date'] == '2026-11-20' and receipt['status'] == 'fold-complete', 'E-date-status')
    need(receipt['receipt_ordinal'] == 'thirty-first (fold24, fourteenth WIN8 receipt fold)', 'E-ordinal')
    need(receipt['single_owner_note'] == 'research/log/2026-11-20-n11-fold24-win8-root438000000818-single-owner-note.md',
         'E-single-owner-note-path')
    need(receipt['previous_fold']['frontier_after'] == bk.fa23, 'E-prev-fold-fa-equals-fa23')
    need(str(receipt['previous_fold']['record']).startswith('research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/output/')
         and FOLD23_SHA in receipt['previous_fold']['record'], 'E-prev-fold-record-pin')
    need(receipt['frontier_before'] == bk.fa23 ==
         {'solved_s6_in_manifest': 1722, 'remaining_s5_orbits': 173, 'unique_remaining_s6': 6126,
          'sum_remaining_cost': 485438, 's6_needed_by_open_classes': 4434,
          'cost_needed_by_open_classes': 351886, 'parent_row_incidence': 11666}, 'E-frontier-before')
    need(receipt['receipt_count'] == 1 and len(receipt['receipts']) == 1, 'E-receipt-count')
    rr = receipt['receipts'][0]
    need(rr['root'] == rr['raw_root_hex'] == ROOT_HEX and rr['receipt'] == 'thirty-first', 'E-receipt-root-fields')
    need(rr['stones'] == 8 and rr['verdict'] == 'WIN8-D10' and rr['legal_next_moves'] == 50, 'E-verdict-stones-moves')
    need(rr['unique_strategy_rows'] == 34843 and rr['certificate_bytes'] == 1260393, 'E-strategy-rows-bytes')
    need(rr['certificate_sha256'] == PIN256[CERT_RELPATH], 'E-receipt-cert-sha')

    # certificate_source provenance block
    cs = receipt['certificate_source']
    need(cs['verification_sha256'] == PIN256[K1136_VERIF_REL] == K1136_VERIF_SHA, 'E-cert-source-verif-sha')
    need(cs['certificate_path'] == 'research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/certs/win8-root-00000000000000043800000008180010-20261120.n11',
         'E-cert-source-path')
    need(cs['certificate_sha256'] == PIN256[CERT_RELPATH], 'E-cert-source-cert-sha')
    need(PIN_K1091_SWEEP in cs['sweep_basis'] and K1097_REL.split('/')[-1] in cs['claims_record'],
         'E-cert-source-sweep-claims')
    need(receipt['source_blob_pins'] == PINS, 'E-source-blob-pins-equal')
    need(receipt['source_sha256_pins'] == PIN256, 'E-source-sha-pins-equal')

    # K1136 verification record recheck (fresh)
    k1136 = bk.load(K1136_VERIF_REL)
    need(k1136['schema'] == 'win8-cert-extract-verification-v1', 'E-k1136-schema')
    need(k1136['all_gates_pass'] is True and k1136['gate_count'] == 19 and len(k1136['gates']) == 19,
         'E-k1136-19-gates')
    need(all(g['passed'] for g in k1136['gates']), 'E-k1136-all-passed')
    need(k1136['root'] == ROOT_HEX and k1136['experiment'] == 'n11-residual29-win8-cert-extract-root438000000818-20261120',
         'E-k1136-root-experiment')
    gmap = {}
    for g in k1136['gates']:
        need(g['gate'] not in gmap, 'E-k1136-gate-unique-' + g['gate'])
        gmap[g['gate']] = g
    need(gmap['g01_k1091_master_sha256_pin']['detail'] == PIN_K1091_SWEEP, 'E-k1136-g01')
    need(gmap['g02_runner_v17_blob_pin_recorded']['detail'] == PIN_RUNNER_V17
         and gmap['g03_runner_v17_copy_git_blob']['detail'] == PIN_RUNNER_V17, 'E-k1136-g02g03')
    need(gmap['g04_root_shape_safe']['detail'] == {'quadruple_free': True, 'stones': 8}, 'E-k1136-g04')
    need(gmap['g05_root_mobility_50']['detail'] == 50, 'E-k1136-g05')
    need(gmap['g06_k1091_root_probes_win_uncapped']['detail'] == {
        'andclose0': {'capped': False, 'loss': True, 'nodes': 1054873, 'terminalStoneRange': [14, 18]},
        'andclose1': {'capped': False, 'loss': True, 'nodes': 882327, 'terminalStoneRange': [14, 18]},
    }, 'E-k1136-g06')
    Claim = sorted(gmap['g07_k1091_root_claimed_coverage_3rows']['detail'])
    need(len(Claim) == 3 and Claim == sorted(k1136['recorded']['k1091_claimed_coverage_rows']), 'E-k1136-g07')
    need(gmap['g08_probe_reproduction_matches_k1091']['detail'] == {'pilot_d6': 4, 'reproduced': {'andclose0': 2, 'andclose1': 2}},
         'E-k1136-g08')
    need(gmap['g09_root_move_list_equals_rederivation']['detail'] == {'file': 50, 'rederived': 50}, 'E-k1136-g09')
    need(gmap['g10_extraction_runs_a1_a2_clean']['detail'] == {'a1_moves': 50, 'a2_moves': 50}, 'E-k1136-g10')
    need(gmap['g11_a1_a2_per_move_node_exact_repeat']['detail'] == {'identical_moves': 50}, 'E-k1136-g11')
    need(gmap['g12_extraction_run_b_single_process_clean']['detail'] == {'b_moves': 50}, 'E-k1136-g12')
    need(gmap['g13_node_accounting_chunk_vs_single']['detail'] == {'a1_chunk_total_nodes': 3539166, 'b_single_process_nodes': 2564865},
         'E-k1136-g13-node-facts-not-verdicts')
    need(gmap['g14_certificate_format_sorted_unique']['detail'] == {'bytes': 1260393, 'rows': 34843, 'sha256': PIN256[CERT_RELPATH]},
         'E-k1136-g14')
    need(gmap['g15_run_b_rowcount_matches_certificate']['detail'] == {'b_nRows': 34843, 'cert': 34843}, 'E-k1136-g15')
    need(gmap['g16_third_method_traversal_pass']['detail'] == {
        'extra': 0, 'failure': None, 'loser_reply_edges': 67581, 'loser_states': 14382, 'missing': 0,
        'subroot_mobility': 50, 'terminal_count': 13173, 'terminal_range': [14, 18],
        'visited_states': 77154, 'winner_states': 49599}, 'E-k1136-g16')
    need(gmap['g17_three_method_aggregate_agreement']['detail'] == {
        'bareiss_subroots': 50, 'bigint_terminal_count': 13173, 'third_method_terminal_count': 13173}, 'E-k1136-g17')
    need(gmap['g18_interpretation_guard_present']['detail'] == '5 guard lines', 'E-k1136-g18')
    g19 = gmap['g19_k1097_footprint_and_fold23_residual_open']['detail']
    need(sorted(g19['claimed']) == Claim and g19['claimed_rows_open_in_residual29'] == 3
         and g19['residual29_rows'] == 29, 'E-k1136-g19')
    need(g19['fold23_sha256'] == PIN256[FOLD23_REL] == FOLD23_SHA, 'E-k1136-g19-fold23-pin')
    need(g19['k1097_sha256'] == PIN256[K1097_REL], 'E-k1136-g19-k1097-pin')
    need(k1136['recorded']['certificate']['sha256'] == PIN256[CERT_RELPATH], 'E-k1136-recorded-cert-sha')
    need(k1136['recorded']['extraction_nodes'] == {'run_a1_chunked': 3539166, 'run_b_single_process': 2564865},
         'E-k1136-node-accounting')
    tm = k1136['recorded']['third_method']
    need(tm['root_first_moves'] == 50 and tm['terminal_count'] == 13173 and tm['terminal_range'] == [14, 18]
         and tm['visited_states'] == 77154 and tm['winner_states'] == 49599
         and tm['loser_states'] == 14382 and tm['loser_reply_edges'] == 67581, 'E-k1136-third-method-agg')

    # certificate bytes (fresh)
    with open(os.path.join(Wmaster, CERT_RELPATH), 'rb') as f:
        cert_b = f.read()
    need(sha_bytes(cert_b) == PIN256[CERT_RELPATH], 'E-cert-sha256')
    need(len(cert_b) == 1260393, 'E-cert-bytes')
    lines = cert_b.decode().splitlines()
    need(lines[0] == 'n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS', 'E-cert-header')
    need(lines[1] == 'root ' + ROOT_HEX, 'E-cert-root-line')
    need(len(lines) - 2 == 34843, 'E-cert-rows-34843')
    data_rows = lines[2:]
    need(all(len(x.split(' ')) == 2 and len(x.split(' ')[0]) == 32 for x in data_rows), 'E-cert-row-format')
    need(data_rows == sorted(data_rows) and len(set(data_rows)) == len(data_rows), 'E-cert-sorted-unique')

    # K1097 refsolve crosscheck (fresh)
    k1097 = bk.load(K1097_REL)
    need(k1097['status'] == 'refsolve-computed', 'E-k1097-status')
    need(len(k1097['gates']) == 27 and all(g['ok'] for g in k1097['gates']), 'E-k1097-27-ok')
    foot = k1097['win16_intrinsic_footprints']
    need(len(foot) == 16 and ROOT_HEX in foot, 'E-k1097-16-roots')
    need(foot[ROOT_HEX]['intrinsic_equals_claimed'] is True, 'E-k1097-root-intrinsic')
    need(sorted(foot[ROOT_HEX]['claimed']) == Claim and sorted(foot[ROOT_HEX]['intrinsic']) == Claim,
         'E-k1097-claimed-intrinsic')
    allc = []
    for r in foot:
        need(len(foot[r]['claimed']) == len(set(foot[r]['claimed'])), 'E-k1097-per-root-unique')
        allc.extend(foot[r]['claimed'])
    need(len(allc) == 49 and len(set(allc)) == 49, 'E-k1097-49-once')
    cnt = {}
    for h in allc:
        cnt[h] = cnt.get(h, 0) + 1
    need(all(v == 1 for v in cnt.values()), 'E-k1097-exactly-once-partition')
    need(all(h in bk.residual29 for h in Claim), 'E-k1097-claim-in-residual29')
    scope1 = k1097['scope1_refsolve_residual23']
    need(ROOT_HEX not in [s['root'] for s in scope1['greedy_selection']], 'E-k1097-root-not-greedy')
    residual23 = k1097['exclusion']['residual23_rows']
    need(len(residual23) == 23 and sorted(residual23) == residual23, 'E-k1097-residual23')
    need(not (set(residual23) & set(allc)), 'E-k1097-residual23-disjoint-claims')

    # fresh geometry of the root
    mask = int(ROOT_HEX, 16)
    need(card(mask) == 8, 'E-root-8-stones')
    need(unsafe_quads(mask) == 0, 'E-root-quadruple-free')
    need(canon_form(mask) == mask, 'E-root-d4-canonical')
    need(legal_move_count(mask) == 50, 'E-root-mobility-rederived-50')

    # two-method receipt geometry (fresh)
    setA = set()
    ops = 0
    for kind in _D4_KINDS:
        image = move_mask(mask, kind)
        for b1, b2 in combinations(stones_of(image), 2):
            setA.add(canon_str(image ^ (1 << b1) ^ (1 << b2)))
            ops += 1
    setB = set()
    for six in combinations(stones_of(mask), 6):
        sm = 0
        for b in six:
            sm |= 1 << b
        setB.add(canon_str(sm))
    need(setA == setB, 'E-two-methods-equal')
    need(len(setB) == 28, 'E-28-canonical-rows')
    geom = rr['independent_verification']['coverage_geometry_two_methods']
    need(geom['canonical_rows'] == sorted(setB), 'E-canonical-rows-equal-record')
    need(geom['d4_images_two_stone_removals_ops'] == ops == 224, 'E-geometry-ops-224')
    need(geom['c86_subsets'] == 28 and geom['canonical_row_sets_equal'] is True, 'E-geometry-record-fields')
    xt = rr['independent_verification']['extraction_and_triple']
    need(xt['gates'] == 19 and xt['all_pass'] is True and len(xt['methods']) == 4, 'E-extraction-triple-record')
    need(xt['third_method_aggregates'] == tm, 'E-third-method-agg-record')
    need(rr['independent_verification']['cross_method_union_exact'] is True, 'E-cross-union-record')

    # classification (fresh)
    my_class = {}
    for h in sorted(setB):
        if h in bk.open29:
            my_class[h] = 'open-frontier'
        elif h in bk.closedHistorical:
            my_class[h] = 'closed-before-this-receipt'
        elif h in bk.wl:
            my_class[h] = 'worklist-but-not-open'
        else:
            my_class[h] = 'not-in-worklist'
    need(all(v != 'worklist-but-not-open' for v in my_class.values()), 'E-no-chain-inconsistency')
    need(my_class == receipt['six_stone_subgeometry_classification'], 'E-classification-equals-record')

    # closure application (fresh)
    rootRows = sorted(h for h in setA if h in bk.open29)
    need(rootRows == rr['covered_s6_rows'] and len(rootRows) == 3, 'E-covered-rows')
    targetRows_new = sorted(h for h in rootRows if h in bk.residual29)
    need(targetRows_new == rr['covered_five_parent_target_rows'] == Claim, 'E-target-rows-equal-claim')
    extra_rows = [h for h in rootRows if h not in bk.residual29]
    need(extra_rows == rr['extra_s6_rows_not_in_target'] == [], 'E-extra-empty')
    closed_cost = sum(bk.open29[h][0] for h in rootRows)
    need(closed_cost == rr['closed_edge_cost'] == 225, 'E-closed-cost-225')

    deltas = {}
    for h in rootRows:
        for p in bk.row_parents(h):
            deltas[p] = deltas.get(p, 0) + 1
    pdeltas = []
    inc = dict(bk.inc)
    for p in sorted(deltas):
        before = inc[p]
        pdeltas.append({'parent_hex': p, 'classes': bk.parents[p]['classes'],
                        'rows_before': before, 'rows_closed': deltas[p],
                        'rows_after': before - deltas[p]})
    need(pdeltas == rr['parent_deltas'], 'E-parent-deltas-equal')
    need(sum(deltas.values()) == 6 and len(deltas) == 4, 'E-deltas-6-across-4')
    need(rr['affected_parents'] == 4, 'E-affected-parents-4')

    open_after = {h: v for h, v in bk.open29.items() if h not in set(rootRows)}
    for h in rootRows:
        for p in bk.row_parents(h):
            inc[p] -= 1
    needed_after = [h for h in open_after if bk.demand(h)['c1'] == 0]
    frontier_after = {
        'solved_s6_in_manifest': bk.fa23['solved_s6_in_manifest'] + len(rootRows),
        'remaining_s5_orbits': sum(1 for v in inc.values() if v > 0),
        'unique_remaining_s6': len(open_after),
        'sum_remaining_cost': sum(v[0] for v in open_after.values()),
        's6_needed_by_open_classes': len(needed_after),
        'cost_needed_by_open_classes': sum(open_after[h][0] for h in needed_after),
        'parent_row_incidence': sum(inc.values()),
    }
    need(frontier_after == receipt['frontier_after'] ==
         {'solved_s6_in_manifest': 1725, 'remaining_s5_orbits': 173, 'unique_remaining_s6': 6123,
          'sum_remaining_cost': 485213, 's6_needed_by_open_classes': 4431,
          'cost_needed_by_open_classes': 351661, 'parent_row_incidence': 11660}, 'E-frontier-after')

    # five-parent target ledger
    closedAllNew = bk.closed_total + len(targetRows_new)
    residualAfter = sorted(bk.residual29 - set(targetRows_new))
    need(closedAllNew == 86 and len(residualAfter) == 26, 'E-target-86-26')
    fpt = receipt['five_parent_target_after']
    need(fpt['closed_target_rows_total'] == closedAllNew, 'E-closed-total-field')
    need(fpt['residual_target_rows'] == 26 and fpt['residual_row_hex_after'] == residualAfter, 'E-residual26-field')

    # coverage rows (fresh; demand/parents/cost/category)
    rec_cov = receipt['new_receipt_coverage']['rows']
    need(receipt['new_receipt_coverage']['unique_s6_rows'] == 3
         and receipt['new_receipt_coverage']['closed_edge_cost'] == closed_cost, 'E-coverage-totals')
    need(len(rec_cov) == 3, 'E-coverage-3')
    mine = [{'row_hex': h, 'cost': bk.wl[h][0], 'category': bk.wl[h][1],
             'demand': bk.demand(h), 'parents': sorted(bk.row_parents(h))} for h in sorted(rootRows)]
    for m, t in zip(mine, rec_cov):
        need(m['row_hex'] == t['row_hex'], 'E-coverage-row-hex')
        need(m['cost'] == t['cost'], 'E-coverage-cost-' + m['row_hex'])
        need(m['category'] == t['category'], 'E-coverage-category-' + m['row_hex'])
        need(m['demand'] == t['demand'], 'E-coverage-demand-' + m['row_hex'])
        need(m['parents'] == t['parents'], 'E-coverage-parents-' + m['row_hex'])
        need(t['receipt'] == {'root': ROOT_HEX, 'verdict': 'WIN8-D10'}, 'E-coverage-receipt-tag')
    need(receipt['parent_closure'] == {'fully_closed_parent_count': 0, 'affected_unique_parents': 4},
         'E-parent-closure')

    # win candidate plan impact
    wpi = receipt['win_candidate_plan_impact']
    need(wpi['retired_win_candidate_root'] == ROOT_HEX, 'E-retired-root')
    need(wpi['rows_of_retired_root'] == Claim, 'E-retired-rows')
    need(wpi['retired_root_predecessor'] == '00000000000020809002000480100000', 'E-retired-predecessor')
    need(wpi['win16_candidates_remaining'] == 2 and wpi['win16_claimed_rows_remaining'] == 3, 'E-win16-remaining')
    need(wpi['residual23_untouched'] is True, 'E-residual23-untouched')
    need(not (set(residual23) & set(rootRows)), 'E-residual23-disjoint-receipt-rows')

    # controls and guards
    ctrls = receipt['controls']
    need(len(ctrls) == 86 and all(v is True for v in ctrls.values()), 'E-controls-86-true')
    ig = receipt['interpretation_guard']
    need(len(ig) == 5, 'E-interpretation-guard-5')
    need(ig[-1].endswith('classes 1/2/4 remain UNKNOWN.'), 'E-guard-unknown-lasting')
    need('REFUTED-D10 witnesses are NOT LOSS proofs' in ig[3], 'E-guard-refuted-not-loss')
    vjs = receipt['verdict_join_summary']
    need(vjs['receipt_root_is'].startswith('certificate-backed WIN8-D10'), 'E-verdict-join')

    # cleanup the copy farm
    shutil.rmtree(rroot)

    # ---- deterministic audit output
    audit = {
        'schema': 'n11-fold24-external-second-verification-20261120-v1',
        'status': 'PASS',
        'gate_count': len(GATES),
        'gates': GATES,
        'published_pins': {
            'receipt_sha256': PUB_RECEIPT_SHA,
            'machine_sha256': PUB_MACHINE_SHA,
            'bundled_independent_audit_sha256': PUB_AUDIT_SHA,
            'reproduction_log_sha256': PUB_REPROLOG_SHA,
            'reconstruct_inputs_sha256': PUB_RECONSTRUCT_SHA,
            'bundled_auditor_sha256': PUB_BUNDLED_AUDITOR_SHA,
            'k1091_sweep_sha256': PIN_K1091_SWEEP,
            'runner_v17_git_blob': PIN_RUNNER_V17,
        },
        'input_pins_verified': len(PINS) + len(PIN256),
        'machine_pristine_runs': runs,
        'bundled_auditor_reexec': {'rc': 0, 'output_sha256': PUB_AUDIT_SHA, 'check_count': 46,
                                   'byte_identical_to_published': True},
        'tamper_tests': tamper_results,
        'rederivation': {
            'root': ROOT_HEX,
            'root_stones': 8,
            'root_unsafe_quads': 0,
            'root_mobility_rederived': 50,
            'canonical_geometry_rows': sorted(setB),
            'geometry_ops_method_a': ops,
            'subsets_method_b': len(setB),
            'covered_rows': rootRows,
            'claim_rows': Claim,
            'extra_rows': extra_rows,
            'closed_edge_cost': closed_cost,
            'parent_deltas': pdeltas,
            'frontier_before': bk.fa23,
            'frontier_after': frontier_after,
            'target_closed_total': closedAllNew,
            'residual_target_after': residualAfter,
            'subgeometry_classification': my_class,
            'needed_rows_before': 4434,
            'needed_cost_before': 351886,
            'needed_rows_after': 4431,
            'needed_cost_after': 351661,
            'chain_summary': {'unique_open_s6': 6126, 'sum_open_cost': 485438,
                              'incidence': 11666, 'solved_s6': 1722,
                              'residual_target_rows': 29, 'closed_target_rows': 83},
        },
        'scope_guard': [
            'This verification re-tests the published fold24 receipt bookkeeping, machine determinism, bundled auditor, and fail-closed inputs. ' + SPAN_SAFE,
            'It closes no S6 row and no five-parent target row; the receipt fold itself already closed 3 rows in bookkeeping (86/112 targets closed, 26 remain).',
            'WIN8-D10 is a certificate for the game tree of the eight-stone root only; REFUTED-D10 is not a LOSS proof; node counts and solved counts are not win/loss readings.',
            'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
        ],
    }
    with open(outpath, 'w') as f:
        json.dump(audit, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps({'status': 'PASS', 'gate_count': len(GATES),
                      'audit_sha256': sha_bytes(open(outpath, 'rb').read()),
                      'machine_runs': len(runs), 'tamper_cases': len(tamper_results)}, indent=1))
    return 0

if __name__ == '__main__':
    sys.exit(main())
