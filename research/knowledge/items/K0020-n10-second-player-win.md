---
id: K0020
title: 10×10は後手必勝
kind: proposition
status: proved
topics:
- square-outcomes
aliases: []
relations:
- type: depends_on
  target: K0022
  note: ''
artifacts:
- path: docs/PROOF_STATUS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: rust/independent-verifier/evidence-sample/10x10-first-move-classification-complete.csv
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 10×10
  level: weak
  outcome: second-player-win
  classification:
  - root
  coverage: 15 D4代表＝100初手
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - exact-search
  - csv-audit
  - partial-kyoenc4
  certificate: 空盤面の単一KYOENC4証明書は未統合
  independent_check: CSV構造監査＋選択局面Rust証明検査
  note: 勝敗確定。全巨大探索の独立再求解ではない
---

# 10×10は後手必勝

標準10×10の空盤面は後手必勝。D4の15初手代表が100初手を被覆し、全代表で先手初手LOSSが厳密探索された。各代表の後手勝ち応手と必要な98第3手分岐を記録する。

独立RustのCSV監査は巨大探索の再求解ではない。選択局面のKYOENC4検査は存在するが、空盤面全体の単一証明書は未統合。弱解決の達成方法と独立検証の限界を分けて読む。
