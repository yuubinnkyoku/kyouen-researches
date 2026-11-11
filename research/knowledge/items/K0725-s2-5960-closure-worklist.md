---
id: K0725
title: S2 {59,60} 閉鎖に必要な新S5 verdictはちょうど1,447 D4 orbit、最小部分証明書は54 orbitで2 blockerを閉じる
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0685
  note: best-S3 blocker監査の直接子列挙による閉鎖要件の定量化
- type: depends_on
  target: K0675
  note: 78先手勝ち/16第二手勝ち五石位置oracle（94位置universe）
- type: depends_on
  target: K0676
  note: S4-A/B/C四石親構造。S4-C={51,59,60,61}のFW子6個を確認
artifacts:
- path: research/experiments/n11-s2-5960-worklist-20261110/scripts/s2_worklist.ts
  role: source
  note: 純TS再現（BigInt盤、Bareiss幾何、D4 canon）。
    単独実行で分布・13,244・classA 32件・worklist 1,447・鏡映同一性まで全数値を再現
- path: research/experiments/n11-s2-5960-worklist-20261110/scripts/s6_census_smallest_blockers.ts
  role: source
  note: 最小2 blockerのS6 census（2,191/2,150/共通79/union 4,262）
- path: research/log/2026-11-10-n11-s2-5960-worklist.md
  role: log
  note: 実行記録
---

# S2 {59,60} の閉鎖worklist: 1,447 orbitの完全一致とfrontier分解

二石root S2 = {60,59} のbest S3 r=61に対する60 blocker S4の全合法五石子を列挙し、
94位置universeに含まれない未知子を集計した（78 FW oracle条件付き）。

- 未知子はdistinct 4,519 S5位置、D4 orbitちょうど1,447。
  q59の独立census（S6義務133,524から逆算した~1,447 orbit）と完全一致する相互検証。
- orbitは1–8個のblockerに使われる（serve分布
  {1:4, 2:50, 3:99, 4:940, 5:172, 6:163, 7:15, 8:4}）。
- 60 blockerのうち56個は極大（他blockerの真部分集合でない）、4個は被他覆、
  極大blockerのorbit unionは全1,447に一致。
- 最小部分証明書: t=5とt=115のorbit集合は完全同一（54 orbit）で2 blockerを同時に閉じる。
  t=27とt=93も同一（54 orbit）。2組の共通orbitは2個のみ。
  blockerごとのorbit必要数は最小54（上記4点）、中央値102、最大107。
- 鏡映同一性: S2 {60,61}（best r=59）のworklistは {59,60} と同一。
  1,447 orbitの解決で両S2のS5要件が同時に満たされる。
- S4-C = {51,59,60,61} のFIRST_WIN六石子は {44,45,66,67,68,69} の6個
  （K0724記録の確認・69はS4-Aと共有）。
- 32 classA S4の未知子unionは2,479 S5（2,227 orbit）。classAだけを先に閉じる道は
  S2 {59,60} 全体worklistより小さいが1,447より大きくない範囲でS2横断の共通率次第。

本計算は78先手勝ちoracleの下の条件付き観察であり、いかなるS2・空盤の勝敗も含まない。
空盤・二石root {49,60} は UNKNOWN のままである。

## 部分証明書のS6規模（追記・同session実測）

- blocker t=5: 未知子97（54 orbit）のS6義務8,682 → distinct 4,421 → S6 orbit 2,191。
- blocker t=27: 未知子98（54 orbit）のS6義務8,595 → S6 orbit 2,150。
- 2組のS6 orbit共通は79。4 blocker（t=5,115,27,93）閉鎖の第1マイルストーンは
  S6 orbit 4,262（41,842全体の約10.2%）。
