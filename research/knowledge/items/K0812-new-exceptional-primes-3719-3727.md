---
id: K0812
title: p=3719・3727・3967・4211・4231・4373は等号A(p)=(p+3)/2を達成せず、単一CNFのDRAT証明書で監査済み（既知4素数の外側で新発見）
kind: proposition
status: computed
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0097
  note: 上界A(p)<=(p+3)/2と、サイズh+2の集合が(1,1,0)の一クラスに限られること
- type: depends_on
  target: K0771
  note: 禁止四点リストの健全・完全・重複なし（CNFの幾何節の根拠）
- type: supports
  target: K0101
  note: 「全奇素数で等号」の反例が4個から6個に増えた
- type: depends_on
  target: K0707
  note: 削除時に代入を失効させる修正版の増分DRAT検査器で証明書を検査
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/census_h2_single_cnf.py
  role: solver
  note: 等号判定を1素数1CNFで行う国勢調査器（サイズh+2は(1,1,0)の一クラスだけ）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3719-1861/receipt.json
  role: manifest
  note: 13,012変数・105,940節・23,750行DRAT・VERIFIED（31.6秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3727-1865/receipt.json
  role: manifest
  note: 13,040変数・100,592節・334,667行DRAT・VERIFIED（929秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3967-1985/receipt.json
  role: manifest
  note: 13,880変数・111,115節・10,941行DRAT・VERIFIED（7.8秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-4211-2107/receipt.json
  role: manifest
  note: 14,734変数・116,331節・326,770行DRAT・VERIFIED（917秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-4231-2117/receipt.json
  role: manifest
  note: 14,804変数・120,635節・547,219行DRAT・VERIFIED（2,396秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-4373-2188/receipt.json
  role: manifest
  note: 15,301変数・115,995節・255,753行DRAT・VERIFIED（469秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3719-1860-x1c0e0/receipt.json
  role: manifest
  note: サイズ1860クラス(1,0,0)のUNSAT証明書（32,354行・VERIFIED 23秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3719-1860-x0c1e0/receipt.json
  role: manifest
  note: サイズ1860クラス(0,1,0)のUNSAT証明書（86,491行・VERIFIED 165秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3719-1860-x1c1e1/receipt.json
  role: manifest
  note: サイズ1860クラス(1,1,1)のUNSAT証明書（472,650行・VERIFIED 1,245秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3719-1861/a3719_1861.cnf
  role: data
  note: 形状(1,1,0)の単一CNF（sha256はreceipt参照）
- path: research/log/2026-11-14-new-exceptional-primes-3719-3727.md
  role: log
  note: 発見の経緯（d走査の候補→単一CNF→証明書）と範囲の注意
scope: p=3719・3727・3967・4211・4231・4373 の6素数。他の素数での不達成は主張しない。
evidence: 両素数とも形状(1,1,0)の単一CNFがcadicalでUNSAT（2.0秒/20.7秒）。DRATを修正版増分検査器で検査し両方VERIFIED（31.6秒/929秒）。d走査でも24個（3719）のdが全て高速UNSATで、候補として独立に一致した。
---

## 主張

`p = 3719`（`h = 1859`）・`p = 3727`（`h = 1863`）・`p = 3967`（`h = 1983`）・
`p = 4211`（`h = 2105`）・`p = 4231`（`h = 2115`）・`p = 4373`（`h = 2186`）について、
サイズ `h+2` の安全集合は存在しない。すなわち

```
A(3719) <= 1860 = h+1
A(3727) <= 1864 = h+1
A(3967) <= 1984 = h+1
A(4211) <= 2106 = h+1
A(4231) <= 2116 = h+1
A(4373) <= 2187 = h+1
```

一般上界 `A(p) <= (p+3)/2`（K0097）に対し、この2素数は等号を達成しない。

## なぜ1個のCNFで足りるか

サイズ `h+2` の集合は `x + c - e = 2`（`x`=0を含む、`c`=完全対数、`e`=空対数）を満たす。
`c <= 1`（二完全対は必ず共円）なので `x=1, c=1, e=0` の一クラスに限られる。
したがって「等号を達成するか」は**1素数につき1個のSAT問題**であり、
従来の `d` ごとの全走査（`h` 個のCNF）は不要である。

実測では **UNSAT 側（不達成）が速い**: p=2207 19.9秒、p=3719 2.0秒、p=3727 20.7秒。
SAT 側（達成）は証人密度が低く単一クエリでは遅いので、この国勢調査は
「速いUNSATで候補を拾い、証明書を付ける」フィルタとして使う。

## 発見の経緯

1. 等号達成の証人を `d = h..h-5` の6通りで探す浅い走査を 3701..3899 に延長した。
2. p=3719 は24個の `d` すべてが**タイムアウトなしで短時間UNSAT**（既知4素数はここで
   タイムアウトしていた）。p=3727 も同様。
3. 単一CNFを直接解いて両方UNSAT、DRATを検査して両方VERIFIED。

既知の4素数（2207・2531・2647・3251）は 2003..3500 の走査で見つかっていた。
3719 と 3727 はその範囲の外側にあり、**不達成素数は4個で閉じていない**ことが分かった。

## さらに強い上界: p=3719 は `A(3719) <= 1859 = h`

サイズ `h+1` の集合は `x + c - e = 1` から3クラスに尽きる。p=3719 ではその3クラスすべてを
証明書つきで UNSAT と確認した:

| クラス | 変数/節 | DRAT行数 | 求解 | 証明書検査 |
|---|---|---|---|---|
| (1,0,0) | 11,154 / 102,225 | 32,354 | 2.0 秒 | 23.3 秒 |
| (0,1,0) | 13,012 / 105,938 | 86,491 | 4.2 秒 | 165.2 秒 |
| (1,1,1) | 14,870 / 109,655 | 472,650 | 150.5 秒 | 1,245 秒 |

よって **`A(3719) <= 1859 = h`**。`h+1` すら存在しないので、2531・3251 と同じ性質を持つ。

## 限界

- この2素数について言えるのは「サイズ `h+2` が存在しない」ことだけ。
  `h+1` が存在するか、`A(p)` の正確な値は未確定。
- 3719 の `h+1 = 1860` と 3727 の `h+1 = 1864` は未判定（(1,0,0)・(0,1,0) は UNSAT、(1,1,1) が未決）。
  3967 の `h+1 = 1984` も未判定。
- 国勢調査は範囲を限った有限計算であり、全素数についての主張ではない。
