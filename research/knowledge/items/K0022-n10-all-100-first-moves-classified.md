---
id: K0022
title: 10×10の100初手完全分類と検証境界
kind: computation
status: computed
topics:
- first-moves
- square-outcomes
- verification
aliases: []
relations:
- type: depends_on
  target: K0002
  note: ''
- type: proves
  target: K0020
  note: 全初手の分類から空盤の勝敗が従う
artifacts:
- path: rust/independent-verifier/evidence-sample/10x10-first-move-classification-complete.csv
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: rust/independent-verifier/README.md
  role: verifier
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: docs/PROOF_STATUS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 10×10（全初手）
  level: weak
  outcome: second-player-win
  classification:
  - root
  - first-moves
  coverage: 100/100 first moves; 15 D4 representatives
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - exact-search
  - csv-audit
  - partial-kyoenc4
  certificate: 空盤全体の単一KYOENC4なし
  independent_check: CSV監査と選択局面独立Rust検査
  note: 100初手完全分類と空盤証明書未統合を区別
---

# 10×10の100初手完全分類と検証境界

全100初手は先手負け。D4の15代表を厳密探索し、各代表の後手勝ち応手と必要な第3手98分岐を保存した。転置対称なケースでは53代表で98通りを被覆する。

Rust監査は代表性・D4展開・応手・分岐CSV整合性を検査する。元の巨大探索を独立Rust再帰で再求解していない。4〜8石などのKYOENC4局所検査は別の証拠であり、空盤全体の単一KYOENC4は未統合。
