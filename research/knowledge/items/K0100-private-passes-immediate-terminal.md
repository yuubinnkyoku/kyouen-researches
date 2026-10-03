---
id: K0100
title: 通常終端即終了の私有パス版は一手終端可能性も必要
kind: proposition
status: proved
topics:
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/verification/structural-lemmas-2026-10-02/finite-passes.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/structural-lemmas-2026-10-02/checks/early_stop_passes.json
  role: data
  note: 勝敗・共通権利消去1191391比較
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 通常終端即終了の私有パス版は一手終端可能性も必要

即終了規約では通常終端は全a,bで負け。同数は通常g、多い側は非終端なら勝ち、少ない側は通常一手で終端にできる場合だけ勝ち。共通権利を加えてもF(G,a+r,b+r)=F(G,a,b)。

同g・同権利差だけでは一般に不足。2×2空盤と二石局面はいずれもg1だが(a,b)=(0,1)では負け対勝ち。最小正方形盤2。終端パス可の式と混ぜない。
