# 2026-11-26 — Frontier-lifecycle kit: K1335 m=15 band COMPLETELY SWEPT (second fully-swept residual band), in-band z=27/z=28 rows m=15..18 all clean, consolidated 14th..25th tail rechecks to s=69, and an INDEPENDENT BLIND REPLICATION of the simultaneously published z27–z34 census (d49b480a, all overlapping values agree) — with a dated counter-probe correction

## §0 Slot check (pre-claim, honest, corrected)

The kit-build counter-probe (~07:30Z) FAILED and its result is
recorded in the frozen docstring: it probed only GUESSED
experiment names by direct path and relied on an experiments
directory listing truncated by the 1000-entry cap, so it found
nothing. The TRUE state of main at freeze time: TWO sibling micro-kits
had already been published by the parallel fast lane —
`research/experiments/strip-frontier-z27-z34-20261126/` (commit
`d49b480a`, pushed 2026-11-26T05:44:42Z: frontier rows m=15..m=18
at z=29..34 (6/6 parity-law hits), one-past m=14/m=15/m=16,
two-past m=13@z=27 and m=14@z=28, three-past m=13@z=28, the
z=28 base-spot touches, k=35 (26th tail) and k=36 (27th tail))
and `research/experiments/strip-decay-z29-z35-20261126/` (commit
`8d53f7d2`, pushed 2026-11-26T05:47:36Z: one-past m=17@z=34 /
m=18@z=35 (3/3 per parity), two-past m=15@z=31 / m=16@z=32 with
the secondary-birth structure, the m=13/m=14 decay curves to
z=30 (separation life-cycle scaffold), the four z=29 touches,
k=37/k=38 (10/10 chains)). NEITHER kit measures any in-band
row: their slot checks enumerate m-row positions only at or past
the frontier; the in-band z=27/z=28 rows for m=15..18 remain
unmeasured by any published kit (content-probe verified).

DATED CORRECTION (2026-11-26T07:41Z): the frozen docstring's
counter-probe paragraph ("NO published m-row record at any
z >= 27 … NO published z >= 28 engine values") is factually
wrong; kit bytes stay frozen per repo convention (the frozen
.SHAs pin the artifact that produced the .out), and this
paragraph plus the README section of the same date are the
correction of record. Lesson (→ knowledge base): counter-probes
must include content-based `search_code` queries on unique
row-record identifiers, never only guessed kit names plus a
capped directory listing.

Slots this kit therefore claims — and ONLY these:
(a) the in-band z=27/z=28 row records for m=15..18 with the
    m=18 arity<=4 extensions (measured by NO published kit);
(b) the K1335 (T-Z20) residual band completion m=15 z in
    {21..28} (8/8 entries swept);
(c) the consolidated supply rechecks of the published
    14th..25th tail constants (k=23..34) over {0} U {12..69},
    domain extended to s=69;
(d) an INDEPENDENT BLIND REPLICATION of the d49b480a overlap
    (frozen-run agreement on every shared value — a verification
    datum, not a novelty claim).

## §1 Context and kit role

The published z26f20 kit (commit `68bc863d`) left four
registrations this kit executes: S5 item #1 (parity-corrected
frontier-record law candidates m=15@z=29 / m=16@z=30), #2 (the
one-past m=14@z=27 datum and the m=13@z=27 two-past
continuation), #3 (26th-tail k=35 ODD supply pre-computation),
#4 (the z=28 base-spot handoff with blind option tables). The
in-band z=27/z=28 row records were swept alongside as the same
slices the frontier entries live in. Unknown to this kit's
build (failed probe, §0), the parallel fast lane had frozen and
pushed the same headline measurements in `d49b480a`; because
this kit's run finished before its author read that output
(timeline §2), the overlap became an independent replication.

## §2 Kit construction and discipline (executed before the first run)

- Files: `explore_frontier_lifecycle.py` (frozen 2026-11-26
  07:35:18Z by file mtime, sha256
  `16d2ea9ed094e7719aba578b2658f443d842088f471eb5cfd30198608cc729fc`,
  37,754 bytes) with the embedded ENGINE_BLOCK byte-identical to
  the published engine (startup pin `bd5f22e4…` asserted,
  engine_gate PASS), `engine_block.py` (byte-clone sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  frozen stdout `explore_frontier_lifecycle.out` (complete
  07:35:44Z by file mtime, sha256
  `9f94b60864e374ed1786e63a75461b1d446019cbf294a2fef446f9f9b7a30b41`,
  60,896 bytes). SIX runs all byte-identical (frozen + default
  ×2 + PYTHONHASHSEED=random + env -i isolated dirs ×2 via
  /usr/local/bin/python3), rc 0, ~15 s per run.
- Pre-declaration: every candidate and every disclosed paper
  constant was frozen in the docstring BEFORE the first run. The
  paper arithmetic is the PROVED K0832 closed form ONLY, on
  paper; no engine recursion on any z >= 27 position was
  evaluated before the freeze. The disclosed constants included
  the v(27,27,41)=2 collapse jump (z==x window at x=27) that the
  two-past record confirmed, and the frozen option tables
  h3=mex{h1,0}, h4=mex{h2,1} with their PUBLISHED C-children from
  the z26f20 z=27 handoff.
- BLINDNESS TIMELINE (machine-anchored): co-kit commit
  05:44:42Z (GitHub) → this kit frozen 07:35:18Z (mtime) →
  frozen run output complete 07:35:44Z (mtime) → the co-kit's
  published .out first fetched and read by the author 07:39:40Z
  (mtime). The run predates the reading of the co-kit's values
  by ~4 minutes.

## §3 Results (finite observations)

1. K0832 battery: 107/107 single-token literals match across
   closed form / canonical / ordered engine; engine gate PASS.
2. **IN-BAND z=27 rows (UNIQUE)**: m=18 R=46 26/0 + arity<=4 ext
   25/0 (future T-Z24 band THIRD entry; S=36 in-record
   re-verify of the published z26f20 h3 z=27 value 1), m=17 R=45
   32/0 (T-Z22 FIFTH; S=35 re-verifies h1=0, S=34 the h4=0),
   m=16 R=44 40/0 (T-Z21 SIXTH; S=33 re-verifies h2=1), m=15
   R=43 50/0 (K1335 SEVENTH). Shape counts shape-for-shape
   comparable with the published entries.
3. **IN-BAND z=28 rows (UNIQUE)**: m=18 R=47 26/0 + ext 25/0
   (T-Z24 FOURTH), m=17 R=46 32/0 (T-Z22 SIXTH), m=16 R=45 40/0
   (T-Z21 SEVENTH), m=15 R=44 50/0 (K1335 EIGHTH). **The
   published K1335 (T-Z20) residual band m=15 z in {21..28} is
   now COMPLETELY SWEPT: 8 entries, 50 shapes each, 0
   separations each — the second fully swept residual band of
   the series after the K1330 m=14 band completion (z25f20
   kit).** Bookkeeping completion of finite sweeps; upgrades
   nothing universal.
4. **INDEPENDENT BLIND REPLICATION of the d49b480a overlap —
   ALL VALUES AGREE (machine-compared at push time, section by
   section):** frontier m=15@z=29 one separation {15,16}@S=31 UP
   2v0 (50 shapes) and m=16@z=30 one separation {16,16}@S=32 UP
   2v1 (40 shapes) — both REGISTERED parity-law candidates HIT;
   one-past m=14@z=27 {14,14}@S=28 DOWN 0v1 (62 shapes),
   m=15@z=30 {15,16}@S=31 UP 1v0, m=16@z31 {16,16}@S=32 DOWN
   0v1 — the ONE-PAST PARITY SPLIT reading (odd drops 2→1 UP
   1v0, even drops 2→0 DOWN 0v1, shape always persists, always
   exactly one separation) now has four data points;
   two-past m=13@z=27 TWO separations ({13,14}@S=27 DOWN 1v2
   with the pre-disclosed collapse jump v(27,27,41)=2 MEASURED +
   the new first-ever {13,16}@S=29 UP 2v0) — the first
   multi-separation frontier-region record; z=28 touches
   0,1,1,0 (four blind option-table CONFORMs; m=18 z-sequence
   z∈{16..28} = 0,1,0,1,0,1,0,1,1,1,1,1,1 — six-slice 1-run;
   m=17 adds a sixth 0); z=27 published anchors 4/4; k=35
   supply table identical in every pair. First publication of
   all these values is `d49b480a`; this kit's datum is the
   independent frozen-run agreement.
5. Consolidated supply rechecks (UNIQUE scope): k in {23..34}
   over {0} U {12..69} — every published 14th..25th tail
   constant reproduced, domain extended by one point to s=69,
   both chain patterns intact (odd-k uniform (0,1); even-k
   (0,2)–(2,1)). k=35 (26th tail, simultaneously published by
   the co-kit, identical): hold {0} U {12..35} (25 equal rows
   incl. s=0), UNIFORM 0v1 for ALL s in {36..69} (34 break
   rows, single (0,1) pattern); odd-z supply chain candidate
   9/9; z=35-slice datum precomputed for the future z=35 lane.

## §4 Honest record

- Kit-build counter-probe FAILED (§0): guessed names + capped
  listing, no content search. The frozen docstring records the
  wrong conclusion; the dated correction of record is this log
  §0 and the kit README. Machine-checkable timeline in §2
  establishes the run's blindness to the co-kit's values
  despite the co-kit's earlier commit.
- Every engine value beyond the four published z=27 anchors is
  FIRST-CONTACT at this run; paper constants from the PROVED
  K0832 closed form only, disclosed per section, all measured as
  pre-declared.
- The one-past parity split and the two-past two-separation
  structure are READINGS across finite data (4 and 2 data
  points respectively), registered as candidates in §5, not
  claims.
- The K1335 band completion is bookkeeping of PUBLISHED finite
  sweeps (this kit adding the 7th/8th entries): 8 z-editions,
  400 shapes, all clean.
- No file edited after any run; six-run determinism
  byte-identical.

## §5 Handoff (new registrations, all BEFORE any future measurement)

State of the registrations BEFORE this push: the z26f20 §5
items #1..#4 that this kit executed are now published HERE and in
`d49b480a` (identical values, independent frozen runs); the decay
kit `8d53f7d2` then executed the one-past m=17/m=18, two-past
m=15/m=16 (secondary-birth FULL HIT, gap-3/gap-2 rules), the
m=13/m=14 decay curves (ROW-parity decay lesson, separation
life-cycle scaffold: births at 2d-past, gaps 2d+1 odd / 2d even,
stuck values 1 (odd row) / 0 (even row), deaths at birth+3), the
z=29 touches (0,1,1,0) and k=37/k=38. Its own §5 has registered
the death-valley (m=15@z=32 / m=16@z=33), tertiary-birth
(m=15@z=33, m=16@z=34, m=13@z=31, m=14@z=31, m=13@z=32), z=30
touch (w1..w4) and k=39/k=40 next points. This kit cedes all of
those and registers ONLY what neither sibling kit has claimed:

1. **FRONTIER-RECORD LAW candidate (parity-corrected, 6/6 data
   through m=18, none of which exceeds the m=18 frontier)**: next
   test data — m=19@z=37 (z*(19)=2·19−2+1=37; odd → predicted
   EXACTLY ONE separation {19,20}@S=39, UP 2v0, collapse
   v(39,37,57)=0 on paper) and m=20@z=38 (z*(20)=38; even →
   predicted EXACTLY ONE separation {20,20}@S=40, UP 2v1,
   collapse v(40,38,59)=1 on paper). Not registered by either
   sibling kit. Record verbatim either way.
2. **IN-BAND ROW CONTINUATION (the fully unclaimed lane)**: the
   published m-row records exist for the frontier and past
   regimes (m=13 down to 5-past, m=14..m=18 to 1..2-past) plus
   this kit's in-band z=27/z=28 rows; the remaining in-band
   (pre-frontier) rows for m=16..18 above z=28 are measured by
   NO kit: the m=16
   row at z=29 (R=46, x0-style) — the T-Z21 residual band m=16
   z in {22..29} COMPLETION entry, the THIRD completed band of
   the series if clean; then the m=17 rows at z in {29..32}
   (T-Z22 band z in {23..32}, 6/10 entries through z=28) and
   the m=18 rows at z in {29..33} (T-Z24 band z in {25..33},
   4/9 entries through z=28), all expected clean (0
   separations, x0-style row records, arity<=4 exts for m=18).
   Roll-ups: the K1330 (m=14), K1335 (m=15) and — with the
   z=29 entry — T-Z21 (m=16) band completions give a three-band
   clean-base dataset for a future stabilization-length
   candidate.
3. **POST-FRONTIER m-ROW CURVES at NEW m (extends the published
   life-cycle scaffold to m=17/m=18)**: the decay curves exist
   for m=13..m=16 only: two-past m=17@z=35 / m=18@z=36 (the
   secondary-birth gap rule predicts {17,20}@S=37 UP 2v0 resp.
   {18,20}@S=38 UP 2v1 for odd/even), three-past m=17@z=36 /
   m=18@z=37. NO CANDIDATE beyond the sibling-declared gap rule;
   record verbatim.
4. **11×11 UNKNOWN: unchanged. No action.**

## §6 Caveats

Finite machine observations only, plus disclosed paper
arithmetic from the PROVED closed form; no universal claim; no K
slot claimed (1 experiment ≠ 1 K). Raw engine pinned at
`bd5f22e4…` (embedded, engine_gate PASS in the frozen output).
11×11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots: all UNKNOWN, unchanged; no verdict
consumed.
