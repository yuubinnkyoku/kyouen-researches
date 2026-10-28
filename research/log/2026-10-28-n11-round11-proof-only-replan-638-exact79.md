# 2026-10-28: N11 round11 proof-only replan, 709 → 638 eligible S9 classes

Reviewed current `main`, `AGENTS.md`, `research/knowledge/README.md`, K0023, the round10/round11 terminal certificates, round11 lift, and the round11 replan implementation. Recovered the completed [round11 replan CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40685524320), **PASS** at commit `dce88b5ffe56e883824ab26c9aa15a8ac4c5985f`. The exact output was uploaded as artifact `n11-round11-proof-only-79-edge-replan` (ID `12814703128`, ZIP SHA-256 `42416f75a17bc7bc53b15c88b6b06ed5124e923685b7b98af1496ae19aa2d415`). No branch or PR was created.

The bounded replan independently replayed the round11 minimal terminal certificate with 3×3 and 4×4 exact integer geometry and forged-witness rejection, verified upstream hashes and all three LOSS10→LOSS9 parent closures, reconstructed the earlier 709-class candidate census, and applied only certified exclusions and fixed-plan incidence pruning:

- Before round11 exclusions: **709** eligible S9 classes.
- Proof exclusions: **45**, comprising **32** selected round11 roots and **13** *additional* LOSS9 parent classes derived from certified LOSS10 witnesses.
- Remaining after proof exclusions: **664**.
- No longer incident to the fixed plan's 79 unproved S8 edges: **26**.
- Still eligible: **638** (a reduction of **71**, or **10.0%** from 709).
- Deterministic incidence-dominance reduction: **84** candidates.
- Next 32 selected S9 roots potentially cover **37** of the 79 unproved S8 classes; they have **807** legal S10 children. The exchange stage made **0** swaps. Potential coverage is not proof.
- Proof-only WIN8 remains **5,545**; fixed conditional 14-root S7 plan remains **548** edges, **469** secured and **79** unproved. No WIN/LOSS conflicts, no new S7/S5 verdicts, no new two-stone closures.

The complete ordered selection and its SHA-256 `05f4f971ffeeadb9688a64ab5c67cb6eb193ab891bc3c34c7a0a09515190b53a` are frozen in `research/experiments/n11-s9-post-round11-replan-20261028/next-plan.json`. The existing replan code compares any frozen plan against a fresh reconstruction and fails on mismatch; the workflow already has a path trigger for this JSON. The **post-freeze** CI outcome must be checked separately and is not inferred from the earlier success.

Next: independently preflight the new 32 S9 roots' complete S10 boundaries before any bounded terminal search. Do not treat pn/dn, a partial run, or selected candidate coverage as a winner or distance.

**Standard 11×11 empty-board winner: UNKNOWN.**
