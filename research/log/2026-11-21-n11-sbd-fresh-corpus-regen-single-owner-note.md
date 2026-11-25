# 2026-11-21 n11 S4 (1297036692683752448,0) corpus fresh regeneration (JS replica): single-owner declaration

- Declaration time: 2026-11-21T15:39Z. HEAD at declaration: `904e7b40b2f8bf7f4e06b19d9f3de13a47124028`. This declaration claims the following 101 S5 keys so that no other agent starts the same exact searches.
- Background: the 2026-11-21 union-audit/reconciliation measurement lane
  (`research/experiments/n11-s5-frontier-census-20261121`, outputs sha256 `7280376d...`, `cd7631a5...`)
  identified 108 backward-only rows (107 LOSS + 1 WIN) that are absent from the current
  reply27 JS-replica chain (probe-13, 5,756 rows, sha256 `60e0dc34...`) and not quarantined,
  and deputed their adoption to the evidence owners. **This lane does NOT adopt them.**
  It re-executes the load-bearing part from scratch, chain-native, under the same
  recipe/evidence norms as reply27 probe #1-#13, so that the decided-class corpus is
  re-established in the live chain lineage by fresh computation instead of by adoption.
  Historical verdicts are used only as post-hoc comparison material; any disagreement
  (including a fresh WIN where history recorded LOSS) is published and blocks the class
  closure claim, exactly as the reply27 acceptance conditions require.
- Claimed targets (deterministic, machine-checkable selection):
  1. The 99 canonical S5 children of S4 `(1297036692683752448,0)` that are absent from the
     probe-13 chain cache (= 106 children - 7 already in chain; identical to the 99
     backward-only rows the union audit attributed to this S4). Includes
     `(1152921504607899649,536870912)` (the historically S6-derived child; handled per
     acceptance condition 5).
  2. The 2 unclaimed backward-only LOSS rows outside that S4's child set:
     `(1152921504606851072,805306370)`, `(1188950301626859520,671088640)`.
  Explicit exclusions (never started by this lane): the 7 focus-class-lane-declared
  backward-only rows (incl. the WIN row `1188950301626859520:603979776`, whose evidence
  stays with the focus lane and K0374/K0379), all reply27-two-target-declared supply probes,
  and all quarantined keys. Overlap with the reply27 13 published targets is empty by
  construction (their targets are in the chain; these keys are not).
- Execution medium: Node.js replica of the pinned exact-replay path of
  `cpp/solvers/kyouen_dfpn_root.cpp` at commit `154f3b7a67`
  (source sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`),
  identical bytes to the reply27 probe publications (`scripts/jsreplay.js`, sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`). This host has no
  C++ toolchain. CPU use: at most 2 workers (host has 2 cores), fresh 2^22 PnTT per row,
  one solver per row, publish=ALL, exact-order=count, <= 15,000,000 node budget.
- Acceptance conditions (all must hold before any verdict is used or published):
  1. Node-exact validation gate (already passed on this host this session, fresh): the
     replica reproduces all 4 published raw replay rows of
     `research/experiments/n11-two-target-design-20261010/output/raw`
     (at2m x2: result 0, nodes 2,000,000, legal 98/99; 15M rows: result 2,
     nodes 3,651,923 and 5,040,200) with identical stones/legal/is_or/budget/result/nodes.
  2. Cold runs only: fresh TT (2^22) per row, deadline 0, exact-order=count, 15,000,000
     node budget per pass; a second independent pass re-runs every settled row for the
     determinism gate (identical result and node count), mirroring probe #13's twice-run
     15M gate and the Oct 12 batch norms. Budget-exhausted UNKNOWN rows are kept as honest
     raws, never forced, and are escalated only by the documented derivation route or a
     later lane.
  3. Every new verdict is geometry-verified with the repo-independent integer geometry
     (`research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py`,
     sha256 `954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f`): 5 stones,
     D4 canonical, safe (no forbidden quadruple), legal count re-derived, S4 parent
     membership in the frozen 3,384-class geometry (sha256
     `146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54`), absence from
     the probe-13 chain base and the quarantine registry (sha256
     `81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9`);
     WIN/LOSS conflict against the base fails closed.
  4. A fresh WIN verdict on any corpus key halts the class closure claim: the witness is
     published, the corresponding classes are then marked per protocol (class completion
     aborted) only with their own machine check, and no S4 class of this lane is marked
     LOSS unless the class-wide all-children-LOSS condition is machine-checked against
     geometry. No third-move coverage claim without a regenerated move-by-move certificate.
  5. For `(1152921504607899649,536870912)`: direct 15M run in pass 1 (history says it stays
     UNKNOWN there); its LOSS, if re-established, is derived only through a fresh cold
     re-execution of the single published S6 LOSS witness `(1152921504675009536,536870912)`
     (6 stones, legal 87, expected 5,859,060 nodes at 15M, twice-run for determinism) plus
     machine-checked membership (independent Board regenerates the S5->S6 boundary and the
     witness must be one of the canonical children) and odd-stone AND polarity; the cache
     row is written with nodes=0 per the Oct 12 derived-row precedent
     (`n11-s4-boundary-direct-20261012`). No S6/S7 exploration beyond this one witness key.
  6. Class-wide closure, coverage, and the root certificate are produced only by the
     published Oct 12 audit pipeline (adapted copies with documented path-only diffs):
     `audit_frontier.py` (all 3,384 S4 boundaries regenerated from the new merged cache),
     `audit_root_loss.py` (move-by-move 119/119 certificate, forcing moves 100/108 to this
     S4), `reclassify_115_candidates.py`, `cache_aware_reply27_cardinality.py`, and
     `analyze.py` over the new cache. The root `{60,27}` statement is only restated with
     this regenerated certificate; it adds chain-native evidence to K0414 (which keeps its
     existing status) and does not touch the empty board.
  7. Publication: raw input/out files per key and per pass + SHA-256 manifest + audit JSON
     + new merged cache file (new file; base probe-13 cache byte-preserved) + analysis
     outputs regenerated from the frozen geometry; latest `main` re-fetched before every
     push; fetch-back byte verification on publish. If another agent's concurrent
     publication touches the same keys, that target is skipped and recorded per the
     reply27 protocol; cache conflict detected anywhere fails closed and stops publication.
- Evidence type: fresh solver-trusted exact rows (replica with node-exact raw validation and
  independent geometry audit); NOT terminal-only minimax. The repo's pinned C++ binary
  remains the reference implementation; any later C++ reproduction disagreeing with these
  rows fails closed in favor of discarding the increment.
- Non-goals: no adoption of historical rows, no focus-class-lane keys, no S6/S7 enumeration
  beyond the single witness key, no multi-root or empty-board claims, no restart of the
  36-root depth-10 sweep, no modification of published files of other lanes.
- Status guard: the standard 11x11 empty board remains UNKNOWN. Nodes, solved counts, and
  proxy values are never verdicts. Until every gate of acceptance condition 6 passes and is
  published, the two-stone root {60,27} keeps its current guarded treatment in lane
  documentation; this lane re-establishes evidence, it does not skip verification steps.
