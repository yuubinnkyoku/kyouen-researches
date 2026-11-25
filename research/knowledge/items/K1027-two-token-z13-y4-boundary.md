---
id: K1027
title: 2トークン残余ゲーム z=13・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z13 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1026
  note: B子の評価とx=4帰納基底にz=13・y=3境界切片を使用する
- type: depends_on
  target: K1024
  note: C子の評価にz=12・y=4境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z13-y4-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z13-y4-boundary-20261119/verify_z13_y4.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z13-y4-boundary-20261119/output/audit.json
  role: data
  note: 13,817,576照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z13-y4-boundary-20261119/census_z13_y4.py
  role: verifier
  note: x=4..45・R=0..x+45の生二再帰センサス（二エンジン一致・閉形式一致・tail）で行表を第三導出から照合する
- path: research/experiments/vertical-fiber-two-token-z13-y4-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z13-y4-boundary.md
  role: log
  note: 最新main確認、y=4切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=13、y=4、
  全x>=4・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=4では二つのトークン減少手が同じ(3,4);13子に合流し、
  K1026のx=4行（(3,4)≡(4,3)の対称性）を基底として使う。x>=5では
  A子を帰納仮説、B子をK1026のz=13,y=3全称公式、C子を1 xor K1024の
  z=12,y=4全称公式で評価する。全R>=1はreport.mdの過渡行x=4..19と
  定常行x>=21奇数/x>=20偶数のA/B/C署名帯表が互いに素に被覆し、
  mex表から本文のT/Pが得られる。K0832からR<=14の高さのみ縮約と
  R>=x+18の一般tailも従う。独立監査は順序保持・降順正準化の二直接再帰、
  B/Cアンカー、署名帯、mex、Theorem T、縮約、tail、散点を含む
  13,817,576照合で不一致0、二回実行byte-identical（別プロセス2回でも
  byte-identical）。加えて生二再帰センサス（x=4..45・R=0..x+45）が
  行表・tailを第三導出から照合して0不一致。有限監査は転写・実装照合であり、
  全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge4\)、\(R\ge0\) について、\(H(R;(x,4);13)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le14\) で単一トークン
\(x+4\) へ縮約し、高残容量は \(R\ge x+18\) で \((x+4)\bmod2\) となる。

値2位置はx=4でO[1,7]、x=5,6でO[1,9]、x=7,8でO[1,11]、x=9（高さx+y=z行）で
O[1,17]（上端17=2y+(d+z)/2・d=5・d+z≡2 (mod 4)のd格子点）、x=10,11,12でO[1,13]、
x=13でO[1,13]∪\{19\}（前倒し点19）、x=14,15,16でO[1,13]、
x=17でO[1,13]∪\{21\}（前倒し点21=pin、掃引行の1行手前）、
x=18の掃引行でO[1,13]∪O[21,35]、x≥19でO[1,13]∪\{21\}に定着する
（pin=21=2y+z・奇数zラダーO[1,z]）。
値1位置はx∈{4,6,8}で空、x=5でI[10,∞)、x=7でI[12,∞)、x=9,11で\{14,16,18\}∪I[19,∞)、
x=10で\{14,16\}、x=12,14で\{14,16,18\}、x=13,15で\{14,16,18,20\}∪I[21,∞)、
x=16,18で\{14,16,18,20\}、x=17で\{14,16,18,20\}∪I[22,∞)、
偶数x≥20で\{14,16,18,20\}∪O[23,x+17]、
奇数x≥19で\{14,16,18,20\}∪O[23,x+16]∪I[x+18,∞)。値1基底点は
\{14,16,18,20\}=\{z+1,z+3,z+5,z+7\}（y=1の1点・y=2の2点・y=3の3点に続き、
値1基底点がy点になる仮説の4例目）、中間帯は z+2y+2=23 から偶奇z追従の奇数帯、
無限I帯は奇数x行のみでtail R≥x+18の値 \((x+4)\bmod2\) と一致する。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。x=4では二つのトークン減少手が
同一の(3,4);13≡(4,3);13多重集合子に合流し、K1026のx=4行を帰納基底として使う。
B子はK1026、C子はK1024の全称定理であり、低R縮約・一般tail・Theorem Tは
K0832から従う。前倒し点はx=13の19（d格子点 \(2y+(d+z)/2\)、\(d=9=x-y\)、
\(d+z\equiv2\pmod4\)）とx=17の21（\(d=13\) の格子点で点値がpin=2y+zに一致、
掃引行の1行手前にpinが出現するK1026のx=16と同型）で、cross-z監査logの
d格子法則どおり。x=19は偶数帯署名12がx+17まで続く移行行で、x≥20偶数/x≥21奇数で
署名帯は定常化する。両子K1026・K1024のverifyスクリプトはrepoに存在しCIで監査済み。
有限監査は二直接再帰・子アンカー・署名帯・mex等の転写を照合するもので、
証明そのものではない。

z≥14のy>=2（y=2はB子がK1023の全z・y=1全称公式・C子が1 xor K1025で着手可能）、
z=13のy>=5（B子は本項だがC子(12,5)が未出版）、y>=2族のパラメトリック機械化、
値1基底点のy点仮説の一般証明、標準二次元盤の固定幅・q点版安定化長は未解決。
