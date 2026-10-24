---
id: K0533
title: λ=0の任意w列盤は最良一様候補数閾値で全Grundy値が高々2の閉公式を持つ
kind: proposition
status: proved
topics: [variants, geometry, grundy, rectangles, maximal-safe, first-moves]
aliases: []
relations:
- type: depends_on
  target: K0532
  note: 二次形式行列式規則とλ=0の退化の扱い
- type: depends_on
  target: K0002
  note: 終局までの固定手数偶奇とmex帰納
artifacts:
- path: research/experiments/quadratic-lambda-zero-strips-20261024/proof.md
  role: proof
  note: 三点補間による上界、全Grundy分類、整数点反例による閾値の全幅最良性
- path: research/experiments/quadratic-lambda-zero-strips-20261024/verify.py
  role: verifier
  note: 18盤の二方式mex検査と小盤Python照合の実行器
- path: research/experiments/quadratic-lambda-zero-strips-20261024/audit.cpp
  role: verifier
  note: 三点補完を増分伝播する全到達局面の再帰mex
- path: research/experiments/quadratic-lambda-zero-strips-20261024/column_audit.cpp
  role: verifier
  note: 列パターン列挙と安全局面集合への所属による独立DP
- path: research/experiments/quadratic-lambda-zero-strips-20261024/results.json
  role: data
  note: 延べ3972161局面。一般候補数条件内3384859局面で公式不一致0
- path: research/experiments/quadratic-lambda-zero-strips-20261024/sharpness.py
  role: verifier
  note: 最良性構成を整数座標化し安全性と極大性を独立行列式で検査
- path: research/experiments/quadratic-lambda-zero-strips-20261024/sharpness.json
  role: data
  note: w=4..10の整数反例と標準5×5の明示終局
scope: w≥3本の相異なる実数x座標上の任意有限実数候補点集合、各列M_w点以上。四点のdet[x²,x,y,1]=0を禁止する通常プレイの全安全局面。
evidence: 補間・列占有数による全称証明。任意wの有限多項式回避構成で一様閾値の最良性を証明。有限監査は証明とは区別する。
---

# λ=0列盤の最良一様閾値と全Grundy閉公式

`M_w=max(3,1+(w−2)(w−3)(w+2)/6)` とする。
相異なるw≥3本の鉛直列が、それぞれ任意の相異なる候補高さをM_w個以上持つなら、
極大安全集合は一列三石かw+1石に限られる。全安全局面で

- w偶数：`g(S)=(1−|S|) mod2`。
- w奇数：同じ一列の二石なら2、同じ一列の三石なら0、その他は `|S| mod2`。

従ってg≤2で、空盤は偶数wで先手必勝、奇数wで後手必勝。
奇数wの一石局面では別列への追加だけが勝ち手、一列二石なら同列三石目だけが勝ち手。

M₃=M₄=3、M₅=8、M₆=17、M₇=31。
これは**任意の列候補集合に対する最良の一様閾値**である。
各列M_w−1点では全局面公式を破る整数点盤を全w≥3で構成できる。
上界は三点補間による禁止高さ数の評価、下界は補間線形形式を有限多項式回避で相異ならせる構成で証明する。

等間隔・共通の連続整数候補に限れば、より小さい閾値を持つことがある。
標準五列盤の真の公式安定化高さ6はK0535。
二列のλ=0ゲームは全四点禁止なので、各列二点以上なら全局面で `(1−|S|) mod2`。
標準λ=1の盤の一般勝敗を主張する結果ではない。
