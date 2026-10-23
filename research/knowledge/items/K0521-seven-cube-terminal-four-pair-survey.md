---
id: K0521
title: 7立方の全1516二石軌道で4手終局未被覆三石軌道の最小値は5
kind: computation
status: computed
topics: [variants, first-moves, search-methods, verification]
aliases: []
relations:
- type: supports
  target: K0505
  note: 残る三石根を19軌道から5軌道へ減らせる中心軸上の二石組を特定
artifacts:
- path: research/experiments/cube-q5-seven-hybrid-20261023/pairs.md
  role: proof
  note: 有限計算の対象・基底5点による終端判定の根拠・再現方法
- path: research/experiments/cube-q5-seven-hybrid-20261023/rank_pairs.cpp
  role: solver
  note: 48対称性の全二石軌道と整数階数による第四手調査
- path: research/experiments/cube-q5-seven-hybrid-20261023/verify_pairs.cpp
  role: verifier
  note: 独立対称性生成と5×5 Bareiss行列式による全1516軌道の再計算
- path: research/experiments/cube-q5-seven-hybrid-20261023/pair-ranking.jsonl
  role: data
  note: 全1516二石軌道の未被覆第三手集合と三石軌道代表
- path: research/experiments/cube-q5-seven-hybrid-20261023/pair-ranking-verified.json
  role: data
  note: 約1.44億行列式の独立再計算と全行一致
scope: 7×7×7整数格子・5点共平面または共球面禁止・通常プレイ、非順序二石集合の全48対称軌道
evidence: 整数階数計算と独立Bareiss計算が全1516行で第三手集合・三石軌道代表まで一致
---

二石集合Aの第三手cを、ある第四手dにより終端四石集合へ移れるとき被覆と呼ぶ。
全1516二石軌道で、未被覆第三手数の最小値は31、未被覆三石軌道数の最小値は5。
全第三手を覆う二石組は存在しない。

点番号49x+7y+zで、5軌道を達成する二石軌道は `{168,173}` と `{169,173}` の2種類。
どちらも未被覆第三手は32手。後者の三石代表は
`{3,169,173}`, `{10,169,173}`, `{17,169,173}`, `{24,169,173}`, `{66,169,173}`。
従来の `{0,5}` は未被覆35手・19軌道なので、別の初手型でより小さい境界が得られる。

4手終局方式だけでは二石Pを証明できないという有限の限界を示す。
これら5三石根をNと証明できれば該当二石根はPとなるが、その証明はまだない。
当該二石根や7立方空盤の勝敗を主張しない。
