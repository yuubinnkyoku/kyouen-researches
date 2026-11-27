# 2026-11-26 — in-band completions + m=19/m=20 new-bands micro-kit: ALL FOURTEEN candidate rows EXACT HIT (frontier m=19@z=37 UP 2v0 / m=20@z=38 UP 2v1 => the parity-corrected frontier-record law is 8/8 for m in {13..20}; one-past decays 2->1 / 2->0 and the FIRST d=1 birth seats for both new bands), the T-Z21 + T-Z22 + T-Z24 residual bands COMPLETED plus the FIRST-EVER m=19/m=20 in-band bands swept COMPLETE (33 in-band rows + 9 exts ALL CLEAN), 30/30 published anchors reproduced, k0832 battery 238/238

Kit: `research/experiments/strip-inband-completions-m19m20-newbands-20261126/`
(explore_inband_m19m20.py `3f4eeb22` 34,015 B / engine_block.py
`582c93c1` pin `bd5f22e4` / frozen .out `9a09b674` 43,675 B / README).

Slot check (pre-claim, content-based, at kit-build time): latest
main head `28ed2d9c`. Content `search_code` queries
("inband_m17_z29", "m16_z29", "m19_z37", "frontier_m19",
"inband_m16_z29") returned NO measurement record; the wave-lane
kits (wavetrain/fifthwave/sixthwave, per their own slot-check
paragraphs) published ONLY past slices z >= z*(m) of the bands
m=13..18, so no published engine value exists for ANY m=19 or
m=20 position, nor for the in-band rows m=16@z=29 / m=17@z in
{29..32} / m=18@z in {29..33} (only z <= 28 entries published).
Every position measured here was first touched at the frozen first
run, except the 30 recheck anchors. 6/6 runs byte-identical
(~26 s per run); post-freeze ordered-engine audit 40/40 (all 10
separation entries + all 30 anchors, independent ordered engine,
identical); K0832 battery 238/238.

## §2 Registered predictions vs measured (all registered BEFORE the freeze; R = m+z+1, K1268: z*(m)=2m-2+(m mod 2))

1. m=16 @ z=29 IN-BAND (registered frontier-lifecycle S5 item (2)):
   candidate 0 separations — MEASURED: 40 shapes, 0 separations —
   **T-Z21 residual band m=16 z in {22..29} COMPLETED, 8/8 entries
   clean** (7 published + this). First m=16 ext: 39/0. HIT.
2. m=17 @ z=29..32 IN-BAND (registered item (2)): candidate 0 —
   MEASURED: 32 shapes × 4 slices, 0 separations — **T-Z22 band
   COMPLETED, 10/10 clean**. First m=17 ext at z=32: 31/0. HIT.
3. m=18 @ z=29..33 IN-BAND (registered item (2)): candidate 0 —
   MEASURED: 26 shapes × 5 slices, 0 separations (m=18 ext series
   continued: 25/0 at each slice) — **T-Z24 band COMPLETED, 9/9
   clean**; the clean z=33 entry derivative-confirms the
   sixthwave-registered z=33 touch candidate x3 = 1. HIT.
4. m=19 @ z=29..36 IN-BAND (KIT-ADDED new-band sweep; window
   z*(19)-8..z*(19)-1; candidate 0 per the six-band in-band-clean
   precedent) — MEASURED: the FIRST-EVER m=19 rows, 22 shapes × 8
   slices, 0 separations — **NEW m=19 in-band residual band swept
   COMPLETE in one kit (8/8 clean)**. HIT.
5. m=20 @ z=30..37 IN-BAND (KIT-ADDED new-band sweep; candidate 0)
   — MEASURED: the FIRST-EVER m=20 rows, 20 shapes × 8 slices,
   0 separations — **NEW m=20 in-band residual band swept COMPLETE
   (8/8 clean)**. The in-band-clean observation window now spans
   EIGHT bands m in {13..20}. HIT.
6. m=19 @ z=37 FRONTIER (registered frontier-lifecycle S5 item
   (1), the parity-corrected frontier-record law): predicted
   EXACTLY ONE — MEASURED: 22 shapes, exactly X={19,20} @S=39 UP
   2v0 (value 2 vs collapse v(39,37,57)=0); all other 21 shapes
   conform — FULL HIT. The law is now 8/8 (m=13..20).
7. m=20 @ z=38 FRONTIER (registered item (1)): predicted EXACTLY
   ONE — MEASURED: 20 shapes, exactly X=(20,20) @S=40 UP 2v1
   (value 2 vs collapse v(40,38,59)=1); all other 19 conform —
   FULL HIT.
8. m=19 @ z=38 ONE-PAST (kit-added scaffold-derived binding
   candidate, same run): predicted EXACTLY ONE — MEASURED:
   exactly {19,20}@S=39 UP 1v0 (collapse v(39,38,58)=0) — the odd
   decay 2->1 gains its 15th observation (first on a NEW band,
   measured in the same run as the birth). FULL HIT.
9. m=20 @ z=39 ONE-PAST: predicted EXACTLY ONE — MEASURED:
   exactly (20,20)@S=40 DOWN 0v1 (collapse v(40,39,60)=1) — the
   even decay 2->0 gains its 14th observation. FULL HIT.
10. m=19 @ z=39 TWO-PAST BIRTH SLICE (kit-added; the FIRST d=1
    birth seat of the new band): predicted EXACTLY TWO — MEASURED:
    exactly stick {19,20}@S=39 DOWN 1v2 (stuck 1 vs the z==x
    collapse jump v(39,39,59)=2, confirmed) + NEW birth {19,22}@
    S=41 UP 2v0 (collapse v(41,39,59)=0), d=1 seat gap 3 (odd
    slot-law shape (m, m+2d+1)) — FULL HIT.
11. m=20 @ z=40 TWO-PAST BIRTH SLICE (FIRST d=1 seat of the new
    band): predicted EXACTLY TWO — MEASURED: exactly stick
    (20,20)@S=40 DOWN 0v2 (stuck 0 vs collapse v(40,40,61)=2) +
    NEW birth (20,22)@S=42 UP 2v1 (collapse v(42,40,61)=1), d=1
    seat gap 2 (even slot-law shape (m, m+2d)) — FULL HIT.
12. m=19/m=20 frontier exts (first-ever for the new bands):
    21/0-with-the-same-single-separation resp.
    19/0-with-the-same-single-separation — consistent.
13. Published anchor rechecks 30/30 reproduce exactly: the z=28
    handoff quad (0,1,1,0), the z=29..32 touch quads (0,1,1,0
    each), the frontier m=15@z=29 / m=16@z=30 separations (2,2),
    the one-past m=15@z=30 / m=16@z=31 separations (1,0), the
    two-past-with-birth m=13@z=27 pair (1,2), the m=17@z=35
    stick+birth (1,2) and the m=13@z=33 stick+birth (1,2).
14. K0832 battery 238/238 (closed form vs canonical vs ordered);
    engine_gate PASS; determinism 6/6 byte-identical; post-freeze
    ordered-engine audit 40/40.

## §3 Scaffold status after this kit (CANDIDATE, finite observations; no universal claim)

- Parity-corrected frontier-record law (K1268 frontier z*(m),
  odd m: birth {m,m+1}@S=2m+1 UP 2v0 / even m: {m,m}@S=2m UP 2v1):
  now 8/8 data points, m in {13..20} (m=19/m=20 datums 7-8 this
  kit).
- Separation life-cycle scaffold (births at z*(m)+2d at shapes
  (m, m+2d+1) odd / (m, m+2d) even; born 2; decay 2,1,1 odd /
  2,0,0 even; death conform at birth+3): the two new bands gain
  their d=0 and d=1 seats (both measured EXACTLY, including the
  first NEW-BAND collapse-jump sticks at the z==x windows
  v(39,39,59)=2 and v(40,40,61)=2); the one-past decay counts move
  to 15 (odd) / 14 (even).
- In-band-clean (rows at z < z*(m) have 0 separations): now EIGHT
  fully-intact bands m in {13..20}; fully-swept residual bands:
  K1330 m=14, K1335 m=15, T-Z21 m=16 (this kit), T-Z22 m=17
  (this kit), T-Z24 m=18 (this kit), m=19 (this kit, window
  {29..36}), m=20 (this kit, window {30..37}).

## §5 Handoff (new registrations, all BEFORE any next measurement; constants from the published K0832 closed form, R = m+z+1, battery-checked at 238/238 including these literals)

1. NEXT SLICES of the new bands (registered in the frozen output
   section future_slice_registration_constants):
   - m=19 @ z=40: EXACTLY ONE — {19,22}@S=41 UP 1v0 (collapse
     v(41,40,60)=0); {19,20} conform-DEAD at its birth+3 slice
     (collapse v(39,40,60)=1) — the FIRST m=19 death datum (d=0
     shape, birth+3 law 22nd observation candidate).
   - m=19 @ z=41 (birth slice d=2): EXACTLY TWO — stick {19,22}@S=41
     DOWN 1v2 (collapse v(41,41,61)=2) + NEW {19,24}@S=43 UP 2v0
     (collapse v(43,41,61)=0), d=2 seat gap 5.
   - m=20 @ z=41: EXACTLY ONE — (20,22)@S=42 DOWN 0v1 (collapse
     v(42,41,62)=1); (20,20) conform-DEAD at its birth+3 (collapse
     v(40,41,62)=0) — the FIRST m=20 death datum.
   - m=20 @ z=42 (birth slice d=2): EXACTLY TWO — stick (20,22)@S=42
     DOWN 0v2 (collapse v(42,42,63)=2) + NEW (20,24)@S=44 UP 2v1
     (collapse v(44,42,63)=1), d=2 seat gap 4.
2. NEW-BAND BAND-START PINNING (cheap candidate lane, this kit's
   windows were z*-8..z*-1 by convention choice): m=19 rows at
   z in {21..28} and m=20 rows at z in {22..29}, candidate 0
   separations each — descending sweeps would pin where the
   in-band-clean window actually begins for the new bands (the
   started bands begin at z*-{6,8,8,10,9} for m in {13,14,15,17,18}).
3. The Sixthwave-kit S5 registrations (two-past/one-past z=37..41
   of the m=13..18 bands, the z=33 touch quad x1/y1/x3/x4 — of
   which x3 is now derivative-confirmed by this kit's clean
   m=18@z=33 row — and the k=45/k=46 tails) remain REGISTERED and
   UNTOUCHED by this kit; the wave lane executes them next.
4. z=26 floor-21 (z-5 CRITICAL) census kit remains the registered
   heavy lane; untouched here.
5. 11x11 UNKNOWN: unchanged. No action.

## §6 Caveats

Finite machine observations only; candidate scaffolds stated per
section; no universal claim; no K slot claimed (1 experiment != 1
K). Raw engine pinned at `bd5f22e4…`. All collapse constants
quoted in the registrations are K0832 closed-form values,
re-derived twice (draft + battery) before the freeze. 11x11 empty
board, two-stone roots, S2, class 1/2/4, 19 central-reply roots
and all closure classes: UNKNOWN unchanged; no verdict consumed.
