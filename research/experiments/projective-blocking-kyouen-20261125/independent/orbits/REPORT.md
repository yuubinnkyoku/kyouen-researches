# Independent verification — PGL orbits in PG(2,3) and PG(2,4)

- **Experiment:** `research/experiments/projective-blocking-kyouen-20261125`
- **Independent workspace:** `independent/orbits/`
- **Date:** 2026-11-25 (Asia/Tokyo); last run generated `2026-11-24T16:26:16+00:00`
- **Tooling:** Python 3.12.13, standard library only
- **Independence:** does not import the experiment's `scripts/` and does not read
  the existing `output/orbits.json`; only `output/board_pg2q3.txt` and
  `output/board_pg2q4.txt` are read (as inputs).
- **Overall verdict: PASS** (claims A, B, C)

## Verdict summary

| Claim | Statement (abridged) | Verdict |
|---|---|---|
| **A** | PG(2,3): the 234 six-point minimal blocking sets are exactly the vertex sets of complete quadrilaterals (4 three-point lines in general position), counted by `C(13,4) − 13·C(4,3)·9 − 13 = 234`, and form one PGL(3,3) orbit | **PASS** |
| **B** | PG(2,4): the 11,480 twelve-point complements of maximal 9-point safe sets split into exactly 3 PGL(3,4) orbits of sizes 10,080 / 1,120 / 280 with profiles `{2:10,3:6,4:3,5:2}` / `{2:9,3:9,5:3}` / `{2:12,4:9}` | **PASS** |
| **C** | The 1,120 orbit is exactly the set of unions of 3 lines in general position (triangles); `C(21,3) − 21·C(5,3) = 1,120` | **PASS** |

Group orders computed by full BFS over projective matrices:

- **|PGL(3,3)| = 5616** = |GL(3,3)| / 2 = (26·24·18) / 2
- **|PGL(3,4)| = 60480** = |GL(3,4)| / 3 = (63·60·48) / 3

Both equal the expected orders, so the orbit computations are full PGL orbits,
not orbits of a proper subgroup.

All per-check results (19 checks for A, 14 for B, 14 for C) are stored in
`results_A.json`, `results_B.json`, `results_C.json`, and
`results_summary.json`. **No check failed.**

## Reproduction

From the repository root:

```powershell
python research/experiments/projective-blocking-kyouen-20261125/independent/orbits/verify_orbits.py
```

Runtime on this machine: **7.93 s**. The console transcript is `run_log.txt`;
JSON outputs are written next to the script.

## Method (independent implementation choices)

1. **Field arithmetic from scratch.**
   - `F_3`: integers mod 3.
   - `GF(4) = {0, 1, w, w+1}` with `w^2 = w + 1`, encoded as
     `a + b·w ↦ a | (b << 1)`; addition is XOR. Includes self-tests
     (`w·w = w+1`, `w·(w+1) = 1`, `(w+1)^2 = w`, inverses, distributivity).
2. **Own model of PG(2,q).** Points are the 1-dimensional subspaces of
   `F_q^3` with canonical representatives (first non-zero coordinate 1); lines
   are the kernels of the non-zero linear forms. This produces 13 points /
   13 lines for q=3 and 21 / 21 for q=4, each line of size q+1.
3. **Board certification.** Each board file is checked against the projective
   plane axioms (line sizes, unique line through two points, unique intersection
   of two lines, q+1 lines per point), and an explicit point bijection to the
   independent `F_q^3` construction is constructed (standard frame fixed;
   constraint propagation/backtracking for the remaining points). Every board
   line is verified to map onto a canonical line. Thus the boards are certified
   as PG(2,3) and PG(2,4) up to a relabelling of points.
4. **PGL(3,q) generation.** 13 generators are used: all elementary
   transvections `x_i ← x_i + a·x_j` (`i ≠ j`, `a ∈ {1, g}`) plus
   `diag(g,1,1)`, where `g` is a multiplicative generator (`g = 2 = w` for q=4).
   The generated projective matrix group is expanded by BFS: 5616 and 60480
   elements respectively. The induced point permutations are then used for
   orbit BFS.
5. **Enumeration.** Safe sets are enumerated by all combinations and filtered
   with bit masks (`≤ 3` points on every line). Maximality by inclusion is
   decided by the union of the lines carrying exactly 3 points. Set orbits are
   computed by BFS under the 13 certified generator permutations.
6. **Second, independent route for the complement families.** Minimal blocking
   sets were also enumerated *directly* (without safe-set enumeration or
   complementation): all 6-subsets for q=3 that are blocking and minimal, and
   all 12-subsets for q=4 that are minimal 2-fold blocking sets. Both counts and
   the resulting set families agree exactly with the complement families.

## Claim A — PG(2,3): complete-quadrilateral vertices

Board: 13 points, 13 lines, 4 points per line; axioms and isomorphism to the
`F_3^3` construction verified.

| Item | Result |
|---|---|
| Safe 7-sets (`≤3` per line) | 702 |
| Maximal safe 7-sets | **234** |
| Complements (6-point sets) | **234** (all distinct) |
| Directly enumerated 6-point minimal blocking sets | **234**, exactly the same family |
| Lines containing 3 points of a complement | histogram `{4: 234}` (every set has exactly 4) |
| Those 4 lines in general position (no 3 concurrent) | yes for all 234 |
| Six-set equals the 6 pairwise intersections of those 4 lines | yes for all 234 |
| 4-line subsets in general position | **234** |
| Distinct quadrilateral vertex sets | **234** |
| Complements equal the quadrilateral vertex sets | yes |
| Count formula `C(13,4) − 13·C(4,3)·9 − 13` | 715 − 468 − 13 = **234** |
| PGL(3,3) orbits | **1 orbit, size 234** |
| |PGL(3,3)| computed by BFS | **5616** |

Representative (board point labels): mask 187, points
`{0,1,3,4,5,7}`; the four 3-point lines are
`{0,1,2,3}`, `{0,4,5,6}`, `{1,4,7,10}`, `{3,5,7,12}`.

## Claim B — PG(2,4): three orbits of twelve-point complements

Board: 21 points, 21 lines, 5 points per line; axioms and isomorphism to the
`GF(4)^3` construction verified.

| Item | Result |
|---|---|
| Safe 9-sets (`≤3` per line) | **11,480** (every one is already maximal) |
| Maximal safe 9-sets | **11,480** |
| Complements (12-point sets) | **11,480** (all distinct) |
| Directly enumerated 12-point minimal 2-fold blocking sets | **11,480**, exactly the same family |
| Minimum line intersection of a complement | 2 |

The PGL(3,4) orbit decomposition (group order 60,480) is:

| Orbit size | Line-intersection profile of the 12-point set | Profile uniform in orbit | Stabilizer order (= 60480 / size) |
|---:|---|---:|---:|
| **10,080** | `{2:10, 3:6, 4:3, 5:2}` | yes | 6 |
| **1,120** | `{2:9, 3:9, 5:3}` | yes | 54 |
| **280** | `{2:12, 4:9}` | yes | 216 |

- Number of orbits: **exactly 3**.
- Multiplicities of the profiles over all 11,480 sets are exactly
  10,080 / 1,120 / 280 as claimed.
- Sum of orbit sizes: 10,080 + 1,120 + 280 = 11,480.
- One representative per orbit (as board point sets) is stored in
  `results_B.json`.

## Claim C — PG(2,4): the 1,120 orbit is the triangle orbit

| Item | Result |
|---|---|
| All line triples | `C(21,3) = 1330` |
| Concurrent triples (3 lines through one point) | `21·C(5,3) = 210` |
| General-position triples (triangles) | **1,120** |
| Distinct unions | **1,120** |
| Every union has 12 points (5+5+5−3) | yes |
| Triangle unions vs. the 1,120 PGL orbit | **exactly equal as sets** |
| Line-intersection profile of a union | `{2:9, 3:9, 5:3}` |
| Complements of the unions are maximal safe 9-sets | yes |
| Formula `C(21,3) − 21·C(5,3)` | 1330 − 210 = **1,120** |

The 1,120-orbit representative in `results_B.json` (mask 140287) is itself one
of the enumerated triangle unions (lines 0, 1, 5 of the board), confirming the
cross-identification explicitly.

## Discrepancies

**None.** Every quantity stated in claims A, B, C was reproduced exactly. No
numerical deviation, no extra or missing sets, no orbit splitting/merging was
observed.

## Caveats and scope

- This is an exhaustive finite computation on the two supplied board
  encodings; the boards themselves were certified isomorphic to the standard
  Desarguesian planes, but this report is not a symbolic proof for arbitrary
  models or all q.
- The words “complete quadrilateral” and “triangle” were tested through the
  stated incidence properties (4 respectively 3 lines, general position,
  vertex/union set), not assumed from terminology.
- The 280 orbit was verified by its size and line-intersection profile only; no
  further geometric identification of that orbit was attempted.
- Point labels of the board files are arbitrary; all reported counts, orbit
  sizes and incidence statements are invariant under relabelling.

## Files and integrity (SHA-256)

| File | Contents | SHA-256 |
|---|---|---|
| `verify_orbits.py` | self-contained verifier | `03A5326F3BCEBBF842BB75D51BA145040600B7EC6C7A9F404C94786DF6C3268D` |
| `results_A.json` | claim A checks and data | `39C6E855AAC3DBFED617EEA3051626287EC4DE6A95BCA89FE1D0F9401648922B` |
| `results_B.json` | claim B checks and data | `081E163D2E31487A242ED67358C5A0B826F8E25E7EAF195C74C09A73A2A156B3` |
| `results_C.json` | claim C checks and data | `01AF294F0BD5F6B64CE8ED6D6345520BCCD4A37989989BE34370CA56407605B1` |
| `results_summary.json` | boards, group orders, overall verdict | `82F8A6A91F8EA373EDF06D6AEB8F8BF0E114571B08E1161F2AFBE828D3FB98FD` |
| `run_log.txt` | console transcript of the final run | — |

No files outside `independent/orbits/` were modified and nothing was committed.
