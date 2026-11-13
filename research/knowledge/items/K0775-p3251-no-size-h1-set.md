---
id: K0775
title: 剰余放物線Q_3251はサイズh+1=1626の集合を持たず、上界はh=1625に下がる（ソルバ主張、証明書未検査）
kind: proposition
status: needs-review
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0097
  note: 上界A(p)<=(p+3)/2と、サイズh+1の集合が(x,c,e)で3形状に尽きること
- type: depends_on
  target: K0708
  note: サイズh+2=1627の不存在（単一CNF・監査済み）からA(3251)<=1626、本項はそこから1下げる
- type: depends_on
  target: K0001
  note: 安全集合の定義（整数平面で共円・共線の四点を含まない）
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3251-1626-shapec/a3251_1626.cnf
  role: data
  note: 形状(c)（0＋一完全対＋一空対＋各対一側）の単一CNF。12,998変数・91,135節、sha256 ac06449e...
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3251-1626-shapec/receipt.json
  role: manifest
  note: ソルバ・実行コマンド・結果・証明書を作らなかった理由の記録
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_class_3251_1626.json
  role: data
  note: 形状(a)(b)のUNSAT記録（3.6秒・5.5秒、200万衝突予算）
- path: research/log/2026-11-13-p3251-no-size-h1-set.md
  role: log
  note: 発見の経緯と当時の検証状態
scope: p=3251のみ。形状(a)(b)は既存記録のUNSAT、形状(c)はcadical 1.7.3の既定設定によるUNSAT主張。
evidence: 形状(a)(b)はshape_class_3251_1626.jsonの記録。形状(c)はCNFのsha256固定済みで、cadicalが`s UNSATISFIABLE`。ただしDRAT証明書は大きすぎて未検査（143MB/212秒時点で中断）。
---

## 主張

`p = 3251`（`h = 1625`）について、サイズ `h+1 = 1626` の安全集合は存在しない。したがって

```
A(3251) <= 1625 = h
```

## 根拠

サイズ `h+1` の集合は `x + c - e = 1`（`x`: 0 を含む、`c`: 完全対数、`e`: 空対数）から3形状に尽きる。

| 形状 | `(x,c,e)` | 判定 | 記録 |
|---|---|---|---|
| (a) | `(1,0,0)` | UNSAT | 3.6 秒（200万衝突予算、`shape_class_3251_1626.json`） |
| (b) | `(0,1,0)` | UNSAT | 5.5 秒（同） |
| (c) | `(1,1,1)` | UNSAT | cadical 1.7.3 既定設定、約 35 分（`receipt.json`） |

3形状がすべて UNSAT なのでサイズ1626の集合は無い。従来の `A(3251) <= 1626`（K0708の
サイズ1627不存在から）が1改善する。

形状(c)のCNFは `search_1104_shape_c.py --write-cnf` で再生成でき、sha256 が
`ac06449ee8f662364e1519201efd9159eec9970dd4ad4c58241b6b3080bd56e5` に一致することを確認した
（証明を出したCNFと同一）。同じ符号化は p=2207 で実際に1104点のモデルを返すので（K0722）、
符号化自体の健全性は別経路で裏づけられている。

## 限界

- **証明書は未検査**。テキストDRATは 212 秒で 143 MB に達し（全体で 2 GB 超の見込み）、
  既存の `drat_check_incremental.cpp` は約 1.3k 行/秒なので検査に数日かかる。
  そのため本項の status は `computed` ではなく `needs-review` とする。
- 独立ソルバ（Glucose4）での確認を実行中。両ソルバ一致でも「証明書検査」ではない。
- 下界は K0787 が与える: `A(3251) >= 1606`（独立整数幾何監査済み）。よって
  `1606 <= A(3251) <= 1625`。サイズ `h=1625` の4形状のうち (0,0,0)・(0,1,1)・(1,0,1) は UNSAT、
  (1,1,2) は走行中。
