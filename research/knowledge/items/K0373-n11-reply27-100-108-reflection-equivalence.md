---
id: K0373
title: 11×11二石局面60・27の第三手100と108は反射対称
kind: proposition
status: proved
topics: [square-outcomes, search-methods, verification]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共円・共線の禁止と通常プレイの対称不変性
- type: depends_on
  target: K0002
  note: 元先手固定の勝敗
- type: depends_on
  target: K0355
  note: 第三手被覆とS4 classの正規化
artifacts:
- path: research/experiments/n11-two-target-design-20261010/README.md
  role: proof
  note: 頂点100・108の根局面安定化群による同一軌道の証明
- path: research/experiments/n11-two-target-design-20261010/output/post-probe/strategy-analysis.json
  role: data
  note: 全115対象S4 classの分類と共有局面の有限監査
scope: 11×11標準通常版。二石盤面{60,27}を固定した合法な第三手100・108の勝敗の同値性と、D4正規化S4 classの両頂点被覆。
---

# 第三手100と108は反射対称

11×11の点番号を `11r+c` とする。変換

\[
f(11r+c)=11r+(10-c)
\]

は盤面の縦軸反射で、中央点60=(5,5)と点27=(2,5)をそれぞれ固定する。また100=(9,1)を108=(9,9)へ写す。この反射は距離・共円・共線、合法な遷移、終局条件と着手順の勝敗を保存する。従って、**二石root `{60,27}` における第三手100と108は同一の勝敗**である。

さらに、第三手100を含む任意の四石局面 `{60,27,100,x}` を反射すると `{60,27,108,f(x)}` となる。どちらもD4で正規化すると同じS4 classに属する。よって **100だけ、または108だけを被覆するS4 classは存在しない**。一方の第三手を覆うS4 LOSS classが見つかれば、他方も同じ証明で覆われる。二つの第三手を別々のLOSS classで証明する方式に固有の被覆上の利益はない。

保存済みの独立整数幾何による全3,384 classの列挙もこの結論を再確認した。最新記録時点で100と108の双方を被覆する115 classのうち53 WIN・62 UNKNOWN・0 LOSSである。ただしこれはsolver/cacheを前提とした有限分類であり、上記の反射同値性そのものは計算を前提にしない数学的証明である。

その他の第三手や11×11空盤全体の勝敗は、この同値性から決まらない。二石rootがLOSSと確定するには、残る同値軌道を覆うS4 LOSS classと、他の117第三手に対する既存の確定根拠を正しく検証する必要がある。
