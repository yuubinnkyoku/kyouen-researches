# 2026-10-19: n11 S11 witness costs, independent dual-and-branch optimality

Starting main: `c6ec3081c0badcfbf98b2341a1afae9f9279a1a7`. Reviewed `AGENTS.md`, `research/knowledge/README.md`, K0023, K0414, K0416, n11 coordinator reports, current compact terminal-cover experiment and recent n11 logs. **Standard 11×11 empty-board outcome remains UNKNOWN. No new two-stone root was closed.**

The existing 18 S8 LOSS roots, 387 S9 obligations, 3,044 S10 boundary positions and 184 S10 LOSS leaves are unchanged. Their 184-leaf global minimum remains restricted to the S10 one-reply certificate format. For the 672 high-dual-weight S10 WIN obligations, all legal S11 replies give 4,522 distinct D4-canonical S11 candidates, of which 982 are LOSS and 3,540 WIN from the S11 side-to-move perspective. A fresh C++ direct-board minimax pass recomputed all 4,522 candidates (86,411 memoized states) and exactly matched the saved classifications, move counts, state counts and witnesses.

**New independently checkable optimality:** the 672-by-982 witness-cover graph has 47 independent connected components. Exact nonnegative rational LP-dual inequalities plus exhaustive 0/1 branching establish the following *global* lower bounds over all 982 eligible S11 LOSS witnesses:

| Objective | Proven minimum | Feasible witnesses | Verified proof nodes |
|---|---:|---:|---:|
| Number of distinct S11 witnesses | 331 | 331 | 109 |
| Sum of per-witness terminal memoized states | 7,779 | 342 | 57 |
| `1000 * states + witness count` | 7,779,342 | 342 | 57 |

Since 1,000 exceeds the entire candidate count 982, the last objective lexicographically minimizes state cost first and witness count second. Thus **342 is the smallest witness count among all covers attaining the proven minimum cost 7,779**. This improves the previously saved 345-witness cost-optimal cover by three witnesses without changing the 7,779-state cost. The 184 S10 LOSS leaves still cost 15,290 states; additive certificate cost remains 23,069. These minima concern the specified one-ply S11 witness-cover formalism and additive independent terminal-state cost, not wall time or the complete game.

The standalone `verify_optimality.py` uses Python standard-library exact fractions, reconstructs the complete witness-incidence graph from board geometry, checks every branch and every dual inequality, and verifies matching feasible covers; it does not call SciPy/HiGHS. `compact_proof184_342.py` independently re-solves the 184 S10 LOSS leaves and 342 selected S11 LOSS witnesses to terminal and verifies the 184-leaf minimum. Fresh C++ direct-board minimax rechecked all 4,522 candidates and the selected 342 (342 LOSS, 7,779 states). The three mutation tests (dual, branch, missing witness) were rejected. A pure-Python full 4,522-candidate rerun was attempted but did not finish within the runtime limit; the prior archive reports full C++/Python cross-check.

**Reproducibility artifact:** `n11-s11-dual-branch-optimality-20261019.zip`, SHA-256 `fdbcbc2f9b3caf8e736f426668ec56db1c84e8ff4649900c60a54be0b7ff71e1`, saved in the user's Library at `/共円ゲーム研究/n11-s11-dual-branch-optimality-20261019.zip`. Contains all 4,522 verdict rows, source and candidates, 3 rational dual/branch certificates, 342-witness compressed independent certificate, checkers, mutation tests and reproduction script. **The complete archive is not part of this Git commit; this log alone is not a standalone proof artifact.** Do not promote this result to the knowledge SSOT without preserving the proof files in-repository and running AGENTS.md checks.

No new S6, S4, two-stone root, or empty-board verdict is claimed. **UNKNOWN**.
