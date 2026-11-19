---
id: K1067
title: 2トークン残余ゲーム z=17・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z17 y3 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1044
  note: B子の評価にz=17・y=2境界切片を、x=3帰納基底の多重集合合流{2,3}の評価にそのx=3行を使用する
- type: depends_on
  target: K1050
  note: C子の評価に1 xor (z=16・y=3境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z17-y3-boundary-20261120/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z17-y3-boundary-20261120/verify_z17_y3.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、K1044/K1050子アンカー、署名帯・mex・低R縮約・tail・閉包掃引・深域bandの独立監査
- path: research/experiments/vertical-fiber-two-token-z17-y3-boundary-20261120/census_z17_y3.py
  role: verifier
  note: 第三の独立実装（値ごと着手列挙のdict memo再帰・閉形式を知らない生再帰）によるx<=45・R<=x+45の再導出
- path: research/experiments/vertical-fiber-two-token-z17-y3-boundary-20261120/output/audit.json
  role: data
  note: 15,367,985照合・不一致0の決定論的監査結果（2回実行・別cwd byte-identical）
- path: research/experiments/vertical-fiber-two-token-z17-y3-boundary-20261120/output/census.txt
  role: data
  note: 第三実装によるT/P全行census（3,010点・閉形式と完全一致・2回実行byte一致）
- path: research/log/2026-11-20-vertical-fiber-two-token-z17-y3-boundary.md
  role: log
  note: 最新main・既存依存定理・未解決範囲の確認、証明・監査・次の着手候補
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=17、y=3、
  全x>=3・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=3では二つのトークン減少手が同じ多重集合{2,3};17
  （=K1044のx=3行）に合流して子はK1044と1 xor K1050の2種だけになり、
  R>=7では両子の全称閉形式からmex{1}=0が全Rで閉じる。x>=4ではA子を
  帰納仮説、B子をK1044、C子を1 xor K1050で評価する。全R>=1のうち
  1<=R<=x+20はreport.mdの静的行x=3..23と定常行x>=24偶数/x>=25奇数の
  A/B/C署名帯表が互いに素に被覆し、mex表から本文のT/Pが得られる。
  R>=x+21は子の一般tailからmexが親tail (x+3) mod 2に帰納的に閉じ、
  R<=18の高さのみ縮約はK0832から従う。独立監査は二直接再帰、K1044/K1050
  子アンカー、署名帯・mex、低R、tail、散点に加え、閉形式の論理述語転写の
  全行照合、帰納基底closure baseと帰納ステップmex{A,B,C}自体の閉包掃引
  (x<=5000・R<=x+20・12,602,434点)、一般行band端点・pin・基底点・定常帯・
  tailの深域サンプル(x<=200000)を含む15,367,985照合で不一致0。
  2回実行・別プロセス別cwdでbyte-identical。第三の独立実装census_z17_y3.pyが
  x<=45・R<=x+45の3,010点を再導出しT/P列入値・被覆性が閉形式と完全一致。
  有限監査は転写・実装照合であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \\(x\\ge3\\)、\\(R\\ge0\\) について、\\(H(R;(x,3);17)\\) のGrundy値0/1/2を
report.mdの \\(T(x),P(x)\\) で完全分類する。低残容量は \\(R\\le18\\) で単一トークン
\\(x+3\\) へ縮約し、高残容量は \\(R\\ge x+21\\) で \\((x+3)\\bmod2\\) となる。

値2はラダーO[1,2⌊x/2⌋+3]（x=13までの対構造）、h=z行x=14の上端19=q_odd(y+z)型
（d+z=28≡0の偶丸め・K1032/K1042/K1044/K1048/K1050/K1064に続き7例目の
q_odd(y+z)一致）、x=15..19のO[1,z] 奇数zラダー、前倒し点x=16→21（d+z=30≡2の
格子2y+(d+z)/2。ただし同格子のx=12候補19は値1側に落ち、結束条件は未解決）、
pin行x=z+y=20の{23}=2y+z（奇数z型3例目）、掃引行x=21のO[23,41]=O[pin,x+y+z]、
x≥22でO[1,17]∪{23}に定着する。

値1は奇数行x=3..13が空、偶数行x=4..12がI[x+4,∞)、基底点{18,20,22}={z+1,z+3,z+5}
が段階出現（x=14で1点・x=15,16で2点・x=19,20で3点）し、
**y点仮説集合{z+1,...,z+2y-1}がy=3で初めて完全実現**
（y=4のK1064では第4点23が値2側に奪われたのと対照的）、中間帯はz+2y+2=25開始の
奇数帯で奇数行は有限O[25,x+20]、偶数行はO[25,x+19]∪I[x+21,∞)に接続する
（I帯はtail値1の偶数行のみの一般則確認）。tailはR≥x+21=z+y+1締まりで
全既報切片とx+(z+y+1)が揃う。

## 現在の根拠と限界

全称性はx外帰納と、全Rを覆うA/B/C署名帯表・mex対応表による。B子はK1044、
C子はK1050の全称定理であり、x=3基底は多重集合合流でK1044のx=3行に直接落ち、
低R縮約・一般tailはK0832から従う。有限監査は二直接再帰・子アンカー・署名帯・
閉包掃引等の転写を照合するもので、証明そのものではない。

## 未解決

z=17・y=4（B=本項・C=1⊕K1064）、z=18・y=3（B=K1051・C=1⊕本項）、z=16・y=5
（B=K1064・C=1⊕K1049）が次の境界切片候補で、いずれも両子出版済み。
y≥2族の一般化、値1基底点y点仮説の一般証明、前倒し格子点の結束条件
（d+z≡2でも値1に落ちる格子点がある）、h=z行上端q_odd(y+z)統一式、
一様tail開始点x+(z+y+1)の一般証明、標準二次元盤の固定幅・q点安定化長は未解決。
