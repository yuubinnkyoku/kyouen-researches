---
id: K1022
title: 2トークン残余ゲームy=1族パラメトリック閉形式の全称定理（z>=6）
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token y1 parametric universal z >= 6]
relations:
- type: depends_on
  target: K0877
  note: 帰納の基底ケースとしてz=6・y=1境界切片の全称定理を使用する
- type: depends_on
  target: K0832
  note: closure子B（単一トークンz+1公式）の評価に単一トークン閉形式を使用する
- type: generalizes
  target: K0977
  note: z=7・y=1境界切片は本定理の特殊例
- type: generalizes
  target: K0983
  note: z=8・y=1境界切片は本定理の特殊例
- type: generalizes
  target: K0985
  note: z=9・y=1境界切片は本定理の特殊例
- type: generalizes
  target: K1003
  note: z=10・y=1境界切片は本定理の特殊例
- type: generalizes
  target: K1012
  note: z=11・y=1境界切片は本定理の特殊例
- type: generalizes
  target: K1016
  note: z=12・y=1境界切片は本定理の特殊例
- type: generalizes
  target: K1017
  note: z=13・y=1境界切片は本定理の特殊例
- type: generalizes
  target: K1018
  note: z=14・y=1境界切片は本定理の特殊例
- type: generalizes
  target: K1020
  note: z=15・y=1境界切片は本定理の特殊例
artifacts:
- path: research/experiments/vertical-fiber-two-token-y1-parametric-proof-20261119/report.md
  role: proof
  note: closure恒等式の帰納構造と21行クラスによる全称化、V0..V7検証器構成
- path: research/experiments/vertical-fiber-two-token-y1-parametric-proof-20261119/verify_y1_parametric_proof.py
  role: verifier
  note: 二直接再帰・出版切片verbatim埋め込み・closure掃引・シンボリック帯監査・partition・決定論audit出力の単一自己完結検証器
- path: research/experiments/vertical-fiber-two-token-y1-parametric-proof-20261119/output/audit.json
  role: data
  note: V0..V6合計21,718,500照合・不一致0・21クラス監査記録・再直列化byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-y1-parametric-proof.md
  role: log
  note: 予想から全称証明への経路の記録
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族におけるy=1・全z>=6・全x>=1・全R>=0。
  センサス仮説P1のうちz>=6の全称部分を閉じる。
evidence: >-
  z外帰納（C子=z-1切片）とx内帰納（A子=同切片x-1行）の二重帰納による。
  z>=7の全(x,R)でclosure恒等式cand(z,x,R)=mex{A=cand(z,x-1,R-1),
  B=single_token(x,z+1,R-1), C=1 xor cand(z-1,x,R-1)}が成立すれば、
  基底z=6（K0877）とB子K0832から定理が閉じる。closure恒等式の全称化は
  21行クラス（族E: 偶数z>=8の10類、族O: 奇数z>=7の11類、x>=1を隙間なく
  分割・機械点検6,179点失敗0）上のシンボリック帯表で行う。各クラスで
  F0/FA/FB/FC四関数の帯端点は(z,m)または(z,k)の一次形式であり、
  ペア傾き構造（傾き種z/m/k）の安定箱上でflip点配置のpattern（順序と
  隣接類{1,>=2}）が一定であることを監査し、サンプル点のsym-eval
  （帯表==コード式、全Rをmaxflip+8まで、計21,394R値）とクロスサンプル
  （同箱のpattern一致点間でセグメント×R偶奇ごとの四関数値と closure
  verdict の直接照合、計1,072 representative）により、不安定帯
  （z-kind: z<=6、m-kind: x<=2、k-kind: z+k<=11で機械確認済み、
  全てV3掃引箱z<=120・x<=4z+240の内部）を除く全ボックスで恒等式が
  成立することを確定する。検証器は単一自己完結ファイルで、出版
  z=6..15切片検証スクリプトをast機械抽出でverbatim埋め込み、
  V0 単一トークン59,568点、V1 両再帰センサス203,910点（z=1..30 Finite）、
  V2 出版切片照合850,000点、V3 closure掃引19,615,182点、V4 
  raw∧closure∧cand一致44,015点、V6 height-only有限945,825点、
  V7 audit.json再直列化byte-identical、全体約50秒で全段階PASS。
---

## 命題・範囲

K1022は2トークン残余ゲームのy=1族について、センサス（vertical-fiber-two-token-y1-parametric-census-20261119）で提案されたパラメトリック閉形式cand(z,x,R)が、全z>=6・全x>=1・全R>=0でH(R;(x,1);z)に一致することを全称証明する。閉形式の値2位置・値1位置の行表はセンサスreportの偶数z/奇数z表の通り（値2ラダー偶数zはz-1、奇数zはzが上端、ピン=z+2y+[z偶]、掃引行x=z+2、tailはR>=x+z+2でH=(x+1) mod 2、R<=z+1はheight-only縮約single_token(x+1,z,R)）。z=6..15の出版切片定理（K0877, K0977, K0983, K0985, K1003, K1012, K1016, K1017, K1018, K1020）とz=16切片はこの定理の系であり、出版センサスのz=17..60行も含め全z>=6が一本の式で確定する。

## 現在の根拠と限界

全称性の根拠は二重帰納とclosure恒等式の全称化である。z>=7で切片の値がどのx行でも三子A（同z・x-1行）、B（K0832単一トークンz+1）、C（1 xor z-1切片）で尽くされることは手の定義から従属し（x=1では二つの減少手が同一の子に合流）、したがってclosure恒等式の全称成立とz=6基底・K0832から全z>=6が従属する。closure恒等式は21行クラスのシンボリック帯表・ペア傾き種・pattern安定性・不安定帯の算術包含と、ボックスサンプルでのsym-eval・クロスサンプルanchor照合（共にclosure verdictを含む）で機械監査し、V3では具体的にz=7..120・x<=4z+240・R<=x+z+10の19,615,182点で恒等式を直接掃引した。出版切片スクリプトはV2で850,000点そこ検証式と照合し（astによるverbatim抽出、手転写なし）、V4でz=7..16に両直接再帰を併合した。限界として、z=1..5は有限センサスのみで本定理には含まれない（closure帯の安定性議論はz>=6の構造を仮定する）、y>=2族のパラメトリック化は未解決、height-only縮約R<=z+1則はz=6..80への有限拡大にとどまり一般証明は未解決、標準二次元盤の固定幅・q点安定化長は未解決である。
