# kit-13: strip-newband m41/m42 frontier first-contact, ladder continuations to depth, pre-registered early-follow shadows, first m=39/m=40 in-band windows, and the even-m z=3m+6 next-depth lifecycle rows (2026-11-26)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-12 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

## Provenance

- kit-12 frozen registration source: `research/experiments/strip-newband-m39m40-frontier-windows-evenlife-20261126/` (commit `0f6c44dc`, frozen .out sha256 `94759406...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c1...`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-13 explorer: `explore_m41m42_frontier_windows.py` sha256 `2d136b01...` (153,304 bytes).
- Frozen official output: `explore_m41m42_frontier_windows.out` sha256 `390b2ade...` (320,775 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 5 byte-identical runs total (default x2, PYTHONHASHSEED=random, PYTHONHASHSEED=12345, env -i).
- Audit: `audit_kit13.py` 18/18 gates PASS on the frozen .out. Tamper battery 3/3 fail-closed (T1 battery-literal closed-value flip -> G3; T2 frontier m41 datum value flip -> G7/G9; T3 anchor value flip -> G4/G5), clean control rc=0 byte-identical after each battery. One audit per shell command.
- Derive check: `derive_check_kit13.py` DERIVE-PASS, 2,617 engine-free arithmetic checks, 0 fails (pre-freeze and re-executed on the final bytes).

## Rows measured (49 row records, 117 separations total)

1. 30 binding rows (28 ladder continuation rows m=19..m=32 at the registered one-past/birth slices + 2 binding frontier first-contact rows). ALL 30 FULL HIT: every registered seat separated exactly as predicted (value + collapse + direction), zero unregistered separations beyond the rule-v2 shadow track. The kit-12 registration was machine-checked at build to contain zero self/earlier overlaps; zero rows skipped, nothing re-measured (audit gate G16).
2. Frontier first-contact rows: m=41 @ z=81 EXACTLY ONE {41,42}@S=83 UP 2v0 (collapse v(83,81,123)=0) and m=42 @ z=82 EXACTLY ONE (42,42)@S=84 UP 2v1 (collapse v(84,82,125)=1). Both EXACT - the 29th/30th K1268 parity datum candidates hit, the FIRST-EVER m>40 rows. Frontier parity-scaffold observation count now 30/30 (m=13..42) - a finite observation count, NOT a law.
3. 16 in-band window rows: m=39 z in {69..76} and m=40 z in {70..77}. All 16 rows CLEAN (0 separations). The m=39 measured line is now z in {69..77} and m=40 is z in {70..78} (frontier rows measured by kit-12); the bands z in {25..68} / {25..69} remain unmeasured and unregistered.
4. 3 NON-BINDING even-m next-depth lifecycle rows (m=14/16/18, z=3m+6), contingent on the kit-12 even-m lifecycle chain (z=3m+4 3/3 EXACT). All 3 rows measured the parity-flipped template EXACTLY: stick {m,2m+6}@S=3m+6 DOWN 0v2 + all four rule-v2 stick-side split stacks as exact mimics, NEW {m,2m+8}@S=3m+8 UP 2v1 + all five rule-v2 NEW-side split stacks as exact mimics, trio {m,m,m} conform (absent). The even-m lifecycle chain now extends one registered depth further (z=3m-1..3m+6 measured per m=14/16/18).

## Headline structural results (finite observations, no universal claim)

- EARLY-FOLLOW OBSERVABLE CONFIRMED A THIRD TIME AS PRE-REGISTERED: at the m=19 z=66 one-past row the upcoming stick seat's full admissible split stack set ({19,19,29},{19,20,28},{19,21,27},{19,22,26},{19,23,25},{19,24,24} @S=67) separated as exact numeric mimics of the one-past host seat (UP 1v0) one slice BEFORE the stick slice; likewise m=20 z=67 (5 stacks @S=68, DOWN 0v1). This is the third consecutive pre-registered confirmation (kit-11 at m19 z62/m20 z63, kit-12 at m19 z64/m20 z65, here at m19 z66/m20 z67). Combined with the z=67/z68 birth rows (stick-side co=48 stacks 5 and NEW-side co=50 stacks 6 at m=19, all exact mimics), the rule-v2 shadow family is observed to track its host at every measured slice of the m19/m20 ladders through z=68 (finite observation, not a law).
- RULE v2 both-side enumeration at the m=19/m20 z=67/z68 births: stick seats (co=48) and NEW seats (co=50) each carry their full admissible split stacks as exact mimics; no other 3-token separations exist in any measured row (audit G13/G14).
- Ladder depths: m19/m20 ladders measured through the z=67/z68 births ({19,50}@S=69 UP 2v0 / {20,50}@S=70 UP 2v1), one registered depth beyond kit-12's z=65/z66 births; m21/m22 through z=62/63, m23/m24 through z=64/65, m25/m26 through z=66/67, m27/m28 through z=67/68, m29/m30 through z=72/73, m31/m32 through z=70/71.
- Kit-14 future constants: 34 items registered in the frozen .out (next one-past/birth pair per m=19..32, frontier 31st/32nd candidates m=43@z=85 {43,44}@S=87 UP 2v0 / m=44@z=86 (44,44)@S=88 UP 2v1 per K1268 z*(m)=2m-2+(m mod 2), window proposals m=41 z in {73..80} / m=42 z in {74..81}, even/odd lifecycle continuation and close-out notes).

## Numbers

- K0832 battery: 1,906 literals (1,804 kit-12 carried + 102 new kit-13 literals), closed == vC == vO all, bad 0.
- Anchor rechecks: 616/616 spots reproduce published values exactly (515 kit-12 anchors byte-carried + 101 kit-12 published census separation spots first-anchored here).
- Row records: 49 (28 ladder + 2 frontier + 3 evenlife + 16 windows). Separations: 117. All measured separations accounted: registered seats, rule-v2 shadow stacks, or the pre-registered families (zero contradictions, zero unregistered residuals; audit gates G13/G14).

## Dated disclosures

1. Build-time fail-closed catches (all fixed BEFORE the freeze; the frozen bytes are the final state only): (a) the generator's birth-row seat annotation wrote the stick seat labels as "DOWN 1v1"/"DOWN 0v0" instead of the correct "DOWN 1v2"/"DOWN 0v2" (a regex group-index slip in the label assembly; the binding prediction texts and all arithmetic were correct throughout). Caught by audit gate G14 (seat-label semantics vs measured value/collapse) on the first full run; the labels were corrected, the explorer regenerated, and the ENTIRE pipeline re-executed on the final bytes (determinism 5 walks, derive-check 2,617 PASS, audit 18/18 PASS, tamper 3/3). The first (pre-fix) run is discarded, not published. (b) The generator's first explorer emission carried no main() (a patch step failed with ValueError); main() was reconstructed from the kit-12 template and verified by AST parse plus the run itself before any freeze.
2. The user's computer was unreachable for this session (GitHub API publication only, standing disclosure of the hourly-lane environment).

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 30/30, the rule-v2 shadow observations (including the early-follow confirmations), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping.
