# kit-19: strip-newband m53/m54 frontier first-contact, ladder continuations to depth, rule-v2 standing enumeration, first m=51/m=52 in-band windows, and the even-m z=3m+18 next-depth lifecycle rows (2026-11-27)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-18 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

TAKEOVER PUBLICATION (disclosure 1): the kit-19 owner lane completed
generation, the 4-run determinism battery, both audit runs and tamper case T1,
then fell silent at ~03:37Z (execution wall). This publication was completed
by the concurrent kit-19x census lane per the kit-16 takeover precedent: NO
measurement was redone, the frozen bytes below are the owner lane's 4-run
battery, and the takeover work was the remaining verification (tamper T2/T3,
clean control, derive_check re-run) plus README/log/push.

## Provenance

- kit-18 frozen registration source: `research/experiments/strip-newband-m51m52-frontier-windows-evenlife-20261126/` (final wave commit 9ac8e079, frozen .out sha256 `c3087285fbdbd44d0588132f9c1d4c75fce2913b816ce383a5f0b377154364ba`, kit-18 explorer sha256 `b591e7e1...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-19 explorer: `explore_m53m54_frontier_windows_evenlife.py` sha256 `9a010e433d030f7a83672db0d9f50d3478152d516e4db17034b7a272ccf398f6` (342,886 bytes).
- Frozen official output: `explore_m53m54_frontier_windows_evenlife.out` sha256 `12277fd483aac7dfed4e3b687f3eb2433de44706d74377b08cd4c7db7acd623f` (626,727 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 4 byte-identical runs (sha256 above; run1..run4 status CHUNK-DONE, all 626,727 bytes, md5-identical across runs and equal to the frozen .out byte-for-byte). The sandbox wall (~280 s) is shorter than one full run, so all four runs were executed through a checkpointed chunked runner (disclosure 2).
- derive_check: `derive_check_kit19.py` (engine-free, K0832 closed form only) 3,533 checks DERIVE-PASS, 0 fails; re-run by the takeover lane 3 times, byte-identical output.
- audit: `audit_kit19.py` 20/20 gates PASS. Two runs by the owner lane (audit1/audit2, CHUNK-DONE rc=0, byte-identical json) plus a takeover-lane clean control through the checkpointed audit runner (caches capped at 200k, pure functions): AUDIT-PASS, byte-identical to the owner lane's two audit payloads (cmp-verified). Tamper battery 3/3 fail-closed (T1 battery closed flip -> G3, owner lane; T2 frontier m53 datum value flip -> G7+G9+G14, takeover lane; T3 anchor published_value flip -> G4, takeover lane); the frozen .out sha256 was re-verified unchanged after the battery.
- Independent blind second census: the concurrent lane published `research/experiments/strip-newband-m53m54-blind-second-census-20261127/` (kit-19x, commit f38d2b43), frozen BEFORE this kit's frozen .out was read by that lane, from a fresh harness and a fresh audit (its census sha256 `275faedc...`). Its pre-publication informational comparison against this kit's local frozen runs matched 49/49 rows and 273/273 separations exactly (fresh comparator, tamper-checked 3/3 fail-closed); this publication makes the authoritative published-vs-published cross-check possible.

## Measured census (49 rows, 273 separations)

- The 30 binding rows (28 ladder m=19..32 next-depth one-past/birth + 2 frontier) are ALL FULL HIT: every registered seat separates with exactly the registered value/direction, every rule-v2 stack split of every 2-token seat with co >= 2m is an exact numerical mimic of its host seat, and there are ZERO unregistered separations (204 separations in the binding rows: 202 ladder + 2 frontier, all registered or exact-mimic shadows).
- Frontier 40th/41st parity datums, FIRST-EVER m>52 rows, both EXACT:
  - m=53 @ z=105 (R=159): seat {53,54} @S=107 UP 2v0 (collapse v(107,105,159)=0). The sweep covers S in {53..107}, 3 shapes at the separation S.
  - m=54 @ z=106 (R=161): seat (54,54) @S=108 UP 2v1 (collapse v(108,106,161)=1).
  - Observation count only: the frontier parity scaffold is now 42/42 (m=13..54). NOT a law.
- Ladder continuations m=19..m=32 to the registered next depths (m19/m20 now at birth z=79/80, new series-deepest). The early-follow observable is confirmed a 9th consecutive time from pre-registration: the m=19 z=78 one-past row carries the full 12-split shadow set of co=60 as exact mimics (host {19,60} UP 1v0) and m=20 z=79 the 11-split set (host {20,60} DOWN 0v1).
- Boundary equistack, FIFTH OBSERVATION (co=2m exactly): at m=27 the birth NEW seat {27,54} @S=81 (co=54=2m, z=79 row) sits exactly on the boundary and the equistack {27,27,27} separates as an exact mimic of the seat (audit G13). Kit-15/16/17/18 observed the first four. Finite observation, no claim.
- In-band windows m=51 z{93..100} and m=52 z{94..101}: 16/16 rows CLEAN (zero separations). FIRST-EVER below-frontier m=51/m=52 rows; no strip-derivation claim is made (m=51/m=52 are NOT strip-covered). With the kit-18 frontier rows, the m=51 measured band is now {93..103} and the m=52 band {94..104}; z below the window remains unmeasured, unregistered.
- Even-m z=3m+18 lifecycle rows (m=14 z=60 / m=16 z=66 / m=18 z=72), NON-BINDING continuation registered contingent on the kit-18 z=3m+16 outcomes (3/3 EXACT): 3/3 EXACT again. Template: stick {m,2m+18} @S=3m+18 DOWN 0v2 + NEW {m,2m+20} @S=3m+20 UP 2v1 + exact-mimic shadows per row (splits(2m+18,m) + splits(2m+20,m), 11+12=23 per row at m=14/16/18) + trio {m,m,m} conform (absent) at z=3m+18; 23 separations per row, 69 total. The even-m lifecycle chain now extends through z=3m+18 (observed z=3m-1..3m+18).
- k0832 battery: 2,290/2,290 literal triples (2,226 kit-18 carried + 64 new; every new literal satisfies closed == vC == vO).
- Published anchor rechecks: 1,662/1,662 spots reproduce exactly (1,421 kit-18 anchors byte-carried + the 241 kit-18 published census separation spots first-anchored here).
- Total separations 273 across 49 rows equals the data-driven registered count (every binding seat + every admissible rule-v2 split + the evenlife seats/splits; audit G8 recomputes this independently).

## Registration for kit-20 (engine-free, NOT measured here)

34 future constants registered in the frozen .out section
future_slice_registration_constants:
- 28 ladder next-depth one-past/birth pairs for m=19..m=32 (one depth beyond this kit), rule-v2 stack lists included wherever co >= 2m, composed FRESH for the kit-20 seats.
- Frontier 42nd/43rd datum candidates: m=55 @ z=109 {55,56}@S=111 UP 2v0 (collapse v(111,109,165)=0) / m=56 @ z=110 (56,56)@S=112 UP 2v1 (collapse v(112,110,167)=1); z*(m)=2m-2+(m mod 2) per K1268, derive_check double-checked.
- In-band window sweep proposals: m=53 z{97..104}, m=54 z{98..105} (both NOT strip-covered).
- Even-m z=3m+20 continuation proposal (contingent on this kit's z=3m+18 outcomes, NON-BINDING) registered.

## Honest disclosure

1. TAKEOVER PUBLICATION: the kit-19 owner lane (single-owner of this kit's build) fell silent at ~03:37Z after completing generation, the 4-run determinism battery (all CHUNK-DONE rc=0, byte-identical), both audit runs (CHUNK-DONE rc=0, gates=20, byte-identical payloads) and tamper case T1 (fail-closed G3). Following the kit-16 takeover precedent the concurrent kit-19x census lane completed: tamper T2 (fail-closed G7+G9+G14; the T2 audit was resumed from the owner lane's checkpoint pkl state, a deterministic state-machine resume, disclosed), tamper T3 (fresh tamper file built with the exact t3() mutation, fail-closed G4 only), a clean control audit (AUDIT-PASS 20/20, byte-identical to the owner lane's audit payloads by cmp), derive_check re-runs (3,533 DERIVE-PASS, 3 identical invocations), this README/log, and the push waves. NO measurement, generation or freeze step was redone; the frozen bytes are the owner lane's 4-run battery (sha256 above, byte-verified by the takeover lane before publishing).
2. Execution-environment wall: this sandbox kills any process at ~280 s and the audit exceeds the wall, so audit runs and tamper audits were executed through the checkpointed audit runner (`audit_chunked_k19.py`, not published; mirrors audit_kit19.py gate-for-gate with caches capped at 200k entries - pure functions, values unchanged). One environment reset occurred during the takeover T3 audit's first invocation; the checkpoint pkl survived on the persistent mount and the audit resumed from it (disclosed; the result equals a fresh run by determinism, and the clean control below is a full independent third audit).
3. Tamper file provenance: T1 was fully executed by the owner lane (T1_audit.json AUDIT-FAIL G3 bad=1, exactly the expected gate); the takeover lane verified the T2 tampered file differed from the frozen .out in exactly one field (frontier_m53_z105_row_record separations[0].value 2->1) before auditing it; T3's tampered file was built by the takeover lane with the published t3() mutation (published_anchor_rechecks rows[500].published_value -> 7, single-field diff verified). All three cases failed exactly the expected gates and nothing else; the frozen .out sha256 was re-verified unchanged after the battery.
4. The frozen kit-18 prediction texts registered here omit the one-past stack lists (the birth texts carry them); the measured one-past shadow sets exactly match the standing rule-v2 admissible co-split enumeration (m19:12, m20:11, m21:7, m22:6, m23:5, m24:4, m25:3, m26:2, m27..32:0, each an exact mimic) and no other unregistered separation exists. This is a text-completeness property of the registration, disclosed as such; the kit-19x census (which received the same texts) reported the same measurement-side facts.
5. FRESH seat labels: the frozen kit-18 prediction texts registered here carry FRESH seat labels (kit-18 received FRESH from kit-17 and emitted FRESH); freshness is ASSERTED in derive_check and in audit G14's seat checks. The cand texts are carried byte-verbatim per the series convention.
6. Memory-safety patch carried forward from kit-15..18: row_record_x0 clears the H cache per S inside the sweep; the engine block itself runs byte-verbatim. Values identical by construction; 4-run determinism + audit G7 full recompute confirm.
7. Battery size: this kit registers 64 new battery literals (2,290 total), the exact v-literal set of its binding+evenlife cand texts per the chain rule (kit-15..18 each added 64 the same way). derive_check_kit19.py reads the kit-18 published explorer for the carried-battery comparison (not re-published in this kit dir; same practice as kit-15..18).
8. The generator (gen_kit19.py, not published but re-runnable from the kit-18 published bytes; transform_lib extended with the 40th/41st ordinal labels) asserts the full kit-18 record of record as a precondition (49 rows / 241 separations / 30 binding FULL HIT / evenlife 3/3 EXACT) before emitting any kit-19 row; the registration was machine-checked for zero self/earlier overlaps, and audit G16 checks all 49 kit-18 row names are absent here.
9. Hand-typed pins forbidden: every pin in this README was machine-extracted from the frozen files.

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 42/42, the rule-v2 shadow observations (including the early-follow 9/9 and boundary-equistack 5-observation series), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping. No K-slot claim is made.
