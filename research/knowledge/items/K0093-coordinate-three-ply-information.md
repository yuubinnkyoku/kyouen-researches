---
id: K0093
title: 同一盤の座標付き三手合法性は全継続ゲームを決める
kind: proposition
status: proved
topics:
- residual-games
aliases: []
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: research/experiments/structural-lemmas-2026-10-02/three-ply-equivalence.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 同一盤の座標付き三手合法性は全継続ゲームを決める

固定盤・禁止集合サイズ≤4で、安全局面S,Tの現在合法点Lが一致し、高々三点の追加合法性が全て一致するなら、全追加集合の安全性、全継続ゲーム、g、勝ち手が一致する。S,Tの石数一致は不要。

禁止四点eが追加集合U内なら両盤共通、既存Sと交わるならe\Sは高々三点なので仮定でT側も禁止。これは情報復元の定理で、深さ3打切り探索の勝敗正当化ではない。
