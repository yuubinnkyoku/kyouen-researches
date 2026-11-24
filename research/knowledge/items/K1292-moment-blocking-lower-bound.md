---
id: K1292
title: モーメント多項式によるブロッキング下界 τ_1 ≥ 2q（q≥9）
kind: proposition
status: proved
topics: [geometry, maximum-safe, statistics]
aliases:
- moment proof of the blocking bound 2q
- tau_1(q) >= 2q for q>=9
- Bruen-Rothschild via moments
relations:
- type: related
  target: K1274
  note: 双対 K_q = q²+1−τ_1 を通じてスペクトル上界と結びつく
- type: related
  target: K1275
  note: q=4,5 の厳密値 K_q=(q−1)² は τ_1=2q を意味し、等号例を与える
- type: related
  target: K1291
  note: 同じモーメント多項式法のブロッキング版（乗数 (r−1)(r−3)(r−4)）
artifacts:
- path: research/experiments/inversive-moment-certificates-20261124/report.md
  role: proof
  note: 定理Cの証明、鋭さ（q=4..8でLPは2q−1）と文献比較
- path: research/experiments/inversive-moment-certificates-20261124/scripts/certificates.py
  role: verifier
  note: Q(r)≥0 と ΣQ(r)t_r=−2(q−8)(q−1) の厳密検査（112件）
- path: research/experiments/inversive-moment-certificates-20261124/independent/output/verification.json
  role: certificate
  note: 独立実装による定理C 192件の再検査（failures 0）
- path: research/experiments/inversive-blocking-equality-20261124/output/blocking_q4_n8.json
  role: certificate
  note: q=4 のサイズ8ブロッキング集合（SAT、2エンジン、独立検証済み）
- path: research/experiments/inversive-blocking-equality-20261124/output/blocking_q5_n10.json
  role: certificate
  note: q=5 のサイズ10ブロッキング集合（SAT、2エンジン、独立検証済み）
scope: Miquelian 反転平面 M(q) のブロッキング集合（全円と交わる点集合）の最小サイズ τ_1(q)。定理は q≥9。q=4,5 の等号（τ_1=2q）は SAT 計算で確認。
evidence: ブロッキング集合 X（m=|X|）は t_0=0。Q(r)=(r−1)(r−3)(r−4) は整数 r≥1 で非負で、{1,r,C(r,2),C(r,3)} 展開は (−12,12,−10,6)。3本のモーメント等式の Q による線形結合は m=2q−1 で ΣQ(r)t_r=−2(q−8)(q−1)<0（q≥9）。左辺は非負の和なので矛盾、τ_1≥2q。q=4..8 ではモーメントLPが m=2q−1 で実行可能なのでこの方法は届かない（Bruen–Rothschild の q≥9 の範囲と一致し、Kiss–Marcugini–Pambianco の q≥4 拡張はモーメント外）。厳密検査112件。独立実装（サブエージェント）も定理C 192件を再検査し PASS（verification.json）。
---

# モーメント多項式によるブロッキング下界 τ_1 ≥ 2q（q≥9）

## 定理

`M(q)` のブロッキング集合（すべての円と交わる点集合）の最小サイズを `τ_1(q)` とすると

```
τ_1(q) ≥ 2q      (q ≥ 9).
```

これは Bruen–Rothschild (1985) の下界を、**3 本のモーメント等式 + 3 次多項式**で
初等的に再証明する。双対 `K_q = q²+1−τ_1` より `K_q ≤ (q−1)²`。

## 証明

`X` をブロッキング集合、`m = |X|`、`t_r = #{C : |X∩C| = r}`（`0 ≤ r ≤ q+1`）。
ブロッキングなので `t_0 = 0`、`r ≥ 1`。モーメント等式:

```
Σ t_r = q(q²+1),   Σ r t_r = m q(q+1),
Σ C(r,2)t_r = C(m,2)(q+1),   Σ C(r,3)t_r = C(m,3).
```

`Q(r) = (r−1)(r−3)(r−4) = −12 + 12r − 10C(r,2) + 6C(r,3)` は
整数 `r ≥ 1` で非負（r=1,3,4 で 0、r=2 で 2、r≥5 で正）。
したがって

```
0 ≤ Σ Q(r)t_r = −12q(q²+1) + 12mq(q+1) − 10C(m,2)(q+1) + 6C(m,3).
```

`m = 2q−1` を代入すると右辺は `−2(q−8)(q−1)`。`q ≥ 9` でこれは負。
矛盾。よって `τ_1 ≥ 2q`。□

## 鋭さと限界

- モーメント線形計画の下限は q=4..8 で `2q−1`（`m=2q−1` が実行可能）。
  この方法では `2q` に届かない。BR の q≥9 と一致するのは偶然ではなく、
  `W` の因子 `(q−8)` がその境界を与える。
- q=4,5 では SAT がサイズ `2q` のブロッキング集合を発見し、
  `τ_1(4)=8`, `τ_1(5)=10` を独立に確認（K1275 の `K_q=(q−1)²` と整合）。
- q=7,8,9 の `2q` 集合の存在は未解決。SAT は今回は UNSAT を確定できなかった。
