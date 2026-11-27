# kit-17: strip-newband m49/m50 frontier first-contact, ladder continuations to depth, rule-v2 standing enumeration, first m=47/m=48 in-band windows, and the even-m z=3m+14 next-depth lifecycle rows (2026-11-26)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-16 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

## Provenance

- kit-16 frozen registration source: `research/experiments/strip-newband-m47m48-frontier-windows-evenlife-20261126/` (commit chain 54c580d5/8382fda1/f997daca, frozen .out sha256 `85c04e43...`, kit-16 explorer sha256 `8b9e0a6c...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c1...`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-17 explorer: `explore_m49m50_frontier_windows_evenlife.py` sha256 `32f1c683...` (259,918 bytes).
- Frozen official output: `explore_m49m50_frontier_windows_evenlife.out` sha256 `420d1c83...` (496,038 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 4 byte-identical runs total (default x2; PYTHONHASHSEED=random; PYTHONHASHSEED=12345) on the FINAL explorer bytes. One run per shell command (see disclosure 2).
- derive_check: `derive_check_kit17.py` (engine-free, K0832 closed form only) 3,205 checks DERIVE-PASS, 0 fails.
- audit: `audit_kit17.py` 20/20 gates PASS, 2 runs byte-identical. Tamper battery 3/3 fail-closed (T1 battery closed flip -> G3; T2 frontier m49 datum value flip -> G7+G9+G14; T3 anchor published_value flip -> G4); clean control PASS on the frozen bytes after the battery; frozen bytes byte-verified unchanged through the battery.

## Measured census (49 rows, 211 separations)

- The 30 binding rows (28 ladder m=19..32 next-depth one-past/birth + 2 frontier) are ALL FULL HIT: every registered seat separates with exactly the registered value/direction, every rule-v2 stack split of every 2-token seat with co >= 2m is an exact numerical mimic of its host seat, and there are ZERO unregistered separations (154 separations in the binding rows, all registered or exact-mimic shadows).
- Frontier 36th/37th parity datums, FIRST-EVER m>48 rows, both EXACT:
  - m=49 @ z=97: seat {49,50} @S=99 UP 2v0 (collapse v(99,97,147)=0).
  - m=50 @ z=98: seat (50,50) @S=100 UP 2v1 (collapse v(100,98,149)=1).
  - Observation count only: the frontier parity scaffold is now 38/38 (m=13..50). NOT a law.
- Ladder continuations m=19..m=32 to the registered next depths (m19/m20 now at birth z=75/76, new series-deepest). The early-follow observable is confirmed a 7th consecutive time from pre-registration: the m=19 z=74 one-past row carries the full 10-split shadow set of co=56 as exact mimics (host value 1, UP 1v0) and m=20 z=75 the 9-split set (host value 0, DOWN 0v1).
- Boundary equistack, THIRD OBSERVATION (one-past side, co=2m exactly): at m=25 (one-past co=50=2m, the exact co >= 2m boundary) the equistack {25,25,25} @S=75 itself separates as an exact mimic of the one-past seat {25,50} @S=75 (both value 1, UP). Kit-15 observed the NEW-seat boundary case (m=24), kit-16 the one-past side (m=24 co=48); this is the first observation at an odd m (m=25), where co=50=2m admits exactly one split {25,25,25}. Finite observation, no claim.
- In-band windows m=47 z{85..92} and m=48 z{86..93}: 16/16 rows CLEAN (zero separations). With the kit-16 frontier rows, the m=47 measured band is now {85..93} and the m=48 band {86..94}; z below the window remains unmeasured, unregistered.
- Even-m z=3m+14 lifecycle rows (m=14/16/18), NON-BINDING continuation registered contingent on the kit-16 z=3m+12 outcomes (3/3 EXACT): 3/3 EXACT again. Template: stick {m,2m+14} @S=3m+14 DOWN 0v2 + NEW {m,2m+16} @S=3m+16 UP 2v1 + 17 exact-mimic shadows per row (8 stick-side + 9 NEW-side splits) + trio {m,m,m} conform (absent) at z=3m+14. The even-m lifecycle chain now extends through z=3m+14 (observed z=3m-1..3m+14).
- k0832 battery: 2,162/2,162 literal triples (2,098 kit-16 carried + 64 new; every new literal satisfies closed == vC == vO).
- Published anchor rechecks: 1,210/1,210 spots reproduce exactly (1,027 kit-16 anchors byte-carried + the 183 kit-16 published census separation spots first-anchored here).
- Total separations 211 across 49 rows equals the data-driven registered count (every binding seat + every admissible rule-v2 split + the evenlife seats/splits; audit G8 recomputes this independently).

## Registration for kit-18 (engine-free, NOT measured here)

34 future constants registered in the frozen .out section
future_slice_registration_constants:
- 28 ladder next-depth one-past/birth pairs for m=19..m=32 (one depth beyond this kit), rule-v2 stack lists included wherever co >= 2m, composed FRESH for the kit-18 seats.
- Frontier 38th/39th datum candidates: m=51 @ z=101 {51,52}@S=103 UP 2v0 (collapse v(103,101,153)=0) / m=52 @ z=102 (52,52)@S=104 UP 2v1 (collapse v(104,102,155)=1); z*(m)=2m-2+(m mod 2) per K1268, derive_check double-checked.
- In-band window sweep proposals: m=49 z{89..96}, m=50 z{90..97} (both NOT strip-covered).
- Even-m z=3m+16 continuation proposal (contingent on this kit's z=3m+14 outcomes, NON-BINDING) + odd-m close-out note.

## Honest disclosure

1. derive_check caught a PRE-FREEZE arithmetic error in the first K18_FUTURE window proposals of the first explorer build (sha256 `03f04f31...`): the m=49/m=50 windows were mis-registered as z{91..98}/{92..99} instead of the correct z*(m)-8..-1 = {89..96}/{90..97}. The explorer was regenerated (final sha256 `32f1c683...`) and the ENTIRE verification battery (4 determinism runs, derive_check, audit x2, tamper 3/3, clean control) was re-executed on the final bytes. The first build was discarded pre-freeze and never published; its measured rows are byte-identical to the final build (the window proposals are registered constants, not measured in this kit; only the future-section text differs). derive_check_kit17.py now checks the kit-18 window arithmetic explicitly, so this class of error is gated for every future kit.
2. Two execution-environment resets occurred during the determinism battery (a two-run command exceeded the 290 s sandbox wall; a follow-up run in the same shell was OOM-killed at 137). Lesson reconfirmed (eighth occurrence): ONE heavy command per shell call. All work products live in the persistent knowledge mount; the published bytes are the 4-run battery on the final explorer.
3. FRESH seat labels: the frozen kit-16 prediction texts registered here carry FRESH seat labels (kit-16 received FRESH from kit-15 and emitted FRESH; this kit received and emits FRESH); freshness is ASSERTED in derive_check and in audit G14's seat checks. The cand texts are carried byte-verbatim per the series convention.
4. Memory-safety patch carried forward from kit-15/16: row_record_x0 clears the H cache per S inside the sweep; the engine block itself runs byte-verbatim. Values identical by construction; 4-run determinism + audit G7 full recompute confirm.
5. Battery size: this kit registers 64 new battery literals (2,162 total), the exact v-literal set of its binding+evenlife cand texts per the chain rule (kit-14/15/16 each added 64 the same way). derive_check_kit17.py reads the kit-16 published explorer `explore_m47m48_frontier_windows_evenlife.py` for the carried-battery comparison (not re-published in this kit dir; same practice as kit-14/15/16).
6. The generator (gen_kit17.py, not published but re-runnable from the kit-16 published bytes; transform_lib extended with the 36th/37th ordinal labels) asserts the full kit-16 record of record as a precondition (49 rows / 183 separations / 30 binding FULL HIT / evenlife 3/3 EXACT) before emitting any kit-17 row; the registration was machine-checked for zero self/earlier overlaps, and audit G16 checks all 49 kit-16 row names are absent here.
7. Hand-typed pins forbidden: every pin in this README was machine-extracted from the frozen files.

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 38/38, the rule-v2 shadow observations (including the early-follow 7/7 and boundary-equistack 3-observation series), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping.
