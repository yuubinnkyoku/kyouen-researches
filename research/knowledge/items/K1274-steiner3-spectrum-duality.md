---
id: K1274
title: Steiner 3-設計の (s,d)-双対と反転平面の円インターセクション・スペクトル上界
kind: proposition
status: proved
topics: [geometry, maximum-safe, variants]
aliases:
- Steiner 3-design (s,d)-duality
- circle-intersection spectrum K_s(q)
- s-arc bound (s-2)(q+1)+2 for inversive planes
- d-fold blocking lower bound d(lambda_2)
relations:
- type: extends
  target: K1252
  note: s=3 が K1252 の K(q)≤q を含み、K1252 は d=q-2 での excess 3 として読める
- type: related
  target: K1250
  note: 弧＝楕円二次曲面上の一般位置集合という同定と並ぶ、交点数による一般化
- type: related
  target: K1251
  note: 弧の厳密値・下界データを s 方向へ拡張する枠組みを与える
artifacts:
- path: research/experiments/inversive-spectrum-20261124/report.md
  role: proof
  note: 定理2.1（一般形）・系2.2（反転平面）・双対・excess の定義と証明
- path: research/experiments/inversive-spectrum-20261124/scripts/bound_audit.py
  role: verifier
  note: 点ごとの不等式・モーメント等式・定理上界との整合の機械監査
- path: research/experiments/inversive-spectrum-20261124/output/summary.md
  role: data
  note: 厳密値と定理上界・双対量の表
scope: Steiner 3-(v,k,1) 設計（各点対が λ_2=(v-2)/(k-2) ブロック、各3点が一意なブロック）。その特殊化として位数 q（素数冪）の Miquelian 反転平面 M(q)。2 ≤ s ≤ k（反転平面では 2 ≤ s ≤ q+1）、1 ≤ d ≤ k-2（反転平面では 1 ≤ d ≤ q-1）。
evidence: ブロック交点数 t_j の2本のモーメント等式 Σ C(j,2)t_j = C(n,2)λ_2 と Σ C(j,3)t_j = C(n,3) だけを使う。2≤j≤s で C(j,2) ≥ (3/(s-2))C(j,3)（j=s で等式）なので C(n,2)λ_2 ≥ (3/(s-2))C(n,3) すなわち n ≤ (s-2)λ_2+2。補集合双対 τ_d = v - K_{k-d} と v-2=λ_2(k-2) から τ_d ≥ dλ_2。反転平面では λ_2=q+1、s=q+1 で K=q²+1、d=q-1 で τ=q²-1（tight）。K1252 の K_3≤q は τ_{q-2} ≥ (q-2)(q+1)+3 と同値。q=9 の K_3(9)=9 で excess はちょうど3。文献調査では同型の一般上界は見つからないが、(α,n)-arc の枠組み（Sane–Shrikhande–Singhi 1985, Ball 1996）が先行するため先行性は未確定。
---

# Steiner 3-設計の (s,d)-双対と反転平面の円インターセクション・スペクトル上界

## 命題

**定理（一般形）.** `D` を Steiner 3-(v,k,1) 設計（各点対が `λ_2 = (v−2)/(k−2)` ブロックに載り、
各 3 点が一意なブロックに載る）とする。

1. `2 ≤ s ≤ k` の任意の s-弧（各ブロックと高々 s 点で交わる点集合）`S` は
   `|S| ≤ (s−2)λ_2 + 2`。
2. `1 ≤ d ≤ k−2` の任意の d 重ブロッキング集合 `X`（各ブロックと少なくとも d 点で交わる）は
   `|X| ≥ d·λ_2`。
3. 双対: `K_s + τ_{k−s} = v`。とくに `s = k−2`（`d = 2`）で `τ_{k−2} = v−2`（2 点集合の補集合）。

**系（反転平面 M(q)）.** `v = q²+1`, `k = q+1`, `λ_2 = q+1` より

```
K_s(q) ≤ (s−2)(q+1) + 2      (2 ≤ s ≤ q+1)
τ_d(q) ≥ d(q+1)              (1 ≤ d ≤ q−1)
K_s(q) = q²+1 − τ_{q+1−s}(q)
```

`s = q+1` で `K_{q+1} = q²+1`、`d = q−1` で `τ_{q−1} = q²−1`（ともに tight）。

## 証明

`s`-弧 `S`（`|S| = n`）に対し `t_j` を `S` とちょうど `j` 点で交わるブロック数とする。

- 各点対は `λ_2` ブロックに載るから `Σ_{j≥2} C(j,2) t_j = C(n,2) λ_2`。
- 各 3 点は一意なブロックに載るから `Σ_{j≥3} C(j,3) t_j = C(n,3)`。

`s`-弧なので `j > s` の項はない。`2 ≤ j ≤ s` について

```
C(j,2) ≥ (3/(s−2)) C(j,3)
```

が成り立つ（`j=2` は両辺 0。`j≥3` では `C(j,2)/C(j,3) = 3/(j−2) ≥ 3/(s−2)`、
`j=s` で等式）。よって

```
C(n,2) λ_2 = Σ_{j=2}^{s} C(j,2) t_j
            ≥ (3/(s−2)) Σ_{j=3}^{s} C(j,3) t_j
            = (3/(s−2)) C(n,3)
            = C(n,2)·(n−2)/(s−2),
```

したがって `λ_2 ≥ (n−2)/(s−2)`、`n ≤ (s−2)λ_2 + 2`。□

(2) は `d = k−s` と補集合双対 `τ_d = v − K_{k−d}` から
`τ_d ≥ v − [(k−d−2)λ_2 + 2] = λ_2(k−2) − (k−d−2)λ_2 = dλ_2`。□

## 反転平面への特殊化と K1252 の読み替え

`λ_2 = q+1`。`s = 3` で `K_3 ≤ q+3`、`d = q−2` で `τ_{q−2} ≥ q²−q−2`。

K1252 の深い定理 `K_3(q) ≤ q`（q ≥ 7）は

```
τ_{q−2}(q) ≥ q² − q + 1 = (q−2)(q+1) + 3
```

と同値であり、一般上界 `d(q+1)` からの **excess がちょうど 3** であることを言う。
q=9 では `K_3(9) = 9 = q` なので `τ_7(9) = 73 = 70+3` で excess は実際に 3。

**excess 関数** `e_d(q) := τ_d(q) − d(q+1)` は

- `e_d ≥ 0`、`e_{q−1} = 0`（`s=2` の 2 点集合）、
- `e_1 ≥ q−1`（Bruen–Rothschild の `τ_1 ≥ 2q`、q ≥ 4。Kiss–Marcugini–Pambianco 2005）、
- `e_{q−2} ≥ 3`（K1252、q ≥ 7）、

を満たす。`d` が小さいほど excess は大きく、`d = q−1` で 0 になる。

## 用語と先行研究

「各ブロックと高々 α 点」の集合は設計論で **(α,n)-arc**（Sane–Shrikhande–Singhi,
*Graphs Combin.* 1 (1985) 97–106）と呼ばれ、射影平面では (k,n)-arc（Ball,
*J. London Math. Soc.* (2) 54 (1996) 581–593）。反転平面の既存語「k-arc」は
「k 点からなる弧」であり、本項の s とは別物。今回の文献調査では
`(s−2)λ_2+2` 型の一般上界は見つからなかったが、全文未取得の文献があるため
先行性は未確定である。

## 限界

- 上界は設計カウントのみで、`s=3` では K1252 の深い定理に 3 及ばない。
- `d=1` では Bruen–Rothschild の `2q` 下界の方が強い。
- 任意の Steiner 3-設計での sharpness は、反転平面の `s=q+1`, `d=q−1` 以外では未調査。
