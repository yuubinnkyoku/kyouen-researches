# kit-13: strip-newband m41/m42 frontier first-contact, ladder continuations to depth, rule-v2 early-follow shadows pre-registered, first m=39/m=40 in-band windows, and the even-m z=3m+6 next-depth lifecycle rows (2026-11-26)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-12 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

## Provenance

- kit-12 frozen registration source: `research/experiments/strip-newband-m39m40-frontier-windows-evenlife-20261126/` (commit `0f6c44dc`, frozen .out sha256 `94759406...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c1...`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-13 explorer: `explore_m41m42_frontier_windows.py` sha256 `f0fb0220...` (147,812 bytes).
- Frozen official output: `explore_m41m42_frontier_windows.out` sha256 `3798d2f0...` (317,247 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 3 byte-identical runs total (default x2 pre-freeze; post-reset fresh-cold run after the sandbox reset noted below, byte-identical to the frozen .out).
- Audit: `audit_kit13.py` 18/18 gates PASS, 2 runs byte-identical. Tamper battery 3/3 fail-closed (battery-literal flip rc=1 -> G3; anchor-value flip rc=1 -> G4+G5; frontier-datum collapse flip rc=1 -> G7+G9), one audit per shell command.
- Derive check: `derive_check_kit13.py` DERIVE-PASS, 2,631 engine-free arithmetic checks, 0 fails (run BEFORE the freeze and re-executed post-reset identically).

## Rows measured (49 row records, 117 separations total)

1. 30 binding rows (28 ladder continuation rows m=19..m=32 at the registered one-past/birth slices + 2 binding frontier first-contact rows). ALL 30 FULL HIT: every registered seat separated exactly as predicted (value + collapse + direction), zero unregistered separations beyond the rule-v2 shadow track. The kit-12 registration was machine-checked at build to contain zero self/earlier overlaps; zero rows skipped, nothing re-measured (audit gate G16).
2. Frontier first-contact rows: m=41 @ z=81 EXACTLY ONE {41,42}@S=83 UP 2v0 (collapse v(83,81,123)=0) and m=42 @ z=82 EXACTLY ONE (42,42)@S=84 UP 2v1 (collapse v(84,82,125)=1). Both EXACT - the 29th/30th K1268 parity datum candidates hit, the FIRST-EVER m>40 rows. Frontier parity-scaffold observation count now 30/30 (m=13..42) - a finite observation count, NOT a law.
3. 16 in-band window rows: m=39 z in {69..76} and m=40 z in {70..77}. All 16 rows CLEAN (0 separations). The m=39 measured line is now z in {69..77} and m=40 is z in {70..78} (frontier rows measured by kit-12); the bands z in {25..68} / {25..69} remain unmeasured and unregistered.
4. 3 NON-BINDING even-m next-depth lifecycle rows (m=14/16/18, z=3m+6), contingent on the kit-12 even-m lifecycle chain (z=3m+4 3/3 EXACT). All 3 rows measured the parity-flipped template EXACTLY: stick {m,2m+6}@S=3m+6 DOWN 0v2 + all four rule-v2 stick-side split stacks as exact mimics, NEW {m,2m+8}@S=3m+8 UP 2v1 + all five rule-v2 NEW-side split stacks as exact mimics, trio {m,m,m} conform (absent, z=3m+4 precedent). The even-m lifecycle chain now extends one registered depth further (z=3m-1..3m+6 measured per m=14/16/18).

## Headline structural results (finite observations, no universal claim)

- EARLY-FOLLOW OBSERVABLE CONFIRMED A THIRD TIME AS PRE-REGISTERED: at the m=19 z=66 one-past row the upcoming stick seat's full admissible split stack set ({19,19,29},{19,20,28},{19,21,27},{19,22,26},{19,23,25},{19,24,24} @S=67) separated as exact numeric mimics of the one-past host seat (UP 1v0) one slice BEFORE the stick slice; likewise m=20 z=67 (5 stacks @S=70, DOWN 0v1). Third consecutive pre-registered confirmation (kit-11 at m19 z=62, kit-12 at m19 z=64, kit-13 at m19 z=66). Combined with the z=67/z=68 birth rows (stick-side co=48 stacks 6 and NEW-side co=50 stacks 7 at m=19; 5 and 6 at m=20, all exact mimics), the rule-v2 shadow family is observed to track its host at every measured slice of the m19/m20 ladders through z=68 (finite observation, not a law).
- RULE v2 both-side enumeration at the m=19/m=20 z=67/z=68 births: stick seats (co=48) and NEW seats (co=50) each carry their full admissible split stacks as exact mimics; no other 3-token separations exist in any measured row (audit G13/G14).
- Ladder depths: m19/m20 ladders measured through the z=67/z=68 births ({19,50}@S=69 UP 2v0 / {20,50}@S=70 UP 2v1), one registered depth beyond kit-12's z=65/z=66 births; m21/m22 through z=63/64, m23/m24 through z=65/66, m25/m26 through z=67/68, m27/m28 through z=67/68, m29/m30 through z=73/74, m31/m32 through z=71/72.
- Kit-14 future constants: 34 items registered in the frozen .out (next one-past/birth pair per m=19..32, frontier 31st/32nd candidates m=43@z=85 {43,44}@87 UP 2v0 / m=44@z=86 (44,44)@88 UP 2v1 per K1268 z*(m)=2m-2+(m mod 2), window proposals m=41 z in {73..80} / m=42 z in {74..81}, even/odd lifecycle continuation and close-out notes).

## Numbers

- K0832 battery: 1,906 literals (1,804 kit-12 carried + 102 new kit-13 literals), closed == vC == vO all, bad 0.
- Anchor rechecks: 616/616 spots reproduce published values exactly (515 kit-12 anchors byte-carried + 101 kit-12 published census separation spots first-anchored here).
- Row records: 49 (28 ladder + 2 frontier + 3 evenlife + 16 windows). Separations: 117. All measured separations accounted: registered seats, rule-v2 shadow stacks, or the pre-registered families (zero contradictions, zero unregistered residuals; audit gates G13/G14).

## Dated disclosures

1. Build-time fail-closed catches (all caught by the byte-validation gates BEFORE the freeze; the frozen bytes are the final state only): (a) a dead-seat regex group off-by-one and a docstring extraction bug in the builder were caught by V1 (parse of the kit-11 registration failed to byte-reproduce the published kit-12 binding); (b) the birth-row generator initially used the previous stick co and the z+1 depth - caught by V2 (byte-mismatch against the published kit-12 future constants) and corrected to stick co = previous NEW co, depth z+2; (c) the frontier generator initially emitted S=2m+1 unconditionally - caught by V2 (m=42 row mismatch) and corrected to the parity-dependent S=2m+1 (odd) / 2m (even); (d) the note generator initially attached a 'z' key to the two lifecycle notes - caught by V2 against the published kit-12 note items. None of these states reached a run or a freeze.
2. Sandbox reset during the tamper battery (a 290s shell timeout on a command that ran three tampered audits in sequence) discarded the working directory. All primary artifacts were regenerated deterministically from the published kit-12/kit-11 sources: the rebuilt explorer is byte-identical to the pre-reset build (f0fb0220...) and the fresh-cold run is byte-identical to the pre-reset frozen .out (3798d2f0...). Every verification was re-executed post-reset: derive-check DERIVE-PASS 2,631 checks, audit 2 runs byte-identical 18/18 PASS, tamper battery 3/3 fail-closed (one audit per command). No partial or suspect bytes entered the frozen .out. Lesson (third occurrence): one slow command per shell call.
3. Hand-typed pins forbidden: every pin in this README/log was machine-extracted from the frozen files.

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 30/30, the rule-v2 shadow observations (including the early-follow confirmations), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping.
