#!/usr/bin/env python3
"""Reconstruct the fold14 external-second-verification input trees from GitHub
at an immutable commit (all sources are public repo bytes fetched over
static raw.githubusercontent.com URLs; no api.github.com dependency).

fold14 = WIN8-D10 receipt fold (twenty-first receipt, fourth WIN8 receipt fold)
of the K1109 certificate root 00000000000000909002200080100000, chained on the
published fold13 record.  This fetcher is part of the fold14 external second
verification (declared in research/log/2026-11-21-n11-fold14-external-second-
verification-single-owner-note.md, commit
2a6f14de952738a5b3177ef4a3468f0cf1cd33ab).

It rebuilds, from published repo bytes only:
  - the published fold13 experiment dir (3 files) into <pub_dir>,
  - the W tree of the fold14 machine (12 Git-blob pins + 19 SHA-256 pins),
    plus the published fold11, fold12 and fold13 machines needed by the
    fold14 machine's byte-identical fold11/fold12/fold13 rerun gates.

Every fetched byte is fail-closed checked against a SHA (blob sha1 for the
legacy pins, sha256 otherwise).  The script exits nonzero on any mismatch.
It also machine-confirms that the fold11 machine's input pins and the fold12
machine's input pins are subsets of the fold14 machine's pins (equal keys and
values).
"""
import ast, hashlib, json, pathlib, re, sys, urllib.request

REPO = 'yuubinnkyoku/kyouen-researches'
HEAD = sys.argv[3] if len(sys.argv) > 3 else '2a6f14de952738a5b3177ef4a3468f0cf1cd33ab'
W_ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/f13ext/W14')
PUB = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else '/home/user/work/f13ext/pub14f')

W_ROOT.mkdir(parents=True, exist_ok=True)
PUB.mkdir(parents=True, exist_ok=True)

def get(url):
    return urllib.request.urlopen(url, timeout=180).read()

def blob_sha1(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()

# ---------------------------------------------------------------- published bytes
PUB_DIR = 'research/experiments/n11-residual62-win8-receipt-fold-root9090022-20261120/'
PUB_FILES = {
    'output/win8-root9090022-receipt-fold-20261120.json':
        'ed3159fdb8cf2dd8884beb845cd4ef776cbc8b4b7b442d568d895cd930a13f71',
    'scripts/fold_win8_root9090022.py':
        '7b88a56565f897a858b90e273199651cb1cf8bb237480b9d78a592edf17c9252',
    'README.md':
        '25f9f08ba9cf8bfb3a1676617842a7d6ec4f780178e44ccaf44b236c8c9e2050',
}
for rel, expected in PUB_FILES.items():
    data = get('https://raw.githubusercontent.com/' + REPO + '/' + HEAD + '/' + PUB_DIR + rel)
    if sha256_hex(data) != expected:
        raise SystemExit(f'published byte mismatch {rel}: {sha256_hex(data)} != {expected}')
    out = PUB / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print('pub', rel, len(data), expected)

machine_src = (PUB / 'scripts/fold_win8_root9090022.py').read_text()

def literal_dict(name, src):
    m = re.search(rf'{name} = (\{{.*?\n\}})', src, re.S)
    return ast.literal_eval(m.group(0).split('=', 1)[1])

PINS = literal_dict('PINS', machine_src)
PIN256 = literal_dict('PIN256', machine_src)
if len(PINS) != 12 or len(PIN256) != 19:
    raise SystemExit(f'unexpected pin counts {len(PINS)}/{len(PIN256)} (want 12/19)')

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

# 16 SHA-256 pins -> W-relative alias/subpath via the folder map.
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
# The fold14 machine re-runs the published fold11 machine from W
# ($W/fold_win8_root8003180.py, FOLD11_W=$W), the published fold12 machine
# from an isolated W copy ($W-rerun-root-f12, FOLD12_W) and the published
# fold13 machine from an isolated W copy ($W-rerun-root-f13, FOLD13_W).
# All machine sources are fetched from their published repo paths; their own
# input pins are machine-confirmed to be subsets of the fold14 machine's 31
# pins.
RAWSCRIPTS = f'https://raw.githubusercontent.com/{REPO}/{HEAD}/'
f11_dir = 'research/experiments/n11-residual72-win8-receipt-fold-root8003180-20261120/scripts/'
f11_src_bytes = get(RAWSCRIPTS + f11_dir + 'fold_win8_root8003180.py')
f11_sha = sha256_hex(f11_src_bytes)
if f11_sha != '9b3e06c8fcf5f37949a611dba57ce6546a7ced69a7e97b7588c66c588c55a5e1':
    raise SystemExit(f'fold11 machine sha mismatch {f11_sha}')
write_checked(W_ROOT / 'fold_win8_root8003180.py', f11_src_bytes, f11_sha, 'sha256')
f11_src = f11_src_bytes.decode()

f12_dir = 'research/experiments/n11-residual68-win8-receipt-fold-root8005021-20261120/scripts/'
f12_src_bytes = get(RAWSCRIPTS + f12_dir + 'fold_win8_root8005021.py')
f12_sha = sha256_hex(f12_src_bytes)
if f12_sha != '706bfa7ae8b8ff022e2f05c91eb0c61da6bf3343805dce7ed7e35289bf3a906c':
    raise SystemExit(f'fold12 machine sha mismatch {f12_sha}')
write_checked(W_ROOT / 'fold_win8_root8005021.py', f12_src_bytes, f12_sha, 'sha256')
f12_src = f12_src_bytes.decode()

f11_PINS = literal_dict('PINS', f11_src)
f11_PIN256 = literal_dict('PIN256', f11_src)
f12_PINS = literal_dict('PINS', f12_src)
f12_PIN256 = literal_dict('PIN256', f12_src)
for k, v in f11_PINS.items():
    if PINS.get(k) != v:
        raise SystemExit(f'fold11 pin {k} not a subset of fold13 pins')
for k, v in f11_PIN256.items():
    if PIN256.get(k) != v:
        raise SystemExit(f'fold11 pin256 {k} not a subset of fold13 pins')
for k, v in f12_PINS.items():
    if PINS.get(k) != v:
        raise SystemExit(f'fold12 pin {k} not a subset of fold13 pins')
for k, v in f12_PIN256.items():
    if PIN256.get(k) != v:
        raise SystemExit(f'fold12 pin256 {k} not a subset of fold13 pins')
f13_dir = 'research/experiments/n11-residual65-win8-receipt-fold-root9840004-20261120/scripts/'
f13_src_bytes = get(RAWSCRIPTS + f13_dir + 'fold_win8_root9840004.py')
f13_sha = sha256_hex(f13_src_bytes)
if f13_sha != '5c27f1ae1362c6f436e126786891bd4617ec92e403d22eff0b3b7537e51b0020':
    raise SystemExit(f'fold13 machine sha mismatch {f13_sha}')
write_checked(W_ROOT / 'fold_win8_root9840004.py', f13_src_bytes, f13_sha, 'sha256')
f13_src = f13_src_bytes.decode()
f13_PINS = literal_dict('PINS', f13_src)
f13_PIN256 = literal_dict('PIN256', f13_src)
if len(f13_PINS) != 12 or len(f13_PIN256) != 16:
    raise SystemExit(f'unexpected fold13 pin counts {len(f13_PINS)}/{len(f13_PIN256)} (want 12/16)')
for k, v in f13_PINS.items():
    if PINS.get(k) != v:
        raise SystemExit(f'fold13 pin {k} not a subset of fold14 pins')
for k, v in f13_PIN256.items():
    if PIN256.get(k) != v:
        raise SystemExit(f'fold13 pin256 {k} not a subset of fold14 pins')

print('subset-check fold11 pins', len(f11_PINS), 'pin256', len(f11_PIN256),
      'fold12 pins', len(f12_PINS), 'pin256', len(f12_PIN256),
      'fold13 pins', len(f13_PINS), 'pin256', len(f13_PIN256),
      'subset of fold14 12+19 OK')

# And the machine under test itself, at the W root for layout parity.
write_checked(W_ROOT / 'fold_win8_root9090022.py', machine_src.encode(),
              sha256_hex(machine_src.encode()), 'sha256')

manifest = {
    'head_ref': HEAD,
    'pub_dir': str(PUB),
    'w_root': str(W_ROOT),
    'pins_blob': len(PINS),
    'pins_sha256': len(PIN256),
    'fold11_machine_sha256': f11_sha,
    'fold12_machine_sha256': f12_sha,
    'fold13_machine_sha256': f13_sha,
    'machines': ['fold_win8_root9090022.py', 'fold_win8_root9840004.py', 'fold_win8_root8005021.py', 'fold_win8_root8003180.py'],
    'note': 'static raw.githubusercontent.com URLs only; every byte digest-checked',
}
(W_ROOT.parent / 'reconstruct14-manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print('RECONSTRUCTED W at', W_ROOT, 'PINS', len(PINS), 'PIN256', len(PIN256))
