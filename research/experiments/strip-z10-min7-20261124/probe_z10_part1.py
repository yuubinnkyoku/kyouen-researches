"""Pre-declaration exploration, PART 1 of 2, for the z=10 slice
(min>=7 band of the critical strip; K1278 candidate).

EXPLORATION ONLY -- no claims, no declared closed forms. This machine
extends the published K1277 D6c census registration (z10_cells,
audit.json sha256 9c0294e9dc413c422a88be17d64aa0325aad5236eca2bcb
3885e8988473b79ae) from bounded census families (330/126/70/35/15
shapes) to FULL decomposition families:

  P1   F10 = H(12;{1}+Y;10), tokens >=3, s in {0} u {3..40}  (3,657)
  P2   G10 = H(13;{2}+Y;10), same family                    (3,657)
  P2b  E10 = H(14;{3}+Y;10), same family                   (3,657)
  P3   D10 floored Y>=5, s in {0} u {5..40}                (1,650)
  P3b  D10 loose census (tokens 3..9)                        (330)
  P4   C10 floored Y>=6, s in {0} u {6..40}                (1,078)
  P4b  B10 floored Y>=7, s in {0} u {7..40}                  (700)
  P4c  A10 floored Y>=8, s in {0} u {8..40}              (machine count)

For every cell: s-only check on BOTH engines (ordered vs canonical),
full value table, deviants vs the collapse candidate
v(s+prefix, 10, R) with shape/direction record.

Engine provenance: sha-gated mechanical cut from the published K1264
verifier (108fdd65...), pin bd5f22e415a78368c9b798296bc84948d5637de
cbf3c21a92404d45fb12e3a92 (identical to the published K1272-K1277
engine chain). No hand transcription.

Writes part1_z10.json (tables for part 2: P5-P10 live there).
"""
import json, hashlib, os, sys
from functools import lru_cache
from itertools import combinations_with_replacement

sys.setrecursionlimit(1_000_000)

def cut_k1264(text):
    lines = text.split('\n'); s = None
    for i, ln in enumerate(lines):
        if ln == 'def mex(values):': s = i; break
    e = None
    for j in range(s, len(lines)):
        if lines[j].startswith('SELF_SHA = hashlib'): e = j; break
    block = lines[s:e]
    while block and block[-1].strip() == '': block.pop()
    return '\n'.join(block) + '\n'

BASE = os.path.dirname(os.path.abspath(__file__))
SRC1 = os.path.join(BASE, 'generalx-min-token-lowr-staircase-20261123',
                    'verify_min_token_staircase.py')
SRC1_PIN = '108fdd65a96588b32cfd64503cf2a22f999d6e4eefded775bb6fda32568e69fa'
ENGINE_PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'

data = open(SRC1, 'rb').read()
assert hashlib.sha256(data).hexdigest() == SRC1_PIN, 'K1264 verifier sha mismatch'
engine = cut_k1264(data.decode('utf-8'))
assert hashlib.sha256(engine.encode('utf-8')).hexdigest() == ENGINE_PIN, 'engine pin mismatch'
print('engine block sha256 OK:', ENGINE_PIN, flush=True)
exec(engine)

def clear_engines():
    H_ordered.cache_clear(); H_canonical.cache_clear()

def decomps(s, tmin, amax=4):
    if s == 0: return [()]
    out = []
    for k in range(1, amax + 1):
        for c in combinations_with_replacement(range(tmin, s + 1), k):
            if sum(c) == s: out.append(c)
    return out

def Y_tokens(tmin, tmax):
    out = []
    for k in range(0, 5):
        out.extend(combinations_with_replacement(range(tmin, tmax + 1), k))
    return out

res = {}

def sweep_cell(tag, pre, R, z, tmin, smax=40, dvoff=0):
    """full-decomposition sweep of H(R; pre+Y; z), Y tokens >= tmin,
    s in {0} u {tmin..smax}; both engines; deviants vs the collapse
    candidate v(s+dvoff, z, R) recorded with shape and direction."""
    pts = 0; engine_bad = 0
    tbl = {}
    devs = []
    srange = sorted(set([0] + list(range(tmin, smax + 1))))
    for s in srange:
        for Y in decomps(s, tmin):
            X = pre + Y
            hc = H_canonical(R, X, z)
            ho = H_ordered(R, X, z)
            pts += 1
            if hc != ho:
                engine_bad += 1
                devs.append({'kind': 'ENGINE', 's': s, 'Y': list(Y)})
            tbl.setdefault(s, set()).add(hc)
            col = single_token(s + dvoff, z, R)
            if dvoff and hc != col:
                devs.append({'kind': 'DEVIANT', 's': s, 'Y': list(Y),
                             'parent': hc, 'collapse': col,
                             'dir': 'UP' if hc > col else 'DOWN'})
    dep_s = [s for s, v in sorted(tbl.items()) if len(v) > 1]
    table = {str(s): sorted(v) for s, v in sorted(tbl.items())}
    res[tag] = {
        'R': R, 'z': z, 'floor': tmin, 'points': pts,
        'engine_bad': engine_bad,
        's_only': len(dep_s) == 0,
        'decomp_dependent_s': dep_s,
        'table': table,
        'deviant_count': sum(1 for d in devs if d['kind'] == 'DEVIANT'),
        'deviants': devs[:60],
    }
    clear_engines()
    print('%s pts=%d engine_bad=%d s_only=%s dep_s=%s devs=%d' % (
        tag, pts, engine_bad, res[tag]['s_only'], dep_s,
        res[tag]['deviant_count']), flush=True)
    # small table printout for s <= 14
    small = {s: sorted(v) for s, v in sorted(tbl.items()) if s <= 14}
    print('  table(s<=14):', json.dumps(small), flush=True)
    dev_sset = sorted(set(d['s'] for d in devs if d['kind'] == 'DEVIANT'))
    print('  deviant s-values:', dev_sset, flush=True)

print('== P1 F10 full family ==', flush=True)
sweep_cell('F10', (1,), 12, 10, 3, dvoff=1)
print('== P2 G10 full family ==', flush=True)
sweep_cell('G10', (2,), 13, 10, 3, dvoff=2)
print('== P2b E10 full family ==', flush=True)
sweep_cell('E10', (3,), 14, 10, 3, dvoff=3)
print('== P3 D10 floored Y>=5 ==', flush=True)
sweep_cell('D10', (4,), 15, 10, 5, dvoff=4)
print('== P4 C10 floored Y>=6 ==', flush=True)
sweep_cell('C10', (5,), 16, 10, 6, dvoff=5)
print('== P4b B10 floored Y>=7 ==', flush=True)
sweep_cell('B10', (6,), 17, 10, 7, dvoff=6)
print('== P4c A10 floored Y>=8 ==', flush=True)
sweep_cell('A10', (7,), 18, 10, 8, dvoff=7)

# D10 loose census (tokens 3..9, no floor) -- mirror of the published
# D10_loose census family (330 shapes)
print('== P3b D10 loose census (tokens 3..9) ==', flush=True)
fam = Y_tokens(3, 9)
tbl = {}; devs = []; engine_bad = 0
for Y in fam:
    s = sum(Y)
    hc = H_canonical(15, (4,) + Y, 10)
    ho = H_ordered(15, (4,) + Y, 10)
    if hc != ho:
        engine_bad += 1
        devs.append({'kind': 'ENGINE', 's': s, 'Y': list(Y)})
    tbl.setdefault(s, set()).add(hc)
    col = single_token(s + 4, 10, 15)
    if hc != col:
        devs.append({'kind': 'DEVIANT', 's': s, 'Y': list(Y),
                     'parent': hc, 'collapse': col,
                     'dir': 'UP' if hc > col else 'DOWN'})
dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
res['D10_loose'] = {
    'R': 15, 'z': 10, 'floor': 3, 'points': engine_bad and 0 or len(fam),
    'engine_bad': engine_bad, 's_only': len(dep) == 0,
    'decomp_dependent_s': dep,
    'table': {str(s): sorted(v) for s, v in sorted(tbl.items())},
    'deviant_count': sum(1 for d in devs if d['kind'] == 'DEVIANT'),
    'deviants': devs[:60],
}
clear_engines()
print('D10_loose family=%d engine_bad=%d dep_s=%s devs=%d' % (
    len(fam), engine_bad, dep, res['D10_loose']['deviant_count']), flush=True)
dev_sset = sorted(set(d['s'] for d in devs if d['kind'] == 'DEVIANT'))
print('  loose deviant s-values:', dev_sset, flush=True)

out_path = os.path.join(BASE, 'part1_z10.json')
with open(out_path, 'w') as f:
    f.write(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=True) + '\n')
print('WROTE', out_path)
print('PART 1 COMPLETE')
