---
id: K0086
title: 旧blind probe中央値3対6の改善主張は対象盤と累積memoの訂正で撤回
kind: proposition
status: withdrawn
topics:
- search-methods
- statistics
aliases: []
relations: []
artifacts:
- path: docs/9X9_TWO_STONE_PROBE_RESEARCH_NOTES.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: docs/MOVE_ORDERING_AUDIT.md
  role: source
  note: 対象10×10と累積memoの訂正文書
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 旧blind probe中央値3対6の改善主張は対象盤と累積memoの訂正で撤回

旧数値fixed中央値3/random6/default3は、docs/9X9_TWO_STONE_PROBE_RESEARCH_NOTES.mdへ9×9の盲検追試として引継がれた。しかし同branch/commitの後続監査は対象を10×10と確認し、memo-descが共有solverの累積量・入力逆順を測っていたと示したため、verdict Cと改善主張は撤回。

これは単に7親へ範囲を狭めれば有効になる結果ではない。9×9で独立に計算した三→四石非重複の幾何定理は、この数値撤回と分けて維持する。独立fresh-process測定と逆方向ascending規則の結果は別の知識を参照する。
