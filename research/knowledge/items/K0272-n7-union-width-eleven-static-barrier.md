---
id: K0272
title: 代表U内の幅11障壁は占有差二層と整数最適21四点で証明
kind: proposition
status: proved
topics:
- reconfiguration
- certificates
aliases:
- F-BG
- Discovery:static-width11
relations:
- type: depends_on
  target: K0266
  note: ''
artifacts:
- path: night-research/DISCOVERY_CORNER_GATE_AND_COMPONENTS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/discovery_corridor_static_certificate.json
  role: certificate
  note: 6460候補の被覆
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/findings.md
  role: source
  note: F-BGの整数・分数最適性
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/verify_corridor_discovery.py
  role: verifier
  note: 全候補被覆の独立検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 代表U内の幅11障壁は占有差二層と整数最適21四点で証明

P=A\B、Q=B\A、d(S)=|S∩Q|−|S∩P|。Aの−5からBの5へ一石操作で移る経路にはd2→3隣接対がある。安全S⊆Uでd∈{2,3}なら|S|≤12。隣接対の石数は一つ違うので片方は≤11。

十三石以上の候補6460をU内59禁止四点のうち21で全被覆する証明書がある。後の有限最適化では整数最適21、分数最適102/5。幅11の十操作経路を検査済みなのでU内幅は正確に11。D4軌道占有数だけの証明ではなく、具体P/Q点の差を使う。
