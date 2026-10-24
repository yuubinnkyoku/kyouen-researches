---
id: K0550
title: 素数と素数平方から作る二次無理数三線q6帯の無限族を全長強解決できる
kind: proposition
status: proved
topics: [geometry, variants, rectangles, maximal-safe, grundy, first-moves, certificates]
aliases: []
relations:
- type: generalizes
  target: K0549
  note: c=4の二次無理数帯をc=1・素数p≥5・素数平方p²の無限族へ拡張
artifacts:
- path: research/experiments/irrational-three-lines-q6-20261024/proof.md
  role: proof
  note: (lB−lA)(lB+lA)=4cの因子対分類と円数上界により全素数・全長を証明
- path: research/experiments/irrational-three-lines-q6-20261024/family.py
  role: verifier
  note: 六つのc値で二次体行列式と二方式の全局面mexを再現
- path: research/experiments/irrational-three-lines-q6-20261024/verify.cpp
  role: verifier
  note: Q(α)を厳密整数対で表し、六点組の直接判定と因子対禁止集合を照合
- path: research/experiments/irrational-three-lines-q6-20261024/family-audit.json
  role: data
  note: 6例・6619338六点組・12036931安全局面の完全一致receipt
solution:
  board: x={0,1,α}、α²−α−c=0、c=1または素数p≥5または素数平方p²
  level: strong
  outcome: conditional
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 上記の全cと全m≥1の全安全局面
  conditions: 整数高さ0..m−1、q6共円共線禁止、通常プレイ
  verification: [mathematical-proof, independent-cpp-check]
  certificate: 非退化因子対は高々一つ、円の幅は5以上、全円数はmax(0,m−5)以下
  independent_check: c1,4,5,7,9,11の厳密二次体・二方式mex。無限族と無界長は別途数学的証明
  note: T=3min(m,5)、g(S)=(T−|S|) mod2。Pはm2,4のみ、安定化開始値は5
scope: c=1、素数p≥5、または素数平方p²。α=(1±√(1+4c))/2、盤{0,1,α}×{0,...,m−1}、m≥1、q6通常プレイ。
evidence: 全整数の弦長因子対分類、対象cの非退化因子対の一意性と円予算による全称数学的証明。六例の全有限監査を独立照合。
---

# 素数・素数平方の二次無理数帯の無限族

上記の全cと全mで全終局は `T=3min(m,5)` 石、全安全局面で `g(S)=(T−|S|) mod2`。
P長はm=2,4だけ。他の全長は先手必勝・全初手勝ちで、満容量15石への安定化は厳密にm=5から。

六点円はrs=c、0<r<sの因子対に対応し、二線の弦がt,t+r+s、α線がt+r,t+sとなる。
c=1では円が存在せず、対象の素数・素数平方では因子対が(1,c)だけで円幅は5以上。
その円予算で全長を解く。六例の二次体・全局面監査は証明の独立有限確認として保持する。

c=3や非退化因子対が複数ある一般合成数へ、同じ安定化値を拡張しない。
