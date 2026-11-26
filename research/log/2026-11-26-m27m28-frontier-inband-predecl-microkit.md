# m27/m28 frontier + m23..m26 band in-band windows pre-declaration micro-kit (kit-6)

- kit id: kit-6 (hourly lane, session 2026-11-26, ~11:20Z build)
- runclass: publish-then-execute pre-declaration census, frozen before the
  literal push; committee by machine observation only
- commit base: d52f2be7 (kit-5, the then-current main at build time)
- files:
  `research/experiments/strip-newband-m27m28-frontier-inband-20261126/{engine_block.py, explore_m27m28_frontier.py, explore_m27m28_frontier.out, README.md}`
- engine: published chain clone, sha 582c93c1…, startup pin bd5f22e4… (PASS)
- explorer sha256: `2c7ac4a9a57c7f112808754cf68d3fee652b6775301dc946c40ca0496d1ca8d9`
- frozen output sha256: `4eda4e1e68bcb8b9645d775be2554504072b97438650efaf81be8b4919f0648e` (74,197 bytes)
- status: EXECUTED, VERIFIED, PUSHED (run rc 0, ~23 s; see S4)

## S1. Anchor re-verification (112/112)

The 93 kit-5-era published anchors verbatim, plus the 19 kit-5
separation spots FIRST re-anchored here. Both stages ran BEFORE the
frozen census: the 19 spots were derive-checked against the published
kit-5 values and passed 19/19, then every anchor was re-executed in
the frozen run and hit exactly (R-first convention asserted, the kit-5
S/R splice class provably void here). Battery 398/398 all-match
(K0832 closed-form vs canonical vs ordered, all candidate literals
and registration literals including the 44 kit-7 future triples).
No prior datum lost; cumulative anchor count 112.

## S2. Registered vs measured (36/36 FULL HIT, zero surprises)

Ladder continuation rows (kit-5 log S5 items (1)-(12)):

| row | registered candidate (binding) | verdict | measured |
|----|----|----|----|
| m=19 z=52 | EXACTLY ONE {19,34}@S=53 UP 1v0, {19,32} dead | HIT | as registered; first m=19 d=6 death |
| m=19 z=53 | EXACTLY TWO: stick {19,34} DOWN 1v2 + {19,36}@S=55 UP 2v0 | HIT | d=8 birth, gap 17; m=19 ladder COMPLETE through d=8 (9 seats) |
| m=20 z=53 | EXACTLY ONE (20,34)@S=54 DOWN 0v1, (20,32) dead | HIT | first m=20 d=6 death |
| m=20 z=54 | EXACTLY TWO: stick + (20,36)@S=56 UP 2v1 | HIT | d=8 birth, gap 16; m=20 ladder COMPLETE through d=8 |
| m=21 z=48 | EXACTLY ONE {21,28}@S=49 UP 1v0, {21,26} dead | HIT | first m=21 d=2 death |
| m=21 z=49 | EXACTLY TWO: stick 1v2 + {21,30}@S=51 UP 2v0 | HIT | d=4 birth, gap 9 |
| m=22 z=49 | EXACTLY ONE (22,28)@S=50 DOWN 0v1, (22,26) dead | HIT | first m=22 d=2 death |
| m=22 z=50 | EXACTLY TWO: stick 0v2 + (22,30)@S=52 UP 2v1 | HIT | d=4 birth, gap 8 |
| m=23 z=50 | EXACTLY ONE {23,28}@S=51 UP 1v0, {23,26} dead | HIT | first m=23 d=1 death |
| m=23 z=51 | EXACTLY TWO: stick 1v2 + {23,30}@S=53 UP 2v0 | HIT | d=2 birth, gap 7 |
| m=24 z=51 | EXACTLY ONE (24,28)@S=52 DOWN 0v1, (24,26) dead | HIT | first m=24 d=1 death |
| m=24 z=52 | EXACTLY TWO: stick (24,28) DOWN 0v2 + (24,30)@S=54 UP 2v1 | HIT | d=3 birth, gap 6 |

m=25 / m=26 mini-ladder (kit-5 S5 items (13)-(18)):

| row | registered candidate | verdict | measured |
|----|----|----|----|
| m=25 z=50 | one-past UP 1v0 {25,26} (decay 2->1 of 13th datum) | HIT | as registered |
| m=25 z=51 | birth d=1 EXACTLY TWO: {25,26} UP 1v2 + {25,28}@S=52 UP 2v1 | HIT | stick slice z=51=S(d0) coincide, parity-exact |
| m=25 z=52 | EXACTLY ONE {25,28}@S=53 UP 1v0, {25,26} dead at z=52=S+1 | HIT | **FIRST m=25 DEATH** (d=0) |
| m=26 z=51 | one-past DOWN 0v1 (26,26) (decay of 14th datum) | HIT | as registered |
| m=26 z=52 | EXACTLY ONE stick (26,26) DOWN 0v2 | HIT | stick slice coincide |
| m=26 z=53 | EXACTLY ONE (26,28)@S=54 DOWN 0v1, (26,26) dead at z=53=S+1 | HIT | **FIRST m=26 DEATH** (d=0) |

Frontier parity law, 15th/16th datum (first-ever m=27/m=28 rows):

| row | registered candidate | verdict | measured |
|----|----|----|----|
| m=27 z=53 | EXACTLY ONE {27,28}@S=55 UP 2v0, collapse v(55,53,81)=0 | HIT | 13 shapes |
| m=28 z=54 | EXACTLY ONE (28,28)@S=56 UP 2v1, collapse v(56,54,83)=1 | HIT | 12 shapes |

In-band windows (kit-5 S5 items (19)/(20); the m=26 label/list
discrepancy resolved by LIST, kit-4 precedent, frozen in the
docstring): m=25 z in {41..48} 8/8 CLEAN (15 shapes each,
R=67..74, all 0 separations); m=26 z in {43..49} 7/7 CLEAN (14 shapes
each, R=70..76); the listed m=26 z=50 row executed as an explicit
BLIND RE-VERIFICATION of the published kit-5 14th frontier datum and
reproduced it EXACTLY ((26,26)@S=52 UP 2v1). Measured in-band
coverage: m=25 z in {41..52} + strip {25,26}; m=26 z in {43..53} +
strip. The z=42 row of the label reading NOT registered, NOT
measured (kit-7 proposal below).

## S3. Scaffolding state after kit-6

- Frontier parity law: **16/16** through m=28 (was 14/14). The
  value alternation v=0 at 15th, v=1 at 16th holds; 17th (m=29@z=57,
  v(59,57,87)=0 predicted) and 18th (m=30@z=58, v(60,58,89)=1
  predicted) registered below.
- Death class witnessed: m=19/m=20 d in {0..6}, m=21/m=22 d in
  {0..2}, m=23/m=24 d in {0..1}, m=25/m=26 d=0 (frontier-adjacent
  seats only, finite observations).
- Ladder completeness: m=19 (complete, d=0..8 birth seats), m=20
  (complete, d=0..8); m=21 d=4 birth witnessed, m=22 d=4, m=23 d=2,
  m=24 d=3.
- One-past decay counts (published + kit-6): odd 2->1 = 31, even
  2->0 = 30. Observation counts, not universal claims.
- Shapes: 22,20,19,18,17,16,15,14,13,12 for m=19..28 frontier-adjacent
  rows (quadratic guess stays refuted).

## S4. Verification (all executed)

1. Frozen published run rc 0, ~23 s.
2. Determinism: default x2 + PYTHONHASHSEED=random + env -i isolated
   x2, total 6 byte-identical runs, plus a push-time rerun; det 1..5.
3. Battery 398/398; anchors 112/112; candidate-vs-measured 36/36.
4. Ordered-engine independent audit (audit_kit6, outside the frozen
   artifact): 36/36 rows separation-value-exact over 568 shapes;
   anchors 112 bad 0.
5. Engine-free derive check (derive_check_kit6): 77 collapse literals
   from the closed form, z*(25)..z*(30) arithmetic, S=sum(X),
   R=m+z+1, UP/DOWN vs collapse direction for every parseable claim.
6. Counter-probe at build (~09:37Z, head d52f2be7): 8/8 queries
   0 hits (frontier_m27, m27_z53, m28_z54, ladder_m19_z52,
   ladder_m25_z50, inband_m25_z41, inband_m26_z43, m27m28).

## S5. Handoff: kit-7 registrations (31 items, frozen in section (d))

All items below are paper-only K0832 closed-form pre-computations,
engine-free, derive_check double-checked and battery-asserted in the
frozen run (44 future triples in the battery). They are candidates to
be measured by the next kit, not measurements.

Ladder next rows (items 1-12: one-past of the fresh d=k birth =
death-of-d=k-1, then the next birth slice):

| # | row | registered candidate (binding for kit-7) |
|---|----|----|
| 1 | m=19 z=54 | EXACTLY ONE {19,36}@S=55 UP 1v0, v(55,54,74)=0; {19,34} conform-DEAD at z=54=S+1 (v(53,54,74)=1); death-of-d=7 |
| 2 | m=19 z=55 | EXACTLY TWO: stick {19,36} DOWN 1v2 + {19,38}@S=57 UP 2v0, v(57,55,75)=0; birth d=9, gap 19 |
| 3 | m=20 z=55 | EXACTLY ONE (20,36)@S=56 DOWN 0v1, v(56,55,76)=1; (20,34) conform-DEAD; death-of-d=7 |
| 4 | m=20 z=56 | EXACTLY TWO: stick + (20,38)@S=58 UP 2v1, v(58,56,77)=1; birth d=9, gap 18 |
| 5 | m=21 z=50 | EXACTLY ONE {21,30}@S=51 UP 1v0, v(51,50,74)=0; {21,28} conform-DEAD; death-of-d=3 |
| 6 | m=21 z=51 | EXACTLY TWO: stick + {21,32}@S=53 UP 2v0, v(53,51,75)=0; birth d=5, gap 11 |
| 7 | m=22 z=51 | EXACTLY ONE (22,30)@S=52 DOWN 0v1, v(52,51,76)=1; (22,28) conform-DEAD |
| 8 | m=22 z=52 | EXACTLY TWO: stick + (22,32)@S=54 UP 2v1, v(54,52,77)=1; birth d=5, gap 10 |
| 9 | m=23 z=52 | EXACTLY ONE {23,30}@S=53 UP 1v0, v(53,52,76)=0; {23,28} conform-DEAD |
| 10 | m=23 z=53 | EXACTLY TWO: stick + {23,32}@S=55 UP 2v0, v(55,53,77)=0; birth d=4, gap 9 |
| 11 | m=24 z=53 | EXACTLY ONE (24,30)@S=54 DOWN 0v1, v(54,53,78)=1; (24,28) conform-DEAD |
| 12 | m=24 z=54 | EXACTLY TWO: stick + (24,32)@S=56 UP 2v1, v(56,54,79)=1; birth d=4, gap 8 |

m=25 / m=26 post-mini-ladder rows (items 13-18, the CORRECTED
seat-lifecycle derivations; see S6 honest record):

| # | row | registered candidate |
|---|----|----|
| 13 | m=25 z=53 | EXACTLY TWO: stick {25,28} DOWN 1v2 (d=1 stick seat coincides, S=53=z) + {25,30}@S=55 UP 2v0, v(55,53,79)=0; birth d=2, gap 5 |
| 14 | m=25 z=54 | EXACTLY ONE {25,30}@S=55 UP 1v0, v(55,54,80)=0; {25,28} conform-DEAD at z=54=S+1 (v(53,54,80)=1); death-of-d=1 |
| 15 | m=25 z=55 | EXACTLY TWO: stick {25,30} DOWN 1v2 + {25,32}@S=57 UP 2v0, v(57,55,81)=0; birth d=3, gap 7 |
| 16 | m=26 z=54 | EXACTLY TWO: stick (26,28) DOWN 0v2 (d=1 stick seat coincides) + (26,30)@S=56 UP 2v1, v(56,54,81)=1; birth d=2, gap 4 |
| 17 | m=26 z=55 | EXACTLY ONE (26,30)@S=56 DOWN 0v1, v(56,55,82)=1; (26,28) conform-DEAD at z=55=S+1 (v(54,55,82)=0); death-of-d=1 |
| 18 | m=26 z=56 | EXACTLY TWO: stick + (26,32)@S=58 UP 2v1, v(58,56,83)=1; birth d=3, gap 6 |

m=27 / m=28 mini-ladder rows (items 19-24, first-ever):

| # | row | registered candidate |
|---|----|----|
| 19 | m=27 z=54 | EXACTLY ONE {27,28}@S=55 UP 1v0, v(55,54,82)=0; one-past of the d=0 seat |
| 20 | m=27 z=55 | EXACTLY TWO: stick {27,28} DOWN 1v2 (d=0 stick seat coincides, S=55=z) + {27,30}@S=57 UP 2v0, v(57,55,83)=0; birth d=1, gap 3 |
| 21 | m=27 z=56 | EXACTLY ONE {27,30}@S=57 UP 1v0, v(57,56,84)=0; {27,28} conform-DEAD at z=56=S+1 — the FIRST m=27 death datum candidate |
| 22 | m=28 z=55 | EXACTLY ONE (28,28)@S=56 DOWN 0v1, v(56,55,84)=1; one-past of the d=0 seat |
| 23 | m=28 z=56 | EXACTLY TWO: stick (28,28) DOWN 0v2 (d=0 stick seat coincides) + (28,30)@S=58 UP 2v1, v(58,56,85)=1; birth d=1, gap 2 |
| 24 | m=28 z=57 | EXACTLY ONE (28,30)@S=58 DOWN 0v1, v(58,57,86)=1; (28,28) conform-DEAD at z=57=S+1 — the FIRST m=28 death datum candidate |

Window sweep PROPOSALS (items 25-28; register before measuring;
strip-coverage re-probe required at kit-7 build time):

- 25: m=25 z in {33..40}, 0 separations each (candidate).
- 26: m=26 z in {35..42} (this RESOLVES the kit-5 label z=42 row),
  0 separations each.
- 27: m=27 z in {45..52} (= z*(27)-8..-1); m=27 is NOT strip-covered
  (z26-floor20 covers m in {20..26} only).
- 28: m=28 z in {46..53} (= z*(28)-8..-1); m=28 is NOT strip-covered.

Frontier 17th / 18th datum candidates (items 29-30, first-ever m=29
/ m=30 rows):

- 29: m=29 z=57, EXACTLY ONE {29,30}@S=59 UP 2v0, v(59,57,87)=0;
  z*(29)=2*29-2+1=57 per K1268, R=87.
- 30: m=30 z=58, EXACTLY ONE (30,30)@S=60 UP 2v1, v(60,58,89)=1;
  z*(30)=2*30-2+0=58, R=89.

NOT registered here (item 31): m=25 z in {27..32}, m=26 z in
{27..34} (scaffold extensions, register before measuring); m=27 z in
{25..44} and m=28 z in {25..45} (not strip-covered, unmeasured,
unregistered).

## S6. Honest record / caveats

- Build-time (pre-freeze) rejection: the first draft's kit-7
  registration constants for the m=25/m=26 post-mini-ladder rows had
  four collapse literals mis-derived from a seat-lifecycle offset
  slip; derive_check_kit6 caught all four BEFORE the freeze; the
  corrected machine derivations are the published ones. The 36
  measured candidates derive-checked PASS on the first attempt; no
  published artifact touched.
- Window label/list discrepancy (kit-5 S5 item (20)): label
  "z*(26)-8..-1" vs list 43..50. LIST binds (kit-4 precedent);
  z=50 executed as a blind re-verification (HIT, published value
  reproduced exactly); z=42 NOT registered (kit-7 proposal).
- m=27/m=28 are NOT strip-covered; their below-window z rows are not
  registered here.
- Counter-probe re-run at push time against then-current main;
  results in the push commit body.
- Finite machine observations against the pinned raw engine; no
  theorem, no universal claim; the 11x11 standard board, two-stone
  roots, S2, class 1/2/4, central-reply roots UNKNOWN, unchanged; no
  K slot claimed; future T-Z19..T-Z22 lanes own their band
  conventions.
