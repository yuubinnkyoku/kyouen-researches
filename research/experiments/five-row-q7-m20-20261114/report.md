# 5x20 (q=7) row-deficient maximal safe configuration nonexistence — complete enumeration + independent SAT cross-check (2026-11-14)

## Claim

**No deficient maximal safe configuration exists on the 5x20 integer grid with q=7**
(any maximal safe configuration on 5x20 has row occupancy exactly (6,6,6,6,6), i.e. exactly 30 stones).

Consequence for the fixed-width stabilization threshold M_{5,7} (least m such that every
maximal safe configuration on 5xm is full): the witness-free set of widths is now {18⁻witness, 19, 20},
i.e. the least witness width m with a deficient maximal is 18 (K0332, 29 stones) and both m=19
(K0738–K0759) and m=20 (this experiment) are witness-free. Therefore **M_{5,7} ∈ {19, 20} or M_{5,7} ≥ 22**
(the [21,158] band of the old upper bound K0332/K0024 remains for persistence beyond 20; the witness
frontier moves to 5x21).

## Method 1: complete class enumeration (primary system)

The K0738–K0759 machine (`multi_deficient_runner.ts`, ported verbatim as `scripts/m20_runner.ts`
with W=5, M=20 and a wall-clock slice driver) partitions all deficient configurations by their
exact row-deficiency set D (rows with ≤5 stones; rows outside D hold exactly 6 = q−1 stones,
forced by safety since a row is a q=7 line). Row reflection (r ↔ 4−r) reduces the 31 nonempty
deficiency sets to **19 canonical classes**. Within each class the machine enumerates, for the first
deficient row Y0, all column-mirror representatives of its contents (k = 0..5 stones:
10,878 representatives at M=20), and for each runs the blocker-obligation DFS with
forced-stone/forced-empty propagation and complete fill enumeration of the full rows.

Coverage: 19 classes x 10,878 = **206,682 representatives, witnesses 0, leaves 0 in every class**
(`output/class_*.jsonl`, `output/summary.json`).

Census: exact integer circle census for 5x20 gives **104 circles of size ≥7 (8 of size 7, 96 of
size 8), no circle of size ≥9** (`output/census.json`). This matters because the shared runner's
blocker branch only admits circles of size 7 or 8 (for size L the blocking circle needs exactly
q−1=6 stones among L−1 others, which forces ≥L−7 further empties; the DFS enumerates the single
extra empty only, so L≥9 blockers would be missed). At M=20 (as at M=19, 95 circles) no L≥9 circle
exists, so the branch is complete. 5x19 control: nC=95 matches the K0759 published census.

Machine controls (both PASS, matching published pair-version values exactly):
- 5x19, DEF_ROWS=[0,1], NODE_CAP=600k: done=117, cappedCase=117, maxCaseNodes=28,488
  (heaviest idx 39 = S0 {0,1,2,5,16}), witnesses 0, leaves 0, nC=95 — identical to the
  K0740/K0741 slice A1 control.
- Positive control (documented in the runner header, re-run this session): 5x18 DEF_ROWS=[0]
  reproduces the known K0332-family third witness and `verify()` passes.

Per-class results (all complete, witnesses 0, leaves 0): see `output/summary.json`
(max case nodes: [0,1] 53,386 / [0,2] 45,442 / [0,1,2] 44,146 / [1] 49,984 / [2] 35,593 / ...).

## Method 2: independent SAT cross-check (second system)

A class-split SAT encoding (`sat-crosscheck/class_sat.js`, on top of the K0810 `sat.js` census —
a different census implementation: circleABC integer triples vs the runner's circumcenter form)
asserts per class: safety (≤6 stones per census curve via sequential ≥-counters), maximality
(every empty cell has a curve through it with ≥6 stones), rows in D ≤5, rows outside D exactly 6.
kissat 4.0.4 (official linux-amd64 binary) decides every instance:

- **17 of 19 classes directly UNSAT** (recorded in `sat-crosscheck/records_final.jsonl` with
  conflicts and wall time; e.g. [0,1,2,3,4] 142,715 conflicts / 4.3 s, [0,1] 913,253 / 28.5 s,
  [2] 814,224 / 24.5 s).
- Class [0]: k-split by the deficient row's stone count (k=0..4 direct UNSAT; k=5 subdivided by
  the row's leftmost-stone column minpos=0..9, a sound column-mirror symmetry break — every
  configuration or its mirror has minpos ≤ 9): all UNSAT.
- Class [1]: same decomposition, k=0..4 direct UNSAT, k=5 via minpos=0..9 all UNSAT
  (hardest instance [1] k=5 mp=0: 2.88M conflicts / 133.5 s).
- Positive control: 5x18 class [0] is SAT; the decoded model is a 29-stone configuration with
  row occupancy (5,6,6,6,6) that passes the census-free independent verifier
  (`sat-crosscheck/control_5x18_sat.json`) — validating the encoding end-to-end.

Raw per-run records (including superseded smaller-budget timeouts, deterministic conflict counts
reproduced bit-exact across environment resets) are in `sat-crosscheck/records.jsonl`;
the deduplicated final verdict set is `records_final.jsonl` (50 entries, every instance UNSAT
after the k/minpos decomposition; the three residual non-UNSAT entries there are the superseded
whole-class attempts of [0] and [1]).

The two systems (DFS enumeration with pruning, CDCL SAT) share no census code, no search code, and
no encoding; they agree on all 19 classes and on the positive control. Both are finite
machine verifications up to the correctness of their own implementations; neither is a
number-theoretic proof of the M_{5,7} threshold beyond width 20.

## Scope and status

- Machine-verified (two independent systems): nonexistence on 5x20, all deficiency classes.
- Not claimed: persistence at m ≥ 21 (open; 5x21 is the new witness-search frontier), any claim
  about M_{5,7} beyond "M ∈ {19,20} or ≥22" pending widths 21.., upper bound 158 (K0332/K0024).
- 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4: all still UNKNOWN
  (fixed-width M results do not transfer to no-board win/loss).

## Operational notes

- Two full workspace losses to environment resets mid-session; all pushed checkpoints survived
  and lost slices were re-run deterministically (identical conflict counts / node counts).
- kissat is deterministic: re-runs after resets reproduced conflict counts exactly
  (e.g. 142,715 for [0,1,2,3,4]).
- The single-deficient-row classes are the hardest for both systems relative to their budgets:
  the enumeration closed each in ≤2 slices (≤200 s), while kissat needed the k×minpos
  decomposition (direct runs resisted 240 s at 5.3M+ conflicts). Notably the SAME enumeration
  that needed 26 slices x 600k nodes at 5x19 completed 5x20 in one slice per class for [0],[2]
  — difficulty is not monotone in m for the DFS machine either.
