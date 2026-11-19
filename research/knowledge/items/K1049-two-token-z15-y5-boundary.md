---
id: K1049
title: 2トークン残余ゲーム z=15・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z15 y5 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1048
  note: B子の評価にz=15・y=4境界切片を使用する
- type: depends_on
  target: K1047
  note: C子の評価に1 xor (z=14・y=5境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z15-y5-boundary-20261120/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z15-y5-boundary-20261120/verify_z15_y5.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、K1048/K1047子アンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z15-y5-boundary-20261120/output/audit.json
  role: data
  note: 4,153,734照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/log/2026-11-20-vertical-fiber-two-token-z15-y5-boundary.md
  role: log
  note: 最新main確認、未解決範囲との照合、証明・監査・次の課題
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=15、y=5、
  全x>=5・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=5では二つの等しいトークンの減少手が同じ(5,4);15
  多重集合子に合流し、K1048のx=5行を基底として使う。x>=6ではA子を帰納仮説、
  B子をK1048（z=15,y=4）、C子を1 xor K1047（z=14,y=5）で評価する。
  全R>=1のうち1<=R<=x+20はreport.mdの過渡行x=5..22と定常行x>=23奇数・
  x>=24偶数のA/B/C署名帯表が互いに素に被覆し、mex表から本文のT/Pが得られる。
  K0832からR<=16の高さのみ縮約とR>=x+21の一般tailも従う。独立監査は二直接再帰、
  子アンカー、署名帯、mex、低R、tail、散点を含む4,153,734照合で不一致0、
  二回実行byte-identical。有限監査は転写・実装照合であり、全称性はx外帰納と
  全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge5\)、\(R\ge0\) について、\(H(R;(x,5);15)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le16\) で単一トークン
\(x+5\) へ縮約し、高残容量は \(R\ge x+21\) で \((x+5)\bmod2\) となる。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1048、C子はK1047の
全称定理であり、低R縮約・一般tailはK0832から従う。有限監査は二直接再帰・
子アンカー・署名帯・mex等の転写を照合するもので、証明そのものではない。

x≥18で値1基底点は \(\{16,18,20,22,24\}=\{z+1,z+3,z+5,z+7,z+9\}\) となり、y=5点型の
全称実例。pinは \(25=2y+z\)、掃引行は \(x=z+y+1=21\)、掃引帯は
\(O[25,41]\)。前倒し点21,23,25は \(d+z\equiv2\pmod4\) の格子式
\(2y+(d+z)/2\) に一致し、h=z行x=10の上端19はq_odd型。
z=15・y>=6はB子K1049、C子1 xor K1062で一様化に着手可能。z=14・y>=6はK1062で全称証明済み。z>=16・y>=2（z=16・y=3はK1050で、z=18・y=2はK1051で、z=19・y=2はK1052で、z=20・y=2はK1053で、z=21・y=2はK1054で解決）、値1基底点y点仮説の一般証明、
d+z剰余格子の一般証明、標準二次元盤の固定幅・q点版安定化長は未解決。
