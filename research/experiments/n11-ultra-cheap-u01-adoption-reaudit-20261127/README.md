# n11-ultra-cheap-u01-adoption-reaudit-20261127

Kit of the FOLLOW-UP Part declared in this kit's DECLARATION.md
(publish-then-execute, declaration commit 740c980b, restated in the
adoption kit README "next follow-up Part" disclosure and in the
adoption completion log): the BASE (1e2eeda2..., the eleventh-cost k01
head of record, 6,890 rows WIN 208 / LOSS 6,682) vs SCENARIO
(0ec4080d..., the adopted ultra-cheap u01 head of record, 6,891 rows
WIN 209 / LOSS 6,682) class-status census measurement and the reaudit
refresh of the new canonical head.

## Files

- DECLARATION.md - the single-owner declaration, published BEFORE
  execution (commit 740c980b).  sha256
  6a2a7c9bb35bdaa00b92555639ea4030b441fc904e257236f753cd8fd3125a3b.
- reaudit/scripts/refresh_adoption_ultra_cheap_u01.py - byte-clone
  of the published eleventh-cost k01 refresh 0355d7fb... (clone chain
  tenth-cost k01/k02 refresh 280d7062... <- ninth-cost 12-row
  c9a7372a... <- eighth-cost k01 7e11a316... <- SZ wave E d8b14697...
  <- SV fd2e799e... <- ST 02987d1c... <- SQ 60dfb1a1... <- SP
  82ddb89c... <- sixthwin5 92a884c9... <- EM 7f379b71... <- EV
  f2edac3e... <- EU 6dc24c15...), differing in EXACTLY the three
  regions (docstring, CACHE path, expected cache sha); every
  computation byte is identical (machine-verified before
  publication).  sha256
  d0fa17627705d816c248bbb28fb5c358dde79d11929bfffdcbb3eedd4199277c.
  The declaration commit placed this file at scripts/ (byte-identical
  copy, same sha256; disclosed here).
- reaudit/output/refresh-summary.json - refreshed class census
  against the adopted ultra-cheap head (6,891 rows WIN 209 / LOSS
  6,682; census unknown 34,385 / excluded_now 135 / free_now 39 /
  excluded 390).  sha256
  2e27ad1afa5eb61ad36d0e8e9a5a4039d3f5e07446ff10163eeedbeba9d94b1c.
  Three determinism runs byte-identical.
- reaudit/output/closure-classes.csv - refreshed closure ladder (803
  data rows).  sha256
  e97ab9865d921c0d1bb69ee995710726a8395f2da1858c86b35b9dc423b187bd -
  NOT byte-identical to the BASE side: the serving class 1849 LEAVES
  the ladder (804 -> 803 rows, left [1849], entered []), class 5160
  loses one unknown child (unknown_now 56 -> 55, the only unknown_now
  churn) and the ladder re-ranks (785 rank-churn cells).
- reaudit/output/per-root-coverage.csv - refreshed per-root coverage
  (20 roots).  sha256
  d2d365393b323d10ae6ab9e03f9fbbf48938b7f57aa0a7256e0941fe50904d6f -
  NOT byte-identical to the BASE side: exactly two rows differ, root
  36's individual greedy union grows 3,001 -> 3,029 and root 49's
  drops 2,696 -> 2,693 (measured greedy re-routes;
  free_now/uncovered identical on all 20 roots).
- reaudit/output/probe-worklist.csv - refreshed probing worklist
  (64,270 data rows, 3,715,117 bytes, sha256
  5feaba280720a1ded80c95e50669162dad7aa0045357a9bceada92373214d0f6)
  - UNPUBLISHED per size policy (smaller than the BASE pin
  407a340f.../3,715,222 bytes: the adopted key's probe row leaves
  the worklist); pinned here.
- scripts/measurer_adoption_ultra_cheap_u01.py - the flip-census
  measurer, a disclosed structural adaptation of the published
  eleventh-cost k01 measurer f286f165... (all expectations measured
  from the first execution run before publication; includes a
  fail-closed tamper battery).  sha256
  c5ff48835fff37364c8c83e4c940f4c5da31ac34f68466e13467eb4787798880.
- output/census-deltas-ultra-cheap-u01-adoption.json - the
  measurement record.  sha256
  a1a84a3e1433534ac763f7b2890540a26ad7ba4e360449bc06cb970d5a2fd644.
  Three determinism runs byte-identical.

## Measured result (win-hit Part EW/EM mechanism)

- The single adopted row (u01 `1153485622925590528:0` WIN(1), s5
  index 81011, serving class 1849) flips exactly its THREE owner
  classes from unknown to excluded_now: 1849
  (`1152922672972169216:0`, cost-unknown 1 -> 0, the adopted row
  owned here), 1858 (`1153484523413962752:0`, 96 -> 95) and 5160
  (`1153485622791372800:0`, 56 -> 55).
- Census: unknown 34,388 -> 34,385, excluded_now 132 -> 135,
  free_now 39 -> 39 (Board-verified both sides), excluded 390 -> 390.
- The closure ladder loses the serving class (804 -> 803 rows) and
  re-ranks (785 cells); one unknown_now churn (5160: 56 -> 55).
- Per-root: two individual greedy re-routes (root 36: 3,001 ->
  3,029; root 49: 2,696 -> 2,693); joint greedy 37,398 -> 43,776 (a
  scheduling quantity, NOT a coverage claim); probing worklist
  64,272 -> 64,270 rows.
- update8: the adopted s5 index 81011 sits INSIDE the frozen baseline
  requirement (resolved 282 -> 283, remaining_now 31,444 -> 31,388,
  groups_free_now 131 -> 131); the win-hit group set grows 25 -> 31
  (six added groups, all owned by class 5160).

## Deviation from the pre-registered expectation (disclosed)

The declaration pre-registered ONE class flip (unknown 34,388 ->
34,387, excluded_now 132 -> 133, free_now 39 unchanged).  The
MEASURED census is unknown 34,385 / excluded_now 135: the WIN key
u01 has THREE owner classes (the serving class 1849 plus 1858 and
5160), the same three-owner pattern the eleventh-cost k01 WIN
measured.  The declaration itself provides that "a deviation is
recorded as an experimental fact, not silently adjusted"; the
measured values supersede the prediction everywhere in this kit.

## Honest disclosures

- The declaration-time placement of the refresh script was
  scripts/ (byte-identical copy of the canonical reaudit/scripts/
  placement; same sha256 d0fa1762...).
- The BASE-side kit inputs (eleventh reaudit reaudit/output trio and
  output census json, and the eleventh k01 head cache) were
  byte-fetched from published main and sha-verified before the
  measurement; the local work tree copies are byte-identical.
- An early owner-class probe in this session mis-read the graph's
  s4_cost layout and briefly suggested owner classes {3170, 3226};
  the corrected machine probe (idx in s4_cost[ci], the same
  expression the published measurers use) yields {1849, 1858, 5160}
  and is what the published measurer asserts.  The erroneous probe
  never left this session's scratch work.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Guards

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO root excluded.  Nodes are bookkeeping, never verdicts.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.
