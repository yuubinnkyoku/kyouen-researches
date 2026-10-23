---
id: K0524
title: 7立方の内側正四面体・中心軸四石Nと五石Pの独立証明
kind: verification
status: verified
topics: [variants, certificates, verification, first-moves]
aliases: []
relations:
- type: supports
  target: K0505
  note: 三石Nを証明する第四手の候補選択に必要なN四石の有限証明。上位根は未確定
artifacts:
- path: research/experiments/cube-q5-seven-inner-tetra-20261023/README.md
  role: proof
  note: 内側正四面体4石Nと中心追加後の5石P、再生成手順、検査範囲
- path: research/experiments/cube-q5-seven-inner-tetra-20261023/manifest.json
  role: manifest
  note: 圧縮全証明・独立検査結果・四石証明再生成のSHA-256
- path: research/experiments/cube-q5-seven-central-line-20261023/README.md
  role: proof
  note: 中心軸四石Nと157着手後の五石P
- path: research/experiments/cube-q5-seven-central-line-20261023/stage-3-verified.json
  role: data
  note: 1590127局面の全証明を約10.87億Bareiss行列式で独立検査
scope: 7×7×7・5点共平面または共球面禁止・通常プレイ、二つの四石Nと対応する五石P
evidence: 通常AND/OR全証明書を独立Bareiss幾何で検査し、全合法応手と全到達局面を確認
---

点番号49x+7y+zで、内側正四面体 `{114,130,214,226}` はN。
171（中心）を置いた五石はP。五石Pの169,941局面と、四石Nの169,942局面を
それぞれ独立検査した。K0523の座標1/5の正四面体はPだったが、こちらの座標2/4はN。

また `{24,169,171,173}` はNで、157着手後はP。
五石の正規形は `{73,150,169,171,173}`。四石根からの1,590,127局面を
独立検査し、その内部の五石Pの全証明も確認した。

これら二つの五石Pの全四石親も、残りの1点を置けばPへ移るのでNである。
直接検査した二つの四石根と、1手の帰結による他の親を区別する。
非終端四石を一律にPとすることはできず、この四石Nから親の三石の勝敗は決まらない。
二石根・全初手・7立方空盤は依然未確定。
