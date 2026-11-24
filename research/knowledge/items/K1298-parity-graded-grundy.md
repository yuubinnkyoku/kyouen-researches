---
id: K1298
title: parity-graded 共演ゲーム — 極大安全集合の偶奇が一様なら Grundy は {0,1}
kind: proposition
status: proved
topics: [grundy, geometry, strategy-length]
aliases:
- parity-graded Grundy lemma
- all maximal safe sets same parity implies Grundy in {0,1}
relations:
- type: related
  target: K1253
  note: 反転平面盤では極大サイズのパリティが混ざり Grundy 2 以上が現れる対照を与える
- type: related
  target: K1293
  note: 設計ボードの graded 性（全極大が同一サイズ）は本補題の特別な場合
- type: depends_on
  target: K1058
  note: 共演ゲーム（通常プレイ、打てない方が負け）の定義
artifacts:
- path: research/experiments/projective-blocking-kyouen-20261125/report.md
  role: proof
  note: 補題の定式化・帰納証明・適用例（PG(2,q) q≤4、設計ボード、反転平面）
- path: research/experiments/projective-blocking-kyouen-20261125/output/grundy_pg2q3.txt
  role: data
  note: PG(2,3) の完全 Grundy（極大サイズ 7,9 がともに奇数、Grundy は 0/1 のみ）
- path: research/experiments/design-kyouen-witt-20261125/output/summary.json
  role: data
  note: 設計ボード 7 枚の graded 性（全極大が同一サイズ）と Grundy ∈{0,1} のデータ
scope: 有限ハイパーグラフ盤（点集合 + ブロック族）上の共演ゲーム。局面は各ブロックと高々3点で交わる点集合、手は1点追加、通常プレイ（打てない方が負け）。極大安全集合のサイズの偶奇が盤全体で一様である場合。
evidence: 証明は極大局面からの降順帰納。極大 S では Grundy(S)=0=(p−|S|) mod 2。非極大 S では全ての子が同じパリティ p の極大集合を含むため帰納法より全ての子の Grundy が同じ値 (p−|S|−1) mod 2 になり、mex が (p−|S|) mod 2 になる。応用は (i) K1293 の 7 設計は全極大が同一サイズ K なので定理の特別な場合で、Grundy 分布が (K−|S|) mod 2 に一致。(ii) PG(2,2), PG(2,3), PG(2,4) は全極大サイズが奇数（7; 7,9; 7,9）で、完全 Grundy が実際に {0,1} のみ・空盤 1。(iii) 反転平面 M(q) は s(q)<K(q) で q=5 では 5 と 6 が混在するため仮定を満たさず、K1253 の完全 Grundy で Grundy 2 以上が観測されている。
---

# parity-graded 共演ゲーム

## 定理

有限な盤（点集合 `V` とブロック族）上の共演ゲームを考える:
局面は各ブロックと高々 3 点で交わる点集合 `S`、手は `S` に 1 点追加、
通常プレイ（打てない方が負け）。盤の**すべての極大安全集合**のサイズの偶奇が
一様で、共通の値を `p mod 2` とする。このとき任意の安全集合 `S` について

```
Grundy(S) = (p − |S|) mod 2 ∈ {0,1}.
```

とくに空盤は `p` が奇数なら先手勝ち（N 位置）、偶数なら後手勝ち（P 位置）。

## 証明

`|S|` に関する降順帰納。

- `S` が極大なら `Grundy(S) = 0`。仮定より `|S| ≡ p (mod 2)` なので
  `(p−|S|) mod 2 = 0`。
- `S` が非極大なら、任意の合法手 `S∪{x}` を取る。`S∪{x}` を含む極大集合は
  すべて `S` を含むのでサイズは `≡ p`。帰納法の仮定から
  子の Grundy はすべて `(p−(|S|+1)) mod 2 = 1 − (p−|S|) mod 2` に等しい。
  したがって `mex{1 − (p−|S|) mod 2} = (p−|S|) mod 2`。□

## 適用と対照

| 盤 | 極大サイズ | 仮定 | Grundy | 空盤 |
|---|---|---|---|---|
| 設計ボード 7 種（K1293） | すべて同一 `K` | 成り立つ | `(K−|S|) mod 2` のみ | `K mod 2` |
| PG(2,2) | 7 | 奇数一様 | `{0,1}`（実測） | 1 |
| PG(2,3) | 7, 9 | 奇数一様 | `{0,1}`（実測） | 1 |
| PG(2,4) | 7, 9 | 奇数一様 | `{0,1}`（実測） | 1 |
| M(q)（反転平面） | `s(q)`〜`K(q)` | q=5 で 5,6 混在 | 2 以上が出現（K1253） | 盤依存 |

## 注意

- 仮定は「盤全体で極大サイズの偶奇が一様」であり、サイズが一様である必要はない
  （PG(2,3), PG(2,4) は 7 と 9 の 2 種類）。
- 偶数パリティ一様の盤では空盤が P 位置になる。設計ボードのうち K が偶数の
  AG(3,2)（K=4）と AG(4,2)（K=6）が実例。
- 仮定を満たさない盤では Grundy 2 以上が起こり得る（M(q) q≥5 の完全 Grundy）。
