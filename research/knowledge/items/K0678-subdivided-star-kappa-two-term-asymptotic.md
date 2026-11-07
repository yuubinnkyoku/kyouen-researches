---
id: K0678
title: 一辺細分星の奇数次数切替閾値は κ(r)=2r log r+r log log r+(1+log 2)r+o(r)
kind: proposition
status: proved
topics: [variants, statistics, geometry, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0677
  note: 単一切替定理、κ(r) の定義と Θ(r log r) 評価
- type: depends_on
  target: K0648
  note: 一辺細分星の終局長差多項式 T_{k,r} の定義
artifacts:
- path: research/experiments/graph-star-subdivided-star-kappa-asymptotic-20261107/proof.md
  role: proof
  note: 両側対数評価・Φ の漸近・二項漸近律の全称証明
- path: research/experiments/graph-star-subdivided-star-kappa-asymptotic-20261107/verify_kappa_asymptotic.py
  role: verifier
  note: κ(3000)=60057, κ(10000)=225393 の厳密証明、残差表、閾値の両側挟み込み、両側評価の数値監査
- path: research/experiments/graph-star-subdivided-star-kappa-asymptotic-20261107/output/kappa_asymptotic.json
  role: data
  note: r=4..10000 の残差表と監査結果
- path: research/experiments/graph-star-subdivided-star-no-contact-double-root-20261107/output/no_contact_double_root.json
  role: data
  note: r=2..1000 の厳密な κ(r) 表（本項の残差表の入力）
scope: 一辺細分星 G_k の終局長差多項式の奇数次数切替閾値 κ(r)、r>=2、q>=5。標準格子盤は対象外。
evidence: r→∞ の全称証明（両側評価と Φ の漸近）。数値は r<=10^4 の厳密 κ と残差の整合。
---

## 命題・範囲

K0677 の切替次数 `κ(r)`（一辺細分星 `G_k` の終局長差多項式 `T_{k,r}` が奇数 `k` で初めて実根をもつ最小の k）について

```
κ(r) = 2 r ln r + r ln ln r + (1 + ln 2) r + o(r)      (r → ∞),
```

特に `κ(r)/(r ln r) → 2`。K0677 の `Θ(r log r)` 評価を先頭2項と定数まで確定する。標準格子盤の勝敗・最大安全サイズへの主張ではない。

## 現在の根拠

1. `M(k) = max_{1<y<a} (a-y)y^k = a^{k+1}k^k/(k+1)^{k+1}`、`a = 1+1/(r+1)`。K0677 より
   `M(k) > r - y_*` なら2実根、`M(k) < r - a` なら根なし（`y_* = ka/(k+1)`）。
2. 両側対数評価（`0<t<=1` の `t-t^2/2 < ln(1+t) < t` と `1-1/(2k) < k ln(1+1/k) < 1` から）:

   ```
   (k+1)/(r+1) - (k+1)/(2(r+1)^2) - ln(k+1) - 1 < ln M(k) < (k+1)/(r+1) - ln(k+1) - 1 + 1/(2k).
   ```

3. `Φ(k) = (k+1)/(r+1) - ln(k+1) - 1 - ln r` とおくと、`k = 2r ln r + r ln ln r + c r + O(1)` で `Φ(k) = c - (1+ln 2) + o(1)`。
4. したがって任意の `c > 1+ln 2` で `κ(r) <= 2r ln r + r ln ln r + cr`、任意の `c < 1+ln 2` で
   `κ(r) >= 2r ln r + r ln ln r + cr`（十分大きい r）。両側から定理が従う。

## 検証と限界

- 厳密値: K0677 の `r=2..1000` の表（サンプル再計算一致）に加え、`κ(3000) = 60,057`、`κ(10000) = 225,393` を新規に厳密証明。
- 比 `κ/(r ln r)`: `5.23 (r=4)` → `2.565 (r=997)` → `2.500 (r=3000)` → `2.447 (r=10000)` と 2 へ近づく。
- 残差率 `δ(r)/r`（`δ = κ - (2r ln r + r ln ln r + (1+ln2)r)`）: `2.458 (4)`、`1.681 (9)`、`1.003 (24)`、`0.519 (100)`、
  `0.274 (1000)`、`0.233 (3000)`、`0.205 (10000)`。補題の補正 `ln(1+(\ln\ln r+O(1))/(2\ln r))` の予測 `0.202 (r=10^4)` と整合。
- `r = 3000, 10000` で `k = floor(2r ln r + r ln ln r + 1.2r)` が根なし、`floor(... + 2.5r)` が2根であることを厳密証明。
- 限界: `o(r)` 項の明示評価は未証明。`κ` は離散関数なので残差率は単調でない（局所的な揺れがある）。
  本項の判定条件は `M` の両側十分条件のみを用い、狭間 `r-a < M < r-y_*` は使わない。
