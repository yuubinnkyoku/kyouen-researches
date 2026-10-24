---
id: K0547
title: α²−α−3=0の三線整数高さq6帯は満容量安定化値7でP長は2・4・5だけ
kind: proposition
status: proved
topics: [geometry, variants, rectangles, maximal-safe, grundy, first-moves, certificates]
aliases: []
relations: []
artifacts:
- path: research/experiments/irrational-three-lines-q6-20261024/proof.md
  role: proof
  note: 幅4対幅2の円分類、m≥7の全称満容量とm6の14石終局による鋭さ
- path: research/experiments/irrational-three-lines-q6-20261024/exception.py
  role: verifier
  note: c3の厳密二次体・二方式全局面照合を再現
- path: research/experiments/irrational-three-lines-q6-20261024/audit-c3.json
  role: data
  note: m6の243324安全局面、全18初手、SG最大3、終局14石48局面と15石96局面
solution:
  board: x={0,1,(1±√13)/2}、整数高さ0..m−1の三線q6帯
  level: strong
  outcome: conditional
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全m≥1。m6は有限全局面DP、その他は閉形式
  conditions: q6共円共線禁止、通常プレイ
  verification: [mathematical-proof, independent-cpp-check]
  certificate: m≤4は3m石、m5は14石、m≥7は15石の固定終局。m6は二方式の全安全局面点別一致
  independent_check: Q(α)の直接六点判定と二方式mex。m6の243324局面を全照合、全初手の子SG0
  note: P長はm2,4,5のみ、他長は全初手勝ち。m6ではSG最大3のため全局面偶奇式を用いない
scope: α=(1±√13)/2、盤{0,1,α}×{0,...,m−1}、m≥1、q6通常プレイ。
evidence: m≥7の全称円予算証明とm6の明示14石終局、有限例外の二次体・全局面独立照合。
---

# √13の三線帯の鋭い安定化値7

満容量15石への安定化開始値は厳密にm=7。
m≥7の全安全局面ではg(S)=(15−|S|) mod2。
m≤4は全3m石、m5は全14石終局なので、それぞれ固定終局石数の偶奇式で全局面を解く。

m6は14石・15石終局が混在し、全局面DPによる有限強解決となる。
全243324安全局面を二方式で点ごとに照合し、根SG1・全初手の子SG0・最大SG3。
P長はm2,4,5だけで、他の全長では全初手が勝ち手。

六点円は二線のt,t+4とα線のt+1,t+3に限る。
m≥7で不足線を塞ぐには他線に少なくとも6個の既存高さが必要となり、容量5と矛盾する。
m6の14石終局を明示し、開始値7の最小性を証明した。
