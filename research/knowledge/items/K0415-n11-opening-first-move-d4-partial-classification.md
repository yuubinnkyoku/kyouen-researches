---
id: K0415
title: 11×11空盤の初手D4分類で2軌道をLOSS、19軌道は未確定
kind: proposition
status: computed
topics: [square-outcomes, first-moves, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の交互AND/OR規則
- type: depends_on
  target: K0414
  note: 二石root {60,27} の119手solver-trusted LOSS結果
artifacts:
- path: research/experiments/n11-opening-orbits-weak-solve-20261012/README.md
  role: source
  note: 軌道分類、応手境界、信頼範囲、再現手順
- path: research/experiments/n11-opening-orbits-weak-solve-20261012/scripts/analyze_openings.py
  role: verifier
  note: 独立BoardによるD4 orbitと限定応手boundaryの列挙
- path: research/experiments/n11-opening-orbits-weak-solve-20261012/output/opening-analysis.json
  role: data
  note: 121初手全ての21軌道、各マス、status、sample response boundaries
- path: research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json
  role: certificate
  note: "`{60,27}` の119/119第三手LOSS応手表"
scope: 11×11標準通常版の空盤面における初手マス。現時点で勝敗を確定したのは21 D4軌道中2軌道だけ。
evidence: 11×11 D4の21軌道・121マスを独立幾何で列挙した。二石局面は着手順を入れ替えても局面と次手番が同じなので `{60,27}` LOSS は `{27,60}` LOSSを与える。さらにD4で中心60を固定し、27の軌道 `{27,57,63,93}` 全てを初手LOSSへ移す。従って初手60とこの4マスの2軌道（5/121マス）がLOSS。中心60は全ての非中心初手に合法な後手応手（120/120）だが、他の `{first,60}` rootの勝敗は未確定。残る19軌道・116マスは未分類で、空盤面全体の弱解決ではない。
---

独立D4分類は21軌道・121マスを全て覆う。二石位置 `{60,27}` の固定元先手視点LOSSは2手の順序交換で `{27,60}` にも適用できる。D4回転・反射で27は `{27,57,63,93}` に移るため、初手60とこの4マスはLOSSである。

他の19初手軌道は未確定。中央60が120個の非中央初手すべてに合法な第二手であることは確認したが、その二石rootがLOSSだとは推論していない。空盤面全体の勝敗、初手の完全分類、独立terminal-only証明は含まない。
