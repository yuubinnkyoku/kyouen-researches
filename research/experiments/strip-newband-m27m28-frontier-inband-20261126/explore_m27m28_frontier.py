"""
explore_m27m28_frontier: FROZEN PRE-DECLARATION census for the LADDER
CONTINUATION of the m=19..m=24 residual bands (the registered kit-5 S5
items m=19@z=52 / z=53, m=20@z=53 / z=54, m=21@z=48 / z=49, m=22@z=49 /
z=50, m=23@z=50 / z=51, m=24@z=51 / z=52), the FRONTIER rows m=27 and
m=28 (the registered 15th / 16th parity datum candidates, the FIRST-EVER
m=27 / m=28 rows), the m=25 / m=26 MINI-LADDER rows (the registered kit-5
S5 items (13)-(18), including the FIRST m=25 / m=26 death datum
candidates), and the REGISTERED in-band window sweeps m=25 z in {41..48}
and m=26 z in {43..50}, plus 112 published anchor rechecks (the 93
kit-5-era anchors verbatim + the 19 kit-5 separation spots, first
re-anchored here and machine-verified 19/19 against the published
values BEFORE this file's first run).
NO K slot is claimed by this file; the 36 registered measurement
candidates in this docstring were frozen BEFORE the first run of this
file. The only edit performed after any run must be disclosed here in
dated form (verifier-table or docstring fixes only; no candidate,
engine, or measurement code was edited at any time).

Registered provenance (all BEFORE any measurement by this kit):
- The thirty-six measurement rows are the REGISTERED binding candidates
  of the published kit-5 log S5 items (1)-(22) and of its frozen output
  section future_slice_registration_constants (commit d52f2be7,
  research/experiments/strip-newband-m25m26-frontier-inband-20261126/),
  verbatim; the 15th / 16th frontier datum arithmetic was re-derived
  and double-asserted at this build (z*(27)=2*27-2+1=53,
  z*(28)=2*28-2+0=54 per K1268; derive_check engine-free).
- DISCLOSED AT THIS BUILD (window label/list discrepancy, resolved by
  the kit-4 label/list precedent): the kit-5 frozen section item (20)
  for the m=26 window carries prediction text "z*(26)-8..-1" (=42..49)
  but lists rows z in {43..50}. The LISTED rows bind: z in {43..49} are
  measured here as plain window rows (candidates 0 separations); the
  listed z=50 row is the ALREADY-PUBLISHED kit-5 frontier 14th datum
  row, measured here as an EXPLICIT BLIND RE-VERIFICATION carrying the
  published registered candidate verbatim (EXACTLY ONE (26,26)@S=52
  UP 2v1, collapse v(52,50,77)=1) — NOT a 0-separations window
  candidate. The z=42 row of the label reading is NOT registered and
  NOT measured here.
- ANCHOR-TABLE LESSON APPLIED (kit-5 disclosure, not repeated here):
  every anchor entry in this file is R-FIRST (R=m+z+1); the 19 new
  kit-5-sourced spots were extracted by machine from the published
  kit-5 frozen output (R, X, z, value straight from the row records),
  and were machine-verified to reproduce all 19 published values
  EXACTLY (19/19) with the canonical engine BEFORE this file's first
  run. The 93 inherited entries reproduce the kit-5 published anchor
  table byte-for-byte.
- m=27 / m=28 below-frontier coverage disclosure: unlike m=25 / m=26
  the m=27 / m=28 rows are NOT strip-covered at z in {25,26}
  (z26-floor20 covers m in {20..26} only), so z in {25..52} of m=27
  and z in {25..53} of m=28 are all unmeasured; no claim of any kind
  is made about them, and the kit-7 window-sweep proposals below are
  the only registrations.
- Counter-probe at this build (~09:37Z, head d52f2be7 = this kit's own
  predecessor kit-5, unchanged): all 8 kit-specific content queries
  (frontier_m27, m27_z53, m28_z54, ladder_m19_z52, ladder_m25_z50,
  inband_m25_z41, inband_m26_z43, m27m28) returned 0 measurement
  records. Re-run at push time against then-current main and disclosed.
- Determinism claim: single JSON line stdout, no dict-ordering or
  hash-seed dependence (six-run byte-identical battery on the kit-5
  explorer; same code structure here).
"""


import hashlib, json, sys
from functools import lru_cache

ENGINE_BLOCK = '''def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier block; the same
# transcription is embedded in the published y22 machine K1257).
# ------------------------------------------------------------------
@lru_cache(maxsize=6_000_000)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(maxsize=6_000_000)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def vC(x, z, R):  # canonical-engine single token
    return H_canonical(R, (x,), z)
def vO(x, z, R):  # ordered-engine single token
    return H_ordered(R, (x,), z)

# ------------------------------------------------------------------
# Published K0832 single-token closed form (transcription of the published
# single_token block in the y22 machine K1257; see report provenance).
# ------------------------------------------------------------------
def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))
'''

PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
sha = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
assert sha == PIN, sha
ns = {'lru_cache': lru_cache}
exec(ENGINE_BLOCK, ns)
H = ns['H_canonical']
v = ns['single_token']


def parts(s, lo, arity):
    """all multisets (nondecreasing tuples) of tokens >= lo, sum s, 1..arity tokens"""
    out = []

    def rec(rem, k, cur):
        if rem == 0:
            if 1 <= len(cur) <= arity:
                out.append(tuple(cur))
            return
        if k == arity:
            return
        for t in range(lo, rem + 1):
            if cur and t < cur[-1]:
                continue
            cur.append(t)
            rec(rem - t, k + 1, cur)
            cur.pop()

    rec(s, 0, [])
    return out


def row_record(sec, rlabel, extra, R, z, m, smin, smax, min_tok):
    """co-token style sweep: X = (m,) U parts >= min_tok (arity up to 4 total)."""
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(max(S - m, 0), min_tok, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(R, XX, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(XX), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return {'section': sec, 'label': rlabel, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}


def row_record_x0(sec, rlabel, extra, R, z, m, smin, smax):
    """published residual-band record style: X = parts(S, m, 3) with
    X[0] == m, i.e. all parts >= m with co-token m allowed, arity <= 3
    TOTAL. Shape-for-shape comparable with the published entries."""
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return {'section': sec, 'label': rlabel, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}



def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    vC = ns['vC']
    vO = ns['vO']

    anchor_spec = [
        (46, (17, 18), 28, 0, 'lifecycle kit z=28 handoff h1'),
        (45, (16, 17), 28, 1, 'lifecycle kit z=28 handoff h2'),
        (47, (18, 18), 28, 1, 'lifecycle kit z=28 handoff h3'),
        (46, (17, 17), 28, 0, 'lifecycle kit z=28 handoff h4'),
        (47, (17, 18), 29, 0, 'decay kit z=29 touch u1'),
        (46, (16, 17), 29, 1, 'decay kit z=29 touch u2'),
        (48, (18, 18), 29, 1, 'decay kit z=29 touch u3'),
        (47, (17, 17), 29, 0, 'decay kit z=29 touch u4'),
        (48, (17, 18), 30, 0, 'wavetrain kit z=30 touch w1'),
        (47, (16, 17), 30, 1, 'wavetrain kit z=30 touch w2'),
        (49, (18, 18), 30, 1, 'wavetrain kit z=30 touch w3'),
        (48, (17, 17), 30, 0, 'wavetrain kit z=30 touch w4'),
        (49, (17, 18), 31, 0, 'fifthwave kit z=31 touch x1'),
        (48, (16, 17), 31, 1, 'fifthwave kit z=31 touch y1'),
        (50, (18, 18), 31, 1, 'fifthwave kit z=31 touch x3'),
        (49, (17, 17), 31, 0, 'fifthwave kit z=31 touch x4'),
        (50, (17, 18), 32, 0, 'sixthwave kit z=32 touch x1'),
        (49, (16, 17), 32, 1, 'sixthwave kit z=32 touch y1'),
        (51, (18, 18), 32, 1, 'sixthwave kit z=32 touch x3'),
        (50, (17, 17), 32, 0, 'sixthwave kit z=32 touch x4'),
        (45, (15, 16), 29, 2, 'frontier m=15@z=29 separation (lifecycle kit + d49b480a blind replication)'),
        (47, (16, 16), 30, 2, 'frontier m=16@z=30 separation (lifecycle kit + d49b480a)'),
        (46, (15, 16), 30, 1, 'one-past m=15@z=30 separation (lifecycle kit + d49b480a)'),
        (48, (16, 16), 31, 0, 'one-past m=16@z=31 separation (lifecycle kit + d49b480a)'),
        (41, (13, 14), 27, 1, 'two-past m=13@z=27 stick separation (d49b480a)'),
        (41, (13, 16), 27, 2, 'two-past m=13@z=27 d=1 birth separation (d49b480a)'),
        (53, (17, 18), 35, 1, 'two-past m=17@z=35 stick separation (fifthwave kit)'),
        (53, (17, 20), 35, 2, 'two-past m=17@z=35 d=1 birth separation (fifthwave kit)'),
        (47, (13, 20), 33, 1, 'm=13@z=33 stick separation (fifthwave kit)'),
        (47, (13, 22), 33, 2, 'm=13@z=33 d=4 birth separation (fifthwave kit)'),
        (57, (19, 20), 37, 2, 'kit-1 (6057ed51) frontier m=19@z=37 d=0 birth separation UP 2v0'),
        (58, (19, 20), 38, 1, 'kit-1 (6057ed51) one-past m=19@z=38 separation UP 1v0 (odd decay 2->1)'),
        (59, (19, 20), 39, 1, 'kit-1 (6057ed51) two-past m=19@z=39 stick separation DOWN 1v2'),
        (59, (19, 22), 39, 2, 'kit-1 (6057ed51) two-past m=19@z=39 d=1 birth separation UP 2v0'),
        (59, (20, 20), 38, 2, 'kit-1 (6057ed51) frontier m=20@z=38 d=0 birth separation UP 2v1'),
        (60, (20, 20), 39, 0, 'kit-1 (6057ed51) one-past m=20@z=39 separation DOWN 0v1 (even decay 2->0)'),
        (61, (20, 20), 40, 0, 'kit-1 (6057ed51) two-past m=20@z=40 stick separation DOWN 0v2'),
        (61, (20, 22), 40, 2, 'kit-1 (6057ed51) two-past m=20@z=40 d=1 birth separation UP 2v1'),
        (45, (19, 19), 25, 0, 'z25-min20 kit base spot H(45;(19,19);25)=0 published CONFORM'),
        (46, (19, 19), 26, 0, 'z26-floor20 kit base spot H(46;(19,19);26)=0 published CONFORM'),
        (60, (19, 22), 40, 1, 'kit-2 (637d15e1) ladder m=19@z=40 one-past-of-d=1 separation UP 1v0'),
        (61, (19, 22), 41, 1, 'kit-2 (637d15e1) ladder m=19@z=41 stick separation DOWN 1v2'),
        (61, (19, 24), 41, 2, 'kit-2 (637d15e1) ladder m=19@z=41 d=2 birth separation UP 2v0'),
        (62, (19, 24), 42, 1, 'kit-2 (637d15e1) ladder m=19@z=42 one-past-of-d=2 separation UP 1v0'),
        (63, (19, 24), 43, 1, 'kit-2 (637d15e1) ladder m=19@z=43 stick separation DOWN 1v2'),
        (63, (19, 26), 43, 2, 'kit-2 (637d15e1) ladder m=19@z=43 d=3 birth separation UP 2v0'),
        (62, (20, 22), 41, 0, 'kit-2 (637d15e1) ladder m=20@z=41 one-past-of-d=1 separation DOWN 0v1'),
        (63, (20, 22), 42, 0, 'kit-2 (637d15e1) ladder m=20@z=42 stick separation DOWN 0v2'),
        (63, (20, 24), 42, 2, 'kit-2 (637d15e1) ladder m=20@z=42 d=2 birth separation UP 2v1'),
        (64, (20, 24), 43, 0, 'kit-2 (637d15e1) ladder m=20@z=43 one-past-of-d=2 separation DOWN 0v1'),
        (65, (20, 24), 44, 0, 'kit-2 (637d15e1) ladder m=20@z=44 stick separation DOWN 0v2'),
        (65, (20, 26), 44, 2, 'kit-2 (637d15e1) ladder m=20@z=44 d=3 birth separation UP 2v1'),
        (64, (19, 26), 44, 1, 'kit-3 (6554de44) ladder m=19@z=44 one-past-of-d=3 separation UP 1v0'),
        (65, (19, 26), 45, 1, 'kit-3 (6554de44) ladder m=19@z=45 stick separation DOWN 1v2'),
        (65, (19, 28), 45, 2, 'kit-3 (6554de44) ladder m=19@z=45 d=4 birth separation UP 2v0 seat gap 9'),
        (66, (19, 28), 46, 1, 'kit-3 (6554de44) ladder m=19@z=46 one-past-of-d=4 separation UP 1v0'),
        (67, (19, 28), 47, 1, 'kit-3 (6554de44) ladder m=19@z=47 stick separation DOWN 1v2'),
        (67, (19, 30), 47, 2, 'kit-3 (6554de44) ladder m=19@z=47 d=5 birth separation UP 2v0 seat gap 11'),
        (66, (20, 26), 45, 0, 'kit-3 (6554de44) ladder m=20@z=45 one-past-of-d=3 separation DOWN 0v1'),
        (67, (20, 26), 46, 0, 'kit-3 (6554de44) ladder m=20@z=46 stick separation DOWN 0v2'),
        (67, (20, 28), 46, 2, 'kit-3 (6554de44) ladder m=20@z=46 d=4 birth separation UP 2v1 seat gap 8'),
        (68, (20, 28), 47, 0, 'kit-3 (6554de44) ladder m=20@z=47 one-past-of-d=4 separation DOWN 0v1'),
        (69, (20, 28), 48, 0, 'kit-3 (6554de44) ladder m=20@z=48 stick separation DOWN 0v2'),
        (69, (20, 30), 48, 2, 'kit-3 (6554de44) ladder m=20@z=48 d=5 birth separation UP 2v1 seat gap 10'),
        (63, (21, 22), 41, 2, 'kit-3 (6554de44) frontier m=21@z=41 d=0 birth separation UP 2v0'),
        (64, (21, 22), 42, 1, 'kit-3 (6554de44) one-past m=21@z=42 separation UP 1v0 (odd decay 2->1)'),
        (65, (21, 22), 43, 1, 'kit-3 (6554de44) two-past m=21@z=43 stick separation DOWN 1v2'),
        (65, (21, 24), 43, 2, 'kit-3 (6554de44) two-past m=21@z=43 d=1 birth separation UP 2v0 seat gap 3'),
        (65, (22, 22), 42, 2, 'kit-3 (6554de44) frontier m=22@z=42 d=0 birth separation UP 2v1'),
        (66, (22, 22), 43, 0, 'kit-3 (6554de44) one-past m=22@z=43 separation DOWN 0v1 (even decay 2->0)'),
        (67, (22, 22), 44, 0, 'kit-3 (6554de44) two-past m=22@z=44 stick separation DOWN 0v2'),
        (67, (22, 24), 44, 2, 'kit-3 (6554de44) two-past m=22@z=44 d=1 birth separation UP 2v1 seat gap 2'),
        (68, (19, 30), 48, 1, 'kit-4 (fe0a2d01) ladder m=19@z=48 one-past-of-d=5 separation UP 1v0'),
        (69, (19, 30), 49, 1, 'kit-4 (fe0a2d01) stick m=19@z=49 separation DOWN 1v2'),
        (69, (19, 32), 49, 2, 'kit-4 (fe0a2d01) birth m=19@z=49 d=6 separation UP 2v0 seat gap 13'),
        (70, (20, 30), 49, 0, 'kit-4 (fe0a2d01) one-past m=20@z=49 separation DOWN 0v1'),
        (71, (20, 30), 50, 0, 'kit-4 (fe0a2d01) stick m=20@z=50 separation DOWN 0v2'),
        (71, (20, 32), 50, 2, 'kit-4 (fe0a2d01) birth m=20@z=50 d=6 separation UP 2v1 seat gap 12'),
        (66, (21, 24), 44, 1, 'kit-4 (fe0a2d01) one-past m=21@z=44 separation UP 1v0 (first m=21 death row: {21,22} conform-DEAD)'),
        (67, (21, 24), 45, 1, 'kit-4 (fe0a2d01) stick m=21@z=45 separation DOWN 1v2'),
        (67, (21, 26), 45, 2, 'kit-4 (fe0a2d01) birth m=21@z=45 d=2 separation UP 2v0 seat gap 5'),
        (68, (22, 24), 45, 0, 'kit-4 (fe0a2d01) one-past m=22@z=45 separation DOWN 0v1 (first m=22 death row: (22,22) conform-DEAD at z=45=S+1)'),
        (69, (22, 24), 46, 0, 'kit-4 (fe0a2d01) stick m=22@z=46 separation DOWN 0v2'),
        (69, (22, 26), 46, 2, 'kit-4 (fe0a2d01) birth m=22@z=46 d=2 separation UP 2v1 seat gap 4'),
        (69, (23, 24), 45, 2, 'kit-4 (fe0a2d01) frontier m=23@z=45 separation UP 2v0 (the 11th datum, corrected registration)'),
        (70, (23, 24), 46, 1, 'kit-4 (fe0a2d01) one-past m=23@z=46 separation UP 1v0'),
        (71, (23, 24), 47, 1, 'kit-4 (fe0a2d01) stick m=23@z=47 separation DOWN 1v2'),
        (71, (23, 26), 47, 2, 'kit-4 (fe0a2d01) birth m=23@z=47 d=1 separation UP 2v0 seat gap 3'),
        (71, (24, 24), 46, 2, 'kit-4 (fe0a2d01) frontier m=24@z=46 separation UP 2v1 (the 12th datum)'),
        (72, (24, 24), 47, 0, 'kit-4 (fe0a2d01) one-past m=24@z=47 separation DOWN 0v1'),
        (73, (24, 24), 48, 0, 'kit-4 (fe0a2d01) stick m=24@z=48 separation DOWN 0v2'),
        (73, (24, 26), 48, 2, 'kit-4 (fe0a2d01) birth m=24@z=48 d=1 separation UP 2v1 seat gap 2'),
        (74, (24, 26), 49, 0, 'kit-4 (fe0a2d01) one-past-of-d=1 m=24@z=49 separation DOWN 0v1 (first m=24 death row: (24,24) conform-DEAD at z=49=S+1)'),
        (70, (19, 32), 50, 1, 'kit-5 (d52f2be7) ladder m=19@z=50 one-past-of-d=6 separation UP 1v0 (first m=19 d=5 death row: {19,30} conform-DEAD)'),
        (71, (19, 32), 51, 1, 'kit-5 (d52f2be7) stick m=19@z=51 separation DOWN 1v2'),
        (71, (19, 34), 51, 2, 'kit-5 (d52f2be7) birth m=19@z=51 d=7 separation UP 2v0 seat gap 15 (m=19 ladder COMPLETE d=7)'),
        (72, (20, 32), 51, 0, 'kit-5 (d52f2be7) ladder m=20@z=51 one-past-of-d=6 separation DOWN 0v1 ((20,30) conform-DEAD, first m=20 d=5 death row)'),
        (73, (20, 32), 52, 0, 'kit-5 (d52f2be7) stick m=20@z=52 separation DOWN 0v2'),
        (73, (20, 34), 52, 2, 'kit-5 (d52f2be7) birth m=20@z=52 d=7 separation UP 2v1 seat gap 14 (m=20 ladder COMPLETE d=7)'),
        (68, (21, 26), 46, 1, 'kit-5 (d52f2be7) ladder m=21@z=46 one-past-of-d=2 separation UP 1v0 ({21,24} conform-DEAD, first m=21 d=1 death row)'),
        (69, (21, 26), 47, 1, 'kit-5 (d52f2be7) stick m=21@z=47 separation DOWN 1v2'),
        (69, (21, 28), 47, 2, 'kit-5 (d52f2be7) birth m=21@z=47 d=3 separation UP 2v0 seat gap 7'),
        (70, (22, 26), 47, 0, 'kit-5 (d52f2be7) ladder m=22@z=47 one-past-of-d=2 separation DOWN 0v1 ((22,24) conform-DEAD, first m=22 d=1 death row)'),
        (71, (22, 26), 48, 0, 'kit-5 (d52f2be7) stick m=22@z=48 separation DOWN 0v2'),
        (71, (22, 28), 48, 2, 'kit-5 (d52f2be7) birth m=22@z=48 d=3 separation UP 2v1 seat gap 6'),
        (72, (23, 26), 48, 1, 'kit-5 (d52f2be7) ladder m=23@z=48 one-past-of-d=1 separation UP 1v0 (THE FIRST m=23 death datum: {23,24} conform-DEAD)'),
        (73, (23, 26), 49, 1, 'kit-5 (d52f2be7) stick m=23@z=49 separation DOWN 1v2'),
        (73, (23, 28), 49, 2, 'kit-5 (d52f2be7) birth m=23@z=49 d=2 separation UP 2v0 seat gap 5'),
        (75, (24, 26), 50, 0, 'kit-5 (d52f2be7) stick m=24@z=50 separation DOWN 0v2 (stick seat coincides S(d1)=50=z)'),
        (75, (24, 28), 50, 2, 'kit-5 (d52f2be7) birth m=24@z=50 d=2 separation UP 2v1 seat gap 4'),
        (75, (25, 26), 49, 2, 'kit-5 (d52f2be7) frontier m=25@z=49 separation UP 2v0 (the 13th datum, first-ever m=25 row)'),
        (77, (26, 26), 50, 2, 'kit-5 (d52f2be7) frontier m=26@z=50 separation UP 2v1 (the 14th datum, first-ever m=26 row)'),
    ]
    # (a) K0832 battery: every single-token literal used by this file.
    battery_lits = []
    rows_stair = []
    meas_rows = [(19, 50), (19, 51), (20, 51), (20, 52),
                 (21, 46), (21, 47), (22, 47), (22, 48),
                 (23, 48), (23, 49), (24, 50), (25, 49), (26, 50)] + \
                [(23, z) for z in range(36, 44)] + \
                [(24, z) for z in range(38, 46)]
    for (m, z) in meas_rows:
        R = m + z + 1
        for S in (m, m + 2, 2 * m, 2 * m + 1, m + 37, m + 38):
            battery_lits.append((S, z, R))
        rows_stair.append((m, z, R))
    # registered kit-4 S5 items (1)-(11) candidate constants
    # (m=22 rows with the CORRECTED R annotations, disclosed in the
    # docstring: values identical to the slipped kit-4 triples)
    for (x, z2, R2) in [
            (51, 50, 70), (49, 50, 70), (51, 51, 71), (53, 51, 71),
            (52, 51, 72), (50, 51, 72), (52, 52, 73), (54, 52, 73),
            (47, 46, 68), (45, 46, 68), (47, 47, 69), (49, 47, 69),
            (48, 47, 70), (46, 47, 70), (48, 48, 71), (50, 48, 71),
            (49, 48, 72), (47, 48, 72), (49, 49, 73), (51, 49, 73),
            (50, 50, 75), (52, 50, 75)]:
        battery_lits.append((x, z2, R2))
    # the SLIPPED kit-4 (f) m=22 annotation triples (kept on record;
    # closed form is parity-constant between the two R windows, so
    # the values coincide — disclosed in the docstring)
    for (x, z2, R2) in [
            (48, 47, 68), (46, 47, 68), (48, 48, 69), (50, 48, 69)]:
        battery_lits.append((x, z2, R2))
    # frontier 13th/14th datum candidates
    for (x, z2, R2) in [(51, 49, 75), (52, 50, 77)]:
        battery_lits.append((x, z2, R2))
    # measured-row constants of THIS kit (the kit-5 frozen section (d)
    # registration list, verbatim; battery-checked again here)
    for (x, z2, R2) in [
            (53, 52, 72), (51, 52, 72), (53, 53, 73), (55, 53, 73),
            (54, 53, 74), (52, 53, 74), (54, 54, 75), (56, 54, 75),
            (49, 48, 70), (47, 48, 70), (49, 49, 71), (51, 49, 71),
            (50, 49, 72), (48, 49, 72), (50, 50, 73), (52, 50, 73),
            (51, 50, 74), (49, 50, 74), (51, 51, 75), (53, 51, 75),
            (52, 51, 76), (50, 51, 76), (52, 52, 77), (54, 52, 77),
            (51, 50, 76), (51, 51, 77), (53, 51, 77), (53, 52, 78),
            (51, 52, 78), (52, 51, 78), (52, 52, 79), (54, 52, 79),
            (54, 53, 80), (52, 53, 80), (55, 53, 81), (56, 54, 83)]:
        battery_lits.append((x, z2, R2))

    # future-slice registration constants of THIS kit (section (d),
    # NOT measured here; kit-7 candidates)
    for (x, z2, R2) in [
            (55, 54, 74),
            (53, 54, 74),
            (55, 55, 75),
            (57, 55, 75),
            (56, 55, 76),
            (54, 55, 76),
            (56, 56, 77),
            (58, 56, 77),
            (51, 50, 74),
            (49, 50, 74),
            (51, 51, 75),
            (53, 51, 75),
            (52, 51, 76),
            (50, 51, 76),
            (52, 52, 77),
            (54, 52, 77),
            (53, 52, 76),
            (51, 52, 76),
            (53, 53, 77),
            (55, 53, 77),
            (54, 53, 78),
            (52, 53, 78),
            (54, 54, 79),
            (56, 54, 79),
            (53, 53, 79),
            (55, 53, 79),
            (55, 54, 80),
            (53, 54, 80),
            (55, 55, 81),
            (57, 55, 81),
            (54, 54, 81),
            (56, 54, 81),
            (56, 55, 82),
            (54, 55, 82),
            (56, 56, 83),
            (58, 56, 83),
            (55, 54, 82),
            (55, 55, 83),
            (57, 55, 83),
            (57, 56, 84),
            (55, 56, 84),
            (56, 55, 84),
            (56, 56, 85),
            (58, 56, 85),
            (58, 57, 86),
            (56, 57, 86),
            (59, 57, 87),
            (60, 58, 89),
        ]:
        battery_lits.append((x, z2, R2))
    # anchor collapse literals (section (h))
    for (R, X, z2) in [t[:3] for t in anchor_spec]:
        battery_lits.append((sum(X), z2, R))
    battery = []
    bad_bat = 0
    for (x, z2, R2) in battery_lits:
        cf = v(x, z2, R2)
        cn = vC(x, z2, R2)
        od = vO(x, z2, R2)
        ok = (cf == cn == od)
        if not ok:
            bad_bat += 1
        battery.append({'x': x, 'z': z2, 'R': R2, 'closed': cf,
                        'vC': cn, 'vO': od, 'match': ok})
    out.append({'section': 'k0832_battery', 'literals': len(battery),
                'all_match': bad_bat == 0, 'bad': bad_bat,
                'rows': battery})


    # (b) LADDER rows (registered kit-5 S5 items (1)-(12)):
#      m=19..m=24 ladder continuation, one-past + birth pairs
    out.append(row_record_x0(
        'ladder_m19_z52_row_record',
        'registered_kit5_S5_item1_one_past_of_d7_death_of_d6',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (1) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation {19,34}@S=53 UP 1v0 (value 1 vs collapse v(53,52,72)=0 on paper); {19,32} conform-DEAD at z=52=S+1 (collapse v(51,52,72)=1); any deviation is the datum'},
        72, 52, 19, 19, 57))

    out.append(row_record_x0(
        'ladder_m19_z53_row_record',
        'registered_kit5_S5_item2_birth_slice_d8',
        {'co_token_19_allowed': True,
         's_domain': '{19..57}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (2) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY TWO separations: stick {19,34} DOWN 1v2 (collapse v(53,53,73)=2) + NEW {19,36}@S=55 UP 2v0 (collapse v(55,53,73)=0), d=8 seat gap 17; any deviation is the datum'},
        73, 53, 19, 19, 57))

    out.append(row_record_x0(
        'ladder_m20_z53_row_record',
        'registered_kit5_S5_item3_one_past_of_d7_death_of_d6',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (3) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation (20,34)@S=54 DOWN 0v1 (value 0 vs collapse v(54,53,74)=1 on paper); (20,32) conform-DEAD at z=53=S+1 (collapse v(52,53,74)=0); any deviation is the datum'},
        74, 53, 20, 20, 58))

    out.append(row_record_x0(
        'ladder_m20_z54_row_record',
        'registered_kit5_S5_item4_birth_slice_d8',
        {'co_token_20_allowed': True,
         's_domain': '{20..58}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (4) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY TWO separations: stick (20,34) DOWN 0v2 (collapse v(54,54,75)=2) + NEW (20,36)@S=56 UP 2v1 (collapse v(56,54,75)=1), d=8 seat gap 16; any deviation is the datum'},
        75, 54, 20, 20, 58))

    out.append(row_record_x0(
        'ladder_m21_z48_row_record',
        'registered_kit5_S5_item5_one_past_of_d3_death_of_d2',
        {'co_token_21_allowed': True,
         's_domain': '{21..59}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (5) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation {21,28}@S=49 UP 1v0 (value 1 vs collapse v(49,48,70)=0 on paper); {21,26} conform-DEAD at z=48=S+1 (collapse v(47,48,70)=1); any deviation is the datum'},
        70, 48, 21, 21, 59))

    out.append(row_record_x0(
        'ladder_m21_z49_row_record',
        'registered_kit5_S5_item6_birth_slice_d4',
        {'co_token_21_allowed': True,
         's_domain': '{21..59}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (6) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY TWO separations: stick {21,28} DOWN 1v2 (collapse v(49,49,71)=2) + NEW {21,30}@S=51 UP 2v0 (collapse v(51,49,71)=0), d=4 seat gap 9; any deviation is the datum'},
        71, 49, 21, 21, 59))

    out.append(row_record_x0(
        'ladder_m22_z49_row_record',
        'registered_kit5_S5_item7_one_past_of_d3_death_of_d2',
        {'co_token_22_allowed': True,
         's_domain': '{22..60}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (7) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation (22,28)@S=50 DOWN 0v1 (value 0 vs collapse v(50,49,72)=1 on paper); (22,26) conform-DEAD at z=49=S+1 (collapse v(48,49,72)=0); any deviation is the datum'},
        72, 49, 22, 22, 60))

    out.append(row_record_x0(
        'ladder_m22_z50_row_record',
        'registered_kit5_S5_item8_birth_slice_d4',
        {'co_token_22_allowed': True,
         's_domain': '{22..60}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (8) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY TWO separations: stick (22,28) DOWN 0v2 (collapse v(50,50,73)=2) + NEW (22,30)@S=52 UP 2v1 (collapse v(52,50,73)=1), d=4 seat gap 8; any deviation is the datum'},
        73, 50, 22, 22, 60))

    out.append(row_record_x0(
        'ladder_m23_z50_row_record',
        'registered_kit5_S5_item9_one_past_of_d2_death_of_d1',
        {'co_token_23_allowed': True,
         's_domain': '{23..61}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (9) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation {23,28}@S=51 UP 1v0 (value 1 vs collapse v(51,50,74)=0 on paper); {23,26} conform-DEAD at z=50=S+1 (collapse v(49,50,74)=1); any deviation is the datum'},
        74, 50, 23, 23, 61))

    out.append(row_record_x0(
        'ladder_m23_z51_row_record',
        'registered_kit5_S5_item10_birth_slice_d3',
        {'co_token_23_allowed': True,
         's_domain': '{23..61}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (10) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY TWO separations: stick {23,28} DOWN 1v2 (collapse v(51,51,75)=2) + NEW {23,30}@S=53 UP 2v0 (collapse v(53,51,75)=0), d=3 seat gap 7; any deviation is the datum'},
        75, 51, 23, 23, 61))

    out.append(row_record_x0(
        'ladder_m24_z51_row_record',
        'registered_kit5_S5_item11_one_past_of_d2_death_of_d1',
        {'co_token_24_allowed': True,
         's_domain': '{24..62}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (11) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation (24,28)@S=52 DOWN 0v1 (value 0 vs collapse v(52,51,76)=1 on paper); (24,26) conform-DEAD at z=51=S+1 (collapse v(50,51,76)=0); any deviation is the datum'},
        76, 51, 24, 24, 62))

    out.append(row_record_x0(
        'ladder_m24_z52_row_record',
        'registered_kit5_S5_item12_birth_slice_d3',
        {'co_token_24_allowed': True,
         's_domain': '{24..62}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (12) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY TWO separations: stick (24,28) DOWN 0v2 (collapse v(52,52,77)=2) + NEW (24,30)@S=54 UP 2v1 (collapse v(54,52,77)=1), d=3 seat gap 6; any deviation is the datum'},
        77, 52, 24, 24, 62))

    # (b2) FRONTIER rows m=27 / m=28 (15th / 16th datum candidates,
#      FIRST-EVER m=27 / m=28 rows)
    out.append(row_record_x0(
        'frontier_m27_z53_row_record',
        'registered_frontier_record_m27_z53_K1268_15th_datum_candidate',
        {'co_token_27_allowed': True,
         's_domain': '{27..65}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (21)/(22) + frozen section (commit d52f2be7), z* arithmetic double-checked at this build',
         'candidate': 'EXACTLY ONE separation X={27,28} @S=55, UP 2v0 (value 2 vs collapse v(55,53,81)=0 on paper); all other shapes conform; the parity frontier law is 14/14 through m=26; any deviation is the datum and is recorded verbatim',
         'z_star': 'z*(27)=2*27-2+1=53 EXACTLY (K1268; hand + derive_check double assertion at this build)'},
        81, 53, 27, 27, 65))

    out.append(row_record_x0(
        'frontier_m28_z54_row_record',
        'registered_frontier_record_m28_z54_K1268_16th_datum_candidate',
        {'co_token_28_allowed': True,
         's_domain': '{28..66}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (21)/(22) + frozen section (commit d52f2be7), z* arithmetic double-checked at this build',
         'candidate': 'EXACTLY ONE separation X=(28,28) @S=56, UP 2v1 (value 2 vs collapse v(56,54,83)=1 on paper); all other shapes conform; any deviation is the datum',
         'z_star': 'z*(28)=2*28-2+0=54 EXACTLY (K1268; hand + derive_check double assertion at this build)'},
        83, 54, 28, 28, 66))

    # (b3) m=25 / m=26 MINI-LADDER rows (registered kit-5 S5 items
#      (13)-(18), incl. the FIRST m=25 / m=26 death candidates)
    out.append(row_record_x0(
        'ladder_m25_z50_row_record',
        'registered_kit5_S5_item13_one_past_of_the_d0_seat',
        {'co_token_25_allowed': True,
         's_domain': '{25..63}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (13) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation {25,26}@S=51 UP 1v0 (value 1 vs collapse v(51,50,76)=0 on paper); any deviation is the datum'},
        76, 50, 25, 25, 63))

    out.append(row_record_x0(
        'ladder_m25_z51_row_record',
        'registered_kit5_S5_item14_birth_slice_d1_stick_coincides',
        {'co_token_25_allowed': True,
         's_domain': '{25..63}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (14) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY TWO separations: stick {25,26} DOWN 1v2 (collapse v(51,51,77)=2) + NEW {25,28}@S=53 UP 2v0 (collapse v(53,51,77)=0), d=1 seat gap 3 (stick seat coincides S(d0)=51=z); any deviation is the datum'},
        77, 51, 25, 25, 63))

    out.append(row_record_x0(
        'ladder_m25_z52_row_record',
        'registered_kit5_S5_item15_one_past_of_d1_death_of_d0_first_m25_death',
        {'co_token_25_allowed': True,
         's_domain': '{25..63}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (15) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation {25,28}@S=53 UP 1v0 (value 1 vs collapse v(53,52,78)=0 on paper); {25,26} conform-DEAD at z=52=S+1 (collapse v(51,52,78)=1) — the FIRST m=25 death datum candidate (d=0 shape); any deviation is the datum'},
        78, 52, 25, 25, 63))

    out.append(row_record_x0(
        'ladder_m26_z51_row_record',
        'registered_kit5_S5_item16_one_past_of_the_d0_seat',
        {'co_token_26_allowed': True,
         's_domain': '{26..64}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (16) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation (26,26)@S=52 DOWN 0v1 (value 0 vs collapse v(52,51,78)=1 on paper); any deviation is the datum'},
        78, 51, 26, 26, 64))

    out.append(row_record_x0(
        'ladder_m26_z52_row_record',
        'registered_kit5_S5_item17_birth_slice_d1_stick_coincides',
        {'co_token_26_allowed': True,
         's_domain': '{26..64}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (17) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY TWO separations: stick (26,26) DOWN 0v2 (collapse v(52,52,79)=2) + NEW (26,28)@S=54 UP 2v1 (collapse v(54,52,79)=1), d=1 seat gap 2 (stick seat coincides S(d0)=52=z); any deviation is the datum'},
        79, 52, 26, 26, 64))

    out.append(row_record_x0(
        'ladder_m26_z53_row_record',
        'registered_kit5_S5_item18_one_past_of_d1_death_of_d0_first_m26_death',
        {'co_token_26_allowed': True,
         's_domain': '{26..64}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 log S5 item (18) + frozen section (commit d52f2be7)',
         'candidate': 'EXACTLY ONE separation (26,28)@S=54 DOWN 0v1 (value 0 vs collapse v(54,53,80)=1 on paper); (26,26) conform-DEAD at z=53=S+1 (collapse v(52,53,80)=0) — the FIRST m=26 death datum candidate (d=0 shape); any deviation is the datum'},
        80, 53, 26, 26, 64))

    # (c) IN-BAND window rows (registered kit-5 S5 items (19)/(20),
#      strip coverage re-probed at this build: free slices)
    for z in range(41, 49):
        R = 25 + z + 1
        out.append(row_record_x0(
            'inband_m25_z%d_row_record' % z,
            'inband_window_m25_z%d' % z,
            {'co_token_25_allowed': True,
             's_domain': '{25..63}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-5 log S5 item (19) (commit d52f2be7), list 41..48 == label z*(25)-8..-1, strip coverage re-probed at this build',
             'candidate': '0 separations (in-band-clean precedent); the z=48 row is the frontier-minus-one precedent candidate (measured clean for m=13..24 one-below the frontier)',
             'band': 'm=25 in-band window pinning: z in {41..48} here; measured slices now z in {41..48} window + {49} frontier (kit-5) + {50,51,52} kit-6 mini-ladder; z in {25,26} strip-derived clean'},
            R, z, 25, 25, 63))

    for z in range(43, 50):
        R = 26 + z + 1
        out.append(row_record_x0(
            'inband_m26_z%d_row_record' % z,
            'inband_window_m26_z%d' % z,
            {'co_token_26_allowed': True,
             's_domain': '{26..64}', 'arity_max': 3,
             'style': 'x0 published residual-band style',
             'registered_by': 'kit-5 log S5 item (20) (commit d52f2be7), LISTED rows 43..50 bind per the kit-4 label/list precedent (label reads z*(26)-8..-1 = 42..49; disclosed in the docstring)',
             'candidate': '0 separations (in-band-clean precedent)',
             'band': 'm=26 in-band window pinning: z in {43..49} here + z=50 blind re-verification; measured slices now z in {43..50} + {51,52,53} kit-6 mini-ladder; z in {25,26} strip-derived clean'},
            R, z, 26, 26, 64))
    # z=50 row REPLACED below by the explicit blind re-verification of the
    # published kit-5 frontier 14th datum (candidate quoted verbatim);
    # the loop above deliberately stops at z=49 and the z=50 call is separate.

    out.append(row_record_x0(
        'frontier_m26_z50_recheck_row_record',
        'registered_frontier_recheck_m26_z50_published_14th_datum_blind_reverification',
        {'co_token_26_allowed': True,
         's_domain': '{26..64}', 'arity_max': 3,
         'style': 'x0 published residual-band style',
         'registered_by': 'kit-5 published frontier row (commit d52f2be7, the frozen ladder/frontier output m=26@z=50); blind re-verification inside the kit-5-listed window sweep 43..50 (label/list discrepancy disclosed in the docstring)',
         'candidate': 'EXACTLY ONE separation X=(26,26) @S=52, UP 2v1 (value 2 vs collapse v(52,50,77)=1 on paper) — the PUBLISHED registered frontier candidate re-measured blind; any deviation from the published row is recorded verbatim'},
        77, 50, 26, 26, 64))

    # (d) future-slice registration constants (engine-free, NOT measured)
    out.append({'section': 'future_slice_registration_constants',
                'label': 'engine_free_paper_only_K0832_closed_form_next_slice_predictions_NOT_measured_here',
                'registered_for_next_execution_kit_log_S5': [[
  {
    "kind": "one-past-of-d=8 / death-of-d=7",
    "m": 19,
    "z": 54,
    "prediction": "EXACTLY ONE: {19,36}@S=55 UP 1v0 (collapse v(55,54,74)=0); {19,34} conform-DEAD at z=54=S+1 (collapse v(53,54,74)=1)"
  },
  {
    "kind": "birth slice d=9",
    "m": 19,
    "z": 55,
    "prediction": "EXACTLY TWO: stick {19,36} DOWN 1v2 (collapse v(55,55,75)=2) + NEW {19,38}@S=57 UP 2v0 (collapse v(57,55,75)=0), d=9 seat gap 19"
  },
  {
    "kind": "one-past-of-d=8 / death-of-d=7",
    "m": 20,
    "z": 55,
    "prediction": "EXACTLY ONE: (20,36)@S=56 DOWN 0v1 (collapse v(56,55,76)=1); (20,34) conform-DEAD at z=55=S+1 (collapse v(54,55,76)=0)"
  },
  {
    "kind": "birth slice d=9",
    "m": 20,
    "z": 56,
    "prediction": "EXACTLY TWO: stick (20,36) DOWN 0v2 (collapse v(56,56,77)=2) + NEW (20,38)@S=58 UP 2v1 (collapse v(58,56,77)=1), d=9 seat gap 18"
  },
  {
    "kind": "one-past-of-d=4 / death-of-d=3",
    "m": 21,
    "z": 50,
    "prediction": "EXACTLY ONE: {21,30}@S=51 UP 1v0 (collapse v(51,50,74)=0); {21,28} conform-DEAD at z=50=S+1 (collapse v(49,50,74)=1)"
  },
  {
    "kind": "birth slice d=5",
    "m": 21,
    "z": 51,
    "prediction": "EXACTLY TWO: stick {21,30} DOWN 1v2 (collapse v(51,51,75)=2) + NEW {21,32}@S=53 UP 2v0 (collapse v(53,51,75)=0), d=5 seat gap 11"
  },
  {
    "kind": "one-past-of-d=4 / death-of-d=3",
    "m": 22,
    "z": 51,
    "prediction": "EXACTLY ONE: (22,30)@S=52 DOWN 0v1 (collapse v(52,51,76)=1); (22,28) conform-DEAD at z=51=S+1 (collapse v(50,51,76)=0)"
  },
  {
    "kind": "birth slice d=5",
    "m": 22,
    "z": 52,
    "prediction": "EXACTLY TWO: stick (22,30) DOWN 0v2 (collapse v(52,52,77)=2) + NEW (22,32)@S=54 UP 2v1 (collapse v(54,52,77)=1), d=5 seat gap 10"
  },
  {
    "kind": "one-past-of-d=3 / death-of-d=2",
    "m": 23,
    "z": 52,
    "prediction": "EXACTLY ONE: {23,30}@S=53 UP 1v0 (collapse v(53,52,76)=0); {23,28} conform-DEAD at z=52=S+1 (collapse v(51,52,76)=1)"
  },
  {
    "kind": "birth slice d=4",
    "m": 23,
    "z": 53,
    "prediction": "EXACTLY TWO: stick {23,30} DOWN 1v2 (collapse v(53,53,77)=2) + NEW {23,32}@S=55 UP 2v0 (collapse v(55,53,77)=0), d=4 seat gap 9"
  },
  {
    "kind": "one-past-of-d=3 / death-of-d=2",
    "m": 24,
    "z": 53,
    "prediction": "EXACTLY ONE: (24,30)@S=54 DOWN 0v1 (collapse v(54,53,78)=1); (24,28) conform-DEAD at z=53=S+1 (collapse v(52,53,78)=0)"
  },
  {
    "kind": "birth slice d=4",
    "m": 24,
    "z": 54,
    "prediction": "EXACTLY TWO: stick (24,30) DOWN 0v2 (collapse v(54,54,79)=2) + NEW (24,32)@S=56 UP 2v1 (collapse v(56,54,79)=1), d=4 seat gap 8"
  },
  {
    "kind": "birth slice d=2 (stick of the d=1 seat coincides: S({25,28})=53=z)",
    "m": 25,
    "z": 53,
    "prediction": "EXACTLY TWO: stick {25,28} DOWN 1v2 (collapse v(53,53,79)=2) + NEW {25,30}@S=55 UP 2v0 (collapse v(55,53,79)=0), d=2 seat gap 5"
  },
  {
    "kind": "one-past-of-d=2 / death-of-d=1",
    "m": 25,
    "z": 54,
    "prediction": "EXACTLY ONE: {25,30}@S=55 UP 1v0 (collapse v(55,54,80)=0); {25,28} conform-DEAD at z=54=S+1 (collapse v(53,54,80)=1)"
  },
  {
    "kind": "birth slice d=3",
    "m": 25,
    "z": 55,
    "prediction": "EXACTLY TWO: stick {25,30} DOWN 1v2 (collapse v(55,55,81)=2) + NEW {25,32}@S=57 UP 2v0 (collapse v(57,55,81)=0), d=3 seat gap 7"
  },
  {
    "kind": "birth slice d=2 (stick of the d=1 seat coincides: S((26,28))=54=z)",
    "m": 26,
    "z": 54,
    "prediction": "EXACTLY TWO: stick (26,28) DOWN 0v2 (collapse v(54,54,81)=2) + NEW (26,30)@S=56 UP 2v1 (collapse v(56,54,81)=1), d=2 seat gap 4"
  },
  {
    "kind": "one-past-of-d=2 / death-of-d=1",
    "m": 26,
    "z": 55,
    "prediction": "EXACTLY ONE: (26,30)@S=56 DOWN 0v1 (collapse v(56,55,82)=1); (26,28) conform-DEAD at z=55=S+1 (collapse v(54,55,82)=0)"
  },
  {
    "kind": "birth slice d=3",
    "m": 26,
    "z": 56,
    "prediction": "EXACTLY TWO: stick (26,30) DOWN 0v2 (collapse v(56,56,83)=2) + NEW (26,32)@S=58 UP 2v1 (collapse v(58,56,83)=1), d=3 seat gap 6"
  },
  {
    "kind": "one-past of the d=0 seat",
    "m": 27,
    "z": 54,
    "prediction": "EXACTLY ONE: {27,28}@S=55 UP 1v0 (collapse v(55,54,82)=0)"
  },
  {
    "kind": "birth slice d=1 (stick coincides: S(d0)=55=z)",
    "m": 27,
    "z": 55,
    "prediction": "EXACTLY TWO: stick {27,28} DOWN 1v2 (collapse v(55,55,83)=2) + NEW {27,30}@S=57 UP 2v0 (collapse v(57,55,83)=0), d=1 seat gap 3"
  },
  {
    "kind": "one-past-of-d=1 / death-of-d=0 \u2014 the FIRST m=27 death datum candidate",
    "m": 27,
    "z": 56,
    "prediction": "EXACTLY ONE: {27,30}@S=57 UP 1v0 (collapse v(57,56,84)=0); {27,28} conform-DEAD at z=56=S+1 (collapse v(55,56,84)=1)"
  },
  {
    "kind": "one-past of the d=0 seat",
    "m": 28,
    "z": 55,
    "prediction": "EXACTLY ONE: (28,28)@S=56 DOWN 0v1 (collapse v(56,55,84)=1)"
  },
  {
    "kind": "birth slice d=1 (stick coincides: S(d0)=56=z)",
    "m": 28,
    "z": 56,
    "prediction": "EXACTLY TWO: stick (28,28) DOWN 0v2 (collapse v(56,56,85)=2) + NEW (28,30)@S=58 UP 2v1 (collapse v(58,56,85)=1), d=1 seat gap 2"
  },
  {
    "kind": "one-past-of-d=1 / death-of-d=0 \u2014 the FIRST m=28 death datum candidate",
    "m": 28,
    "z": 57,
    "prediction": "EXACTLY ONE: (28,30)@S=58 DOWN 0v1 (collapse v(58,57,86)=1); (28,28) conform-DEAD at z=57=S+1 (collapse v(56,57,86)=0)"
  },
  {
    "kind": "in-band window sweep proposal",
    "m": 25,
    "z": "33..40",
    "prediction": "0 separations each (candidate); below the measured window toward the strip zone; strip-coverage re-probe required at build time"
  },
  {
    "kind": "in-band window sweep proposal",
    "m": 26,
    "z": "35..42",
    "prediction": "0 separations each (candidate); below the measured window toward the strip zone; strip-coverage re-probe required at build time"
  },
  {
    "kind": "in-band window sweep proposal",
    "m": 27,
    "z": "45..52",
    "prediction": "0 separations each (candidate); z*(27)-8..-1; NOTE: m=27 is NOT strip-covered (z26-floor20 covers m in {20..26} only), so z in {25..44} remains unmeasured and unregistered"
  },
  {
    "kind": "in-band window sweep proposal",
    "m": 28,
    "z": "46..53",
    "prediction": "0 separations each (candidate); z*(28)-8..-1; NOTE: m=28 is NOT strip-covered, so z in {25..45} remains unmeasured and unregistered"
  },
  {
    "kind": "frontier first contact proposal (FIRST-EVER m=29 row)",
    "m": 29,
    "z": 57,
    "prediction": "EXACTLY ONE: {29,30}@S=59 UP 2v0 (collapse v(59,57,87)=0); z*(29)=2*29-2+1=57 per K1268 (derive_check double-checked); R=87; the 17th datum candidate"
  },
  {
    "kind": "frontier first contact proposal (FIRST-EVER m=30 row)",
    "m": 30,
    "z": 58,
    "prediction": "EXACTLY ONE: (30,30)@S=60 UP 2v1 (collapse v(60,58,89)=1); z*(30)=2*30-2+0=58 per K1268 (derive_check double-checked); R=89; the 18th datum candidate"
  },
  {
    "kind": "not registered here \u2014 derivable scaffold extensions, register before measuring",
    "prediction": "below-window rows m=25 z in {27..32} and m=26 z in {27..34}: NOT registered by this kit; m=27 z in {25..44} and m=28 z in {25..45} are NOT strip-covered and NOT registered; the m=26 z=42 row (in the kit-5 label reading of its window) is NOT registered"
  }
]]})

    # (h) published anchor rechecks (112 spots, verbatim published values)
    rechecks = []
    H.cache_clear()
    for (R, X, z2, expected, role) in anchor_spec:
        XX = tuple(sorted(X, reverse=True))
        hv = H(R, XX, z2)
        S = sum(X)
        ev = v(S, z2, R)
        rechecks.append({'R': R, 'X': list(XX), 'z': z2, 'value': hv,
                         'collapse': ev, 'published_value': expected,
                         'match': hv == expected,
                         'conform': hv == ev,
                         'role': role})
    out.append({'section': 'published_anchor_rechecks',
                'label': 'one_hundred_twelve_published_spots_reproduce_exactly_match_field_is_value_equality_with_published',
                'rows': rechecks,
                'note': 'the separation spots are separations by construction (value != collapse BY DESIGN); the z=25/z=26 base spots are published CONFORM values; the match criterion is equality with the PUBLISHED value'})

    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
