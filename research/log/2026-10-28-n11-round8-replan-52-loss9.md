# 2026-10-28: round8 certified LOSS10 parent reuse prunes 52 S9 candidates

Reviewed main at `69e285089248e18f6f7357d6dfb347301b933ae2`, AGENTS.md, knowledge/README.md, K0105, K0329, round8 certificate and latest N11 logs. Recovered completed GitHub Actions run 40631305392, which independently replayed the 32 terminal LOSS9 certificates and ran `replan.js`. Its archived `round8-next-plan.json` is now frozen in `research/experiments/n11-s9-post-s10-reuse-round8-20261028/next-plan.json`; the workflow checks byte-for-byte equality against a fresh deterministic replan.

- Before: 1,063 eligible S9 classes (after earlier 383 certified LOSS9 exclusions).
- After adding the 32 round8 certified LOSS10 witnesses and all legal nine-stone parents: **52** eligible S9 classes excluded, including the 32 selected roots and **20 additional unselected classes**; **1,011** remain.
- Dominance-pruned candidate count: **156**. The next fixed 32-class plan has **47 potential S8 coverage classes** and **842 legal S10 child edges**; no exchange improvement was found.
- Frozen selection SHA-256: `b1cce4963565e850598ed0dce4361077ace6933f74855cfd6b187e9cbb1907db`. The full 52 excluded keys and 32 selected keys are stored in the JSON.
- This is **certified candidate elimination**, not a new WIN9 or WIN8 result. Proof-only WIN8 remains **5,407**; conditional 14-root unproved S8 edges **100**; two-stone roots closed **0**; empty-board winner **UNKNOWN**.

The plan is a scheduling heuristic and its 47 potential hits are not a proven coverage increase. It is intentionally not promoted to the knowledge SSOT as an empty-root verdict. Source: https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40631305392 .
