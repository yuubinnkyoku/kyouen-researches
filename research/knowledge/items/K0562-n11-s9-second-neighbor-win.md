---
id: K0562
title: 11×11の別の9石WIN局面を17個の終局10石子で独立検証
kind: verification
status: verified
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の奇数AND・偶数OR伝播
- type: depends_on
  target: K0560
  note: 既存9石WINの一石交換近傍と独立検証の比較
- type: depends_on
  target: K0105
  note: 局所終局証明は空盤勝敗を確定しない
artifacts:
- path: research/experiments/n11-s9-second-neighbor-20261025/s10-win17.keys
  role: certificate
  note: 9石局面の全17合法10石WIN子
- path: research/experiments/n11-s9-second-neighbor-20261025/s8-win9.keys
  role: certificate
  note: 9個の合法8石WIN親
- path: research/experiments/n11-s9-second-neighbor-20261025/verify.py
  role: verifier
  note: 独立Python整数幾何と終局までの再帰・親子照合
- path: research/experiments/n11-s9-second-neighbor-20261025/reproduce.sh
  role: verifier
  note: 4×4整数行列式C++と3×3 Pythonの17葉判定・合法着手数照合
scope: 標準11×11、q=4、完全指摘、通常プレイ。9石根00000000040400111000010a00001000と9個の8石親。元先手固定視点。
evidence: 9石根の全17合法10石子が終局まで元先手WIN。独立Python探索の葉別状態数合計1745、C++探索1806。17葉の勝敗と合法着手数が一致。9石ANDで元先手WIN、8石ORで9親が元先手WIN。凍結8石LOSS294件との衝突0。空盤UNKNOWN。
---

# 9石局面の全子終局証明

9石 `00000000040400111000010a00001000` は元先手WIN（後手番側LOSS）。全17合法10石子を再列挙し、各子の終局までの独立再帰で全子元先手WINを確認した。3×3差分行列式Pythonと4×4整数行列式C++の17子判定と合法手数が一致する。

9個の8石親はそれぞれ合法な9石WIN証人を持つため元先手WIN。比較用の既存凍結8石LOSSと矛盾なし。二石root・空盤は未確定であり、標準11×11空盤はUNKNOWN。
