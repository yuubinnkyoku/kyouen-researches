---
id: K1024
title: 2トークン残余ゲーム z=12・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z12 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1021
  note: B子の評価にz=12・y=3境界切片を使用する
- type: depends_on
  target: K1015
  note: C子の評価にz=11・y=4境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z12-y4-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z12-y4-boundary-20261119/verify_z12_y4.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z12-y4-boundary-20261119/output/audit.json
  role: data
  note: 2,317,475照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/log/2026-11-19-vertical-fiber-two-token-z12-y4-boundary.md
  role: log
  note: 最新main確認、y=4切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=12、y=4、
  全x>=4・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=4ではA/Bの減少手が同じ(4,3);12子に合流し、
  K1021を基底として使う。x>=5ではA子を帰納仮説、B子をK1021の
  z=12,y=3全称公式、C子を1 xor K1015のz=11,y=4全称公式で評価する。
  全R>=1はreport.mdの過渡行x=4..18と定常行x>=19奇数/x>=20偶数の
  A/B/C署名帯表が互いに素に被覆し、mex表から本文のT/Pが得られる。
  K0832からR<=13の高さのみ縮約とR>=x+17の一般tailも従う。
  独立監査は順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯、
  mex、Theorem T、縮約、tail、散点を含む2,317,475照合で不一致0、
  二回実行byte-identical。有限監査は転写・実装照合であり、全称性は
  x外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge4\)、\(R\ge0\) について、\(H(R;(x,4);12)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le13\) で単一トークン
\(x+4\) へ縮約し、高残容量は \(R\ge x+17\) で \((x+4)\bmod2\) となる。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1021、C子はK1015の
全称定理であり、低R縮約・一般tail・Theorem TはK0832から従う。
有限監査は二直接再帰・子アンカー・署名帯・mex等の転写を照合するもので、
証明そのものではない。

z=12のy>=5、z>=13のy>=2、全高さを統合する2トークン一般式、
標準二次元盤の固定幅・q点版安定化長は未解決。
