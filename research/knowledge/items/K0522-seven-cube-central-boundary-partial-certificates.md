---
id: K0522
title: 7立方の中心軸二石根の下で五石N・六石Pを独立検証
kind: verification
status: verified
topics: [variants, certificates, verification, first-moves]
aliases: []
relations:
- type: supports
  target: K0505
  note: 中心側四石根の48子のうち4五石Nと3六石Pを独立検証。四石根以上は未確定
- type: supports
  target: K0521
  note: 未被覆三石境界の一つの下にある有限部分証明
artifacts:
- path: research/experiments/cube-q5-seven-hybrid-20261023/central-results.md
  role: proof
  note: 四石根・第五手・勝ち手・独立検査範囲・再現方法
- path: research/experiments/cube-q5-seven-hybrid-20261023/manifest-central.json
  role: manifest
  note: 四つの圧縮全証明書と独立検査結果のSHA-256
- path: research/experiments/cube-q5-seven-hybrid-20261023/central-five-witnesses.json
  role: data
  note: 正規化根と元の座標での第五手・勝ち手・P六石証人
- path: research/experiments/cube-q5-seven-hybrid-20261023/central-five-parents.json
  role: data
  note: 3六石Pの全五石親を正規化した10軌道への1手の帰結
scope: 7×7×7・5点共平面または共球面禁止・通常プレイ。四石集合{3,169,173,339}の下の有限部分証明
evidence: 四つの通常AND/OR全証明書を独立Bareiss幾何で検査。合計約13.03億行列式
---

点番号49x+7y+zで、四石 `{3,169,173,339}` に第五手10・45・87・129を加えた
四つの五石軌道はN。勝ち手はそれぞれ332・255・297・45で、その後の六石局面はP。
五石根からの全証明書を独立検査し、同型を除く六石P証人は3種類である。

3六石Pの全五石親は正規化して10軌道となり、それぞれ残りの1点を置けばPへ移るのでN。
10本の別々の全証明書検査を主張せず、4五石根・3六石Pの直接検査と、1手の帰結を分ける。

当該四石根の第五手は48軌道あり、今回の直接検査は4軌道だけである。
四石根、その親の三石 `{3,169,173}`、二石 `{169,173}`、7立方空盤はいずれも未確定。
