---
id: K0753
title: S2 {59,60} milestone-3のS6 orbit worklist manifest（greedy証明書1–8・blocker 12個・S6 orbit 20,534 = 49.1%・milestone-2完全包含）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0748
  note: milestone-2 manifest（証明書1–5・S6 orbit 10,988）のgreedy順拡張。
    milestone-2の10,988鍵は本unionの部分集合でcost全件一致・共有2,248件はcerts拡張
- type: depends_on
  target: K0729
  note: 34 certificate崩壊とgreedy順序（証明書6–8位 {73},{90,96},{23}）。
    単独S6 orbit 3,868/4,232/4,416と累積union 20,534はladder測定と完全一致
- type: depends_on
  target: K0675
  note: 78先手勝ち/16第二手勝ち五石位置oracle（94位置universe）
artifacts:
- path: research/experiments/n11-s2-5960-milestone3-20261112/scripts/milestone3_worklist.ts
  role: source
  note: 証明書6–8（{73},{90,96},{23}）のS6 orbit列挙（整数外接円circle-mask幾何・
    D4 canon・K0746/K0748と同一機械）。単独実行でfresh unionを再生成する
- path: research/experiments/n11-s2-5960-milestone3-20261112/scripts/merge_manifest.sh
  role: source
  note: milestone-2 output と fresh union を jq でmergeしてmilestone-3 manifestを
    再構築する完全再現手順（16MiB sandbox制約による分割生成）
- path: research/experiments/n11-s2-5960-milestone3-20261112/output/milestone3_manifest.json
  role: data
  note: milestone-3 manifest（compact形式627,770 bytes・S5 orbit 516 rep・
    S6 orbit 20,534のcost順フルリスト [非ゼロパディングhex, cost, certs]・
    certs bitmask（9 entry）・protocol）。merge_manifest.shがbyte-exact再現
- path: research/log/2026-11-12-n11-s2-5960-milestone3-manifest.md
  role: log
  note: 実行記録・milestone-2 subset検証（cost不一致0件）・16MiB制約への対応
---

# S2 {59,60} milestone-3: greedy証明書1–8のS6 worklist manifest

S2 {59,60}（best S3 r=61）閉鎖のgreedy証明書順
{5,115} → {27,93} → {71} → {82} → {104} → {73} → {90,96} → {23}
（**60 blocker中12個閉鎖**）に対して、milestone-2（K0748）と同一の幾何機関で
S6 orbit worklistを完全列挙した（78 FW oracle条件付き）。

- 単独証明書S6 orbit: 3,868 / 4,232 / 4,232 / 4,416（{73}/{90}/{96}/{23}）。
  **{90}と{96}のorbit集合はD4鏡映で完全同一**（全要素一致を機械検証）で、
  greedyの{90,96}は1証明書（bits 64|128）。義務数 7,890/8,626/8,626/8,859
  （{73}の7,890はverify_conditional_s6_cover_46.pyと同規約）。
- 証明書6–8の相互union 11,794、**merged union 20,534**（41,842全体の49.1%）。
  K0748の別実行ladder測定（10,988→14,134→17,395→20,534）と完全一致する
  第三系統の独立再現。S5 orbit union 516 / 1,447（35.7%）。
- **milestone-2 subset検証PASS**: milestone-2の10,988鍵は本unionの部分集合、
  cost不一致0件・重複キー0件。共有2,248件は証明書6–8ビットを含むcertsに拡張、
  新規9,546件。s6Allはcost昇順にソート済み（単調性を機械検証）。
- cost（合法S7子数）: min 50 / 中央値 78 / max 101 / 平均 78.117 /
  **合計 1,604,047 raw S7辺**（milestone-2の874,761比 +729,286）。
  新規帯はmin 50と軽く、cost下位からの消化でcache暖機が早い。

solver protocolはK0746/K0748と同一（WIN証明書=認定済みWIN7子鍵1個・LOSS=全合法子認定・
同一canonical鍵のverdict不一致=WIN/LOSS conflictで即停止・D4で1 orbit 1 rep）。

本計算は78 FW oracleの下の条件付きworklist確定であり、いかなるS6 verdict・
S2・空盤の勝敗も含まない。空盤・二石root {49,60} は **UNKNOWN** のままである。
