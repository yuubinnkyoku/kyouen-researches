---
id: K0354
title: 任意次元平行列盤の極大安全集合数は母関数で閉形式に数えられる
kind: proposition
status: proved
topics: [variants, geometry, maximal-safe, statistics]
aliases: []
relations:
- type: depends_on
  target: K0352
  note: 極大占有数の完全分類を使う
artifacts: []
scope: K0352と同じd>=3,w>=d,q>2wの平行列盤、非自明領域(d-1)m>q-1
evidence: K0352の極大分類からの全称組合せ証明
---

# 極大安全集合の終局サイズ別個数

h=d-1, r=q-1 とし、b の範囲を K0352 の L<=b<=U とする。
s=r-hb, M=m-b と置く。

終局パラメータ b を持つラベル付き占有ベクトルの個数は

A_b = sum_{j=0}^{h-1} C(w,j) [z^s] (z+z^2+...+z^M)^j.

さらに、列内の点の位置まで区別した実際の極大安全集合数は

N_b = sum_{j=0}^{h-1} C(w,j) C(m,b)^(w-j)
      [z^s] ( sum_{y=1}^M C(m,b+y) z^y )^j.

従って全極大安全集合数は sum_{b=L}^U N_b である。
K0352より終局石数は r+(w-d+1)b なので、N_b は終局サイズごとの正確な多重度でもある。

証明は極大配置を y_i=x_i-b に書き換えるだけである。
正の余剰を持つ列は高々h-1本、余剰和はs、各余剰は1以上M以下。
その列を選ぶ C(w,j) と、各列内の点を選ぶ二項係数を掛ければ上式を得る。
安全性は占有数だけに依存するため追加の幾何条件はない。
