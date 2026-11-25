---
id: K1050
title: 2トークン残余ゲーム z=16・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z16 y3 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1042
  note: B子の評価にz=16・y=2境界切片を使用する
- type: depends_on
  target: K1034
  note: C子の評価に1 xor (z=15・y=3境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z16-y3-boundary-20261120/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z16-y3-boundary-20261120/verify_z16_y3.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、K1042/K1034子アンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z16-y3-boundary-20261120/output/audit.json
  role: data
  note: 45,804照合・不一致0の決定論的監査結果
- path: research/log/2026-11-20-vertical-fiber-two-token-z16-y3-boundary.md
  role: log
  note: 最新main・既存依存定理・未解決範囲の確認、証明・監査・次の着手候補
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=16、y=3、
  全x>=3・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=3ではA子とB子が同じ多重集合(3,2);16に合流し、
  K1042のx=3行とK1034のx=3行を基底にする。x>=4ではA子を帰納仮説、
  B子をK1042、C子を1 xor K1034で評価する。全R>=1のうち1<=R<=x+19は
  report.mdの過渡行x=3..21と定常行x>=22偶数/x>=23奇数のA/B/C署名帯表が
  互いに素に被覆し、mex表から本文のT/Pが得られる。K0832からR<=17の
  高さのみ縮約とR>=x+20の一般tailも従う。独立監査は二直接再帰、K1042/K1034
  子アンカー、署名帯・mex、低R、tail、散点を含む45,804照合で不一致0。
  有限監査は転写・実装照合であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge3\)、\(R\ge0\) について、\(H(R;(x,3);16)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le17\) で単一トークン
\(x+3\) へ縮約し、高残容量は \(R\ge x+20\) で \((x+3)\bmod2\) となる。

## 現在の根拠と限界

全称性はx外帰納と、全Rを覆うA/B/C署名帯表による。B子はK1042、C子はK1034の
全称定理であり、低R縮約・一般tailはK0832から従う。有限監査は二直接再帰・
子アンカー・署名帯・mex等の転写を照合するもので、証明そのものではない。

値1基底点は \(x\ge19\) で
\(\{17,19,21\}=\{z+1,z+3,z+5\}\) となり、y=3点型の全称実例。
pinは \(23=2y+z+1\)、掃引行は \(x=z+y+1=20\)、掃引帯は \(O[23,39]\)。
前倒し点21は \(d+z\equiv2\pmod4\) の格子式 \(2y+(d+z)/2\) に一致し、
h=z行x=13の上端19はq_odd型。z=16・y>=4、z=17・y>=3、y>=2族の一般化、
値1基底点y点仮説・d+z剰余格子の一般証明、標準二次元盤の固定幅・q点版
安定化長は未解決。
