---
id: K0942
title: 2トークン残余ゲーム z=6・y=28切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y28 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C残余再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0940
  note: B子とx=28境界のA子をz=6,y=27全Grundy公式で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y28-boundary-20261118/report.md
  role: proof
  note: z=6,y=28切片の全x,R分類、選択肢署名表、xに関する帰納証明
- path: research/experiments/vertical-fiber-two-token-z6-y28-boundary-20261118/verify_z6_y28.py
  role: verifier
  note: 順序付き・降順正準化の二方式直接再帰、y=27/z=5アンカー、全署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y28-boundary-20261118/output/audit.json
  role: data
  note: 6,355,952検査・不一致0・二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-18-vertical-fiber-two-token-z6-y28-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=28切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,28);6)の2トークン族、固定高さz=6、y=28、全x≥28・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する帰納。x=28ではA子の(27,28)が正準化後にK0940の(28,27)となりB子と一致する。x≥29ではA子をx-1の帰納仮説、B子をK0940、C子をK0873で評価する。x=28..36の過渡署名表とx≥37 odd/x≥38 evenの一般署名表で1≤R<x+35を全て覆い、R≥x+35はK0832の一般tail定理H=(x+28) mod 2で閉じる。K0832のTheorem Tとも整合する。独立有限監査は6,355,952検査で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx帰納・署名表・一般tail定理による。
---
