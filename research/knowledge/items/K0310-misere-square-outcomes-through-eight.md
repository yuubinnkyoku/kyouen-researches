---
id: K0310
title: misère版の6×6は後手勝ち、7×7・8×8は先手勝ち
kind: computation
status: computed
topics:
- variants
- square-outcomes
- first-moves
aliases: [B226]
relations: []
artifacts:
- path: research/experiments/game-structure/reports/game-structure-20261003.md
  role: source
  note: §6のmisère 1..8盤の厳密勝敗と全初手分類
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/game-structure/output/game_structure_20261003_eight.json
  role: data
  note: 8×8全初手証明の集計
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/game-structure/scripts/game_structure_20261003_eight_check.cpp
  role: verifier
  note: 行列式ベースの独立検証器
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/game-structure/output/game_structure_20261003_boards.json
  role: data
  note: 6盤全局面mex対と7盤の独立P/N証明検査集計
---

# misère版の6×6は後手勝ち、7×7・8×8は先手勝ち

最後の合法手を指した側が負けるmisère変種では、6×6空盤は後手勝ち、7×7と8×8は先手勝ち。

7×7は49初手すべてが勝ち。8×8は64初手のうち16初手だけが勝ち、D4代表は(0,0),(1,0),(2,2)で、残り48初手は負け。8×8の検査対象は34,665,160局面・175,599,160合法辺で、独立検証済み。

6×6は全安全局面の通常・補助mex値を計算した。7×7・8×8は空盤と全初手を覆うP/N証明の完了であり、全安全局面のmisère値を計算した結果ではない。

B226の原文監査では、通常版も先手勝ちである8×8が一致例、通常後手・misère先手の4×4が不一致例となり、n≥4の正方形内で両型の存在が確定する。
