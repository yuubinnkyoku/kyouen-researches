# Part EL declaration (single-owner): aj039loss1 loss-only canonical adoption

- **Part**: EL (continues the n11-centralreply closure lane; Part EK completion
  log registered this as Resume #1).
- **Owner**: this lane (single-owner).  Counter-declaration sweep performed at
  main `b68256ba` immediately before this declaration: commit-message scan for
  "Part EL" returned NOTHING; scan for an aj039 adoption in progress returned
  only the Part EK completion log (which registered aj039 as an unconsumed
  candidate) and the historical Part EH/EI logs.  No counter-claim exists.
- **Adopted object**: exactly ONE row - the aj039 fresh exact-LOSS row of the
  published Part EK 30M re-probe kit
  (`research/experiments/n11-centralreply-closure-class30484-aj030aj039-reprobe30m-20261125/`,
  MANIFEST-sha256 rev2 `97574401309964806a8eed4968496dcd222aecaf029aa9b1115dcaaa2ec78a68`,
  42 files, audit_ek.json `d9aa8aab...` all 79 gates PASS):
  `s5verdict,1152922606282735616,65536,5,2,16549916`
  (key (1152922606282735616, 65536), legal 88, s5_index 897668; two-pass
  fresh-cold node-exact at budget 30,000,000 order 0, pass walls 96 s / 98 s,
  both passes identical, MISMATCH 0; resolves in (15M, 30M] beyond the honest
  EXHAUSTED 15M history - NOT a same-condition re-probe).
- **BASE**: the published Part EI canonical merged cache
  `merged-exact-s5-chain-plus-b39loss46-20261125.cache` (6,712 rows, WIN 158 /
  LOSS 6,554, sha256 `73482be0cf0201b2d812f9205b0315e91527234e02196691279753853feddc70`).
  The aj039 key is proven absent from BASE (fresh-increment gate carried over
  from the Part EK kit; re-proven by this Part's maker).
- **Merger**: the pinned fail-closed union merger `s5_union_merge.py`
  (sha256 `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`)
  byte-clone, exactly as in Parts EE/EI.  Merge order BASE first, increment
  second; 3 consecutive runs must be byte-identical (cache + merge-audit).
  Expected chain head after merge: 6,713 rows, WIN 158 / LOSS 6,555.
- **Explicity NOT adopted / NOT consumed**:
  - aj030 (key (1152922604135251976, 65536)): probe-level WIN 15,284,699 at
    the 30M condition (WIN-HALT), consumed NOWHERE; WIN canonical adoption is
    scrutiny-owner C++ second-implementation gate `9193f5b6...` exclusive
    (g++ unavailable in this environment; nothing about aj030 is decided
    here and aj030 must sit in NO cache).
  - ai044 / ai048 (claim-reserved dual-class batch-38 keys, Part EF
    in-flight single-owner): untouched at pair level.
  - aj049 / aj050 (probe-level WINs of batch-39, unconsumed): untouched.
  - No EXHAUSTED verdict is converted; the honest 15M exhaustion history of
    aj030/aj039 (raws pinned in both the batch-39 kit and the Part EK kit
    sources/exh15m/) stays intact.
- **Expected structural effect (to be machine-pinned, never asserted by
  hand)**: closure class 30484 (54-child Board boundary) unknown 6 -> 5
  (remaining: aj030 probe-level WIN unconsumed, ai044/ai048 EF claim-reserved,
  aj049/aj050 probe-level WINs unconsumed); class 30484 is NOT freed and NOT
  excluded.  Secondary-dual-class and byte-static class sets, update8
  quantities, per-root coverage, closure-table churn, joint greedy and
  worklist bookkeeping are all recomputed by the EL refresh fork and the EL
  delta extractor and pinned from measured output only.
- **Protocol** (identical to Part EI):
  1. kit wave B: `make_increments_el_adoption.py` (EI-maker fork adapted to
     the Part EK artifacts, single-row pool) + merger byte-clone, published
     first (publish-then-execute), fetch-back byte-verified;
  2. maker executed 3x byte-identical + tamper battery fail-closed; emits
     increment-aj039loss1-20261125.cache + increments-manifest.json
     (schema `ek-aj039loss1-increments-manifest-v1`);
  3. merger executed 3x byte-identical; outputs published (wave C);
  4. EL refresh fork (`refresh_adoption_el.py`, EI-refresh fork with the EL
     merged cache pin) published, executed against the published EL cache,
     reaudit outputs published (wave D);
  5. EL delta extractor (`compare_deltas_el_adoption.py`, EI-extractor fork)
     published with machine-measured pins, executed, decomp published
     (wave E);
  6. README + MANIFEST-sha256 + completion log (wave F).
- **UNKNOWN guards**: the standard 11x11 empty board, the 19 central-reply
  roots, the two-stone roots {49,60}/{59,60}, S2 (59,60) and classes 1/2/4
  all stay UNKNOWN.  Loss-only adoption consumes no WIN verdict, frees no
  class, excludes no class; nodes are bookkeeping, never verdicts.  No
  verdict about the 11x11 game value may be inferred from this Part.
