---
id: K0001
title: 完全指摘ルールの共円ゲームと安全局面
kind: definition
status: active
topics:
- rules
aliases: []
relations: []
artifacts:
- path: README.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: Kyouen/Rules.lean
  role: lean
  note: 整数行列式・ForbiddenFour・LegalMove・movesの実行可能定義
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 完全指摘ルールの共円ゲームと安全局面

盤点集合の未占有点に交互に石を置く。石の所有者は区別しない。新石を含む四点が同一円または同一直線上になると着手者が負ける。完全指摘では安全な追加だけを合法手とし、合法手なしの側が負ける有限通常プレイと等価である。

標準盤はB_n={0,…,n−1}²、長方形はD(w,m)={0,…,m−1}×{0,…,w−1}。安全集合の部分集合も安全なので、全安全集合は空盤から到達できる。禁止四点は相異なる点の整数行列式 [x²+y²,x,y,1] の零判定で定義する。浮動小数点による近似判定は使わない。
