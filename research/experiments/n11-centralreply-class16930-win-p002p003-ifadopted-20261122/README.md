# n11 central-reply closure: batch-13 (class 16930) p002/p003 IF-ADOPTED decomposition (Part AI, 2026-11-22)

Read-only planning/audit experiment (no solver search, no new verdicts),
declared before any execution in the single-owner note as **Part AI**
(note amendment commit `a0cdb0da`, 2026-11-22T13:08Z).

## Takover record (honesty first)

The Part AI declaring host pushed its declaration at 13:08Z and then went
silent: no status update, no experiment directory, and no kit evidence
appeared on main for more than two hours (observed at HEAD `858a4158`,
2026-11-22T15:18Z, and again at HEAD `ada9bc95`, 2026-11-22T15:25Z; the
`n11-centralreply-class16930-win-p002p003-ifadopted-20261122` directory was
absent both times). Under the same convention previously applied in Part U
(batch-8) and Part Z (batch-11) - a declaring host silent well past the
20-minute threshold with no status publication allows takeover - the hosts of
this session executed the published declaration. Every input is a published
main byte re-verified on this host before use; nothing in the Part AI
declaration was changed. Verdicts were NOT consumed at any point.

## Scope

Batch 13 (class 16930, renewed closure rank 11) probed 4 keys (p001-p004,
probe_order 486-489 of the canonical worklist) before its pre-registered
WIN-HALT rule fired twice in the same wave: p002 and p003 are the 11th/12th
unconsumed closure WINs (p002: 2-pass node-exact result 1, 10,770,254 nodes;
p003: result 1, 7,489,274 nodes), p001/p004 are exact LOSS (4,631,275 /
2,291,059 nodes). Third-implementation verdict-level cross-verification of
all four rows is published (Part AG, audit 71/71 gates). This experiment is
the Part V/R/AB/AH-style if-adopted decomposition of those 4 rows:

* **PWIN2**  = BASE + the 2 WIN rows only (p002/p003)
* **PLOSS2** = BASE + the 2 LOSS rows only (p001/p004)
* **PFULL4** = BASE + all 4 resolved rows

BASE is the published Part AH base control
(`research/experiments/n11-class8106-n005n006-base-control-20261122/`), whose
three outputs are byte-identical to the published Part Y canonical
(closure-classes `61943b85...`, per-root-coverage `33f01a0c...`,
refresh-summary `25987add...`) over the canonical 6,027-row merged cache
(sha256 `95e868d6...`). The identical 3-file payload is NOT republished here.

## Bring-up verification on this host (fail-closed, all PASS)

* Published batch-13 sources re-verified byte-identical against main
  (commit-pinned raw URLs at `858a4158...`): 8 raw replay files
  (p001-p004 x p1/p2), status.log, and input/batch-keys.json
  (sha256 `c6c56a1a...`, 52 keys): 10/10 byte-identical.
* BASE control refresh re-executed fresh twice on this host with the pinned
  Part Y refresh script (`88671526...`): both runs byte-identical to each
  other AND to the published canonical on all four outputs, including the
  probe-worklist (`1807e4d2...`, 65,154 rows). This is the fifth independent
  cross-host reproduction of the Part Y canonical outputs.
* Increments maker executed twice: byte-identical outputs.
* Scenario merges: sha-pinned union merger (`90711961...`, selftest PASS) -
  6,027 + increment, WIN/LOSS conflicts 0, duplicates elided 0.
* Scenario refresh: 4-hunk diff-verified adapt of the pinned base script
  (docstring / ROOT / CACHE path / CACHE_SHA_EXPECTED only), executed twice
  per scenario, 6/6 runs byte-identical.
* Honest operational note: the first win2 attempt was OOM-killed at ~4s
  because two refresh processes were launched concurrently on this 2-core
  host; all six final runs were executed serially. No partial output reached
  any published or canonical file.

## Increments (fail-closed gates, all PASS)

3-way node-exact gate (p1/p2/status; batch-13 has no takeover pass - the
batch was executed by the declaring host only, Part AE verbatim),
batch-keys legal/(lo,hi) agreement for every key, 4 distinct keys, ZERO
overlap with the canonical BASE cache (structural gate, any overlap ABORTs;
batch-13 post-dates the Part Y merge), ZERO quarantine registry hits, WIN
set exactly {p002, p003}:

| increment | rows | sha256 |
|---|---|---|
| increment-batch13-wins2-IFADOPTED-20261122.cache  | 2 (WIN p002/p003) | `bb238f67...` |
| increment-batch13-loss2-IFADOPTED-20261122.cache  | 2 (LOSS p001/p004) | `50c09a06...` |
| increment-batch13-full4-IFADOPTED-20261122.cache  | 4 (2 WIN + 2 LOSS) | `3a8bcb11...` |

## Scenario caches (analysis-only, NOT canonical)

| cache | rows | WIN/LOSS | sha256 |
|---|---|---|---|
| merged-batch13-wins2-scenario-20261122.cache  | 6,029 | 160/5,869 | `c180e6d6...` |
| merged-batch13-loss2-scenario-20261122.cache  | 6,029 | 158/5,871 | `ac7b6cdd...` |
| merged-batch13-full4-scenario-20261122.cache  | 6,031 | 160/5,871 | `faacb374...` |

## Machine-verified decomposition results (output/decomp-deltas-batch13.json)

Every class_status_count was recomputed from graph + update8 + cache and
asserted equal to the published summaries for BASE and all three scenarios
before any delta was reported (fail-closed). The delta extractor ran twice
with byte-identical output (`c62cabb4...`).

* **PWIN2**: excluded_now 23 -> 28. The flip set is machine-measured
  IDENTICAL to the frozen-graph eligible holder union of the two WIN S5
  children: **{4903, 5471, 5513, 5626, 16930}** (5 classes; p002 s5 185003
  holders {4903, 16930} with membership_class_count 2; p003 s5 203419
  holders {5471, 5513, 5626, 16930} with membership_class_count 4; overlap =
  class 16930 only; all 5 baseline UNKNOWN, none already excluded_now -
  exactly the declaration's frozen-graph expectation, re-derived here from
  the graph). Class 16930 is the only multi-WIN holder (2 WINs), the same
  structure class 8106 showed in Part AH/AJ. unknown classes 34,501 -> 34,496.
* **PLOSS2**: ZERO flips (excluded_now 23, free_now 35, unknown 34,501);
  update8 resolved 75 unchanged (p001/p004 are NOT frozen-baseline
  requirements; 0 newly-resolved rows, in contrast to batch-12 whose LOSS
  rows were baseline requirements); joint greedy 35,242 unchanged; probe
  worklist 65,154 -> 65,152 (-2).
* **PFULL4**: excluded 28 / unknown 34,496 (identical to PWIN2: the LOSS rows
  flip nothing); class 16930 unknown_now 52 -> 50/50/48 (PWIN2/PLOSS2/PFULL4,
  additivity True); probe worklist -> 65,150 (-4, additive).
* **update8**: resolved 75, remaining 31,784, win-hit groups 0 in EVERY
  scenario - neither p002/p003 nor p001/p004 sit inside the frozen update8
  baseline requirement, so this batch is update8-neutral (contrast Part AH:
  batch-12 rows resolved 75->163, and Part AJ: win_hit_groups 0->29).
* **free_now 35 and per-root free coverage identical to BASE in every
  scenario; root 27 (known-loss baseline) stays 119/119 everywhere.**
* **joint greedy 35,242 unchanged in all scenarios** (cost-neutral batch,
  like batch-6). Per-root individual_greedy_union scheduling sizes DID move:
  roots 26 and 48 each -2 (PWIN2) / -2 (PLOSS2) / -4 (PFULL4), additive on
  every root (no nonadditive roots).
* Class 16930's row in closure-classes.csv moves rank 11 -> 5 with
  unknown_now 52 -> 50 in BOTH PWIN2 and PLOSS2 (adopting any 2 resolved
  children tightens the scheduling rank identically); the flips themselves
  are status-level and are not visible in closure-classes.csv, which lists
  candidate classes by unknown-count only. closure-classes.csv is
  byte-identical between PWIN2 and PLOSS2 for this structural reason.

Scheduling reading only (not a verdict): adopting the 2 published LOSS rows
of batch-13 would shrink the probe worklist by 2 with zero status flips and
zero update8 movement; adopting the two WINs would exclude exactly 5 classes
(the batch class 16930 itself plus its 4 peers of the frozen-graph holder
union) and shrink the worklist by 2 as well, but remain HYPOTHETICAL
adoptions pending the scrutiny owner. The 4 increment verdicts stay
unconsumed published evidence outside the canonical cache. p005-p052
(48 keys) remain unprobed and UNKNOWN.

## Files

Not published here (kept in the lane kit mirror with recorded sha256s):
the three scenario probe-worklist.csv files (~3.7 MB each; Part AH
precedent), whose sha256 values are:

* PWIN2 probe-worklist.csv: `2d2dbad4cb2871b14b1d0be48c3ca6c32c01d5d5f7c47d835434f00ee1f857b1`
* PLOSS2 probe-worklist.csv: `07036eaee53a30f594b4b692eb6b7271f4da19450c4600c3fa82c5ae819f526f`
* PFULL4 probe-worklist.csv: `b1bbee4b0cc64e6c6a1b041e7f6cb62de57cca9aee0ef86137ae3f225948f9d6`

MANIFEST-sha256.txt covers every published file of this directory.

## Interpretation guards (unchanged)

* Verdicts are NOT consumed. The p002/p003 WINs remain unconsumed closure
  WINs (adoption waits on the scrutiny owner, C++ second-implementation
  gate pin `9193f5b6...`); p001/p004 LOSS rows remain unconsumed published
  evidence outside the canonical cache.
* The standard 11x11 empty board, the 19 central-reply roots, class 16930
  (p005-p052 unprobed) and every other class remain UNKNOWN.
* Nodes/expansions are bookkeeping, never verdicts.
* Batch 14 (Part AF, in flight) and batch 16 (Part AM, class 10687) files
  were read-only throughout this experiment.
