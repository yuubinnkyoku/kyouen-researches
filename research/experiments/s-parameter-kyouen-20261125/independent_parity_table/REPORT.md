# Independent verification of K1358 — cross-`s` maximal-cap parity vs maximum Grundy

**Verifier:** independent sub-agent (separate implementation, Python 3.12.13,
standard library only)
**Date:** 2026-11-28
**Scope:** only `research/experiments/s-parameter-kyouen-20261125/independent_parity_table/`.
No commit was made; no file outside this directory was created or modified.
**Inputs:** the ten board files and the published data files listed in §2.1/§2.4
(read-only). The experiment solvers were not used; all game values below were
recomputed from the incidence data.

---

## 0. Verdict

**PASS — no numerical discrepancy.** Every one of the 14 rows of the K1358 table
is confirmed: the maximal sizes, the parity classification, and the maximum
Grundy value all match an independent recomputation. All maximal **counts** that
the sources publish are reproduced exactly, as are the complete Grundy
distributions, position totals, and root values.

**The general conclusion is correct.** Uniform parity of the maximal sizes is
equivalent to all Grundy values being in `{0,1}` (so the board maximum is 1 on a
non-degenerate board); mixed parity forces the board maximum to be at least 2.
This is the proved theorem K1298 (Lean formalisation K0305); §5 gives the short
proof and an exhaustive independent check over **all** non-empty downward-closed
families on at most 5 points (7,771 boards, 0 violations).

**Discrepancies found are provenance/documentation only, not table values.**
K1358's artifact note misattributes the `W_22`/`W_24` data to
`grundy_general.json` (that file contains no W board at all); `AG(2,7)` s=2 is
likewise absent from it; the PG(2,9) maximum (2) is not contained in the cited
`census_pg2q9.txt`; and the AG(2,9) maximal sizes are not contained in
`ag2q9_spectrum.json` (its `T` column is a cone census, not a terminal census).
Details in §7. These do not change any table entry.

---

## 1. The claim and the game

**Claim (K1358).** For the normal-play s-parameter Kyouen game on the listed
boards:

| board | s | maximal sizes | parity | max G |
|---|---:|---|---|---:|
| PG(2,9) | 2 | 6,7,8,10 | mixed | 2 |
| AG(2,5) | 2 | 5,6 | mixed | 2 |
| AG(2,7) | 2 | 6,7,8 | mixed | 2 |
| AG(2,9) | 2 | 6,7,8,9,10 | mixed | 3 |
| PG(2,3) | 3 | 7,9 | odd-uniform | 1 |
| PG(2,4) | 3 | 7,9 | odd-uniform | 1 |
| AG(2,4) | 3 | 8,9 | mixed | 2 |
| AG(2,5) | 3 | 9,10,11 | mixed | 4 |
| PG(2,5) | 3 | 9,10,11 | mixed | 4 |
| PG(2,4) | 4 | 12,13,14,16 | mixed | 3 |
| W_22 | 5 | 11,12,15 | mixed | 3 |
| W_24 | 5 | 6 | even-uniform | 1 |
| W_24 | 6 | 12 | even-uniform | 1 |
| W_24 | 7 | 12,13 | mixed | 2 |

with the conclusion: **uniform parity ⇒ maximum Grundy 1; mixed parity ⇒
maximum Grundy ≥ 2**.

**Game.** A board is a finite point set with a family of blocks. Fix `s`. A
position is a point set `S` with `|S ∩ B| ≤ s` for every block `B`; a move adds
one point while remaining a position; normal play (the player with no move
loses). `G(S) = mex{G(S+p) : p addable}`; the terminal positions are exactly the
maximal safe sets. The "maximal sizes" of the table are the sizes of these
terminal positions, and "max G" is the maximum of `G` over all positions.

---

## 2. Method and inputs

### 2.1 Board files (read-only inputs)

| board | file | n | b | block size | point degree | pairs / λ |
|---|---|---:|---:|---:|---:|---|
| PG(2,9) | `pg2q9-cap-game-20261125/output/board_pg2q9.txt` | 91 | 91 | 10 | 10 | 4,095, λ=1 |
| AG(2,9) | `ag2q9-cap-game-20261128/output/board_ag2q9.txt` | 81 | 90 | 9 | 10 | 3,240, λ=1 |
| AG(2,7) | `s-parameter-kyouen-20261125/output/board_ag2q7.txt` | 49 | 56 | 7 | 8 | 1,176, λ=1 |
| AG(2,5) | `s-parameter-kyouen-20261125/output/board_ag2q5.txt` | 25 | 30 | 5 | 6 | 300, λ=1 |
| AG(2,4) | `s-parameter-kyouen-20261125/output/board_ag2q4.txt` | 16 | 20 | 4 | 5 | 120, λ=1 |
| PG(2,3) | `projective-blocking-kyouen-20261125/output/board_pg2q3.txt` | 13 | 13 | 4 | 4 | 78, λ=1 |
| PG(2,4) | `projective-blocking-kyouen-20261125/output/board_pg2q4.txt` | 21 | 21 | 5 | 5 | 210, λ=1 |
| PG(2,5) | `projective-blocking-kyouen-20261125/output/board_pg2q5.txt` | 31 | 31 | 6 | 6 | 465, λ=1 |
| W_22 | `design-kyouen-witt-20261125/output/board_w22.txt` | 22 | 77 | 6 | 21 | 231, λ₂=5; 3-(22,6,1), λ₃=1 |
| W_24 | `design-kyouen-witt-20261125/output/board_w24.txt` | 24 | 759 | 8 | 253 | 276, λ₂=77; 5-(24,8,1), λ₅=1 |

Every pair of points lies on exactly one block for the eight plane boards, so the
incidence data are genuine projective/affine planes of the stated order. For
W_22/W_24 the t-design property was checked exhaustively (`λ₃ = 1` for t=3,
`λ₅ = 1` for t=5: 1,540 / 42,504 t-subsets, all distinct, zero duplicates).

### 2.2 Complete enumeration (no symmetry assumptions)

Safe sets are enumerated by DFS with incremental block counts, then evaluated by
a descending-size DP over all positions. This gives the exact count of positions,
maximal sets, and Grundy values. It was run on the whole board for:

* AG(2,5) s=2 — 16,426 positions;
* AG(2,4) s=3 — 26,073 positions;
* PG(2,3) s=3 — 4,330 positions;
* PG(2,4) s=3 — 180,058 positions;
* PG(2,4) s=4 — 1,234,016 positions;
* AG(2,5) s=3 — 1,365,826 positions;
* W_22 s=5 — 2,168,521 positions;
* W_24 s=5 — 168,799 positions;
* W_24 s=6 — 1,937,867 positions;
* AG(2,7) s=2 — 1,108,724 positions (43 s, dict DP).

An additional dense full enumeration of W_24 s=7 was started (§8.3) but did not
complete in the available CPU time; that row rests on the cone computation and
the published full-DP data, which agree exactly.

### 2.3 Cone + frame double counting (large boards)

For a board whose automorphism group acts transitively on t-subsets, let `F` be
a safe t-set, `N_t` the number of t-subsets, `T_m(g)` the number of cone
positions (safe sets containing `F`) of size `m` and Grundy `g`, and `T_max(m)`
the number of those that are maximal. Every m-set contains `C(m,t)` t-subsets,
and Grundy/maximality are automorphism-invariant, so

```
N_m(g) = N_t · T_m(g) / C(m,t),      N_max(m) = N_t · T_max(m) / C(m,t).
```

The cone is closed under moves, so the DP on it is exact. All divisions were
checked to be exact integers. This was used for PG(2,9) s=2, AG(2,9) s=2,
PG(2,5) s=3, and W_24 s=7:

| board | orbit(s) | N_t | cone size(s) | transitivity used |
|---|---|---:|---|---|
| PG(2,9) s=2 | triangles | 110,565 | 31,681 | PGL(3,9) transitive on triangles |
| AG(2,9) s=2 | triangles | 77,760 | 21,353 | AGL(2,9) transitive on triangles |
| PG(2,5) s=3 | triangles + collinear triples | 3,875 + 620 | 114,705 + 82,676 | PGL(3,5) on each orbit |
| W_24 s=7 | all 5-subsets | 42,504 | 65,503 | M₂₄ 5-transitive |

For PG(2,5) s=3 both 3-subset orbits are summed before dividing by `C(m,3)`.
The transitivity facts are elementary for PGL/AGL (a projectivity/affine map is
determined by the images of three non-collinear points; on a line PGL(2,q) is
3-transitive) and standard for the Mathieu group M₂₄. As an empirical control,
each cone was recomputed from 2–3 different representatives `F` and gave
**identical** `T_m`, `T_m(g)`, and `T_max` (all rows in
`out/cone_invariance.json`).

For **PG(2,9)** the cone `F={0,1,10}` reproduces the published 3-cap upset
exactly: 31,681 positions and layer sizes `1, 64, 1,344, 9,408, 16,320, 4,032,
448, 64` (`small_cap_grundy.json`). For **AG(2,9)** the cone `F={0,9,1}`
reproduces the published `T` and `T_g` of `ag2q9_spectrum.json` **exactly**
(including the 60 cone positions of Grundy 3 at size 5). For PG(2,3) and PG(2,4)
s=3 the two cones reproduce the published `T_g`/`U_g` exactly (PG(2,3): 260/214;
PG(2,4): 5,038/3,809).

### 2.4 Published sources used for comparison

* `s-parameter-kyouen-20261125/output/grundy_general.json` — AG(2,5) s=2,
  AG(2,4) s=3, AG(2,5) s=3, PG(2,4) s=4;
* `s-parameter-kyouen-20261125/output/stats_ag2q7_s2.txt` (identical to
  `pg2q7-cap-game-20261125/output/grundy_ag2q7_s2.txt`) — AG(2,7) s=2;
* `s-parameter-kyouen-20261125/output/grundy_pg2q5_s3.txt` — PG(2,5) s=3;
* `pg2q9-cap-game-20261125/output/census_pg2q9.txt` — PG(2,9) sizes/maximal;
* `ag2q9-cap-game-20261128/output/ag2q9_spectrum.json` — AG(2,9) N/N_g, T/T_g;
* `pg2q3-s3-20261128/output/pg2q3_s3_spectrum.json`,
  `pg2q4-s3-20261128/output/pg2q4_s3_spectrum.json` — PG(2,3)/PG(2,4) N/N_g,
  T/T_g, U/U_g; maximal counts from K1357;
* `design-kyouen-witt-20261125/output/grundy_w22_s5.txt`,
  `grundy_w24_s5.txt`, `grundy_w24_s6.txt`, `grundy_w24_s7.txt` — W boards;
* K1352 (knowledge item) for the complete PG(2,9) Grundy classification;
  K1357 for the PG(2,3)/PG(2,4) maximal counts. These two are not in K1358's
  artifact list but are the only published homes of those two facts.

---

## 3. Verified table

Recomputed maximal counts are in parentheses. "Full" = complete enumeration;
"cone" = cone + double counting. Every row also matches the claim exactly.

| # | board | s | maximal sizes (counts) | parity | max G | method | claim |
|---:|---|---:|---|---|---:|---|---|
| 1 | PG(2,9) | 2 | 6 (707,616), 7 (2,021,760), 8 (5,307,120), 10 (58,968) | mixed | 2 | cone | OK |
| 2 | AG(2,5) | 2 | 5 (600), 6 (1,000) | mixed | 2 | full | OK |
| 3 | AG(2,7) | 2 | 6 (271,656), 7 (2,352), 8 (6,174) | mixed | 2 | full + cone | OK |
| 4 | AG(2,9) | 2 | 6 (357,696), 7 (2,332,800), 8 (2,303,640), 9 (6,480), 10 (23,328) | mixed | 3 | cone | OK |
| 5 | PG(2,3) | 3 | 7 (234), 9 (13) | odd-uniform | 1 | full + cone | OK |
| 6 | PG(2,4) | 3 | 7 (360), 9 (11,480) | odd-uniform | 1 | full + cone | OK |
| 7 | AG(2,4) | 3 | 8 (120), 9 (1,120) | mixed | 2 | full | OK |
| 8 | AG(2,5) | 3 | 9 (12,500), 10 (28,000), 11 (9,000) | mixed | 4 | full | OK |
| 9 | PG(2,5) | 3 | 9 (93,000), 10 (248,000), 11 (65,100) | mixed | 4 | cone | OK |
| 10 | PG(2,4) | 4 | 12 (280), 13 (10,080), 14 (360), 16 (21) | mixed | 3 | full | OK |
| 11 | W_22 | 5 | 11 (1,344), 12 (22,176), 15 (352) | mixed | 3 | full + cone | OK |
| 12 | W_24 | 5 | 6 (113,344) | even-uniform | 1 | full + cone | OK |
| 13 | W_24 | 6 | 12 (2,576) | even-uniform | 1 | full + cone | OK |
| 14 | W_24 | 7 | 12 (1,020,096), 13 (30,912) | mixed | 2 | cone | OK |

**Recomputed Grundy distributions** (all exact; compared cell-by-cell with the
published data where the source gives them):

| # | board | s | G0 | G1 | G2 | G3 | G4 | total |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | PG(2,9) | 2 | 49,672,000 | 65,093,392 | 14,152,320 | 0 | 0 | 128,917,712 |
| 2 | AG(2,5) | 2 | 5,401 | 8,025 | 3,000 | 0 | 0 | 16,426 |
| 3 | AG(2,7) | 2 | 581,827 | 477,505 | 49,392 | 0 | 0 | 1,108,724 |
| 4 | AG(2,9) | 2 | 19,276,705 | 29,537,217 | 13,996,800 | 466,560 | 0 | 63,277,282 |
| 5 | PG(2,3) | 3 | 2,184 | 2,146 | 0 | 0 | 0 | 4,330 |
| 6 | PG(2,4) | 3 | 89,799 | 90,259 | 0 | 0 | 0 | 180,058 |
| 7 | AG(2,4) | 3 | 12,184 | 12,929 | 960 | 0 | 0 | 26,073 |
| 8 | AG(2,5) | 3 | 402,925 | 323,901 | 227,000 | 358,000 | 54,000 | 1,365,826 |
| 9 | PG(2,5) | 3 | 2,056,726 | 2,083,666 | 1,519,000 | 2,061,500 | 186,000 | 7,906,892 |
| 10 | PG(2,4) | 4 | 402,633 | 381,983 | 262,920 | 186,480 | 0 | 1,234,016 |
| 11 | W_22 | 5 | 784,412 | 949,829 | 332,640 | 101,640 | 0 | 2,168,521 |
| 12 | W_24 | 5 | 124,247 | 44,552 | 0 | 0 | 0 | 168,799 |
| 13 | W_24 | 6 | 955,651 | 982,216 | 0 | 0 | 0 | 1,937,867 |
| 14 | W_24 | 7 | 3,662,291 | 1,662,832 | 2,606,912 | 0 | 0 | 7,932,035 |

---

## 4. Row-by-row comparison with the sources

Each line lists the source value and my value; all are identical.

1. **PG(2,9) s=2.** Census maximal counts `6:707,616; 7:2,021,760;
   8:5,307,120; 10:58,968; 9:0` — reproduced exactly. Maximal sizes
   `{6,7,8,10}`, mixed. My full distribution
   `G0 49,672,000 / G1 65,093,392 / G2 14,152,320` equals the K1352
   classification (k=6 has G0 37,857,456 and G2 14,152,320; k=7 has
   G0 2,021,760 and G1 49,533,120; k=8,9,10 follow the parity law). Max G 2.
   The 3-cap cone (31,681 positions) and the published one agree layer-by-layer.
2. **AG(2,5) s=2.** `grundy_general.json AG2(5)_s2`: maximal `{5:600, 6:1000}`,
   Grundy `{0:5401, 1:8025, 2:3000}`, positions 16,426 — exact. Max G 2.
3. **AG(2,7) s=2.** `stats_ag2q7_s2.txt`: maximal `{6:271,656; 7:2,352;
   8:6,174}`, Grundy `{0:581,827; 1:477,505; 2:49,392}`, positions 1,108,724 —
   exact; independently reproduced by a full 1,108,724-position enumeration as
   well as by the 993-position triangle cone. Max G 2.
4. **AG(2,9) s=2.** Spectrum `N` per size and `N_g`
   `{G0 19,276,705; G1 29,537,217; G2 13,996,800; G3 466,560}`, positions
   63,277,282 — exact; the 21,353-position cone reproduces the published
   `T`/`T_g` cell-by-cell. Maximal sizes `{6,7,8,9,10}` with terminal counts
   `357,696 / 2,332,800 / 2,303,640 / 6,480 / 23,328` (computed here; the
   spectrum JSON has no maximal column). Max G 3.
5. **PG(2,3) s=3.** Spectrum `N_g` gives `G0 2,184 / G1 2,146`, 4,330
   positions — exact, per-size too. K1357 maximal `7:234, 9:13` — exact; full
   enumeration confirms; no maximal 8-cap (although there are 117 8-caps).
   Max G 1.
6. **PG(2,4) s=3.** `G0 89,799 / G1 90,259`, 180,058 positions — exact.
   K1357 maximal `7:360, 9:11,480` — exact; no maximal 8-cap (42,840 8-caps).
   Max G 1.
7. **AG(2,4) s=3.** `grundy_general.json AG2(4)_s3`: maximal `{8:120, 9:1120}`,
   Grundy `{0:12,184; 1:12,929; 2:960}`, 26,073 positions — exact. Max G 2.
8. **AG(2,5) s=3.** `grundy_general.json AG2(5)_s3`: maximal
   `{9:12,500; 10:28,000; 11:9,000}`, Grundy
   `{0:402,925; 1:323,901; 2:227,000; 3:358,000; 4:54,000}`, 1,365,826
   positions — exact. Max G 4.
9. **PG(2,5) s=3.** `grundy_pg2q5_s3.txt`: maximal `{9:93,000; 10:248,000;
   11:65,100}`, Grundy `{0:2,056,726; 1:2,083,666; 2:1,519,000;
   3:2,061,500; 4:186,000}`, positions 7,906,892 — exact. The maximal total
   406,100 also matches the earlier independent brute force
   `independent_pg25s3/brute_out.txt` (SAFE 7,906,892 / MAXIMAL 406,100).
   Max G 4.
10. **PG(2,4) s=4.** `grundy_general.json PG2(4)_s4`: maximal
    `{12:280; 13:10,080; 14:360; 16:21}`, Grundy `{0:402,633; 1:381,983;
    2:262,920; 3:186,480}`, 1,234,016 positions — exact. Max G 3.
11. **W_22 s=5.** `grundy_w22_s5.txt`: maximal `{11:1,344; 12:22,176;
    15:352}`, Grundy `{0:784,412; 1:949,829; 2:332,640; 3:101,640}`,
    2,168,521 positions — exact. Max G 3.
12. **W_24 s=5.** `grundy_w24_s5.txt`: maximal `{6:113,344}`, Grundy
    `{0:124,247; 1:44,552}`, 168,799 positions — exact. Max G 1.
13. **W_24 s=6.** `grundy_w24_s6.txt`: maximal `{12:2,576}`, Grundy
    `{0:955,651; 1:982,216}`, 1,937,867 positions — exact. Max G 1.
14. **W_24 s=7.** `grundy_w24_s7.txt`: maximal `{12:1,020,096; 13:30,912}`,
    Grundy `{0:3,662,291; 1:1,662,832; 2:2,606,912}`, 7,932,035 positions —
    exact. Max G 2.

Where a board was solved by both a full enumeration and a cone, the two methods
agree exactly (after adding the `mex`-chain layers of sizes below `t` that no
cone contains): PG(2,3), PG(2,4), AG(2,7), W_22, W_24 s=5, W_24 s=6.

---

## 5. Parity classification and the conclusion

### 5.1 The parity theorem

Let `M` be the set of maximal safe sets (terminal positions).

> **Theorem (K1298; Lean K0305).** (a) all Grundy values are in `{0,1}`;
> (b) all `M ∈ M` have the same size parity. Then (a) ⇔ (b). If (b) holds with
> common parity `p`, then `G(S) = (p − |S|) mod 2` for every safe `S`.

**Proof.** (b)⇒(a): every maximal extension of `S` is in `M`, hence has size
`≡ p`, so every complete play from `S` has length `≡ p − |S|`. Descending
induction: all children of `S` have the same Grundy value `1 − q`, where
`q = (p − |S|) mod 2`; `mex{1} = 0` and `mex{0} = 1`, so `G(S) = q`.
(a)⇒(b): if all values are 0/1, then `G(T)=0` forces all children to be 1 and
`G(T)=1` forces all children to be 0. Values alternate `0,1,0,1,…` along any
play, and terminal values are 0, so the parity of the distance from any `S` to a
terminal is `G(S)`; in particular all maximal extensions of `S` have one parity,
and for `S = ∅` this is (b). ∎

Consequently, on a board with at least one move, **uniform parity ⇒ max G = 1**
(all values are 0/1 and some value is 1), and **mixed parity ⇒ max G ≥ 2**
(otherwise (a), hence (b), would hold). For the degenerate board with no move
the only value is 0 and the maximum is 0; all 14 rows are non-degenerate. Also
note that "max G" is the maximum over *all* positions: a mixed board can have
`G(∅) ∈ {0,1}`; e.g. PG(2,9) has root 0, PG(2,3) has root 1.

### 5.2 Verification of the conclusion on the table

* Uniform rows: **PG(2,3) s=3** (7,9 odd), **PG(2,4) s=3** (7,9 odd),
  **W_24 s=5** (6 even), **W_24 s=6** (12 even). All four have Grundy values
  exactly `{0,1}` and maximum 1. In each case the full distribution satisfies
  the quantitative law: with common parity `p`, the number of G0 positions is
  exactly the number of positions of size `≡ p (mod 2)`, and similarly for G1.
  For example W_24 s=5: even sizes give `1 + 276 + 10,626 + 113,344 = 124,247
  = G0`, odd sizes give `24 + 2,024 + 42,504 = 44,552 = G1`.
* Mixed rows: the remaining 10 rows, with maxima `2, 2, 3, 2, 4, 4, 2, 3, 2`
  (rows 1,2,3,4,7,8,9,10,11,14), all `≥ 2`; in fact G=2 or G=3 or G=4 occurs.

### 5.3 Independent exhaustive test of the theorem

Independently of these boards, the theorem was checked on **all** non-empty
downward-closed families (simplicial complexes) on `n ≤ 5` points — this is the
general safe-set family of a Kyouen board. For every family the full Grundy
table was computed and (a)/(b), the formula `G(S) = (p−|S|) mod 2`, and
"mixed ⇒ max G ≥ 2" were tested:

| n | boards | uniform | mixed | violations |
|---:|---:|---:|---:|---:|
| 2 | 5 | 5 | 0 | 0 |
| 3 | 19 | 16 | 3 | 0 |
| 4 | 167 | 99 | 68 | 0 |
| 5 | 7,580 | 2,280 | 5,300 | 0 |
| **total** | **7,771** | **2,400** | **5,371** | **0** |

(Counts are the Dedekind numbers 6, 20, 168, 7,581 minus the empty family.) The
zero-violation result confirms both directions and the quantitative formula on
all boards of at most 5 points. This supplements, but does not replace, the
proof of K1298/K0305.

---

## 6. Internal arithmetic / consistency checks

All of the following were checked and hold:

* **Maximal counts ≤ size totals and ≤ G0 counts.** For every row, every
  positive maximal count is at most the number of positions of that size and at
  most the number of G0 positions of that size (terminal positions always have
  G=0). Globally, the sum of maximal counts is at most G0.
* **PG(2,9) s=2.** Maximal sizes are `{6,7,8,10}`, with **no maximal 9-cap**
  although 589,680 9-caps exist; all 58,968 10-caps are maximal. Total maximal
  caps `707,616 + 2,021,760 + 5,307,120 + 58,968 = 8,095,464`, matching the
  census/report.
* **AG(2,9) s=2.** Maximal sizes `6,7,8,9,10` are contiguous (6..10) and every
  one is attained. Terminal counts: `6:357,696; 7:2,332,800; 8:2,303,640;
  9:6,480; 10:23,328`. At sizes 9 and 10 the terminal counts equal the G0
  counts (6,480 and 23,328), so every G0 9-/10-cap is terminal. The 5 maximal
  sizes are exactly the claim's list; 11 is impossible because 10 is the
  largest cap.
* **W_24 s=5.** The unique maximal size 6 is even; the number of safe 6-sets is
  `C(24,6) − 759·C(8,6) = 134,596 − 21,252 = 113,344`, all maximal and all G0
  (the published SIZE line has total = maximal = G0 = 113,344).
* **W_24 s=6.** The unique maximal size 12 is even; all 2,576 safe 12-sets are
  maximal and G0 (total = maximal = G0 = 2,576).
* **W_24 s=7.** Maximal size 12: 1,020,096 of 1,393,616 12-caps; maximal size
  13: all 30,912; mixed.
* **Totals.** Every row's `ΣG` equals the published SAFE count (and the sum of
  its size totals): row 1: 128,917,712; row 2: 16,426; row 3: 1,108,724; row 4:
  63,277,282; row 5: 4,330; row 6: 180,058; row 7: 26,073; row 8: 1,365,826;
  row 9: 7,906,892; row 10: 1,234,016; row 11: 2,168,521; row 12: 168,799;
  row 13: 1,937,867; row 14: 7,932,035.
* **Root values.** `G(∅) = 0` for rows 1,2,3,4,7,8,10,12,13,14 and `G(∅) = 1`
  for rows 5,6,9,11; all match the sources' ROOT / size-0 rows.
* **Cone arithmetic.** All `N_t·T_m(g)/C(m,t)` divisions were exact (no
  remainder), and all cone totals add up to the published board totals.

---

## 7. Discrepancies found (documentation/provenance only)

**No numerical discrepancy in any of the 14 rows.** The following are source
attribution/completeness defects in K1358 (and in the task's DATA SOURCES
summary), which do not affect the table:

* **D1 — `grundy_general.json` does not contain W_22 or W_24.** K1358's artifact
  note says it contains "W_22 s=5、W_24 s=5/6". The file has 11 games:
  AG(2,2), AG(2,3), AG(2,4), AG(2,5) (s=2, plus s=3 for q=4,5) and
  PG(2,2), PG(2,3), PG(2,4), PG(2,5) s=2, plus PG(2,4) s=4. The W data are in
  `design-kyouen-witt-20261125/output/grundy_w22_s5.txt`,
  `grundy_w24_s5.txt`, `grundy_w24_s6.txt` (W_22 is also duplicated as
  `s-parameter-kyouen-20261125/output/stats_w22_s5.txt`, with identical
  numbers). Fix: correct the artifact note/path.
* **D2 — `grundy_general.json` does not contain AG(2,7).** The file has
  AG(2,2), AG(2,3), AG(2,4), AG(2,5) only. The AG(2,7) s=2 data are
  `s-parameter-kyouen-20261125/output/stats_ag2q7_s2.txt` (identical to
  `pg2q7-cap-game-20261125/output/grundy_ag2q7_s2.txt`). Fix: cite that file.
* **D3 — PG(2,9) `max G = 2` is not in `census_pg2q9.txt`.** The census has
  only sizes and maximal counts; it establishes mixed parity (hence `≥2` by the
  theorem) but no upper bound on G. The value 2 comes from the complete
  classification K1352 (and from the cone computation here, which reproduces
  K1352's `G0/G1/G2` counts). Fix: cite K1352 for the `max G` column.
* **D4 — AG(2,9) maximal sizes are not in `ag2q9_spectrum.json`.** The `T`
  column there is the number of cone caps containing the fixed 3-cap, not a
  terminal count: `T(3)=1` while the 3-cap has G=1, and `T(5)=1071` includes
  both G=1 and G=3 positions. The terminal counts were computed here:
  `6:92; 7:1050; 8:1659; 9:7; 10:36` in the cone, giving the global maximal
  counts in §3. Fix: state that maximality is a separate cone computation (or
  record it in the JSON).
* **D5 — PG(2,3)/PG(2,4) s=3 maximal sizes are not in their spectrum JSONs.**
  Those JSONs contain N/N_g and T_g/U_g but no maximality column. The maximal
  counts in the table (7:234/9:13 and 7:360/9:11,480) are from K1357; the full
  enumeration here confirms them.
* **D6 (wording).** "Uniform parity ⇒ max G 1" is a statement about the
  *maximum over all positions* and needs a non-degenerate board (at least one
  legal move); otherwise the maximum is 0. Likewise, mixed parity gives
  `max G ≥ 2` somewhere, not at the root/at every position. All 14 rows are
  non-degenerate, so the table's "1" values are correct.

The table's **values** are all correct as printed. The earlier K1358 evidence
sentence also mentions PG(2,2)–PG(2,8) and AG(2,8) as uniform-parity examples;
those boards are outside the 14-row table and were not checked here.

---

## 8. What is proved, and limitations

### 8.1 Established by this verification

1. **Every table entry** (maximal sizes, parity class, maximum Grundy) is
   correct, and every published maximal count / Grundy distribution / position
   total is reproduced exactly.
2. **The general implication** is correct as a theorem (K1298/K0305): uniform
   parity ⇔ all Grundy values in `{0,1}`; the common parity `p` gives the exact
   formula `G(S) = (p−|S|) mod 2`; mixed parity is equivalent to the existence
   of a position with G ≥ 2. This was additionally verified exhaustively on all
   7,771 non-empty downward-closed families on ≤ 5 points.

### 8.2 Nature of the evidence per row

* Rows 2, 3, 5, 6, 7, 8, 10, 11, 12, 13: **complete enumeration**, no symmetry
  assumptions.
* Rows 1, 4, 9, 14: **cone + frame double counting**. This is exact given the
  stated orbit-transitivity facts (elementary for PGL/AGL; standard for M₂₄).
  The computations are validated by (i) integer divisibility, (ii) exact
  reproduction of the published full-board totals/maximal counts, (iii) exact
  reproduction of the published cone tables where they exist, and (iv)
  invariance of the cone distribution across 2–3 different representatives.
* Row 14 (W_24 s=7) uses cone + double counting. A dense full enumeration was
  attempted but did not finish (§8.3); the cone result matches the published
  full-DP distribution cell by cell, and 7,932,035 = SAFE.

### 8.3 Full W_24 s=7 enumeration (not completed)

A dense DP was written (`full_dense.py`: mark all safe sets in a `2^24`
bytearray, then descend the integer masks; because adding a point increases the
mask, every child is evaluated before its parent). The enumeration of the 7.93M
safe sets is expensive because every candidate-point test scans the 253 blocks
through that point. Under CPU contention the run had not completed when the
verification window closed and was stopped. Consequently row 14 is established
by the cone computation (validated against the published full-DP data), not by
this second full enumeration. `out/full_dense_W24_s7.json` was therefore not
produced; the partial run had only printed the board validation.

### 8.4 Not established here

* The wider claims of K1358's evidence about other boards (PG(2,2)–PG(2,8),
  AG(2,8), etc.) — outside the 14-row table.
* A machine-checked proof of the theorem: K1298 is a paper proof and K0305
  records a Lean formalisation of the general game-theory core; this report
  re-derives the proof and checks it exhaustively on ≤5 points, but does not
  run Lean.
* Completeness of the PG(2,9) maximal-7 census was not re-enumerated (128.9M
  caps); the census value is used as the published source, while the cone
  computation independently reproduces it via double counting.

---

## 9. Files and reproduction

All files are in this directory; outputs in `out/`.

| file | purpose |
|---|---|
| `kyouen_lib.py` | board loading/validation, safe-set DFS, Grundy DP, cone DP, double counting |
| `sources.py` | parsers for all published data files; K1352/K1357 constants |
| `run_small.py` | complete enumeration of the n ≤ 25 boards |
| `run_cones.py` | cone + double counting for the large boards |
| `full_ag27.py` | complete AG(2,7) s=2 enumeration (49 points, dict DP) |
| `full_dense.py` | dense full-DP fallback (W_24 s=7); started but not completed (see §8.3) |
| `compare.py` | row-by-row comparison, `out/comparison.json` |
| `theorem_check.py` | exhaustive small-board test of the parity theorem |
| `cone_invariance.py` | cone-seed invariance check |
| `smoke_ag25s2.py` | initial smoke test |

Reproduce:

```sh
python run_small.py
python run_cones.py
python full_ag27.py
python compare.py
python theorem_check.py
python cone_invariance.py
# optional; did not complete in this session (see §8.3):
# python full_dense.py 7
```

Key output files: `out/comparison.json` (per-row checks, all true),
`out/theorem_small_boards.json` (0 violations), `out/cone_invariance.json`
(all equal), `out/full_*.json` and `out/cone_*.json` (raw computations).

---

**Bottom line.** K1358's table is numerically correct in all 14 rows, and its
parity/Grundy conclusion is a correct theorem. The only needed changes are
documentation: fix the artifact attributions (D1–D2), cite K1352 for the
PG(2,9) maximum (D3), and state explicitly that the AG(2,9) maximal sizes and
the PG(2,3)/PG(2,4) maximal counts are separate computations (D4–D5). No
correction to any size, count, parity label, or maximum Grundy value is needed.
