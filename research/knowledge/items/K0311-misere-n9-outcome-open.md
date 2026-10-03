---
id: K0311
title: misère版9×9の空盤勝敗は未確定
kind: question
status: open
topics: [variants, square-outcomes, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0310
  note: 8×8までの確定結果の次の盤
artifacts:
- path: research/game-structure-20261003-nine.md
  role: source
  note: 9×9の128-bit探索とUNKNOWN境界
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/game_structure_20261003_nine_audit.json
  role: data
  note: 9×9実装監査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# misère版9×9の空盤勝敗は未確定

中央優先・角優先の二つの128-bit探索はいずれも約1.3億保存局面で資源上限に達しUNKNOWN。全29,152禁止四点集合、組合せ順位、UNKNOWN伝播、小盤回帰は監査済みだが、勝敗そのものは確定していない。
