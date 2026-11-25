---
id: K0311
title: misère版9×9の空盤勝敗は未確定
kind: question
status: open
topics:
- variants
- square-outcomes
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0310
  note: 8×8までの確定結果の次の盤
- type: depends_on
  target: K0019
  note: 通常版9×9の先手勝ちはmisère版へ移せない
artifacts:
- path: research/experiments/game-structure/reports/game-structure-20261003-nine.md
  role: source
  note: 9×9の128-bit探索とUNKNOWN境界
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/game-structure/output/game_structure_20261003_nine_audit.json
  role: data
  note: 9×9実装監査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/game-structure/output/game_structure_20261003_nine_center.json
  role: data
  note: 資源上限でUNKNOWN、証明書なしの実行結果
- path: research/experiments/game-structure/output/game_structure_20261003_nine_corner.json
  role: data
  note: 資源上限でUNKNOWN、証明書なしの実行結果
scope: 標準q=4の合法手、最後の合法手を指した側が負けるmisère変種の9×9空盤。
---

# misère版9×9の空盤勝敗は未確定

misère版9×9の空盤勝敗はUNKNOWN。中央優先・角優先の二つの128-bit探索はいずれも130,000,000保存局面で資源上限に達し、証明書を生成していない。

全29,152禁止四点集合、組合せ順位、UNKNOWN伝播、小盤回帰は監査済みだが、実装の監査は勝敗の証明ではない。通常版9×9の空盤先手勝ち・81初手全勝ちとは別の問題である。

直前の確定範囲はmisère 6×6後手勝ち、7×7先手勝ち・49初手全勝ち、8×8先手勝ち・勝ち初手16/負け初手48。7・8盤の全初手分類を全安全局面分類へ拡張しない。

## 2026-10-17 bounded advance (round 3)

New finite evidence: bounded misere recomputation for nearest solved square boards. 7x7: first player win, all 49 first moves winning; 7,785,121 memo records; 792,507 terminal; 44,262,805 legal edges checked; 6,364 forbidden 4-sets; independent checker passed (verified:true). 8x8: first player win; winning first moves 16 in D4 orbits {(0,0),(1,0),(2,2)}; losing 48; 84,870,165 memo records; 496,988 tiny endgame; 34,665,160 proof records; 5,582,508 terminal; 175,599,160 legal edges checked; 14,564 forbidden 4-sets; checker passed (verified:true, all_first_moves_classified:true).

Scope clarification: reproduces K0310 values and provides verified baseline only; does not determine 9x9 misere outcome. K0311 remains open.

Next steps: 9x9 misere remains unsolved/uncomputed. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
