---
id: K0549
title: α²−α−4=0の三線整数高さq6帯は全長強解決でき満容量安定化値は5
kind: proposition
status: proved
topics: [geometry, variants, rectangles, maximal-safe, grundy, first-moves, certificates]
aliases: []
relations: []
artifacts:
- path: research/experiments/irrational-three-lines-q6-20261024/proof.md
  role: proof
  note: 六点円を幅5対幅3の平行弦に完全分類し全長の終局石数を証明
- path: research/experiments/irrational-three-lines-q6-20261024/verify.cpp
  role: verifier
  note: Q(α)の4×4行列式で全六点組と公式を比較し二方式の全安全局面mexを点ごとに照合
- path: research/experiments/irrational-three-lines-q6-20261024/audit.json
  role: data
  note: m1..10の1103223六点組とm1..7の1977032安全局面の完全一致receipt
- path: research/experiments/irrational-three-lines-q6-20261024/run.py
  role: verifier
  note: 一時バイナリで厳密二次体・二方式mex監査を再現
solution:
  board: x={0,1,(1±√17)/2}、整数高さ0..m−1の三線q6帯
  level: strong
  outcome: conditional
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全m≥1の全安全局面
  conditions: 共円または共線の6石禁止、通常プレイ、α²−α−4=0
  verification: [mathematical-proof, independent-cpp-check]
  certificate: 六点円は二線の高さt,t+5とα線のt+1,t+4だけ、全円数max(0,m−5)から満容量を証明
  independent_check: 厳密Q(α)行列式による全六点組と二方式の全安全局面mex、有限範囲を明示
  note: T=3min(m,5)、g(S)=(T−|S|) mod2。Pはm2,4のみ、他の全長は先手勝ち・全初手勝ち
scope: α=(1±√17)/2、m≥1、盤{0,1,α}×{0,...,m−1}、q6共円共線禁止の通常プレイ。
evidence: 因数分解(lB−lA)(lB+lA)=16による全六点円分類と全称円予算。m≤10の二次体幾何・m≤7の全局面は独立計算監査。
---

# 特定二次無理数の三線帯の全長強解決

全終局石数は `T=3min(m,5)`、全安全局面で `g(S)=(T−|S|) mod2`。
P長はm=2,4だけで、他の全m≥1では先手必勝・全初手勝ち。
満容量15石への安定化開始値は厳密にm=5。

六点円の全てはx=0,1で高さt,t+5、x=αで高さt+1,t+4となる。
盤全体の円はmax(0,m−5)本しかないので、4石以下の線の利用不能点は常にm−1以下。
この全称予算でmの無界部分を解き、二次体の直接行列式と二方式の全局面計算で有限部分を確認した。

標準等間隔三行の結論ではなく、αの多項式と整数高さに依存する。
