# 2026-11-26 m23/m24 frontier + below-window pre-declaration micro-kit (log)

Primary source timeline for `research/experiments/strip-newband-m23m24-frontier-belowwindow-20261126/`
(publish-then-execute). Predecessors: kit-1 in-band completions (`6057ed51`), kit-2 newband ladders
+ band-start (`637d15e1`, `research/log/2026-11-26-newband-ladders-bandstart-predecl-microkit.md`),
kit-3 m21/m22 frontier + ladders (`6554de44`, `research/log/2026-11-26-m21m22-frontier-ladders-predecl-microkit.md`).
Parallel activity at build time: the n11 sixth-cost lane batch-published commits
(`7fc6727e`..`0f2440c8`), unrelated to this lane's scope (verified by content probe).

## 2. Registered targets vs measured outcomes

| Target | Registered by | Candidate | Measured |
| --- | --- | --- | --- |
| m=19@z=48 one-past-of-d=5 / death-of-d=4 | kit-3 S5 item (1) | EXACTLY ONE {19,30}@49 UP 1v0; {19,28} conform-DEAD | **HIT** |
| m=19@z=49 birth d=6 | kit-3 S5 item (2) | EXACTLY TWO: stick 1v2 + {19,32}@51 UP 2v0 gap 13 | **HIT** |
| m=20@z=49 one-past-of-d=5 / death-of-d=4 | kit-3 S5 item (3) | EXACTLY ONE (20,30)@50 DOWN 0v1; (20,28) conform-DEAD | **HIT** |
| m=20@z=50 birth d=6 | kit-3 S5 item (4) | EXACTLY TWO: stick 0v2 + (20,32)@52 UP 2v1 gap 12 | **HIT** |
| m=21@z=44 one-past-of-d=1 / death-of-d=0 | kit-3 S5 item (5) | EXACTLY ONE {21,24}@45 UP 1v0; {21,22} conform-DEAD | **HIT** (first m=21 death) |
| m=21@z=45 birth d=2 | kit-3 S5 item (6) | EXACTLY TWO: stick 1v2 + {21,26}@47 UP 2v0 gap 5 | **HIT** |
| m=22@z=45 one-past-of-d=1 / death-of-d=0 | kit-3 S5 item (7) | EXACTLY ONE (22,24)@46 DOWN 0v1; (22,22) conform-DEAD | **HIT** (first m=22 death) |
| m=22@z=46 birth d=2 | kit-3 S5 item (8) | EXACTLY TWO: stick 0v2 + (22,26)@48 UP 2v1 gap 4 | **HIT** |
| m=23@z=44 (misregistered frontier slice) | kit-3 S5 item (9) | 0 separations (corrected expectation; registered EXACTLY ONE VOIDED by the z*(23) slip) | **HIT** (clean) |
| m=23@z=45 CORRECTED frontier (11th datum) | this kit (erratum discharge, pre-freeze) | EXACTLY ONE {23,24}@47 UP 2v0 (v(47,45,69)=0) | **HIT** |
| m=24@z=46 frontier (12th datum) | kit-3 S5 item (9), arithmetic verified | EXACTLY ONE (24,24)@48 UP 2v1 (v(48,46,71)=1) | **HIT** |
| m=23@z=46 / z=47 mini-ladder | this kit (same-kit, kit-1 precedent) | EXACTLY ONE 1v0 / TWO stick 1v2 + {23,26}@49 UP 2v0 gap 3 | **HIT** (2/2) |
| m=24@z=47 / z=48 / z=49 mini-ladder | this kit (same-kit); z=49 candidate corrected by build check pre-freeze | EXACTLY ONE 0v1 / TWO stick 0v2 + (24,26)@50 UP 2v1 gap 2 / ONE (24,26)@50 DOWN 0v1 with (24,24) conform-DEAD | **HIT** (3/3, first m=24 death witnessed at z=49=S+1) |
| m=21 below-window z∈{27..32} (6 rows) | kit-3 S5 item (10), strip re-probed | 0 separations each | **HIT** (19 shapes each) |
| m=22 below-window z∈{27..33} (7 rows) | kit-3 S5 item (10), strip re-probed | 0 separations each | **HIT** (18 shapes each) |

Erratum record (disclosed FIRST in the frozen docstring, before any run): kit-3 S5 item (9) wrote
"z*(23)=2*23-2+1=44" — the K1268 formula z*(m)=2m-2+(m mod 2) evaluates to 45 for m=23. Discharge
protocol: measure the misregistered m=23@z=44 as registered (candidate corrected to 0 separations
per the frontier-minus-one precedent, the EXACTLY ONE prediction voided, not re-asserted) AND
register the corrected frontier m=23@z=45 kit-added in the same run. Both hit as corrected. The
registered collapse constants inside item (9) carried the slip only in the z-index; every
per-slice collapse value used here was re-derived from K1268 at this build and battery-checked.

## 3. Scaffold status after this kit (finite observations, candidate status)

- **Parity frontier law: 12/12 through m=24** (11th: m=23@z=45 {23,24}@S=47 UP 2v0; 12th:
  m=24@z=46 (24,24)@S=48 UP 2v1; both EXACT, first-ever m=23/m=24 rows). The m=13..23
  frontier-minus-one rows are all published clean (m=23 contribution: the erratum row z=44).
  Registered next: m=25@z=49 and m=26@z=50 — the 13th/14th datum candidates (below).
- m=19/m=20 ladders COMPLETE through d=6 birth (7 birth seats each): m=19 births z37..49,
  m=20 births z38..50; deaths now witnessed for d in {0..4} of each (4 new: m19 d=4@z48,
  m20 d=4@z49 here plus the kit-3 d=2/3 set); class counts: one-past decays odd 2->1 now 23
  observations, even 2->0 now 23; sticks +3 odd (m19@z49, m21@z45, m23@z47) +3 even
  (m20@z50, m22@z46, m24@z48); deaths +5 datums here (m19 d=4, m20 d=4, m21 d=0, m22 d=0,
  m24 d=0). The death-class machinery (conform-at-birth+3, value = collapse from then on)
  held at every datum so far.
- m=23/m=24: frontier + one-past + d=1 birth slices measured (17 / 16 shapes per row);
  m=24 d=0 death witnessed; m=23 d=0 death is the first REGISTERED m=23 death candidate
  (m=23@z=48, below).
- Measured in-band coverage: m=21 z∈{25..40} (25/26 strip-derived), m=22 z∈{25..41};
  m=19 z∈{25..36}(+ strip to 21), m=20 z∈{27..37}(+ strip). The m=23/m=24 windows are
  registered below.

## 4. Verification

- K0832 battery: 297/297 closed == canonical == ordered (all literals incl. S5 registrations).
- Anchors: 72/72 exact (52 kit-3 + 20 kit-3 separation spots `6554de44`, roles in the frozen
  output `published_anchor_rechecks`).
- Determinism: 7 runs byte-identical (frozen + default ×2 + PYTHONHASHSEED=random + env -i
  isolated ×2 + push-time rerun), rc 0, ~15 s/run. Frozen output sha256
  `4d433267b88791e322c34861b4e981f372be2a07af5ec45f7c1e483160f2dda3`.
- Ordered-engine audit (outside the frozen artifact): 29/29 rows separation-value-exact
  (530 shapes), anchors 72/72.
- Counter-probe at build (~09:12Z, head `6554de44`, this kit's predecessor): all kit-specific
  content queries return 0 measurement records (docstring); re-run at push time against
  then-current main (head `0f2440c8`): target paths absent on main, only n11-lane commits
  after kit-3.
- Frozen-file typo disclosures (frozen files NOT edited): docstring paragraph 1 reads
  "11th / 10th" where the intent (and kit-3 S5 item (9) itself) is 11th (m=23) / 12th (m=24);
  the future-slice section's m=23 window label reads "z*(23)-8..-1" while listing rows
  z∈{36..43} — the listed rows are the binding proposal.

## 5. Handoff / registered items for the next execution (binding constants, engine-free)

All constants K0832 paper derivations, battery-checked in the frozen section (f):

1. m=19@z=50 (one-past-of-d=6 / death-of-d=5): EXACTLY ONE {19,32}@S=51 UP 1v0 (collapse
   v(51,50,70)=0); {19,30} conform-DEAD at z=50=S+1 (collapse v(49,50,70)=1).
2. m=19@z=51 (birth d=7): EXACTLY TWO: stick {19,32} DOWN 1v2 (v(51,51,71)=2) + NEW
   {19,34}@S=53 UP 2v0 (v(53,51,71)=0), d=7 seat gap 15.
3. m=20@z=51 (one-past-of-d=6 / death-of-d=5): EXACTLY ONE (20,32)@S=52 DOWN 0v1
   (v(52,51,72)=1); (20,30) conform-DEAD at z=51=S+1 (v(50,51,72)=0).
4. m=20@z=52 (birth d=7): EXACTLY TWO: stick (20,32) DOWN 0v2 (v(52,52,73)=2) + NEW
   (20,34)@S=54 UP 2v1 (v(54,52,73)=1), seat gap 14.
5. m=21@z=46 (one-past-of-d=2 / death-of-d=1): EXACTLY ONE {21,26}@S=47 UP 1v0
   (v(47,46,68)=0); {21,24} conform-DEAD at z=46=S+1 (v(45,46,68)=1).
6. m=21@z=47 (birth d=3): EXACTLY TWO: stick {21,26} DOWN 1v2 (v(47,47,69)=2) + NEW
   {21,28}@S=49 UP 2v0 (v(49,47,69)=0), seat gap 7.
7. m=22@z=47 (one-past-of-d=2 / death-of-d=1): EXACTLY ONE (22,26)@S=48 DOWN 0v1
   (v(48,47,68)=1); (22,24) conform-DEAD at z=47=S+1 (v(46,47,68)=0).
8. m=22@z=48 (birth d=3): EXACTLY TWO: stick (22,26) DOWN 0v2 (v(48,48,69)=2) + NEW
   (22,28)@S=50 UP 2v1 (v(50,48,69)=1), seat gap 6.
9. m=23@z=48 (one-past-of-d=1 / death-of-d=0 — the FIRST m=23 death datum candidate):
   EXACTLY ONE {23,26}@S=49 UP 1v0 (v(49,48,72)=0); {23,24} conform-DEAD at z=48=S+1
   (v(47,48,72)=1).
10. m=23@z=49 (birth d=2): EXACTLY TWO: stick {23,26} DOWN 1v2 (v(49,49,73)=2) + NEW
    {23,28}@S=51 UP 2v0 (v(51,49,73)=0), seat gap 5.
11. m=24@z=50 (birth d=2, stick coincides S(d1)=50=z): EXACTLY TWO: stick (24,26)@S=50
    DOWN 0v2 (v(50,50,75)=2) + NEW (24,28)@S=52 UP 2v1 (v(52,50,75)=1), seat gap 4.
12. Frontier proposals (13th/14th datum candidates, FIRST-EVER m=25/m=26 rows):
    m=25@z=49 (z*(25)=2*25-2+1=49, arithmetic double-checked at this build; R=75):
    EXACTLY ONE {25,26}@S=51 UP 2v0 (collapse v(51,49,75)=0); m=26@z=50 (z*(26)=2*26-2+0=50;
    R=77): EXACTLY ONE (26,26)@S=52 UP 2v1 (collapse v(52,50,77)=1).
13. In-band window sweep proposals: m=23 z∈{36..43} (8 rows) and m=24 z∈{38..45} (8 rows),
    candidates 0 separations each; STRIP-COVERAGE RE-PROBE REQUIRED at build time before
    measuring (no z=36..45 census kit exists today; the z=26 heavy-lane future extensions
    and any parallel run must be probed against). The below-window rows m=23 z∈{27..35},
    m=24 z∈{27..37} are NOT registered here; they are derivable scaffold extensions —
    register fully before measuring per protocol.
14. NOT taken by this lane (other lanes' items — do not touch): the wave-lane S5 items
    (m=17/m=18 past-side z∈{37..41} rows, the z=33 touch quad, k45/k46 supply constants),
    the z=26 floor-21 heavy census lane, the n11 sixth-cost lane batches. 11×11 verdicts
    UNKNOWN; no K slot claimed.
15. Parallel-run coordination: if a parallel hourly run has already executed any items 1-13
    when this is read, treat as blind replication or pivot; re-fetch the latest main before
    any push and record conflicts without forcing.

## 6. Caveats

Finite machine observations against the pinned raw engine only; no theorem, no universal
claim; the 23/23 decay-class counts are observation counts over published + this kit's data,
not laws; the quadratic shape-count pattern stays refuted (m=21:19, m=22:18, m=23:17,
m=24:16 measured); the z*(23) registration slip is discharged and documented above, and no
quantity depending on it survives elsewhere; standard 11×11 empty board, two-stone roots,
S2, class 1/2/4 and all central-reply roots: all UNKNOWN, unchanged; no verdict consumed.
