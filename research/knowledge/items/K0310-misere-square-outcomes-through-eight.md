---
id: K0310
title: misère版の6×6は後手勝ち、7×7・8×8は先手勝ち
kind: computation
status: computed
topics: [variants, square-outcomes, first-moves]
aliases: []
relations: []
artifacts:
- path: research/game-structure-20261003-nine.md
  role: source
  note: 正方形盤misère探索のまとめ
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/game_structure_20261003_eight.json
  role: data
  note: 8×8全初手証明の集計
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/game_structure_20261003_eight_check.cpp
  role: verifier
  note: 行列式ベースの独立検証器
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# misère版の6×6は後手勝ち、7×7・8×8は先手勝ち

最後の合法手を指した側が負けるmisère変種では、6×6空盤は後手勝ち、7×7と8×8は先手勝ち。

7×7は49初手すべてが勝ち。8×8は64初手のうち16初手だけが勝ち、D4代表は(0,0),(1,0),(2,2)で、残り48初手は負け。8×8の検査対象は34,665,160局面・175,599,160合法辺で、独立検証済み。
