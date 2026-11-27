# 2026-11-25 z=21/z=22 beyond-frontier probe kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY RECORD of
the spot-probe kit `research/experiments/strip-z21-beyond-probe-20261125/`.
No K slot is claimed, no universal statement is claimed. Everything below
is finite machine observation against the pinned raw engine, plus
engine-free closed-form pre-computations. No verdict is consumed.

## 1. Context, prior-lane state and slot check

Beyond-probe series state: `strip-z19-beyond-probe-20261125` (m-rows 8..13
at z=19 and spots) and `strip-z20-beyond-probe-20261125` (z=20 slices,
including the FIRST re-emergence event {(8,12) DOWN 0v2, (8,14) UP 2v1} and
the (10,12) gap+4 birth) are published. The z=21/z=22 frontier and beyond
slices of the m=8..12 arcs were UNMEASURED: the z21-min16/z22-min17 census
kits swept cell ladders and m>=13 residual-band rows only; the K1322 m=11
band closed at z=20 and the K1325 m=12 band closed at z=21, leaving their
frontier slices (z*=21, z*=22 per the published K1268 formula
z*(m)=2m−2+(m mod 2)) unmeasured. Checked: no
`research/experiments/strip-z21-beyond-probe*` directory, no z21beyond log.
Main tip at build: `4761668e`; by push time `9e8db4b5` (the PG(2,9)/cap-game
and Part EP/EQ lanes landed meanwhile; no path conflicts).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`);
  embedded startup pin `bd5f22e4…` asserted by the script (gate PASS).
- `beyond_z21.py` (sha256
  `945fda07b999ced47b7314cdfd051e099440168728e67e9131f5eb69f948e7da`)
  — adapted from the frozen published `beyond_z20.py` (`17974ab0…`) by
  the disclosed scope: eight sections — (1) m=11-row z=21 FRONTIER record
  (z*(11)=21, third frontier of the series, second odd-m frontier);
  (2) m=12-row z=22 FRONTIER record (z*(12)=22, fourth frontier, second
  even-m); (3) m=10-row z=21 (+3); (4) m=9-row z=21 (+4); (5) m=8-row
  z=21 (+7, post-re-emergence); (6) m=11-row z=22 (FIRST beyond slice of
  the m=11 arc); (7) FIFTEENTH-tail recheck (k=24) s∈{0}∪{12..60};
  (8) NEW SIXTEENTH-tail pre-computation (k=25) s∈{0}∪{12..61}. Row-record
  enumeration identical to the published frontier records (arity<=4,
  co-token allowed).
- PREDECLARED CANDIDATES (docstring, written before the first run):
  odd-m frontier singleton (11,12) UP with the z=17 constants 2v0;
  even-m frontier singleton (12,12) UP 2v1 (the m=10 z=18 constants); the
  m=10/m=9/m=8 beyond-behavior candidate lists (reabsorb/persist/flip/
  birth; first-ever gap+4 birth listed for m=10); the m=11 +1-beyond
  persist-decay/flip/reabsorb list; and the sixteenth-tail ENGINE-FREE
  candidate from K1334 theorem A k=25: hold {0}∪{12..25}, uniform 0v1
  break s>=26.
- Determination protocol: SIX runs (default ×3, PYTHONHASHSEED=1, env -i
  isolated ×2), all byte-identical (sha256
  `2854595747472b82ddc370431be2cd5712294afc4908f3468649ef6e036228dd`,
  rc 0, ~15 s each). The frozen `beyond_z21.out` IS that stdout.
- Independent ordered-engine cross-check: all 7 separation positions with
  H_ordered: 0 mismatches (part of this run's 37/37 three-kit crosscheck).

## 3. Observations (all judgment-free)

### 3.1 Frontier slices

- **m=11-row z=21: 125 shapes, exactly ONE separation X=(11,12) UP 2v0
  (S=23, collapse 0)** — the odd-m frontier candidate with the z=17
  constants CONFIRMED (rule 2/2: m=9 `(9,10) 2v0`; m=11 `(11,12) 2v0`).
- **m=12-row z=22: 95 shapes, exactly ONE separation X=(12,12) UP 2v1
  (S=24, collapse 1)** — the even-m frontier candidate with the z=18
  constants CONFIRMED (rule 2/2: m=10 `(10,10) 2v1`; m=12 `(12,12) 2v1`).
  The K1325 m=12 residual band (z∈{18..21}, closed 0-separation in the
  z21 census kit) ends here: the arc's quiet region terminates at z*.
- Frontier parity candidate (4/4 singleton, z=17/18/21/22): at odd m the
  singleton is (m,m+1) UP 2v0; at even m it is (m,m) UP 2v1. Next
  testable: m=13 at z=24, m=14 at z=26.

### 3.2 Beyond slices

- **m=10 z=21 (+3): 170 shapes, ONE separation (10,12) DOWN 0v1** — the
  (10,10) diagonal DIED at +3 (the (8,8)-arc precedent held) and the
  z=20-born (10,12) FLIPPED DOWN. The m=10 arc at z=21 matches the m=8
  arc at its singleton (m,m+2) DOWN stage structurally.
- **m=9 z=21 (+4): 234 shapes, TWO separations: (9,12) DOWN 1v2 and
  (9,14) UP 2v0** — the z=20 singleton (9,12) flipped DOWN, and a NEW
  co-token +2 birth (9,14) appeared: the FIRST gap+5 birth ever recorded
  (published births were gap+2/gap+3/gap+4/gap+6; the intra-arc co-token
  +2 cadence — m=8: 10→12→14, m=9: 12→14 — remains the organizing rule).
- **m=8 z=21 (+7): 362 shapes, ONE separation (8,14) DOWN 0v1** — the
  z=20 re-emergent pair {(8,12) DOWN 0v2, (8,14) UP 2v1} shrank to the
  singleton: (8,12) reabsorbed, (8,14) flipped DOWN. Second
  post-re-emergence datum; no second re-emergence event.
- **m=11 z=22 (the m=11 arc's FIRST beyond slice): 125 shapes, ONE
  separation (11,12) UP 1v0** — the frontier separation DECAYED
  2v0→1v0 and PERSISTED, identical to the m=9 arc's z=17→18 decay.
  +1-beyond candidate: odd-m arcs decay-persist (2/2: m=9, m=11);
  even-m arcs flip (1/1: m=10). The m=11 arc is now measured at every
  slice z∈{17..22}.

### 3.3 Supply identities (engine-free)

- FIFTEENTH-tail recheck: hold {0}∪{12..23}, 0v2 at s=24, uniformly 2v1
  for s∈{25..60} — the published z22-min17 constants reproduced,
  extended by one.
- **SIXTEENTH-tail (NEW): hold {0}∪{12..25}, UNIFORM 0v1 break for ALL
  s∈{26..61}** — exactly the predeclared K1334 theorem A k=25 odd-form
  candidate. The odd-z supply datum series is now z=17 (partner recheck,
  this run's z18-min12 kit), z=19 (tenth), z=21 (twelfth), z=23
  (fourteenth), z=25 (sixteenth): five value-uniform instances.

## 4. Honest record (this run)

- All predeclarations were written before the first run; the engine-free
  sixteenth-tail candidate comes from the K1334 theorem A machine-checked
  family (proved statement; this kit's section (8) is the measured
  z=25-slice datum).
- No wall-clock, no randomness, no hash-order dependence. The shape
  counts 125/95/170/234/362/125 are the same enumeration families as the
  published z=17..z=20 records (cross-artifact: m=10 170 and m=9 234 and
  m=8 362 reproduce the published counts; the co-token-allowed 125/95
  extensions of the m=11/m=12 rows are new measured lattices).
- Push protocol: latest main re-fetched immediately before the push; the
  z21-beyond-probe slot confirmed unclaimed.

## 5. Handoff to the later runs

- The frontier parity candidate (4/4) and the +1-beyond parity candidate
  (2/2 odd decay, 1/1 even flip) are now the two strongest finite laws of
  the arc side; the m=13 z=24 / m=14 z=26 frontier tests are the next
  discriminating measurements (heavier: R=43/45-class rows; a dedicated
  kit is appropriate).
- The m=11 arc at z=23 (+2) and the m=9/m=8 arcs deeper (z=22..24) give
  the decay-cadence follow-ups; the m=12 arc beyond (z=23: does the
  (12,12) UP 2v1 flip at +1 like m=10's did at z=19, or persist?) is the
  even-side +1 datum.
- The supply-identity chain can be extended mechanically (seventeenth
  k=26 even form: hold {0}∪{12..27}? — per K1334 theorem A the even-k
  break is 0v2-then-2v1; measure, don't assume).

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation over the
swept domains, plus pure closed-form pre-computations for the identity
sections. Nothing here is a theorem; no universal statement is claimed;
no verdict of any game position is consumed. Standard 11×11 empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4, and all
central-reply roots: all UNKNOWN, unchanged.
