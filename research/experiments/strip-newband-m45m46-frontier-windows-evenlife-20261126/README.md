# kit-15: strip-newband m45/m46 frontier first-contact, ladder continuations to depth, rule-v2 standing enumeration, first m=43/m=44 in-band windows, and the even-m z=3m+10 next-depth lifecycle rows (2026-11-26)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-14 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

## Provenance

- kit-14 frozen registration source: `research/experiments/strip-newband-m43m44-frontier-windows-evenlife-20261126/` (commit `cf989198`, frozen .out sha256 `5f985e73...`, kit-14 explorer sha256 `5c071e64...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c1...`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-15 explorer: `explore_m45m46_frontier_windows_evenlife.py` sha256 `98f31765...` (196,276 bytes).
- Frozen official output: `explore_m45m46_frontier_windows_evenlife.out` sha256 `eec9bd10...` (394,485 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 4 byte-identical runs total (default x2; PYTHONHASHSEED=random; PYTHONHASHSEED=12345). One run per shell command (see disclosure 1).
- derive_check: `derive_check_kit15.py` (engine-free, K0832 closed form only) 2,885 checks DERIVE-PASS, 0 fails.
- audit: `audit_kit15.py` 20/20 gates PASS, 2 runs byte-identical (`74056175...`); tamper battery 3/3 fail-closed (T1 battery closed flip -> G3; T2 frontier m45 datum value flip -> G7+G9+G14; T3 anchor published_value flip -> G4).

## Measured census (49 rows, 158 separations)

- The 30 binding rows (28 ladder m=19..32 next-depth one-past/birth + 2 frontier) are ALL FULL HIT: every registered seat separates with exactly the registered value/direction, every rule-v2 stack split of every 2-token seat with co >= 2m is an exact numerical mimic of its host seat, and there are ZERO unregistered separations (113 separations in the binding rows, all registered or exact-mimic shadows).
- Frontier 32nd/33rd parity datums, FIRST-EVER m>44 rows, both EXACT:
  - m=45 @ z=89: seat {45,46} @S=91 UP 2v0 (collapse v(91,89,135)=0).
  - m=46 @ z=90: seat (46,46) @S=92 UP 2v1 (collapse v(92,90,137)=1).
  - Observation count only: the frontier parity scaffold is now 34/34 (m=13..46). NOT a law.
- Ladder continuations m=19..m=32 to the registered next depths (m19/m20 now at birth z=71/72, series-deepest). The early-follow observable is confirmed a 5th consecutive time from pre-registration: the m=19 z=70 one-past row carries the full 8-split shadow set of co=52 as exact mimics (host value 1) and m=20 z=71 the 7-split set (host value 0).
- Boundary equistack, FIRST OBSERVATION: at m=24 (NEW-seat co=48=2m, the exact co >= 2m boundary) the equistack {24,24,24} @S=72 itself separates as an exact mimic of the NEW seat {24,48} @S=72 (both value 2, UP). Previously only strict co > 2m splits had been observed as shadows; the boundary case is now measured once (m=24 z=70 row, 3 separations). Finite observation, no claim.
- In-band windows m=43 z{77..84} and m=44 z{78..85}: 16/16 rows CLEAN (zero separations). With the kit-14 frontier rows, the m=43 measured band is now {77..85} and the m=44 band {78..86}; z below the window remains unmeasured, unregistered.
- Even-m z=3m+10 lifecycle rows (m=14/16/18), NON-BINDING continuation registered contingent on the kit-14 z=3m+8 outcomes (3/3 EXACT): 3/3 EXACT again. Template: stick {m,2m+10} @S=3m+10 DOWN 0v2 + NEW {m,2m+12} @S=3m+12 UP 2v1 + 13 exact-mimic shadows per row (6 stick-side + 7 NEW-side splits) + trio {m,m,m} conform (absent) at z=3m+10. The even-m lifecycle chain now extends through z=3m+10 (observed z=3m-1..3m+10).
- k0832 battery: 2,034/2,034 literal triples (1,970 kit-14 carried + 64 new; every new literal satisfies closed == vC == vO).
- Published anchor rechecks: 869/869 spots reproduce exactly (733 kit-14 anchors byte-carried + the 136 kit-14 published census separation spots first-anchored here).
- Total separations 158 across 49 rows equals the data-driven registered count (every binding seat + every admissible rule-v2 split + the evenlife seats/splits; audit G8 recomputes this independently).

## Registration for kit-16 (engine-free, NOT measured here)

34 future constants registered in the frozen .out section
future_slice_registration_constants:
- 28 ladder next-depth one-past/birth pairs for m=19..m=32 (one depth beyond this kit, e.g. m19 one-past z=72 {19,52}@S=73, birth z=73 stick {19,52} + NEW {19,54}), rule-v2 stack lists included wherever co >= 2m, composed FRESH for the kit-16 seats (see disclosure 4).
- Frontier 34th/35th datum candidates: m=47 @ z=93 {47,48}@S=95 UP 2v0 (collapse v(95,93,141)=0) / m=48 @ z=94 (48,48)@S=96 UP 2v1 (collapse v(96,94,143)=1); z*(m)=2m-2+(m mod 2) per K1268, derive_check double-checked.
- In-band window sweep proposals: m=45 z{81..88}, m=46 z{82..89} (both NOT strip-covered).
- Even-m z=3m+12 continuation proposal (contingent on this kit's z=3m+10 outcomes, NON-BINDING) + odd-m close-out note.

## Honest disclosure

1. Total clean-room rebuild after TWO sandbox resets: the first kit-15 build (previous execution of this lane) completed audit 19/20 with a single audit-source typo (G13 compared a dict to a list) but was destroyed unpublished when a 290 s shell wall reset the execution environment twice (one command carrying two audits; one recursive grep over the persistent kit tree). Nothing was published from that build. This kit is a full rebuild from the published kit-14 SSOTs only: kit-14 explorer/.out/engine re-fetched and byte-pin verified (5c071e64... / 5f985e73... / 582c93c1...), the binding transform re-created and BYTE-VALIDATED against the published kit-13 -> kit-14 chain (regenerating K14_BINDING_JSON from the kit-13 future constants reproduces the published bytes exactly) before being applied to the kit-14 constants. Register-before-measure is intact: the registration authority is the PUBLISHED kit-14 frozen .out (commit cf989198), not any local state. Lesson (fifth/sixth occurrence): one slow command per shell call; kit work product lives in the persistent knowledge mount, not the session scratch.
2. Stale seat labels in the frozen kit-14 prediction texts: all 28 ladder cand texts carry kit-14 seat tokens (off by co-2 from the kit-15 seats, e.g. the text says {19,50}@S=71 where the kit-15 one-past seat is {19,52}@S=71). The collapse literals are authoritative (every one re-verified under the closed form before the freeze); all seats/stacks in this kit are machine-derived from the S=z (stick) / S=z+1 (one-past) / S=z+2 (NEW) / S=z-1 (dead) arithmetic, and derive_check G-stale-label asserts the co-2 relation on every ladder row. The cand texts are carried byte-verbatim per the series convention.
3. Memory-safety patch: row_record_x0 clears the H cache per S inside the sweep (the kit-14 explorer cleared once per row). Pure memoization management; values are identical by construction and the 4-run determinism + audit G7 full recompute confirm it. Needed to stay inside the 1 GB sandbox cgroup at the m=45/m=46 row sizes.
4. The kit-16 future texts registered here carry FRESH stack lists (recomputed for the kit-16 seats), unlike the stale lists this kit received from kit-14; the next kit's binding transform derives seats arithmetically either way.
5. Battery size: this kit registers 64 new battery literals (2,034 total), the exact v-literal set of its binding+evenlife cand texts per the chain rule (kit-14 added 64 the same way). derive_check_kit15.py reads the kit-14 published explorer `explore_m43m44_frontier_windows_evenlife.py` for the carried-battery comparison (not re-published in this kit dir; same practice as kit-14).
6. The generator (gen_kit15.py, not published but re-runnable from the kit-14 published bytes) asserts the full kit-14 record of record as a precondition (49 rows / 136 separations / 30 binding FULL HIT / evenlife 3/3 EXACT) before emitting any kit-15 row; the registration was machine-checked for zero self/earlier overlaps, and audit G16 checks all 49 kit-14 row names are absent here.
7. Hand-typed pins forbidden: every pin in this README was machine-extracted from the frozen files.

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 34/34, the rule-v2 shadow observations (including the early-follow and boundary-equistack observations), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping.
