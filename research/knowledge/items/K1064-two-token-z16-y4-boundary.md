---
id: K1064
title: 2トークン残余ゲーム z=16・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z16 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1050
  note: B子の評価にz=16・y=3境界切片を使用する
- type: depends_on
  target: K1048
  note: C子の評価に1 xor (z=15・y=4境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z16-y4-boundary-20261120/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z16-y4-boundary-20261120/verify_z16_y4.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、K1050/K1048子アンカー、署名帯・mex・低R縮約・tail・閉包掃引・深域bandの独立監査
- path: research/experiments/vertical-fiber-two-token-z16-y4-boundary-20261120/census_z16_y4.py
  role: verifier
  note: 第三の独立実装（値ごと着手列挙のdict memo再帰・閉形式を知らない生再帰）によるx<=45・R<=x+45の再導出
- path: research/experiments/vertical-fiber-two-token-z16-y4-boundary-20261120/output/audit.json
  role: data
  note: 14,667,509照合・不一致0の決定論的監査結果（2回実行・別cwd byte-identical）
- path: research/experiments/vertical-fiber-two-token-z16-y4-boundary-20261120/output/census.txt
  role: data
  note: 第三実装によるT/P全行census（2,961点・閉形式と完全一致・2回実行byte一致）
- path: research/log/2026-11-20-vertical-fiber-two-token-z16-y4-boundary.md
  role: log
  note: 最新main・既存依存定理・未解決範囲の確認、証明・監査・次の着手候補
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=16、y=4、
  全x>=4・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=4ではA子とB子が同じ多重集合(3,4);16に合流し、
  K1050のx=4行とK1048のx=4行を基底にする。x>=5ではA子を帰納仮説、
  B子をK1050、C子を1 xor K1048で評価する。全R>=1のうち1<=R<=x+20は
  report.mdの過渡行x=4..22と定常行x>=24偶数/x>=23奇数のA/B/C署名帯表が
  互いに素に被覆し、mex表から本文のT/Pが得られる。K0832からR<=17の
  高さのみ縮約とR>=x+21の一般tailも従う。独立監査は二直接再帰、K1050/K1048
  子アンカー、署名帯・mex、低R、tail、散点に加え、閉形式の論理述語転写の
  全行照合、帰納ステップmex{A,B,C}自体の閉包掃引(x<=5000・R<=x+20・
  12,602,434点)、一般行band端点・pin・定常帯・tailの深域サンプル
  (x<=200000)を含む14,667,509照合で不一致0。2回実行・別プロセス別cwdで
  byte-identical。第三の独立実装census_z16_y4.pyがx<=45・R<=x+45の2,961点を
  再導出しT/P列入値・被覆性が閉形式と完全一致。有限監査は転写・実装照合
  であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge4\)、\(R\ge0\) について、\(H(R;(x,4);16)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le17\) で単一トークン
\(x+4\) へ縮約し、高残容量は \(R\ge x+21\) で \((x+4)\bmod2\) となる。

## 現在の根拠と限界

全称性はx外帰納と、全Rを覆うA/B/C署名帯表による。B子はK1050、C子はK1048の
全称定理であり、低R縮約・一般tailはK0832から従う。有限監査は二直接再帰・
子アンカー・署名帯・閉包掃引等の転写を照合するもので、証明そのものではない。
閉包掃引は帰納ステップの機械照合である。

値1基底点は \(x\ge20\) で
\(\{17,19,21,23\}=\{z+1,z+3,z+5,z+7\}\) となり、y=4点型の全称実例。
pinは \(25=2y+z+1\)、掃引行は \(x=z+y+1=21\)、掃引帯は \(O[25,41]\)。
前倒し点21・23は \(d+z\equiv2\pmod4\) の格子式 \(2y+(d+z)/2\) に一致し、
h=z行x=12の上端19はq型。z=16・y>=5、z=17・y>=3の次の境界切片、\(y\ge z/2\)
一様族の奇数z統一式、値1基底点y点仮説・d+z剰余格子の一般証明、標準二次元盤の
固定幅・q点版安定化長は未解決。
