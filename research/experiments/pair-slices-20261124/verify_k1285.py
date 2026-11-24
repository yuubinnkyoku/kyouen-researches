#!/usr/bin/env python3
"""verify_k1285: machine audit for the pair-slices / pure-c1 ladder package.

Theorems under audit (declarations and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses, it does NOT replace the proofs; all quantifiers in the
theorems are UNBOUNDED, censuses are consistency checks only):

  D1  T-PS0  z0 pair slices k=1,2,3: H(2m+g+k; (m, m+g); 0) = [g odd]
               for every m>=1, g>=1                               [1296 pts]
  D2  T-PS1  z1 pair slices k=2,3:   H(2m+g+k; (m, m+g); 1) = [g odd]   [864]
  D3  T-PS2  z2 pair slices k=3,4:   H(2m+g+k; (m, m+g); 2) = [g odd]   [864]
  D4  T-L1/L2/L3 pure-c1 ladders all d:
               H(2m+d+2; (m,m+d); 0) = H(2m+d+3; ...; 1) =
               H(2m+d+4; ...; 2) = [d odd]  (d=1 z1 row resolves the c=1
               half of the K1284 open registration C-PC1z1-d4)     [768]
  D5  T-ALM  allm-2 zeros: (m,m) at (2m+2,z0) (2m+3,z0) (2m+2,z1)
               (2m+3,z1) (2m+3,z2) (2m+4,z2) all = 0                [180]
  D6  floors  L-11z0a/b, L-1z1 singles, L-EMPTY grid,
               singles closed form v vs BOTH engines               [400]
  D7  C-PB2/C-PC pre-band single-layer corollaries (published band
               collapse instances): (x^c)@(x+2,z1)/(x+1,z0)
               = (c=1: [x odd], c>=2: [x even])                    [130]
  D8  wide    all 7 slice families m<=30, g<=20 (enlarged census)  [4200]
  D9  cross-engine canonical vs ordered slice agreement           [560]
  D10 OBS     finite observations (NO universal claims): border
               triangle z0-k0 / z1-k1 / z2-k2 exact pattern tables,
               z2-k1 clean-tail observation, z1-delta-3 allm ladder,
               multi-c web F(1,c)/G(1,c) blocker census            [532]

Engine block embedded verbatim from the published K1138/K1282/K1283/K1284
chain, sha256-gated at startup. TAMPER modes: --tamper-engine (rc 2),
--tamper=zz0|zz1|zz2|lad|alm|fl|pb (rc 1). Determinism: official runs are
byte-identical on stdout (volatile timestamps/elapsed on stderr only).
"""
import json, hashlib, sys, time
from functools import lru_cache

ENGINE_BLOCK = 'def mex(values):\n    values = set(values)\n    m = 0\n    while m in values:\n        m += 1\n    return m\n\n# ------------------------------------------------------------------\n# Raw engines (verbatim from the published K1138 verifier block; the same\n# transcription is embedded in the published y22 machine K1257).\n# ------------------------------------------------------------------\n@lru_cache(maxsize=6_000_000)\ndef H_ordered(R, X, z):\n    if R == 0:\n        return 0\n    opts = set()\n    for i, v in enumerate(X):\n        if v > 1:\n            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))\n        else:\n            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))\n    if z >= 1:\n        opts.add(1 ^ H_ordered(R - 1, X, z - 1))\n    return mex(opts)\n\n@lru_cache(maxsize=6_000_000)\ndef H_canonical(R, X, z):\n    X = tuple(sorted(X, reverse=True))\n    if R == 0:\n        return 0\n    opts = set()\n    i = 0\n    while i < len(X):\n        v = X[i]\n        if v > 1:\n            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))\n            opts.add(H_canonical(R - 1, child, z))\n        else:\n            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))\n            opts.add(H_canonical(R - 1, child, z + 1))\n        while i + 1 < len(X) and X[i + 1] == v:\n            i += 1\n        i += 1\n    if z >= 1:\n        opts.add(1 ^ H_canonical(R - 1, X, z - 1))\n    return mex(opts)\n\ndef vC(x, z, R):  # canonical-engine single token\n    return H_canonical(R, (x,), z)\ndef vO(x, z, R):  # ordered-engine single token\n    return H_ordered(R, (x,), z)\n\n# ------------------------------------------------------------------\n# Published K0832 single-token closed form (transcription of the published\n# single_token block in the y22 machine K1257; see report provenance).\n# ------------------------------------------------------------------\ndef q_odd(k):\n    return k if k % 2 else k - 1\n\ndef single_token(x, z, R):\n    if R == 0 or x <= 0:\n        return 0\n    if z == 0:\n        return min(R, x) % 2\n    if z == x:\n        if R % 2 and R <= 2 * x - 1:\n            return 2\n        if R % 2 == 0 and R <= x - 1:\n            return 0\n        return x % 2\n    if 1 <= z <= x - 1:\n        m = q_odd(z)\n        if R <= m:\n            return 2 if R % 2 else 0\n        if m < R < x + z:\n            return (R + z) % 2\n        return x % 2\n    if z >= x + 1:\n        m = q_odd(x)\n        if R <= m:\n            return 2 if R % 2 else 0\n        return x % 2\n    raise ValueError((x, z, R))\n'

ENGINE_SHA = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'

if '--tamper-engine' in sys.argv:
    tmp = ENGINE_BLOCK.replace('return k if k % 2 else k - 1',
                               'return k if k % 2 else k')
    sha2 = hashlib.sha256(tmp.encode('utf-8')).hexdigest()
    assert sha2 != PIN, 'tamper must change the sha'
    print('TAMPER-ENGINE: sha mismatch: %s != %s' % (sha2, PIN))
    sys.exit(2)
assert ENGINE_SHA == PIN, 'engine sha256 gate FAILED: %s' % ENGINE_SHA
exec(ENGINE_BLOCK)
v = single_token

TAMPER = None
for a in sys.argv[1:]:
    if a.startswith('--tamper='):
        TAMPER = a.split('=', 1)[1]

FAMS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (2, 4)]

def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()

def godd(g):
    return 1 if g % 2 == 1 else 0

def main():
    t0 = time.time()
    res = {'kit': 'verify_k1285', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS', 'tamper': TAMPER}
    ND = 10
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]
    hists = {}
    obs = {}

    zz0_flip = (TAMPER == 'zz0')
    zz1_flip = (TAMPER == 'zz1')
    zz2_flip = (TAMPER == 'zz2')
    lad_flip = (TAMPER == 'lad')
    alm_exp = 1 if TAMPER == 'alm' else 0
    fl_flip = (TAMPER == 'fl')
    pb_flip = (TAMPER == 'pb')

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6: ex[i].append(note)

    def pair(z, k, m, g):
        R = 2 * m + g + k
        return H_canonical(R, tuple(sorted([m, m + g], reverse=True)), z)

    # -------- D1: z0 pair slices k=1,2,3 -------------------------------
    for k in (1, 2, 3):
        for m in range(1, 25):
            for g in range(1, 19):
                h = pair(0, k, m, g)
                key = 'D1_z0_k%d' % k
                hists.setdefault(key, {})
                hists[key][str(h)] = hists[key].get(str(h), 0) + 1
                exp = 1 - godd(g) if zz0_flip else godd(g)
                cmpd(0, h == exp, [1, k, m, g, h, exp])
            clear()

    # -------- D2: z1 pair slices k=2,3 ---------------------------------
    for k in (2, 3):
        for m in range(1, 25):
            for g in range(1, 19):
                h = pair(1, k, m, g)
                key = 'D2_z1_k%d' % k
                hists.setdefault(key, {})
                hists[key][str(h)] = hists[key].get(str(h), 0) + 1
                exp = 1 - godd(g) if zz1_flip else godd(g)
                cmpd(1, h == exp, [2, k, m, g, h, exp])
            clear()

    # -------- D3: z2 pair slices k=3,4 ---------------------------------
    for k in (3, 4):
        for m in range(1, 25):
            for g in range(1, 19):
                h = pair(2, k, m, g)
                key = 'D3_z2_k%d' % k
                hists.setdefault(key, {})
                hists[key][str(h)] = hists[key].get(str(h), 0) + 1
                exp = 1 - godd(g) if zz2_flip else godd(g)
                cmpd(2, h == exp, [3, k, m, g, h, exp])
            clear()

    # -------- D4: pure-c1 ladders, all d, three planes ------------------
    ld_hist = {}
    for m in range(1, 17):
        for d in range(1, 17):
            for (off, z) in [(3, 1), (2, 0), (4, 2)]:
                h = H_canonical(2 * m + d + off, (m, m + d), z)
                ld_hist[str(h)] = ld_hist.get(str(h), 0) + 1
                exp = 1 - godd(d) if lad_flip else godd(d)
                cmpd(3, h == exp, [4, m, d, off, z, h, exp])
        clear()

    # -------- D5: allm-2 zeros -----------------------------------------
    for m in range(1, 31):
        for (off, z) in [(2, 0), (3, 0), (2, 1), (3, 1), (3, 2), (4, 2)]:
            h = H_canonical(2 * m + off, (m, m), z)
            cmpd(4, h == alm_exp, [5, m, off, z, h, alm_exp])
        clear()

    # -------- D6: floors + L-EMPTY + singles vs closed form -------------
    for (R, X, z, val) in [(3, (1, 1), 0, 0), (4, (1, 1), 0, 0),
                           (2, (1,), 1, 1), (3, (1,), 1, 1), (4, (1,), 1, 1)]:
        h = H_canonical(R, X, z)
        cmpd(5, h == (1 - val if fl_flip else val), [6, R, list(X), z, h, val])
    for R in range(0, 7):
        for z in range(0, 5):
            h = H_canonical(R, (), z)
            cmpd(5, h == 0, [6, 'EMPTY', R, z, h])
    for x in range(2, 17):
        for z in (1, 2, 3):
            for R in range(x + 1, x + 5):
                hc = H_canonical(R, (x,), z)
                ho = H_ordered(R, (x,), z)
                cmpd(5, hc == v(x, z, R), [6, 'sv-c', x, z, R, hc])
                cmpd(5, ho == v(x, z, R), [6, 'sv-o', x, z, R, ho])
            clear()

    # -------- D7: C-PB2 / C-PC pre-band single-layer corollaries --------
    for x in range(2, 15):
        for c in range(1, 6):
            exp = (x % 2) if c == 1 else (1 - x % 2)
            if pb_flip:
                exp = 1 - exp
            X = tuple([x] * c)
            h1 = H_canonical(x + 2, X, 1)
            cmpd(6, h1 == exp, [7, 'PB2', x, c, h1, exp])
            h0 = H_canonical(x + 1, X, 0)
            cmpd(6, h0 == exp, [7, 'PC', x, c, h0, exp])
            clear()

    # -------- D8: wide census, all 7 families ----------------------------
    for (z, k) in FAMS:
        for m in range(1, 31):
            for g in range(1, 21):
                h = pair(z, k, m, g)
                cmpd(7, h == godd(g), [8, z, k, m, g, h])
            clear()

    # -------- D9: cross-engine agreement (slices) ------------------------
    for (z, k) in FAMS:
        for m in range(1, 9):
            for g in range(1, 11):
                R = 2 * m + g + k
                X = tuple(sorted([m, m + g], reverse=True))
                hc = H_canonical(R, X, z)
                ho = H_ordered(R, X, z)
                cmpd(8, hc == ho, [9, z, k, m, g, hc, ho])
            clear()

    # -------- D10: finite observations (NO universal claims) -------------
    # border triangle pattern functions (observed, m-uniform):
    def P0(g):  # z0-k0: 2, 1, 0, then [g even]
        if g == 1: return 2
        if g == 2: return 1
        if g == 3: return 0
        return 0 if g % 2 == 1 else 1
    def P1(g):  # z1-k1: 1, 2, 0, then [g even]
        if g == 1: return 1
        if g == 2: return 2
        if g == 3: return 0
        return 0 if g % 2 == 1 else 1
    def P2(g):  # z2-k2: 1, 0, 2, then [g even]
        if g == 1: return 1
        if g == 2: return 0
        if g == 3: return 2
        return 0 if g % 2 == 1 else 1
    for (z, k, fn, tag) in [(0, 0, P0, 'z0k0'), (1, 1, P1, 'z1k1'),
                            (2, 1, godd, 'z2k1-clean-obs'), (2, 2, P2, 'z2k2')]:
        match = 0; mism = 0
        for m in range(1, 9):
            for g in range(1, 15):
                h = pair(z, k, m, g)
                if h == fn(g):
                    match += 1
                else:
                    mism += 1
                    if len(ex[9]) < 6: ex[9].append([10, tag, m, g, h, fn(g)])
            clear()
        obs[tag] = {'matches': match, 'mismatches': mism, 'm': '1..8',
                    'g': '1..14',
                    'claim': 'finite observation only (no universal claim)'}
        counts[9] += match + mism

    # z1-delta-3 allm ladder observation (m>=2): [0, 1, 2, 2, 2] for a=2..6
    match = 0; mism = 0
    for m in range(2, 9):
        for (a, val) in [(2, 0), (3, 1), (4, 2), (5, 2), (6, 2)]:
            h = H_canonical(2 * m + 3, tuple([m] * a), 1)
            if h == val: match += 1
            else:
                mism += 1
                if len(ex[9]) < 6: ex[9].append([10, 'aladder', m, a, h, val])
        clear()
    obs['aladder_z1d3'] = {'matches': match, 'mismatches': mism,
                           'm': '2..8', 'a': '2..6',
                           'claim': 'finite observation only'}
    counts[9] += match + mism
    # m=1 row: (1^a)@5 z1: [1, 0, 1, 0, 2, 2, 2] for a=1..7
    m1 = []
    for a in range(1, 8):
        m1.append(H_canonical(5, tuple([1] * a), 1))
    obs['aladder_m1'] = {'vals': m1,
                         'claim': 'finite observation only'}
    counts[9] += 7
    # multi-c web blockers: F(1,c) z1 -> 0 (c>=2), G(1,c) z0 -> 0/2
    matchF = 0; mismF = 0; matchG = 0; mismG = 0
    for m in range(2, 9):
        for c in range(2, 5):
            X = tuple(sorted([m] + [m + 1] * c, reverse=True))
            hF = H_canonical(2 * m + 4, X, 1)
            if hF == 0: matchF += 1
            else:
                mismF += 1
                if len(ex[9]) < 6: ex[9].append([10, 'F1c', m, c, hF, 0])
            hG = H_canonical(2 * m + 3, X, 0)
            expG = 0 if c == 2 else 2
            if hG == expG: matchG += 1
            else:
                mismG += 1
                if len(ex[9]) < 6: ex[9].append([10, 'G1c', m, c, hG, expG])
        clear()
    obs['F1c_z1d4'] = {'matches': matchF, 'mismatches': mismF,
                       'm': '2..8', 'c': '2..4',
                       'claim': 'finite observation only (open C-PC1z1-d4 c>=2 half)'}
    obs['G1c_z0d3'] = {'matches': matchG, 'mismatches': mismG,
                       'm': '2..8', 'c': '2..4',
                       'claim': 'finite observation only (pure-count ladder open)'}
    counts[9] += matchF + mismF + matchG + mismG

    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['hists'] = hists
    res['ladder_hist'] = ld_hist
    res['obs'] = obs
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)

main()
