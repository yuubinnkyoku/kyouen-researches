---
id: K0268
title: 7×7必須六軌道骨格の容量13は排他的二拡張だけで14へ上がる
kind: proposition
status: computed
topics:
- maximum-safe
- geometry
aliases:
- Cycle15:capacity-decomposition
relations:
- type: depends_on
  target: K0053
  note: ''
- type: depends_on
  target: K0269
  note: 骨格容量の上界認証
artifacts:
- path: research/log/discovery-cycles/CYCLE15_CAPACITY_DECOMPOSITION.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/log/discovery-cycles/CYCLE15_VERIFY.md
  role: verifier
  note: Pythonによる骨格制約の独立再計算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 7×7必須六軌道骨格の容量13は排他的二拡張だけで14へ上がる

MはD4セル軌道(0,0),(0,1),(0,2),(1,1),(1,2),(1,3)の36点。α(M)=13で最高層88集合・六占有型。中心追加はα14・A八配置、B-bundle=(0,3)∪(2,3)追加はα14・B八配置。B軌道の片方だけならα13（288/304最高配置）、(2,2)を足してもα13。

中心とBを同時に使用する十四石配置はない。骨格最高88集合のうち中心を追加可能なのはAから中心を除いた八集合だけ。allowed集合を広げるだけで「使用必須」とする条件を落とさない。
