# Part EM declaration (single-owner): b38loss24 loss-only canonical adoption

- **Part**: EM (continues the n11-centralreply closure lane; the Part EF
  batch-38 completion log registered exactly this adoption as its resume
  note (b)).
- **Owner**: this lane (single-owner).  Counter-declaration sweep performed
  at main `86644142` immediately before this declaration: commit-message scan
  for "Part EM" returned NOTHING; scan for a b38loss24 / ai044 adoption in
  progress returned only the Part EF kit README and the Part EF completion
  log (which registered the 24 fresh exact-LOSS rows - incl. the class-30484
  dual-class child ai044 - as unconsumed future loss-only adoption
  candidates).  No counter-claim exists.  Part EJ (batch-40, class 30118)
  stays in-flight under its original owner (stall window at this
  declaration below the 3.5h takeover threshold; untouched here).
- **Adopted object**: exactly 24 rows - ALL fresh exact-LOSS rows of the
  published, complete Part EF batch-38 kit
  (`research/experiments/n11-centralreply-closure-class30345-batch38-20261125/`,
  MANIFEST-sha256 fixed by `17489a6b` to sha256
  `4dbf8856597709b3bd41d6f185a0502ebbdee447b1fc48d0caab586fdcc5ac02`, 181
  kit files, machine audit batch-audit.json `73652099...` all gates PASS,
  verdicts_consumed false): ai001, ai004, ai008, ai009, ai011, ai012,
  ai015, ai016, ai018, ai019, ai020, ai021, ai022, ai025, ai026, ai027,
  ai029, ai031, ai032, ai033, ai037, ai042, **ai044**, ai045 - every one a
  first-ever probe (absent from the published prior-probe universe
  `6deee846...`, 2,104 pairs), two-pass fresh-cold node-exact at budget
  15,000,000 order 0, both passes identical per key, MISMATCH 0, resolved
  within its own single 15M condition (NO exhaustion history, NO
  re-probe anywhere).  Adopted node total per pass 168,055,078;
  adopted-table digest `a56b1cde...`.  Increment bytes:
  `increment-b38loss24-20261125.cache` (25 comment lines + 24 `s5verdict`
  rows, sha256 `3c6326618944b4c18d37e1fe6cad470b53e712592fe7a19d7190f44f5a26bed4`,
  pinned in this Part's maker).
- **BASE**: the published Part EL canonical merged chain head
  `merged-exact-s5-chain-plus-aj039loss1-20261125.cache` (6,713 rows, WIN 158
  / LOSS 6,555, sha256
  `cf08e1817a369853747706872763046c4544e289eae6d847bfd27d7503d23e7d`).
  All 24 adopted keys are proven absent from BASE (fresh-increment gate;
  the EF kit machine audit already proved all 50 batch-38 child pairs
  absent from the canonical cache; this Part's maker re-proves).
- **Merger**: the pinned fail-closed union merger `s5_union_merge.py`
  (sha256 `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`)
  byte-clone, exactly as in Parts EE/EI/EL.  Merge order BASE first,
  increment second; 3 consecutive runs must be byte-identical (cache +
  merge-audit).  Expected chain head after merge: 6,737 rows, WIN 158 /
  LOSS 6,579.
- **Explicitly NOT adopted / NOT consumed**:
  - The 19 probe-level WIN rows of batch-38 (incl. **ai048**, the
    class-30484 dual-class sibling of ai044, WIN 2,232,854): consumed
    NOWHERE; WIN canonical adoption is scrutiny-owner C++
    second-implementation gate `9193f5b6...` exclusive (g++ unavailable in
    this environment; nothing about any WIN is decided here).
  - The 6 EXHAUSTED keys (ai007/ai024/ai030/ai038/ai040/ai041): honest
    UNKNOWN at the 15M condition; no EXHAUSTED verdict is ever converted;
    the same-condition re-probe prohibition stays in force.
  - b018 (key (1153204079095189504, 65536), prior batch-1 dual-class
    probe-level WIN, 2026-11-22): still unconsumed, still excluded, still
    same-condition re-probe prohibited.
  - aj030 / aj049 / aj050 (batch-39/EK probe-level WINs): unconsumed, sit
    in NO cache.
- **Expected structural effect (to be machine-pinned, never asserted by
  hand)**: closure class 30484 unknown 5 -> 4 through the adopted ai044
  (the remaining 4: aj030 + aj049 + aj050 unconsumed probe-level WINs and
  ai048 the unconsumed dual-class WIN; NOT freed, NOT excluded); closure
  class 30345 fresh-unknown shrinks by the adopted LOSS rows; per-root
  coverage, update8 quantities, closure-table churn, joint greedy and
  worklist bookkeeping are all recomputed by the EM refresh fork and the
  EM delta extractor and pinned from measured output only.
- **Protocol** (ident to Part EL):
  1. kit wave B: `make_increments_em_adoption.py` (EL-maker fork adapted to
     the Part EF artifacts, 24-row pool) + merger byte-clone, published
     first (publish-then-execute), fetch-back byte-verified;
  2. maker executed 3x byte-identical + tamper battery fail-closed; emits
     increment-b38loss24-20261125.cache + increments-manifest.json (schema
     `em-b38loss24-increments-manifest-v1`);
  3. merger executed 3x byte-identical; outputs published (wave C);
  4. EM refresh fork (`refresh_adoption_em.py`, EL-refresh fork with the EM
     merged cache pin) published, executed against the published EM cache,
     reaudit outputs published (wave D);
  5. EM delta extractor (`compare_deltas_em_adoption.py`, EL-extractor
     fork with BASE = the published Part EL reaudit outputs) published
     with machine-measured pins, executed, decomp published (wave E);
  6. README + MANIFEST-sha256 + completion log (wave F).
- **UNKNOWN guards**: the standard 11x11 empty board, the 19 central-reply
  roots, the two-stone roots {49,60}/{59,60}, S2 (59,60) and classes 1/2/4
  all stay UNKNOWN.  Loss-only adoption consumes no WIN verdict, frees no
  class, excludes no class; nodes are bookkeeping, never verdicts.  No
  verdict about the 11x11 game value may be inferred from this Part.
