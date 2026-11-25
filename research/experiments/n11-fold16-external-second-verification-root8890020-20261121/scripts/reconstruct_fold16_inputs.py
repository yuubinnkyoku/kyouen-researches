#!/usr/bin/env python3
"""Reconstruct the fold16 external-second-verification input trees from GitHub
at an immutable commit (all sources are public repo bytes fetched over
static raw.githubusercontent.com URLs; no api.github.com dependency).

fold16 = WIN8-D10 receipt fold (twenty-third receipt, sixth WIN8 receipt fold)
of the K1113 certificate root 00000000010000889002000080100000, chained on the
published fold15 record.  This fetcher is part of the fold16 external second
verification (declared in research/log/2026-11-21-n11-fold16-external-second-
verification-single-owner-note.md, commit
c6a55000f773e869ea60938b2efec1a7d6c9346c).

It rebuilds, from published repo bytes only:
  - the published fold16 experiment dir (3 files) into <pub_dir>,
  - the W tree of the fold16 machine (12 Git-blob pins + 25 SHA-256 pins),
    plus the published fold11, fold12, fold13, fold14 and fold15 machines
    needed by the fold16 machine's byte-identical rerun gates.

Every fetched byte is fail-closed checked against a SHA (blob sha1 for the
legacy pins, sha256 otherwise).  The script exits nonzero on any mismatch.
It also machine-confirms that the fold11/fold12/fold13/fold14/fold15 machines'
input pin tables are subsets of the fold16 machine's pins (equal keys and
values).
"""
import ast, hashlib, json, pathlib, re, sys, urllib.request

REPO = 'yuubinnkyoku/kyouen-researches'
HEAD = sys.argv[3] if len(sys.argv) > 3 else 'c6a55000f773e869ea60938b2efec1a7d6c9346c'
W_ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/f16ext/W16')
PUB = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else '/home/user/work/f16ext/pub16f')

W_ROOT.mkdir(parents=True, exist_ok=True)
PUB.mkdir(parents=True, exist_ok=True)

def get(url):
    return urllib.request.urlopen(url, timeout=180).read()

def blob_sha1(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()

# ---------------------------------------------------------------- published bytes
PUB_DIR = 'research/experiments/n11-residual55-win8-receipt-fold-root8890020-20261120/'
PUB_FILES = {
    'output/win8-root8890020-receipt-fold-20261120.json':
        'edd552588e265ada1cf015b4359584288cca3f18686c0fc8ca1536b6458b969b',
    'scripts/fold_win8_root8890020.py':
        'ecaef742bbb98874ce09f9af96666541cc0acb43706396f54f442c9e29b40200',
    'README.md':
        '7b68d5d5ac3bfc77e6d5470ebe9a8c2f92f4323576f6364938c3cf5818215416',
}
for rel, expected in PUB_FILES.items():
    data = get('https://raw.githubusercontent.com/' + REPO + '/' + HEAD + '/' + PUB_DIR + rel)
    if sha256_hex(data) != expected:
        raise SystemExit(f'published byte mismatch {rel}: {sha256_hex(data)} != {expected}')
    out = PUB / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print('pub', rel, len(data), expected)

machine_src = (PUB / 'scripts/fold_win8_root8890020.py').read_text()

def literal_dict(name, src):
    m = re.search(rf'{name} = (\{{.*?\n\}})', src, re.S)
    return ast.literal_eval(m.group(0).split('=', 1)[1])

PINS = literal_dict('PINS', machine_src)
PIN256 = literal_dict('PIN256', machine_src)
if len(PINS) != 12 or len(PIN256) != 25:
    raise SystemExit(f'unexpected pin counts {len(PINS)}/{len(PIN256)} (want 12/25)')

# ------------------------------------------------------- static repo path maps
RAWTREE = f'https://raw.githubusercontent.com/{REPO}/{HEAD}/research/experiments/'

# 12 legacy Git-blob pins -> exact repo path (static map, all byte-verified).
BLOB_PATHS = {
 'inputs/worklist.csv':
   'n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv',
 'inputs/ledger.json':
   'n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json',
 'inputs/globalFold.json':
   'n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-receipt-harvest-global-fold-20261118.json',
 'inputs/previousCostFold.json':
   'n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78c-79c-receipts-recompute-20261118.json',
 'inputs/firstFoldTarball.tar.gz':
   'n11-head1410-residual-cover-after-receipt-fold-20261119/output/first-win7-root-evidence-20261119.tar.gz',
 'inputs/census.json':
   'n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json',
 'inputs/audit.json':
   'n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-cover-cost16-five-parent-independent-audit-20261118.json',
 'ex48/output/secondThirdFold.json':
   'n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/second-third-win7-root-receipt-fold-20261119.json',
 'fold4rec/fold4.json':
   'n11-head1410-fourth-win7-receipt-fold-20261119/output/fourth-win7-root-receipt-fold-20261119.json',
 'fold56rec/fold56.json':
   'n11-head1410-fifth-sixth-win7-receipt-fold-20261119/output/fifth-sixth-win7-root-receipt-fold-20261119.json',
 'fold9/output/ninth-twelfth-win7-receipt-fold-20261119.json':
   'n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/ninth-twelfth-win7-receipt-fold-20261119.json',
 'fold_fourth_fifth_sixth.py':
   'n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/fold_fourth_fifth_sixth.py',
}

# 25 SHA-256 pins -> W-relative alias/subpath via the folder map.
FOLDERS = {
    'foldv2': 'n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2',
    'resolve6': 'n11-residual78-cache-join-resolve6-20261120',
    'fs13': 'n11-residual78-windfall4-receipt-fold-20261120',
    'sv17pub': 'n11-residual78-seventeenth-win7-cert-extract-20261120',
    'fold10': 'n11-seventeenth-win7-receipt-fold-20261120/fold',
    'k1096': 'n11-residual72-win8-cert-extract-root8003180-20261120',
    'k1097': 'n11-residual72-safe8-refuted50-refsolve-20261120',
    'fold11': 'n11-residual72-win8-receipt-fold-root8003180-20261120',
    'k1106': 'n11-residual72-win8-cert-extract-root8005021-20261120',
    'fold12': 'n11-residual68-win8-receipt-fold-root8005021-20261120',
    'k1108': 'n11-residual65-win8-cert-extract-root9840004-20261120',
    'fold13': 'n11-residual65-win8-receipt-fold-root9840004-20261120',
    'k1109': 'n11-residual65-win8-cert-extract-root9090022-20261120',
    'fold14': 'n11-residual62-win8-receipt-fold-root9090022-20261120',
    'k1114': 'n11-residual58-win8-cert-extract-root120000038-20261120',
    'fold15': 'n11-residual58-win8-receipt-fold-root120000038-20261120',
    'k1113': 'n11-residual58-win8-cert-extract-root8890020-20261120',
}

def write_checked(path, data, expected, kind):
    if kind == 'sha256':
        actual = sha256_hex(data)
    elif kind == 'blob':
        actual = blob_sha1(data)
    else:
        raise ValueError(kind)
    if actual != expected:
        raise SystemExit(f'{kind} mismatch {path}: {actual} != {expected}')
    out = pathlib.Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(kind, out.relative_to(W_ROOT), len(data), actual)

for rel, sha in PINS.items():
    if rel not in BLOB_PATHS:
        raise SystemExit(f'no static path mapping for pinned blob {rel} {sha}')
    write_checked(W_ROOT / rel, get(RAWTREE + BLOB_PATHS[rel]), sha, 'blob')

for rel, expected in PIN256.items():
    alias, sub = rel.split('/', 1)
    if alias not in FOLDERS:
        raise SystemExit('unmapped alias ' + alias)
    write_checked(W_ROOT / rel, get(RAWTREE + FOLDERS[alias] + '/' + sub), expected, 'sha256')

# ---------------------------------------------------------------- chain machines
# The fold16 machine re-runs the published fold11 machine from W
# ($W/fold_win8_root8003180.py, FOLD11_W=$W), and the published fold12/fold13/
# fold14/fold15 machines from isolated W copies ($W-rerun-root-f12/-f13/-f14/
# -f15, FOLD12_W/FOLD13_W/FOLD14_W/FOLD15_W).  All machine sources are fetched
# from their published repo paths; their own input pins are machine-confirmed
# to be subset chains of the fold16 machine's 37 pins (F11 <= F12 <= F13 <=
# F14 <= F15 <= F16, equal keys and values).
RAWSCRIPTS = f'https://raw.githubusercontent.com/{REPO}/{HEAD}/'

MACHINES = [
    ('fold11', 'fold_win8_root8003180.py',
     'research/experiments/n11-residual72-win8-receipt-fold-root8003180-20261120/scripts/',
     '9b3e06c8fcf5f37949a611dba57ce6546a7ced69a7e97b7588c66c588c55a5e1', 10),
    ('fold12', 'fold_win8_root8005021.py',
     'research/experiments/n11-residual68-win8-receipt-fold-root8005021-20261120/scripts/',
     '706bfa7ae8b8ff022e2f05c91eb0c61da6bf3343805dce7ed7e35289bf3a906c', 13),
    ('fold13', 'fold_win8_root9840004.py',
     'research/experiments/n11-residual65-win8-receipt-fold-root9840004-20261120/scripts/',
     '5c27f1ae1362c6f436e126786891bd4617ec92e403d22eff0b3b7537e51b0020', 16),
    ('fold14', 'fold_win8_root9090022.py',
     'research/experiments/n11-residual62-win8-receipt-fold-root9090022-20261120/scripts/',
     '7b88a56565f897a858b90e273199651cb1cf8bb237480b9d78a592edf17c9252', 19),
    ('fold15', 'fold_win8_root120000038.py',
     'research/experiments/n11-residual58-win8-receipt-fold-root120000038-20261120/scripts/',
     '03000c14f443bc4cf694e233d189fef159ef2b7a20420fa94c30879986ef771e', 22),
]

prev_pins = None
machine_info = []
for tag, fname, rdir, expect_sha, expect_n256 in MACHINES:
    src_bytes = get(RAWSCRIPTS + rdir + fname)
    got = sha256_hex(src_bytes)
    if got != expect_sha:
        raise SystemExit(f'{tag} machine sha mismatch {got}')
    write_checked(W_ROOT / fname, src_bytes, got, 'sha256')
    m_src = src_bytes.decode()
    m_PINS = literal_dict('PINS', m_src)
    m_PIN256 = literal_dict('PIN256', m_src)
    if len(m_PINS) != 12 or len(m_PIN256) != expect_n256:
        raise SystemExit(f'unexpected {tag} pin counts {len(m_PINS)}/{len(m_PIN256)} (want 12/{expect_n256})')
    for k, v in m_PINS.items():
        if PINS.get(k) != v:
            raise SystemExit(f'{tag} pin {k} not a subset of fold16 pins')
    for k, v in m_PIN256.items():
        if PIN256.get(k) != v:
            raise SystemExit(f'{tag} pin256 {k} not a subset of fold16 pins')
    if prev_pins is not None:
        for k, v in prev_pins.items():
            if m_PIN256.get(k) != v:
                raise SystemExit(f'previous chain pin256 {k} not a subset of {tag} pins')
    prev_pins = m_PIN256
    machine_info.append((tag, len(m_PIN256)))

print('subset-check fold11(10) <= fold12(13) <= fold13(16) <= fold14(19) <= fold15(22) <= fold16(12+25) OK:',
      machine_info)

# And the machine under test itself, at the W root for layout parity.
write_checked(W_ROOT / 'fold_win8_root8890020.py', machine_src.encode(),
              sha256_hex(machine_src.encode()), 'sha256')

manifest = {
    'head_ref': HEAD,
    'pub_dir': str(PUB),
    'w_root': str(W_ROOT),
    'pins_blob': len(PINS),
    'pins_sha256': len(PIN256),
    'fold11_machine_sha256': MACHINES[0][3],
    'fold12_machine_sha256': MACHINES[1][3],
    'fold13_machine_sha256': MACHINES[2][3],
    'fold14_machine_sha256': MACHINES[3][3],
    'fold15_machine_sha256': MACHINES[4][3],
    'machines': ['fold_win8_root8890020.py', 'fold_win8_root120000038.py', 'fold_win8_root9090022.py',
                 'fold_win8_root9840004.py', 'fold_win8_root8005021.py', 'fold_win8_root8003180.py'],
    'note': 'static raw.githubusercontent.com URLs only; every byte digest-checked',
}
(W_ROOT.parent / 'reconstruct16-manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print('RECONSTRUCTED W at', W_ROOT, 'PINS', len(PINS), 'PIN256', len(PIN256))
