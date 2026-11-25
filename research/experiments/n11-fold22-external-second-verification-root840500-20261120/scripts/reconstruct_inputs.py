#!/usr/bin/env python3
"""Reconstruct the fold22 external-second-verification input trees from GitHub
at an immutable commit.

fold22 (K1132) = WIN8-D10 receipt fold of the K1125 certificate root
00000000000000801202000000840500, chained on the published fold21 record.
This fetcher is part of the fold22 external second verification (declared in
research/log/2026-11-20-n11-fold22-external-second-verification-single-owner-note.md,
commit 01c0855fd935b1951d686294efbb9305a3e4f4d8).

It rebuilds, from published repo bytes only:
  - the published fold22 experiment dir (4 files) into <pub_dir>,
  - the W tree of the fold22 machine (12 Git-blob pins + 43 SHA-256 pins),
    plus the published chain machines that the fold22 machine's pristine
    rerun gate (fold21 machine, which nests fold20 -> fold19 -> fold18,
    fold18 preverified copy) needs.

Every fetched byte is fail-closed checked against a SHA (blob sha1 for the
legacy pins, sha256 otherwise).  The script exits nonzero on any mismatch.
"""
import ast, hashlib, json, pathlib, re, sys, urllib.request

REPO = 'yuubinnkyoku/kyouen-researches'
HEAD = sys.argv[3] if len(sys.argv) > 3 else '34c29854c64286bbb1792ff28dc1973aef341e20'
W_ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/f22ext/W22')
PUB = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else '/home/user/work/f22ext/pub')
RAW = f'https://raw.githubusercontent.com/{REPO}/{HEAD}/'
API = f'https://api.github.com/repos/{REPO}/git/trees/'

W_ROOT.mkdir(parents=True, exist_ok=True)
PUB.mkdir(parents=True, exist_ok=True)

def get(url):
    return urllib.request.urlopen(url, timeout=180).read()

def blob_sha1(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()

# ---------------------------------------------------------------- published bytes
PUB_DIR = 'research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/'
PUB_FILES = {
    'output/win8-root840500-receipt-fold-20261120.json':
        'f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488',
    'scripts/fold_win8_root840500.py':
        'd5721408e7fb41e794175f3f3bb8b9d43fae13d18c244a831b81532aa9f1db1d',
    'scripts/build_fold22.py':
        'a73995be2ac448f2e56f804b3263330513c5bcb8a9e4042661c56e1deb4d7085',
    'README.md':
        '0e6861bf2970bead67ce77de9361e11a435cb27ee668e066a565a6fe808c29da',
}
for rel, expected in PUB_FILES.items():
    data = get(RAW + PUB_DIR + rel)
    if sha256_hex(data) != expected:
        raise SystemExit(f'published byte mismatch {rel}: {sha256_hex(data)} != {expected}')
    out = PUB / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print('pub', rel, len(data), expected)

machine_src = (PUB / 'scripts/fold_win8_root840500.py').read_text()

def literal_dict(name, src):
    m = re.search(rf'{name} = (\{{.*?\n\}})', src, re.S)
    return ast.literal_eval(m.group(0).split('=', 1)[1])

PINS = literal_dict('PINS', machine_src)
PIN256 = literal_dict('PIN256', machine_src)
if len(PINS) != 12 or len(PIN256) != 43:
    raise SystemExit(f'unexpected pin counts {len(PINS)}/{len(PIN256)} (want 12/43)')

# ---------------------------------------------------------------- tree walk
root_tree = json.loads(get(API + HEAD))['tree']
research = next(x for x in root_tree if x['path'] == 'research')
research_tree = json.loads(get(API + research['sha']))['tree']
experiments = next(x for x in research_tree if x['path'] == 'experiments')
exp_raw = json.loads(get(API + experiments['sha'] + '?recursive=1'))
if exp_raw.get('truncated'):
    raise SystemExit('experiments tree truncated; use per-dir tree walk fallback')
exp_tree = exp_raw['tree']
by_sha = {x['sha']: x['path'] for x in exp_tree if x['type'] == 'blob'}

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

# 12 legacy Git-blob pins -> exact tree path via blob sha1.
for rel, sha in PINS.items():
    p = by_sha.get(sha)
    if not p:
        raise SystemExit(f'no tree path for pinned blob {rel} {sha}')
    write_checked(W_ROOT / rel, get(RAW + 'research/experiments/' + p), sha, 'blob')

# 43 SHA-256 pins -> W-relative alias/subpath via the folder map.
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
    'fold16': 'n11-residual55-win8-receipt-fold-root8890020-20261120',
    'k1117': 'n11-residual55-win8-cert-extract-root22081000-20261120',
    'fold17': 'n11-residual51-win8-receipt-fold-root22081000-20261120',
    'k1120': 'n11-residual48-win8-cert-extract-root00901010-20261120',
    'fold18': 'n11-residual48-win8-receipt-fold-root00901010-20261120',
    'k1119': 'n11-residual51-win8-cert-extract-root1009000-20261120',
    'fold19': 'n11-residual41-win8-receipt-fold-root1009000-20261120',
    'k1121': 'n11-residual48-win8-cert-extract-root08d10000-20261120',
    'fold20': 'n11-residual38-win8-receipt-fold-root08d10000-20261120',
    'k1124': 'n11-residual45-win8-cert-extract-root80880200-20261120',
    'fold21': 'n11-residual35-win8-receipt-fold-root80880200-20261120',
    'k1125': 'n11-residual45-win8-cert-extract-root840500-20261120',
}
for rel, expected in PIN256.items():
    alias, sub = rel.split('/', 1)
    if alias not in FOLDERS:
        raise SystemExit('unmapped alias ' + alias)
    wanted = FOLDERS[alias] + '/' + sub
    paths = [x['path'] for x in exp_tree if x['type'] == 'blob' and x['path'] == wanted]
    if not paths:
        paths = [x['path'] for x in exp_tree if x['type'] == 'blob'
                 and x['path'].startswith(FOLDERS[alias] + '/')
                 and x['path'].split('/')[-1] == sub.split('/')[-1]]
    if len(paths) != 1:
        raise SystemExit(f'cannot uniquely resolve {rel}: {paths}')
    write_checked(W_ROOT / rel, get(RAW + 'research/experiments/' + paths[0]), expected, 'sha256')

# ---------------------------------------------------------------- chain machines
# Machine pins are read from the published sources themselves (no hand
# transcription): fold22 machine pins the fold21 machine; the fold21 machine
# pins the fold20 machine; the fold20 machine pins the fold19 machine; the
# fold19 machine pins the fold18 machine and its preverified copy.
MACHINE_DIR = {
    'fold21': 'research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/scripts/fold_win8_root80880200.py',
}
def machine_sha_pin(src, name):
    m = re.search(rf"{name} = '([0-9a-f]{{64}})'", src)
    if not m:
        raise SystemExit(f'no pin {name} in source')
    return m.group(1)

f21_pin = machine_sha_pin(machine_src, 'PIN_F21_MACHINE_SHA256')
f21_src = get(RAW + MACHINE_DIR['fold21']).decode()
write_checked(W_ROOT / 'fold_win8_root80880200.py',
              f21_src.encode(), f21_pin, 'sha256')

f20_pin = machine_sha_pin(f21_src, 'PIN_F20_MACHINE_SHA256')
f20_src = get(RAW + 'research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/scripts/fold_win8_root08d10000.py').decode()
write_checked(W_ROOT / 'fold_win8_root08d10000.py', f20_src.encode(), f20_pin, 'sha256')

f19_pin = machine_sha_pin(f20_src, 'PIN_F19_MACHINE_SHA256')
f19_src = get(RAW + 'research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/fold_win8_root1009000.py').decode()
write_checked(W_ROOT / 'fold_win8_root1009000.py', f19_src.encode(), f19_pin, 'sha256')

f18_pin = machine_sha_pin(f19_src, 'PIN_F18_MACHINE_SHA256')
f18_pre_pin = machine_sha_pin(f19_src, 'PATCHED_F18_SHA256')
f18_src = get(RAW + 'research/experiments/n11-residual48-win8-receipt-fold-root00901010-20261120/scripts/fold_win8_root00901010.py').decode()
write_checked(W_ROOT / 'fold_win8_root00901010.py', f18_src.encode(), f18_pin, 'sha256')
f18_pre = get(RAW + 'research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/fold_win8_root00901010_preverified.py')
write_checked(W_ROOT / 'fold_win8_root00901010_preverified.py', f18_pre, f18_pre_pin, 'sha256')

# fold22 printing convention uses its own receipt output path; record manifest.
manifest = {
    'head_ref': HEAD,
    'pub_dir': str(PUB),
    'w_root': str(W_ROOT),
    'pins_blob': len(PINS),
    'pins_sha256': len(PIN256),
    'machines': ['fold_win8_root80880200.py', 'fold_win8_root08d10000.py',
                 'fold_win8_root1009000.py', 'fold_win8_root00901010.py',
                 'fold_win8_root00901010_preverified.py'],
}
(W_ROOT.parent / 'reconstruct-manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print('RECONSTRUCTED W at', W_ROOT, 'PINS', len(PINS), 'PIN256', len(PIN256))
