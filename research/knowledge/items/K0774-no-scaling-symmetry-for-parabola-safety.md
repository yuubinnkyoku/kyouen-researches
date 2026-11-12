---
id: K0774
title: パラメータの単元倍 t↦at は剰余放物線の安全性を保たない（p=2207の1104点証人で反例）
kind: proposition
status: computed
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線・共円四点を含まない安全集合の定義（整数平面の点として判定する）
- type: depends_on
  target: K0334
  note: 四点のパラメータ和0 mod pは整数共円性の必要条件にすぎないという限定
- type: depends_on
  target: K0097
  note: 完全対{t,p−t}の数え上げが使う反射t↦p−tの正当化との対比
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/check_scaling_invariance.py
  role: verifier
  note: 証人を単元倍し、辺リストとの包含と独立なgeneric整数4x4行列式で共円性を再計算する
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/scaling_invariance.json
  role: data
  note: 原証人0辺・単元倍後1957辺（1957件すべて独立行列式で共円）の生出力
- path: research/experiments/parabola-p2207-1104-witness-20261110/output/candidate.txt
  role: certificate
  note: 監査済みのp=2207の1104点（形状(1,1,1)、完全対307、空対1078）
scope: p=2207 の一点集合とその307^-1倍のみ。一般の素数での反例の存在は主張しない。
---

## 主張

`Q_p = {(t, t² mod p)}` の部分集合の安全性（整数平面で共線・共円の四点を含まない）について、
パラメータの単元倍 `t ↦ a t`（`a ∈ (Z/p)^*`）は安全性を保たない。

## 根拠

- 反射 `t ↦ p−t` は整数平面の等長変換 `(x, y) ↦ (p−x, y)` から来るので、円も直線も保つ。
  完全対 `{t, p−t}` の数え上げ（K0097）はこの反射にだけ依存している。
- 一方 `t ↦ a t` は K0334 の mod p の四元和条件 `t1+t2+t3+t4 ≡ 0` を保つが、それは整数共円性の
  必要条件にすぎない。実際 `p=2207` の監査済み1104点証人（完全対307）を `a = 307^{-1} = 1560` 倍すると、
  形状は `(x,c,e) = (1,1,1)`、完全対 `{1}`、空対 `{54}` のまま変わらないのに、
  辺リスト（`forbidden_edges` の整数行列式つき列挙）の禁止四点を **1957個** 含むようになる。
- 1957個すべてを、辺生成器とは別実装の generic な整数4×4行列式
  （行 `(x²+y², x, y, 1)`）で再検査し、共円であることを確認した（1957/1957）。
  原証人は同じ検査で辺を0個しか含まない（安全）。

## 帰結

- 形状 `(c)`（`x=1, c=1, e=1`）の探索で「完全対を `{1, p−1}` に正規化する」対称性破りは**使えない**。
  全 `h` 通りの完全対を走査する必要がある。
- mod p の四元和だけで共円を判定してよいのは、必要条件として辺を絞る場面（K0334）に限る。

## 限界

- 単一素数 `p=2207` の明示的な反例であり、「他の素数では常に成り立つ」といった肯定的主張はしていない。
- この項目は探索手法の制約を与えるだけで、`A(p)` の値そのものは変えない。
