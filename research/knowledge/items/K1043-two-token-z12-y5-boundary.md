---
id: K1043
title: 2トークン残余ゲーム z=12・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z12 y5 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1024
  note: B子の評価にz=12・y=4境界切片を使用する
- type: depends_on
  target: K1037
  note: C子の評価にz=11・y=5境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z12-y5-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z12-y5-boundary-20261119/verify_z12_y5.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、K1024/K1037アンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z12-y5-boundary-20261119/output/audit.json
  role: data
  note: 5,413,820照合・不一致0・別プロセス別cwd二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z12-y5-boundary-20261119/census_z12_y5.py
  role: verifier
  note: x=5..45の生二再帰行表・閉形式・tailの第三導出センサス（二回実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-z12-y5-boundary-20261119/output/census.txt
  role: data
  note: センサス行表（x=5..45・R=0..x+45・tail R=x+18..x+21）
- path: research/log/2026-11-19-vertical-fiber-two-token-z12-y5-boundary.md
  role: log
  note: 最新main確認、z=12 y=5切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=12、y=5、
  全x>=5・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=5では二つのトークン減少手が同じ多重集合子
  (5,4);12に合流し、K1024を基底として使う。x>=6ではA子を帰納仮説、
  B子をK1024のz=12,y=4全称公式、C子を1 xor K1037のz=11,y=5全称公式
  で評価する。全R>=1はreport.mdの過渡行x=5..19と定常行x>=20偶数/
  x>=21奇数のA/B/C署名帯表が互いに素に被覆し、mex表から本文のT/Pが
  得られる。K0832からR<=13の高さのみ縮約とR>=x+18の一般tailも従う。
  独立監査は順序保持・降順正準化の二直接再帰、K1024/K1037子アンカー、
  署名帯、mex、Theorem T、縮約、tail、固定seed散点、深行は閉形式子
  アンカー署名を含む5,413,820照合で不一致0、別プロセス別cwdで二回実行
  byte-identical、生二再帰センサスx=5..45でも行表・閉形式・tailが一致。
  有限監査は転写・実装照合であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge5\)、\(R\ge0\) について、\(H(R;(x,5);12)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le13\) で単一トークン
\(x+5\) へ縮約し、高残容量は \(R\ge x+18\) で \((x+5)\bmod2\) となる。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1024、C子はK1037の
全称定理であり、低R縮約・一般tail・Theorem TはK0832から従う。
有限監査は二直接再帰・子アンカー・署名帯・mex等の転写を照合するもので、
証明そのものではない。

値1基底点\{13,15,17,19,21\}=\{z+1,...,z+9\}はy点仮説の第6実例（5点型の
偶数z初例）、pin=23=2y+z+1は偶数zラダーO[1,z-1]に載り掃引行x=z+y+1と
一致、h=z行x=7の孤立上端17=2y+(d+z)/2（d=2・d+z≡2 (mod 4)）は
d+z mod 4二値規則のy=5・偶数z初例である。z=12のy>=6はK1056で一様全称分類済み。z=13のy>=6はB子K1045・C子K1056が揃い着手可能。全高さを統合する2トークン一般式、値1基底点y点仮説・h=z孤立上端d+z mod 4二値規則の一般証明、標準二次元盤の固定幅・q点版安定化長は未解決。
