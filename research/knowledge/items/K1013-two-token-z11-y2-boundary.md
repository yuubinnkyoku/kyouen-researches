---
id: K1013
title: 2トークン残余ゲーム z=11・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z11 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 一般tail、Theorem T、高さのみ縮約、単一トークン全z公式を使用する
- type: depends_on
  target: K1012
  note: B子の評価にz=11,y=1境界切片を使用する
- type: depends_on
  target: K1004
  note: C子の評価にz=10,y=2境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z11-y2-boundary-20261119/report.md
  role: proof
  note: x外帰納と全R署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z11-y2-boundary-20261119/verify_z11_y2.py
  role: verifier
  note: 順序保持・正準化直接再帰、A/B/Cアンカー、署名帯・mex・高さのみ縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z11-y2-boundary-20261119/output/audit.json
  role: data
  note: 27,672,638比較点・不一致0・二回実行と独立プロセス再実行でbyte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z11-y2-boundary.md
  role: log
  note: z=11,y=2切片の選定・証明・監査・次のy=3接続
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=11、y=2、全x>=2・全R>=0。
  Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x>=3ではA子を帰納仮説、B子をK1012のz=11,y=1公式、C子をK1004の
  z=10,y=2公式で評価する。x=2では2つのトークン減少手が同一の(2,1);11子に合流する。
  x=2..14の個別署名帯とx>=16偶/x>=15奇の定常署名帯で全R>=1を被覆し、Theorem Tの
  mex規則で閉じる。R<=12は高さのみ縮約でv_single(x+2,11,R)に一致し、tailはR>=x+14で
  H=(x+2) mod 2。独立有限監査は27,672,638比較点・不一致0であり、全称性の根拠は
  外帰納と署名帯表である。
---

## 命題・範囲

K1013は抽象残余ゲームのz=11・y=2切片を全x>=2・全R>=0で分類する。値2位置はx=2..8で高さのみ縮約ラダー{1,3}/{1,3,5}/{1,3,5,7}/{1,3,5,7,9}、x=9（高さx+y=z行）で{1,3,5,7,9,11,13}（追加点13）、x∈{10,11,12}で{1,3,5,7,9,11}、x=13で{1,3,5,7,9,11,15}、x=14（掃引行x=z+y+1）で{1,3,5,7,9,11}∪O[15,27]、x>=15で{1,3,5,7,9,11,15}に定着する。値1位置はx∈{2,4,6,8}で空、x∈{3,5,7}でI[6,∞)/I[8,∞)/I[10,∞)、基底点{12,13,14}={z+1,…,z+2y−1}、x∈{9,11}で{12,14}∪I[15,∞)、x=10で{12}、x=12で{12,14}、x=13で{12,14}∪I[16,∞)、x=14で{12,14}、x>=16偶数で{12,14}∪O[17,x+13]、x>=15奇数で{12,14}∪O[17,x+12]∪I[x+14,∞)。tailはR>=x+14で(x+2) mod 2。R<=12は高さのみ縮約v_single(x+2,11,R)に一致する。掃引帯はO[15,27]=O[pin,x+y+z]（pin=2y+z=15、z奇数）で、帯開始はz+2y+2=17（偶奇はzの偶奇=O帯）。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1012のz=11,y=1全称定理、C子はK1004のz=10,y=2全称定理。監査は二つの直接再帰、子アンカー、署名帯、mex、高さのみ縮約、tailを有限範囲で照合するもので、全称証明そのものではない。z=11のy>=3、z>=12の一般分類、zやyをまたぐ2トークン一般式、標準二次元盤の固定幅・q点版安定化長は未解決。次のy=3切片はB=K1013・C=K1005（z=10,y=3）で着手できる。
