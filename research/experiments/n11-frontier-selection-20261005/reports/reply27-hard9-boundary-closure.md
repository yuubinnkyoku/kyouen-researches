# Reply=27 hard-s5 boundary closure

Date: 2026-10-05

11×11 empty board remains **UNKNOWN**.

For the fixed root first=60, reply=27, the 31-class selected frontier left nine hard canonical s5 roots after the 15M cold replay pass. Their complete canonical s6 boundary contains 816 positions. The sharded GitHub Actions proof run `37269759034` solved or exhausted every one of those 816 boundary entries and the merge verifier rejected verdict conflicts.

Boundary totals:

- canonical s6: **816**
- exact WIN: **729**
- exact LOSS: **81**
- still UNKNOWN at the per-root budget: **6**
- conflict count: **0**
- total exact nodes: **901,901,494**

The parent s5 recurrence is decisive despite six unresolved s6 entries: a five-stone parent is LOSS as soon as one s6 child is exact LOSS, and is WIN only when all canonical s6 children are exact WIN. The nine hard s5 roots therefore classify as:

| s5 key | verdict | s6 children | WIN | LOSS | UNKNOWN |
|---|---|---:|---:|---:|---:|
| (1152921504742115328, 536870912) | LOSS | 92 | 90 | 2 | 0 |
| (3602879701897445376, 134217728) | LOSS | 89 | 85 | 4 | 0 |
| (10520408729537478660, 67108864) | WIN | 88 | 88 | 0 | 0 |
| (10520408729538527232, 16384) | LOSS | 94 | 79 | 15 | 0 |
| (10520408729541689344, 0) | LOSS | 103 | 50 | 47 | 6 |
| (10520408729554255872, 32768) | LOSS | 77 | 75 | 2 | 0 |
| (10520408730615414784, 0) | LOSS | 100 | 99 | 1 | 0 |
| (10520408730619609088, 0) | LOSS | 90 | 89 | 1 | 0 |
| (10520408746717347840, 8) | LOSS | 91 | 82 | 9 | 0 |

Thus the hard set is **8 LOSS / 1 WIN / 0 UNKNOWN**.

The reusable derived cache is:

`research/experiments/n11-frontier-selection-20261005/output/reply27-hard9-s5-verdict-cache.csv`

The derivation script is:

`research/experiments/n11-frontier-selection-20261005/scripts/derive_hard9_s5_cache.py`


## Cheap-witness heuristics failed

Before the 816-root boundary solve, the focused workflow `N11 hard s6 witness probe` (run `37268780726`) tested two cheaper policies.

- the six shared s6 roots from the first outcome-blind greedy cover were **WIN 6 / LOSS 0**, all exact;
- a broader 54-root low-legal probe was **WIN 54 / LOSS 0**, all exact.

So neither maximizing shared parents nor trying the cheapest-looking low-legal s6 first found a LOSS witness for any hard s5. The complete boundary nevertheless contained **81 LOSS s6** and closed eight parents as LOSS. The measured positive relation between legal count and exact-search cost therefore must not be reinterpreted as an outcome predictor.

The proof is a frontier result only. It does not by itself decide reply=27 or the 11×11 empty board.
