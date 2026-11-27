# kit-12: strip-newband m39/m40 frontier first-contact, ladder continuations to depth, rule-v2 early-follow shadows pre-registered, first m=37/m=38 in-band windows, and the even-m z=3m+4 next-depth lifecycle rows (2026-11-26)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-11 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

## Provenance

- kit-11 frozen registration source: `research/experiments/strip-newband-m37m38-frontier-windows-evenlife-20261126/` (commit `44a36e35`, frozen .out sha256 `3f2cc395...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c1...`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-12 explorer: `explore_m39m40_frontier_windows.py` sha256 `60fe1249...` (129,051 bytes).
- Frozen official output: `explore_m39m40_frontier_windows.out` sha256 `94759406...` (283,254 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 6 byte-identical runs total (default x2, PYTHONHASHSEED=random, PYTHONHASHSEED=12345, env -i, post-reset fresh-cold run after the sandbox reset noted below).
- Audit: `audit_kit12.py` 18/18 gates PASS, 2 runs byte-identical + clean control byte-identical. Tamper battery 3/3 fail-closed (frontier-datum value flip rc=1 -> G7+G9; window-row deletion rc=1 -> fail-closed KeyError on the missing section; battery-literal flip rc=1 -> G3), clean control rc=0 byte-identical after the battery. One audit per shell command.
- Derive check: `derive_check_kit12.py` DERIVE-PASS, 2,387 engine-free arithmetic checks, 0 fails.

## Rows measured (49 row records, 101 separations total)

1. 30 binding rows (28 ladder continuation rows m=19..m=32 at the registered one-past/birth slices + 2 binding frontier first-contact rows). ALL 30 FULL HIT: every registered seat separated exactly as predicted (value + collapse + direction), zero unregistered separations beyond the rule-v2 shadow track. The kit-11 registration was machine-checked at build to contain zero self/earlier overlaps (the kit-10 self-overlap precedent asserted absent); zero rows skipped, nothing re-measured (audit gate G16).
2. Frontier first-contact rows: m=39 @ z=77 EXACTLY ONE {39,40}@S=79 UP 2v0 (collapse v(79,77,117)=0) and m=40 @ z=78 EXACTLY ONE (40,40)@S=80 UP 2v1 (collapse v(80,78,119)=1). Both EXACT - the 27th/28th K1268 parity datum candidates hit, the FIRST-EVER m>38 rows. Frontier parity-scaffold observation count now 28/28 (m=13..40) - a finite observation count, NOT a law.
3. 16 in-band window rows: m=37 z in {65..72} and m=38 z in {66..73}. All 16 rows CLEAN (0 separations). The m=37 measured line is now z in {65..73} and m=38 is z in {66..74} (frontier rows measured by kit-11); the bands z in {25..64} / {25..65} remain unmeasured and unregistered.
4. 3 NON-BINDING even-m next-depth lifecycle rows (m=14/16/18, z=3m+4), contingent on the kit-11 even-m lifecycle chain (z=3m+2 3/3 EXACT). All 3 rows measured the parity-flipped template EXACTLY: stick {m,2m+4}@S=3m+4 DOWN 0v2 + all three rule-v2 stick-side split stacks as exact mimics, NEW {m,2m+6}@S=3m+6 UP 2v1 + all four rule-v2 NEW-side split stacks as exact mimics, trio {m,m,m} conform (absent, z=3m+2 precedent). The even-m lifecycle chain now extends one registered depth further (z=3m-1..3m+4 measured per m=14/16/18).

## Headline structural results (finite observations, no universal claim)

- EARLY-FOLLOW OBSERVABLE CONFIRMED AGAIN AS PRE-REGISTERED: at the m=19 z=64 one-past row the upcoming stick seat's full admissible split stack set ({19,19,27},{19,20,26},{19,21,25},{19,22,24},{19,23,23} @S=65) separated as exact numeric mimics of the one-past host seat (UP 1v0) one slice BEFORE the stick slice; likewise m=20 z=65 (4 stacks @S=66, DOWN 0v1). This is the second consecutive pre-registered confirmation (kit-11 first confirmed it at m19 z62 / m20 z63; here the next-depth one-past slices m19 z64 / m20 z65 hit the same way). Combined with the z=65/z66 birth rows (stick-side co=46 stacks 4 and NEW-side co=48 stacks 6 at m=19, all exact mimics), the rule-v2 shadow family is observed to track its host at every measured slice of the m19/m20 ladders through z=66 (finite observation, not a law).
- RULE v2 both-side enumeration at the m=19/m20 z=65/z66 births: stick seats (co=46) and NEW seats (co=48) each carry their full admissible split stacks as exact mimics; no other 3-token separations exist in any measured row (audit G13/G14).
- Ladder depths: m19/m20 ladders measured through the z=65/z66 births ({19,48}@S=67 UP 2v0 / {20,48}@S=68 UP 2v1), one registered depth beyond kit-11's z=63/z=64 births; m21/m22 through z=61/62, m23/m24 through z=62/63, m25/m26 through z=64/65, m27/m28 through z=64/65, m29/m30 through z=70/71, m31/m32 through z=68/69.
- Kit-13 future constants: 34 items registered in the frozen .out (next one-past/birth pair per m=19..32, frontier 29th/30th candidates m=41@z=81 {41,42}@83 UP 2v0 / m=42@z=82 (42,42)@84 UP 2v1 per K1268 z*(m)=2m-2+(m mod 2), window proposals m=39 z in {69..76} / m=40 z in {70..77}, even/odd lifecycle continuation and close-out notes).

## Numbers

- K0832 battery: 1,804 literals (1,702 kit-11 carried + 102 new kit-12 literals), closed == vC == vO all, bad 0.
- Anchor rechecks: 515/515 spots reproduce published values exactly (429 kit-11 anchors byte-carried + 86 kit-11 published census separation spots first-anchored here).
- Row records: 49 (28 ladder + 2 frontier + 3 evenlife + 16 windows). Separations: 101. All measured separations accounted: registered seats, rule-v2 shadow stacks, or the pre-registered families (zero contradictions, zero unregistered residuals; audit gates G13/G14).

## Dated disclosures

1. Build-time fail-closed catches (all fixed BEFORE the freeze; the frozen bytes are the final state only): (a) the first generated explorer still measured the m=35/m=36 window slices because the main-region window loop bodies carried the kit-11 m values - caught immediately by the run output section names (inband_m35/m36) before any freeze, and the corrected explorer re-measures the intended m=37/m=38 windows; (b) the same catch showed the s_domain/co_token window metadata needed the m=37/m=38 update. No already-published slice was re-measured in the frozen run: the buggy pre-freeze run is discarded, not published, and audit gate G16 asserts the non-remeasurement against the frozen .out.
2. Sandbox reset during the tamper battery (a 260s shell timeout on a command that ran two audits plus a tampered audit in sequence) discarded the working directory. All primary artifacts were recovered byte-exact from the persistent backup directory (explorer 60fe1249..., frozen .out 94759406...) and every verification was re-executed post-reset from the published kit-11 sources + the backup: derive-check DERIVE-PASS 2,387 checks, audit 2 runs byte-identical 18/18 PASS, tamper battery 3/3 fail-closed (one audit per command), clean control rc=0 byte-identical, and a post-reset fresh-cold determinism run byte-identical to the frozen .out (the 6th determinism run). No partial or suspect bytes entered the frozen .out. Lesson reconfirmed a second time: one slow command per shell call; back up primary artifacts to the persistent directory after every freeze step.

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 28/28, the rule-v2 shadow observations (including the early-follow confirmations), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping.
