---
id: K0955
title: 2トークン残余ゲーム z=6・y=32切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y32 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C残余再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使う
- type: depends_on
  target: K0953
  note: B子とx=32境界のA子をz=6,y=31全Grundy公式で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y32-boundary-20261118/report.md
  role: proof
  note: z=6,y=32切片の全x,R分類、選択肢署名表、xに関する帰納証明
- path: research/experiments/vertical-fiber-two-token-z6-y32-boundary-20261118/verify_z6_y32.py
  role: verifier
  note: 順序付き・降順正準化の二方式直接再帰、y=31/z=5アンカー、全署名・mex・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y32-boundary-20261118/output/audit.json
  role: data
  note: 署名・mex各2,075,326件、直接再帰16,878件、tail126,016件、不一致0、二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-18-vertical-fiber-two-token-z6-y32-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=32切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,32);6)の2トークン族、固定高さz=6、y=32、全x≥32・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する帰納。x=32ではA子の(31,32)が正準化後に(32,31)となりB子と一致する。x≥33ではA子をx-1の帰納仮説、B子をK0953、C子をK0873で評価する。1≤R<x+39の過渡署名表（x=32..40）と一般署名表（x≥41 odd/x≥42 even）で全選択肢を覆い、Theorem Tの偶奇制約とmexからT32/P32を得る。R≥x+39はK0832の一般tail定理H=(x+32) mod 2で閉じる。独立有限監査は直接再帰16,878件、署名・mex各2,075,326件、tail126,016件で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx帰納・署名表・既証明アンカーによる。
