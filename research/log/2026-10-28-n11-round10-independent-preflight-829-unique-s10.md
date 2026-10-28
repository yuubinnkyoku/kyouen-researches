# 2026-10-28: N11 post-round9 next-batch independent geometry preflight

Read current main, `AGENTS.md`, knowledge README, K0023/K0105, the round9 terminal and proof-only replan logs, and the frozen `next-plan.json`. The empty-board result remains **UNKNOWN**.

The next 32 proposed canonical S9 keys were independently checked with 4x4 integer Bareiss determinants, including all 126 quadruples of each S9 root. Their complete legal S10 child boundaries were independently enumerated and D4-canonicalized; the 3x3 determinant method agreed.

| Bounded preflight metric | Value |
|---|---:|
| Safe canonical S9 candidates | 32 / 32 |
| Ordered legal S9→S10 obligations | 830 |
| Distinct canonical S10 children | **829** |
| Repeated S10 child classes | **1** |
| Ordered S9→S8 reverse incidences | 288 |
| Distinct canonical S8 predecessors | **286** |
| Repeated S8 predecessor classes | **2** |

The only shared S10 child is `00006000100020821080000000000030`, shared by selection indices 22 and 24 (zero-based). The other 828 S10 children occur once in this batch. Consequently, **within-batch S10 leaf deduplication saves only 1 of 830 obligations (0.12%)**, before any cross-batch cache lookup or early LOSS witness search. This is an exact structural measurement, not a measured wall-clock speedup and not a terminal verdict. The 43 potential S8 hits in the replan are still potential, not proven WIN8.

Added `research/experiments/n11-s9-post-round9-replan-20261028/audit_next_batch.js` with frozen selection SHA-256 checking, independent S9 safety, 3x3/4x4 child-set comparison, reverse S8 incidence checks, expected child-sharing regression, and negative controls for duplicate/modified keys and forged empty-board claims. Added a bounded sparse-checkout CI workflow `.github/workflows/n11-s9-post-round9-preflight.yml`; [workflow run 40654502979](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40654502979) was pending at recording time. The direct independent 4x4 calculation agreed on 32, 830, 829, and the shared S10 key; the full committed script and reverse-incidence assertions still require the CI run to complete.

The practical implication is that a large within-batch shared-terminal-cache speedup is **not** available for these 32 candidates. Cross-batch certified S10 WIN reuse, early LOSS witnesses, or different candidate selection remain more promising. Do not interpret 829 distinct children as 829 mandatory terminal searches: LOSS9 needs only one LOSS10 witness, whereas WIN9 requires all children.

Proof-only WIN8 remains **5449**, conditional 14-root unproved edges **93**, new two-stone closures **0**. Standard 11×11 empty-board outcome **UNKNOWN**.
