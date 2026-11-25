---
id: K0292
title: 5×5の勝ち初手は中央3×3窓ではない
kind: proposition
status: refuted
topics:
- first-moves
aliases:
- Cycle1:H3
relations:
- type: depends_on
  target: K0043
  note: ''
artifacts:
- path: research/log/discovery-cycles/CYCLE1_RESULTS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 5×5の勝ち初手は中央3×3窓ではない

中央3×3窓が勝ち初手集合になるという候補は、n5で窓外(2,0),(0,2)が勝ち、窓内(2,1),(1,2)が負けなので反証。実際の全九勝ちセルは偶数和から四隅を除いた集合。

この修正版は5×5限定。n3の全九初手勝ち、n9の全81勝ちへ同じ座標パターンを外挿できない。
