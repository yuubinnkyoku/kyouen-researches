# n11 sixth-cost k09..k43 resolved-rows third-implementation batch session log (2026-11-26)

Session lane: the recurring n11 long-term lane. Scope executed under the
single-owner declaration
`research/log/2026-11-26-n11-sixthcost-k09-k43-resolved32-thirdimpl-batch-single-owner-note.md`
(push `4d1b7db7`, declared 2026-11-26T08:45Z at HEAD `4e87e67b`): the
third-implementation verdict re-verification program was extended to the thirty
resolved-LOSS rows of the fifth-resumption batch and to the two parked4-L50M-ladder
WIN rows k13/k19, per the program's fresh-declaration rule. Completed rows:
ALL THIRTY-TWO (no budget-stop needed; the batch ran to full completion).

## Chain

1. Declaration pushed (`4d1b7db7`) BEFORE any target-row execution, after a repo
   probe finding no competing claim (audit_k09 0 hits; no k09..k43 third-impl
   artifact of any kind on main; the parked4 close-out explicitly left the k13/k19
   WINs unconsumed pending this scrutiny).
2. All one hundred replica raws consumed over raw.githubusercontent.com at the
   recorded HEADs (90 fifth-resumption raws from the probe dir at `0971173e`,
   10 parked4-ladder raws at `4e87e67b`), byte-hashed; at publication time ALL
   ONE HUNDRED were re-fetched and byte-verified against BOTH current main and
   the recorded consumption HEAD (100/100 sha-identical to both; the 32 row-spec
   inputs likewise 32/32 against main and their recorded HEADs), then
   re-published inside the experiment dir at `out/<row>-replica-raws/`.
3. C1 calibration honestly REUSED from the k06/k07/k08 addendum (same host, same
   session, no restart between; declared before any run; k04-addendum
   precedent): verify_tbl quads 95,670 == 95,670 over 195,044 triples, 0
   mismatches; anchor w2 WIN(1) expansions 7,583,990 == the published ea73c3e3
   witness on two identical executions.
4. C2 runs (all cold, independent solvers, serial, one node process at a time,
   --cap=400000000 --wallcap=270 --memo-power=22), ascending machine order:
   all 30 LOSS rows LOSS(2) with identical (result, expansions, ttHits,
   ttOverwrites) per 2-run pair; k13 WIN(1) expansions 19,433,195 ttHits
   10,181,270 ttOverwrites 15,238,891, 3/3 identical (a, b, v-legal, wall
   54.12/54.20/97.84s, the v run with --verify-legal=1); k19 WIN(1) expansions
   17,955,947 ttHits 9,504,863 ttOverwrites 13,761,643, 3/3 identical (a, b,
   v-legal, wall 50.94/50.66/90.65s, the v run with --verify-legal=1).
   Verdict-level agreement with the published replica raws on all 32 rows; the
   auditor additionally enforces expansions != replica resolution nodes
   (anti-copy) on every run.
5. C4 negative gates: all 64 GATE_FAIL rc=1 with the pinned mismatch strings
   (per-row legal+1 and stones=6; `out/neg-gate-k*.txt`).
6. `audit_k09k43.py` written as a SEPARATE data-driven auditor (audit.py,
   audit_k04.py, audit_k05.py, audit_k06k07k08.py byte-frozen): 850/850 gates
   ALL PASS rc=0; deterministic byte-identical output across runs in a fixed
   layout. Tamper battery 3/3 fail-closed (T1 k43 cold verdict flip 2->1;
   T2 k13 verdict flip 1->2; T3 k09 replica-raw nodes edit), restores
   byte-verified, final clean control rc=0
   (`out/audit-tamper-controls-k09k43.txt`).
7. Publication: addendum files (266 batch files: auditor + 32 inputs + 132 out
   run/gate/audit files + 100 per-row replica raws) + README batch addendum +
   MANIFEST.sha256 extension (79 -> 344 lines) + this session log pushed in
   chunks; raw fetch-back byte-verified for every pushed file.

## Honest session notes

- **Declaration miscounts, corrected here and in the README batch addendum
  (dated corrections; declaration bytes immutable)**: the k13/k19 replica-raw
  count is TEN per two rows (five raws per row), not "twelve"; the batch's total
  replica-raw count is ONE HUNDRED, not "102". No stage, verdict, key, node
  count or scope statement is affected by these two count typos.
- **Batch driver awk incident**: the driver's first attempt mis-parsed the
  published row-spec table (an awk `$3 $4 $5` column-offset error, correct
  columns being `$2 $3 $4`), producing four bad invocations: k09/k10 emitted
  GATE_FAIL (stones mismatch) and k11/k12 ran under a wrong key (hi=65536 with
  lo misread). All four outputs were deleted and never published; the driver was
  fixed and the four rows re-run cleanly (k09 4,622,038; k10 4,945,820; k11
  8,105,873; k12 6,593,392, each LOSS(2) with identical 2-run pairs). The
  pre-registered C4 fail-closed input gates demonstrated the mismatch catch on
  invocation; the wrong-key runs for k11/k12 were detected by the driver's
  expected-key check before audit.
- **k19 v-run supersede**: the first k19 -v attempt was executed without the
  pre-registered `--verify-legal=1` (identical verdict/expansions/ttHits, wall
  ~50.9s); it was superseded BEFORE publication by the correctly flagged re-run
  (identical counts, wall 90.65s). The published `out/k19-cold-v-legal.txt` is
  the flagged run. The k13 v run was executed with the flag from the start
  (wall 97.84s).
- The tamper battery's first baseline attempt in its freshly built kit layout
  failed ONLY 36 file-location pin gates (the harness had laid inv/ and inv5/
  one directory too deep); fixed by moving the two symlinks, no audit-content
  edit; re-run then 850/850 rc=0 (recorded in the tamper log).
- No verdict consumed. The still-parked keys k20/k33/k38 were neither measured
  nor claimed (k38's L50M follow-up remains unclaimed). The delegated pinned C++
  second-implementation gate (`9193f5b6...`) stays with the scrutiny owner; it
  could not be run in this sandbox (no C++ toolchain, re-verified); the parallel
  C++-gate lane separately closed the k01..k08 chain (`28ed2d9c`).
- Concurrency: HEAD re-fetched immediately before pushing; the six commits
  pushed to main between the declaration and this publication (C++ gate kit
  `e42e44a4`/`2112241a`/`c5a67038`/`342abc50`/`28ed2d9c`, z-strip
  `6057ed51`/`637d15e1`...) touched no path written by this batch (verified by
  path-filtered commit listing; the experiment dir was last touched by this
  lane's own `ebdc7de7`).

## Result summary (verdict-level; nothing consumed)

32/32 rows verdict-level agreement: 30 LOSS rows third-impl LOSS(2) vs replica
LOSS(2) (2-run determinism pairs identical each); k13 WIN(1) vs replica WIN(1)
L50M x4 (nodes 16,402,480); k19 WIN(1) vs replica WIN(1) L50M x4 (nodes
15,379,062). Batch a-run expansion total 248,762,398. This is the first
independent third-implementation confirmation of the parked4 L50M ladder halt
(k13 and k19), recorded as the scrutiny step required by that lane's
consumption gate; consumption/adoption remains with the scrutiny owner.

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining
third moves {100,108} remain UNKNOWN throughout. Node/expansion counts, budgets
and wall times are never verdicts. This session consumed no verdict, touched no
cache file, no probe-dir path, no parked4-kit path (READ-only), no K item and
no knowledge README (repo).
