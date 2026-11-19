---
id: K1045
title: 2トークン残余ゲーム z=13・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z13 y5 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、一般tail、単一トークン閉形式を使用する
- type: depends_on
  target: K1027
  note: B子の評価にz=13・y=4境界切片を使用する
- type: depends_on
  target: K1043
  note: C子の評価に1 xor (z=12・y=5境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z13-y5-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z13-y5-boundary-20261119/verify_z13_y5.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、K1027/K1043子アンカー、署名帯・mex・低R縮約・tailの決定論的監査
- path: research/experiments/vertical-fiber-two-token-z13-y5-boundary-20261119/output/audit.json
  role: data
  note: 616,611照合・不一致0・同一実行内および別プロセス再実行でbyte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z13-y5-boundary.md
  role: log
  note: 最新main確認、K1044採番衝突回避、z=13,y=5切片の証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=13、y=5、
  全x>=5・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=5では二つの等しいトークンの減少手が同じ多重集合子
  (5,4);13に合流し、K1027を基底として使う。x>=6ではA子を帰納仮説、
  B子をK1027のz=13,y=4全称公式、C子を1 xor K1043のz=12,y=5全称公式
  で評価する。全R>=1のうち1<=R<=x+18はreport.mdの過渡行x=5..20と
  定常行x>=21奇数/x>=22偶数のA/B/C署名帯表が互いに素に被覆し、mex表から
  本文のT/Pが得られる。K0832からR<=14の高さのみ縮約とR>=x+19の一般tailも従う。
  独立監査は二直接再帰・K1027/K1043子アンカー・署名帯・mex・低R・tail・散点を
  含む616,611照合で不一致0、同一実行内2回および別プロセス再実行で
  audit.jsonがbyte-identical。有限監査は転写・実装照合であり、全称性は
  x外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge5\)、\(R\ge0\) について、\(H(R;(x,5);13)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le14\) で単一トークン
\(x+5\) へ縮約し、高残容量は \(R\ge x+19\) で \((x+5)\bmod2\) となる。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1027、C子はK1043の
全称定理であり、低R縮約・一般tailはK0832から従う。有限監査は二直接再帰・
子アンカー・署名帯・mex等の転写を照合するもので、証明そのものではない。

値1基底点は \(\{14,16,18,20,22\}=\{z+1,z+3,z+5,z+7,z+9\}\) で、y点仮説のy=5例。
pinは \(23=2y+z\) で奇数zラダー \(O[1,z]\) に載る。掃引行は \(x=z+y+1=19\)、
掃引帯は \(O[pin,x+y+z]=O[23,37]\)。h=z行x=8の上端17は
\(q_{\rm odd}(2y+(d+z)/2)=q_{\rm odd}(18)\) でd+z≡0 (mod 4)の例、前倒し点x=10,14,18は
同式でd+z≡2 (mod 4)の格子点である。z=13・y≥6、z≥14・y≥2、
2トークン族の全高さ一般式、値1基底点y点仮説・h=z孤立上端とpin前置の
d+z mod 4規則の一般証明、標準二次元盤の固定幅・q点版安定化長は未解決。
