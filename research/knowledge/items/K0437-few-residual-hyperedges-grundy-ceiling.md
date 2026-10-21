---
id: K0437
title: 残余禁止辺h本の一点追加ゲームはGrundy値が最大2^h−1（h≥1）
kind: proposition
status: proved
topics:
- grundy
- residual-games
- variants
- geometry
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常プレイのmexと独立成分のxor
- type: depends_on
  target: K0108
  note: 極小残余禁止辺による継続ゲームの表現
artifacts:
- path: research/experiments/sparse-hyperedge-nimber-20261019/reports/sparse-hyperedge-nimber.md
  role: proof
  note: 署名類・mexによる全称証明と2辺での鋭い整数格子例
- path: research/experiments/sparse-hyperedge-nimber-20261019/scripts/verify_sparse_hyperedge.py
  role: verifier
  note: 2種類の独立再帰と小超グラフの有限全数監査
- path: research/experiments/sparse-hyperedge-nimber-20261019/scripts/verify_two_circle.cpp
  role: verifier
  note: 独立C++行列式・部分集合Grundy検証
- path: research/experiments/sparse-hyperedge-nimber-20261019/output/verification.json
  role: data
  note: 7点整数座標例と6頂点全2辺監査の再現結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 任意有限禁止集合超グラフの一点追加通常プレイ。現在の安全局面の極小残余禁止辺数h。h=0ではg≤1、h≥1ではg≤2^h−1。misèreや他人の専有石を含む多人数ゲームには直接適用しない。
evidence: '2026-10-21監査。署名交換による子局面同型、空署名のxor分離、上界2^h−1のxor閉性を確認。Python全1180二辺型とC++113安全局面を再検査。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 少数残余禁止辺からGrundy値を一様に抑える

任意の有限点集合・任意の禁止点数について、現在の残余禁止辺がh本なら、h≥1で `g≤2^h−1`、h=0で `g≤1`。残余辺に対する所属署名が等しい合法手は同型の子を生む。空署名点は独立した自由手なのでxorで分離でき、残りの署名種類数からmex上界を得る。

特に残余辺2本以下なら `g≤3` で、この上界は鋭い。整数格子7点 `[(3,4),(-5,0),(-4,-3),(-4,3),(1,0),(2,-3),(6,-5)]` は共円・共線4点組が `{0,1,2,3}` と `{0,4,5,6}` のみ。安全局面 `{1,4,5}` で `g=3`。35組の整数行列式検査、113安全局面の完全再帰、独立C++検査、6頂点の2辺超グラフ1180種類の監査で再確認した。

全称上界の証明、整数格子達成例の有限完全検査、補助的な標本監査を区別する。11×11の根の勝敗・計算時間改善は主張しない。
