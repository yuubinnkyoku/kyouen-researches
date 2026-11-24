---
id: K1291
title: "3次モーメント多項式による s-弧上界 — K_4 ≤ 2q+1 と K_s ≤ (s−2)q（5≤s≤q−1, q≥9）"
kind: proposition
status: proved
topics: [geometry, maximum-safe, variants]
aliases:
- moment-polynomial s-arc bound
- K_4(q) <= 2q+1
- K_s(q) <= (s-2)q for 5<=s<=q-1
relations:
- type: extends
  target: K1274
  note: K1274 の設計上界 (s−2)(q+1)+2 を3次多項式乗数で改善し、加法的な s を消す
- type: related
  target: K1275
  note: 厳密値 K_4(4)=9, K_4(5)=10, K_4(7)=13, K_4(8)=14 と整合し、K_4(9) の上界を 22 から 19 に改善
- type: related
  target: K1058
  note: 反転平面の3-(q²+1,q+1,1)設計パラメータとモーメント等式の出典
artifacts:
- path: research/experiments/inversive-moment-certificates-20261124/report.md
  role: proof
  note: 定理A/Bの完全な証明、W>0 の範囲確認、比較表と帰結
- path: research/experiments/inversive-moment-certificates-20261124/scripts/certificates.py
  role: verifier
  note: 整数・Fraction の厳密算術で非負性・係数展開・Y<0 を検査
- path: research/experiments/inversive-moment-certificates-20261124/output/certificates.json
  role: data
  note: 検査件数（s=4..80、定理B 6,664件、定理A 115件）
scope: Miqueian 反転平面 M(q)（q 素数冪）。K_s は各円と高々 s 点で交わる集合の最大サイズ。定理Aは s=4, q≥6。定理Bは 5≤s≤q−1, q≥9。
evidence: 3-(q²+1,q+1,1) 設計の3本のモーメント等式 (M1)-(M4) と、多項式 P_s(r)=−(r−(s−3))(r−(s−2))(r−s)（整数 0≤r≤s で非負）を使う。P_s を {1,r,C(r,2),C(r,3)} で展開し n=(s−2)q+1 を代入すると ΣP_s(r)t_r = −qW(s,q), W=q(s−1)(s−4)−s(s−2)(s−3)−2。主張範囲で W>0（s=5..7 は q=9 で正、s≥8 は q=s+1 で s²−7s+2>0 かつ q について増加）。s=4 は P_4=−(r−1)(r−2)(r−4), n=2q+2 で ΣP_4 t_r = −4(q²−5q−2)<0（q≥6）。いずれも矛盾により上界。整数/Fraction の厳密検査で 6,664+115 件を確認（certificates.json）。
---

# 3次モーメント多項式による s-弧上界

## 定理

`M(q)` を位数 q の Miquelian 反転平面（3-(q²+1,q+1,1) 設計）とし、
`K_s(q)` を「各円と高々 s 点で交わる集合」の最大サイズとする。

1. **`K_4(q) ≤ 2q+1`（q ≥ 6）**
2. **`K_s(q) ≤ (s−2)q`（5 ≤ s ≤ q−1, q ≥ 9）**

これは K1274 の `K_s(q) ≤ (s−2)(q+1)+2 = (s−2)q + s` を改善する
（s=4 では 2q+4 → 2q+1、s≥5 では加法的な s を完全に消す）。

## 証明

`s`-弧 `S`（`n = |S|`）とし `t_r = #{C : |S∩C| = r}` とおく。3-設計のモーメント:

```
Σ t_r = q(q²+1),   Σ r t_r = n q(q+1),
Σ C(r,2)t_r = C(n,2)(q+1),   Σ C(r,3)t_r = C(n,3).
```

多項式 `P(r) = a0 + a1 r + a2 C(r,2) + a3 C(r,3)` に対し

```
Σ P(r)t_r = a0 q(q²+1) + a1 n q(q+1) + a2 C(n,2)(q+1) + a3 C(n,3) =: Y.
```

`P(r) ≥ 0`（すべての可能な r）なら `Y ≥ 0` が必須。

### s=4

`P_4(r) = −(r−1)(r−2)(r−4) = 8 − 8r + 8C(r,2) − 6C(r,3)`。
整数 `r=0..4` で `P_4 = (8,0,0,2,0) ≥ 0`。
`n = 2q+2` を代入すると `Y = −4(q²−5q−2) < 0`（q≥6）。矛盾。□

### 一般 s（5 ≤ s ≤ q−1）

`P_s(r) = −(r−(s−3))(r−(s−2))(r−s)` は整数 `r=0..s` で非負
（r≤s−3 で3因子すべて非正、r=s−1 で積負、r=s−3,s−2,s で0）。
係数は `(a0,a1,a2,a3) = (s(s−3)(s−2), −(s−3)(3s−4), 2(3s−8), −6)`。
`n = (s−2)q+1` で

```
Y = −q·W(s,q),  W(s,q) = q(s−1)(s−4) − s(s−2)(s−3) − 2.
```

`W>0`:
- `W` は q の一次関数で傾き `(s−1)(s−4) > 0`。
- s=5,6,7: q=9 で `W(5,9)=4`, `W(6,9)=16`, `W(7,9)=20`。
- s≥8: q=s+1 で `W = s²−7s+2 > 0`（s=8 で 10、以降増加）。

よって `Y < 0`、矛盾。□

## 帰結

- `K_4(9) ≤ 19`（旧上界 22、下界 16）、`K_4(7) ≤ 15`, `K_4(8) ≤ 17`。
- `K_5(9) ≤ 27`, `K_6(9) ≤ 36`, `K_7(9) ≤ 45`, `K_8(9) ≤ 54`。
- スペクトルの上包絡は `(s−2)q`（中域）、`K_q ≤ (q−1)²`（K1292）、
  `K_{q+1} = q²+1`。

## 限界

- モーメント緩和は緩い。実測 `K_4(7)=13`, `K_4(8)=14` に対し上界 15,17。
- `s=3` では同じ方法で `q+3` しか出ず、K1252 の `q` には届かない。
- `s=q` では `W<0` で証明不能（別のブロッキング上界が必要）。
- q<9 の一般 s は範囲外。
