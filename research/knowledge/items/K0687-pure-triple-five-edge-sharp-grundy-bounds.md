---
id: K0687
title: 純三点残余辺1〜7本の通常値とmisère補助値の鋭い最大値は1,1,1,3,5,7,9
kind: proposition
status: proved
topics:
- grundy
- residual-games
- geometry
- variants
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 純三点残余族の通常ゲームと自由点のxor分離
- type: depends_on
  target: K0683
  note: 抽象三点禁止族の全型を指定有限整数点盤へ移せる
- type: depends_on
  target: K0704
  note: 全核への自由点付加は補助値にもxor1として扱える一般補題
artifacts:
- path: research/experiments/pure-triple-few-edge-grundy-20261107/proof.md
  role: proof
  note: 所属cellの行和3による全称有限帰着、孤立点処理、鋭い達成例
- path: research/experiments/pure-triple-few-edge-grundy-20261107/audit.py
  role: verifier
  note: Venn行和生成と独立辺追加生成の全型集合一致、cell占有数mex
- path: research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp
  role: verifier
  note: 個別頂点占有subsetによる全527型の別根値計算
- path: research/experiments/pure-triple-few-edge-grundy-20261107/output/audit.json
  role: certificate
  note: h1..5の全型・度数・527型の個別一致・199922安全状態監査
- path: research/log/2026-11-07-pure-triple-spectra-and-incidence-bounds.md
  role: log
  note: 六点全数計算から、辺数による頂点無制限の定理へ進んだ経緯
- path: research/experiments/pure-triple-six-edge-complete-20261108/proof.md
  role: proof
  note: 全称有限帰着・完全生成・独立総数監査・自由点二個周期
- path: research/experiments/pure-triple-six-edge-complete-20261108/audit.py
  role: verifier
  note: 六辺全核の生成と別subset根値比較
- path: research/experiments/pure-triple-six-edge-complete-20261108/generate.cpp
  role: verifier
  note: 辺次数profileで正規化する完全辺追加生成器
- path: research/experiments/pure-triple-six-edge-complete-20261108/count_signatures.py
  role: verifier
  note: 母関数係数と分割束反転による独立辺ラベル付き総数
- path: research/experiments/pure-triple-six-edge-complete-20261108/output/audit.json
  role: certificate
  note: 全4279型と3190580安全状態の通常値
- path: research/experiments/pure-triple-six-edge-complete-20261108/output/misere.json
  role: certificate
  note: 五辺以下を含む4806核の両偶奇と10171506安全状態
- path: research/experiments/pure-triple-six-edge-complete-20261108/output/misere_values.json
  role: data
  note: 核順序hash付きの両自由点偶奇の全補助値
- path: research/experiments/pure-triple-six-edge-complete-20261108/output/generation_regression.json
  role: certificate
  note: 一般化生成器と元の六辺全署名・安定化群位数の完全一致
- path: research/experiments/pure-triple-seven-edge-complete-20261108/proof.md
  role: proof
  note: 全53340七辺核・両値最大9・七辺g8唯一核の完全証明
- path: research/experiments/pure-triple-seven-edge-complete-20261108/audit.py
  role: verifier
  note: 全生成と独立母関数・二つの通常値C++計算
- path: research/experiments/pure-triple-seven-edge-complete-20261108/misere.py
  role: verifier
  note: 自由点両偶奇の通常値と補助値の全件照合
- path: research/experiments/pure-triple-seven-edge-complete-20261108/output/audit.json
  role: certificate
  note: 七辺全53340型と通常値ヒストグラム
- path: research/experiments/pure-triple-seven-edge-complete-20261108/output/misere.json
  role: certificate
  note: 106680根・199776072安全状態の両値比較と全補助値
scope: 任意個の合法点、極小残余禁止辺は全て三点集合、辺数e<=7。gは通常Grundy、hは終局1のmisère補助mex。任意個の自由点を許す。標準全正方形盤での達成は含まない。
evidence: 所属cellの整数行和3への全称帰着と自由点周期。五辺以下527・六辺4279・七辺53340の全核を完全生成し、独立母関数総数と照合。通常値と自由点両偶奇の補助値をcell再帰と別の個別subsetで全根照合。
---


## 点数を制限しない鋭い最大値

純三点禁止辺の本数がe=1..7のとき、通常Grundy gと終局1のmisère補助mex hの
自由点を任意個許した鋭い最大値は、どちらも

\[
\boxed{1,1,1,3,5,7,9.}
\]

従って辺数e≤3なら両値≤1、e≤4で≤3、e≤5で≤5、e≤6で≤7、e≤7で≤9。
値2・3に必要な三点辺の最小本数は4、4・5では5、6・7では6、8・9では7。
これは両値の最適上界が一致するという主張で、個々の族のg=hを意味しない。

非孤立点は高々3e個。所属署名cellの点数を各辺の行和3になる非負整数ベクトルで表し、
辺置換で同型を除くと、e=1..7の核数は **1,3,12,66,445,4279,53340**。
全58,146核を完全生成した。通常gは自由点一個ごとにxor1。
hにも一自由点でのxor1則がK0704により成立する。
元の完全計算はそれを仮定せず、全核の自由点0/1を独立に検査した。この有限帰着と周期が任意点数への量化を保証する。

## 完全性と独立検査

五辺以下の527核は所属署名の行和生成と辺追加生成で全型集合が一致した。
六辺・七辺は完全辺追加生成を、別の多変数母関数と分割束Möbius反転の総数で監査した。
核の辺置換安定化群をAとしたe!/|A|の和は、独立総数と両辺数で一致した。

六辺核のg最大は6で十型、七辺核のg最大は8で十一点のただ一型。
それぞれ自由点を加えると7と9を達成する。
通常値の別subset比較は、六辺3,190,580、七辺66,592,024安全状態で全根一致。
自由点両偶奇の(g,h)比較は、六辺以下10,171,506、七辺199,776,072安全状態で全件一致した。
七辺ではC++ cell方式も全根一致し、さらに400核をPython再帰で確認した。

六辺g6の十型分類はK0691、点数と辺数の全最適組合せはK0699を参照。

## 適用境界

[五辺以下の当初の証明](../../experiments/pure-triple-few-edge-grundy-20261107/proof.md)、
[六辺の証明と全表](../../experiments/pure-triple-six-edge-complete-20261108/proof.md)、
[七辺の証明と全表](../../experiments/pure-triple-seven-edge-complete-20261108/proof.md)を保存。
二点辺・四点辺が混じる族や、八本以上の鋭い最大値には拡張しない。
hは直和のSprague–Grundy値ではなく、xor合成には使わない。
K0683で達成型を指定有限整数点盤へ移せるが、標準全正方形格子盤の達成ではない。
