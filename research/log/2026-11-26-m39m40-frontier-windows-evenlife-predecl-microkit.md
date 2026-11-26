# 2026-11-26 kit-12: strip-newband m39/m40 frontier first-contact + ladder continuations + pre-registered early-follow shadows + m37/m38 windows + even-m z=3m+4 next-depth (pre-declaration micro-kit)

## S1 Provenance and protocol

- Registration source: the kit-11 frozen output section future_slice_registration_constants (commit 44a36e35, .out pin 3f2cc395..., 34 items), byte-verbatim prediction texts.
- Build: machine assembly from the kit-11 artifacts (engine block byte-clone 582c93c1... / embedded pin bd5f22e4..., anchors 429 byte-carried, battery 1,702 carried). Builder: build_kit12.py (not published; every published byte is regenerable from the kit-11 published artifacts by the documented recipe).
- Pre-declaration: every binding row was frozen inside the explorer BEFORE the official run; derive_check_kit12.py ran BEFORE the official run and gated the freeze (DERIVE-PASS, 2,387 checks).
- Official run: 6 byte-identical determinism walks (default x2, PYTHONHASHSEED=random, PYTHONHASHSEED=12345, env -i, post-reset fresh-cold), frozen .out = run 1 bytes (sha256 94759406...).
- Audit: audit_kit12.py 18/18 gates PASS, 2 runs byte-identical, clean control byte-identical, tamper battery 3/3 fail-closed (T1 frontier-datum value flip -> G7+G9; T2 window-row deletion -> fail-closed KeyError rc=1 on the missing section; T3 battery-literal flip -> G3), clean control rc=0 after the battery.

## S2 Measured rows (49 row records, 101 separations)

1. 28 binding ladder continuation rows m=19..m=32 at the kit-11 registered slices: ALL 28 FULL HIT (registered seats exact value/collapse/direction, rule-v2 shadows exact mimics, zero unregistered residuals). Zero rows skipped: the kit-11 registration was machine-checked at build to contain no self/earlier overlaps (the kit-10 self-overlap precedent asserted absent).
2. 2 binding frontier first-contact rows: m=39@z=77 EXACTLY ONE {39,40}@S=79 UP 2v0 (collapse v(79,77,117)=0) and m=40@z=78 EXACTLY ONE (40,40)@S=80 UP 2v1 (collapse v(80,78,119)=1). BOTH EXACT: the 27th/28th parity datums, first-ever m>38 rows. Scaffold observation count 28/28 (m=13..40). Finite observation, NOT a law.
3. 16 window rows m=37 z{65..72} / m=38 z{66..73}: ALL CLEAN. m=37 measured line z{65..73}, m=38 z{66..74} (frontier rows measured by kit-11); below-frontier bands z{25..64} / {25..65} remain unmeasured, unregistered.
4. 3 NON-BINDING even-m next-depth rows (m=14/16/18, z=3m+4): ALL 3 measured the parity-flipped template EXACTLY (stick {m,2m+4} DOWN 0v2 + 3 stick-side stacks as mimics; NEW {m,2m+6} UP 2v1 + 4 NEW-side stacks as mimics; trio conform/absent). Even-m lifecycle chain: z=3m-1..3m+4 now measured per m=14/16/18.

## S3 Headline structural observations (finite, no universal claim)

- EARLY-FOLLOW CONFIRMED A SECOND TIME AS PRE-REGISTERED: kit-11 first confirmed (m19 z=62 / m20 z=63); kit-12 registered the NEXT one-past shadow sets (m19 z=64 / m20 z=65) before the run and both measured exactly (m19 z=64: 5 stacks @S=65 UP 1v0; m20 z=65: 4 stacks @S=66 DOWN 0v1). With the birth-slice both-side enumerations (stick co=46 4 stacks + NEW co=48 6 stacks at z=65/z=66), the shadow family tracked its host at every separating slice of the measured m19/m20 ladder territory through z=66.
- Rule v2 both sides at the m19/m20 z=65/z=66 births: complete admissible split sets as exact mimics, no other 3-token separations anywhere in the census (G13/G14).
- Ladder depth records: m19/m20 through the z=65/z=66 births ({19,48}@67 / {20,48}@68); m21/m22 z=61/62; m23/m24 z=62/63; m25/m26 z=64/65; m27/m28 z=64/65; m29/m30 z=70/71; m31/m32 z=68/69.
- Kit-13 future constants (34 items, registered engine-free in the frozen .out): next one-past/birth pair per m=19..32; frontier 29th/30th candidates m=41@z=81 {41,42}@83 UP 2v0 (collapse v(83,81,123)=0) / m=42@z=82 (42,42)@84 UP 2v1 (collapse v(84,82,125)=1), K1268 z*(41)=81, z*(42)=82; window proposals m=39 z{69..76} / m=40 z{70..77}; even-m z=3m+6 continuation + odd-m close-out notes (contingent, NON-BINDING).

## S4 Verification record

- K0832 battery: 1,804 literals (1,702 carried + 102 new), closed==vC==vO, bad 0, recompute gate PASS.
- Anchors: 515/515 reproduce published values exactly (429 kit-11 carried + 86 kit-11 separation spots first-anchored), independent recompute gate PASS.
- Sweeps: all 49 row records recomputed shape-for-shape (separation multisets + shape counts identical), total separations 101.
- derive_check_kit12.py: 2,387 engine-free arithmetic checks, 0 fails (pre-freeze; re-executed post-reset identically).
- Determinism: 6 byte-identical walks (see S1); post-reset fresh-cold walk byte-identical to the frozen .out.
- Tamper battery: 3/3 fail-closed with per-tamper gate fingerprints; clean control rc=0 byte-identical; one audit per shell command.

## S5 Resume kit (registered constants for the next execution, binding unless noted)

1. Binding: the 30 kit-13 next-depth ladder pairs and frontier rows as itemized in the frozen .out future_slice_registration_constants (m19..m32 one-past/birth pairs; frontier 29th/30th m=41@z=81 / m=42@z=82).
2. Binding: the window proposals m=39 z in {69..76} and m=40 z in {70..77} (both NOT strip-covered; register-before-measure satisfied by the kit-13 freeze).
3. NON-BINDING (contingent): the even-m z=3m+6 continuation rows (stick {m,2m+6} + NEW {m,2m+8}) IF the kit-12 z=3m+4 rows measured the templates as registered (they did, 3/3 EXACT, so the z=3m+6 rows are the natural kit-13 candidates).
4. Standing rule (reconfirmed twice now): rule-v2 stack splits must be enumerated for EVERY registered 2-token seat with co >= 2m, including one-past seats (the early-follow sets are registered observables, not post-hoc).
5. Standing rule (clean this kit): the build-time duplicate check crosses the registration source's OWN measured slices; kit-11's registration was clean (zero skips), the first zero-skip kit since kit-9.
6. Rule-v2 stack-splits exist only when the seat co >= 2m (log-standing law); the kit-13 m=19/m=20 rows will again be the only split-carrying rows (stick co=48 / NEW co=50 at m=19; co=48/50 at m=20).

## S6 Dated disclosures

1. Build-time window-loop catch (pre-freeze, nothing published): the first generated explorer's main region still measured the m=35/m=36 window slices (kit-11 loop bodies carried the old m values). Caught immediately from the run output section names (inband_m35/m36) before any freeze; the corrected explorer measures the intended m=37/m=38 windows; the buggy run is discarded, not published, and audit gate G16 asserts non-remeasurement against the frozen .out.
2. Sandbox reset during the tamper battery (260s shell timeout, two clean audits plus a tampered audit in one command): working directory lost; all primary artifacts recovered byte-exact from the persistent backup (explorer 60fe1249..., .out 94759406...); every verification re-executed post-reset from the published kit-11 sources + the backup (S4). Lesson reconfirmed a second time: one slow command per shell call; freeze-step backups to the persistent directory (executed throughout this kit, zero byte loss).
3. Hand-typed pins forbidden: every pin in this log/README was machine-extracted from the frozen files.
4. Counter-probe: build-time and push-time repo code searches for kit-12/m39m40/frontier_m39/explore_m39m40 territory returned only the kit-11 files' own kit-12 future references (no concurrent publisher); push-time probe repeated before the push.

## S7 Standing no-claim caveats

- The standard 11x11 empty board, all 19 central-reply roots, the two-stone root {60,27}, the third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed. The frontier parity count (28/28), the rule-v2 shadow and early-follow observations, and the even-m lifecycle template are finite observation counts, NOT laws. Nodes and shape counts are bookkeeping.
