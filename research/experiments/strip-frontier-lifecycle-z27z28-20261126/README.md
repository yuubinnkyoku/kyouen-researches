# strip-frontier-lifecycle — in-band z=27/z=28 row records (K1335 band completion) + independent blind replication of the d49b480a z27–z34 census + consolidated supply rechecks (2026-11-26)

Registered-execution successor micro-kit of the published z26f20
kit (commit `68bc863d`). TWO roles, separated explicitly:

1. UNIQUE content (no other published kit measures these): the
   in-band z=27/z=28 row records for m=15..18 (including the
   arity<=4 extensions for m=18), completing the published K1335
   (T-Z20) residual band m=15 z in {21..28} — the SECOND fully
   swept residual band of the series — and extending the T-Z21 /
   T-Z22 / T-Z24 band progressions; plus the consolidated supply
   rechecks of the published 14th..25th tail constants over the
   domain extended by one point to s=69.
2. INDEPENDENT BLIND REPLICATION of the simultaneously published
   kit `research/experiments/strip-frontier-z27-z34-20261126/`
   (commit `d49b480a`, 2026-11-26T05:44:42Z): this kit was frozen
   and its run completed BEFORE the co-kit's output was read
   (machine-anchored timeline below); every overlapping value
   agrees exactly (list below). These sections are NOT claimed as
   first measurements — the first publication is `d49b480a`; the
   value here is the independent frozen-run agreement. A second
   sibling kit published three minutes later
   (`strip-decay-z29-z35-20261126`, commit `8d53f7d2`, executes
   decay curves at z=29..35, the z=29 touches, k=37/k=38) does
   NOT overlap this kit's measured values; it re-verified the
   co-kit's values with a post-freeze ordered-engine audit
   (16/16 identical), making this frozen run a THIRD independent
   source agreeing on the z=27/z=28 overlap.

NO K slot is claimed, NO universal statement is claimed; every
candidate/expectation was frozen in the docstring BEFORE the
first run.

## Counter-probe: DATED CORRECTION (2026-11-26T07:41Z)

The frozen docstring's counter-probe paragraph (lines 27–35 of
`explore_frontier_lifecycle.py`, quote: "at kit-build time the
latest main contained … NO published m-row record at any
z >= 27 … NO published z >= 28 engine values at all") is
FACTUALLY WRONG against the main that existed at freeze time.
Per the repo's frozen-bytes convention the kit files are NOT
edited (the sha below pins the artifact that produced the .out);
the correction lives here and in the log, dated.

What the kit-build counter-probe actually did (~07:30Z) and why
it failed: (a) it probed a handful of GUESSED experiment
directory names by direct path read (all 404), and (b) the
experiments directory listing was truncated by the 1000-entry
listing cap, so the two sibling kits (pushed 05:44:42Z and 05:47:36Z,
~1 h 48 min before the freeze at 07:35:18Z) were never seen.
The probe used NO
content-based `search_code` query. Lesson recorded in the knowledge
base and the log §4: counter-probes must include content queries
(e.g. unique row-record section ids), not only guessed names and
capped listings. A corrected probe (content query) was performed
at push time and confirmed the overlap boundary described above.

## Machine-anchored timeline (all times UTC, 2026-11-26)

- 05:44:42Z — co-kit `d49b480a` pushed to main (GitHub API commit
  timestamp).
- 07:35:18Z — `explore_frontier_lifecycle.py` frozen (file mtime;
  sha256 `16d2ea9e…` unchanged since).
- 07:35:44Z — frozen first run stdout complete (`.out` mtime;
  sha256 `9f94b608…`).
- 07:39:40Z — the co-kit's published `.out` first fetched and read
  by the author (file mtime): the frozen run of THIS kit
  predates any reading of the co-kit's values by ~4 minutes, and
  predates awareness of the co-kit's path as well. The six-run
  determinism suite then re-confirmed the frozen .out
  byte-identically. Neither sibling kit's values were read
  before the frozen run completed.

## Files

- `explore_frontier_lifecycle.py` — frozen pre-declaration
  explorer, sha256
  `16d2ea9ed094e7719aba578b2658f443d842088f471eb5cfd30198608cc729fc`
  (37,754 bytes). Structure assembled from the published
  `explore_z26f20.py` (byte-identical embedded ENGINE_BLOCK,
  provenance-asserted at startup) with the disclosed micro-kit
  sections: z=27/z=28 in-band row records (incl. the K1335 m=15
  band 7th and 8th entries, the band COMPLETION), the one-past
  m=14@z=27 and m=13@z=27 records, the frontier test rows m=15@z29
  and m=16@z30, the one-past companion rows m=15@z30 and
  m=16@z31, the z=28 handoff with frozen option tables, published
  z=27 anchor rechecks, the consolidated supply rechecks k =
  23..34 over {0} U {12..69}, and the NEW k=35 pre-computation.
- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  identical to the z24-floor18 / z25-min20 / z26-floor20 / z27-z34
  kit bytes; the embedded ENGINE_BLOCK startup pin `bd5f22e4…` is
  asserted by the machinery (engine_gate PASS in the frozen
  output).
- `explore_frontier_lifecycle.out` — frozen stdout, sha256
  `9f94b60864e374ed1786e63a75461b1d446019cbf294a2fef446f9f9b7a30b41`
  (60,896 bytes). Determinism: SIX runs all byte-identical (the
  frozen first run + default ×2 + PYTHONHASHSEED=random + env -i
  isolated directories ×2 via /usr/local/bin/python3), rc 0,
  ~15 s per run.

## What the run measured (all finite observations)

- K0832 battery: 107/107 single-token literals match across
  closed form / canonical engine / ordered engine; engine gate
  PASS.
- IN-BAND z=27 rows (UNIQUE): m=18 R=46 26/0 (+ arity<=4 ext
  25/0, the future T-Z24 band THIRD entry; the S=36 shape
  re-verifies the published z26f20 z=27 h3 value 1 in-record),
  m=17 R=45 32/0 (T-Z22 band FIFTH; S=35 re-verifies h1=0, S=34
  re-verifies h4=0), m=16 R=44 40/0 (T-Z21 band SIXTH; S=33
  re-verifies h2=1), m=15 R=43 50/0 (K1335 band SEVENTH).
- IN-BAND z=28 rows (UNIQUE): m=18 R=47 26/0 (+ ext 25/0, T-Z24
  FOURTH), m=17 R=46 32/0 (T-Z22 SIXTH), m=16 R=45 40/0 (T-Z21
  SEVENTH), m=15 R=44 50/0 (K1335 EIGHTH) — **the K1335 (T-Z20)
  residual band m=15 z in {21..28} is now COMPLETELY SWEPT: 8
  published entries, 50 shapes, 0 separations each — the second
  fully swept residual band of the series after the K1330 m=14
  band.** Neither the co-kit nor any other published kit contains
  these in-band records.
- Consolidated supply rechecks (UNIQUE scope): every published
  constant of the 14th..25th tails (k=23..34) reproduced over
  {0} U {12..69}, the domain extended by one point to s=69; both
  chain patterns intact (odd-k uniform (0,1), even-k
  (0,2)–(2,1)); plus the k=35 (TWENTY-SIXTH tail, ODD)
  pre-computation FIRST registered by the z26f20 kit and
  simultaneously published by the co-kit, hence part of the
  replication scope below.

## Independent blind replication vs `d49b480a` (all values AGREE)

Overlap machine-compared section-by-section at push time
(theirs = published `explore_z27z34_frontier.out`):

- frontier m=15@z=29: one separation {15,16}@S=31 UP 2v0, 50
  shapes — identical.
- frontier m=16@z=30: one separation {16,16}@S=32 UP 2v1, 40
  shapes — identical.
- one-past m=14@z=27: {14,14}@S=28 DOWN 0v1, 62 shapes —
  identical.
- one-past m=15@z=30: {15,16}@S=31 UP 1v0 — identical.
- one-past m=16@z=31: {16,16}@S=32 DOWN 0v1 — identical.
- two-past m=13@z=27: TWO separations {13,14}@S=27 DOWN 1v2 +
  {13,16}@S=29 UP 2v0, 76 shapes — identical.
- z=28 base-spot touches h1..h4 = 0,1,1,0 — identical.
- z=27 published recheck anchors 4/4 — identical.
- k=35 supply table (hold/break rows, all pairs) — identical.

First publication of these values: `d49b480a`. This kit's
frozen run reached the same values independently, before its
author read the co-kit's output (timeline above). Sections the
co-kit contains that this kit does NOT: frontier m=17@z=33 /
m=18@z=34 (both HIT the parity law, 6/6 through m=18), one-past
up to m=16, three-past m=13@z=28 (persistent shape exits,
secondary {13,16}@29 decays to 1v0), two-past m=14@z=28
({14,14}@28 DOWN 0v2 + {14,16}@30 UP 2v1) and k=36 (27th tail,
EVEN). The decay sibling `8d53f7d2` then added the one-past
m=17@z=34 / m=18@z=35 hits (parity-decay 3/3 per parity), the
two-past m=15@z=31 / m=16@z=32 secondary births, the m=13/m=14
decay curves (separation life-cycle scaffold), the z=29 touches
(0,1,1,0) and k=37/k=38. No claim is made on those here beyond
citation.

## Honesty notes

- The frozen docstring's counter-probe paragraph is WRONG (dated
  correction above); kit bytes stay frozen per repo convention,
  and this README plus the dated log are the correction of record.
- Every engine value at z >= 27 beyond the four published z=27
  anchors is first-contact FOR THIS RUN; the collapse constants
  quoted with the candidates were computed on paper from the
  PROVED K0832 closed form before the freeze (disclosed per
  section, incl. the v(27,27,41)=2 collapse jump that the
  two-past record confirmed).
- The replication role is stated because the run was designed
  and executed blind to the co-kit; the overlap agreement is a
  verification datum, not a novelty claim.
- Shape counts 26/32/40/50/62/76 are shape-for-shape identical
  to the co-kit's records where they overlap.
- No file edited after any run; six-run determinism
  byte-identical.

## Caveats

Finite machine observations only, plus disclosed paper
arithmetic from the PROVED closed form; no universal claim; no K
slot claimed (1 experiment ≠ 1 K). Raw engine pinned at
`bd5f22e4…` (embedded, engine_gate PASS in the frozen output).
11×11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots: all UNKNOWN, unchanged; no verdict
consumed.
