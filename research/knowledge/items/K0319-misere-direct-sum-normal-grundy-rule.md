---
id: K0319
title: swap則が全後続局面で成り立つ部品のmisère直和は通常Grundy値だけで解ける
kind: proposition
status: proved
topics: [variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0309
  note: 各部品と全後続局面が0↔1 swap則を満たすことを仮定する
artifacts:
- path: research/game-structure-20261003.md
  role: proof
  note: misère直和の必要十分条件と共円ゲームへの適用
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/game_structure_20261003_complexes.json
  role: data
  note: swap則の有限分類と境界例
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# swap則が全後続局面で成り立つ部品のmisère直和は通常Grundy値だけで解ける

各部品とその全後続局面で、通常Grundy値gとmisère補助値hが
`0↔1`、2以上不変のswap則を満たすとする。このとき部品の通常Grundy値だけから、misère直和のP/Nを通常のmisère Nimと同じ規則で判定できる。

全ての部品値が0または1ならxorが1のときP、少なくとも一つ2以上ならxorが0のときP。

1×1〜4×4の任意の共円ゲーム局面を部品とする任意個数の直和に適用できる。一方5×5にはswap則を破る後続構造が実現されるため、この適用範囲は自動には拡張しない。
