---
id: K0081
title: H1/H2のLOSS共通コアをD4不変構造とみなす仮説は偽
kind: proposition
status: refuted
topics:
- residual-games
- provenance
aliases:
- H1
- H2
relations:
- type: depends_on
  target: K0080
  note: CSVのstate列が入力座標であり、各局面のD4正規形ではないことを前提に解釈する
artifacts:
- path: research/hypotheses.md
  role: source
  note: H1/H2の原仮説と機械集計
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/findings.md
  role: source
  note: F-Bの座標frame訂正
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments.jsonl
  role: log
  note: 固定R部分集合の層別LOSS数と共通部分の再集計
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# H1/H2のLOSS共通コアをD4不変構造とみなす仮説は偽

固定した8石LOSS根
`R={90,61,2,73,69,66,13,91}`
の入力座標では、層ごとのLOSS集合に共通部分が見える。保存済み再集計では、4石LOSS 12個の共通部分は `{61,66}`、5石LOSS 11個では `{91}`、6石LOSS 3個では `{61,66,69,90}` である。

しかしCSVの `state` はD4正規形ではなく入力時の座標である。各局面を個別にD4正規化すると、4石LOSS 12個のうち既知2石LOSS正規形を含むのは4個だけで、残り8個はどちらも含まない。したがって、固定Rの座標表示で見える共通石を盤面に内在するD4不変な「LOSSコア」とみなすことはできない。

H1の「4石以上で同じ{61,66}コア」という読みも、層別共通部分が5石で{91}へ変わるため成立しない。H2の「層ごとに座標コアが切り替わる」という記述自体は固定入力frameの集計事実だが、ゲーム局面の不変構造を表す一般則ではない。
