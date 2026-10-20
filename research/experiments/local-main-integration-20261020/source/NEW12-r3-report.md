# NEW12-r3: a new 12-stone maximal safe set on 12×12

## Question

Does a maximal safe set of exactly 12 stones exist on the 12×12 board (standard rules: 4 concyclic or collinear points forbidden)? If so, how does it compare with the known 11×11 constructions (minimum maximal 10 stones, maximum lower bound 21 stones)?

## Method

- Reused the existing heuristic fixed-size safe-set walker `saturation_20261003_search.cpp` (random restarts, remove-and-replace moves, energy = number of legal additions), compiled with `g++ -O3 -std=c++17`.
- Target: `n=12, k=12`, run for a bounded 90 s (seed 20261017). A run with `legal_count == 0` at size 12 is a maximal safe 12-stone set.
- Candidate was then independently verified by exhaustive integer geometry in Python (4×4 determinant for circle/collinearity; no use of the search's internal masks).

## Parameters

- Board: 12×12, `V = 144`.
- Forbidden quads enumerated by search: 158,426.
- Search time: 90.0 s wall clock.
- Steps: 11,302; restarts: 1.
- Best energy reached: 0 (maximal).

## Result

A maximal safe 12-stone set was found. Row-major indices `p = x + 12*y`:

```
5, 50, 56, 57, 61, 66, 68, 72, 77, 88, 98, 107
```

Coordinates `(x,y)`:

```
(5,0), (2,4), (8,4), (9,4), (1,5), (6,5), (8,5),
(0,6), (5,6), (4,7), (2,8), (11,8)
```

## Independent verification

Python verifier (`scratchpad/verify_new12.py`) checked:

- Safety: all `C(12,4) = 495` 4-subsets have nonzero circle/collinearity determinant → **0 forbidden quadruples**.
- Maximality: all 132 empty points are blocked (each has at least one triple of stones forming a forbidden quadruple with it; block-count distribution over empty points: 1:34, 2:32, 3:33, 4:16, 5:11, 6:4, 7:2; minimum 1, maximum 7).
- Therefore the set is safe and maximal. Density: 12/144 = 8.33%.

## Comparison with n = 11

- Minimum maximal sizes: `s_11 ≤ 10` (known 10-stone maximal on 11×11), `s_12 ≤ 11` (known 11-stone maximal on 12×12 by translating the 10-stone 11×11 set and adding one stone). The new 12-stone set shows a maximal of size 12 exists on 12×12, i.e. one above the `n−1` construction.
- Maximum (largest safe set) lower bounds: `K_11 ≥ 21`, `K_12 ≥ 22` (known 21/22-stone safe maximal constructions). The 12-stone set is far below these and does not improve them; it is a small maximal example.
- Density comparison of the small maximals: 10/121 = 8.26% (n=11) vs 12/144 = 8.33% (n=12), essentially comparable.
- The new 12-stone set is structurally different from the 11-stone `n−1` construction (which comes from translating the 10-stone 11×11 set); its 12 points are clustered in the middle/right of the board with no full-row/column pattern.

## Additional bounded probe (maximum direction)

A 60 s attempt to find a safe 23-stone set on 12×12 (target beating the known `K_12 ≥ 22`) using the same walker, with and without seeding from the known 22-stone set, did not produce a safe 23-stone set (`legal_count` never reached 0; no 23-stone safe set was constructed). This is negative evidence only and does not establish `K_12 ≤ 22`.

## Bounds (unchanged)

- `s_12`: still `≤ 11` for the minimum; existence of 12-stone maximals does not change `s_12`.
- `K_12`: still `≥ 22` (K0313). No new upper bound.
- New fact established: there exists at least one maximal safe set of size 12 on 12×12 (verified).

## Artifacts

- Witness verification: `scratchpad/verify_new12.py` (session scratchpad), result: 0 forbidden quads, 0 unblocked empty points.
- Search binary/output: `scratchpad/safe_search_12.exe`, run log (stdout captured during the 90 s run).
- Known constructions for comparison: `research/experiments/saturation/reports/saturation-20261003-extra.md` (21/22/24-stone sets).

## Reproduction

```sh
g++ -O3 -std=c++17 research/experiments/saturation/scripts/saturation_20261003_search.cpp \
  -o scratchpad/safe_search_12.exe
scratchpad/safe_search_12.exe 12 12 90 20261017
# expect a JSON line with legal_count 0 and witness_ids [5,50,56,57,61,66,68,72,77,88,98,107]
python scratchpad/verify_new12.py
```

## Limitations

- The 12-stone witness is an existence result from a heuristic search plus independent geometric verification; it is not a complete enumeration and implies nothing about `s_12` or `K_12`.
- The 23-stone probe is a bounded heuristic failure, not a proof.
- No claim is made that 12 is the minimum or maximum size; only that a verified maximal safe set of that size exists.
