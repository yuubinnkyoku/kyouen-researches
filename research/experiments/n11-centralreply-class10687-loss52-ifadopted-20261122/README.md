# n11 central-reply closure: batch-16 (class 10687) 52-row all-LOSS IF-ADOPTED decomposition (Part AO, 2026-11-22)

Read-only planning/audit experiment (no solver search, no new verdicts),
declared before any execution in the single-owner note as **Part AO**
(declaration appended after the Part AM status update, observed against
HEAD `6af95d9c`, commit `ede3eb42`, 2026-11-22; no counter-declaration was
present on main at push time).

## Scope (single scenario)

Batch 16 (class 10687, renewed closure rank 14, mask
`[1224979098661617664, 0]`, unknown 52, groups (16,56)+(16,64)) probed all
52 of the class's unknown canonical S5 children (t001-t052, probe_order
642-693) and resolved **52/52 all LOSS** with 2-pass fresh-cold node-exact
replay, WIN 0, exhaustion 0, determinism mismatch 0 (published as Part AM:
commits `14092b5e`/`0aac7e0c`/`d349e8f8` plus README erratum `572dcbc3`,
fetch-back 180/180 byte-identical; `input/batch-keys.json` sha256
`465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e`).

Because the batch has zero WIN rows and zero exhaustion rows, adopting
every resolved row of batch-16 equals adopting the 52 LOSS rows exactly.
There is no PWIN/PFULL split; this experiment computes the single scenario

* **PLOSS52** = BASE + all 52 LOSS rows (t001..t052)

which is machine-asserted to be the full-packet scenario
(`increments-manifest.json`: row_counts 52 resolved / 52 losses / 0 wins /
0 exhausted, `full_packet_eq_loss_only` true, `win_scenario_exists`
false, base-cache absent hits 0, quarantine hits 0).

BASE is the published Part AH base control
(`research/experiments/n11-class8106-n005n006-base-control-20261122/`,
refresh-summary `25987add...`) over the canonical 6,027-row merged cache
(sha256 `95e868d6...`). The identical 3-file BASE payload is NOT
republished here.

## Bring-up verification on this host (fail-closed, all PASS)

* Batch-16 corpus on main re-verified before use against the pinned shas
  of the declaration round (batch-keys `465cf447...`, raw 104 = complete
  p1/p2 pairs, status.log) from the kit mirror.
* Increments maker executed twice: byte-identical 52-row increment
  (sha256 `95345a5b...`).
* Union merge: sha-pinned merger `90711961...` (selftest PASS), BASE +
  52-row increment, WIN/LOSS conflicts 0, run twice byte-identical
  (6,079 rows, WIN 158 / LOSS 5,921, scenario cache sha256 `342e8683...`).
* Scenario refresh: 5-hunk adapt of the pinned Part Y refresh script
  (`88671526...`; docstring, scenario cache path, cache sha expectation,
  EXP/ROOT parents depth for the loss52/scripts placement only; adapted
  script sha256 `fb846776...`), executed twice **serially** (~60 s each;
  single-process execution is mandatory on this host after the batch-13
  concurrent-launch OOM), all 4 outputs byte-identical between runs:
  refresh-summary `7fd15927...`, closure-classes `7405699e...`,
  per-root-coverage `ec52a56d...`, probe-worklist (unpublished)
  `3b28ba59...`.
* Delta extractor executed three times: byte-identical output
  `dd6a01ef...`, zero gate failures. It re-executes the published refresh
  class pass from graph + update8 + scenario cache (including Board
  fail-closed child verification of every free candidate) and asserts
  class_status_counts, known-universe counts and per-root coverage
  equality with the published BASE and PLOSS52 summaries before any
  delta is emitted.

## Machine-verified decomposition results (output/decomp-deltas-batch16.json)

* **Zero flips.** A zero-WIN increment can only free, never exclude: the
  excluded_now flip set is machine-checked EMPTY, excluded_now stays 23,
  and the global transition table is exactly
  excluded->excluded (390), excluded_now->excluded_now (23),
  free_now->free_now (35), unknown->free_now (1), unknown->unknown
  (34,500). free_now 35 -> 36, unknown classes 34,501 -> 34,500.
* **The batch's own class is the only mover.** Class 10687 was BASE-unknown
  with all 52 cost children unknown; its BASE-unknown children are
  machine-checked to be exactly the 52 increment keys, so under PLOSS52 it
  becomes (Board-verified) **free_now**: the single newly free class.
  Every other graph holder of an increment child keeps its status; the
  143-class holder union is gated to
  scenario_unknown_now == BASE unknown_now - own increment membership
  per class (e.g. class 10661: 53 -> 52 with own membership 1, class
  10695: remains unknown with own membership 2).
* **Newly free thirds are exactly the batch's two closure groups.** The
  per-root free-coverage recompute (asserted equal to the published
  per-root-coverage.csv for BASE and PLOSS52) finds newly free thirds
  {root first 16, third 56} and {root first 16, third 64} - machine-checked
  identical to the batch's `groups_served_full`. The (central, 16) row is
  the only changed coverage row: free_now 14 -> 16, uncovered 105 -> 103
  (free + uncovered == 119 invariant held); root 27 (known-loss baseline)
  stays 119/119.
* **update8 moves by exactly one requirement.** One of the 52 rows is a
  frozen update8 baseline requirement: resolved 75 -> 76 (the newly
  resolved s5 index 376421 is exactly the increment row at that index),
  remaining 31,784 -> 31,783, win_hit_groups stays 0.
* **Scheduling quantities (measured, heuristic only):** joint greedy
  union 35,242 -> 38,522 (heuristic re-selection, NOT a coverage
  regression: the free-coverage columns are the gated quantity and they
  only improve); unique non-free groups 2,127 -> 2,125; probe worklist
  65,154 -> 65,097 (-57); individual greedy movers: root first 16
  2,539 -> 3,037 (+498), root first 48 2,822 -> 2,880 (+58), root first
  36 2,704 -> 2,703 (-1), all other roots byte-stable.
* **Renewed closure candidate table:** class 10687 leaves the table
  (closure_classes_count 811 -> 810; machine-checked absent), and the
  rank-14 row passes to **class 10661** (mask
  `[1152921505697431552, 0]`, unknown 52, groups (24,30)-range), the
  machine-identified next all-LOSS candidate for a future batch.

Scheduling reading only (not a verdict): if the 52 LOSS rows are ever
consumed through the fail-closed merger as a canonical increment plus an
independent refresh re-audit, class 10687 would qualify as the 36th
Board-verified free class, root 16's two closure groups would be secured,
update8 would advance by one requirement and the worklist would shrink by
57. **None of that is claimed here**: consumption is a separate
declaration + refresh re-run + independent audit (Part AP-equivalent,
batch-10/8784, 8784-reaudit precedent). The adoptions remain
HYPOTHETICAL; the 52 verdicts stay unconsumed published evidence outside
the canonical cache.

## Files

* `status.log` records every doubled run on this host with byte-comparison
  results.
* Not published here (kept in the lane kit mirror with recorded sha256):
  the scenario probe-worklist.csv (~3.7 MB; Part AH precedent), sha256
  `3b28ba59b60f41b82ee9a83bf111164ac87219cec44e4207e15a0fd6c1a72098`.

MANIFEST-sha256.txt covers every published file of this directory.

## Interpretation guards (unchanged)

* Verdicts are NOT consumed. The 52 LOSS rows remain unconsumed Part AM
  evidence; the 14 unconsumed closure WINs (including batch-15 r001/r002)
  still await the scrutiny owner (C++ second-implementation gate pin
  `9193f5b6...`) and are untouched by this experiment.
* Class 10687 is NOT closed by this experiment; `free_now` here is a
  what-if projection on the PLOSS52 scenario cache only. The canonical
  cache is unchanged.
* The standard 11x11 empty board, the 19 central-reply roots, and every
  class remain UNKNOWN.
* Nodes/expansions are bookkeeping, never verdicts.
* Batch 14 (Part AF, declared; Part AQ takeover in flight - the Part AQ
  declaration explicitly does not touch this experiment's scope) and
  batch-15 (Part AN) files were read-only throughout this experiment.
