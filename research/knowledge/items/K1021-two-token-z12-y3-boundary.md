---
id: K1021
title: 2トークン残余ゲーム z=12・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z12 y3 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、単一トークン全z閉形式、一般tail、Theorem Tを使用する
- type: depends_on
  target: K1019
  note: B子の評価にz=12,y=2の全称公式を使用する
- type: depends_on
  target: K1014
  note: C子の評価にz=11,y=3の全称公式を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z12-y3-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明・2026-11-19バックフィル補記つき
- path: research/experiments/vertical-fiber-two-token-z12-y3-boundary-20261119/verify_z12_y3.py
  role: verifier
  note: 順序保持・正準化の二直接再帰、子アンカー、署名帯・mex・縮約・tailの独立監査・2026-11-19バックフィル実装
- path: research/experiments/vertical-fiber-two-token-z12-y3-boundary-20261119/output/audit.json
  role: data
  note: バックフィル検証器の監査データ・13,955,311照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z12-y3-boundary.md
  role: log
  note: z=12,y=3切片の選定・証明・監査・次のy=4接続
- path: research/log/2026-11-19-vertical-fiber-two-token-z12-y3-verify-backfill.md
  role: log
  note: 欠落していたverify/audit成果物のバックフィル修復記録
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=12、y=3、
  全x>=3・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。A子は同じz=12,y=3のx-1行、B子はK1019のz=12,y=2全称公式、
  C子は1 xor K1014のz=11,y=3全称公式で評価する。x=3では同値トークンの
  減少手が同じ(3,2);12子に合流する。x=3..17の個別署名帯とx>=18の偶奇別
  署名帯が全R>=1を被覆し、各帯のmexがT/P閉形式を与える。定常値2位置は
  O[1,11]とpin=19=2y+z+1、掃引行はx=16=z+y+1で掃引帯O[19,31]。
  値1基底点は{13,15,17}、帯開始は20=z+2y+2、tailはR>=x+16で
  H=(x+3) mod 2、R<=13は高さのみ縮約v_single(x+3,12,R)。
  出版時の独立監査（323,643照合）は成果物が一度も公開されず検証不能のまま
  だったため、2026-11-19にreportの表と出版済み子閉形式から新規実装した
  検証器（13,955,311照合・不一致0・二回実行byte-identical）が有限監査の
  役割を引き継いだ。全称性の根拠は外帰納と署名帯表であり、有限監査自体ではない。
---

## 命題・範囲

K1021は抽象κ=1残余ゲームのz=12・y=3切片を全x>=3・全R>=0で分類する。
値2位置はx=3..16の過渡行を経て、x>=17でO[1,11]∪{19}に定着する。
値1位置の基底は{13,15,17}、中間帯は偶数位置20から始まり、tailは
R>=x+16で(x+3) mod 2。低RのR<=13は単一トークンへ縮約する。

## 現在の根拠と限界

全称性はx外帰納と全R署名帯表による。B子はK1019、C子はK1014の全称定理。
有限監査は二直接再帰・子アンカー・署名帯の転写を照合するもので、証明そのものではない。
2026-11-19に、CI監査stepが参照するverify_z12_y3.pyとoutput/audit.jsonが
一度もpublishされていないままだったことが判明したため、reportの閉形式・
署名帯・mex表とK1019/K1014の出版閉形式から検証器を新規実装してバックフィルし、
13,955,311照合・不一致0で監査役割を復元した。
z=12のy>=4、z>=13のy一般、標準二次元盤の固定幅・q点安定化長は未解決。
次のz=12,y=4はB=K1021・C=1 xor K1015で着手できる。
