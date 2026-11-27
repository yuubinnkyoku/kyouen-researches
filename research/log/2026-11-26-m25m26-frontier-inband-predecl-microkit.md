# 2026-11-26 m25/m26 frontier + m23/m24 in-band pre-declaration micro-kit (log)

Primary source timeline for `research/experiments/strip-newband-m25m26-frontier-inband-20261126/`
(publish-then-execute). Predecessors: kit-3 m21/m22 frontier + ladders (`6554de44`), kit-4 m23/m24
frontier + below-window (`fe0a2d01`, `research/log/2026-11-26-m23m24-frontier-belowwindow-predecl-microkit.md`).
Parallel activity at build time: none observed — main HEAD stayed `fe0a2d01` from ~09:09Z through push time
(re-probed; no sixthwave/z26/n11 commits in the window).

## 2. Registered targets vs measured outcomes

| Target | Registered by | Candidate | Measured |
| --- | --- | --- | --- |
| m=19@z=50 one-past-of-d=6 / death-of-d=5 | kit-4 S5 item (1) | EXACTLY ONE {19,32}@51 UP 1v0; {19,30} conform-DEAD | **HIT** (first m=19 d=5 death) |
| m=19@z=51 birth d=7 | kit-4 S5 item (2) | EXACTLY TWO: stick 1v2 + {19,34}@53 UP 2v0 gap 15 | **HIT** (m=19 ladder COMPLETE d=7) |
| m=20@z=51 one-past-of-d=6 / death-of-d=5 | kit-4 S5 item (3) | EXACTLY ONE (20,32)@52 DOWN 0v1; (20,30) conform-DEAD | **HIT** (first m=20 d=5 death) |
| m=20@z=52 birth d=7 | kit-4 S5 item (4) | EXACTLY TWO: stick 0v2 + (20,34)@54 UP 2v1 gap 14 | **HIT** (m=20 ladder COMPLETE d=7) |
| m=21@z=46 one-past-of-d=2 / death-of-d=1 | kit-4 S5 item (5) | EXACTLY ONE {21,26}@47 UP 1v0; {21,24} conform-DEAD | **HIT** (first m=21 d=1 death) |
| m=21@z=47 birth d=3 | kit-4 S5 item (6) | EXACTLY TWO: stick 1v2 + {21,28}@49 UP 2v0 gap 7 | **HIT** |
| m=22@z=47 one-past-of-d=2 / death-of-d=1 | kit-4 S5 item (7), R-corrected annotations | EXACTLY ONE (22,26)@48 DOWN 0v1; (22,24) conform-DEAD | **HIT** (first m=22 d=1 death) |
| m=22@z=48 birth d=3 | kit-4 S5 item (8), R-corrected annotations | EXACTLY TWO: stick 0v2 + (22,28)@50 UP 2v1 gap 6 | **HIT** |
| m=23@z=48 one-past-of-d=1 / death-of-d=0 | kit-4 S5 item (9) | EXACTLY ONE {23,26}@49 UP 1v0; {23,24} conform-DEAD | **HIT** (THE FIRST m=23 death datum) |
| m=23@z=49 birth d=2 | kit-4 S5 item (10) | EXACTLY TWO: stick 1v2 + {23,28}@51 UP 2v0 gap 5 | **HIT** |
| m=24@z=50 birth d=2 (stick coincides S(d1)=50=z) | kit-4 S5 item (11) | EXACTLY TWO: stick (24,26)@50 0v2 + (24,28)@52 UP 2v1 gap 4 | **HIT** |
| m=25@z=49 frontier (13th datum) | kit-4 S5 item (12) | EXACTLY ONE {25,26}@51 UP 2v0 (v(51,49,75)=0) | **HIT** |
| m=26@z=50 frontier (14th datum) | kit-4 S5 item (12) | EXACTLY ONE (26,26)@52 UP 2v1 (v(52,50,77)=1) | **HIT** |
| m=23 in-band z∈{36..43} (8 rows) | kit-4 S5 item (13), strip re-probed | 0 separations each | **HIT** (17 shapes each, R=60..67) |
| m=24 in-band z∈{38..45} (8 rows) | kit-4 S5 item (13), strip re-probed | 0 separations each | **HIT** (16 shapes each, R=63..70) |

Erratum records (both disclosed FIRST in the frozen docstring, before the published run):

- kit-4 frozen section (f) R-ANNOTATION slip (carried disclosure, dated correction at this build): items
  (7)/(8) quoted collapses v(48,47,68)=1 / v(46,47,68)=0 / v(48,48,69)=2 / v(50,48,69)=1 where the
  mechanical R=m+z+1 gives R=70/70/71/71. The collapse VALUES coincide in both annotation windows
  (parity-constant closed form), so no prediction changed; this kit quotes corrected annotations and
  battery-checks BOTH triples. Kit-4 published bytes NOT edited (series convention).
- THIS BUILD's anchor-table splice fix (no published artifact affected): the 21 kit-4 separation spots
  were first assembled into anchor_spec with the seat S in the R slot (kit-era anchor entries are
  R-first; the kit-4 extraction produced S-first 5-tuples). An internal pre-publication check run
  (`explore_m25m26_frontier.out.run1`, kept locally, NOT a datum) surfaced exactly 15 false-conform
  mismatches, all kit-4-entry spots. The 21 first fields were corrected to R=m+z+1 and pre-verified
  21/21 exact against the published values. The 29 measurement sections are byte-identical between
  that internal run and the published run, demonstrating no candidate/engine/measurement change.

## 3. Scaffold status after this kit (finite observations, candidate status)

- **Parity frontier law: 14/14 through m=26** (13th: m=25@z=49 {25,26}@S=51 UP 2v0; 14th: m=26@z=50
  (26,26)@S=52 UP 2v1; both EXACT, the first-ever m=25/m=26 rows). Registered next: m=27@z=53 and
  m=28@z=54 — the 15th/16th datum candidates (below). Frontier-minus-one rows stay published clean for
  m=13..24; m=25 z=48 (frontier-minus-one candidate) is included in the m=25 window sweep below.
- m=19/m=20 ladders COMPLETE through the d=7 birth (8 birth seats each: m=19 births z37..51, m=20
  births z38..52); deaths witnessed for d in {0..5} of each. m=21/m=22 through d=3 (deaths d in {0,1});
  m=23 through d=2 (death d=0, witnessed here — the first m=23 death); m=24 through d=2 (death d=0,
  kit-4).
- Class counts (cumulative observation counts): one-past decays odd 2->1 now 26, even 2->0 now 25;
  sticks +3 odd +3 even this kit; deaths +5 this kit (m19 d5, m20 d5, m21 d1, m22 d1, m23 d0). The
  death-class machinery (conform-at-birth+3, value = collapse from then on) held at every datum so far.
- Measured in-band coverage: m=23 z∈{25,26} strip-derived + z∈{36..49} contiguous; m=24 z∈{25,26}
  strip + z∈{38..50} contiguous; m=21 z∈{25..47}, m=22 z∈{25..48} with the kit-3/kit-4 ladder rows.
  Below-window m=25 z∈{27..40}, m=26 z∈{27..42} remain unregistered (derivable scaffold extensions).
- Shapes per row (measured): m=19:22, m=20:20, m=21:19, m=22:18, m=23:17, m=24:16, m=25:15, m=26:14;
  the quadratic shape-count guess stays refuted (not used).

## 4. Verification

- K0832 battery: 331/331 closed == canonical == ordered (all registration literals + BOTH R-annotation
  triples of the kit-4 slip on record).
- Anchors: 93/93 exact (72 kit-era + 21 kit-4 separation spots, first re-anchored here, values verbatim
  from the kit-4 published output; corrected R=m+z+1 slots, 21/21 pre-verified before the published run).
- Candidate-vs-measured hit check: 29/29 rows reproduce the frozen candidates exactly (EXACTLY ONE/TWO
  sets, values, collapses, conform-DEAD seats).
- Determinism: published run + default ×2 + PYTHONHASHSEED=random + env -i isolated ×2 all
  byte-identical, rc 0, ~18 s/run. Frozen output sha256
  `9d32f5fcd5cfb1209868e2e3773704d47b59e45a92829e047f807b7e769fd9fb`.
- Ordered-engine audit (outside the frozen artifact): 29/29 rows separation-value-exact (501 shapes),
  anchors 93/93.
- Derivation check (build, engine-free): 60 constants machine-derived from K0832 and double-asserted,
  incl. z*(25)=49, z*(26)=50, z*(27)=53, z*(28)=54.
- Internal-run equality: the 29 measurement sections of the pre-fix internal run and of the published
  run are byte-identical (29/29).
- Counter-probe at build (~09:15Z, head `fe0a2d01`): all kit-specific content queries 0 hits; re-run at
  push time (head `fe0a2d01`, unchanged): 8/8 queries 0 hits, no new commits after kit-4.

## 5. Handoff / registered items for the next execution (binding constants, engine-free)

All constants K0832 paper derivations, battery-checked in the frozen section (f):

1. m=19@z=52 (one-past-of-d=7 / death-of-d=6): EXACTLY ONE {19,34}@S=53 UP 1v0 (collapse
   v(53,52,72)=0); {19,32} conform-DEAD at z=52=S+1 (collapse v(51,52,72)=1).
2. m=19@z=53 (birth d=8): EXACTLY TWO: stick {19,34} DOWN 1v2 (v(53,53,73)=2) + NEW {19,36}@S=55
   UP 2v0 (v(55,53,73)=0), d=8 seat gap 17.
3. m=20@z=53 (one-past-of-d=7 / death-of-d=6): EXACTLY ONE (20,34)@S=54 DOWN 0v1 (v(54,53,74)=1);
   (20,32) conform-DEAD at z=53=S+1 (v(52,53,74)=0).
4. m=20@z=54 (birth d=8): EXACTLY TWO: stick (20,34) DOWN 0v2 (v(54,54,75)=2) + NEW (20,36)@S=56
   UP 2v1 (v(56,54,75)=1), seat gap 16.
5. m=21@z=48 (one-past-of-d=3 / death-of-d=2): EXACTLY ONE {21,28}@S=49 UP 1v0 (v(49,48,70)=0);
   {21,26} conform-DEAD at z=48=S+1 (v(47,48,70)=1).
6. m=21@z=49 (birth d=4): EXACTLY TWO: stick {21,28} DOWN 1v2 (v(49,49,71)=2) + NEW {21,30}@S=51
   UP 2v0 (v(51,49,71)=0), seat gap 9.
7. m=22@z=49 (one-past-of-d=3 / death-of-d=2): EXACTLY ONE (22,28)@S=50 DOWN 0v1 (v(50,49,72)=1);
   (22,26) conform-DEAD at z=49=S+1 (v(48,49,72)=0).
8. m=22@z=50 (birth d=4): EXACTLY TWO: stick (22,28) DOWN 0v2 (v(50,50,73)=2) + NEW (22,30)@S=52
   UP 2v1 (v(52,50,73)=1), seat gap 8.
9. m=23@z=50 (one-past-of-d=2 / death-of-d=1): EXACTLY ONE {23,28}@S=51 UP 1v0 (v(51,50,74)=0);
   {23,26} conform-DEAD at z=50=S+1 (v(49,50,74)=1).
10. m=23@z=51 (birth d=3): EXACTLY TWO: stick {23,28} DOWN 1v2 (v(51,51,75)=2) + NEW {23,30}@S=53
    UP 2v0 (v(53,51,75)=0), seat gap 7.
11. m=24@z=51 (one-past-of-d=2 / death-of-d=1): EXACTLY ONE (24,28)@S=52 DOWN 0v1 (v(52,51,76)=1);
    (24,26) conform-DEAD at z=51=S+1 (v(50,51,76)=0).
12. m=24@z=52 (birth d=3): EXACTLY TWO: stick (24,28) DOWN 0v2 (v(52,52,77)=2) + NEW (24,30)@S=54
    UP 2v1 (v(54,52,77)=1), seat gap 6.
13. m=25@z=50 (one-past of the d=0 seat): EXACTLY ONE {25,26}@S=51 UP 1v0 (v(51,50,76)=0).
14. m=25@z=51 (birth d=1, stick coincides S(d0)=51=z): EXACTLY TWO: stick {25,26} DOWN 1v2
    (v(51,51,77)=2) + NEW {25,28}@S=53 UP 2v0 (v(53,51,77)=0), seat gap 3.
15. m=25@z=52 (one-past-of-d=1 / death-of-d=0 — the FIRST m=25 death datum candidate): EXACTLY ONE
    {25,28}@S=53 UP 1v0 (v(53,52,78)=0); {25,26} conform-DEAD at z=52=S+1 (v(51,52,78)=1).
16. m=26@z=51 (one-past of the d=0 seat): EXACTLY ONE (26,26)@S=52 DOWN 0v1 (v(52,51,78)=1).
17. m=26@z=52 (birth d=1, stick coincides S(d0)=52=z): EXACTLY TWO: stick (26,26) DOWN 0v2
    (v(52,52,79)=2) + NEW (26,28)@S=54 UP 2v1 (v(54,52,79)=1), seat gap 2.
18. m=26@z=53 (one-past-of-d=1 / death-of-d=0 — the FIRST m=26 death datum candidate): EXACTLY ONE
    (26,28)@S=54 DOWN 0v1 (v(54,53,80)=1); (26,26) conform-DEAD at z=53=S+1 (v(52,53,80)=0).
19. In-band window sweep proposals: m=25 z∈{41..48} (8 rows; the z=48 row is the frontier-minus-one
    precedent candidate — measured clean for m=13..24 one-below the frontier) and m=26 z∈{43..50}
    (8 rows); candidates 0 separations each; STRIP-COVERAGE RE-PROBE REQUIRED at build time before
    measuring (the z26-floor20 strips cover m∈{20..26} at z=25/26 only).
20. Frontier proposals (15th/16th datum candidates, FIRST-EVER m=27/m=28 rows): m=27@z=53
    (z*(27)=2*27-2+1=53, arithmetic double-checked at this build; R=81): EXACTLY ONE {27,28}@S=55
    UP 2v0 (collapse v(55,53,81)=0); m=28@z=54 (z*(28)=2*28-2+0=54; R=83): EXACTLY ONE (28,28)@S=56
    UP 2v1 (collapse v(56,54,83)=1).
21. NOT taken by this lane (other lanes' items — do not touch): the wave-lane S5 items (m=17/m=18
    past-side rows, k45/k46 supply constants), the z=26 floor-21 heavy census lane, the n11 sixth-cost
    lane batches. 11×11 verdicts UNKNOWN; no K slot claimed. The below-window rows m=25 z∈{27..40},
    m=26 z∈{27..42} are NOT registered here (derivable scaffold extensions — register fully before
    measuring per protocol).
22. Parallel-run coordination: if a parallel hourly run has already executed any items 1-20 when this
    is read, treat as blind replication or pivot; re-fetch the latest main before any push and record
    conflicts without forcing.

## 6. Caveats

Finite machine observations against the pinned raw engine only; no theorem, no universal claim; the
26/25 decay-class counts are observation counts over published + this kit's data, not laws; the
quadratic shape-count pattern stays refuted (m=19:22, m=20:20, m=21:19, m=22:18, m=23:17, m=24:16,
m=25:15, m=26:14 measured); the two erratum/build-fix disclosures are documented above and no
quantity depending on them survives elsewhere; standard 11×11 empty board, two-stone roots, S2,
class 1/2/4 and all central-reply roots: all UNKNOWN, unchanged; no verdict consumed.
