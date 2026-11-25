---
id: K1037
title: 2トークン残余ゲーム z=11・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z11 y5 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1015
  note: B子の評価にz=11・y=4境界切片を使用する
- type: depends_on
  target: K1007
  note: C子の評価にz=10・y=5境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z11-y5-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z11-y5-boundary-20261119/verify_z11_y5.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、B/Cアンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z11-y5-boundary-20261119/output/audit.json
  role: data
  note: 5,406,960照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z11-y5-boundary-20261119/census_z11_y5.py
  role: verifier
  note: x=5..45の生二再帰行表・閉形式・tailの第三導出センサス（二回実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-z11-y5-boundary-20261119/output/census.txt
  role: data
  note: センサス行表（x=5..45・R=0..x+45・tail R=x+17..x+20）
- path: research/log/2026-11-19-vertical-fiber-two-token-z11-y5-boundary.md
  role: log
  note: 最新main確認、y=5切片の選定・証明・監査・次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=11、y=5、
  全x>=5・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=5では二つのトークン減少手が同じ多重集合子
  (5,4);11に合流し、K1015を基底として使う。x>=6ではA子を帰納仮説、
  B子をK1015のz=11,y=4全称公式、C子を1 xor K1007のz=10,y=5全称公式
  で評価する。全R>=1はreport.mdの過渡行x=5..18と定常行x>=19奇数/
  x>=20偶数のA/B/C署名帯表が互いに素に被覆し、mex表から本文のT/Pが
  得られる。K0832からR<=12の高さのみ縮約とR>=x+17の一般tailも従う。
  独立監査は順序保持・降順正準化の二直接再帰、K1015/K1007子アンカー、
  署名帯、mex、Theorem T、縮約、tail、固定seed散点、深行は閉形式子
  アンカー署名を含む5,406,960照合で不一致0、二回実行byte-identical、
  生二再帰センサスx=5..45でも行表・閉形式・tailが一致。有限監査は
  転写・実装照合であり、全称性はx外帰納と全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge5\)、\(R\ge0\) について、\(H(R;(x,5);11)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le12\) で単一トークン
\(x+5\) へ縮約し、高残容量は \(R\ge x+17\) で \((x+5)\bmod2\) となる。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1015、C子はK1007の
全称定理であり、低R縮約・一般tail・Theorem TはK0832から従う。
有限監査は二直接再帰・子アンカー・署名帯・mex等の転写を照合するもので、
証明そのものではない。

z=12のy=5はB子K1024・C子1⊕本項で、z=11のy=6はB子本項・C子1⊕K1008で、
いずれも着手可能になった。全高さを統合する2トークン一般式、値1基底点の
y点仮説の一般証明、h=z孤立上端のd+z mod 4二値規則の一般証明、
標準二次元盤の固定幅・q点版安定化長は未解決。
