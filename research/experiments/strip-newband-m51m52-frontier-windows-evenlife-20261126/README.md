# kit-18: strip-newband m51/m52 frontier first-contact, ladder continuations to depth, rule-v2 standing enumeration, first m=49/m=50 in-band windows, and the even-m z=3m+16 next-depth lifecycle rows (2026-11-26)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-17 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

## Provenance

- kit-17 frozen registration source: `research/experiments/strip-newband-m49m50-frontier-windows-evenlife-20261126/` (final wave commit f90d5d5e, frozen .out sha256 `420d1c83350e5a1c38d1282fa974a3e91d3e50ddd26d82b4c069ea82c4367d95`, kit-17 explorer sha256 `32f1c683...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-18 explorer: `explore_m51m52_frontier_windows_evenlife.py` sha256 `b591e7e1a9b3ec582a25a4bdf6c6f5dc71848a485d7eb2d90eab461a85c9fde1` (298,671 bytes).
- Frozen official output: `explore_m51m52_frontier_windows_evenlife.out` sha256 `c3087285fbdbd44d0588132f9c1d4c75fce2913b816ce383a5f0b377154364ba` (557,319 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 4 byte-identical runs (sha256 above) on the FINAL explorer bytes. The sandbox wall (~280 s) is shorter than one full run in this environment, so all four runs were executed through a checkpointed chunked runner (see disclosure 1); each run is the same deterministic computation split across two process invocations.
- derive_check: `derive_check_kit18.py` (engine-free, K0832 closed form only) 3,365 checks DERIVE-PASS, 0 fails.
- audit: `audit_kit18.py` 20/20 gates PASS, 2 runs byte-identical (audit json sha256 `252a0973...`), plus a post-environment-reset clean control AUDIT-PASS. Tamper battery 3/3 fail-closed (T1 battery closed flip -> G3; T2 frontier m51 datum value flip -> G7+G9+G14; T3 anchor published_value flip -> G4); clean control PASS on the frozen bytes after the battery; frozen bytes byte-verified unchanged through the battery.
- Independent blind second census: the concurrent lane published `research/experiments/strip-newband-m51m52-blind-second-census-20261126/` (kit-18x), frozen BEFORE this kit's frozen .out was read by that lane, from a fresh harness and a fresh audit. Its informational comparison against this kit's local frozen artifact matched 49/49 rows exactly (shapes, R, all 241 separations); this publication makes the pending authoritative cross-check possible (same registration source, same engine SSOT, both frozen).

## Measured census (49 rows, 241 separations)

- The 30 binding rows (28 ladder m=19..32 next-depth one-past/birth + 2 frontier) are ALL FULL HIT: every registered seat separates with exactly the registered value/direction, every rule-v2 stack split of every 2-token seat with co >= 2m is an exact numerical mimic of its host seat, and there are ZERO unregistered separations (178 separations in the binding rows, all registered or exact-mimic shadows).
- Frontier 38th/39th parity datums, FIRST-EVER m>50 rows, both EXACT:
  - m=51 @ z=101 (R=153): seat {51,52} @S=103 UP 2v0 (collapse v(103,101,153)=0). The sweep covers S in {51..103}, 3 shapes at the separation S.
  - m=52 @ z=102 (R=155): seat (52,52) @S=104 UP 2v1 (collapse v(104,102,155)=1).
  - Observation count only: the frontier parity scaffold is now 40/40 (m=13..52). NOT a law.
- Ladder continuations m=19..m=32 to the registered next depths (m19/m20 now at birth z=77/78, new series-deepest). The early-follow observable is confirmed an 8th consecutive time from pre-registration: the m=19 z=76 one-past row carries the full 11-split shadow set of co=58 as exact mimics (host {19,58} UP 1v0) and m=20 z=77 the 10-split set (host {20,58} DOWN 0v1).
- Boundary equistack, FOURTH OBSERVATION (co=2m exactly): at m=26 the one-past seat {26,52} @S=78 (co=52=2m, z=77 row) and the birth stick seat {26,52} @S=78 (z=78 row) both sit exactly on the boundary, and the equistack {26,26,26} separates as an exact mimic of the seat in BOTH rows (audit G13 checks both). Kit-15/16/17 observed the first three (NEW seat m=24; one-past m=24; one-past m=25 odd-m). Finite observation, no claim.
- In-band windows m=49 z{89..96} and m=50 z{90..97}: 16/16 rows CLEAN (zero separations). FIRST-EVER below-frontier m=49/m=50 rows; no strip-derivation claim is made (m=49/m=50 are NOT strip-covered). With the kit-17 frontier rows, the m=49 measured band is now {89..97} and the m=50 band {90..98}; z below the window remains unmeasured, unregistered.
- Even-m z=3m+16 lifecycle rows (m=14 z=58 / m=16 z=64 / m=18 z=70), NON-BINDING continuation registered contingent on the kit-17 z=3m+14 outcomes (3/3 EXACT): 3/3 EXACT again. Template: stick {m,2m+16} @S=3m+16 DOWN 0v2 + NEW {m,2m+18} @S=3m+18 UP 2v1 + exact-mimic shadows per row (splits(2m+16,m) + splits(2m+18,m), e.g. 9+10=19 at m=14/16/18) + trio {m,m,m} conform (absent) at z=3m+16; 21 separations per row, 63 total. The even-m lifecycle chain now extends through z=3m+16 (observed z=3m-1..3m+16).
- k0832 battery: 2,226/2,226 literal triples (2,162 kit-17 carried + 64 new; every new literal satisfies closed == vC == vO).
- Published anchor rechecks: 1,421/1,421 spots reproduce exactly (1,210 kit-17 anchors byte-carried + the 211 kit-17 published census separation spots first-anchored here).
- Total separations 241 across 49 rows equals the data-driven registered count (every binding seat + every admissible rule-v2 split + the evenlife seats/splits; audit G8 recomputes this independently).

## Registration for kit-19 (engine-free, NOT measured here)

34 future constants registered in the frozen .out section
future_slice_registration_constants:
- 28 ladder next-depth one-past/birth pairs for m=19..m=32 (one depth beyond this kit), rule-v2 stack lists included wherever co >= 2m, composed FRESH for the kit-19 seats.
- Frontier 40th/41st datum candidates: m=53 @ z=105 {53,54}@S=107 UP 2v0 (collapse v(107,105,159)=0) / m=54 @ z=106 (54,54)@S=108 UP 2v1 (collapse v(108,106,161)=1); z*(m)=2m-2+(m mod 2) per K1268, derive_check double-checked.
- In-band window sweep proposals: m=51 z{93..100}, m=52 z{94..101} (both NOT strip-covered).
- Even-m z=3m+18 continuation proposal (contingent on this kit's z=3m+16 outcomes, NON-BINDING) registered.

## Honest disclosure

1. Execution-environment wall: this sandbox kills any process at ~280 s and one full explorer run needs ~470 s here, so NO single-process run of main() completes. All four determinism runs were executed through a checkpointed chunked runner (`driver_chunked.py`, not published; mirrors main() row-for-row, statement-for-statement, task-granularity pickle checkpoints, final payload assembled with the identical json.dumps call). The audit likewise OOMs at the engine's 6M-entry lru caches and exceeds the wall, so both audit runs were executed through an equivalent checkpointed audit runner with the caches capped at 200k entries (pure functions, values unchanged; audit G5/G7 fully recompute every quantity). The published explorer and audit scripts are the canonical single-process artifacts; the runners are execution aids only, and 4-run (explorer) + 2-run (audit) byte-identity is the determinism evidence.
2. Two environment resets occurred during the battery (a remote-command artifact failure, then a full sandbox filesystem reset). All work products were backed up in the persistent knowledge mount after every stage; the frozen bytes are the 4-run battery on the final explorer, and the post-reset clean control re-confirmed AUDIT-PASS on the restored frozen bytes.
3. run1's stdout was initially recovered through a tool-result JSON capture that appended one trailing newline; it was normalized to the exact print() bytes and then verified byte-identical to runs 2-4 (all sha256 `c3087285...`). No content byte ever differed.
4. Tamper battery note: the tamper cases were driven through a sandbox variant (`tamper_sandbox.py`, not published) that calls the checkpointed audit runner instead of the single-process audit; the tamper logic, the expected-fail gates, and the pass criteria are identical to the published `tamper_kit18.py`. All three cases failed exactly the expected gates and nothing else; the frozen .out sha256 was re-verified unchanged after the battery.
5. Generation-time defects: during the kit-17 -> kit-18 transformation five defects appeared (a leftover fut17 reference; a constant-ordering interference that corrupted one LITS text; a missing parenthesis in one window row; a double-parenthesis in the KIT17_ROWS splice; a raw-string newline bug in a docstring rewrite). All five were caught by the fail-closed build gates (count asserts, derive_check), fixed before freeze, and none reached the frozen bytes.
6. FRESH seat labels: the frozen kit-17 prediction texts registered here carry FRESH seat labels (kit-17 received FRESH from kit-16 and emitted FRESH; this kit received and emits FRESH); freshness is ASSERTED in derive_check and in audit G14's seat checks. The cand texts are carried byte-verbatim per the series convention.
7. Memory-safety patch carried forward from kit-15/16/17: row_record_x0 clears the H cache per S inside the sweep; the engine block itself runs byte-verbatim. Values identical by construction; 4-run determinism + audit G7 full recompute confirm.
8. Battery size: this kit registers 64 new battery literals (2,226 total), the exact v-literal set of its binding+evenlife cand texts per the chain rule (kit-15/16/17 each added 64 the same way). derive_check_kit18.py reads the kit-17 published explorer `explore_m49m50_frontier_windows_evenlife.py` for the carried-battery comparison (not re-published in this kit dir; same practice as kit-15/16/17).
9. The generator (gen_kit18.py, not published but re-runnable from the kit-17 published bytes; transform_lib extended with the 38th/39th ordinal labels) asserts the full kit-17 record of record as a precondition (49 rows / 211 separations / 30 binding FULL HIT / evenlife 3/3 EXACT) before emitting any kit-18 row; the registration was machine-checked for zero self/earlier overlaps, and audit G16 checks all 49 kit-17 row names are absent here.
10. Hand-typed pins forbidden: every pin in this README was machine-extracted from the frozen files.

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 40/40, the rule-v2 shadow observations (including the early-follow 8/8 and boundary-equistack 4-observation series), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping. No K-slot claim is made.
