---
id: K0322
title: 同nimberの占有配置は共通の幾何的追加で勝敗が分かれる
kind: proposition
status: computed
topics: [residual-games, grundy]
aliases: [B240]
relations:
- type: depends_on
  target: K0108
  note: 幾何的追加は直和との合成ではない
artifacts:
- path: research/experiments/original-claims/output/round5_b231_n4.json
  role: data
  note: b240.embedding_splitの占有mask1,2と共通追加mask4
- path: research/experiments/original-claims/scripts/round5_b231_n4.py
  role: solver
  note: 標準全Grundyから同値配置の追加後値を照合
- path: research/experiments/original-claims/reports/round68-b201-b250-original-scope-audit.md
  role: source
  note: B240原文の存在量化の監査
---

# 同nimberの占有配置は共通の幾何的追加で勝敗が分かれる

標準4×4盤、点ID=4y+xでS1={0}, S2={1}, T={2}とする。g(S1)=g(S2)=1だが、同じ占有Tを追加したg(S1∪T)=5、g(S2∪T)=0となる。

nimberが同じ継続ゲームは通常プレイの直和では同値でも、盤上で同じ点を占有する操作との合成では同値性を保たない。Rの完全同型であるとは主張せず、同nimberだけから幾何的置換を正当化できないという有限証人を記す。
