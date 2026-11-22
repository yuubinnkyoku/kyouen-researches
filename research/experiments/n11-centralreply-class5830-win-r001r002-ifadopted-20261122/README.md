# n11 central-reply closure: batch-15 (class 5830) r001/r002 IF-ADOPTED decomposition (Part AN, 2026-11-22)

Read-only planning/audit experiment (no solver search, no new verdicts),
declared before any execution in the single-owner note as **Part AN**
(declaration appended after the Part AI status update, observed against
HEAD `953ae601`, 2026-11-22; no counter-declaration was present on main at
push time).

## Scope (single scenario)

Batch 15 (class 5830, renewed closure rank 13) probed 4 keys (r001-r004,
probe_order 590-593 of the canonical worklist) and produced a structurally
new outcome: **two honest UNKNOWN exhaustion rows and zero resolved LOSS
rows**.

* r001: 2-pass node-exact **WIN** (2,521,302 nodes, legal 82,
  membership_class_count 1, s5 103560)
* r002: 2-pass node-exact **WIN** (5,973,924 nodes, legal 82,
  membership_class_count 1, s5 103561)
* r003 / r004: 15M-node budget **exhaustion** (result 0, nodes == budget,
  honest UNKNOWN; r003 s5 120355 membership 3, r004 s5 120370 membership 3)

Because the exhaustion rows carry no verdict and the type gate excludes
them from every increment, adopting every *resolved* row of batch-15 equals
adopting {r001, r002} exactly. There is no PLOSS2/PFULL4 scenario; this
experiment computes the single scenario

* **PWIN2** = BASE + the 2 WIN rows only (r001/r002)

which is machine-asserted to also be the full-packet scenario
(`increments-manifest.json`: row_counts losses 0, full_packet_eq_win_only
true, exhausted_excluded_ids [r003, r004] with verdict null and
nodes == budget).

BASE is the published Part AH base control
(`research/experiments/n11-class8106-n005n006-base-control-20261122/`,
refresh-summary `25987add...`) over the canonical 6,027-row merged cache
(sha256 `95e868d6...`). The identical 3-file BASE payload is NOT
republished here.

## Bring-up verification on this host (fail-closed, all PASS)

* Batch-15 corpus on main re-verified before use: 8 raw replay files
  (r001-r004 x p1/p2), status.log and input/batch-keys.json
  (sha256 `af3e4c46...`, 52 keys) - 10/10 byte-identical (verified in the
  declaration round and re-checked against the copies in the kit before
  every run below).
* Increments maker executed twice: byte-identical outputs.
* Union merge: sha-pinned merger `90711961...` (selftest PASS), BASE +
  2-row increment, WIN/LOSS conflicts 0, run twice byte-identical.
* Scenario refresh: 4-hunk diff-verified adapt of the pinned Part AI win2
  refresh script (docstring / cache path / cache sha expectations only),
  executed twice **serially** (66 s / 61 s; single-process execution is
  mandatory on this host after the batch-13 concurrent-launch OOM), all 3
  outputs byte-identical between runs: refresh-summary `496f3761...`,
  closure-classes `37223c04...`, per-root-coverage `f4256c28...`.
* Delta extractor executed three times: byte-identical output
  `e67df758...`, zero gate failures. It re-executes the published refresh
  class pass from graph + update8 + scenario cache (including Board
  fail-closed child verification of every free candidate) and asserts
  equality with the published summaries for BASE and PWIN2 before any
  delta is emitted.

## Machine-verified decomposition results (output/decomp-deltas-batch15.json)

* **The flip is NOT the batch's own class.** Class 5830 was ALREADY
  excluded_now at BASE (5 pre-existing WIN cost children among its 57);
  adopting r001/r002 therefore newly excludes exactly one class: **side
  class 2634** (baseline UNKNOWN, cost 51, holds both r001 and r002 as
  cost children). Flips = {2634}, machine-verified identical to the
  eligible holder union. excluded_now 23 -> 24, unknown classes
  34,501 -> 34,500, free_now 35 unchanged.
* **membership_class_count is closure-scoped.** The batch-keys report
  membership 1 for r001/r002 (their closure-class membership: class 5830
  only), while the frozen-graph s4_cost holder sets, which alone drive
  the refresh semantics, are {2634, 5830} for both keys. Both figures are
  recorded per key in the delta output; the graph holder set gates the
  flip identity. This scope distinction did not arise in batch-13 (whose
  graph holders matched membership counts) and is now explicit machinery.
* **Per-holder unknown_now deltas** (gated to per-class cost membership):
  class 5830 52 -> 50 (own delta 2), class 2634 51 -> 49 (own delta 2),
  both keys multi-WIN holders of exactly 2 holder classes.
* **update8 baseline movement (unlike batch-13, which was update8-
  neutral):** r001/r002 (s5 103560/103561) ARE frozen update8 baseline
  requirements. Adopting them moves resolved 75 -> 77 (the 2 newly
  resolved s5 are exactly the increment universe), remaining 31,784 ->
  31,734, and creates the first win-hit group: win_hit_groups 0 -> 1.
* Scheduling: joint greedy 35,242 -> 35,240 (-2); probe worklist
  65,154 -> 65,150 (-4); free_now 35 and every per-root free coverage
  column identical to BASE; root 27 (known-loss baseline) stays 119/119.
  The only individual_greedy_union mover is the root with origin first 49
  (2,890 -> 2,888, -2).

Scheduling reading only (not a verdict): if the scrutiny owner ever
adopts the two WIN rows, the worklist shrinks by 4, update8 advances by 2
resolved requirements plus one newly win-hit group, and the exclusion
lands on the side class 2634 rather than the (already excluded) batch
class 5830. The adoptions remain HYPOTHETICAL; the increment verdicts
stay unconsumed published evidence outside the canonical cache. r003/r004
are honest UNKNOWN and must not be read as verdicts of any kind;
r005-r052 (48 keys) remain unprobed.

## Files

Not published here (kept in the lane kit mirror with recorded sha256):
the scenario probe-worklist.csv (~3.7 MB; Part AH precedent), sha256
`951b88972ff60a290174cef2dafb78daf3395b424710e1f28d12c58e05d115df`.

MANIFEST-sha256.txt covers every published file of this directory.

## Interpretation guards (unchanged)

* Verdicts are NOT consumed. The r001/r002 WINs remain unconsumed closure
  WINs (adoption waits on the scrutiny owner, C++ second-implementation
  gate pin `9193f5b6...`).
* The standard 11x11 empty board, the 19 central-reply roots, class 5830
  (r003-r052 unresolved/unprobed) and every other class remain UNKNOWN.
* Nodes/expansions are bookkeeping, never verdicts.
* Batch 14 (Part AF, in flight) and batch 16 (Part AM) files were
  read-only throughout this experiment.
