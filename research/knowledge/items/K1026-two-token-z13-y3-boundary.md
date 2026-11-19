---
id: K1026
title: 2トークン残余ゲーム z=13・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z13 y3 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1025
  note: B子の評価にz=13・y=2境界切片を使用する
- type: depends_on
  target: K1021
  note: C子の評価にz=12・y=3境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z13-y3-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z13-y3-boundary-20261119/verify_z13_y3.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z13-y3-boundary-20261119/output/audit.json
  role: data
  note: 13,811,937照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z13-y3-boundary-20261119/census_z13_y3.py
  role: verifier
  note: x=3..45・R=0..x+45の生二再帰センサスで report の行表・tail を独立照合する
- path: research/experiments/vertical-fiber-two-token-z13-y3-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z13-y3-boundary.md
  role: log
  note: 最新main確認、y=3切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=13、y=3、
  全x>=3・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=3では二つのトークン減少手が同じ(2,3);13子に合流し、
  K1025のx=3行（(2,3)≡(3,2)の対称性）を基底として使う。x>=4では
  A子を帰納仮説、B子をK1025のz=13,y=2全称公式、C子を1 xor K1021の
  z=12,y=3全称公式で評価する。全R>=1はreport.mdの過渡行x=3..18と
  定常行x>=19奇数/x>=20偶数のA/B/C署名帯表が互いに素に被覆し、
  mex表から本文のT/Pが得られる。K0832からR<=14の高さのみ縮約と
  R>=x+17の一般tailも従う。独立監査は順序保持・降順正準化の二直接再帰、
  B/Cアンカー、署名帯、mex、Theorem T、縮約、tail、散点を含む
  13,811,937照合で不一致0、二回実行byte-identical。有限監査は転写・
  実装照合であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \\(x\\ge3\\)、\\(R\\ge0\\) について、\\(H(R;(x,3);13)\\) のGrundy値0/1/2を
report.mdの \\(T(x),P(x)\\) で完全分類する。低残容量は \\(R\\le14\\) で単一トークン
\\(x+3\\) へ縮約し、高残容量は \\(R\\ge x+17\\) で \\((x+3)\\bmod2\\) となる。

値2位置はx=3で \\(\\{1,3,5\\}\\)、x=4,5でO[1,7]、x=6,7でO[1,9]、x=8,9でO[1,11]、
x=10（高さx+y=z行）でO[1,15]、x=11でO[1,13]、x=12でO[1,13]∪\\{17\\}（前倒し点17）、
x=13,14,15でO[1,13]、x=16でO[1,13]∪\\{19\\}（前倒し点19=pin）、
x=17の掃引行でO[1,13]∪O[19,33]、x≥18でO[1,13]∪\\{19\\}に定着する
（pin=19=2y+z・奇数zラダーO[1,z]）。
値1位置は奇数x≤9で空、x∈{4,6,8}でI[x+4,∞)、x=10で\\(\\{14\\}\\cup I[16,\\infty)\\)、
x=11,13で\\(\\{14,16\\}\\)、x=12,14で\\(\\{14,16\\}\\cup I[18,\\infty)\\)、
x=15,17で\\(\\{14,16,18\\}\\)、x=16で\\(\\{14,16,18\\}\\cup I[20,\\infty)\\)、
偶数x≥18で\\(\\{14,16,18\\}\\cup O[21,x+15]\\cup I[x+17,\\infty)\\)、
奇数x≥19で\\(\\{14,16,18\\}\\cup O[21,x+16]\\)。値1基底点は \\(\\{14,16,18\\}=\\{z+1,z+3,z+5\\}\\)
（y=1で1点・y=2で2点に続きy個の仮説の3例目）、中間帯は z+2y+2=21 から偶奇z追従の奇数帯、
無限I帯は偶数x行のみでtail R≥x+17の値 \\((x+3)\\bmod2\\) と一致する。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1025、C子はK1021の
全称定理であり、低R縮約・一般tail・Theorem TはK0832から従う。
前倒し点はx=12の17（d格子点 \\(2y+(d+z)/2\\)、\\(d=9=x-y\\)、\\(d+z\\equiv2\\pmod4\\)）と
x=16の19（\\(d=13\\) の格子点で点値がpin=2y+zに一致、掃引行の1行手前にpinが
出現するK1017のx=14・K1025のx=15と同型）で、cross-z監査logのd格子法則どおり。
有限監査は二直接再帰・子アンカー・署名帯・mex等の転写を照合するもので、
証明そのものではない。なおC子K1021のrepo上のverify_z12_y3.pyは押し込み漏れで
存在しないが、本項のderive工程でK1021 report.mdの閉形式転写を第二の生再帰
エンジンで全照合し0不一致を確認済みであり、定理の数学的内容に影響しない。

z=13のy>=4、z>=14のy>=2、y>=2族のパラメトリック機械化、
標準二次元盤の固定幅・q点版安定化長は未解決。
