---
id: K0096
title: 二次パラメータmodp非零認証の最大はp≡3 mod4で(p+13)/4
kind: proposition
status: proved
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0095
  note: ''
artifacts:
- path: research/verification/structural-lemmas-2026-10-02/quadratic-constructions.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/structural-lemmas-2026-10-02/checks/independent_geometry.json
  role: data
  note: 独立合同式・上界+1有限全数
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 二次パラメータmodp非零認証の最大はp≡3 mod4で(p+13)/4

p≡3 mod4,p≥7の二次P(t)=ut²+vt+wについて、全四点det非零modpを要求する認証方式の最大M_quad=(p+13)/4。四元和回避とDias da Silva–Hamidoune制限和定理による上界を区間構成が達成。p=3は3、p≡1 mod4はp。

これは認証方式内の最大。modp零でも整数det非零なら実際には安全なので、K_pや整数剰余放物線内最大の上界ではない。
