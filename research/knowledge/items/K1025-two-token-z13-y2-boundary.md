---
id: K1025
title: 2トークン残余ゲーム z=13・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z13 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1017
  note: B子の評価にz=13・y=1境界切片を使用する
- type: depends_on
  target: K1019
  note: C子の評価にz=12・y=2境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z13-y2-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z13-y2-boundary-20261119/verify_z13_y2.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z13-y2-boundary-20261119/output/audit.json
  role: data
  note: 13,806,285照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z13-y2-boundary-20261119/census_z13_y2.py
  role: verifier
  note: x=2..45・R=0..x+45の生二再帰センサスで report の行表・tail を独立照合する
- path: research/experiments/vertical-fiber-two-token-z13-y2-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z13-y2-boundary.md
  role: log
  note: 最新main確認、y=2切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=13、y=2、
  全x>=2・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=2では二つのトークン減少手が同じ(2,1);13子に合流し、
  K1017のx=2行を基底として使う。x>=3ではA子を帰納仮説、B子をK1017の
  z=13,y=1全称公式、C子を1 xor K1019のz=12,y=2全称公式で評価する。
  全R>=1はreport.mdの過渡行x=2..17と定常行x>=18偶数/x>=19奇数の
  A/B/C署名帯表が互いに素に被覆し、mex表から本文のT/Pが得られる。
  K0832からR<=14の高さのみ縮約とR>=x+16の一般tailも従う。
  独立監査は順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯、
  mex、Theorem T、縮約、tail、散点を含む13,806,285照合で不一致0、
  二回実行byte-identical。有限監査は転写・実装照合であり、全称性は
  x外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge2\)、\(R\ge0\) について、\(H(R;(x,2);13)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le14\) で単一トークン
\(x+2\) へ縮約し、高残容量は \(R\ge x+16\) で \((x+2)\bmod2\) となる。

値2位置は x=2 で \(\{1,3\}\)、x=3,4 で O[1,5]、x=5,6 で O[1,7]、
x=7,8 で O[1,9]、x=9,10 で O[1,11]、x=11 で O[1,15]（前倒し点15）、
x=12..14 で O[1,13]、x=15 で O[1,13]∪\{17\}（前倒し点17）、
x=16 の掃引行で O[1,13]∪O[17,31]、x≥17 で
\(\{1,3,5,7,9,11,13,17\}\)（pin=17=2y+z・奇数zラダーO[1,z]）に定着する。
値1位置は偶数x≤10で空、x∈{3,5,7,9} で I[x+3,∞)、x=11,13 で
\(\{14\}\cup I[16,\infty)\)、x=12 で \(\{14\}\)、x=14,16 で \(\{14,16\}\)、
x=15 で \(\{14,16\}\cup I[18,\infty)\)、奇数x≥17 で
\(\{14,16\}\cup O[19,x+15]\cup I[x+16,\infty)\)、偶数x≥18 で
\(\{14,16\}\cup O[19,x+15]\)。値1基底点は \(\{14,16\}=\{z+1,z+3\}\)、
中間帯は z+2y+2=19 から始まる。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1017、C子はK1019の
全称定理であり、低R縮約・一般tail・Theorem TはK0832から従う。
前倒し点x=11の15とx=15の17はd格子点 \(2y+(d+z)/2\)（\(d+z\equiv2\pmod4\)）で、
cross-z監査logのd格子法則どおり。有限監査は二直接再帰・子アンカー・署名帯・
mex等の転写を照合するもので、証明そのものではない。

z=13のy>=3、z>=14のy>=2、全高さを統合する2トークン一般式、
標準二次元盤の固定幅・q点版安定化長は未解決。
