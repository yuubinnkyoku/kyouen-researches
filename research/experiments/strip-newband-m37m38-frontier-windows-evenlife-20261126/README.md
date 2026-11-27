# kit-11: strip-newband m37/m38 frontier first-contact, ladder continuations to depth, rule-v2 early-follow shadows pre-registered, first m=35/m=36 in-band windows, and the even-m z=3m+2 next-depth lifecycle rows (2026-11-26)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-10 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

## Provenance

- kit-10 frozen registration source: `research/experiments/strip-newband-m35m36-frontier-windows-evenlife-20261126/` (commit `a0166a12`, frozen .out sha256 `31dc6b2a...`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c1...`, embedded ENGINE_BLOCK pin `bd5f22e4...`, asserted in-explorer at run time).
- This kit-11 explorer: `explore_m37m38_frontier_windows.py` sha256 `1cb7d53e...` (111,770 bytes).
- Frozen official output: `explore_m37m38_frontier_windows.out` sha256 `3f2cc395...` (252,545 bytes, one JSON line, sort_keys separators-compact).
- Determinism: 8 byte-identical runs total (default x2, PYTHONHASHSEED=random, PYTHONHASHSEED=12345, env -i x2, push-time rerun, post-reset fresh-cold run after the sandbox reset noted below).
- Audit: `audit_kit11.py` 18/18 gates PASS, 2 runs byte-identical + clean control byte-identical. Tamper battery 3/3 fail-closed (battery-literal flip rc=1 -> G3; anchor-value flip rc=1 -> G4+G5; phantom window separation rc=1 -> G7+G11), frozen bytes restored and verified after each.
- Derive check: `derive_check_kit11.py` DERIVE-PASS, 2,237 engine-free arithmetic checks, 0 fails, 2 runs byte-identical (plus a fail-closed catch record: see disclosures).

## Rows measured (47 row records, 86 separations total)

1. 28 binding rows (26 ladder continuation rows m=19..m=32 at the registered slices + 2 binding frontier first-contact rows). ALL 28 FULL HIT: every registered seat separated exactly as predicted (value + collapse + direction), zero unregistered separations beyond the rule-v2 shadow track. The two kit-10 self-overlap registrations (m31 z=66 / m32 z=67, already measured by kit-10 as ladder_m31_z66 / ladder_m32_z67) were SKIPPED per the kit-9b/kit-10 duplicate-skip precedent and are NOT re-measured here (audit gate G16).
2. Frontier first-contact rows: m=37 @ z=73 EXACTLY ONE {37,38}@S=75 UP 2v0 (collapse v(75,73,111)=0) and m=38 @ z=74 EXACTLY ONE (38,38)@S=76 UP 2v1 (collapse v(76,74,113)=1). Both EXACT - the 25th/26th K1268 parity datum candidates hit, the FIRST-EVER m>36 rows. Frontier parity-scaffold observation count now 26/26 (m=13..38) - a finite observation count, NOT a law.
3. 16 in-band window rows: m=35 z in {61..68} and m=36 z in {62..69}. All 16 rows CLEAN (0 separations). m=35 measured line is now z in {61..69}, m=36 is z in {62..70}; the bands z in {25..60} / {25..61} remain unmeasured and unregistered.
4. 3 NON-BINDING even-m next-depth lifecycle rows (m=14/16/18, z=3m+2), contingent on the kit-10 even-m lifecycle chain (9/9 EXACT). All 3 rows measured the parity-flipped template EXACTLY: stick {m,2m+2}@S=3m+2 DOWN 0v2 + both rule-v2 stick-side split stacks as exact mimics, NEW {m,2m+4}@S=3m+4 UP 2v1 + all three rule-v2 NEW-side split stacks as exact mimics, trio {m,m,m} conform (absent, terminus precedent). The even-m lifecycle chain now extends one registered depth further (z=3m-1..3m+2 measured per m=14/16/18).

## Headline structural results (finite observations, no universal claim)

- EARLY-FOLLOW OBSERVABLE CONFIRMED AS PRE-REGISTERED: at the m=19 z=62 one-past row the upcoming stick seat's full admissible split stack set ({19,19,25},{19,20,24},{19,21,23},{19,22,22} @S=63) separated as exact numeric mimics of the one-past host seat (UP 1v0) one slice BEFORE the stick slice; likewise m=20 z=63 (3 stacks @S=64, DOWN 0v1). Kit-10 observed this post-hoc at m=19 z=60; kit-11 registered the m19/m20 one-past shadow sets BEFORE the run and both measured as predicted. Combined with the z=63/z64 birth rows (stick-side co=44 stacks + NEW-side co=46 stacks, all exact mimics), the rule-v2 shadow family is now observed to track its host at every slice where the host separates, in every measured slice of the m19/m20 ladders (finite observation, not a law).
- RULE v2 both-side enumeration completed at the m=19/m20 z=63/z=64 births: stick seats (co=44) and NEW seats (co=46) each carry their full admissible split stacks as exact mimics; no other 3-token separations exist in any measured row (audit G13/G14).
- Ladder depths: m19/m20 ladders measured through the z=63/z=64 births ({19,46}@S=65 UP 2v0 / {20,46}@S=66 UP 2v1), one registered depth beyond kit-10's d=12 births; m21/m22 through z=59/60, m23/m24 through z=61/62, m25/m26 through z=63/64, m27/m28 through z=63/64, m29/m30 through z=69/70, m31/m32 through z=67/68.
- Kit-12 future constants: 34 items registered in the frozen .out (next one-past/birth pair per m=19..32, frontier 27th/28th candidates m=39@z=77 {39,40}@79 UP 2v0 / m=40@z=78 (40,40)@80 UP 2v1 per K1268 z*(m)=2m-2+(m mod 2), window proposals m=37 z in {65..72} / m=38 z in {66..73}, even/odd lifecycle continuation and close-out notes).

## Numbers

- K0832 battery: 1,702 literals (1,604 kit-10 carried + 98 new kit-11 literals), closed == vC == vO all, bad 0.
- Anchor rechecks: 429/429 spots reproduce published values exactly (334 kit-10 anchors byte-carried + 95 kit-10 published census separation spots first-anchored here).
- Row records: 47 (26 ladder + 2 frontier + 3 evenlife + 16 windows). Separations: 86. All measured separations accounted: registered seats, rule-v2 shadow stacks, or the pre-registered families (zero contradictions, zero unregistered residuals; audit gates G13/G14).

## Dated disclosures

1. kit-10 SELF-OVERLAP registrations detected and skipped: the kit-10 frozen future constants registered m31 z=66 and m32 z=67 for kit-11, but kit-10 itself had already measured those exact slices in its own binding rows (ladder_m31_z66_row_record / ladder_m32_z67_row_record). This is the first observed self-overlap of a registration source against its own measured territory (the kit-9/kit-9b precedent was an overlap with the PREVIOUS kit). Skipped per the standing duplicate-skip protocol; audit gate G16 asserts the non-remeasurement. Lesson (extends the standing rule): the K(n) build-time duplicate check must cross the registration source's own binding rows, not only earlier kits' measured slices.
2. Build-time derive-check fail-closed catches (all fixed BEFORE the freeze; the frozen bytes are the final state only): (a) the machine-generated kit-12 one-past prediction texts initially had a substitution-order bug (the '=c' replacement consuming the '=cd' placeholder) that produced a wrong dead-seat collapse literal - caught by the engine-free literal check; (b) the frontier 27th/28th candidates were initially generated at z=75/76, but K1268 gives z*(39)=2*39-2+1=77 and z*(40)=2*40-2+0=78 - caught by the K1268 arithmetic checks and corrected before any run; (c) a z-sanity threshold was too strict for the shallow kit-12 rows (z=60/61). None of these entered the frozen .out; the kit-12 constants embedded in the frozen .out are the corrected machine-derived values.
3. Sandbox reset during the tamper battery (a 250s shell timeout on a command that ran three tampered audits in sequence) discarded the working directory. All primary artifacts were recovered byte-exact from the persistent backup directory (explorer 1cb7d53e..., frozen .out 3f2cc395...) and every verification was re-executed post-reset: derive-check 2 runs byte-identical DERIVE-PASS, audit 2 runs byte-identical 18/18 PASS, tamper battery 3/3 fail-closed (one audit per command), clean control rc=0 byte-identical, and a post-reset fresh-cold determinism run byte-identical to the frozen .out. No partial or suspect bytes entered the frozen .out. Lesson reconfirmed: one slow command per shell call; back up primary artifacts to the persistent directory after every freeze step (this kit did so and lost nothing).

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a non-ASCII byte scan before push; a hard gate at push assembly). The log file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only. The frontier parity count 26/26, the rule-v2 shadow observations (including the early-follow confirmation), and the even-m lifecycle template are observation counts, not laws. The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. Nodes and shape counts are bookkeeping.
