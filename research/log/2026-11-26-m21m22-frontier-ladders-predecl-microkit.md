# 2026-11-26 m21/m22 frontier + newband ladder continuation pre-declaration micro-kit (log)

Primary source timeline for `research/experiments/strip-newband-m21m22-frontier-ladders-20261126/`
(publish-then-execute). Predecessors: kit-1 in-band completions (`6057ed51`), kit-2 newband
ladders + band-start (`637d15e1`, `research/log/2026-11-26-newband-ladders-bandstart-predecl-microkit.md`).
Parallel activity at build time: the n11 sixth-cost lane batch-published 5+ commits
(`71bf3e01`..), unrelated to this lane's scope (verified by content probe).

## 2. Registered targets vs measured outcomes

| Target | Registered by | Candidate | Measured |
| --- | --- | --- | --- |
| m=19@z=44 one-past-of-d=3 / death-of-d=2 | kit-2 S5 item (1) | EXACTLY ONE {19,26}@45 UP 1v0; {19,24} conform-DEAD | **HIT** |
| m=19@z=45 birth d=4 | kit-2 S5 item (2) | EXACTLY TWO: stick 1v2 + {19,28}@47 UP 2v0 gap 9 | **HIT** |
| m=20@z=45 one-past-of-d=3 / death-of-d=2 | kit-2 S5 item (3) | EXACTLY ONE (20,26)@46 DOWN 0v1; (20,24) conform-DEAD | **HIT** |
| m=20@z=46 birth d=4 | kit-2 S5 item (4) | EXACTLY TWO: stick 0v2 + (20,28)@48 UP 2v1 gap 8 | **HIT** |
| m=21@z=41 frontier (FIRST-EVER m=21 row) | kit-2 S5 item (5) | EXACTLY ONE {21,22}@43 UP 2v0 (v(43,41,63)=0) | **HIT** |
| m=22@z=42 frontier (FIRST-EVER m=22 row) | kit-2 S5 item (5) | EXACTLY ONE (22,22)@44 UP 2v1 (v(44,42,65)=1) | **HIT** |
| m=21 in-band z∈{33..40} (8 rows) | kit-2 S5 item (5) | 0 separations each | **HIT** (19 shapes each) |
| m=22 in-band z∈{34..41} (8 rows) | kit-2 S5 item (5) | 0 separations each | **HIT** (18 shapes each) |
| m=19@z=46/z=47, m=20@z=47/z=48 ladder | this kit (same-kit, kit-1 precedent) | EXACTLY ONE / TWO per scaffold | **HIT** (4/4) |
| m=21@z=42/z=43, m=22@z=43/z=44 mini-ladder | this kit (same-kit) | EXACTLY ONE / TWO per scaffold | **HIT** (4/4) |

Recorded deviation (non-binding guess, disclosed): the kit-2 S5 registration guessed 20 shapes
for the m=21 row by the m19/m20 quadratic pattern; measured counts are 19 (m=21) and 18
(m=22). Counts are measured at run time per series convention; the quadratic extrapolation is
refuted for m=21/m=22 and is NOT used anywhere as a candidate constant.

## 3. Scaffold status after this kit (finite observations, candidate status)

- **Parity frontier law: 10/10 through m=22** (9th: m=21@z=41 {21,22}@S=43 UP 2v0; 10th:
  m=22@z=42 (22,22)@S=44 UP 2v1; both EXACT). Registered next: m=23@z=44 {23,24}@S=47 UP 2v0
  (collapse v(47,44,68)=0, R=68), m=24@z=46 (24,24)@S=48 UP 2v1 (collapse
  v(48,46,71)=1, R=71) — the 11th/12th datum candidates.
- m=19/m=20 ladders COMPLETE through d=5 birth (6 birth seats each): births z37..47 / z38..48;
  one-past decays class counts: odd 2->1 now 20 observations, even 2->0 now 19; sticks +2
  odd (m19@z45, z47) +2 even (m20@z46, z48) +1 each for m=21/m=22 (z43/z44); deaths: 4 new
  datums (m19 d=2@z44, d=3@z46; m20 d=2@z45, d=3@z47) — the death class is now observed for
  d in {0..3} of m=19/m=20 and the class machinery (conform-at-birth+3, value = stuck parity
  value) held at every datum so far.
- m=21/m=22 in-band windows measured clean: m=21 z∈{33..40}, m=22 z∈{34..41} (z*-8..z*-1);
  below-window z∈{25,26} strip-derived clean; z∈{27..32} (m=21) / {27..33} (m=22) registered
  for the next execution.

## 4. Verification

- K0832 battery: 274/274 closed == canonical == ordered (all literals incl. S5 registrations).
- Anchors: 52/52 exact (40 kit-2 + 12 kit-2 ladder separation spots `637d15e1`).
- Determinism: 6 runs byte-identical (frozen + default ×2 + PYTHONHASHSEED=random + env -i
  isolated ×2), rc 0, ~16 s/run. Frozen output sha256
  `c4ef061023ead9dec65be335a82e418c88463b1767c7468921455a005aed5d63`.
- Ordered-engine audit (outside the frozen artifact): 30/30 rows separation-value-exact
  (575 shapes), anchors 52/52.
- Counter-probe at build (~08:57Z, head `7fc6727e`): all kit-specific section ids return 0
  measurement records; re-run at push time against then-current main.

## 5. Handoff / registered items for the next execution (binding constants, engine-free)

All constants K0832 paper derivations, battery-checked in the frozen section (f):

1. m=19@z=48 (one-past-of-d=5 / death-of-d=4): EXACTLY ONE {19,30}@S=49 UP 1v0 (collapse
   v(49,48,68)=0); {19,28} conform-DEAD (v(47,48,68)=1).
2. m=19@z=49 (birth d=6): EXACTLY TWO: stick {19,30} DOWN 1v2 (v(49,49,69)=2) + NEW
   {19,32}@S=51 UP 2v0 (v(51,49,69)=0), seat gap 13.
3. m=20@z=49 (one-past-of-d=5 / death-of-d=4): EXACTLY ONE (20,30)@S=50 DOWN 0v1
   (v(50,49,70)=1); (20,28) conform-DEAD (v(48,49,70)=0).
4. m=20@z=50 (birth d=6): EXACTLY TWO: stick (20,30) DOWN 0v2 (v(50,50,71)=2) + NEW
   (20,32)@S=52 UP 2v1 (v(52,50,71)=1), seat gap 12.
5. m=21@z=44 (one-past-of-d=1 / death-of-d=0 — the FIRST m=21 death datum): EXACTLY ONE
   {21,24}@S=45 UP 1v0 (v(45,44,66)=0); {21,22} conform-DEAD (v(43,44,66)=1).
6. m=21@z=45 (birth d=2): EXACTLY TWO: stick {21,24} DOWN 1v2 (v(45,45,67)=2) + NEW
   {21,26}@S=47 UP 2v0 (v(47,45,67)=0), seat gap 5.
7. m=22@z=45 (one-past-of-d=1 / death-of-d=0 — the FIRST m=22 death datum): EXACTLY ONE
   (22,24)@S=46 DOWN 0v1 (v(46,45,68)=1); (22,22) conform-DEAD (v(44,45,68)=0).
8. m=22@z=46 (birth d=2): EXACTLY TWO: stick (22,24) DOWN 0v2 (v(46,46,69)=2) + NEW
   (22,26)@S=48 UP 2v1 (v(48,46,69)=1), seat gap 4.
9. Frontier proposals (11th/12th datum candidates): m=23@z=44 (z*(23)=44, R=68):
   EXACTLY ONE {23,24}@S=47 UP 2v0 (collapse v(47,44,68)=0); m=24@z=46 (z*(24)=46, R=71):
   EXACTLY ONE (24,24)@S=48 UP 2v1 (collapse v(48,46,71)=1); plus the kit-added-style
   one-past/d=1-birth mini-ladders derivable from the scaffold (register fully before
   measuring per protocol).
10. Below-window band-start proposals: m=21 z∈{27..32} (6 rows), m=22 z∈{27..33} (7 rows),
    candidates 0 separations; the z∈{25,26} equivalents are strip-derived clean
    (z25-min20 strips m∈{20..25}, z26-floor20 m∈{20..26}); re-probe strip coverage at build
    time before measuring.
11. NOT taken by this lane (other lanes' items — do not touch): the wave-lane S5 items
    (m=17/m=18 past-side z∈{37..41} rows, the z=33 touch quad, k45/k46 supply constants),
    the z=26 floor-21 heavy census lane, the n11 sixth-cost lane batches. 11×11 verdicts
    UNKNOWN; no K slot claimed.
12. Parallel-run coordination: if a parallel hourly run has already executed any items 1-10
    when this is read, treat as blind replication or pivot; re-fetch the latest main before
    any push and record conflicts without forcing.

## 6. Caveats

Finite machine observations against the pinned raw engine only; no theorem, no universal
claim; the 20/19/10-count class statements are observation counts over published + this
kit's data, not laws; the quadratic shape-count guess for m=21/m=22 is refuted and recorded;
standard 11×11 empty board, two-stone roots, S2, class 1/2/4 and all central-reply roots:
all UNKNOWN, unchanged; no verdict consumed.
