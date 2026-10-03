---
id: K0150
title: s_nが一段の拡大で2以上増える
kind: proposition
status: computed
topics:
- maximal-safe
- geometry
aliases:
- B098
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round54-small-board-saturation-jump.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B098の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 原文の指定有限盤・証人範囲
evidence: 原文監査 SUPPORTED / complete_small_board_saturation_jump
---

# s_nが一段の拡大で2以上増える

対象命題: s_nが一段の拡大で2以上増える。 n→n+1で `s_{n+1}−s_n≥2` の例がある。滑らかな線形成長ではなく、被覆デザインの適合・不適合による跳びを予想する。

現在の結論: s2=3、s3=5なので増分2が存在。原文にはn≥4という条件はなく、後からその条件を加えた問いの決着とはしない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
