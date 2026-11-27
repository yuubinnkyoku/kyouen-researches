# kit-14: strip-newband m43/m44 frontier first-contact, ladder continuations to depth, rule-v2 standing enumeration, first m=41/m=42 in-band windows, and the even-m z=3m+8 next-depth lifecycle rows (2026-11-26)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-13 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

## Provenance

- kit-13 frozen registration source: `research/experiments/strip-newband-m41m42-frontier-windows-evenlife-20261126/` (commit `1a480530`, frozen .out sha256 `3798d2f0...`, kit-13 explorer sha256 `f0fb0220...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c1...`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-14 explorer: `explore_m43m44_frontier_windows_evenlife.py` sha256 `5c071e64...` (170,208 bytes).
- Frozen official output: `explore_m43m44_frontier_windows_evenlife.out` sha256 `5f985e73...` (353,101 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 4 byte-identical runs total (default; PYTHONHASHSEED=random; PYTHONHASHSEED=12345; post-verify fresh-cold). One run per shell command (see disclosure 1).
- derive_check: `derive_check_kit14.py` (engine-free, K0832 closed form only) 2,715 checks DERIVE-PASS, 0 fails.
- audit: `audit_kit14.py` 18/18 gates PASS, 2 runs byte-identical (`306cf5c6...`); tamper battery 3/3 fail-closed (T1 battery closed flip -> G3; T2 frontier m43 datum value flip -> G7+G9+G14; T3 anchor published_value flip -> G4).

## Measured census (49 rows, 136 separations)

- The 30 binding rows (28 ladder m=19..32 next-depth one-past/birth + 2 frontier) are ALL FULL HIT: every registered seat separates with exactly the registered value/direction, every rule-v2 stack split of every 2-token seat with co >= 2m is an exact numerical mimic of its host seat, and there are ZERO unregistered separations (97 separations in the binding rows, all registered or exact-mimic shadows).
- Frontier 30th/31st parity datums, FIRST-EVER m>42 rows, both EXACT:
  - m=43 @ z=85: seat {43,44} @S=87 UP 2v0 (collapse v(87,85,129)=0).
  - m=44 @ z=86: seat (44,44) @S=88 UP 2v1 (collapse v(88,86,131)=1).
  - Observation count only: the frontier parity scaffold is now 32/32 (m=13..44). NOT a law.
- Ladder continuations m=19..m=32 to the registered next depths (m19/m20 now at birth z=69/70, series-deepest). The early-follow observable is confirmed a 4th consecutive time from pre-registration: the m=19 z=68 one-past row carries the full 7-split shadow set of co=50 as exact mimics (host value 1) and m=20 z=69 the 6-split set (host value 0).
- In-band windows m=41 z{73..80} and m=42 z{74..81}: 16/16 rows CLEAN (zero separations). With the kit-13 frontier rows, the m=41 measured band is now {73..81} and the m=42 band {74..82}; z below the window remains unmeasured, unregistered.
- Even-m z=3m+8 lifecycle rows (m=14/16/18), NON-BINDING continuation registered contingent on the kit-13 z=3m+6 outcomes (3/3 EXACT): 3/3 EXACT again. Template: stick {m,2m+8} @S=3m+8 DOWN 0v2 + NEW {m,2m+10} @S=3m+10 UP 2v1 + 11 exact-mimic shadows per row (5 stick-side + 6 NEW-side splits) + trio {m,m,m} conform (absent) at z=3m+8. The even-m lifecycle chain now extends through z=3m+8 (observed z=3m-1..3m+8).
- k0832 battery: 1,970/1,970 literal triples (1,906 kit-13 carried + 64 new; every new literal satisfies closed == vC == vO).
- Published anchor rechecks: 733/733 spots reproduce exactly (616 kit-13 anchors byte-carried + the 117 kit-13 published census separation spots first-anchored here).
- Total separations 136 across 49 rows equals the data-driven registered count (every binding seat + every admissible rule-v2 split + the evenlife seats/splits; audit G8 recomputes this independently).

## Registration for kit-15 (engine-free, NOT measured here)

34 future constants registered in the frozen .out section
future_slice_registration_constants:
- 28 ladder next-depth one-past/birth pairs for m=19..m=32 (one depth beyond this kit, e.g. m19 one-past z=70 {19,52}@S=71, birth z=71 stick {19,52} + NEW {19,54}), rule-v2 stack lists included wherever co >= 2m.
- Frontier 32nd/33rd datum candidates: m=45 @ z=89 {45,46}@S=91 UP 2v0 (collapse v(91,89,135)=0) / m=46 @ z=90 (46,46)@S=92 UP 2v1 (collapse v(92,90,137)=1); z*(m)=2m-2+(m mod 2) per K1268, derive_check double-checked.
- In-band window sweep proposals: m=43 z{77..84}, m=44 z{78..85} (both NOT strip-covered).
- Even-m z=3m+10 continuation proposal (contingent on this kit's z=3m+8 outcomes, NON-BINDING) + odd-m close-out note.

## Honest disclosure

1. Sandbox reset mid-session: a shell command carrying TWO full explorer runs exceeded the 290 s wall and reset the execution environment, destroying the then-current local scratch (kit-13 SSOT copies, the first-built kit-14 explorer, and the first official run's .out; none of it was published). All kit-13 SSOTs were re-fetched and re-verified byte-exact (git blob sha 6/6), the explorer was regenerated from the pinned generator, and the entire pipeline (determinism, derive, audit, tamper) was re-executed from scratch on the post-reset bytes. Every published byte is post-reset. Lesson (fourth occurrence): one slow command per shell call.
2. Datum numbering: the kit-13 frozen .out labels its frontier rows m41/m42 as the 28th/29th parity datums, so this kit continues 30th/31st for m43/m44 (and registers 32nd/33rd for m45/m46). Earlier lane notes elsewhere used a different ad-hoc count; the frozen .out sequence is authoritative here.
3. The evenlife candidate texts in this kit carry numeric collapse literals (v(S,z,R)=c) where kit-13's used generic placeholders; both are derive-checked; the rows are NON-BINDING scaffold rows.
4. derive_check_kit14.py reads the kit-13 published explorer `explore_m41m42_frontier_windows.py` for the carried-battery comparison (not re-published in this kit dir; same practice as kit-13, which referenced `explore_kit12.py`).
5. The generator (gen_kit14.py) asserts the full kit-13 record of record as a precondition (49 rows / 117 separations / 30 binding FULL HIT / evenlife 3/3 EXACT) before emitting any kit-14 row; the registration was machine-checked for zero self/earlier overlaps, and audit G16 checks all 49 kit-13 row names are absent here.
6. Hand-typed pins forbidden: every pin in this README was machine-extracted from the frozen files.

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 32/32, the rule-v2 shadow observations (including the early-follow confirmations), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping.
