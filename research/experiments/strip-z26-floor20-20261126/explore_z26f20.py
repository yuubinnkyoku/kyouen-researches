#!/usr/bin/env python3
"""
explore_z26f20: FROZEN PRE-DECLARATION census for the z=26 FLOOR-20
(z-6, SUB-CRITICAL floor) cell ladder — the ELEVENTH edition of the
floor-(z-6) series (z=15 K1321, z=16 `059c531e`, z=17 `82f98ef4`,
z=18 `0bb7e440`, z=19 `5b2275bc`, z=20 `2d8cea40`, z=21 `5b01e14c`,
z=22 `fb215b76`/`daa9a805`, z=23 `9577fadc`, z=24 `35f7fe59`) and
the SIXTH EVEN edition of the 11-entry lattice prediction. NO K slot
is claimed by this file; the constants below were frozen into this
docstring BEFORE the first run of this file and the file has not been
edited after any of its runs.

The architectural target is the REGISTERED PREDICTION carried by the
published z25f20 kit log section 5 item #1 (commit `155c6ad2`) and
before it by the m18spot kit log section 5 item #2 (commit
`b8146415`): "z=26 floor-20 (z-6 sub-critical, EVEN) census kit ...
its head (s=20) row derives from THIS kit's published s=20 row by the
same disclosed cascade discipline (single observational dependency on
this kit's finite observations; disclose per rung). Executes the
registered 11-entry deviant lattice at positions {20,22,24,26} (head
trio @s=20 {B DOWN 0v2, A UP 1v0, A2 UP 2v1}; @s=22 {C UP 1v0, B UP
2v1, D DOWN 0v2}; @s=24 {E UP 1v0, D UP 2v1, G DOWN 0v2}; @s=26 {F
UP 1v0, G UP 2v1}; all other rungs conform; 0 multivalue), the
+2-shift structural crosscheck against this kit, the strip m in
{21..26} segments, and the m=14-row z=26 record — which sits AT ITS
OWN FRONTIER (z*(14)=26, K1268): register it with NO candidate,
explicitly first-contact." The registered TWENTY-FIFTH-tail handoff
of the z25f20 kit log section 5 item #4 ("k=34 EVEN form candidate:
hold {0} U {12..33}, 0v2@34, UNIFORM 2v1 s in {35..68}") and item "the
m=18 base-spot z-sequence next appreciable extension needs a z=27
touch — register the blind option table before measuring" are ALSO
executed here. The counter-probe required before claiming was
performed at kit-build time: NO z=26 census kit exists on main
(filename:explore_z26 returns nothing; `z26f20` returns nothing; the
kit path does not exist), NO T-Z26 declaration exists, and the only
published z=26 engine values are the four z25f20 handoff spots h1..h4.

HONEST DISCLOSURE (drafting discipline, before the freeze): the head
(s=20) row below was DERIVED BY HAND in-session from published inputs
ONLY: (1) the published z25f20 frozen census s=20 row (finite
observations: deviants C/B/A = station values {1,0,2} at j=5/6/7,
every other rung conform at its PROVED K0832 collapse constant — the
observational dependency REDUCES to the three published deviant
cells), (2) the PROVED K0832 closed form for every stair / removal /
collapse literal, (3) the PROVED K1264 stair equality at the
floor-token decrease (window R <= z+min(X), here EXACT equality R =
26+j for the (19,j) children of the j=1..19 rungs), and (4) the
left-to-right in-head cascade, with the j=20 (A14) rung derived via
the coinciding-decrease structure (X=(20,20): both B-children land on
Cell_19(20) exactly). The drafting scratch machine cross-checked
ONLY the published z=25 input literals H(j+26;(20,j);25), j=1..20,
against the engine (20/20 exact matches); it evaluated NO z=26 or
z=27 multi-token position, and no single-token z=26/z=27 engine
position either — every z=26/z=27 value below is touched by the
engine for the first time at the frozen first run. The s>=21 rows are
NOT derivable from published data (the z=25 census rows are finite
observations, not proved constants) — they are pre-declared
STRUCTURAL candidates from the published EVEN chain (z=16 `059c531e`,
z=18 `0bb7e440`, z=20 `2d8cea40`, z=22 `fb215b76`, z=24 `35f7fe59`,
all measured value-exact at positions {z-6,z-4,z-2,z}): the
registered 11-entry lattice below. The even editions carry NO F
persistent tail (the odd-edition F HOLE+TAIL signature does not
continue; the even F cell carries a single UP 1v0 at s=z only).

Scope (this file measures and reports; it proves nothing by itself):

  (a) cell census: for each j in 1..20 (rungs F,G,E,D,C,B,A,A2..A14)
      the floor-20 cell Cell_j(s) := H(j+27; {j} U Y; 26), Y tokens
      >= 20, s = sum(Y) in {0} U {20..51}, arity(Y) in 0..4 (0 only
      at s=0), swept EXHAUSTIVELY against the published raw engine
      (K1138 recursion, embedded block byte-identical to the
      K1282..K1344 chain, pin bd5f22e4...). Reported per cell:
      deviants from the Sigma-collapse v(s+j,26,j+27) (K0832 closed
      form) and any multivalue (decomposition-dependence) rows.
      20 rungs = F..A14: A12 (j=18) and A13 (j=19) close the
      stair-derivable ladder (R = j+26 = 26+min=j EXACT window
      equalities); A14 (j=20) is derived via the coinciding-decrease
      structure (both B-children = Cell_19(20); C-child = the
      published z25f20 m=20 base-spot member H(46;(20,20);25)=1).
      PREDECLARED CANDIDATES (frozen before the first run):
      (i) THE s=20 ROW (derived, per-rung option sets below;
          collapse = v(j+20,26,j+27)):
          j=1  F   CONFORM  1  ({stair v(20,26,27)=0,
               removal v(20,27,27)=0, 1^c1=1^1=0} -> mex 1);
          j=2  G   CONFORM  0  ({stair v(21,26,28)=1, cascade 1,
               1^c2=1^0=1} -> mex 0);
          j=3  E   CONFORM  1  ({stair v(22,26,29)=0, cascade 0,
               1^c3=1^1=0} -> mex 1);
          j=4  D   CONFORM  0  ({stair v(23,26,30)=1, cascade 1,
               1^c4=1^0=1} -> mex 0);
          j=5  C   CONFORM  1  ({stair v(24,26,31)=0, cascade 0,
               1^c5=1^1=0} -> mex 1);
          j=6  B   DOWN 0v2 (value 0 vs collapse 2)  ({stair
               v(25,26,32)=1, cascade 1, 1^c6=1^0=1} -> mex 0 !=
               collapse v(26,26,33)=2) — THE REGISTERED HEAD TRIO
               ENTRY 1;
          j=7  A   UP 1v0 (value 1 vs collapse 0)  ({stair
               v(26,26,33)=2, cascade 0, 1^c7=1^2=3} -> mex 1 !=
               collapse v(27,26,34)=0; the exotic A-cell option set
               {0,2,3} of the even chain) — THE REGISTERED HEAD TRIO
               ENTRY 2;
          j=8  A2  UP 2v1 (value 2 vs collapse 1)  ({stair
               v(27,26,34)=0, cascade 1, 1^c8=1^1=0} -> mex 2 !=
               collapse v(28,26,35)=1) — THE REGISTERED HEAD TRIO
               ENTRY 3;
          j=9..19 A3..A13 CONFORM, alternating 0/1 in step
               (j=9 {1,1,2}->mex 0 = v(29,26,36); j=10 {0,0,0}->mex
               1 = v(30,26,37); ... j=19 A13 closes conform
               mex{1}=0 = v(39,26,46)=0);
          j=20 A14 CONFORM 1 = v(40,26,47)  (X=(20,20): both
               decreases coincide with Cell_19(20), options {cascade
               head_19=0, 1^c20=1^1=0} -> mex 1).
          where the C-child inputs c_j := H(j+26;{j,20};25) are the
          PUBLISHED z25f20 census values at s=20:
          c = [1,0,1,0,1,0,2,1,0,1,0,1,0,1,0,1,0,1,0,1] for j=1..20
          (j=5/6/7 the measured deviants {1,0,2}; every other j the
          conform PROVED closed form v(j+20,25,j+26)).
          THE REGISTERED CLAIM CARRIED BY THIS ROW: the even
          sub-critical head trio {B DOWN 0v2, A UP 1v0, A2 UP 2v1}
          at s=z-6=20 extends its published value-exact even chain
          (z=16/18/20/22/24) to candidate 6/6, the mirror of the odd
          head-empty rule 5/5 (z=15/17/19/21/23); the A RANK stays
          DEAD at even z (UP 1v0, not the odd UP 2v0 rebirth).
      (ii) s in {21..51}: THE REGISTERED 11-ENTRY LATTICE read at
           positions {22,24,26} — value-exact BLIND candidates
           (scaled +2 from the measured value-exact even chain
           z=16/18/20/22/24, 5/5 at positions {z-4, z-2, z};
           cellwise identical value/collapse numbers):
           at s=22 (z-4): C(j=5) UP 1v0 (vs collapse v(27,26,32)=0),
               B(j=6) UP 2v1 (vs v(28,26,33)=1), D(j=4) DOWN 0v2
               (vs v(26,26,31)=2);
           at s=24 (z-2): E(j=3) UP 1v0 (vs v(27,26,30)=0),
               D(j=4) UP 2v1 (vs v(28,26,31)=1), G(j=2) DOWN 0v2
               (vs v(26,26,29)=2);
           at s=26 (=z): F(j=1) UP 1v0 (vs v(27,26,28)=0),
               G(j=2) UP 2v1 (vs v(28,26,29)=1);
           and NO other deviant row in {21..51} — the even-edition
           chain shows clean conform rows outside the 11 positions
           and NO F persistent tail (the odd editions' F UP 2v0 tail
           for s >= z+1 does NOT appear at even z; the sub-floor
           block s in {40..51} where multi-token Y=(20,k) components
           enter — (20,20) first at s=40 — carries the published
           even-chain candidates NO multivalue rows and NO new
           deviant classes), 0 multivalue. Total predicted deviant
           rows: 11 = 3 (head trio) + 8 (lattice).
      (iii) all cells s-only; multivalue rows 0.
  (b) tail spots: s in {52..59}, single-token shape Y=(s,), all 20
      cells — candidate 160/160 MATCH (the EVEN-edition signature:
      the published z24f18 tail spots were 136/136 match — the odd
      editions' F 8/8 value-2 mismatch signature does NOT appear at
      even z). BLIND (no even tail-spot row was published at more
      than two editions before; z24f18 136/136 is the prior datum).
  (c) strip sweep m in {20..26} at R=m+27, z=26: NO T-Z26 exists, so
      every segment is a NEW in-band z=26 measurement (z*(m) =
      2m-2+(m mod 2) > 26 for all m in {19..26}); m=20 is the
      head-floor row segment (the even-chain convention: the m=z-6
      strip segment, like the published z24f18 m=18), m in {21..26}
      the would-be T-Z26 claim positions (the registered handoff
      range; the even-chain convention adds the m=20 floor segment —
      both are swept and disclosed). Candidates 0 violations for
      every segment (the strip family has never produced a violation
      in any published kit); measured counts recorded whatever they
      are.
  (d) IN-BAND m=18-row z=26 record at R=45, x0 published
      residual-band style (all parts >= 18, co-token 18 allowed,
      arity <= 3 TOTAL, S in {18..56}): the SECOND entry of the
      future T-Z24 declaration residual band m=18 z in {25..33}
      (first: the published z25f20 26/0); the S=36 shape X=(18,18)
      re-verifies the published z25f20 handoff h3 value 1 inside the
      record. Candidate 0 separations. PLUS the arity<=4 co-token
      extension sweep.
  (d2) IN-BAND m=17-row z=26 record at R=44, S in {17..55}: the
      FOURTH entry of the future T-Z22 declaration residual band
      m=17 z in {23..32} (published: 32/0 at z=23/24/25); contains
      the published handoff h1 (17,18)@S=35 = 0 and h4 (17,17)@S=34
      = 0 as in-record recheck anchors. Candidate 0 separations.
  (d3) IN-BAND m=16-row z=26 record at R=43, S in {16..54}: the
      z=26 entry of the future T-Z21 residual band m=16 z in
      {22..29} (published: 40/0 at z=22/23/24/25); contains the
      published handoff h2 (16,17)@S=33 = 1 as in-record anchor.
      Candidate 0 separations.
  (d4) IN-BAND m=15-row z=26 record at R=42, S in {15..53}: the
      SIXTH entry of the K1335 (T-Z20) published residual band m=15
      z in {21..28} (published: 50/0 at z=21..25). Candidate 0
      separations.
  (d5) THE FRONTIER m=14-row z=26 record at R=41, S in {14..52}:
      z*(14)=26 = z EXACTLY (K1268) — the row sits ON ITS OWN
      FRONTIER, the second at-frontier row record of the series
      after the published z25f20 m=13 datum. NO CANDIDATE: first
      contact, unexplored regime, the constants are recorded whatever
      they are; the registered z25f20 section-5 frontier-separation
      law candidate (ONE prior datum: m=13 at z=25, exactly one
      separation X={13,14} @S=27, UP, value 2 vs collapse 0)
      predicts the separations BEGINNING at the first co-token
      shape X={14,15} @S=29, UP, value 2 vs collapse 0 — recorded
      here as a NON-BINDING structural expectation; its confirmation
      or refutation is itself the datum.
  (d6) THE ONE-PAST-FRONTIER m=13-row z=26 record at R=40, S in
      {13..51}: z*(13)=25 < 26 — the row is one slice BEYOND its
      frontier (the published z=25 record showed exactly one
      separation {13,14}@S=27). This section is NOT required by the
      registered handoff; it is added by this kit as the third
      frontier-region datum (m=13 z=25 at-frontier / m=14 z=26
      at-frontier / m=13 z=26 one-past). NO CANDIDATE: first contact
      of the one-past regime, the separation list is recorded
      verbatim whatever it is.
  (e) strip spots m in {27..30} at R=m+27, X in
      {(m,m+1),(m,m+2),(m,m,m+1)}: NEW z=26 spots (candidate 12/12
      conform per the strip family), PLUS the z=26 base spots:
      (e1) m=20 base spot H(47;(20,20);26): paper-derived candidate
           1 CONFORMING (options {B-child H(46;(19,20);26) = the
           m=19-strip z=26 position with the published-formula
           conform candidate v(39,26,46)=0, 1^c = 1^H(46;(20,20);25)
           = 1^1 = 0 PUBLISHED (the z25f20 m=20 base spot)} ->
           mex{0,0} = 1 = the collapse v(40,26,47)); the disclosed
           premise (conform value of the unmeasured m=19-strip
           position) is an observation the run tests together — the
           same composite-honesty structure as the published z25f20
           (e1).
      (e2) m=19 base spot H(46;(19,19);26): paper-derived candidate
           0 CONFORMING (options {B-child H(45;(18,19);26) = the
           m=18-row z=26 record position S=37 with conform candidate
           v(37,26,45)=1 (in-kit premise: the (d) record tested in
           the same run), 1^H(45;(19,19);25) = 1^0 = 1 PUBLISHED
           (the z25f20 m=19 base spot)} -> mex{1,1} = 0 = the
           collapse v(38,26,46)).
      (e3) published recheck anchors (4 spots, all published by the
           z25f20 kit z=26 handoff): (44;{17,18};26)=0,
           (43;{16,17};26)=1, (45;(18,18);26)=1, (44;(17,17);26)=0.
  (f) below-band bottom-rung child census: the j=1 cell's removal
      child is the below-band position H(27;Y;27) with min(Y) >= 20
      (child slice z'=27, floor 20 = z'-7), swept over s in {0} U
      {20..51}, arity 0..4, against v(s,27,27). This is the NINTH
      z'-7 empty-datum candidate of the series (the eight published
      below-band full collapses were swept at z'=17/19/20/21/22/23/
      24/25; the z25f20 kit below-band was the z'-6 BB-type at z'=26
      — a different series). Candidate 0 deviants, 0 multivalue
      rows. The published K1264 stair applicability R=27 <= 27+min
      suggests the collapse is a stair consequence at ANY floor;
      recorded here as a machine corroboration of that PROVED
      lemma's instance; the generalization belongs to a declaration
      lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed
      form, NO engine recursion), all over the EXTENDED domain
      s in {0} U {12..68} (each extended by one point from the
      published z25f20 kit domain {0} U {12..67}): the CONSOLIDATED
      14th..24th tail table v(s,k+1,k+1) vs v(s,k,k+1) for k in
      {23..33} — RECHECKS of every published constant (odd k: hold
      {0} U {12..k}, UNIFORM 0v1 for all s >= k+1; even k: hold
      {0} U {12..k-1}, 0v2 at s=k, UNIFORM 2v1 for all s >= k+1) —
      the z25f20 consolidated table extended by one point; PLUS
      the NEW TWENTY-FIFTH-tail PRE-COMPUTATION v(s,35,35) vs
      v(s,34,35), k=34 — the REGISTERED candidate of the z25f20 kit
      log section 5 item #4: hold {0} U {12..33}, break 0v2 at s=34,
      then UNIFORM 2v1 for ALL s in {35..68} (the even-z supply
      chain graduates to candidate 8/8: k=20/22/24/26/28/30 measured
      + k=32 closed-form published + k=34 closed-form here).
  (h) z=27 CROSS-SLICE HANDOFF (four FIRST-EVER z=27 engine touches,
      option tables frozen here BEFORE the run — the z25f20 section-5
      registration "the next appreciable extension needs a z=27
      touch; register the blind option table before measuring"):
      (h1) H(45;{17,18};27) [the m=17-row z=27 first co-token
           member]: candidate collapse-CONFORM 0 = v(35,27,45).
      (h2) H(44;{16,17};27) [the m=16-row z=27 first co-token
           member]: candidate collapse-CONFORM 1 = v(33,27,44).
      (h3) H(46;(18,18);27) [the m=18 base-spot z-sequence next
           on-line member]: candidate 1 = collapse v(36,27,46)
           CONFORMING via the frozen table: options {B-child =
           (h1) [itself first-contact, in-kit premise disclosed],
           C-child 1^H(45;(18,18);26) = 1^1 = 0 PUBLISHED (the
           z25f20 z=26 handoff h3)} -> mex{0,0} = 1 iff (h1)
           conforms 0.
      (h4) H(45;(17,17);27) [the m=17 base-spot z-sequence next
           on-line member]: candidate 0 = collapse v(34,27,45)
           CONFORMING via the frozen table: options {B-child =
           (h2) [in-kit premise disclosed], C-child
           1^H(44;(17,17);26) = 1^0 = 1 PUBLISHED (the z25f20 z=26
           handoff h4)} -> mex{1,1} = 0 iff (h2) conforms 1.
      The m=18 on-line z-sequence so far: z in {16..26} =
      0,1,0,1,0,1,0,1,1,1,1 (published, incl. both z=25 readings
      by the m18spot kit and the z=26 value by the z25f20 h3); the
      z=27 candidates here are structural continuations registered
      BEFORE any z=27 lattice exists (the honest form is the full
      option-set table, not a naked value pick).
  (i) K0832 closed-form-vs-engine battery: every single-token
      literal used by this file's derivations (stair/removal
      children, collapses of every measured anchor spot, supply
      samples), checked closed-form vs canonical-engine vs
      ordered-engine. Candidate: all match.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z26f20.out).
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


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    vC = ns['vC']
    vO = ns['vO']
    # (i) K0832 battery: every single-token literal used by the file.
    battery_lits = []
    for j in range(1, 21):                       # stair children j=1..20
        battery_lits.append((19 + j, 26, j + 26))
    battery_lits.append((20, 27, 27))            # j=1 removal child
    # head/station collapse literals (j=1..20)
    for (x, z2, R2) in [(21,26,28),(22,26,29),(23,26,30),(24,26,31),
                        (25,26,32),(26,26,33),(27,26,34),(28,26,35),
                        (29,26,36),(30,26,37),(31,26,38),(32,26,39),
                        (33,26,40),(34,26,41),(35,26,42),(36,26,43),
                        (37,26,44),(38,26,45),(39,26,46),(40,26,47),
                        (25,26,32),(26,26,31),(28,26,33),(27,26,32),
                        (26,26,29),(28,26,31),(27,26,30),(27,26,28),
                        (28,26,29),(26,26,31)]:
        battery_lits.append((x, z2, R2))
    # measured anchor spot collapses (z=26 rechecks, base spots, z=27)
    for (x, z2, R2) in [(35,26,44),(33,26,43),(36,26,45),(34,26,44),
                        (39,26,46),(40,26,47),(37,26,45),(38,26,46),
                        (40,25,46),(38,25,45),
                        (35,27,45),(33,27,44),(36,27,46),(34,27,45),
                        (52,27,27),(59,27,27)]:
        battery_lits.append((x, z2, R2))
    # C-child input collapse literals of the head derivation (z=25
    # published conform rungs; deviant j=5/6/7 excluded since their
    # engine value is not the closed form)
    for j in range(1, 21):
        if j not in (5, 6, 7):
            battery_lits.append((20 + j, 25, j + 26))
    # supply identity sample points
    for (x, z2, R2) in [(12,34,34),(33,34,34),(34,34,34),(33,33,34),
                        (67,34,34),(12,35,35),(33,35,35),(34,35,35),
                        (35,35,35),(34,34,35),(68,35,35)]:
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
    # (a) cell census j=1..20 (F..A14)
    cells = {}
    names = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
             'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
             'A13', 'A14']
    for j in range(1, 21):
        name = names[j - 1]
        dev, multi, total = cell_sweep(j, 51)
        cells[f'cell{j}_{name}26f20'] = {
            'z': 26, 'min': j, 'R': j + 27, 'floor': 20,
            's_domain': '{0} U {20..51}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}26f20',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots s in {52..59}
    tail = []
    for j in range(1, 21):
        nm = names[j - 1]
        for s in range(52, 60):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 27, X, 26)
            exp = v(s + j, 26, j + 27)
            tail.append({'cell': f'{nm}26f20', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s52_59', 'rows': tail})
    # (c) strip sweep m in {20..26} at R=m+27 (no T-Z26 exists)
    sv = []
    viol = []
    cnt = 0
    for m in range(20, 27):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 27, XX, 26)
                ev = v(S, 26, m + 27)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z26_m20_26', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND m=18-row z=26 record — T-Z24 band second entry.
    out.append(row_record_x0(
        'inband_m18_z26_row_record',
        'second_entry_tz24_residual_band_m18_z26_after_published_z25_26shapes',
        {'co_token_18_allowed': True,
         'residual_band': 'no T-Z24 published yet (the future T-Z24 declaration residual band m=18 z in {25..33}; frontier z*(18)=34 per the K1268 formula z*(m)=2m-2+(m mod 2)); published z=25 entry: 26 shapes 0 separations (z25f20 kit); candidate 0 separations here; the S=36 shape X=(18,18) re-verifies the published z25f20 handoff h3 value 1',
         's_domain': '{18..56}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        45, 26, 18, 18, 56))
    out.append(row_record(
        'inband_m18_z26_row_record_ext_arity4',
        'arity_le4_extension_cotoken_style',
        {'co_token_18_allowed': True,
         's_domain': '{18..56}', 'arity_max': 4},
        45, 26, 18, 18, 56, 18))
    # (d2) IN-BAND m=17-row z=26 record: future T-Z22 band fourth entry.
    out.append(row_record_x0(
        'inband_m17_z26_row_record',
        'future_tz22_residual_band_m17_z26_fourth_entry',
        {'co_token_17_allowed': True,
         'residual_band': 'future T-Z22 declaration residual band m=17 z in {23..32} (frontier z*(17)=33); published z=23/24/25 entries: 32 shapes 0 separations each; candidate 0 separations here; the S=35 shape X=(17,18) re-verifies the published z25f20 handoff h1 value 0 and the S=34 shape X=(17,17) the handoff h4 value 0',
         's_domain': '{17..55}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        44, 26, 17, 17, 55))
    # (d3) IN-BAND m=16-row z=26 record.
    out.append(row_record_x0(
        'inband_m16_z26_row_record',
        'future_tz21_residual_band_m16_z26_entry',
        {'co_token_16_allowed': True,
         'residual_band': 'future T-Z21 residual band m=16 z in {22..29}; published entries: 40 shapes 0 separations at z=22/23/24/25; candidate 0 separations here; the S=33 shape X=(16,17) re-verifies the published z25f20 handoff h2 value 1',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        43, 26, 16, 16, 54))
    # (d4) IN-BAND m=15-row z=26 record.
    out.append(row_record_x0(
        'inband_m15_z26_row_record',
        'k1335_residual_band_m15_z26_sixth_entry',
        {'co_token_15_allowed': True,
         'residual_band': 'K1335 (T-Z20) published residual band m=15 z in {21..28}; published entries: 50 shapes 0 separations at z=21/22/23/24/25; candidate 0 separations here',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        42, 26, 15, 15, 53))
    # (d5) THE FRONTIER m=14-row z=26 record — NO CANDIDATE, first
    #      contact at the row's own frontier z*(14)=26 = z (K1268).
    out.append(row_record_x0(
        'inband_m14_z26_row_record_FRONTIER',
        'frontier_record_m14_z26_NO_CANDIDATE_first_contact_zstar14_equals_26_K1268',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25} COMPLETE with 62 shapes 0 separations at each of z=20..25 (band completion by the z25f20 kit); z=26 sits ON the row frontier z*(14)=26 exactly (K1268: z*(m)=2m-2+(m mod 2)); NO CANDIDATE: first contact of the at-frontier regime, constants recorded whatever they are; the registered z25f20 S5 frontier-separation law candidate (ONE prior datum: m=13 at z=25, exactly one separation X={13,14} @S=27 UP 2v0) predicts separations BEGINNING at the first co-token shape X={14,15} @S=29 UP 2v0 - NON-BINDING structural expectation recorded before the run; the confirmation or refutation is itself the datum',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        41, 26, 14, 14, 52))
    # (d6) ONE-PAST-FRONTIER m=13-row z=26 record — NO CANDIDATE (extra
    #      section added by this kit; not required by the handoff).
    out.append(row_record_x0(
        'inband_m13_z26_row_record_ONE_PAST_FRONTIER',
        'one_past_frontier_record_m13_z26_NO_CANDIDATE_first_contact_added_by_this_kit',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24} complete 76/0 at each; published z=25 at-frontier record: 76 shapes EXACTLY ONE separation X={13,14} @S=27 UP 2v0 (z*(13)=25, the first frontier datum of the series); z=26 is ONE PAST the frontier - an unexplored regime; NO CANDIDATE: the separation list is recorded verbatim whatever it is; added by this kit as the third frontier-region datum (m13 z25 at-frontier / m14 z26 at-frontier / m13 z26 one-past)',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        40, 26, 13, 13, 51))
    # (e) strip spots m in {27..30} at R=m+27 (NEW z=26 spots)
    spots = []
    for m in range(27, 31):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 27, X, 26)
            ev = v(S, 26, m + 27)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m27_30', 'rows': spots})
    # (e1) m=20 base spot (paper-derived candidate 1, conforming)
    w20 = H(47, (20, 20), 26)
    w20v = v(40, 26, 47)
    out.append({'section': 'm20_base_spot', 'X': [20, 20], 'R': 47,
                'z': 26, 'value': w20, 'collapse_single': w20v,
                'match': w20 == w20v,
                'published_probe_crossref': 'NEW measurement (no published kit measured H(47;(20,20);26)); paper-derived candidate value 1 = v(40,26,47) conforming, derivation frozen in this file docstring before the first run (B-child on the m=19-strip z=26 position H(46;(19,20);26) with conform candidate v(39,26,46)=0 - an UNMEASURED premise the run tests together, same composite-honesty structure as the published z25f20 (e1), C-child 1^H(46;(20,20);25) = 1^1 = 0 PUBLISHED (the z25f20 m=20 base spot)) -> mex{0,0} = 1'})
    # (e2) m=19 base spot (paper-derived candidate 0, conforming)
    w19 = H(46, (19, 19), 26)
    w19v = v(38, 26, 46)
    out.append({'section': 'm19_base_spot', 'X': [19, 19], 'R': 46,
                'z': 26, 'value': w19, 'collapse_single': w19v,
                'match': w19 == w19v,
                'published_probe_crossref': 'NEW measurement (no published kit measured H(46;(19,19);26)); paper-derived candidate value 0 = v(38,26,46) conforming, derivation frozen in this file docstring before the first run (B-child on the m=18-row z=26 record position H(45;(18,19);26) S=37 with conform candidate v(37,26,45)=1 (in-kit premise: the (d) record tested in the same run), C-child 1^H(45;(19,19);25) = 1^0 = 1 PUBLISHED (the z25f20 m=19 base spot)) -> mex{1,1} = 0'})
    # (e3) published recheck anchors (4 spots, all published by the
    #      z25f20 kit z=26 handoff)
    rechecks = []
    for (R, X, expected) in [
            (44, (17, 18), 0), (43, (16, 17), 1), (45, (18, 18), 1),
            (44, (17, 17), 0)]:
        XX = tuple(sorted(X, reverse=True))
        hv = H(R, XX, 26)
        S = sum(X)
        ev = v(S, 26, R)
        rechecks.append({'R': R, 'X': list(XX), 'value': hv,
                         'collapse': ev, 'published_value': expected,
                         'match': hv == ev == expected})
    out.append({'section': 'published_recheck_anchors_z26', 'rows': rechecks})
    # (f) below-band j=1 removal child H(27;Y;27), Y >= 20
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(20, 52)):
        ys = [()] if s == 0 else parts(s, 20, 4)
        vals = {}
        for y in ys:
            h = H(27, y, 27)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 27, 27)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H27_27',
                'label': 'observational_only_ninth_zprime7_datum_belowband_supply_source_at_z26_floor20',
                'R': 27, 'z': 27, 'floor': 20,
                's_domain': '{0} U {20..51}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g) consolidated tail supply identities k in {23..34}
    for k in range(23, 35):
        holds = []
        breaks = []
        for s in [0] + list(range(12, 69)):
            a = v(s, k + 1, k + 1)
            b = v(s, k, k + 1)
            row = {'s': s, f'v_{k+1}_{k+1}': a, f'v_{k}_{k+1}': b,
                   'equal': a == b}
            (holds if a == b else breaks).append(row)
        if k == 34:
            lab = ('observational_only_new_registered_candidate_twentyfifth_tail_k34_even_form_8of8_candidate_z25f20_S5_item4')
            note = ('REGISTERED candidate (z25f20 kit log S5 item #4, commit 155c6ad2): hold {0} U {12..33}, break 0v2 at s=34, UNIFORM 2v1 for ALL s in {35..68}; even-z supply form measured chain k=20/22/24/26/28/30 (6/6 measured) + k=32 closed-form published (7/7) + k=34 closed-form here = 8/8 candidate; the z=34-slice supply datum for the future z=34 declaration lane')
            secname = 'twentyfifth_tail_supply_identity_precalc'
        elif k in (32, 33):
            lab = ('observational_only_closed_form_recheck_supply_identity_k0832')
            if k == 32:
                note = ('NEW by the z25f20 kit (23rd tail, m18spot S5 item #1 registered candidate CONFIRMED): hold {0} U {12..31}, 0v2 break at s=32, UNIFORM 2v1 for ALL s >= 33 (7/7); rechecked here extended by one point')
            else:
                note = ('NEW registration by the z25f20 kit (24th tail, both components predeclared): hold {0} U {12..33}, UNIFORM 0v1 for ALL s >= 34 (odd-z supply form 8/8); rechecked here extended by one point')
            secname = f'{ORDINAL[k]}_tail_supply_identity_recheck'
        else:
            lab = ('observational_only_closed_form_recheck_supply_identity_k0832')
            if k % 2 == 0:
                shape = 'even-k identity: hold {0} U {12..k-1}, 0v2 break at s=k, UNIFORM 2v1 for all s >= k+1'
            else:
                shape = 'odd-k identity: hold {0} U {12..k}, UNIFORM 0v1 for all s >= k+1'
            note = ('published constant recheck (published by the series kits z20f14/z21f15/z22f16/z23f17/z24f18/m18spot/z25f20): ' + shape)
            secname = f'{ORDINAL[k]}_tail_supply_identity_recheck'
        out.append({'section': secname,
                    'label': lab,
                    'k': k, 'ordinal': ORDINAL[k],
                    'identity': f'v(s,{k+1},{k+1}) =? v(s,{k},{k+1})',
                    's_domain': '{0} U {12..68}',
                    'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                    'published_anchor': note,
                    'hold_rows': holds, 'break_rows': breaks})
    # (h) z=27 cross-slice handoff, four first-ever z=27 engine touches
    #     with option tables frozen before the run (z25f20 S5 item on
    #     the m=18 base-spot z-sequence extension).
    h1 = H(45, tuple(sorted((17, 18), reverse=True)), 27)
    h2 = H(44, tuple(sorted((16, 17), reverse=True)), 27)
    h3 = H(46, (18, 18), 27)
    h4 = H(45, (17, 17), 27)
    out.append({'section': 'z27_crossslice_handoff',
                'label': 'z25f20_S5_registration_base_spot_blind_picks_first_ever_z27_engine_touches',
                'spots': [
                    {'id': 'h1', 'X': [17, 18], 'R': 45, 'z': 27,
                     'value': h1, 'collapse': v(35, 27, 45),
                     'role': 'm17-row z=27 first co-token member; candidate collapse-conform 0 = v(35,27,45)',
                     'match': h1 == v(35, 27, 45)},
                    {'id': 'h2', 'X': [16, 17], 'R': 44, 'z': 27,
                     'value': h2, 'collapse': v(33, 27, 44),
                     'role': 'm16-row z=27 first co-token member; candidate collapse-conform 1 = v(33,27,44)',
                     'match': h2 == v(33, 27, 44)},
                    {'id': 'h3', 'X': [18, 18], 'R': 46, 'z': 27,
                     'value': h3, 'collapse': v(36, 27, 46),
                     'role': 'm=18 base-spot z-sequence next on-line member; frozen option table {B-child = h1 (in-kit first-contact premise disclosed), C-child 1^H(45;(18,18);26)=1^1=0 PUBLISHED z25f20 h3}; candidate mex{0,0}=1 = collapse v(36,27,46) CONFORMING iff h1 conforms 0',
                     'match': h3 == v(36, 27, 46)},
                    {'id': 'h4', 'X': [17, 17], 'R': 45, 'z': 27,
                     'value': h4, 'collapse': v(34, 27, 45),
                     'role': 'm=17 base-spot z-sequence next on-line member; frozen option table {B-child = h2 (in-kit first-contact premise disclosed), C-child 1^H(44;(17,17);26)=1^0=1 PUBLISHED z25f20 h4}; candidate mex{1,1}=0 = collapse v(34,27,45) CONFORMING iff h2 conforms 1',
                     'match': h4 == v(34, 27, 45)}],
                'published_anchor': 'm=18 on-line z-sequence z in {16..26} = 0,1,0,1,0,1,0,1,1,1,1 (published incl. both z=25 readings by the m18spot kit and the z=26 value by the z25f20 h3); the z=27 candidates here are structural continuations registered BEFORE any z=27 lattice exists'})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
