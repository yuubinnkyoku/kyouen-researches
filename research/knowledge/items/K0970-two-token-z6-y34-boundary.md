---
id: K0970
title: 2トークン残余ゲーム z=6・y=34切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y34 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C残余再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使う
- type: depends_on
  target: K0967
  note: B子とx=34境界のA子をz=6,y=33全Grundy公式で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y34-boundary-20261118/report.md
  role: proof
  note: z=6,y=34切片の全x,R分類、選択肢署名表、xに関する帰納証明
- path: research/experiments/vertical-fiber-two-token-z6-y34-boundary-20261118/verify_z6_y34.py
  role: verifier
  note: 順序付き・降順正準化の二方式直接再帰、y=33/z=5アンカー、全署名・mex・tailの独立監査。SHA-256 3edce940…
- path: research/experiments/vertical-fiber-two-token-z6-y34-boundary-20261118/output/audit.json
  role: data
  note: 2,079,119署名・mex、4,872直接再帰呼び出し、5,311帰納再帰、125,888 tail検査、不一致0、二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-18-vertical-fiber-two-token-z6-y34-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=34切片の証明・監査・限界
date: 2026-11-18
scope: >-
  κ=1残余ゲームH(R;(x,34);6)の2トークン族、固定高さz=6、y=34、全x≥34・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する帰納。x=34ではA子の(33,34)が正準化後に(34,33)となりB子と一致する。x≥35ではA子をx-1の帰納仮説、B子をK0967、C子をK0873で評価する。1≤R<x+41の過渡署名表（x=34..42）と一般署名表（x≥43）で全選択肢を覆い、Theorem Tの偶奇制約とmexからT34/P34を得る。R≥x+41はK0832の一般tail定理H=(x+34) mod 2で閉じる。独立有限監査は順序付き・正準化直接再帰4,872呼び出し、A/B/C署名・mex各2,079,119件、帰納再帰5,311件、tail125,888件で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx帰納・署名表・既証明アンカーによる。
---
