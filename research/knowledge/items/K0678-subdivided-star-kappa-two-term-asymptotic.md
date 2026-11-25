---
id: K0678
title: 一辺細分星の奇数次数切替閾値 κ(r) の三項漸近則
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
  note: 両側対数評価・M の展開・閾値の位置・三項（および二項・先頭項）漸近の全称証明
- path: research/experiments/graph-star-subdivided-star-kappa-asymptotic-20261107/verify_kappa_asymptotic.py
  role: verifier
  note: κ(3000)=60057, κ(10000)=225393, κ(30000)=744937 の厳密証明、三項照合表、閾値の挟み込み、両側評価の数値監査
- path: research/experiments/graph-star-subdivided-star-kappa-asymptotic-20261107/output/kappa_asymptotic.json
  role: data
  note: r=4..30000 の残差表・三項照合表と監査結果
- path: research/experiments/graph-star-subdivided-star-no-contact-double-root-20261107/output/no_contact_double_root.json
  role: data
  note: r=2..1000 の厳密な κ(r) 表（本項の残差表の入力）
scope: 一辺細分星 G_k の終局長差多項式の奇数次数切替閾値 κ(r)、r>=2、q>=5。標準格子盤は対象外。
evidence: r→∞ の全称証明（両側評価・M の展開・Φ の漸近）。数値は r<=30000 の厳密 κ と三項公式の照合。
---

## 命題・範囲

K0677 の切替次数 `κ(r)`（一辺細分星 `G_k` の終局長差多項式 `T_{k,r}` が奇数 `k` で初めて実根をもつ最小の k）について

```
κ(r) = 2r ln r + r ln ln r + (1+ln 2) r + r (ln ln r + 1 + ln 2)/(2 ln r) + O(r (ln ln r)^2/(ln r)^2).
```

特に

```
κ(r) = 2r ln r + r ln ln r + (1+ln 2) r + o(r),      κ(r)/(r ln r) → 2.
```

K0677 の `Θ(r log r)` 評価を先頭3項と誤差の次数まで確定する。標準格子盤の勝敗・最大安全サイズへの主張ではない。

## 現在の根拠

1. `M(k) = max_{1<y<a} (a-y)y^k = a^{k+1}k^k/(k+1)^{k+1}`、`a = 1+1/(r+1)`、`y_* = ka/(k+1)`。K0677 より
   `M(k) > r - y_*` なら2実根、`M(k) < r - a` なら根なし。実際の切替点は `min_y F = 0` の境界で、
   最小点は `y_c = y_* + O(a^{-k})` だから `ln M(κ) = ln(r - y_*) + O(a^{-k})`。
2. 両側対数評価（`0<t<=1` の `t-t^2/2 < ln(1+t) < t` と `1-1/(2k) < k ln(1+1/k) < 1`）:
   `Ψ(k) = (k+1)/(r+1) - ln(k+1) - 1 - ln r` とおくと
   `ln M(k) = Ψ(k) + ln r + e1 + e2`、`e1 = (k+1)(ln a - 1/(r+1)) ∈ (-(k+1)/(2(r+1)^2), -(k+1)/(2(r+1)^2)+(k+1)/(3(r+1)^3))`、
   `e2 = 1 - k ln(1+1/k) ∈ (0, 1/(2k))`。
3. これから `Ψ(κ) = (κ+1)/(2(r+1)^2) + O(1/κ + 1/r) = (ln r + O(ln ln r))/r`。
4. `T = k/r = 2 ln r + ln ln r + μ`、`x = (ln ln r + μ)/(2 ln r)` とおくと
   `Ψ = μ - ln 2 - 1 - x + x^2/2 - (2 ln r + ln ln r + μ)/(r+1) + O(1/(r ln r))`。
   3. と等置して `μ = 1 + ln 2 + x + O(ln r/r + x^2)`、さらに
   `x = (ln ln r + 1 + ln 2)/(2 ln r) + O(ln ln r/(ln r)^2)`。
   よって `κ = r(2 ln r + ln ln r + μ) + O(1)` に代入して三項漸近を得る。
   二項漸近・先頭項 `κ ~ 2r ln r` はこの帰結。

## 検証と限界

- 厳密値: K0677 の `r=2..1000` の表（サンプル再計算一致）に加え、`κ(3000) = 60,057`、`κ(10000) = 225,393`、
  `κ(30000) = 744,937` を新規に厳密証明。
- 比 `κ/(r ln r)`: `5.23 (r=4)` → `2.565 (r=998)` → `2.500 (r=3000)` → `2.447 (r=10000)` → `2.409 (r=30000)`。
- 三項公式の照合: 誤差は `r=1000: +11.3`、`3000: -8.3`、`10000: -73.0`、`30000: -243.2` で、
  `O(r(\ln\ln r)^2/(\ln r)^2)` の 0.16 倍以内。残差の三項項に対する比は `1.043 (1000)`、`0.988 (3000)`、
  `0.966 (10000)`、`0.959 (30000)` で 1 に近づき、三項の係数と符号を支持する。
- `r = 3000, 10000, 30000` で `k = floor(2r ln r + r ln ln r + 1.2r)` が根なし、`floor(...+2.5r)` が2根であることを厳密証明。
- 限界: 誤差の定数は明示していない（数値では `r >= 1000` で 0.16 未満）。`κ` は離散関数なので残差率は単調でない。
  判定は `M` の両側十分条件のみを用い、狭間 `r-a < M < r-y_*` は使わない。
