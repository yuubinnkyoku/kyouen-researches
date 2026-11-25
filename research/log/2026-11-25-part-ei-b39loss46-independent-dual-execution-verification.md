# Part EI b39loss46 46-LOSS adoption: independent dual-execution verification

Date: 2026-11-25.  Author: the second (parallel) hourly run of the Part EI
long-term lane.  This log is NOT the owner completion log (that is the
publication chain 7400d708 -> cb93eb9a -> 29d0a0ff -> cbe900bc -> fd29f7db ->
651a0670); it records an additive verification fact: the Part EI adoption was
executed end-to-end TWICE by two fully independent tool implementations that
converged byte-for-byte on every canonical object, and the published wave-1
kit was re-executed in an isolated clean tree reproducing every published
byte.  No conflicting file is touched; 11x11 stays UNKNOWN throughout.

## 1. The independent (pre-kit) execution

Before the wave-1 kit appeared on main, this run had already executed the
declared Part EI plan (declaration 8ddb0c72) with its own fail-closed tooling
(all gates fail-closed, tamper batteries included; byte pins below; local
execution tree, never pushed):

* maker 1d18f12e7761c802eba9609aba2f6cd2565cf1f2222f56bd101677cdc9a5e441 ->
  increment 440399f4d866187c7544df43ed627fafefc24b6be2bcf292ad03828f041f9e04
  (46 LOSS rows, 3x byte-identical), manifest 300b9290a0d718c936034e4089bcb6bdad33bc882448254943f1542e2affad8b,
  adopted-table digest a7ef2336dd7a93f43619a58677de2c11b6126bb89c5c8cb7fef144dfc4b3d2db,
  adopted nodes/pass 140,162,086 of packet 177,032,132;
* refresh fork be41fe28ea1674ddd59aa062277d3223a1162821290d2d6055dc5959adf45996
  (EE wave-F fork 01937f23 + docstring/CACHE pin only) -> reaudit outputs
  closure-classes e12bf3280c77e31fc91e30e6806d2828b141af565bfa5e565a2aa3410d974673,
  per-root-coverage 2525f3069826a055bf9bf4343c08ac217722beefdce054138a68a0976c875b8d,
  probe-worklist 98529a8ddd457c09506a80ce2f7a6344fee3c3fcc0d63969aa391e67ad6c8e79,
  refresh-summary 414314eb38776f7fee69b3f6d1b894ab24b8e4fac4ea578bc109fce82863329f;
* union merger byte-clone 90711961 + adopted increment -> merged canonical cache
  73482be0cf0201b2d812f9205b0315e91527234e02196691279753853feddc70
  (6,712 rows, WIN 158 / LOSS 6,554; 3x byte-identical);
* extractor e4385dd6c9926c155e66dc223b4f33a55fc02c188f020914ad783006b22d769a
  (EE extractor 7660b441 as model, EH-kit honesty gates folded in) -> PASS with
  tamper battery 3/3 (below).

## 2. Convergence with the published wave-1/2/3 chain

Two independent implementations produced:

* the SAME adopted-table digest a7ef2336... (identical 46 (lo,hi,legal,result,
  nodes) rows row-for-row; only serialization headers differ: published
  increment a2b24baa... vs 440399f4...);
* the BYTE-IDENTICAL merged canonical cache 73482be0... (the merger keeps
  comments from the BASE input, so the header difference vanishes: the
  canonical object is serialization-independent);
* the BYTE-IDENTICAL all-four reaudit outputs (e12bf328 / 2525f306 /
  98529a8d / 414314eb), reproduced by both refresh forks;
* the SAME delta conclusions: class 30484 unknown 52 -> 6 rank 20 -> 9 (46 own
  adopted; 2 EXHAUSTED honest-UNKNOWN aj030/aj039 + 2 unconsumed probe-level
  WIN aj049/aj050 + 2 claim-reserved batch-38 pairs ai044/ai048 remain; NOT
  freed, NOT excluded), class 30118 unknown 54 -> 52 rank 39 -> 21 (its only
  2 children adopted in common with the packet), closure table 807 rows
  static with exactly 29 rank-churn-only rows and 776 fully stable rows,
  update8/class_status byte-static (resolved 259 / remaining 31,600 /
  groups_free 131; every adopted s5 index outside the frozen baseline
  requirement AND outside the receipt), joint greedy 36,508 -> 36,505,
  worklist 64,414 -> 64,366, known_universe 845 -> 891, cache_in_universe
  822 -> 868.

## 3. Clean-tree re-execution of the published wave-1 kit

Fresh download of the published kit (maker ff96435a..., refresh 1bcf1972...,
extractor 5433c4c2..., merger 90711961 byte-clone identical to the pinned
clone), executed in an isolated 195-file tree staged from published inputs
only (BASE fc3e4ac9, Part EH kit 52b69c04 178 files, graph 54f9c364,
update8 b658290a, board 954d3a10, policy 78655e94, quarantine 81d23160):

* their maker -> increment a2b24baa0acb253f6b5a2901b601834b8dc50163ad500407192989efcc75e659,
  manifest 6ae4058b4e419a4a05ddfff1947b23aa52acdd54febecb5d207aed7241ea5338, PASS;
* their merger 3x -> audits 387010c54846676aed1cc83ae5606bc8b6e8399fc022ee9bee8f192786b128e1
  x3 identical, merged cache 73482be0... (byte-equal to BOTH executions);
* their refresh -> closure e12bf328 / prc 2525f306 / worklist 98529a8d /
  summary 414314eb (all byte-equal to published and to the independent run);
* their extractor -> PASS (same deltas) -> decomp
  6b8b3e7d9e2103a813f0b97ff144b47655635cd7f8f4f79ac604f23f902ba0ba (byte-equal
  to published).

Every byte of the publication chain (14 MANIFEST pins) was thus reproduced by
a second party before this log was written.

## 4. Tamper batteries executed during this verification

* independent maker battery 9/9 fail-closed + control PASS (BASE byte-flip,
  raw flip, status digit; deep rewires: batch-audit 46->45, status nodes,
  quarantine, universe, closure 52->51, increment pin; each caught by the gated
  pin or a results-level arithmetic gate);
* union merger battery: WIN/LOSS conflict abort, within-increment conflict
  abort, duplicate-nodes first-occurrence determinism;
* independent extractor battery 3/3 fail-closed: (1) closure-classes unknown
  tamper + pin rewire -> caught by the refresh double-run byte-regeneration
  gate; (2) manifest row_counts 46->45 + full rewire -> caught by the
  row_counts decomposition gate; (3) coordinated increment+merged cache+
  manifest+audit node bump + 4-pin rewire -> caught by the adopted per-pass
  node-sum gate (140,162,086 pinned from the published kit raws).

## 5. Honest notes

* The published Part EH README Results table transposes the WIN node counts
  (lists aj049 (1,871,594) / aj050 (4,998,452)); the status.log SSOT and every
  machine object (batch-keys, batch-audit, raws, both EI manifests) agree on
  aj049 = 4,998,452 / aj050 = 1,871,594.  Both Part EI publications record the
  SSOT values.  No adoption impact (WIN rows are consumed nowhere).
* This run started as the declared single-owner execution; main advanced
  during the run (waves 1a-1c arrived 11:38-11:40Z from the parallel run).
  Per the lane protocol this run then switched to verification mode, adopted
  the published kit as SSOT, and published only this additive log.  No
  conflicting write was made.

## 6. Resume state (machine-derived from the published bytes)

* 11x11 empty board and all 19 central-reply roots stay UNKNOWN.
* Class 30484 is NOT freed (6 remaining) and NOT excluded; the two
  claim-reserved batch-38 pairs belong to Part EF (single-owner in-flight).
* Next adoption opportunities: Part EF batch-38 completion; fresh-frontier
  probing now points below rank 9 (closure_classes_first after this Part:
  23101/1849/2251 unknown 1, 16371 unknown 2, 16757 unknown 3, 5804 unknown 4,
  34908 unknown 6, 20421 unknown 6, 30484 unknown 6, 34269 unknown 11).
* WIN rows are consumed ONLY by the scrutiny-owner C++ second-implementation
  gate (pin 9193f5b6...); EXHAUSTED rows are non-reprobe at the same
  condition (a higher-budget re-probe needs its own declaration).
