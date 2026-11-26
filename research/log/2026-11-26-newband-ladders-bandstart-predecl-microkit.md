# 2026-11-26 newband ladders + band-start pinning pre-declaration micro-kit (log)

Primary source timeline for `research/experiments/strip-newband-ladders-bandstart-20261126/`
(publish-then-execute). Predecessor: kit-1 in-band completions kit (commit `6057ed51`,
`research/log/2026-11-26-inband-completions-m19m20-newbands-predecl-microkit.md`).

## 2. Registered targets vs measured outcomes

| Target | Registered by | Candidate | Measured |
| --- | --- | --- | --- |
| m=19@z=40 one-past-of-d=1 / death-of-d=0 | kit-1 S5 item (1) + frozen (g) | EXACTLY ONE {19,22}@S=41 UP 1v0; {19,20} conform-DEAD | **HIT** (22 shapes, 1 sep exactly as declared) |
| m=19@z=41 birth slice d=2 | kit-1 S5 item (2) | EXACTLY TWO: stick 1v2 + birth {19,24} UP 2v0 gap 5 | **HIT** |
| m=20@z=41 one-past-of-d=1 / death-of-d=0 | kit-1 S5 item (3) | EXACTLY ONE (20,22) DOWN 0v1; (20,20) conform-DEAD | **HIT** |
| m=20@z=42 birth slice d=2 | kit-1 S5 item (4) | EXACTLY TWO: stick 0v2 + birth (20,24) UP 2v1 gap 4 | **HIT** |
| m=19@z=42 one-past-of-d=2 / death-of-d=1 | this kit (same-kit registration, kit-1 precedent) | EXACTLY ONE {19,24}@43 UP 1v0; {19,22} conform-DEAD | **HIT** |
| m=19@z=43 birth d=3 | this kit (same-kit) | EXACTLY TWO: stick 1v2 + birth {19,26}@45 UP 2v0 gap 7 | **HIT** |
| m=20@z=43 one-past-of-d=2 / death-of-d=1 | this kit (same-kit) | EXACTLY ONE (20,24) DOWN 0v1; (20,22) conform-DEAD | **HIT** |
| m=20@z=44 birth d=3 | this kit (same-kit) | EXACTLY TWO: stick 0v2 + birth (20,26)@46 UP 2v1 gap 6 | **HIT** |
| band-start windows m=19 z∈{25..28}, m=20 z∈{27..29} | kit-1 S5 item (5), amended by overlap census | 0 separations each; 2 in-row base spots reproduce | **HIT** (7/7 rows clean) |

Overlap census (why the window is restricted): the published strip sweeps (base token m,
R=m+z+1, S∈{m..m+39}, arity≤4 TOTAL) of z21-min16 (m∈{16..20}), the z=22 kits, z23-floor17
(m∈{17..22}), z24-floor18, z25-min20 (m∈{20..25}), z26-floor20 (m∈{20..26}) contain every
x0-window position for m=19 at z∈{21..24} and m=20 at z∈{21..26}; those strips are published
0 violations, so the contained rows are derivable-clean and were NOT re-swept
(duplicate-avoidance). Verified free slices only were measured.

## 3. Scaffold status after this kit (finite observations, candidate status)

- New-band life cycles m=19 (odd) / m=20 (even): **4/4 birth seats each through d=3**
  (frontier z37/z38, z39/z40, z41/z42, z43/z44; shapes (m, m+2d+1)/(m, m+2d), born
  UP 2v0 / UP 2v1).
- One-past decays: odd 2->1 now **17 observations** (15 published + m=19@z=40, z=42 here);
  even 2->0 now **16** (14 published + m=20@z=41, z=43 here).
- Sticks (birth+2, collapse jumps to 2, value stays at the decayed parity value):
  odd gains m=19@z=41, z=43; even gains m=20@z=42, z=44.
- Deaths (birth+3 conform, value = collapse from then on): **4 NEW datums, the first for
  m=19/m=20** — m=19 d=0@z40 (v(39,40,60)=1), d=1@z42 (v(41,42,62)=1); m=20 d=0@z41
  (v(40,41,62)=0), d=1@z43 (v(42,43,64)=0). Death class observed for d∈{0,1} of each parity.
- Frontier parity law: unchanged 8/8 (m=13..20). The m=21/m=22 datum candidates are
  REGISTERED in S5 below (not measured here).
- In-band clean windows (x0 style): m=19 measured z∈{25..36} (=z*(19)-12..-1; 12 slices),
  m=20 measured z∈{27..37} (11 slices); strip-derived clean extension to z=21 for both.
  Band-start conventions undetermined (declaration lane).

## 4. Verification

- K0832 battery: 156/156 closed form == canonical == ordered engine (every literal used
  by the file, incl. the S5 registration constants).
- Published anchors: 40/40 exact (30 kit-1 + 8 kit-1 new-band separation spots `6057ed51`
  + 2 z25/z26 base spots inside the window rows).
- Determinism: 6 runs byte-identical (default ×2, PYTHONHASHSEED=random, env -i isolated
  dirs ×2), rc 0, ~7.5 s/run.
- Ordered-engine audit (outside the frozen artifact): all 15 rows re-enumerated with
  H_ordered — 316 shapes, separation lists value-exact 15/15, anchors 40/40.
- Engine gate PASS (pin `bd5f22e4…`); frozen output sha256
  `6c85f8c2b8649b558f4833dca2bdfd4b901c3c17c2d5cec5a79e6396a39ed3c4`.
- Timestamp erratum (disclosed; frozen file NOT edited): the docstring counter-probe note
  reads 09:02Z; the probes actually ran at ~08:57-08:59Z before assembly, HEAD `6057ed51`
  confirmed unchanged at both times; probes re-run at push time against then-current main.

## 5. Handoff / registered items for the next execution (binding constants, engine-free)

All collapse constants below are K0832 paper derivations, battery-checked in the frozen
output section future_slice_registration_constants:

1. m=19@z=44 (one-past-of-d=3 / death-of-d=2): EXACTLY ONE {19,26}@S=45 UP 1v0
   (collapse v(45,44,64)=0); {19,24} conform-DEAD at birth+3 (collapse v(43,44,64)=1).
2. m=19@z=45 (birth d=4): EXACTLY TWO: stick {19,26}@S=45 DOWN 1v2 (collapse
   v(45,45,65)=2) + NEW {19,28}@S=47 UP 2v0 (collapse v(47,45,65)=0), seat gap 9.
3. m=20@z=45 (one-past-of-d=3 / death-of-d=2): EXACTLY ONE (20,26)@S=46 DOWN 0v1
   (collapse v(46,45,66)=1); (20,24) conform-DEAD (collapse v(44,45,66)=0).
4. m=20@z=46 (birth d=4): EXACTLY TWO: stick (20,26)@S=46 DOWN 0v2 (collapse
   v(46,46,67)=2) + NEW (20,28)@S=48 UP 2v1 (collapse v(48,46,67)=1), seat gap 8.
5. FIRST-EVER m=21/m=22 row proposals (frontier law 9th/10th datum candidates):
   m=21@z=41 (z*(21)=41, R=63, 20 shapes expected by the m²−41m+440 pattern, count
   measured at run time): EXACTLY ONE {21,22}@S=43 UP 2v0 (collapse v(43,41,63)=0);
   m=22@z=42 (z*(22)=42, R=65): EXACTLY ONE (22,22)@S=44 UP 2v1 (collapse
   v(44,42,65)=1). In-band window sweep proposals m=21 z∈{33..40}, m=22 z∈{34..41}
   (candidates 0 separations) — CAVEAT: re-probe strip coverage at build time (the
   z=33..41 census kits do not exist yet, so the slices are expected free; verify by
   content probe before measuring, as done for m=19/m=20 here).
6. Ladder continuation past these constants (m19@z46+ / m20@z47+, further d) derivable
   from the scaffold; register before measuring per protocol.
7. NOT taken by this lane (other lanes' registered items — do not touch): the
   sixthwave §5 items (m=17/m=18 past-side z∈{37..41} rows, z=33 touch, k45/k46 supply
   constants), the z=26 floor-21 heavy census lane, the 11×11 lane. No K slot claimed;
   T-Z19/T-Z20 declaration lanes own their band conventions.
8. Parallel-run coordination: this lane's items 1-5 are now published registrations;
   if a parallel hourly run has already executed any of them when this is read, treat
   the second execution as blind replication or pivot to an unregistered slice
   (e.g. m19@z46 / m20@z47 single-slice extensions), and re-fetch latest main before
   any push.

## 6. Caveats

Finite machine observations against the pinned raw engine only; no theorem, no universal
claim (the 17/16/4-count class statements are observation counts over published + this
kit's data, not laws); strip-derivation is set-containment over published artifacts, not a
new measurement; standard 11×11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots: all UNKNOWN, unchanged; no verdict consumed.
