---
id: K0046
title: 証明書の石数パリティとWIN/LOSS分離は形式の帰結
kind: proposition
status: proved
topics:
- certificates
- provenance
aliases: []
relations:
- type: depends_on
  target: K0007
  note: ''
artifacts:
- path: night-research/CYCLE5_GRUNDY_STRUCTURE.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/cycle6-parity-law-verify.json
  role: data
  note: 全9証明書のパリティ則照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 証明書の石数パリティとWIN/LOSS分離は形式の帰結

各証明辺は一石追加してWIN/LOSSを反転するので、証明DAGノードの石数kのラベルはrootラベルとkの偶奇で決まる。全9証明書を0違反で照合した。

これをゲーム全安全局面のパリティ則と解釈しない。旧scanは後手盤方向だけを仮定して先手盤をmixedと誤標記した。小盤の全安全局面ではn=4,5などでパリティだけの勝敗判定が破れる。
