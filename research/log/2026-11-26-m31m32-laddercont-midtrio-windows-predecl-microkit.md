# m31/m32 frontier + m19..m30 ladder continuation + trio mid-ladder probes + m29/m30 windows pre-declaration micro-kit (kit-8, concurrent second census + recovery edition)

- kit id: kit-8 (hourly lane, session 2026-11-26; registered/frozen/executed/audited pre-reset ~09:58..10:41Z; sandbox LOST at ~10:41Z; recovered, rebuilt and re-verified ~11:00Z)
- runclass: publish-then-execute pre-declaration census, frozen before the literal push; committee by machine observation only
- commit base: a62c5d2e (kit-7); main head at build-time counter-probe: a62c5d2e (0 hits for the kit-8 territory at build)
- CONCURRENT LANE DISCLOSED: a parallel hourly execution of the same lane registered and measured the same kit-7 section (d) targets and pushed FIRST (7af915fb, 10:54:57Z; part-ew waves 7fcf9dde..2db639d0, disjoint paths). Push-time latest-main re-fetch recorded that head. This kit publishes second, as the independent blind census (48/48 row agreement, below)
- files: `research/experiments/strip-newband-m31m32-laddercont-midtrio-windows-20261126/{engine_block.py, explore_m31m32_laddercont_midtrio_windows.py, explore_m31m32_laddercont_midtrio_windows.out, README.md, sumonly_probe.py, sumonly_probe_R1.out, sumonly_probe_R2.out}`
- engine: published chain clone, sha 582c93c1..., startup pin bd5f22e4... (engine_gate PASS in the frozen output; engine file re-fetched from the kit-7 commit and sha-verified at recovery)
- original explorer sha256 (LOST in the sandbox reset; never pushed): 38c6074247b234f90facc5cee22c8e5fb5aa5f5bd8741de67591c79f3d45b344 (77,379 bytes)
- published explorer (RECOVERY REBUILD) sha256: 6ba3df72d4ecdeb87b2425a401f04a38c62b787ff28bbb4972a8e348e7ad2a2c (73,496 bytes)
- frozen output sha256: 487970c9db06e44902eb625401348a8d37e33d49b19781aaaa42da9e2d6f081e (123,422 bytes; recovered byte-exactly post-reset, sha verified against the pre-reset record before any use; the rebuild regenerates it byte-identically, rc 0)
- status: EXECUTED (pre-reset, rc 0 ~38 s), VERIFIED (pre-reset, 5-run determinism + audit + derive), LOST (sandbox reset), RECOVERED, RE-VERIFIED (rebuild byte-identity + fresh audit/derive/probes), PUSHED (680421eb), ENCODING-CORRECTED (e9847712, all 8 published files fetch-back byte-verified at e9847712 (8/8) compare-candidates identical incl. the frozen .out; corrected-explorer re-run byte-identical, see S6.8)

## S1. Anchor re-verification (180/180)

The 141 published chain anchors verbatim, plus the 39 kit-7 separation
spots (including the kit-7 unregistered stacked-trio shadow datum
{19,19,19}@57, now a first-class anchor) FIRST re-anchored here. The 39
spots were machine-verified 39/39 against the published kit-7 frozen
output values BEFORE the census (pre-reset), then every anchor was
re-executed in the frozen run and hit exactly (battery 769/769
all-match in the same run, R-first convention asserted).
Post-recovery, the independent ordered-engine audit re-measured all
180 spots (180/180) and the concurrent kit's output agrees on all 179
distinct (R, X, z) spots (the 180th is a registered double-mention,
S6.2). Cumulative anchor count 180.

## S2. Registered vs measured (25 FULL HIT + 6 DEVIATION of the 31 template rows; 17 plain-scan rows clean)

31 template rows executed (the 28 binding kit-7 section (d) rows + the
3 trio mid-ladder probes), then 17 plain-scan rows (16 windows + the
hole). Totals: 48 rows, 760 shapes, 54 separations = 46 registered seat
separations ALL HIT + 8 unregistered stack-class extras. Measured values
below verbatim from the frozen output (dead shapes conform-DEAD are
recorded in the candidates, not the separation lists):

| row (seat kind) | registered | verdict | measured separations {stack}/(seat): S dir value v collapse |
|----|----|----|----|
| m=19 z=56 (one-past-of-d=9 / death-of-d=8) | EXACTLY ONE | **DEVIATION** | {19,19,19}@57 UP 1v0; (19,38)@57 UP 1v0 |
| m=19 z=57 (birth slice d=10) | EXACTLY TWO | **DEVIATION** | {19,19,19}@57 DOWN 1v2; (19,38)@57 DOWN 1v2; {19,19,21}@59 UP 2v0; {19,20,20}@59 UP 2v0; (19,40)@59 UP 2v0 |
| m=20 z=57 (one-past-of-d=9 / death-of-d=8) | EXACTLY ONE | **HIT** | (20,38)@58 DOWN 0v1 |
| m=20 z=58 (birth slice d=10) | EXACTLY TWO | **DEVIATION** | (20,38)@58 DOWN 0v2; {20,20,20}@60 UP 2v1; (20,40)@60 UP 2v1 |
| m=21 z=52 (one-past-of-d=5 / death-of-d=4) | EXACTLY ONE | **HIT** | (21,32)@53 UP 1v0 |
| m=21 z=53 (birth slice d=6) | EXACTLY TWO | **HIT** | (21,32)@53 DOWN 1v2; (21,34)@55 UP 2v0 |
| m=22 z=53 (one-past-of-d=5 / death-of-d=4) | EXACTLY ONE | **HIT** | (22,32)@54 DOWN 0v1 |
| m=22 z=54 (birth slice d=6) | EXACTLY TWO | **HIT** | (22,32)@54 DOWN 0v2; (22,34)@56 UP 2v1 |
| m=23 z=54 (one-past-of-d=4 / death-of-d=3) | EXACTLY ONE | **HIT** | (23,32)@55 UP 1v0 |
| m=23 z=55 (birth slice d=5) | EXACTLY TWO | **HIT** | (23,32)@55 DOWN 1v2; (23,34)@57 UP 2v0 |
| m=24 z=55 (one-past-of-d=4 / death-of-d=3) | EXACTLY ONE | **HIT** | (24,32)@56 DOWN 0v1 |
| m=24 z=56 (birth slice d=5) | EXACTLY TWO | **HIT** | (24,32)@56 DOWN 0v2; (24,34)@58 UP 2v1 |
| m=25 z=56 (one-past-of-d=3 / death-of-d=2) | EXACTLY ONE | **HIT** | (25,32)@57 UP 1v0 |
| m=25 z=57 (birth slice d=4) | EXACTLY TWO | **HIT** | (25,32)@57 DOWN 1v2; (25,34)@59 UP 2v0 |
| m=26 z=57 (one-past-of-d=3 / death-of-d=2) | EXACTLY ONE | **HIT** | (26,32)@58 DOWN 0v1 |
| m=26 z=58 (birth slice d=4) | EXACTLY TWO | **HIT** | (26,32)@58 DOWN 0v2; (26,34)@60 UP 2v1 |
| m=27 z=56 (one-past-of-d=1 / death-of-d=0) | EXACTLY ONE | **HIT** | (27,30)@57 UP 1v0 |
| m=27 z=57 (birth slice d=2) | EXACTLY TWO | **HIT** | (27,30)@57 DOWN 1v2; (27,32)@59 UP 2v0 |
| m=28 z=57 (one-past-of-d=1 / death-of-d=0) | EXACTLY ONE | **HIT** | (28,30)@58 DOWN 0v1 |
| m=28 z=58 (birth slice d=2) | EXACTLY TWO | **HIT** | (28,30)@58 DOWN 0v2; (28,32)@60 UP 2v1 |
| m=29 z=58 (one-past of the d=0 seat) | EXACTLY ONE | **HIT** | (29,30)@59 UP 1v0 |
| m=29 z=59 (birth slice d=1) | EXACTLY TWO | **HIT** | (29,30)@59 DOWN 1v2; (29,32)@61 UP 2v0 |
| m=29 z=60 (one-past-of-d=1 / death-of-d=0) | EXACTLY ONE | **HIT** | (29,32)@61 UP 1v0 |
| m=30 z=59 (one-past of the d=0 seat) | EXACTLY ONE | **HIT** | {30,30}@60 DOWN 0v1 |
| m=30 z=60 (birth slice d=1) | EXACTLY TWO | **HIT** | {30,30}@60 DOWN 0v2; (30,32)@62 UP 2v1 |
| m=30 z=61 (one-past-of-d=1 / death-of-d=0) | EXACTLY ONE | **HIT** | (30,32)@62 DOWN 0v1 |
| m=31 z=61 (frontier first contact proposal) | EXACTLY ONE | **HIT** | (31,32)@63 UP 2v0 |
| m=32 z=62 (frontier first contact proposal) | EXACTLY ONE | **HIT** | {32,32}@64 UP 2v1 |
| m=13 z=37 (trio mid-ladder slice d=6) | EXACTLY TWO | **DEVIATION** | (13,24)@37 DOWN 1v2; {13,13,13}@39 UP 2v0; (13,26)@39 UP 2v0 |
| m=15 z=43 (trio mid-ladder slice d=7) | EXACTLY TWO | **DEVIATION** | (15,28)@43 DOWN 1v2; {15,15,15}@45 UP 2v0; (15,30)@45 UP 2v0 |
| m=17 z=49 (trio mid-ladder slice d=8) | EXACTLY TWO | **DEVIATION** | (17,32)@49 DOWN 1v2; {17,17,17}@51 UP 2v0; (17,34)@51 UP 2v0 |

(frontier m=31@z=61 {31,32}@63 UP 2v0 and m=32@z=62 (32,32)@64 UP 2v1:
both HIT exactly as registered, EXACTLY ONE each.)

Plain-scan rows: m=29 z in {49..56} and m=30 z in {50..57} windows 16
rows, 0 separations each (registered candidates clean -- the
below-frontier history of m=29/m=30 opens with 16 clean rows); hole row
m=26@z=25 clean (registered candidate 0 separations) -- the m=26
measured line closes to {25..56}, the second fully-swept m-line of the
series after m=25 {25..55} (kit-7).

All six deviations are of the stack class (a stacked shape sharing S
with a seat separates with the seat's signature):

1. m=19 z=56: trio {19,19,19}@S=57 mirrors the birth seat's one-past
   (UP 1v0) -- the kit-7 log S5 item 10 tracker's mimic candidate
   measured exactly; the trio LIFECYCLE CONTINUES past its birth slice.
2. m=19 z=57: the stick-S=57 trio mimics the stick (DOWN 1v2), and the
   ENTIRE in-sweep birth-S=59 family separates with identical
   signatures: {19,19,21} UP 2v0 and {19,20,20} UP 2v0 alongside the
   registered NEW seat {19,40}.
3. m=20 z=58: the EVEN-m mid-slice (d=m/2, S_birth=3m=60) trio
   {20,20,20} mirrors its birth seat (20,40) -- the first even-m
   mid-slice witness.
4.-6. m=13 z=37, m=15 z=43, m=17 z=49: trio {m,m,m}@S=3m mirrors the
   mid-ladder birth seat (UP 2v0) at EVERY probe (measured with the
   DATED z-CORRECTIONS of the kit-7 log S5 item 12: the published item
   listed z=42/z=48; engine-free re-derivation z(birth)=z*(m)+2(m-1)/2
   gives z=43/z=49; frozen in the docstring BEFORE the run).

With kit-7's m=19 z=55 trio birth datum, the odd-m mid-slice trio
separation now has FOUR witnesses (m in {13,15,17,19}) plus the even-m
witness (m=20), and the m=19 trio has a THREE-SLICE measured lifecycle
(birth UP 2v0 at z=55 -> one-past UP 1v0 at z=56 -> stick DOWN 1v2 at
z=57), an exact mimic of the co-token seat's life at S=57/59.

## S3. State after kit-8 (scaffolding bookkeeping, no claim)

- Frontier parity scaffold: 20/20 (m=13..32; the 19th/20th datums
  measured blind here and published first by the concurrent kit
  7af915fb at 10:54:57Z; the two censi agree verbatim).
- Ladder depths after kit-8: m=19/20 d=10 COMPLETE (deepest measured of
  the series); m=21/22 d=6; m=23/24 d=5; m=25/26 d=4; m=27/28 d=2;
  m=29/30 d=1. One-past d=0 decay counts: odd 33 (m in {13..29}),
  even 32 (m in {14..30}) -- the m=29 z=58 / m=30 z=59 rows of this kit
  are the first m=29/m=30 decay datums.
- Deaths witnessed: 10 NEW death datums (m=19/m=20 d=8, m=21/m=22 d=4,
  m=23/m=24 d=3, m=25/m=26 d=2, m=29/m=30 d=0 -- the first m=29 and
  m=30 deaths), plus TWO re-verified duplicates (S6.2).
- Measured lines: m=25 {25..55} (kit-7); m=26 {25..56} (CLOSED this
  kit). Below-frontier windows opened for m=27..m=30.
- L8 candidate law (see S4.5, finite observation, falsifiable): on
  x0-style rows the measured value is a function of (S, z, R) alone --
  seats ARE sums; stack shadows are necessary seats of their sums.

## S4. Verification (pre-reset and post-recovery records, all executed)

1. Pre-freeze derivation (pre-reset): `derive_check_kit8.py` --
   engine-free paper derivation of every registered literal from the
   K0832 closed form and the seat lifecycle arithmetic: 204 checks,
   0 errors, run before the row sweeps. (Script bytes lost in the
   reset; result recorded here as executed history.)
2. Pre-freeze anchor verification (pre-reset): the 39 kit-7 spots
   re-measured 39/39 on the published canonical engine before any row
   ran (also pre-reset).
3. Frozen run (pre-reset): rc 0, ~38 s, stdout sha 487970c9...;
   determinism pre-reset: published run + default rerun +
   PYTHONHASHSEED=random + env -i isolated: 5 runs byte-identical.
4. Post-recovery (post-reset): frozen output recovered byte-exactly
   (sha verified against the pre-reset record); REBUILD explorer
   (6ba3df72...) regenerated the output BYTE-IDENTICALLY at recovery
   time (rc 0, ~46 s, internal sha assert) plus a PYTHONHASHSEED=random
   rerun byte-identical; the rebuild re-executes every row sweep,
   anchor and battery check live (only documentation constants are
   carried; see the kit README Recovery note).
5. Fresh post-recovery audits (scripts re-executed in the recovery
   environment):
   - `audit_kit8b.py` (ordered-engine independent audit): 48 rows,
     760 shapes, 0 bad rows; 54 ordered separations identical to the
     frozen 54; classification 25 FULL HIT + 6 DEVIATION (template
     rows) + 17 clean plain-scan rows; anchors ordered 180/180; L8
     in-row sum-only family check 32 multi-shape families, 32 agree,
     0 violations. AUDIT-KIT8B: PASS.
   - `derive_check_kit8b.py` (engine-free re-derivation): 278 checks,
     0 errors, PASS (v-literals, R=z+m+1 identities, seat sums,
     lifecycle z/S/co-token/death-depth identities, window ranges,
     mid-slice d=(m-1)/2 and S=3m identities).
   - `sumonly_probe.py` (recovery-run probes): R1 m in {13..19},
     z in {25..66}: 7,293 positions, 994 multi-shape sum-families, 994
     agree, 0 violations; R2 mid-slice trio-vs-seat under R offsets
     {-3,-2,-1,+1,+2,+3}, m in {13,15,17,19,20}: 30 checks, 30 agree.
6. Concurrent-kit cross-verification (blind, post-publication): the
   concurrent kit (7af915fb) and this kit agree on ALL 48/48 common
   (m,z) rows' separation sets (54/54 separations with identical
   shapes, sums, values, collapses, directions) and on all common
   anchors (179/179 distinct spots value-identical; both censi
   re-measured the same 180 published spots). The two censi used
   independently written explorers, different batteries (1004 vs 769
   literals) and slightly different sweep domains (theirs
   max(m+38,z+2) everywhere; mine m+38 except two disclosed
   birth-seat extensions).
7. Standard caveats: the K0832 closed form remains the only PROVED
   statement; every item above is a finite machine observation; the
   standard 11x11 cell remains UNKNOWN at all times; no K slot is
   claimed; no residual verdict is consumed.

## S5. Handoff: kit-9 registrations

OPERATIVE (published by the concurrent kit 7af915fb, first): 34 binding
rows (m=19..m=32 ladder/frontier continua incl. the d=11 stack-split
candidates {19,19,23}/(19,23), (20,22), (21,21), and m=33@z=65 /
m=34@z=66 FRONTIER 21st/22nd datum candidates -- the kit-9 censi should
take THEIR registration table as the operative one).

CONFIRMATORY (frozen blind in this kit's own output section
`future_slice_registration_constants`, identical where overlapping):
the 32 core binding rows: m=19..m=30 ladder continuations 2 rows each
(one-past/death + birth) through d=11 (m19/20), d=7 (m21/22), d=6
(m23/24), d=5 (m25/26), d=3 (m27/28), d=2 (m29/30); m=31/m=32 3 rows
each (birth d=0 one-past, birth d=1, one-past-of-d=1/death-of-d=0);
frontier m=33@z=65/m=34@z=66 21st/22nd candidates; window proposals
m=31 z in {53..60}, m=32 z in {54..61} (z*(m)-8..-1). smax note: kit-9
rows m=19 z=59 (birth S=61) and m=20 z=60 (birth S=62) need the
disclosed z+2 sweep extension.

NEW NON-BINDING (this kit's observation registrations, for whichever
kit-9 executes, tracked beside the operative candidates, singles:
L8 trackers at m=19 z=59 (in-sweep birth-S=61 family expected size 4:
(19,42), {19,19,23}, {19,20,22}, {19,21,21} all UP-2v0-seat-mimic
expected by L8) and m=20 z=60 (family size 3: (20,42), {20,20,22},
{20,21,21}); trio death expectation at m=19 z=58 (the S=57 family
GLIDE-DEAD slice: by L8 the trio {19,19,19} tracks down with its
family; any other outcome is the datum) -- rider on the registered
row 1 of the section (d); even-m mid-slice probe proposals m=14@z=40,
m=16@z=46, m=18@z=52 (d=m/2, S_birth=3m, trio {m,m,m} mimic expected;
COUNTER-PROBE BEFORE REGISTERING; full x0 row records).

## S6. Honest record / caveats

1. Sandbox loss and recovery: the analysis sandbox environment was
   reset (~10:41Z) during the sum-only probe of the first session, and
   EVERY unpushed local artifact of the kit was lost: the original
   frozen explorer bytes (sha 38c60742..., recorded, unrecoverable and
   never claimed recoverable), the original generator, the original
   audit/derive scripts, and the first post-restart probe attempts.
   The frozen output was recovered byte-exactly from the saved
   pre-reset stdout dump (sha 487970c9 verified against the pre-reset
   record before any use); the published explorer is an analysis-time
   REBUILD whose run must (and does) regenerate the frozen output
   byte-identically with every measured field re-executed live; the
   audit and derivation checks were re-executed fresh (S4.5). No value
   anywhere in the frozen record is copied from the output into a
   measurement claim -- every claim above is re-executed.
2. DATED DISCLOSURE: the published kit-7 frozen section (d)
   double-registered two rows kit-7 itself had ALREADY measured
   (m=27@z=56 and m=28@z=57: registered in kit-6 S5 items 21/24,
   measured by kit-7 items 21/24, then re-registered verbatim in
   kit-7's own section (d)). This kit took them as the binding
   candidates they were frozen as; both measured EXACTLY the published
   values, so they count as blind re-verifications, not new deaths;
   the first m=27/m=28 death datums remain kit-7's. The concurrent
   kit measured them too (agreement). The kit-9 registration tables
   should keep checking for double-registration at build time.
3. DATED CORRECTION (registered in the frozen docstring BEFORE the
   run): the kit-7 log S5 item 12 mid-slice z values were misstated
   (z=42 for m=15, z=48 for m=17); the engine-free derivation gives
   z=43 and z=49; corrected values were registered and measured (no
   datum was affected -- those rows had never been measured).
4. Concurrency record: the kit-8 territory was registered and measured
   BLIND by two censi the same hour (this kit, and the concurrent lane
   at 7af915fb which pushed first at 10:54:57Z while this kit was
   mid-recovery). Cross-checks: 48/48 rows and 179/179 anchor spots
   agree verbatim (S4.6). Publication priority for the shared datums
   (incl. the frontier 19th/20th) belongs to the concurrent kit; this
   kit claims no firsts. The overlap exists because both censi wrote
   the same kit-7 section (d) -- the protocol worked as designed:
   registrations were binding, and the outcome is a blind
   double-census verification of the whole kit-8 territory. Registered
   duplication risk for FUTURE kits is handled by the counter-probe
   at every build; the fresh-main re-fetch before every push (done)
   and the operative/published registrations quoted in S5.
5. The six deviations are all stack-class and all L8-consistent
   (same-S families share one value and one separation signature at a
   slice); the two-token seat scaffold survived 46/46. The candidate
   law L8 is a finite observation, NOT a theorem; the pre-reset probe
   numbers are NOT relied on anywhere (artifacts lost); the recovery
   probes (S4.5) are the citable ones and are published with the kit.
6. No universal claim is made here. K0832 is the only PROVED
   statement. The 11x11 standard cell remains UNKNOWN at all times.
   No K slot is claimed. No residual verdict is consumed.
7. Push-time records: latest-main re-fetch before the push returned
   head 7af915fb (the concurrent kit-8) and the part-ew wave commits
   (disjoint paths, no conflict); the push of this kit re-used no
   existing path; the push commit body carries this note and the
   published-vs-rebuild facts (explorer sha 6ba3df72, original sha
   38c60742 recorded as lost). Fetch-back verification (commit-pin
   raw URL byte-comparison of every pushed file) and the push-time
   rerun of the published explorer are recorded in the follow-up
   commit once executed.

8. DATED CORRECTION (same day, post first push): the first push of this
   kit (680421eb) double-encoded the non-ASCII punctuation of four
   files (the explorer docstring, the kit README, the probe script and
   this log) to mojibake (a byte->code-unit->UTF-8 re-encoding glitch of
   the push transport; the frozen .out, engine and probe outputs were
   pure ASCII and pushed byte-exact). The correction commit
   re-publishes the four files ASCII-normalized (em-dash to --, arrow
   to ->, set-membership to plain words); the explorer docstring is the
   ONLY changed part of the explorer, so its sha changes from
   cbd521157b74006a27c300ff60d30daa3232964599709de5941e3d626028a8b1
   to 6ba3df72d4ecdeb87b2425a401f04a38c62b787ff28bbb4972a8e348e7ad2a2c
   (73,496 bytes); the re-normalized explorer was RE-RUN at correction
   time and REGRESSES the frozen output byte-identically (rc 0, internal
   sha assert PASS). Fetch-back of the corrected files is
   byte-verified in the correction commit body.

9. Fetch-back completion record (same day): at commit e9847712 every
   published file of this kit was fetched back over raw commit-pin URLs
   and byte-compared with the intended local state: 8/8 identical
   (engine_block.py, explorer, frozen .out, kit README, sumonly_probe.py,
   probe R1/R2 outputs, kit log; the log compared at its final pushed
   state). The corrected explorer was RE-RUN at push time and regressed
   the frozen output byte-identically (rc 0, internal sha assert PASS).
   Cumulative post-recovery determinism: 4 explorers runs + 1
   push-time rerun, all byte-identical to 487970c9...
