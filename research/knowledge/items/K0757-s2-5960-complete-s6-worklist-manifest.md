---
id: K0757
title: S2 {59,60} 完全S6 worklist manifest（greedy証明書1–33・43,375 S6 orbit = 全worklist・S5 1,447・q59推定41,842の訂正）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0754
  note: milestone-3 manifest（証明書1–8・S6 20,534）の全33ステップ拡張。
    milestone-3の20,534鍵は本unionの部分集合でcost不一致0件（機械検証）・
    516 s5Repsも義務数不一致0件で部分集合
- type: depends_on
  target: K0729
  note: 34 certificate崩壊とgreedy順序。step 9–33の証明書選択は
    greedy-ladder-complete log（2026-11-12）のS5レベル確定値と完全一致
- type: depends_on
  target: K0675
  note: 78先手勝ち/16第二手勝ち五石位置oracle（94位置universe）。
    本計算は78 FW oracle条件下の条件付きworklist確定
artifacts:
- path: research/experiments/n11-s2-5960-milestone4-20261112/scripts/milestone4_worklist.ts
  role: source
  note: 証明書1–33のS6 orbit列挙（整数外接円circle-mask幾何・D4 canon・K0746/K0748/K0754と同一機関）。
    16MiB制約のためCHUNK=1..10の分割実行でフラグメントを生成
- path: research/experiments/n11-s2-5960-milestone4-20261112/scripts/merge_ms4.sh
  role: source
  note: フラグメント10個からpublished manifestをbyte-exactに再構築する手順
    （certsビットはフラグメント間で非交差なので加算merge＝OR）
- path: research/experiments/n11-s2-5960-milestone4-20261112/output/milestone4_manifest.json.part1
  role: data
  note: 完全S2 {59,60} S6 worklist manifest（compact形式・S5 orbit 1,447 rep・
    S6 orbit 43,375のcost順フルリスト [unpadded hex, cost, certs]・
    certStats（greedy step 1–33・0-marginalクラス除く）・protocol・検証記録）。
    16MiB sandbox制約により等幅3分割で公開: milestone4_manifest.json.part1/part2/part3
    （`cat` で byte-exact 再結合。全体 1,782,977 bytes・
    md5 f8c1a724c6c7d757192f15f38d4c5da0）
- path: research/log/2026-11-12-n11-s2-5960-ms4-complete-worklist.md
  role: log
  note: 実行記録・milestone-1/2/3再生成による制御検証・milestone-3 subset検証PASS・
    q59推定の訂正・実装教訓（32ビットOR・8MiB上限・フラグメント破損）
---

# S2 {59,60} milestone-4: 完全S6 worklist manifest（greedy証明書1–33・43,375 orbit）

S2 {59,60}（best S3 r=61）閉鎖のgreedy証明書ladder（K0729/K0754-ladder、
{5,115} → {27,93} → {71} → {82} → {104} → {73} → {90,96} → {23} → … → {114,116}、
計33ステップ・61/61 blocker、step 16/24/26は0-marginalで追加orbit 0）に対して、
milestone-1/2/3と同一の幾何機関でS6 orbit worklistを完全列挙した（78 FW oracle条件付き）。

- **完全worklist: S6 orbit 43,375 / S5 orbit rep 1,447**。S5 union 1,447は
  K0725/K061の完全D4 orbit censusと一致、**S5義務総和133,524はq59のraw義務censusと一致**
  → worklistの完全性を2つの独立した既知censusで確認。
- **訂正: q59のhash-dedupe推定「S6 orbit ≈41,842」は過少**（完全列挙で43,375、約3.6%低）。
  したがってmilestone-2/3のcoverageは 20,534/41,842=49.1% でなく
  **20,534/43,375=47.3%** が正しい。以後の進捗測定は分母43,375を用いる。
- cost（合法S7子数）: min 50 / 中央値 81 / max 101 / 平均 80.165 /
  **合計 3,477,178 raw S7辺**（milestone-3の1,604,047比 +1,873,131）。
- 単体証明書S6 orbit（step 9–33は本項目が初測定; 値はlog・manifest certStats参照）。
  step 1–8の単体値・累積値はK0746/K0748/K0754と完全一致（第三系統再現）。
- **milestone-3 subset検証PASS**: 公表manifestの20,534 s6All鍵は本unionの部分集合で
  cost不一致0件・516 s5Repsも義務数不一致0件（group_by join機械検証）。
- merge中間値の累積S5 orbit（756→1,248→1,349→1,415→1,439→1,447）は
  greedy-ladder-complete logの確定値と全て一致。

solver protocolはK0746/K0748/K0754と同一（WIN証明書=認定済みWIN7子鍵1個・
LOSS=全合法子認定・同一canonical鍵のverdict不一致=WIN/LOSS conflictで即停止・D4で1 orbit 1 rep）。

## 意味

S2 {59,60}閉鎖に必要なS6 verdict作業の全体像が確定した:
43,375 S6 orbit（1 orbit 1 rep）にWIN/LOSSを認定すればS5 1,447 repが閉じ、
61 blocker→S2 {59,60}の条件付き判定に到達する。

本計算は78 FW oracleの下の条件付きworklist確定であり、いかなるS6 verdict・
S2・空盤の勝敗も含まない。空盤・二石root {49,60} は **UNKNOWN** のままである。
