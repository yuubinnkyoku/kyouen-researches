# kit-16: strip-newband m47/m48 frontier first-contact, ladder continuations to depth, rule-v2 standing enumeration, first m=45/m=46 in-band windows, and the even-m z=3m+12 next-depth lifecycle rows (2026-11-26)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-15 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

## Provenance

- kit-15 frozen registration source: `research/experiments/strip-newband-m45m46-frontier-windows-evenlife-20261126/` (commit chain 47d28b38/6bbfcebc/5e8f48c0, frozen .out sha256 `eec9bd10...`, kit-15 explorer sha256 `98f31765...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c1...`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-16 explorer: `explore_m47m48_frontier_windows_evenlife.py` sha256 `8b9e0a6c...` (226,117 bytes).
- Frozen official output: `explore_m47m48_frontier_windows_evenlife.out` sha256 `85c04e43...` (442,100 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 4 byte-identical runs total (default x2; PYTHONHASHSEED=random; PYTHONHASHSEED=12345). One run per shell command (see disclosure 1).
- derive_check: `derive_check_kit16.py` (engine-free, K0832 closed form only) 3,053 checks DERIVE-PASS, 0 fails.
- audit: `audit_kit16.py` 20/20 gates PASS, 2 runs byte-identical; an INDEPENDENT second audit implementation (18 gates, separate lane) also AUDIT-PASS 18/18 on the same frozen bytes. Tamper battery 3/3 fail-closed (T1 battery closed flip -> G3; T2 frontier m47 datum value flip -> G7+G9+G14; T3 anchor published_value flip -> G4).

## Measured census (49 rows, 183 separations)

- The 30 binding rows (28 ladder m=19..32 next-depth one-past/birth + 2 frontier) are ALL FULL HIT: every registered seat separates with exactly the registered value/direction, every rule-v2 stack split of every 2-token seat with co >= 2m is an exact numerical mimic of its host seat, and there are ZERO unregistered separations (132 separations in the binding rows, all registered or exact-mimic shadows).
- Frontier 34th/35th parity datums, FIRST-EVER m>46 rows, both EXACT:
  - m=47 @ z=93: seat {47,48} @S=95 UP 2v0 (collapse v(95,93,141)=0).
  - m=48 @ z=94: seat (48,48) @S=96 UP 2v1 (collapse v(96,94,143)=1).
  - Observation count only: the frontier parity scaffold is now 36/36 (m=13..48). NOT a law.
- Ladder continuations m=19..m=32 to the registered next depths (m19/m20 now at birth z=73/74, series-deepest). The early-follow observable is confirmed a 6th consecutive time from pre-registration: the m=19 z=72 one-past row carries the full 9-split shadow set of co=54 as exact mimics (host value 1) and m=20 z=73 the 8-split set (host value 0).
- Boundary equistack, SECOND OBSERVATION (one-past side): at m=24 (one-past co=48=2m, the exact co >= 2m boundary) the equistack {24,24,24} @S=72 itself separates as an exact mimic of the one-past seat {24,48} @S=72 (both value 0, DOWN). Kit-15 observed the NEW-seat boundary case; the one-past side is now measured once (m=24 z=71 row, 2 separations). Finite observation, no claim.
- In-band windows m=45 z{81..88} and m=46 z{82..89}: 16/16 rows CLEAN (zero separations). With the kit-15 frontier rows, the m=45 measured band is now {81..89} and the m=46 band {82..90}; z below the window remains unmeasured, unregistered.
- Even-m z=3m+12 lifecycle rows (m=14/16/18), NON-BINDING continuation registered contingent on the kit-15 z=3m+10 outcomes (3/3 EXACT): 3/3 EXACT again. Template: stick {m,2m+12} @S=3m+12 DOWN 0v2 + NEW {m,2m+14} @S=3m+14 UP 2v1 + 15 exact-mimic shadows per row (7 stick-side + 8 NEW-side splits) + trio {m,m,m} conform (absent) at z=3m+12. The even-m lifecycle chain now extends through z=3m+12 (observed z=3m-1..3m+12).
- k0832 battery: 2,098/2,098 literal triples (2,034 kit-15 carried + 64 new; every new literal satisfies closed == vC == vO).
- Published anchor rechecks: 1,027/1,027 spots reproduce exactly (869 kit-15 anchors byte-carried + the 158 kit-15 published census separation spots first-anchored here).
- Total separations 183 across 49 rows equals the data-driven registered count (every binding seat + every admissible rule-v2 split + the evenlife seats/splits; audit G8 recomputes this independently).

## Registration for kit-17 (engine-free, NOT measured here)

34 future constants registered in the frozen .out section
future_slice_registration_constants:
- 28 ladder next-depth one-past/birth pairs for m=19..m=32 (one depth beyond this kit), rule-v2 stack lists included wherever co >= 2m, composed FRESH for the kit-17 seats.
- Frontier 36th/37th datum candidates: m=49 @ z=97 {49,50}@S=99 UP 2v0 (collapse v(99,97,147)=0) / m=48+2: m=50 @ z=98 (50,50)@S=100 UP 2v1 (collapse v(100,98,149)=1); z*(m)=2m-2+(m mod 2) per K1268, derive_check double-checked.
- In-band window sweep proposals: m=47 z{85..92}, m=48 z{86..93} (both NOT strip-covered).
- Even-m z=3m+14 continuation proposal (contingent on this kit's z=3m+12 outcomes, NON-BINDING) + odd-m close-out note.

## Honest disclosure

1. Publication lane takeover after an execution-environment reset: the kit-16 build (generation, 4 determinism runs, derive_check, audit runs 1-2 and the start of the tamper battery) was completed by one execution of this hourly lane which then hit the 290 s sandbox wall mid-tamper and went silent (its surviving artifacts were stashed in the persistent knowledge mount). A second execution of the same lane verified the stash byte-pins, completed the tamper battery 3/3 fail-closed with the published audit script, independently re-audited the frozen .out with a separate 18-gate implementation (AUDIT-PASS), wrote this README/log and pushed. Nothing was rebuilt or re-measured: the frozen .out pushed here is byte-identical to the four determinism runs (`85c04e43...`). Register-before-measure is intact: the registration authority is the PUBLISHED kit-15 frozen .out (commit 5e8f48c0 chain), not any local state. Lesson (seventh occurrence): one slow command per shell call; kit work product lives in the persistent knowledge mount.
2. FRESH seat labels: unlike kit-15 (which received co-2-stale labels from kit-14), the frozen kit-15 prediction texts registered here carry FRESH seat labels (label co == derived seat co, label sums to its own S literal); this freshness is ASSERTED in derive_check (replacing kit-15's stale-label co-2 assertion) and in audit G14 of the independent audit. The cand texts are carried byte-verbatim per the series convention.
3. Memory-safety patch carried forward from kit-15: row_record_x0 clears the H cache per S inside the sweep; the engine block itself runs byte-verbatim (no memo adaptation). Values identical by construction; 4-run determinism + audit G7 full recompute confirm.
4. Battery size: this kit registers 64 new battery literals (2,098 total), the exact v-literal set of its binding+evenlife cand texts per the chain rule (kit-14 and kit-15 each added 64 the same way). derive_check_kit16.py reads the kit-15 published explorer `explore_m45m46_frontier_windows_evenlife.py` for the carried-battery comparison (not re-published in this kit dir; same practice as kit-14/15).
5. The generator (gen_kit16.py, not published but re-runnable from the kit-15 published bytes) asserts the full kit-15 record of record as a precondition (49 rows / 158 separations / 30 binding FULL HIT / evenlife 3/3 EXACT) before emitting any kit-16 row; the registration was machine-checked for zero self/earlier overlaps, and audit G16 checks all 49 kit-15 row names are absent here.
6. Hand-typed pins forbidden: every pin in this README was machine-extracted from the frozen files.

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 36/36, the rule-v2 shadow observations (including the early-follow and boundary-equistack observations), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping.
