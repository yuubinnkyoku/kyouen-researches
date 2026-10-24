---
id: K0531
title: 11×11の7個の9石WINを89個の終局WIN葉で独立検証し63個の8石WINを導出
kind: verification
status: verified
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の奇数AND・偶数OR伝播
- type: depends_on
  target: K0516
  note: 既存86個の9石WIN根との比較
- type: depends_on
  target: K0528
  note: 既存10石LOSS葉からの不足境界探索
artifacts:
- path: research/experiments/n11-s9-win7-expansion-20261024/s9-win7.keys
  role: certificate
  note: 9石WIN根7件
- path: research/experiments/n11-s9-win7-expansion-20261024/s10-win89.keys
  role: certificate
  note: 全合法10石WIN子89件
- path: research/experiments/n11-s9-win7-expansion-20261024/s8-win63.keys
  role: certificate
  note: 導出した8石WIN親63件
- path: research/experiments/n11-s9-win7-expansion-20261024/verify.py
  role: verifier
  note: 全子・親・独立終局勝敗の検証
- path: research/experiments/n11-s9-win7-expansion-20261024/frontier_audit.py
  role: verifier
  note: 427個の既存LOSS葉の逆向き構造と最小不足8件の監査
- path: research/experiments/n11-s9-win7-expansion-20261024/audit_coverage.py
  role: verifier
  note: 63親の新規性・504辺の監査
scope: 標準11×11、q=4、完全指摘、通常プレイ、元先手固定視点。指定9石7根と8石親63件のみ。
evidence: 7根の全合法10石子89件をC++4×4整数行列式とPython3×3整数行列式で終局WINと独立検証し、合法手数不一致0。別の盤面再帰C++/Pythonで状態数合計2800が一致。9石ANDの全子WINから7根WIN、8石ORの合法9石WIN子から63親WIN。旧86根由来の687親・凍結8石WIN13501件と重複0、凍結8石LOSS294件と矛盾0。7石親247件への証明辺504本を追加。新規7石閉包・二石root閉鎖0。空盤UNKNOWN。
---

# 7個の9石WINと63個の8石WINを終局から証明

証明根・全合法子・導出親は対応する実験ディレクトリに固定。9石は元先手固定のANDなので89個の10石子がすべてWINなら7根WIN、8石はORなので証明済み9石WIN子を持つ63親もWIN。

427個の既存10石LOSS葉からの逆向き被覆では、8石候補17,338件中、全子が覆われたのは既存38根のみ。最小不足8件の8石候補に9石WIN子が見つかり、その証明を近隣へ広げた。最小不足はLOSSの証拠ではない。

63親は旧86根の8石親687件と重ならず、凍結8石WIN13,501件にも含まれない。7石への証明済み504辺は増加したが、7石の新規全子閉包はない。証明は凍結cache判定に依存しない。二石rootと空盤勝敗は未解決であり、標準11×11空盤はUNKNOWN。
