# Independent verification of claim K1324 — PG(2,8) cap orbits under PGL(3,8)

Independent re-computation, written from scratch in this directory on 2026-11-26.
Nothing outside `research/experiments/pg2q8-cap-game-20261125/independent_orbits/`
was created or modified; no git commit was made.

Board under test: `../output/board_pg2q8.txt`
sha256 `E3FDAD754BDF4D42DE7BBFA076768F18A6FC141D48F42435CCF7EABFC93F6ADB`
(read-only; the file was not touched).

Environment: Windows 10, Python 3.12.13 (standard library only), gcc 15.2.0 (MSYS2)
for the cap census.

## 0. Verdict

| Task | Claim under test | Verdict |
|---|---|---|
| 1 | both start sets are caps and maximal | **PASS** |
| 2 | own PGL(3,8) from GF(8); generators act by collineations | **PASS** |
| 3 | hyperoval orbit = 32,704, all 10-caps, single orbit, stabilizer 504 | **PASS** |
| 4 | maximal 6-cap orbit = 686,784; exactly 3 orbits of 686,784 (stab. 24) | **PASS** |
| 5 | \|PGL(3,8)\| = 16,482,816 and orbit·stabilizer = \|PGL\| | **PASS** |

56/56 automated checks pass (`logs/verify_orbits.log`, `results_orbits.json`),
plus 34 self-tests of the field/geometry/group-order machinery (`logs/selftest.log`)
and the independent C cap census (`logs/census_c.log`).

One discrepancy was found, but it is in a *supporting artefact of the parent
experiment*, not in the claim: see §8.

## 1. Artefacts and commands

```
cd research/experiments/pg2q8-cap-game-20261125/independent_orbits

gcc -O2 -o census_pg2q8_independent.exe census_pg2q8_independent.c
./census_pg2q8_independent.exe ../output/board_pg2q8.txt   > logs/census_c.log
python -u selftest.py                                      > logs/selftest.log   (tee'd)
python -u verify_orbits.py                                 > logs/verify_orbits.log (tee'd)
python -u check_probe_masks.py                             > logs/probe_masks.log  (tee'd)
```

| file | role |
|---|---|
| `pg8core.py` | GF(8), points/lines of PG(2,8), matrix generators, deterministic Schreier–Sims, 73-bit-mask orbit BFS, cap predicates |
| `selftest.py` | field axioms, geometry axioms, board/construction equality, group-order validation |
| `verify_orbits.py` | tasks 1–5, writes `results_orbits.json` |
| `census_pg2q8_independent.c` | independent full cap census (all caps by size, maximal caps by size) |
| `check_probe_masks.py` | decodes the parent's stored cap masks and classifies them (§8) |
| `logs/*.log` | raw run logs |

Runtimes: census 0.7 s; selftest ≈ 15 s; `verify_orbits.py` 108.6 s.

## 2. Board and geometry (task 0, prerequisites)

* header `73 73`; 73 lines, 9 points each; every one of the 2628 point pairs lies
  on exactly one line; two distinct lines meet in ≤ 1 point.
* PG(2,8) was rebuilt from the field alone: points = canonical nonzero vectors of
  GF(8)³ (first nonzero coordinate 1) sorted lexicographically, lines = 2-dim
  subspaces. The resulting **line set is identical** to the board's line set
  (not merely isomorphic), so the board's index model
  (`index = rank among sorted canonical vectors`) is confirmed, not assumed.

## 3. Task 1 — start sets

| set | cap | maximal | addable points | pair-lines cover |
|---|---|---|---|---|
| hyperoval `{0,5,13,18,27,38,46,53,59,66}` | yes | yes | none | 73/73 points |
| 6-cap `{10,47,49,55,61,64}` | yes | yes | none | 73/73 points |

All C(10,3) = 120 and C(6,3) = 20 triples checked individually: no three collinear.
Maximality: the union of the lines spanned by all pairs of the cap covers all 73
points, so no point can be added.

## 4. Task 2 — PGL(3,8) built from GF(8)

Generators (my own choice, as permutations of the 73 points, each induced by a
matrix with non-zero determinant):

* all 12 transvections `E_ij(1)`, `E_ij(w)` with `w = x` a primitive element, i ≠ j;
* `diag(w,1,1)` (order 7);
* the coordinate swap (0 1) (order 2).

Checks:

* GF(8) = GF(2)[x]/(x³+x+1): commutativity, associativity, distributivity,
  inverses for all elements, x primitive of order 7, x³ = x+1, and x³+x+1 has no
  root in GF(2) (hence irreducible, degree 3) — 0 violations.
* each generator is a bijection of the 73 points;
* **every** generator maps **every** line onto a line: 14 × 73 = 1022 line images,
  all members of the board line set. So the induced permutations are
  collineations (no generator is a "fake" collineation).
* group order by a deterministic Schreier–Sims implementation:
  base `(1,0,9,2,10)`, orbit sizes `(73,72,64,7,7)`,
  `|⟨generators⟩| = 16,482,816`, chain verification 0 failures.
* `|PGL(3,8)| = 511·504·448/7 = 115,379,712/7 = 16,482,816` (count of bases of
  GF(8)³ divided by the scalars) — equal to the computed order, and
  `73·72·64·49 = 16,482,816`. Since every generator is projective-linear,
  `⟨generators⟩ ⊆ PGL(3,8)`, and equality of orders gives
  **⟨generators⟩ = PGL(3,8)**.
* sanity of the action: transitive on points (73), on ordered pairs (5256),
  and on ordered frames/non-collinear triples (336,384 = 73·72·64).

The Schreier–Sims implementation was validated against brute-force group
closures: 120 random permutation groups on 5–8 points (order ≤ 40320), plus
C5, C7×C11, S7 (5040), A5 (60), PGL(2,8) on PG(1,8) (504) and its Borel
subgroup (56 = q(q−1)). All orders matched; 0 mismatches (`logs/selftest.log`).
The transvection-only subgroup also yields 16,482,816 = |SL(3,8)| = |PSL(3,8)|,
as it must for q = 8 because gcd(3, q−1) = gcd(3,7) = 1.

## 5. Task 3 — orbit of the hyperoval

BFS over 73-bit masks under the 14 generators:

* orbit size **32,704** (expected 32,704);
* every member has exactly 10 points (histogram `{10: 32704}`);
* every member was re-checked to be a cap **and** maximal (0 failures);
* my independent census gives exactly **32,704** caps of size 10 (all maximal),
  so the orbit is the entire set of 10-caps ⇒ **the hyperovals form exactly one
  orbit**, of size 32,704;  32,704 = 8⁵ − 8² also matches the classical number of
  conics in PG(2,8) (each conic plus its nucleus in characteristic 2);
* stabilizer order = 16,482,816 / 32,704 = **504** (division exact, remainder 0);
  `32,704 · 504 = 16,482,816`. Note 504 = |PGL(2,8)| = 8·(8²−1).
* maximality of every orbit member does not rest on sampling: for each of the 14
  generators, `addable(g(S)) = g(addable(S))`, so the empty addable set (hence
  maximality) is transported along the whole orbit; checked directly.

An independent frozenset-based BFS (no bitmask code) gives the same size, and
`permute_mask` was verified against explicit set images on 2000 random masks
(0 mismatches).

## 6. Task 4 — orbit of the maximal 6-cap and the other orbits

* Orbit of `{10,47,49,55,61,64}`: size **686,784** (expected 686,784); every
  member has exactly 6 points; a random sample of 500 members was checked to be
  caps and maximal (0 failures). As above, `addable(g(S)) = g(addable(S))` holds
  for all 14 generators, so *every* orbit member is maximal (not just the sample).
* 12 further maximal 6-caps, sampled uniformly (uniform random 6-subsets,
  rejected unless cap and maximal), all verified cap + maximal:
  `{14,22,27,32,69,71}`, `{9,42,50,51,57,60}`, `{7,10,41,43,59,61}`,
  `{0,12,20,40,47,65}`, `{7,9,37,40,50,58}`, `{3,8,11,14,57,64}`,
  `{10,15,22,28,41,66}`, `{0,1,18,31,33,43}`, `{3,7,15,32,42,57}`,
  `{20,26,44,48,65,70}`, `{10,28,44,57,65,66}`, `{2,7,19,59,66,72}`.
  Membership in the start orbit: **7 in, 5 out**.
* Orbits of two of the "out" caps were computed: each has size **686,784**.
  Three orbits (reps `{10,47,49,55,61,64}`, `{7,10,41,43,59,61}`,
  `{0,1,18,31,33,43}`) are **pairwise disjoint**, and their union has
  **2,060,352** elements.
* My independent C census counts exactly **2,060,352** maximal 6-caps
  (all sizes below), and since the union of three orbits already has that size,
  the union is *all* maximal 6-caps ⇒ **exactly 3 orbits of 686,784 each**;
  stabilizer 16,482,816 / 686,784 = **24** (exact).
* The 6-cap orbit masks are disjoint from the hyperoval orbit masks (different
  cardinality, so this is automatic; the substantive point is that a maximal
  6-cap cannot be extended to a hyperoval at all, which follows from maximality).

Independent census (my own C program, all caps enumerated by DFS, maximality
computed as "cap ∪ pair-lines = all 73 points"):

| size | caps | maximal |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 73 | 0 |
| 2 | 2,628 | 0 |
| 3 | 56,064 | 0 |
| 4 | 686,784 | 0 |
| 5 | 4,120,704 | 0 |
| 6 | 8,928,192 | **2,060,352** |
| 7 | 3,924,480 | 0 |
| 8 | 1,471,680 | 0 |
| 9 | 327,040 | 0 |
| 10 | 32,704 | **32,704** |
| total | 19,550,350 | 2,093,056 |

No maximal cap of size 3,4,5,7,8,9 exists; every 10-cap is maximal. These
totals coincide with the parent experiment's census, from an independent
implementation.  Arithmetic consistency of the census with the orbit data:

* 2,060,352 = 63 · 32,704 and 686,784 = 21 · 32,704;
* the parent's inclusion identity for 6-caps is reproduced:
  `8,928,192 = 2,060,352 + 32,704 · C(10,6) = 2,060,352 + 6,867,840`;
* 32,704 = 8⁵ − 8² (number of conics of PG(2,8), = number of hyperovals in even
  characteristic).

## 7. Task 5 — group and stabilizer arithmetic

| check | value |
|---|---|
| \|PGL(3,8)\| = 511·504·448/7 | 16,482,816 |
| \|GL(3,8)\| = 511·504·448 = 7·\|PGL\| | 115,379,712 |
| 73·72·64·49 | 16,482,816 |
| hyperoval orbit · stabilizer | 32,704 · 504 = 16,482,816 (remainder 0) |
| 6-cap orbit · stabilizer | 686,784 · 24 = 16,482,816 (remainder 0) |
| Schreier–Sims order of my generators | 16,482,816 |
| 504 = 8·(8²−1) = \|PGL(2,8)\| | yes |
| 24 = \|S4\| | yes |

## 8. Discrepancy (supporting artefact, not the claim)

`../output/starts6.txt`, `../output/probes6.txt`, `../output/starts.txt` store caps
as `"<tag> <high-word> <low-64-bit mask>"` — points 64…72 live in the high word
(bit 0 ↔ point 64). Decoding that way reproduces **exactly** the two start caps
given in the claim (high word 1 → point 64; high word 4 → point 66), and turns all
four 6-cap probes into maximal 6-caps (probe 1 only becomes maximal with point 70,
which is precisely high-word 64 = 2⁶).

The four probes therefore are

```
cap0 = {8,48,50,51,58,61}      cap1 = {17,27,30,44,52,70}
cap2 = {15,22,27,43,53,55}     cap3 = {4,8,40,44,47,56}
```

and their orbit membership (my computation, two independent BFS implementations):

```
cap0 -> orbit C    cap1 -> orbit B    cap2 -> orbit C    cap3 -> orbit B
```

but `../output/orbits_maximal.txt` records

```
probes vs orbit of {10,47,49,55,61,64}: cap0 in, cap1 out, cap2 in, cap3 out
```

i.e. the recorded reference orbit behaves like orbit C, not like the orbit of
`{10,47,49,55,61,64}` (orbit A). The in/out *pattern* is reproduced exactly
(relative to C: in, out, in, out), so the partition statement of the claim is
unaffected; the likely cause is a mislabelled reference orbit or stale verdict
line in that artefact. The claim's own numbers (3 orbits × 686,784; 2,060,352
total; 24) are confirmed here independently.

## 9. What is proved, and what is inferred

**Proved** (finite computations, on machinery that is itself validated):

1. the board is exactly the PG(2,8) built from GF(8) (identical line sets);
2. both start sets are caps and maximal;
3. my 14 generators are collineations and generate a permutation group of order
   16,482,816 = |PGL(3,8)|, hence generate all of PGL(3,8);
4. the orbit of the hyperoval has 32,704 elements, all 10-caps, all maximal;
5. the orbit of the given maximal 6-cap has 686,784 elements; two further
   maximal-6-cap orbits of the same size exist; three such orbits are pairwise
   disjoint and their union is all maximal 6-caps (union size equals my own
   census count 2,060,352);
6. orbit–stabilizer: stabilizer orders are exactly 504 and 24, with
   orbit · stabilizer = 16,482,816 in both cases.

**Inferred / not independently established here:**

1. the *isomorphism types* of the stabilizers (only orders 504 and 24 are
   verified; 504 = |PGL(2,8)| and 24 = |S4| is suggestive, not proved);
2. the geometric meaning/typing of the three 6-cap orbits — the natural
   blocking-count invariant (36/24/7 outside points blocked by 1/2/3 pairs) is
   *identical* for all maximal 6-caps and therefore does not separate them;
3. the parent experiment's other results (AG(2,8), Grundy/parity theorem, conic
   layer) — out of scope;
4. the correctness of the census relies on my C DFS being right; its agreement
   with the parent's independently written census (19,550,350 caps, 2,060,352
   maximal 6-caps, 32,704 10-caps) is corroboration, not proof.

## 10. Reproducing

```
cd research/experiments/pg2q8-cap-game-20261125/independent_orbits
gcc -O2 -o census_pg2q8_independent.exe census_pg2q8_independent.c
./census_pg2q8_independent.exe ../output/board_pg2q8.txt
python -u selftest.py
python -u verify_orbits.py
python -u check_probe_masks.py
```

Expected: `ALL SELFTESTS PASSED`; `56 checks, 0 failed` and `TASK 0..5 -> PASS`;
census table as in §6; probe table as in §8.

---

### 日本語要約

K1324 の主張（hyperoval は 32,704 の単一軌道・固定群 504、極大 6-キャップは
2,060,352 = 3×686,784 の 3 軌道・固定群 24）は、GF(8) からの独自構成・独自生成元
（12 個の transvection + diag + 座標置換）・決定論的 Schreier–Sims・73 bit マスク BFS
により **全項目 PASS**。|PGL(3,8)| = 16,482,816 も二経路（511·504·448/7 と
Schreier–Sims の計算）で一致。独自 C 国勢調査も全キャップ数 19,550,350、
極大 6-キャップ 2,060,352、10-キャップ 32,704 を再現。軌道の分割は
「3 軌道の非交和 = 国勢調査の全極大 6-キャップ数」で証明される。
唯一の不一致は親実験の補助データ `output/orbits_maximal.txt` の probe 判定行で、
参照軌道のラベルが実際には別軌道（C）を指している（主張自体には影響なし）。
