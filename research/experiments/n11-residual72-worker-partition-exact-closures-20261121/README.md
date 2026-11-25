# 36-root worker-partition exact closures and UB witnesses

## Scope

This is an exploratory worker-allocation study on the already-published 36-root, three-ply D4 overlap material. It runs no game search, no depth-10 probes, no certificate extraction, and no receipt folding. The active 36-root depth-10 sweep remains owned by its declared lane and is not modified; no sweep-assignment change is proposed.

The study answers two measurement questions left open by the two preceding lanes:

1. The [worker-partition candidate](../n11-residual72-worker-partition-candidate-20261121/README.md) (class10 1,998 / pair10 2,000, one-swap local optimum under an 8% D4-load spread cap) was proven to be neither a global optimum nor improvable by one swap, but nothing was known about the unconstrained objective landscape, other worker counts, or the 9-stone layer.
2. The [exact class-membership regeneration](../n11-residual72-36root-exact-class-membership-20261121/README.md) published exact class-level copy counts but no optimum or bound for any allocation objective.

## Objectives and constraints

For a balanced assignment of the 36 roots into `W` workers (`36/W` roots each):

- **class10** = cross-worker 10-stone class copies, i.e. `sum` over multi-root 10-stone D4 classes of `(worker span − 1)`; exactly the objective whose baseline/candidate values are 4,189 / 1,998.
- **pair10** = cross-worker pairwise D4 overlap weight; baseline/candidate 4,193 / 2,000.
- **cross9** = the class-type objective restricted to the 9-stone layer (all multi-root 9-stone classes are 2-root); baseline/candidate 104 / 49.
- **T1** = balance only (9 roots per worker, `W = 4`). **T2** = T1 plus the candidate lane's 8% D4-load spread cap.

## Inputs (all published, SHA-256 pinned in the scripts)

- `research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json` (census; `94fdb0c6…`)
- `research/experiments/n11-residual72-worker-partition-candidate-20261121/output/worker-partition-candidate-20261121.json` (candidate partition; `09b394b8…`)
- `research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-10stone-20261121.json` (`5fec87af…`)
- `research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-09stone-20261121.json` (`68aa7df1…`)
- `research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/exact-class-membership-20261121.json` (`37ea472e…`)

## Method

Each mode first runs a deterministic simulated-annealing UB search (xorshift128, mode-specific fixed seed, 60,000 iterations per restart), then a DFS branch-and-bound that enumerates only assignments with objective strictly below that UB. **Closure therefore proves the UB is the exact global optimum over all balanced `W`-worker assignments; budget exhaustion is recorded honestly as "not closed"** (the UB is then only an upper bound). Branch-and-bound uses heavy-first root ordering (this alone cut w3class from 324M to 326k nodes), group-label symmetry breaking, capacity propagation, and a min-conflict lower bound restricted to feasible groups. The anneal and every leaf assert accrued-objective equality.

Determinism: closed modes re-run byte-identically (modulo wall-clock fields). For budget-exhausted runs the node counts reflect the publishing machine's speed and are recorded as run conditions, not as reproducible constants.

## Results

Exact global optima (closed by branch-and-bound; the anneal witness and the B&B bound coincide):

| mode | W | objective | exact optimum | witness pair10 | witness cross9 | B&B nodes | budget |
|---|---|---|---|---|---|---|---|
| w2class | 2 | class10 | **732** | 737 | 17 | 1,931 | 100 s |
| w2pair | 2 | pair10 | **737** | 732 | 17 | 1,955 | 100 s |
| w3class | 3 | class10 | **908** | 913 | 22 | 301,671 | 100 s |
| w3pair | 3 | pair10 | **913** | 908 | 22 | 308,146 | 100 s |

Not closed within budget (upper bounds only; **not** proven optima):

| mode | W | objective | UB witness | B&B nodes | budget |
|---|---|---|---|---|---|
| w4class | 4 | class10 | **1937** | 501,219,328 | 170 s |
| w4pair | 4 | pair10 | **1939** | 686,817,280 | 170 s |
| w6class | 6 | class10 | **2558** | 249,561,088 | 90 s |
| w6pair | 6 | pair10 | **2562** | 351,272,960 | 90 s |
| x9 | 4 | cross9 | **47** | 316,669,952 | 150 s |

Structural findings:

- For every `W` in {2, 3, 4, 6} the class-objective witness and the pair-objective witness are the **same partition**.
- The W=4 witness is a **super-witness**: one partition attains class10 1937, pair10 1939, and cross9 47 simultaneously (9-stone UB 47 independently witnessed also by a different x9-mode partition; the 47-witness is not unique).
- Super-witness gaps vs the published candidate: class10 −61, pair10 −61, cross9 −2.
- The super-witness is **T2-infeasible** (D4-load spread 10.7893% > 8% cap), so it does not contradict the candidate's T2 one-swap optimality.
- One-swap certificates from the published candidate partition: under T1, 486 feasible swaps, 3 improving, best `13 ↔ 19` reaching 1937 (class) / 1939 (pair) — the unconstrained witness is reachable by a single swap from the candidate. Under T2 the published check is reproduced exactly (222 feasible, 0 improving, best 1,998 / 2,000).
- Large-budget anneal: T1 modes (1,500 restarts each) never beat 1937/1939; T2 modes (2,500 restarts × 60,000 iterations each) never beat 1998/2000. **T2 global optimality remains UNKNOWN** (no closure run).
- Heavy-first ordering helped w2/w3 but did not close w4/w6/x9; index and dynamic orderings also failed to close x9 within budget.

- **Addendum (9-stone-layer closures, same day)**: the branch-and-bound also closed the 9-stone-layer cut for `W = 2` and `W = 3`: exact global optima **cross9 = 17** (1,198 nodes) and **cross9 = 22** (157,346 nodes). The x9w2 witness is the **same partition** as the w2class/w2pair witness: for `W = 2` one single balanced partition simultaneously attains class10 732, pair10 737, and cross9 17 — all three optima co-attained. At `W = 3` the 10-stone-optimal witness also attains cross9 22; a distinct x9w3 partition attains 22 as well, so the 9-stone optimum 22 is non-unique.

- **Addendum 2 (witness neighborhood certificates, same day)**: exhaustive 486-swap neighborhoods around the UB witnesses: the W=4 super-witness is a **strict 1-swap local optimum in all three objectives simultaneously** (best neighbors class10 1962, pair10 1966, cross9 48 — every balanced swap strictly worsens), and the distinct 9-stone x9 witness is a (non-strict) cross9 1-swap local optimum (best neighbor 47). This is local-optimality evidence only, not a global-optimality proof.

## Output and verification

`output/` contains 22 JSON results: 11 closure-suite runs (9 plus addendum x9w2/x9w3), plus the addendum-2 witness-neighborhood certificate, 4 one-swap exhaustive checks, 4 anneal searches, the consolidated `experiment_summary_20261121.json`, and the verifier result.

`scripts/verify_worker_partition_20261121.py` is a fail-closed independent verifier (pure Python, no code shared with the JS search/solver): it re-pins all five inputs, rebuilds all objectives from the raw class lists, reproduces the published candidate-lane statistics (including its one-swap check), reproduces the exact-class-membership experiment's published `partition_stats`, recomputes every witness, and checks closure wording, same-partition findings, the super-witness, and T2 infeasibility. **ALL 167 GATES PASS** (142 in the first publication, plus 20 addendum gates (x9w2/x9w3) and 5 addendum-2 witness-neighborhood gates: x9w2/x9w3 witness recomputation, closure wording, same-partition check against w2class, distinctness from w3class, and 9-stone co-attainment of the 10-stone witnesses). Re-run from the repository root, it reproduces the checked-in verifier result byte-identically.

Reproduction (from the repository root; run scripts print JSON to stdout):

```sh
node research/experiments/n11-residual72-worker-partition-exact-closures-20261121/scripts/worker_partition_bnb_closure_20261121.mjs w3class 100 > w3class_result.json
#   args: <mode> [budget_seconds] [anneal_restarts]; modes: w2class|w2pair|w3class|w3pair|w4class|w4pair|w6class|w6pair|x9|x9w{N}
node research/experiments/n11-residual72-worker-partition-exact-closures-20261121/scripts/worker_partition_witness_search_20261121.mjs t2class 2500 > t2class_result.json
#   modes: t1class|t1pair|t2class|t2pair|oneswapT1class|oneswapT1pair|oneswapT2class|oneswapT2pair
python3 research/experiments/n11-residual72-worker-partition-exact-closures-20261121/scripts/verify_worker_partition_20261121.py
#   all 22 result JSONs must be present in output/; writes output/verify_worker_partition_20261121_result.json
python3 research/experiments/n11-residual72-worker-partition-exact-closures-20261121/scripts/oneswap_witness_neighborhood_20261121.py
#   addendum 2: witness-neighborhood certificates; writes output/oneswap_witness_neighborhood_20261121.json
#   (requires w4class_result.json and x9_result.json in output/)
```

Node counts for the closed modes are deterministic; wall-clock-bound modes will differ. w4/w6/x9 closure needs a stronger lower bound or a different method; those runs are recorded as honest not-closed results, not as optima.

## Interpretation boundary

This is a geometric worker-allocation study of the published 36-root class tables. Class-copy objectives measure geometric redundancy only; a shared D4 class does not establish an actual transposition-table hit, and no measured TT hit rate exists yet. Do not change the active sweep's assignment based on these numbers: the super-witness is T2-infeasible, and its hypothetical gain (−61/−61/−2) is unvalidated against real cache behavior.

No new WIN/LOSS verdict, certificate, or closed receipt row is produced. Node counts and solved/objective values must not be read as win/loss evidence; REFUTED-D10 is not a LOSS proof. **The standard 11×11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and class 1/2/4 verdicts all remain UNKNOWN.**
