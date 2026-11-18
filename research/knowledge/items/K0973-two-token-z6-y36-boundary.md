---
id: K0973
title: 2トークン残余ゲーム z=6・y=36切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y36 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C残余再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使う
- type: depends_on
  target: K0972
  note: B子とx=36境界のA子をz=6,y=35全Grundy公式で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y36-boundary-20261119/report.md
  role: proof
  note: z=6,y=36切片の全x,R分類、選択肢署名表、xに関する帰納証明
- path: research/experiments/vertical-fiber-two-token-z6-y36-boundary-20261119/verify_z6_y36.py
  role: verifier
  note: 順序付き・降順正準化の二方式直接再帰、y=35/z=5アンカー、全署名・mex・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y36-boundary-20261119/output/audit.json
  role: data
  note: 2,082,900署名・mex、5,208直接再帰呼び出し、5,355帰納再帰、123,795 tail検査、不一致0、二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-19-vertical-fiber-two-token-z6-y36-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=36切片の証明・監査・限界
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,36);6)の2トークン族、固定高さz=6、y=36、全x>=36・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する帰納。x=36ではA子の(35,36)が正準化後に(36,35)となりB子と一致する。x>=37ではA子をx-1の帰納仮説、B子をK0972、C子をK0873で評価する。1<=R<x+43の過渡署名表（x=36..44）と一般署名表（x>=45 odd / x>=46 even）で全選択肢を覆い、Theorem Tの偶奇制約とmexからT36/P36を得る。R>=x+43はK0832の一般tail定理H=(x+36) mod 2で閉じる。独立有限監査は順序付き・正準化直接再帰5,208呼び出し、A/B/C署名・mex各2,082,900件、帰納再帰5,355件、tail123,795件で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx帰納・署名表・既証明アンカーによる。
---
## 命題

全ての \(x\ge36,R\ge0\) について、Grundy値は証明報告の \(T_{36}(x)\) と \(P_{36}(x)\) により0/1/2へ完全分類される。tailは
\[
R\ge x+43\implies H(R;(x,36);6)=(x+36)\bmod2.
\]

\(y=26..36\) の11切片で値2の追加位置が同一の正規化形に一致する。ただし全 \(y\ge26\) への一般化は未証明である。

## 現在の根拠と限界

A/B/C再帰とx帰納。基底x=36ではAの(35,36)が正準化後にBの(36,35)と一致する。帰納段のBはK0972、CはK0873。過渡域x=36..44と一般域x>=45 odd / x>=46 evenの全署名表、K0832のTheorem T、一般tail定理で全x・全Rを覆う。有限監査は直接再帰5,208件、署名・mex各2,082,900件、tail123,795件で不一致0、二回実行byte-identical。有限監査は全称性の根拠ではなく、全称性はx帰納と明示署名表による。

z=6,y>=37、z>=7、全高さを統合する値2位置の一般式、標準二次元共円ゲームの固定幅・q点版の真の安定化長は未解決。
