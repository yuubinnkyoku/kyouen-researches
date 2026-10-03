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
- path: research/game-structure-20261003-nine.md
  role: source
  note: 9×9の128-bit探索とUNKNOWN境界
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/game_structure_20261003_nine_audit.json
  role: data
  note: 9×9実装監査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/game_structure_20261003_nine_center.json
  role: data
  note: 資源上限でUNKNOWN、証明書なしの実行結果
- path: research/verification/game_structure_20261003_nine_corner.json
  role: data
  note: 資源上限でUNKNOWN、証明書なしの実行結果
scope: 標準q=4の合法手、最後の合法手を指した側が負けるmisère変種の9×9空盤。
---

# misère版9×9の空盤勝敗は未確定

misère版9×9の空盤勝敗はUNKNOWN。中央優先・角優先の二つの128-bit探索はいずれも130,000,000保存局面で資源上限に達し、証明書を生成していない。

全29,152禁止四点集合、組合せ順位、UNKNOWN伝播、小盤回帰は監査済みだが、実装の監査は勝敗の証明ではない。通常版9×9の空盤先手勝ち・81初手全勝ちとは別の問題である。

直前の確定範囲はmisère 6×6後手勝ち、7×7先手勝ち・49初手全勝ち、8×8先手勝ち・勝ち初手16/負け初手48。7・8盤の全初手分類を全安全局面分類へ拡張しない。
