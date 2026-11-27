# n11-ultra-cheap-u04-adoption-reaudit-20261127

Kit of the FOLLOW-UP Part declared in this kit's DECLARATION.md
(publish-then-execute, declaration commit `34b3c559`): the BASE
(c5082866..., the ultra-cheap u03 head of record, 6,893 rows WIN 211 /
LOSS 6,682) vs SCENARIO (beecb024..., the adopted ultra-cheap u04 head
of record, 6,894 rows WIN 212 / LOSS 6,682) class-status census
measurement and the reaudit refresh of the new canonical head.

## Files

- DECLARATION.md - the single-owner declaration, published BEFORE
  execution (log commit `34b3c559`); this kit copy differs from the
  published log file in exactly the title line (the u03 kit
  precedent).  sha256
  47ca38c8c750c17c59dd2086cfef56abf9dda8faf788747934eb8a0cb3e05ee0.
- reaudit/scripts/refresh_adoption_ultra_cheap_u04.py - byte-clone
  of the published ultra-cheap u03 refresh 84304650... (clone chain
  ultra-cheap u02 refresh 525a130d... <- eleventh-cost k01 refresh
  0355d7fb... <- tenth-cost k01/k02 refresh 280d7062... <- ninth-cost
  12-row c9a7372a... <- eighth-cost k01 7e11a316... <- SZ wave E
  d8b14697... <- SV fd2e799e... <- ST 02987d1c... <- SQ 60dfb1a1...
  <- SP 82ddb89c... <- sixthwin5 92a884c9... <- EM 7f379b71... <- EV
  f2edac3e... <- EU 6dc24c15...), differing in EXACTLY the three
  regions (docstring, CACHE path, expected cache sha); every
  computation byte is identical (machine-verified before
  publication: line diff = only the two CACHE/SHA config lines).
  sha256 db61c8505b122c0e99cd6c51ed10ab6c2920ec79c590580911650d7f461c0d49.
  A byte-identical copy is also placed at scripts/ (same sha256;
  u01/u02/u03 kit precedent).
- reaudit/output/refresh-summary.json - refreshed class census
  against the adopted ultra-cheap u04 head (6,894 rows WIN 212 / LOSS
  6,682; census unknown 34,376 / excluded_now 144 / free_now 39 /
  excluded 390).  sha256
  d35900b9a8eb4d6043fef7ce4bfe8950c8749ac5ec2685fe51af96e604dac958.
  Three determinism runs byte-identical (fresh cold, ~58 s each).
- reaudit/output/closure-classes.csv - refreshed closure ladder (800
  data rows).  sha256
  ef3447481abb14af3c56a64251d86e63b178c7fb57b0ce8898e67303c24dc3e2 -
  NOT byte-identical to the BASE side: the serving class 23101 LEAVES
  the ladder (801 -> 800 rows, left [23101], entered []) and the
  ladder re-ranks (800 rank-churn cells, ZERO unknown_now churn - the
  first all-rank churn in the ultra-cheap family).
- reaudit/output/per-root-coverage.csv - refreshed per-root coverage
  (20 roots).  sha256
  d3c404e9d216d2e953082b7862ecec217e5c27e4baf798cfc286b7f870e311e8 -
  NOT byte-identical to the BASE side: exactly two rows differ, root
  26's individual greedy union drops 5,227 -> 5,087 and root 24's
  drops 2,776 -> 2,775 (measured greedy re-routes;
  free_now/uncovered identical on all 20 roots).
- reaudit/output/probe-worklist.csv - refreshed probing worklist
  (64,265 data rows, 3,714,832 bytes, sha256
  c38831c1c2ed9a2f186386111fcfcd9657e1b08fe15b3398f86cfbd02328a2e5)
  - UNPUBLISHED per size policy (smaller than the BASE pin
  ece16723.../3,714,889 bytes); pinned here.
- scripts/measurer_adoption_ultra_cheap_u04.py - the flip-census
  measurer, a disclosed structural adaptation of the published
  ultra-cheap u03 measurer a86cf188... (all expectations measured
  from the first execution run before publication; includes a
  fail-closed tamper battery 4/4).  sha256
  8f2451903c3444e3e3428a25847a8bc017fee136dcf117fd0b6131fae50765b8.
- output/census-deltas-ultra-cheap-u04-adoption.json - the
  measurement record.  sha256
  2092e7a8807035888566f225aecfeaa6047d6919714ae434072c57b68e7ddee1.
  Three determinism runs byte-identical.

## Measured result (win-hit Part EW/EM mechanism)

- The single adopted row (u04 `1152921505747697664:1032` WIN(1),
  s5 index 745184, serving class 23101) flips ALL FOUR of its owner
  classes from unknown to excluded_now (the first 4-owner adoption in
  the ultra-cheap family): 23092 (`1152921505747697664:8`,
  cost-unknown 112 -> 111), 23101 (`1152921504892059648:16`, the
  serving class, 1 -> 0), 23115 (`1152921505680588800:1032`, 105 ->
  104) and 23938 (`1152921504673955840:1032`, 100 -> 99).
- The serving class 23101 was still UNKNOWN on the BASE head (the
  u03 serving-class pre-exclusion caveat did NOT materialise); the
  adopted row resolves its LAST unknown cost child (1 -> 0, the
  class leaves the closure ladder 801 -> 800) and flips it to
  excluded_now (its first win-hit).
- Census: unknown 34,380 -> 34,376, excluded_now 140 -> 144,
  free_now 39 -> 39 (Board-verified both sides), excluded 390 -> 390.
- The closure ladder loses the serving class and re-ranks (800
  cells); ZERO unknown_now churn (the first all-rank churn).
- Per-root: two individual greedy re-routes (root 26: 5,227 ->
  5,087; root 24: 2,776 -> 2,775); joint greedy UNCHANGED at 43,830
  (a scheduling quantity, NOT a coverage claim); probing worklist
  64,266 -> 64,265 rows.
- update8: the adopted s5 index 745184 sits OUTSIDE the frozen
  baseline requirement (resolved 284 -> 284, remaining_now 31,332 ->
  31,332, groups_free_now 131 -> 131); the win-hit group set is
  UNCHANGED (35 -> 35, no added or removed groups).

## Deviation from the pre-registered expectation (disclosed)

The declaration pre-registered the graph-derived FOUR-owner union
flip prediction (23092, 23101, 23115, 23938 all unknown ->
excluded_now, census unknown 34,380 -> 34,376, excluded_now 140 ->
144).  The MEASURED census and flip list match the prediction
EXACTLY (the first ultra-cheap adoption with zero census/flip
deviation); the pre-disclosed serving-class pre-exclusion caveat did
NOT materialise.  The only measured deviation is in a SCHEDULING
quantity: the probing worklist drops 64,266 -> 64,265 (ONE row, the
adopted key's own probe row for serving class 23101), not the naive
four-membership-rows prediction 64,266 -> 64,262; a sorted content
diff against the BASE-variant regen shows exactly one deleted row
plus trailing-counter decrements on surviving rows.  Recorded as an
experimental fact, not silently adjusted; scheduling quantities are
never coverage claims.

## Honest disclosures

- The BASE-side kit inputs (u03 reaudit reaudit/output trio and
  output census json, and the u03 head cache c5082866..., plus the
  u04 adoption manifest 3241759f... and increment c6344d3a...) were
  byte-fetched from published main and sha-verified before the
  measurement; the local work tree copies are byte-identical.
- The BASE-side worklist pin ece16723.../3,714,889 bytes was
  additionally reproduced by a temporary (unpublished) BASE-variant
  refresh run (the u03 refresh config with the u03 head cache): the
  regen reproduced the published BASE worklist pin sha
  byte-for-byte, plus the BASE summary/closure/per-root pins
  7cd44879.../137cc49b.../4e27453a... byte-for-byte.
- The measurer transform from the u03 measurer was machine-verified
  (unique-count assertions on every replacement region); the full
  assertion chain of the u03 measurer was preserved with the u04
  measured values substituted, then run three times fresh cold from
  the published-byte-verbatim inputs.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Guards

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO root excluded.  Nodes are bookkeeping, never verdicts.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.
