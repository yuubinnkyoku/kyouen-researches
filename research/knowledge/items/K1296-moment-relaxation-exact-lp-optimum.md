---
id: K1296
title: "3-モーメント緩和の厳密 LP 最適値（反転平面 s-弧）— s=4 は 2q+1 が方法最適、q≥19・s≥8 に第3乗数"
kind: computation
status: computed
topics: [geometry, maximum-safe, statistics]
aliases:
- exact LP optimum of the s-arc moment relaxation
- K1291 theorem A is LP-optimal
- third multiplier s-arc
relations:
- type: supports
  target: K1291
  note: 定理A（s=4 の 2q+1）が 3-モーメント緩和の LP 最適値と一致することを q=4..25 で確認。定理B は q≥11 で LP 最適でない
- type: related
  target: K1295
  note: 第2乗数族 P2 が多くの格子点で LP 最適値を達成する。q≥19・s≥8 の3例外では第3乗数が上回る
- type: depends_on
  target: K1058
  note: 反転平面 3-(q²+1,q+1,1) 設計のモーメント等式 (M1)–(M4) が LP の制約
artifacts:
- path: research/experiments/inversive-k4q9-exact-20261124/scripts/moment_lp.py
  role: verifier
  note: 制約系の実行可能性を有理数で厳密判定（階数4なので Carathéodory により4列列挙で十分）
- path: research/experiments/inversive-k4q9-exact-20261124/scripts/moment_certificate.py
  role: verifier
  note: 各格子点の明示的乗数を Fraction で抽出し再検査
- path: research/experiments/inversive-k4q9-exact-20261124/output/moment_lp_s4.json
  role: data
  note: s=4, q=4,5,7,8,9,11,13,16 の LP 最適値（2q+1、q=4 は 10、q=5 は 12）
- path: research/experiments/inversive-k4q9-exact-20261124/output/moment_lp_general.json
  role: data
  note: s=3,5,6,7,8 と q=9,11,13,16 の LP 最適値（s=3 は q+3）
- path: research/experiments/inversive-k4q9-exact-20261124/output/moment_p2_large.json
  role: data
  note: q=17,19,25 で min(P1,P2) と LP 最適値の比較（3例外を明示）
- path: research/experiments/inversive-k4q9-exact-20261124/report.md
  role: proof
  note: 表3（LP 最適値と min(P1,P2) の比較）と読み方
scope: Miquelian 反転平面 M(q)。緩和 {t_r ≥ 0 かつ (M1)–(M4)} の実行可能最大 n を LP 最適値とする。格子は q ∈ {4,5,7,8,9,11,13,16,17,19,25}、s ∈ {3,4,5,6,7,8,9}（s ≤ q+1）。非 Miquelian 盤・一般の Steiner 3-設計は対象外。
evidence: 制約行列 A（行が (M1)–(M4)、列が r=0..s の (1,r,C(r,2),C(r,3))）は階数4なので、b(n,q) が列錐に入るかは4列部分集合の列挙で厳密に判定できる（Carathéodory）。各4列について Fraction の 4×4 消去で解き、解が非負かつ Aλ=b を厳密に再現するかで実行可能性を決める。結果として s=4 では q≥7 で LP 最適値がちょうど 2q+1（q=7,8,9,11,13,16,17,19,25）、すなわち K1291 定理A の乗数 P_4 が最適で、これ以上の改善はこの方法では不可能。s=3 は q+3（K1291 の注記と一致）。s=5..9 の大半で LP 最適値 = min(P1 上界, P2 上界)（K1295）。例外は (q,s)=(19,9) で LP 122 < 123、(25,8) で 135 < 137、(25,9) で 157 < 161 となり、第3の乗数が上回る。s=4 で LP 最適値が 2q+1 を超えるのは q=4 (10) と q=5 (12) のみ。すべて整数・Fraction で計算し浮動小数を使っていない。
---

# 3-モーメント緩和の厳密 LP 最適値

## 計算した量

`s`-弧 `S`（`|S| = n`）の円交点数 `t_r`（`r = 0..s`）は

```
(M1) Σ t_r = q(q²+1),      (M2) Σ r t_r = n q(q+1),
(M3) Σ C(r,2) t_r = C(n,2)(q+1),   (M4) Σ C(r,3) t_r = C(n,3),   t_r ≥ 0
```

を満たす。この緩和が `n` で実行可能かどうかを **有理数で厳密に** 判定し、
実行可能な最大 `n` を「3-モーメント法の最適上界」とした。
制約行列は階数 4 なので、`b(n,q)` が列錐に入るかは 4 列部分集合の全列挙で
決まる（Carathéodory）。各 4 列は `Fraction` の消去で解き、非負性と
`Aλ = b` の厳密再現を確認する。

## 結果

| 対象 | LP 最適値 | 備考 |
|---|---|---|
| `s=4`, `q=7,8,9,11,13,16,17,19,25` | `2q+1` | K1291 定理A が方法最適 |
| `s=4`, `q=4 / q=5` | `10 / 12` | 定理A の適用範囲（q≥6）外 |
| `s=3`, `q=9,11,13,16` | `q+3` | K1291 の注記と一致 |
| `s=5..9`, 大半の格子点 | `= min(P1 上界, P2 上界)` | K1295 の第2乗数族が達成 |
| `(19,9)` | `122` | `min(P1,P2)=123`、第3乗数が強い |
| `(25,8)` | `135` | `min(P1,P2)=137` |
| `(25,9)` | `157` | `min(P1,P2)=161` |

## 読み方

- **`s=4` は打ち止め**: `K_4(q) ≤ 2q+1` はこの方法の限界に到達している。
  `K_4(7)=13`, `K_4(8)=14` との差（15, 17）は整数性・幾何を使わないと詰まらない。
- **`s≥5` はまだ余地**: `q ≥ 11` で `(s−2)q` が LP 最適でなく、
  `P2`（K1295）が改善する。さらに `q ≥ 19`, `s ≥ 8` では第 3 の乗数が要る。
- `q = 9` は `P1` が LP 最適（K1291 の数値検算と整合）。

## 限界

- 有限格子（`q ≤ 25`, `s ≤ 9`）の計算であり、一般 `(s,q)` の LP 最適値の
  公式は未証明。`min(P1,P2)` が常に LP 最適とは限らない（上の 3 例外）。
- 第 3 乗数の族・その閉形式は未同定。`(25,9)` の `157` を与える乗数は
  本実験では抽出していない（LP 実行可能性の判定のみ）。
- 「LP 最適」は 3-モーメント緩和の中での話で、真の `K_s(q)` の上界としては
  さらに弱い（例: `K_4(8)=14 < 17`）。
