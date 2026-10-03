---
id: K0299
title: q≥3の完全格子円の窓点数スペクトルは可変0..m・固定0..M_n
kind: proposition
status: proved
topics:
- geometry
aliases: []
relations: []
artifacts:
- path: research/verification/round4-circle-windows.md
  role: proof
  note: q≥3の固定窓・可変窓スペクトルの一般証明
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_circle_windows.json
  role: data
  note: 明示証人と有限照合結果
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_circle_windows.py
  role: verifier
  note: 円窓スペクトルと反例の独立検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# q≥3の完全格子円の窓点数スペクトルは可変0..m・固定0..M_n

正半径の有理中心円 (C) について (P=C\cap\mathbb Z^2)、(m=|P|)、中心の共通最小分母 (q\ge3) とする。整数位置の軸平行正方形窓
(W(a,b,n)=[a,a+n-1]\times[b,b+n-1])
を動かすと、固定 (n\ge1) で実現する点数は

[
A_n(P)=\{0,1,\ldots,M_n(P)\}
]

となる。さらに窓サイズも可変にすると

[
\bigcup_{n\ge1} A_n(P)=\{0,1,\ldots,m\}.
]

理由は、(q\ge3) なら少なくとも一方の座標方向への射影が単射になり、窓を整数一つずつ移動したとき点数が一度に2以上変化しないためである。十分大きい窓では (M_n(P)=m)。

これはK0232の曖昧な「種類が多い」という比較のうち、量化が明確で一般証明済みの部分である。q≤2との厳密優位や母集団を指定した統計比較までは含まない。
