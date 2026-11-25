---
id: K0321
title: 4×4は容量損失ゼロの二点削除で勝者が反転する
kind: proposition
status: computed
topics: [variants, maximum-safe, grundy]
aliases: [B204, B207]
relations:
- type: depends_on
  target: K0001
  note: 標準禁止ルールを残存盤点に誘導する
artifacts:
- path: research/experiments/original-claims/output/batch09_pairs_n4.json
  role: data
  note: 全120二点削除対と単独削除のg・K
- path: research/experiments/original-claims/reports/round68-b201-b250-original-scope-audit.md
  role: source
  note: B204/B207の量化照合、非零損失という追加条件を課さない
---

# 4×4は容量損失ゼロの二点削除で勝者が反転する

標準4×4盤の点IDを4y+xとする。盤からp=0=(0,0)、q=3=(3,0)を最初から使用不能にする。石を置く操作ではない。

全盤・p単独削除・q単独削除の空盤Grundyはすべて0で、二点同時削除では2になる。最大安全容量は四つの盤すべて7。容量損失は0=0+0と加法的でも、勝敗には単独削除から出ない相互作用がある。

旧出力の全120対中12対が同型の反転を示す。有限の存在証人であり、一般盤の反転頻度、非零容量損失での相互作用、最小盤の証明までは含めない。
