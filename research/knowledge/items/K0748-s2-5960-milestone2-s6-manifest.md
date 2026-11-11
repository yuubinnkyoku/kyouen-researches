---
id: K0748
title: S2 {59,60} milestone-2のS6 orbit worklist manifest（greedy証明書1–5・blocker 7個・S6 orbit 10,988・cost分布とladder拡張測定）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0746
  note: milestone-1 manifest（証明書2個・S6 orbit 4,262）のgreedy順拡張。
    milestone-1の4,262鍵は本unionのcerts&3部分集合として完全一致・cost全件一致
- type: depends_on
  target: K0729
  note: 34 certificate崩壊とgreedy順序（証明書3–5位 {71},{82},{104} の選定基準）。
    単独S6 orbit 2,421/2,516/2,563と累積union曲線は全て一致
- type: depends_on
  target: K0675
  note: 78先手勝ち/16第二手勝ち五石位置oracle（94位置universe）
artifacts:
- path: research/experiments/n11-s2-5960-milestone2-20261111/scripts/milestone2_worklist.ts
  role: source
  note: 純JS/TS再現（整数外接円circle-mask幾何・D4 canon・K0746と同一機械）。
    単独実行でmanifest全体を再生成する
- path: research/experiments/n11-s2-5960-milestone2-20261111/output/milestone2_manifest.json
  role: data
  note: milestone-2 manifest（261 S5 orbit rep×義務数・S6 orbit 10,988の
    cost順フルリスト・certs bitmask・protocol）
- path: research/log/2026-11-11-n11-s2-5960-milestone2-manifest.md
  role: log
  note: 実行記録・milestone-1 subset検証・greedy ladder証明書8位までの拡張測定・
    K0729義務数の訂正
---

# S2 {59,60} milestone-2: greedy証明書1–5のS6 worklist manifest

S2 {59,60}（best S3 r=61）閉鎖のgreedy証明書順
{5,115} → {27,93} → {71} → {82} → {104}（**60 blocker中7個閉鎖**）に対して、
milestone-1（K0746）と同一の幾何機関でS6 orbit worklistを完全列挙した
（78 FW oracle条件付き）。

- 単独証明書S6 orbit: 2,191 / 2,150 / 2,421 / 2,516 / 2,563。
  累積union: 2,191 → 4,262 → 6,517 → 8,780 → **10,988**
  （41,842全体の26.3%）。S5 orbit union 261 / 1,447（35.7%）。
  すべてK0729/K0746と一致する第三系統の独立再現。
- **milestone-1 subset検証**: milestone-1の4,262 S6鍵は本unionの
  certs bit 1|2 部分集合と集合として完全一致、4,262件のcost全件一致、
  106 S5 rep全件包含。単独証明書3–5はmilestone-1とほぼ disjoint
  （ペア重なり80–95、A∩B=79不変）で、単一バッチ消化に向く。
- cost（合法S7子数）: min 52 / p25 74 / 中央値 80 / p75 85 / max 101 /
  平均 79.61 / **合計 874,761 raw S7辺**。
- greedy ladder拡張測定（同一機関・別実行）: 第6–8位 {73}/{90,96}/{23} で
  累積S6 union 14,134 → 17,395 → **20,534（49.1%）**、S5 union 516（35.7%）、
  証明書8個で12 blocker閉鎖。単体S6 orbit 3,868/4,232/4,416はK0729と一致。
- 訂正: K0729本文のt=71/82/104の義務数（9,684/10,156/10,348）は再現不能
  （正しくは5,186/5,472/5,577。{73}の7,890がpython invariantと同規約）。
  orbit数・unionは全て一致するため、義務数の集計のみ本manifestのcertStatsを正とする。

solver protocolはK0746と同一（WIN証明書=認定済みWIN7子鍵1個・LOSS=全合法子認定・
同一canonical鍵のverdict不一致=WIN/LOSS conflictで即停止・D4で1 orbit 1 rep）。

本計算は78 FW oracleの下の条件付きworklist確定であり、いかなるS6 verdict・
S2・空盤の勝敗も含まない。空盤・二石root {49,60} は **UNKNOWN** のままである。
