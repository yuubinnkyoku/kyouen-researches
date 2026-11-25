---
id: K0523
title: 7立方の非終端正四面体4石Pと正三角形3石Nを独立検証
kind: verification
status: verified
topics: [variants, certificates, verification, first-moves]
aliases: []
relations:
- type: supports
  target: K0505
  note: 4手終局だけでは閉じない三石軌道を一つNと確定。二石根と空盤は未確定
- type: supports
  target: K0521
  note: 二石組{61,85}の未被覆23三石軌道の一つを処理
artifacts:
- path: research/experiments/cube-q5-seven-tetra-20261023/README.md
  role: proof
  note: 根・勝ち手・全証明書・独立検査の範囲と再現
- path: research/experiments/cube-q5-seven-tetra-20261023/manifest.json
  role: manifest
  note: 四石全証明書・三石証明の再生成・private snapshotのSHA-256
- path: research/experiments/cube-q5-seven-tetra-20261023/stage-2-verified.json
  role: data
  note: 正四面体4石Pの337060局面・全28五石応手軌道を独立検査
- path: research/experiments/cube-q5-seven-tetra-20261023/parent-three-verified.json
  role: data
  note: 正三角形3石Nの337061局面を独立検査
scope: 7×7×7・5点共平面または共球面禁止・通常プレイ、中心正四面体4石とその三石親の一軌道
evidence: 通常AND/OR全証明書を独立Bareiss検査器で検査し、根P/N・合法手境界・全到達局面を確認
---

点番号49x+7y+zで、正四面体 `{57,89,257,281}` はP。
座標は `(1,1,1),(1,5,5),(5,1,5),(5,5,1)`。
合法な第五手は335手あり、終端Pではない。全28五石応手軌道を処理した
337,060局面の証明書を175,627,813行列式で独立検査した。

その全三石親は立方体対称性で一軌道となり、正規形 `{61,85,253}` はN。
285 `(5,5,5)` を置けば上の正四面体の等長像Pへ移る。
三石根を加えた337,061局面の全証明書も独立検査した。
この三石根には4手終局応手がなく、組 `{61,85}` の未被覆23三石軌道の一つである。

これは当該三石・四石からの有限証明であり、二石根、全初手、7立方空盤の勝敗を
確定するものではない。対応する戦略は証明書内にあり、この証明で現れる石数は最大14。
