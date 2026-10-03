---
id: K0078
title: 3×m・q=5のm=22..39にも不足極大安全集合は存在しない
kind: proposition
status: computed
topics: [rectangles, variants]
aliases: []
relations:
- type: supports
  target: K0071
  note: M_{3,5}=12の有限区間部分を閉じる
artifacts:
- path: research/q35-exact-threshold.md
  role: source
  note: 支持集合グラフによる完全排除
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/q35_exact_threshold.json
  role: data
  note: m=12..40の全候補集計
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/q35_support_exclusion.cpp
  role: solver
  note: 外部4点集合を全列挙する完全排除
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 3×m・q=5のm=22..39にも不足極大安全集合は存在しない

旧未解決区間m=22..55のうち、m=22..39は支持集合による必要条件と正確なblockerグラフを用いた完全列挙で不足極大が0。m≥40は別の一般被覆上界で排除される。

したがって旧「22..55で再出現するか」という問題は否定され、K0071のM_{3,5}=12が確定する。
