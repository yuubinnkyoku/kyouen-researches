---
id: K0947
title: 2トークン残余ゲーム z=6・y=30切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y30 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C残余再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0944
  note: B子とx=30境界のA子をz=6,y=29全Grundy公式で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y30-boundary-20261118/report.md
  role: proof
  note: z=6,y=30切片の全x,R分類、選択肢署名表、xに関する帰納証明
- path: research/experiments/vertical-fiber-two-token-z6-y30-boundary-20261118/verify_z6_y30.py
  role: verifier
  note: 順序付き・降順正準化の二方式直接再帰、y=29/z=5アンカー、全署名・mex・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y30-boundary-20261118/output/audit.json
  role: data
  note: 6,382,085検査・不一致0・二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-18-vertical-fiber-two-token-z6-y30-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=30切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,30);6)の2トークン族、固定高さz=6、y=30、全x≥30・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する帰納。x=30ではA子の(29,30)が正準化後にK0944の(30,29)となりB子と一致する。x≥31ではA子をx-1の帰納仮説、B子をK0944、C子をK0873で評価する。1≤R<x+37の過渡署名表（x=30..38）と一般署名表（x≥39 odd/x≥40 even）で全選択肢を覆い、mexからT30/P30を得る。R≥x+37はK0832の一般tail定理H=x mod 2で閉じる。独立有限監査は6,382,085検査で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx帰納・署名表・既証明アンカーによる。
---

## 命題・範囲

全ての整数x≥30,R≥0について、Grundy値はT30/P30で完全分類される。値2位置は
\[
T_{30}(x)=\{1,3,5\}\cup
\begin{cases}
\{63\}&x=30,\\
\{65\}&x=34,\\
\{67,69,71,73\}&x=37,\\
\{67\}&x\ge38,\\
\varnothing&x\in\{31,32,33,35,36\}.
\end{cases}
\]
値1位置は証明報告のP30式のとおりであり、tailはR≥x+37でx mod 2。

## 現在の根拠と限界

A/B/C再帰とx帰納。基底x=30はA=Bの正準化合流によりK0944へ接続する。帰納段のBはK0944、CはK0873。過渡域x=30..38と一般域x≥39 odd/x≥40 evenの全署名表、K0832のTheorem T、一般tail定理で全x・全Rを覆う。有限監査は6,382,085検査・不一致0・二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx帰納・署名表・既証明アンカーによる。

y=26..34の9切片では値2の追加位置が同じ正規化形に一致するが、全y≥26への一般化は未証明。z=6,y≥35、z≥7、全高さを統合する値2位置の一般式、標準二次元共円ゲームの固定幅・q点安定化長は未解決。