# NEW13-r4: a maximal safe 13-stone set on 13×13

## Question

Does a maximal safe set of about 12–13 stones exist on the 13×13 board (standard rules: 4 concyclic or collinear points forbidden)? If so, is it independently verifiable?

## Method

- Reused the existing heuristic fixed-size safe-set walker `saturation_20261003_search.cpp` (random restarts, remove-and-replace moves, energy = number of legal additions), compiled with `g++ -O3 -std=c++17`.
- Target: `n=13, k=13`, run with a 90 s wall-clock bound (seed 20261017). A run with `legal_count == 0` at size 13 is a maximal safe 13-stone set.
- Candidate was then independently verified by exhaustive integer geometry in Python (4×4 determinant for circle/collinearity; no use of the search's internal masks).

## Parameters

- Board: 13×13, `V = 169`.
- Forbidden quads enumerated by search: 252,362.
- Search bound: 90.0 s wall clock (terminated early when `legal_count` reached 0).
- Actual wall clock: 0.1054 s.
- Steps: 23,519; restarts: 2.
- Best energy reached: 0 (maximal).

## Result

A maximal safe 13-stone set was found. Row-major indices `p = x + 13*y`:

```
25, 28, 35, 55, 84, 85, 90, 99, 107, 108, 119, 130, 140
```

Coordinates `(x,y)`:

```
(12,1), (2,2), (9,2), (3,4), (6,6), (7,6), (12,6),
(8,7), (3,8), (4,8), (2,9), (0,10), (10,10)
```

## Independent verification

Python verifier (`scratchpad/verify_new13.py`) checked:

- Safety: all `C(13,4) = 715` 4-subsets have nonzero circle/collinearity determinant → **0 forbidden quadruples**.
- Maximality: all 156 empty points are blocked (each has at least one triple of stones forming a forbidden quadruple with it; block-count distribution over empty points: 1:38, 2:51, 3:32, 4:23, 5:8, 6:3, 7:1; minimum 1, maximum 7).
- Therefore the set is safe and maximal. Density: 13/169 = 7.69%.

## Comparison with known 13×13 construction

- The saturation report lists a verified maximal safe set of 12 stones on 13×13 (indices `7, 29, 41, 48, 49, 54, 58, 63, 84, 131, 132, 163`).
- The present 13-stone set is one stone larger and is structurally different (it is not a superset of the 12-stone set; only index 84 is shared).
- This adds an existence result at size 13 but does not change the upper bound `s_13 ≤ 12` (minimum maximal size), which still comes from the known 12-stone construction.

## Bounds (unchanged)

- `s_13`: still `≤ 12` for the minimum. Existence of 13-stone maximals does not change `s_13`.
- `K_13`: no claim made; this is a small maximal example, not a large safe set.
- New fact established: there exists at least one maximal safe set of size 13 on 13×13 (verified).

## Artifacts

- Witness verification: `scratchpad/verify_new13.py`, result: 0 forbidden quads, 0 unblocked empty points.
- Search binary: `scratchpad/safe_search_13.exe` (compiled from `research/experiments/saturation/scripts/saturation_20261003_search.cpp`).
- Run output: JSON line with `legal_count: 0` and `witness_ids: [25,28,35,55,84,85,90,99,107,108,119,130,140]`.

## Reproduction

```sh
g++ -O3 -std=c++17 research/experiments/saturation/scripts/saturation_20261003_search.cpp \
  -o scratchpad/safe_search_13.exe
scratchpad/safe_search_13.exe 13 13 90 20261017
# expect a JSON line with legal_count 0 and witness_ids [25,28,35,55,84,85,90,99,107,108,119,130,140]
python scratchpad/verify_new13.py
```

## Limitations

- The 13-stone witness is an existence result from a heuristic search plus independent geometric verification; it is not a complete enumeration and implies nothing about `s_13` or `K_13`.
- The search terminated in 0.105 s, so this is a bounded (not exhaustive) heuristic success.
- No claim is made that 13 is the minimum or maximum size; only that a verified maximal safe set of that size exists.