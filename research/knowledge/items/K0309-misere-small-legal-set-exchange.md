---
id: K0309
title: 合法点5個以下では通常値とmisère補助値は0と1だけ交換される
kind: proposition
status: proved
topics: [variants, grundy]
aliases: []
relations: []
artifacts:
- path: research/experiments/game-structure/reports/game-structure-20261003.md
  role: proof
  note: 5合法点交換則の一般証明
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/game-structure/reports/game-structure-20261003-extra.md
  role: source
  note: 6合法点での最初の例外分類
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/game-structure/output/game_structure_20261003_complexes.json
  role: data
  note: 6頂点全族の完全分類
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 合法点5個以下では通常値とmisère補助値は0と1だけ交換される

任意の遺伝的配置ゲームで、現在の合法点が5個以下なら、通常Grundy値gと終端を1にしたmisère補助mex値hは0↔1を交換し、2以上は不変である。列挙に依存しない構造証明がある。

境界は鋭く、合法点6個で初めて例外が現れる。6頂点の7,785,062族を完全分類すると例外69,940個、同型169種で、全て両ルールで負ける局面である。
