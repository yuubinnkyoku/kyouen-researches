---
id: K0455
title: 独立行容量ゲームの勝敗局面数と非終局負け局面の漸近密度
kind: proposition
status: proved
topics:
- rectangles
- variants
- grundy
- statistics
aliases: []
relations:
- type: depends_on
  target: K0025
  note: 独立行容量への幾何的帰着が成立する盤に適用
artifacts:
- path: research/experiments/fixed-width/reports/capacity-parity-state-count-20261016.md
  role: proof
  note: 二項恒等式と偶奇射影による全称証明
- path: research/experiments/fixed-width/scripts/verify_capacity_parity_counts_20261016.py
  role: verifier
  note: 75組の全ビット集合直接列挙
- path: research/experiments/fixed-width/output/capacity_parity_counts_audit_20261016.txt
  role: data
  note: 有限監査と五行九点版の具体値
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 幅w・長さm・各行容量rの独立行石置き通常プレイ、w,m,r>=1。標準共円ゲームへの適用には独立行帰着の別証明が必要。
evidence: '2026-10-21監査。偶奇射影・交代二項和・固定不足層の漸近式を確認し75条件を直接列挙。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


`a=min(m,r)`, `S=sum_{j=0}^a binom(m,j)` とおく。独立行容量ゲームの全安全局面数は `S^w`、勝ち局面数は `(S^w−binom(m−1,a)^w)/2`、負け局面数は `(S^w+binom(m−1,a)^w)/2`、極大局面数は `binom(m,a)^w` である。

固定 `w,r` で `m→∞` のとき、勝ち局面の割合は `wr/m+O(m^−2)`、非終局の負け局面の割合は `[wr(r−1)+binom(w,2)r²]/m²+O(m^−3)`。これらは全称数学的証明であり、有限監査は補助に限る。

5行q=9については、五行円が最大8点という別の幾何証明が成立する場合に `w=5,r=8` を代入でき、係数は40および920となる。幾何の新規証明はこの項目に含めない。

また全局面の合法辺数は `wm*(sum_{j=0}^{a-1} binom(m-1,j))*S^(w-1)`。固定不足数 `d` の局面割合は `m^(-d)*[z^d] (sum_{j=0}^r (r)_j z^j)^w+O(m^(-d-1))` であり、任意の固定層の主項が厳密に決まる。
