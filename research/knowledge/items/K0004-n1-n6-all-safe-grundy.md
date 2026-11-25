---
id: K0004
title: 1×1〜6×6の全安全局面Grundy分類
kind: computation
status: computed
topics:
- grundy
- square-outcomes
aliases: []
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/log/discovery-cycles/CYCLE5_GRUNDY_STRUCTURE.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/structural-discovery/scripts/grundy_cycle5.cpp
  role: solver
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/structural-discovery/output/cycle5-grundy-n6-cap14.json
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 1×1〜6×6
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全安全局面
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - exhaustive-enumeration
  certificate: 空盤は各nのAND/OR証明書あり
  independent_check: 小盤参照実装照合、空盤C++検査
  note: 勝者は各盤の個別項目を参照
---

# 1×1〜6×6の全安全局面Grundy分類

1×1〜6×6の全安全局面のGrundy数が計算済み。2×2〜6×6の安全集合数は次のとおり。

| 盤面 | 安全集合数 |
|---|---:|
| 2×2 | 15 |
| 3×3 | 298 |
| 4×4 | 5,811 |
| 5×5 | 151,394 |
| 6×6 | 5,081,289 |

6×6では最大石数11で自然に列挙が終了し、`max_stones=14` の設定は値を打ち切っていない。
1×1〜6×6の空盤Grundy数は順に `1, 1, 1, 0, 1, 1`。
小盤Python参照・Rust初手分類との照合範囲は出典を参照する。全数計算と空盤証明書を同一資産とは扱わない。
