---
id: K0720
title: 剰余放物線の禁止四点の列挙アルゴリズムは健全・完全・重複なしで、辺リストは過不足がない
kind: proposition
status: proved
topics: [geometry, maximum-safe, verification]
aliases: []
relations:
- type: depends_on
  target: K0719
  note: 系C1 の必要方向と第四点の一意性
- type: supports
  target: K0718
  note: 前提(1)（辺リスト完全性）
artifacts:
- path: research/experiments/frontier-geometry-2026-10-05/forbidden_edges.cpp
  role: verifier
  note: 列挙本体（i<j<k と l の一意化）
- path: research/log/2026-11-10-k0334-identity-verification-omp.md
  role: log
  note: 4.3 の 1-4 と p=2647 実走の会計
scope: forbidden_edges.cpp の列挙アルゴリズムの論理。実行記録の真正性は範囲外（限界に明記）。
evidence: 健全性・完全性・重複なし・計算の完全性の4点の証明（W12 4.3）。p=2647 の総数 928,389 = 台形辺 C(1323,2)=874,503 + 残余 53,886（0 を含む辺 4）は会計の整合検査として一致。
---

## 命題

`forbidden_edges.cpp` は `i<j<k` を全走査し `l = (−(i+j+k)) mod p` を取って
`l>k` かつ `det({i,j,k,l})=0` の行だけを出力する。この出力集合は全禁止四点集合に一致する:

(i) 健全性は出力条件 `det==0` と K0719 の同値性から従う。
(ii) 完全性は、禁止四点なら `Σt≡0` より `t_4 ≡ −(t_1+t_2+t_3)` で、
`l` の計算値が `t_4` に一致し `l>k` を満たすことから従う。
(iii) 重複なしは、同一 4 点集合の他の三つ組から得られる `l` が常に `k` より
小さいことから従う。
(iv) 計算の完全性は `__int128_t` 評価と入力検査 `p<=100000` から従う
（中間積は型の範囲に収まり、丸めは入らない）。

よって p=2647 の 928,389 辺は過不足なく、うち台形辺 `C(1323,2)=874,503`、
残余 53,886（0 を含む辺 4）で、クラスCNF構築の `kept_edges=53,886` と一致する。

## 限界（実行の真正性は信頼境界として残る）

証明されるのはアルゴリズムの論理であって、実行記録ではない。残るのは次の3点で、
いずれも数学的欠落ではない:

- 走らせたバイナリが読んだソースと同一であること。
- `edges2647.txt` が 928,389 行であるという記録の真正性。
- p=2647 での独立再列挙は行っていない（総数の一致は上記を前提とした整合検査）。
