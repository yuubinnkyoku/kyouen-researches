# n11-ultra-cheap-u02-adoption-reaudit-20261127

Kit of the FOLLOW-UP Part declared in this kit's DECLARATION.md
(publish-then-execute, declaration commit a95f1fd4): the BASE
(0ec4080d..., the ultra-cheap u01 head of record, 6,891 rows WIN 209 /
LOSS 6,682) vs SCENARIO (82b52577..., the adopted ultra-cheap u02 head
of record, 6,892 rows WIN 210 / LOSS 6,682) class-status census
measurement and the reaudit refresh of the new canonical head.

## Files

- DECLARATION.md - the single-owner declaration, published BEFORE
  execution (commit a95f1fd4).  sha256
  1d0f1e7d4fc481b445944db4ad075edfc78f2710034571b62d75814c166fed47.
- reaudit/scripts/refresh_adoption_ultra_cheap_u02.py - byte-clone
  of the published ultra-cheap u01 refresh d0fa1762... (clone chain
  eleventh-cost k01 refresh 0355d7fb... <- tenth-cost k01/k02 refresh
  280d7062... <- ninth-cost 12-row c9a7372a... <- eighth-cost k01
  7e11a316... <- SZ wave E d8b14697... <- SV fd2e799e... <- ST
  02987d1c... <- SQ 60dfb1a1... <- SP 82ddb89c... <- sixthwin5
  92a884c9... <- EM 7f379b71... <- EV f2edac3e... <- EU 6dc24c15...),
  differing in EXACTLY the three regions (docstring, CACHE path,
  expected cache sha); every computation byte is identical
  (machine-verified before publication: line diff = only the two
  CACHE/SHA config lines).  sha256
  525a130d4597e3438baa41ea8802777cd2729edca6b841246ff5f7cf3c07a3db.
  The declaration commit placed this file at scripts/ (byte-identical
  copy, same sha256; disclosed in the u01 precedent kit and kept
  here).
- reaudit/output/refresh-summary.json - refreshed class census
  against the adopted ultra-cheap u02 head (6,892 rows WIN 210 / LOSS
  6,682; census unknown 34,382 / excluded_now 138 / free_now 39 /
  excluded 390).  sha256
  722c70d89aa125b8abe089807d87b56a893d3fc6113ce42e7d99662b9b9da70d.
  Three determinism runs byte-identical (fresh cold, ~59 s each).
- reaudit/output/closure-classes.csv - refreshed closure ladder (802
  data rows).  sha256
  535e2684c11e659a9f1c36d70094cd8e0567277c199c708ddd79d35cbf0849e1 -
  NOT byte-identical to the BASE side: the serving class 2251 LEAVES
  the ladder (803 -> 802 rows, left [2251], entered []), class 14338
  loses one unknown child (unknown_now 56 -> 55, the only unknown_now
  churn) and the ladder re-ranks (779 rank-churn cells).
- reaudit/output/per-root-coverage.csv - refreshed per-root coverage
  (20 roots).  sha256
  a5d0e9dee1ed842557344fb475e28f4bccfaffecc3230523b800fc5610eac57a -
  NOT byte-identical to the BASE side: exactly two rows differ, root
  5's individual greedy union drops 2,866 -> 2,865 and root 37's
  grows 3,619 -> 3,639 (measured greedy re-routes;
  free_now/uncovered identical on all 20 roots).
- reaudit/output/probe-worklist.csv - refreshed probing worklist
  (64,268 data rows, 3,715,002 bytes, sha256
  9fec423a4c62ce7cf5048b2e5c5f34ece768246e5e5fe2c39e5aeb4ab7689d6b)
  - UNPUBLISHED per size policy (smaller than the BASE pin
  5feaba28.../3,715,117 bytes: the adopted key's probe row leaves
  the worklist); pinned here.
- scripts/measurer_adoption_ultra_cheap_u02.py - the flip-census
  measurer, a disclosed structural adaptation of the published
  ultra-cheap u01 measurer c5ff4883... (all expectations measured
  from the first execution run before publication; includes a
  fail-closed tamper battery 4/4).  sha256
  e3df6a7368b6b80511a8fa6cdc0bc534682b07527b37ecfaba55a498e3a2ad4d.
- output/census-deltas-ultra-cheap-u02-adoption.json - the
  measurement record.  sha256
  fe4e0ad1740833fa45639652d5293fcaa103737f0fdd6d94eb15a0a941b71f45.
  Three determinism runs byte-identical.

## Measured result (win-hit Part EW/EM mechanism)

- The single adopted row (u02 `1297036830121656320:131074` WIN(1),
  s5 index 93815, serving class 2251) flips exactly its THREE owner
  classes from unknown to excluded_now: 2251
  (`1155314042043105280:0`, cost-unknown 1 -> 0, the adopted row
  owned here), 2287 (`10412322888236400640:0`, 92 -> 91) and 14338
  (`1152921504606847008:544`, 56 -> 55).
- Census: unknown 34,385 -> 34,382, excluded_now 135 -> 138,
  free_now 39 -> 39 (Board-verified both sides), excluded 390 -> 390.
- The closure ladder loses the serving class (803 -> 802 rows) and
  re-ranks (779 cells); one unknown_now churn (14338: 56 -> 55).
- Per-root: two individual greedy re-routes (root 5: 2,866 ->
  2,865; root 37: 3,619 -> 3,639); joint greedy 43,776 -> 43,830 (a
  scheduling quantity, NOT a coverage claim); probing worklist
  64,270 -> 64,268 rows.
- update8: the adopted s5 index 93815 sits INSIDE the frozen baseline
  requirement (resolved 283 -> 284, remaining_now 31,388 -> 31,332,
  groups_free_now 131 -> 131); the win-hit group set grows 31 -> 35
  (four added groups, all owned by class 14338).

## Deviation from the pre-registered expectation (disclosed)

The declaration pre-registered ONE class flip (unknown 34,385 ->
34,384, excluded_now 135 -> 136, free_now 39 unchanged; the u01
three-owner caveat pre-disclosed).  The MEASURED census is unknown
34,382 / excluded_now 138: the WIN key u02 has THREE owner classes
(the serving class 2251 plus 2287 and 14338), the same three-owner
pattern the u01 WIN measured.  The declaration itself provides that
"a deviation is recorded as an experimental fact, not silently
adjusted"; the measured values supersede the prediction everywhere
in this kit.

## Honest disclosures

- The declaration commit placed the refresh script at scripts/
  (byte-identical copy of the canonical reaudit/scripts/ placement;
  same sha256 525a130d...).
- The BASE-side kit inputs (u01 reaudit reaudit/output trio and
  output census json, and the u01 head cache 0ec4080d..., plus the
  u02 adoption manifest d8321e8a... and increment ef727442...) were
  byte-fetched from published main and sha-verified before the
  measurement; the local work tree copies are byte-identical.
- The measurer transform from the u01 measurer was machine-verified
  (unique-count assertions on every replacement); the full assertion
  chain of the u01 measurer was preserved with the u02 measured
  values substituted, then run three times fresh cold from the
  published-byte-verbatim inputs.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Guards

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO root excluded.  Nodes are bookkeeping, never verdicts.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.
