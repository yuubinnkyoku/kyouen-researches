---
id: K0097
title: 整数剰余放物線の安全最大は高々(p+3)/2、29素数では等号
kind: proposition
status: proved
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: research/experiments/structural-lemmas-2026-10-02/quadratic-constructions.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/structural-lemmas-2026-10-02/checks/independent_parabola.json
  role: data
  note: 29素数の証人の独立全四点検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 整数剰余放物線の安全最大は高々(p+3)/2、29素数では等号

Q_p={(t,t² modp)}について奇素数pではA(p)≤(p+3)/2。対{t,p−t}を二組丸ごと取ると同高さ二弦の等脚台形になり共円、完全対は高々一組なので上界が従う。

5..127の全29素数で安全証人が達成し、全3310721四点組を別Bareiss実装で検算した。全奇素数の達成は未証明。全盤K_pではなく制限集合Q_p内の値。
