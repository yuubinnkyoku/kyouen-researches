---
id: K0303
title: 幅3・全q≥4・全長の空盤Grundyと全局面最大値を分類
kind: computation
status: computed
topics: [rectangles, variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0024
  note: ''
artifacts:
- path: research/q34-exact-threshold.md
  role: source
  note: q=4全長分類
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/q35-exact-threshold.md
  role: source
  note: q=5全長分類
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/q36-three-row-classification.md
  role: source
  note: q=6およびq≥7を含む統一分類
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/check_fixed_width_20261003.py
  role: verifier
  note: 軽量統合再現
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 幅3・全q≥4・全長の空盤Grundyと全局面最大値を分類

3×m盤についてq≥4の全長分類を得た。全安全局面で現れるGrundy値の最大は、q=4,5,6,q≥7でそれぞれ6,8,8,1。

標準q=4では空盤後手勝ちはm=2,5,8だけで、m≥9は先手勝ち。q=5では空盤先手勝ちはm=1,3だけ。q=6の短盤を含め、各qの有限例外と安定末尾を完全に接続している。
