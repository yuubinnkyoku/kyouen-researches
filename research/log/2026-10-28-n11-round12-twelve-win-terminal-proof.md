# 2026-10-28: N11 round12, twelve independently verified WIN9 roots

Continued from the frozen round11 proof-only replan, selecting only its **32** canonical nine-stone positions (selection SHA-256 `05f4f971ffeeadb9688a64ab5c67cb6eb193ab891bc3c34c7a0a09515190b53a`). The independent S9→S10 preflight had already established 807 legal edges / 805 distinct S10 children.

[Bounded discovery run 40702770011](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40702770011) **PASS**. [Independent replay 40702942607](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40702942607) **PASS**. The fixed `certificate.json` proves **12 WIN9 and 20 LOSS9**. For the WIN9 roots, all **311** legal S10 children are terminal-WIN. Each LOSS9 root has a fixed terminal-LOSS S10 witness. Both exact 3×3 difference determinant and independent 4×4 Bareiss integer geometry agree on every terminal verdict, legal move count, and recursion-state count.

Discovery checked 443 distinct terminal S10 classes / 444 first-loss obligations / 80,850 recursion states per geometry. The compact verifier checked 330 distinct terminal S10 classes / 331 obligations / 59,233 recursion states per geometry, rejecting forged WIN9 and LOSS9 witnesses. These are **25.5%** fewer terminal leaves and **26.7%** fewer recursion states, not measured wall-clock speedups. The LOSS10 witness parents form 200 canonical LOSS9 classes, not necessarily 200 globally new verdicts. No within-batch WIN/LOSS conflict.

The upward proof-only WIN8 lift was launched separately at [run 40703068702](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40703068702). Its result must be recovered and checked before claiming an increase over the previous 5,545 WIN8 classes or a reduction of the 79 unproved edges of the fixed 14-root plan.

No new S7/S5 verdicts or two-stone root closures. **Standard 11×11 empty-board winner: UNKNOWN.**
