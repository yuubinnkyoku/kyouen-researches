#!/usr/bin/env python3
"""
explore_frontier_lifecycle: FROZEN PRE-DECLARATION census for the
FRONTIER-REGIME x0 row records at z=27..31, the z=28 base-spot
handoff, and the TWENTY-SIXTH-tail supply pre-computation.

This is the registered-execution successor micro-kit of the
published z26f20 kit (commit 68bc863d, research/experiments/
strip-z26-floor20-20261126). It executes the published z26f20 kit
log section 5 items: #1 (the PARITY-CORRECTED FRONTIER-RECORD LAW
candidate test data: the m=15 row at z=29 and the m=16 row at
z=30, with the registered predictions), #2 (the ONE-PAST-FRONTIER
second datum candidates m=14@z=27 and m=13@z=27), #3 (the
TWENTY-SIXTH-tail k=35 ODD form pre-computation over {0} U
{12..69}), and #4 (the m=18/m=17 base-spot z=28 touch, registered
blind option tables BEFORE any measurement), and it ALSO sweeps
the in-band z=27 and z=28 row records (m=18/17/16/15) — including
the K1335 (T-Z20) m=15 residual band z=27 SEVENTH entry and z=28
EIGHTH entry (the band COMPLETION candidate, the second
fully-swept band of the series after the published K1330 m=14
completion) — plus THIS KIT'S OWN new sections: the m=15 and m=16
ONE-PAST companion records at z=30/z=31 (NO CANDIDATE, disclosed
before the run). NO K slot is claimed by this file; the constants
below were frozen into this docstring BEFORE the first run of
this file and the file has not been edited after any of its runs.

Counter-probe (required before claiming, per the registered
handoffs; re-run at push time against the then-current main): at
kit-build time the latest main contained NO z=27/z=28/z=29/z=30/
z=31 slice census kit (no `explore_z27`, `explore_z28`,
`frontier_lifecycle` or `tail26` filename or kit path exists), NO
T-Z27..T-Z31 declaration, and NO published m-row record at any
z >= 27; the ONLY published z=27 engine values anywhere are the
four z26f20 handoff spots h1..h4 (re-verified here as anchors)
and there are NO published z >= 28 engine values at all.

HONEST DISCLOSURE (paper arithmetic, before the freeze): every
collapse constant stated below is the PROVED K0832 single-token
closed form computed on paper (engine-free); the z=26 chain
values quoted as published are the z26f20/z25f20/z24f18 published
measurements. NO engine recursion on ANY z >= 27 multi-token or
single-token position was evaluated before the freeze — every
engine value below is touched for the FIRST time at the frozen
first run (the sole expected exceptions are the four published
z=27 anchor re-checks, which must reproduce 0/1/1/0).

Scope (this file measures and reports; it proves nothing by
itself):

  (a) K0832 battery: every single-token literal used by this
      file's candidate constants and derivations (row-record
      collapse staircase samples for every record, handoff
      collapse literals, published z=27 anchor collapses, supply
      identity samples incl. the k=35 anchor points and the
      previous-domain k=34 extension literals at s=69), checked
      closed-form vs canonical-engine vs ordered-engine.
      Candidate: all match.
  (b) IN-BAND z=27 row records, x0 published residual-band style
      (X = parts(S, m, 3) with X[0] == m, all parts >= m, co-token
      m allowed, arity <= 3 TOTAL, S in {m..m+38}, R = m+27+1),
      recorded against the collapse v(S,27,R):
      - m=18 R=46: the THIRD entry of the future T-Z24 residual
        band m=18 z in {25..33} (published z=25/26 entries 26/0);
        candidate 0 separations; the S=36 shape X=(18,18)
        re-verifies the published z26f20 h3 value 1 IN-RECORD.
      - m=17 R=45: the FIFTH entry of the future T-Z22 residual
        band m=17 z in {23..32}; candidate 0 separations; the
        S=35 shape X=(17,18) re-verifies the published z26f20 h1
        value 0 and the S=34 shape X=(17,17) the h4 value 0.
      - m=16 R=44: the SIXTH entry of the future T-Z21 residual
        band m=16 z in {22..29}; candidate 0 separations; the
        S=33 shape X=(16,17) re-verifies the published z26f20 h2
        value 1.
      - m=15 R=43: the SEVENTH entry of the published K1335
        (T-Z20) residual band m=15 z in {21..28}; candidate 0
        separations.
      PLUS the m=18 arity<=4 co-token extension sweep (same
      row, co-token style, arity up to 4 TOTAL), like the
      published z25f20/z26f20 m=18 ext sections.
  (c) THE ONE-PAST-FRONTIER m=14-row z=27 record at R=42, S in
      {14..52}: z*(14)=26 (K1268) — the row is ONE slice BEYOND
      its frontier (the published z26f20 at-frontier record
      showed EXACTLY ONE separation X={14,14} @S=28 UP 2v1,
      value 2 vs collapse 1). REGISTERED z26f20 S5 item #2 second
      datum candidate. NO CANDIDATE: the separation list is
      recorded verbatim whatever it is. The disclosed paper
      constants: at this slice the frontier shape X=(14,14) has
      collapse v(28,27,42)=1 (unchanged); the possible outcomes
      spelled out BEFORE the run: the separation PERSISTS at
      value 2 (UP 2v1, as at the frontier), the shape VANISHES
      into collapse (value 1 = 1v1) if the odd-analogy value
      drop 2->1 applies, or any NEW shape/value appears — each
      outcome is itself the datum.
  (d) THE TWO-PAST-FRONTIER m=13-row z=27 record at R=41, S in
      {13..51}: z*(13)=25 — the row is TWO slices beyond its
      frontier (published: z=25 at-frontier UP 2v0, z=26
      one-past UP 1v0, always the SAME single separation
      X={13,14} @S=27). REGISTERED z26f20 S5 item #2 continuation
      candidate. NO CANDIDATE: recorded verbatim. Disclosed
      paper constant: at THIS slice the persistent shape has
      collapse v(27,27,41)=2 — a JUMP (0 at z=25/z=26) caused by
      the z==x window at x=27: possible outcomes spelled out
      before the run: value 1 -> DOWN 1v2, value 2 -> 2v2 (the
      separation VANISHES into equality at higher collapse),
      value 0 -> DOWN 0v2, or any new shape; recorded as found.
  (e) IN-BAND z=28 row records, same style, R = m+28+1:
      - m=18 R=47: the FOURTH entry of the future T-Z24 residual
        band; candidate 0 separations; the S=36 shape X=(18,18)
        is the h3 z=28 handoff position (in-record cross-check).
      - m=17 R=46: the SIXTH entry of the future T-Z22 residual
        band; candidate 0 separations; the S=35 shape X=(17,18)
        is the h1 z=28 handoff position and the S=34 shape
        X=(17,17) the h4 z=28 handoff position (in-record).
      - m=16 R=45: the SEVENTH entry of the future T-Z21 residual
        band; candidate 0 separations; the S=33 shape X=(16,17)
        is the h2 z=28 handoff position (in-record).
      - m=15 R=44: the EIGHTH entry of the published K1335
        (T-Z20) residual band m=15 z in {21..28} — the band
        COMPLETION candidate: 50 shapes, candidate 0 separations,
        which would COMPLETE the second fully-swept residual band
        of the series (after the K1330 m=14 band completion,
        published by the z25f20 kit).
      PLUS the m=18 arity<=4 co-token extension sweep.
  (f) THE FRONTIER TEST ROWS (the registered z26f20 S5 item #1
      parity-corrected law candidates, the headline of the kit):
      - m=15-row z=29 record at R=45, S in {15..53} (z*(15)=29
        exactly, K1268): REGISTERED candidate — EXACTLY ONE
        separation, X={15,16} @S=31, UP 2v0 (odd parity: the
        m=13 datum shape; collapse v(31,29,45)=0 on paper); all
        other 49 shapes conform (0 separations).
      - m=16-row z=30 record at R=47, S in {16..54} (z*(16)=30
        exactly): REGISTERED candidate — EXACTLY ONE separation,
        X={16,16} @S=32, UP 2v1 (even parity: the m=14 datum
        shape; collapse v(32,30,47)=1 on paper); all other 39
        shapes conform. Any deviation (extra separations, missing
        separation, different shape/value) is itself the datum
        and is recorded verbatim.
  (g) THE ONE-PAST COMPANION ROWS (NEW sections added by this
      kit, NOT required by the registered handoff; NO CANDIDATE,
      disclosed before the run) — the one-past regime only has
      the single published m=13 datum (value drop 2->1 at the
      persistent shape) and these two rows pair directly with
      the (f) frontier rows to make the at-frontier/one-past
      comparison SAME-shape:
      - m=15-row z=30 record at R=46, S in {15..53} (one past
        z*(15)=29): collapse of the frontier shape
        X={15,16}@S=31 is v(31,30,46)=0 on paper; disclosed
        expectation (non-binding, the odd m=13 analogy): the
        separation persists at the same shape with dropped value
        UP 1v0; recorded verbatim whatever it is.
      - m=16-row z=31 record at R=48, S in {16..54} (one past
        z*(16)=30): collapse of the frontier shape
        X={16,16}@S=32 is v(32,31,48)=1 on paper; disclosed
        expectation (non-binding, the even analog of the
        value-drop): a drop 2->1 would make the shape EQUAL its
        collapse (1v1, vanish branch), persistence keeps UP 2v1,
        recorded verbatim whatever it is.
  (h) z=28 CROSS-SLICE HANDOFF (the registered z26f20 S5 item #4
      z=28 touch; option tables frozen here BEFORE the run):
      - h1 = H(46;{17,18};28) [m=17-row z=28 first co-token
        member, blind]: candidate collapse-CONFORM 0 (the m=17
        first co-token conformed 0 at z=26 and z=27; collapse
        v(35,28,46)=0 on paper).
      - h2 = H(45;{16,17};28) [m=16-row z=28 first co-token
        member, blind]: candidate collapse-CONFORM 1 (the m=16
        first co-token conformed 1 at z=26 and z=27; collapse
        v(33,28,45)=1 on paper).
      - h3 = H(47;(18,18);28) [m=18 base-spot z-sequence next
        on-line member]: frozen option table {B-child = h1
        [itself first-contact, in-kit premise disclosed],
        C-child 1^H(46;(18,18);27) = 1^1 = 0 PUBLISHED (the
        z26f20 z=27 handoff h3)} -> mex{h1, 0} = 1 (conform,
        collapse v(36,28,47)=1 on paper) iff h1 conforms 0.
      - h4 = H(46;(17,17);28) [m=17 base-spot z-sequence next
        on-line member]: frozen option table {B-child = h2
        [in-kit premise disclosed], C-child 1^H(45;(17,17);27) =
        1^0 = 1 PUBLISHED (the z26f20 z=27 handoff h4)} ->
        mex{h2, 1} = 0 (conform, collapse v(34,28,46)=0 on
        paper) iff h2 conforms 1.
      The m=18 on-line z-sequence so far: z in {16..27} =
      0,1,0,1,0,1,0,1,1,1,1,1 (published incl. the z=27 value by
      the z26f20 kit); the z=28 candidate here is a structural
      continuation registered BEFORE any z=28 lattice exists.
  (i) published recheck anchors: the four published z=27 spots
      (45;{17,18};27)=0, (44;{16,17};27)=1, (46;(18,18);27)=1,
      (45;(17,17);27)=0 — must reproduce exactly.
  (j) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed
      form, NO engine recursion), all over the EXTENDED domain
      s in {0} U {12..69} (each extended by one point from the
      published z26f20 kit domain {0} U {12..68}): the
      CONSOLIDATED 14th..25th tail table v(s,k+1,k+1) vs
      v(s,k,k+1) for k in {23..34} — RECHECKS of every published
      constant (odd k: hold {0} U {12..k}, UNIFORM 0v1 for all
      s >= k+1; even k: hold {0} U {12..k-1}, 0v2 at s=k, UNIFORM
      2v1 for all s >= k+1) — PLUS the NEW TWENTY-SIXTH-tail
      PRE-COMPUTATION v(s,36,36) vs v(s,35,36), k=35 — the
      REGISTERED candidate of the z26f20 kit log S5 item #3:
      hold {0} U {12..35}, UNIFORM 0v1 for ALL s in {36..69}
      (paper anchors: v(35,36,36)=v(35,35,36)=1 equal at the hold
      edge; v(36,36,36)=0 vs v(36,35,36)=1 the 0v1 break at
      s=36; v(69,36,36)=0 vs v(69,35,36)=1 uniform at the end;
      the odd-z supply chain graduates to candidate 9/9:
      k=19/21/23/25/27/29/31/33 measured (8) + k=35 closed-form
      here); the z=35-slice supply datum is precomputed for the
      future z=35 declaration lane.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_frontier_lifecycle.out).
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

ORDINAL = {23: 'fourteenth', 24: 'fifteenth', 25: 'sixteenth',
           26: 'seventeenth', 27: 'eighteenth', 28: 'nineteenth',
           29: 'twentieth', 30: 'twenty-first', 31: 'twentysecond',
           32: 'twentythird', 33: 'twentyfourth', 34: 'twentyfifth'}
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


def cell_sweep(j, smax):
    """sweep cell_j over s in {0} U {20..smax}; returns (dev, multi, total)"""
    R = j + 27
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(20, smax + 1)):
        ys = [()] if s == 0 else parts(s, 20, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 26)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 26, R)
            if val != exp:
                dev.append({'s': s, 'value': val, 'collapse': exp,
                            'direction': 'UP' if val > exp else 'DOWN',
                            'shapes': len(vals[val])})
    H.cache_clear()
    return dev, multi, total


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



ORDINAL = {23: 'fourteenth', 24: 'fifteenth', 25: 'sixteenth',
           26: 'seventeenth', 27: 'eighteenth', 28: 'nineteenth',
           29: 'twentieth', 30: 'twenty-first', 31: 'twentysecond',
           32: 'twentythird', 33: 'twentyfourth', 34: 'twentyfifth',
           35: 'twentysixth'}


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    vC = ns['vC']
    vO = ns['vO']
    # (a) K0832 battery: every single-token literal used by this file.
    battery_lits = []
    # z=27 record collapse staircase samples (one per record edge + band points)
    for (x, z2, R2) in [
            (18, 27, 46), (20, 27, 46), (24, 27, 46), (36, 27, 46),
            (37, 27, 46), (45, 27, 46), (56, 27, 46),
            (17, 27, 45), (19, 27, 45), (33, 27, 45), (34, 27, 45),
            (35, 27, 45), (52, 27, 45), (55, 27, 45),
            (16, 27, 44), (22, 27, 44), (32, 27, 44), (33, 27, 44),
            (45, 27, 44), (54, 27, 44),
            (15, 27, 43), (29, 27, 43), (30, 27, 43), (36, 27, 43),
            (43, 27, 43), (53, 27, 43),
            (14, 27, 42), (26, 27, 42), (27, 27, 42), (28, 27, 42),
            (30, 27, 42), (40, 27, 42), (42, 27, 42), (52, 27, 42),
            (13, 27, 41), (26, 27, 41), (27, 27, 41), (28, 27, 41),
            (39, 27, 41), (40, 27, 41), (51, 27, 41)]:
        battery_lits.append((x, z2, R2))
    # z=28 record collapse staircase samples
    for (x, z2, R2) in [
            (18, 28, 47), (24, 28, 47), (36, 28, 47), (37, 28, 47),
            (46, 28, 47), (56, 28, 47),
            (17, 28, 46), (19, 28, 46), (33, 28, 46), (34, 28, 46),
            (35, 28, 46), (53, 28, 46), (55, 28, 46),
            (16, 28, 45), (22, 28, 45), (32, 28, 45), (33, 28, 45),
            (44, 28, 45), (54, 28, 45),
            (15, 28, 44), (29, 28, 44), (30, 28, 44), (31, 28, 44),
            (43, 28, 44), (53, 28, 44)]:
        battery_lits.append((x, z2, R2))
    # frontier + one-past companion collapse literals
    for (x, z2, R2) in [
            (15, 29, 45), (31, 29, 45), (32, 29, 45), (44, 29, 45),
            (53, 29, 45), (45, 29, 45),
            (16, 30, 47), (32, 30, 47), (33, 30, 47), (46, 30, 47),
            (54, 30, 47),
            (15, 30, 46), (31, 30, 46), (32, 30, 46), (45, 30, 46),
            (53, 30, 46),
            (16, 31, 48), (32, 31, 48), (33, 31, 48), (47, 31, 48),
            (54, 31, 48)]:
        battery_lits.append((x, z2, R2))
    # handoff option-table + published z=27 anchor collapse literals
    for (x, z2, R2) in [
            (35, 28, 46), (33, 28, 45), (36, 28, 47), (34, 28, 46),
            (35, 27, 45), (33, 27, 44), (36, 27, 46), (34, 27, 45)]:
        battery_lits.append((x, z2, R2))
    # supply identity sample points: k=35 NEW anchors + k=34 s=69 extension
    for (x, z2, R2) in [
            (12, 36, 36), (35, 36, 36), (36, 36, 36), (35, 35, 36),
            (36, 35, 36), (69, 36, 36), (69, 35, 36),
            (69, 35, 35), (69, 34, 35), (12, 35, 35), (35, 35, 35),
            (36, 35, 35)]:
        battery_lits.append((x, z2, R2))
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
    # (b) IN-BAND z=27 row records
    out.append(row_record_x0(
        'inband_m18_z27_row_record',
        'third_entry_tz24_residual_band_m18_z27',
        {'co_token_18_allowed': True,
         'residual_band': 'future T-Z24 declaration residual band m=18 z in {25..33} (frontier z*(18)=34 per K1268: z*(m)=2m-2+(m mod 2)); published z=25 entry 26/0 (z25f20 kit), z=26 entry 26/0 (z26f20 kit); candidate 0 separations here; the S=36 shape X=(18,18) re-verifies the published z26f20 z=27 handoff h3 value 1',
         's_domain': '{18..56}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        46, 27, 18, 18, 56))
    out.append(row_record(
        'inband_m18_z27_row_record_ext_arity4',
        'arity_le4_extension_cotoken_style',
        {'co_token_18_allowed': True,
         's_domain': '{18..56}', 'arity_max': 4},
        46, 27, 18, 18, 56, 18))
    out.append(row_record_x0(
        'inband_m17_z27_row_record',
        'fifth_entry_tz22_residual_band_m17_z27',
        {'co_token_17_allowed': True,
         'residual_band': 'future T-Z22 declaration residual band m=17 z in {23..32} (frontier z*(17)=33); published entries 32/0 at z=23/24/25/26 (z23f17/z24f18/z25f20/z26f20 kits); candidate 0 separations here; the S=35 shape X=(17,18) re-verifies the published z26f20 z=27 handoff h1 value 0 and the S=34 shape X=(17,17) the h4 value 0',
         's_domain': '{17..55}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        45, 27, 17, 17, 55))
    out.append(row_record_x0(
        'inband_m16_z27_row_record',
        'sixth_entry_tz21_residual_band_m16_z27',
        {'co_token_16_allowed': True,
         'residual_band': 'future T-Z21 residual band m=16 z in {22..29} (frontier z*(16)=30); published entries 40/0 at z=22..26; candidate 0 separations here; the S=33 shape X=(16,17) re-verifies the published z26f20 z=27 handoff h2 value 1',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        44, 27, 16, 16, 54))
    out.append(row_record_x0(
        'inband_m15_z27_row_record',
        'k1335_residual_band_m15_z27_seventh_entry',
        {'co_token_15_allowed': True,
         'residual_band': 'K1335 (T-Z20) published residual band m=15 z in {21..28} (frontier z*(15)=29); published entries 50/0 at z=21..26; candidate 0 separations here; the z=28 entry (measured by this kit) completes the band',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        43, 27, 15, 15, 53))
    # (c) ONE-PAST-FRONTIER m=14-row z=27 record (registered z26f20 S5 #2)
    out.append(row_record_x0(
        'onepast_m14_z27_row_record',
        'one_past_frontier_record_m14_z27_NO_CANDIDATE_registered_z26f20_S5_item2',
        {'co_token_14_allowed': True,
         'residual_band': 'z*(14)=26 (K1268); the published at-frontier z=26 record showed EXACTLY ONE separation X={14,14} @S=28 UP 2v1 (value 2 vs collapse 1, z26f20 kit); z=27 is ONE PAST the frontier; NO CANDIDATE: the separation list is recorded verbatim; disclosed paper constants: the frontier shape collapse stays v(28,27,42)=1, so the spelled-out outcomes are persist UP 2v1 / vanish into equality 1v1 (the odd-analogy value drop 2->1) / any new shape — each outcome is the datum',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        42, 27, 14, 14, 52))
    # (d) TWO-PAST-FRONTIER m=13-row z=27 record (registered z26f20 S5 #2)
    out.append(row_record_x0(
        'twopast_m13_z27_row_record',
        'two_past_frontier_record_m13_z27_NO_CANDIDATE_registered_z26f20_S5_item2',
        {'co_token_13_allowed': True,
         'residual_band': 'z*(13)=25 (K1268); published frontier series for the SAME shape X={13,14}@S=27: z=25 at-frontier UP 2v0, z=26 one-past UP 1v0 (both z25f20/z26f20 kits); z=27 is TWO PAST the frontier; NO CANDIDATE: recorded verbatim; disclosed paper constant: the persistent-shape collapse JUMPS to v(27,27,41)=2 at this slice (z==x window at x=27), so the spelled-out outcomes are value 1 -> DOWN 1v2 / value 2 -> 2v2 vanish-into-equality / value 0 -> DOWN 0v2 / any new shape',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        41, 27, 13, 13, 51))
    # (e) IN-BAND z=28 row records
    out.append(row_record_x0(
        'inband_m18_z28_row_record',
        'fourth_entry_tz24_residual_band_m18_z28',
        {'co_token_18_allowed': True,
         'residual_band': 'future T-Z24 declaration residual band m=18 z in {25..33}; published z=25/26 entries 26/0, this kit publishes the z=27 entry; candidate 0 separations here; the S=36 shape X=(18,18) is the h3 z=28 handoff position (in-record cross-check)',
         's_domain': '{18..56}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        47, 28, 18, 18, 56))
    out.append(row_record(
        'inband_m18_z28_row_record_ext_arity4',
        'arity_le4_extension_cotoken_style',
        {'co_token_18_allowed': True,
         's_domain': '{18..56}', 'arity_max': 4},
        47, 28, 18, 18, 56, 18))
    out.append(row_record_x0(
        'inband_m17_z28_row_record',
        'sixth_entry_tz22_residual_band_m17_z28',
        {'co_token_17_allowed': True,
         'residual_band': 'future T-Z22 declaration residual band m=17 z in {23..32}; candidate 0 separations here; the S=35 shape X=(17,18) is the h1 z=28 handoff position and the S=34 shape X=(17,17) the h4 z=28 handoff position (in-record cross-checks)',
         's_domain': '{17..55}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        46, 28, 17, 17, 55))
    out.append(row_record_x0(
        'inband_m16_z28_row_record',
        'seventh_entry_tz21_residual_band_m16_z28',
        {'co_token_16_allowed': True,
         'residual_band': 'future T-Z21 residual band m=16 z in {22..29}; candidate 0 separations here; the S=33 shape X=(16,17) is the h2 z=28 handoff position (in-record cross-check)',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        45, 28, 16, 16, 54))
    out.append(row_record_x0(
        'inband_m15_z28_row_record',
        'k1335_residual_band_m15_z28_eighth_entry_BAND_COMPLETION',
        {'co_token_15_allowed': True,
         'residual_band': 'K1335 (T-Z20) published residual band m=15 z in {21..28}; published entries 50/0 at z=21..26 and 50/0 at z=27 (this kit, in the same run); candidate 0 separations here COMPLETES the band — the second fully-swept residual band of the series after the published K1330 m=14 band completion (z25f20 kit)',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        44, 28, 15, 15, 53))
    # (f) THE FRONTIER TEST ROWS (registered z26f20 S5 item #1 candidates)
    out.append(row_record_x0(
        'frontier_m15_z29_row_record',
        'frontier_record_m15_z29_registered_parity_candidate_odd_K1268_L1',
        {'co_token_15_allowed': True,
         'residual_band': 'z*(15)=29 = z EXACTLY (K1268: z*(m)=2m-2+(m mod 2)); REGISTERED candidate (z26f20 S5 item #1, the parity-corrected frontier-record law, two published data points m=13 odd {m,m+1}@S=2m+1 UP 2v0 / m=14 even {m,m} @S=2m UP 2v1): EXACTLY ONE separation X={15,16} @S=31, UP 2v0 (collapse v(31,29,45)=0 on paper); all other 49 shapes conform; any deviation (extra/missing/different separation) is itself the datum and is recorded verbatim',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        45, 29, 15, 15, 53))
    out.append(row_record_x0(
        'frontier_m16_z30_row_record',
        'frontier_record_m16_z30_registered_parity_candidate_even_K1268_L2',
        {'co_token_16_allowed': True,
         'residual_band': 'z*(16)=30 = z EXACTLY (K1268); REGISTERED candidate (z26f20 S5 item #1): EXACTLY ONE separation X={16,16} @S=32, UP 2v1 (collapse v(32,30,47)=1 on paper); all other 39 shapes conform; any deviation is itself the datum and is recorded verbatim',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        47, 30, 16, 16, 54))
    # (g) THE ONE-PAST COMPANION ROWS (own sections, NO CANDIDATE)
    out.append(row_record_x0(
        'onepast_m15_z30_row_record',
        'one_past_frontier_record_m15_z30_NO_CANDIDATE_added_by_this_kit',
        {'co_token_15_allowed': True,
         'residual_band': 'z*(15)=29; z=30 is ONE PAST the frontier of the m=15 row; added by this kit to pair with the at-frontier m=15 z=29 record measured in the same run; NO CANDIDATE: recorded verbatim; disclosed non-binding expectation (the odd m=13 analogy): the frontier separation X={15,16}@S=31 persists at the same shape with dropped value UP 1v0 (collapse v(31,30,46)=0 on paper)',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        46, 30, 15, 15, 53))
    out.append(row_record_x0(
        'onepast_m16_z31_row_record',
        'one_past_frontier_record_m16_z31_NO_CANDIDATE_added_by_this_kit',
        {'co_token_16_allowed': True,
         'residual_band': 'z*(16)=30; z=31 is ONE PAST the frontier of the m=16 row; added by this kit to pair with the at-frontier m=16 z=30 record measured in the same run; NO CANDIDATE: recorded verbatim; disclosed non-binding expectation (the even analog of the value-drop): the frontier shape X={16,16}@S=32 has collapse v(32,31,48)=1 on paper, so a 2->1 value drop would VANISH into equality (1v1), persistence keeps UP 2v1, any new shape/value is the datum',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        48, 31, 16, 16, 54))
    # (h) z=28 cross-slice handoff (registered z26f20 S5 item #4)
    h1 = H(46, tuple(sorted((17, 18), reverse=True)), 28)
    h2 = H(45, tuple(sorted((16, 17), reverse=True)), 28)
    h3 = H(47, (18, 18), 28)
    h4 = H(46, (17, 17), 28)
    out.append({'section': 'z28_crossslice_handoff',
                'label': 'z26f20_S5_item4_registration_base_spot_blind_picks_first_ever_z28_engine_touches',
                'spots': [
                    {'id': 'h1', 'X': [17, 18], 'R': 46, 'z': 28,
                     'value': h1, 'collapse': v(35, 28, 46),
                     'role': 'm17-row z=28 first co-token member; candidate collapse-conform 0 (conformed 0 at z=26 and z=27; collapse v(35,28,46)=0 on paper)',
                     'match': h1 == v(35, 28, 46)},
                    {'id': 'h2', 'X': [16, 17], 'R': 45, 'z': 28,
                     'value': h2, 'collapse': v(33, 28, 45),
                     'role': 'm16-row z=28 first co-token member; candidate collapse-conform 1 (conformed 1 at z=26 and z=27; collapse v(33,28,45)=1 on paper)',
                     'match': h2 == v(33, 28, 45)},
                    {'id': 'h3', 'X': [18, 18], 'R': 47, 'z': 28,
                     'value': h3, 'collapse': v(36, 28, 47),
                     'role': 'm=18 base-spot z-sequence next on-line member; frozen option table {B-child = h1 (in-kit first-contact premise disclosed), C-child 1^H(46;(18,18);27)=1^1=0 PUBLISHED z26f20 z=27 handoff h3}; candidate mex{h1,0}=1 (collapse v(36,28,47)=1 on paper) CONFORMING iff h1 conforms 0',
                     'match': h3 == v(36, 28, 47)},
                    {'id': 'h4', 'X': [17, 17], 'R': 46, 'z': 28,
                     'value': h4, 'collapse': v(34, 28, 46),
                     'role': 'm=17 base-spot z-sequence next on-line member; frozen option table {B-child = h2 (in-kit premise disclosed), C-child 1^H(45;(17,17);27)=1^0=1 PUBLISHED z26f20 z=27 handoff h4}; candidate mex{h2,1}=0 (collapse v(34,28,46)=0 on paper) CONFORMING iff h2 conforms 1',
                     'match': h4 == v(34, 28, 46)}],
                'published_anchor': 'm=18 on-line z-sequence z in {16..27} = 0,1,0,1,0,1,0,1,1,1,1,1 (published incl. the z=26 value by the z25f20 h3 and the z=27 value by the z26f20 h3); the z=28 candidate here is a structural continuation registered BEFORE any z=28 lattice exists'})
    # (i) published recheck anchors (4 spots, all published by the z26f20 kit)
    rechecks = []
    for (R, X, expected) in [
            (45, (17, 18), 0), (44, (16, 17), 1), (46, (18, 18), 1),
            (45, (17, 17), 0)]:
        XX = tuple(sorted(X, reverse=True))
        hv = H(R, XX, 27)
        S = sum(X)
        ev = v(S, 27, R)
        rechecks.append({'R': R, 'X': list(XX), 'z': 27, 'value': hv,
                         'collapse': ev, 'published_value': expected,
                         'match': hv == ev == expected})
    out.append({'section': 'published_recheck_anchors_z27', 'rows': rechecks})
    # (j) consolidated tail supply identities k in {23..35}
    for k in range(23, 36):
        holds = []
        breaks = []
        for s in [0] + list(range(12, 70)):
            a = v(s, k + 1, k + 1)
            b = v(s, k, k + 1)
            row = {'s': s, f'v_{k+1}_{k+1}': a, f'v_{k}_{k+1}': b,
                   'equal': a == b}
            (holds if a == b else breaks).append(row)
        if k == 35:
            lab = ('observational_only_new_registered_candidate_twentysixth_tail_k35_odd_form_9of9_candidate_z26f20_S5_item3')
            note = ('REGISTERED candidate (z26f20 kit log S5 item #3, commit 68bc863d): hold {0} U {12..35}, UNIFORM 0v1 for ALL s in {36..69}; odd-z supply form measured chain k=19/21/23/25/27/29/31/33 (8/8 measured) + k=35 closed-form here = 9/9 candidate; the z=35-slice supply datum for the future z=35 declaration lane')
            secname = 'twentysixth_tail_supply_identity_precalc'
        elif k == 34:
            lab = ('observational_only_closed_form_recheck_supply_identity_k0832')
            note = ('published by the z26f20 kit (25th tail, registered candidate CONFIRMED): hold {0} U {12..33}, 0v2 break at s=34, UNIFORM 2v1 for ALL s >= 35 (even-z supply chain candidate 8/8); rechecked here extended by one point to s=69')
            secname = f'{ORDINAL[k]}_tail_supply_identity_recheck'
        elif k in (32, 33):
            lab = ('observational_only_closed_form_recheck_supply_identity_k0832')
            if k == 32:
                note = ('NEW by the z25f20 kit (23rd tail, m18spot S5 item #1 registered candidate CONFIRMED): hold {0} U {12..31}, 0v2 break at s=32, UNIFORM 2v1 for ALL s >= 33; rechecked here extended by one point')
            else:
                note = ('NEW registration by the z25f20 kit (24th tail, both components predeclared): hold {0} U {12..33}, UNIFORM 0v1 for ALL s >= 34 (odd-z supply form 8/8 with k=35); rechecked here extended by one point')
            secname = f'{ORDINAL[k]}_tail_supply_identity_recheck'
        else:
            lab = ('observational_only_closed_form_recheck_supply_identity_k0832')
            if k % 2 == 0:
                shape = 'even-k identity: hold {0} U {12..k-1}, 0v2 break at s=k, UNIFORM 2v1 for all s >= k+1'
            else:
                shape = 'odd-k identity: hold {0} U {12..k}, UNIFORM 0v1 for all s >= k+1'
            note = ('published constant recheck (published by the series kits z20f14/z21f15/z22f16/z23f17/z24f18/m18spot/z25f20/z26f20): ' + shape)
            secname = f'{ORDINAL[k]}_tail_supply_identity_recheck'
        out.append({'section': secname,
                    'label': lab,
                    'k': k, 'ordinal': ORDINAL[k],
                    'identity': f'v(s,{k+1},{k+1}) =? v(s,{k},{k+1})',
                    's_domain': '{0} U {12..69}',
                    'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                    'published_anchor': note,
                    'hold_rows': holds, 'break_rows': breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
