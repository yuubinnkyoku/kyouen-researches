---
id: K0193
title: 木の競合グラフで効く三点制約には最小の接続型がある
kind: question
status: open
topics:
- residual-games
- reconfiguration
aliases:
- B344
relations:
- type: depends_on
  target: K0108
  note: ''
- type: depends_on
  target: K0300
  note: 最小接続型K1,3は証明済みで、残るのは大きな木の一般分類
- type: depends_on
  target: K0680
  note: 三葉制約付き箒の全長分類と固定半径・偶奇だけでの判定の不可能性は確定した特殊族
artifacts:
- path: research/experiments/tree-triple-broom-periodicity-20261107/proof.md
  role: proof
  note: 無界箒族の34周期による全長分類と、固定半径・枝長偶奇だけでは効果を判定できない全称系
- path: research/experiments/original-claims/reports/round44-three-stone-cliques-and-tree-minima.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B344の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round44_tree_clique_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round44_tree_and_clique.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票03・B051〜B058](../../log/claim-audit/batch-03.md)、[個票04・B064〜B068](../../log/claim-audit/batch-04.md)。孤立点だけによる退化例は除いて考える。'
evidence: 原文監査 PARTIAL / minimum_connecting_tree_classification。K0680で箒族の全長34周期分類と固定半径・偶奇のみの判定不可能性を証明。任意の木の一般分類は未解決。
---

# 木の競合グラフで効く三点制約には最小の接続型がある

未確定の命題: 木の競合グラフで効く三点制約には最小の接続型がある。 三点が木のどこに位置するかを、分岐点までの距離の偶奇と共有パスで分類できる。

適用文脈: 起点: [個票03・B051〜B058](../../log/claim-audit/batch-03.md)、[個票04・B064〜B068](../../log/claim-audit/batch-04.md)。孤立点だけによる退化例は除いて考える。

現在の結論: 効く三点辺の最小接続木はK1,3と三葉上の三点辺で格子実現済みで、この部分はK0300としてprovedに分離した。より大きな木の距離偶奇による分類は未完成。

採用境界: 効く三点辺の最小接続木はK1,3・三葉上の辺、格子実現を検算。大きな木の距離偶奇による一般分類は未証明。

現在の追加到達点: K0680は、三葉と長枝を持つ箒木に三葉上の三点辺を置いた全長を分類した。
長枝L>=311でGrundy列は厳密に34周期となり、値が変わらないのはL≡5,12、
勝敗反転はL≡2,6,13,18,22,26,32 (mod34)。
任意の固定半径のマーク付き近傍・三点間距離・付加枝の偶奇が同じでも効果が異なる無限族を作れるため、
これらの局所情報だけによる一般判定は不可能。K0681で各族の有限整数点盤への実現も保証される。
任意の木全体を使う一般分類と、標準全正方形格子盤の実現問題は未解決のままである。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: abstract residual-game enumeration up to 7 vertices: K_{1,3} (Y(1,1,1)) confirmed effective (minimal type). Effectiveness depends on more than Steiner distances (e.g. Y(1,1,1) effective in 24080/27440 seven-vertex trees; ineffective when extras distributed one on each leaf). Minimal-type effectiveness shows periodic/number-theoretic dependence on arm lengths.

Scope clarification: no simple parity rule sufficient; effectiveness not determined by parity alone.

Next steps: derive pair-only Grundy values of tripods/paths and identify exact arithmetic condition. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
