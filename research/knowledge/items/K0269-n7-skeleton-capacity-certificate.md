---
id: K0269
title: 骨格容量α(M)≤13は120占有候補と七残余補題で認証される
kind: proposition
status: proved
topics:
- maximum-safe
- certificates
aliases:
- Cycle34:occupancy-certificate
- Cycle40:compressed-certificate
relations:
- type: depends_on
  target: K0053
  note: ''
artifacts:
- path: research/log/discovery-cycles/CYCLE40_COMPRESSED_CERTIFICATE.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/cycle34_occupancy_lattice_certificate.json
  role: certificate
  note: 全120候補の不実現と対照
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/cycle40_compressed_inequalities.json
  role: data
  note: 113候補を除外する部分集合容量
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/cycle40b_residual_joint_lemmas.json
  role: data
  note: 七残余候補の完全決定
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 骨格容量α(M)≤13は120占有候補と七残余補題で認証される

六骨格軌道の各占有≤3から、和14の整数占有候補は120。完全計算したproper-subset最大容量だけで113候補を排除し、残る七候補を個別のexact occupancy決定で排除する。和13の実現対照がありα(M)=13。

full-Mの既知上界13を部分集合不等式の根拠へ流用する循環証明は使わない。幾何的軌道上限は一般定理、部分集合容量と七例外は有限solver依存であり、全てが紙上幾何証明という主張ではない。
