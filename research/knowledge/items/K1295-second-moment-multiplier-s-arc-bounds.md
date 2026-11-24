---
id: K1295
title: "第2乗数族による s-弧上界の改善 — K_s(q) ≤ min((s−2)q, n₂(s,q)) と漸近定数 s−2−d*(s)"
kind: proposition
status: proved
topics: [geometry, maximum-safe, variants]
aliases:
- second multiplier s-arc bound
- P2_s multiplier for s-arcs
- asymptotic s-arc bound s-2-2/3
relations:
- type: extends
  target: K1291
  note: 同じ3本のモーメント等式のまま乗数を P2_s=−(r−(s−4))(r−(s−3))(r−s) に替え、(s−2)q を q≥11・s≥6 で厳密に改善する
- type: depends_on
  target: K1058
  note: 反転平面の 3-(q²+1,q+1,1) 設計パラメータ（各点対は q+1 円、各点は q(q+1) 円）から (M1)–(M4) を得る
- type: related
  target: K1274
  note: 設計上界 (s−2)(q+1)+2 と双対 τ_d ≥ d(q+1) の枠を、同じ設計パラメータのまま締める
- type: related
  target: K1275
  note: 既知の厳密値（K_4(7)=13, K_4(8)=14 等）と矛盾しない。s=4 は本手法では改善しない
artifacts:
- path: research/experiments/inversive-k4q9-exact-20261124/report.md
  role: proof
  note: 定理1・系1の証明、改善表（表2）、手法の限界（表3）、検証と限界の本文
- path: research/experiments/inversive-k4q9-exact-20261124/scripts/moment_p2_bound.py
  role: verifier
  note: P2 の非負性、Y_{P2}(n₂+1)<0、K1291 の (s−2)q の再現、実盤面での恒等式照合を厳密整数で検査
- path: research/experiments/inversive-k4q9-exact-20261124/scripts/moment_certificate.py
  role: verifier
  note: 各 (s,q) の明示的乗数を Fraction で抽出し P≥0 と Y=−1 を独立再検査
- path: research/experiments/inversive-k4q9-exact-20261124/output/moment_p2.json
  role: data
  note: q=9,11,13,16・s=4..8 の上界表（P1/P2/LP 最適値）
- path: research/experiments/inversive-k4q9-exact-20261124/output/moment_p2_large.json
  role: data
  note: q=17,19,25・s=4..9 の上界表（第3乗数が強い3例外を含む）
- path: research/experiments/inversive-k4q9-exact-20261124/output/moment_certificates.json
  role: certificate
  note: 乗数証明書（全件 certificate_ok）
- path: research/experiments/inversive-k4q9-exact-20261124/output/identity_checks.json
  role: data
  note: 実 s-弧 8 例で Σ_r P1(r)t_r=Y_{P1} と Σ_r P2(r)t_r=Y_{P2} が一致
scope: Miquelian 反転平面 M(q)（q 素数冪）。K_s(q) は各円と高々 s 点で交わる点集合の最大サイズ。定理1は 5 ≤ s ≤ q−1, q ≥ 9。系1は q→∞ の漸近形。2 ≤ s ≤ 4、q < 9、s = q 行、非 Miquelian 盤は対象外。
evidence: s-弧 S（|S|=n）の円交点数 t_r は t_r=0 (r>s), t_r≥0 と 4 本のモーメント等式 (M1) Σt_r=q(q²+1), (M2) Σr t_r=nq(q+1), (M3) ΣC(r,2)t_r=C(n,2)(q+1), (M4) ΣC(r,3)t_r=C(n,3) を満たす。補題として P2_s(r)=−(r−(s−4))(r−(s−3))(r−s) が整数 0..s で非負（根が連続整数 s−4,s−3 と s）であることを示し、モーメント基底で (a0,a1,a2,a3)=(s(s−3)(s−4), −(3s²−17s+20), 6s−20, −6) と展開する。よって Y_{P2}(n,q)=a0 q(q²+1)+a1 n q(q+1)+a2 C(n,2)(q+1)+a3 C(n,3)=Σ_r P2(r)t_r ≥ 0 が必要で、n の 3 次式（最高次係数 −1）なので Y<0 となる n 以上は排除される。各 (s,q) で Y_{P2}(n₂+1,q)<0 を厳密整数で確認（s=6,q=16 では Y(59)=1122, Y(60)=−168）。系1は n=cq, q→∞ で Y/q³→f(c)=−c³+(3s−10)c²−(3s²−17s+20)c+s(s−3)(s−4) となり、c=s−2−d で f=(8−2s)+(3s−8)d−4d²+d³。h(d)=d³−4d²+(3s−8)d−(2s−8) は h(0)=8−2s<0, h(1)=s−3>0, h'(d)≥3s−13>0 (0≤d≤1, s≥5) なので (0,1) に唯一の根 d*(s) があり、c≥c*(s)=s−2−d*(s) で f<0。実盤面での照合は貪欲 s-弧 8 例（q=9,11,13,16; s=3..9）で ΣP t_r=Y_P が厳密一致。改善例は K_6(13)≤49（旧52）, K_7(16)≤74（旧80）, K_8(19)≤105（旧114）, K_9(25)≤161（旧175）。q=9 は P1 と一致し改善しない。d*(5..9)≈0.35,0.43,0.49,0.54,0.59 で d*→2/3。
---

# 第2乗数族による s-弧上界の改善

## 命題

`M(q)` を位数 `q` の Miquelian 反転平面、`K_s(q)` を「各円と高々 `s` 点で交わる
集合」の最大サイズとする。`5 ≤ s ≤ q−1`, `q ≥ 9` で

```
K_s(q) ≤ min( (s−2)q ,  n₂(s,q) ),
n₂(s,q) = max{ n : Y_{P2}(n,q) ≥ 0 },
P2_s(r) = −(r−(s−4))(r−(s−3))(r−s)
        = s(s−3)(s−4) − (3s²−17s+20) r + (6s−20) C(r,2) − 6 C(r,3),
Y_{P2}(n,q) = s(s−3)(s−4) q(q²+1) − (3s²−17s+20) n q(q+1)
              + (6s−20) C(n,2)(q+1) − 6 C(n,3).
```

第 1 項 `(s−2)q` は K1291 の定理 B。第 2 項は `q ≥ 11`, `s ≥ 6` で
厳密に小さい（下表）。

## 証明

`s`-弧 `S`（`|S| = n`）の円交点数 `t_r` は `t_r = 0 (r > s)`, `t_r ≥ 0` で
4 本のモーメント等式を満たす（K1274 / K1291）。任意の乗数

```
P(r) = a0 + a1 r + a2 C(r,2) + a3 C(r,3)
```

に対し `Σ_r P(r) t_r = Y_P(n,q)`（右辺は上と同じ形）なので、
整数 `0..s` で `P(r) ≥ 0` なら `Y_P(n,q) ≥ 0` が必要。

`P2_s` は `r ≤ s−5` で 3 因子すべて負、`r = s−4, s−3, s` で零、
`r = s−2, s−1` では 2 因子正 1 因子負で積が負なので、符号反転した `P2_s` は
`0 ≤ r ≤ s` で非負（`s−4` と `s−3` が連続整数なので間の整数は無い）。
`Y_{P2}` は `n` の 3 次式で最高次係数 `−1`（`a3 C(n,3) = −n³+3n²−2n`）なので、
`Y_{P2}(n₂+1,q) < 0` かつ以後単調減少であることを確かめれば、
`n ≥ n₂+1` はすべて排除される。□

## 系（漸近）

`n = cq`, `q → ∞` で `Y_{P2}(cq,q)/q³ → f(c)`、`f(s−2−d) = (8−2s) + (3s−8)d − 4d² + d³`。
`h(d) = d³ − 4d² + (3s−8)d − (2s−8)` は `(0,1)` に唯一の根 `d*(s)` をもち
（`h(0) < 0 < h(1)`, `h' > 0`）、`c ≥ c*(s) = s−2−d*(s)` で `f(c) < 0`。よって

```
limsup_{q→∞} K_s(q)/q ≤ s − 2 − d*(s),    d*(s) → 2/3.
```

`d*(5..9) ≈ 0.35, 0.43, 0.49, 0.54, 0.59`。

## 改善表（K1291 の `(s−2)q` との差）

| q | s | 旧 | 新 | 差 |
|---:|---:|---:|---:|---:|
| 11 | 6 | 44 | 43 | 1 |
| 13 | 6 | 52 | 49 | 3 |
| 13 | 8 | 78 | 73 | 5 |
| 16 | 6 | 64 | 59 | 5 |
| 16 | 8 | 96 | 89 | 7 |
| 17 | 9 | 119 | 111 | 8 |
| 19 | 8 | 114 | 105 | 9 |
| 19 | 9 | 133 | 123 | 10 |
| 25 | 7 | 125 | 113 | 12 |
| 25 | 8 | 150 | 137 | 13 |
| 25 | 9 | 175 | 161 | 14 |

`q = 9` は改善しない（`P2` の上界が `(s−2)q` 以上になる）。

## 限界

- `n₂(s,q)` は閉形式ではない（各 `(s,q)` の整数計算）。漸近系は `cq` の主項のみで
  `O(1)` の下端を与えない。
- `s = 4` は改善しない。K1291 の `2q+1` が 3-モーメント法の LP 最適値であり
  （K1296）、差 `K_4(7)=13 vs 15`, `K_4(8)=14 vs 17` は整数性・幾何の入力が必要。
- `q ≥ 19`, `s ≥ 8` では `min(P1,P2)` より LP 最適値が小さい（K1296 の 3 例外）。
  第 3 乗数の族は未同定。
- 非 Miquelian 盤（K1254）は `λ₂` が異なるため別計算。`s = q` 行は対象外。
