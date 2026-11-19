---
id: K1052
title: 2トークン残余ゲーム z=19・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z19 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1023
  note: B子の評価にy=1パラメトリック全z閉形式のz=19行を使用する
- type: depends_on
  target: K1051
  note: C子の評価に1 xor (z=18・y=2境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z19-y2-boundary-20261120/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z19-y2-boundary-20261120/verify_z19_y2.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、K1023/K1051子アンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z19-y2-boundary-20261120/output/audit.json
  role: data
  note: 3,599,136照合・不一致0の決定論的監査結果
- path: research/log/2026-11-20-vertical-fiber-two-token-z19-y2-boundary.md
  role: log
  note: 最新main・既存依存定理・未解決範囲の確認、証明・監査・次の着手候補
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=19、y=2、
  全x>=2・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=2では2つのトークン減少手が同じ多重集合(1,2);19に合流し、
  K1023のz=19行x=2を基底にする。x>=3ではA子を帰納仮説、B子をK1023、
  C子を1 xor K1051で評価する。全R>=1のうち1<=R<=x+21はreport.mdの
  過渡行x=2..23と定常行x>=25奇数/x>=24偶数のA/B/C署名帯表が互いに素に被覆し、
  mex表から本文のT/Pが得られる。K0832からR<=21の高さのみ縮約とR>=x+22の
  一般tailも従う。独立監査は二直接再帰、K1023/K1051子アンカー、署名帯・mex、
  低R、tail、散点を含む3,599,136照合で不一致0。有限監査は転写・実装照合であり、
  全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \\(x\\ge2\\)、\\(R\\ge0\\) について、\\(H(R;(x,2);19)\\) のGrundy値0/1/2を
report.mdの \\(T(x),P(x)\\) で完全分類する。低残容量は \\(R\\le21\\) で単一トークン
\\(x+2\\) へ縮約し、高残容量は \\(R\\ge x+22\\) で \\((x+2)\\bmod2\\) となる。

## 現在の根拠と限界

全称性はx外帰納と、全Rを覆うA/B/C署名帯表による。B子はK1023、C子はK1051の
全称定理であり、低R縮約・一般tailはK0832から従う。有限監査は二直接再帰・
子アンカー・署名帯・mex等の転写を照合するもので、証明そのものではない。

値1基底点は \\(\\{20,22\\}=\\{z+1,z+3\\}\\)（\\(x\\ge19\\) の全行、\\(x=18\\) 行は
\\(\\{20\\}\\) のみ）で、y=2族ではz=12..19の8連続。
pinは \\(23=2y+z\\)（奇数z型）、掃引行は \\(x=z+y+1=22\\)、掃引帯は
\\(O[23,43]\\)。\\(x+y=z\\) 行x=17の連続上端21と \\(x=z+2\\) 行x=21の孤立pin 23は
ともに \\(d+z\\equiv2\\pmod4\\) の格子式 \\(2y+(d+z)/2\\) に一致し、奇数zの配置は
K1044と同じで偶数zのK1051/K1042と対称。低R縮約の境界 \\(R\\le21=z+2\\) は
K1051と同じく \\(z+1\\) を1つ超える。
z=19・y>=3、y>=2族の一般化、値1基底点y点仮説・d+z剰余格子の一般証明、
標準二次元盤の固定幅・q点版安定化長は未解決。
