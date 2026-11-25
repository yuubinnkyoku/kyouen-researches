---
id: K0746
title: S2 {59,60} milestone-1のS6 orbit worklist manifest（greedy先頭2証明書・blocker 4個・S6 orbit 4,262・コスト分布とsolver protocol確定）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0725
  note: 閉鎖worklist 1,447 orbit・最小部分証明書 {5,115}/{27,93} 54 orbitの直接の子列挙
- type: depends_on
  target: K0729
  note: 34 certificate崩壊とgreedy順序（先頭2証明書の選定基準）
- type: depends_on
  target: K0675
  note: 78先手勝ち/16第二手勝ち五石位置oracle（94位置universe）
artifacts:
- path: research/experiments/n11-s2-5960-milestone1-20261111/scripts/milestone1_worklist.ts
  role: source
  note: 純JS/TS再現（整数外接円circle-mask幾何・D4 canon・full S6 worklist出力）。
    単独実行でmanifest全体を再生成する
- path: research/experiments/n11-s2-5960-milestone1-20261111/output/milestone1_manifest.json
  role: data
  note: milestone-1 manifest（106 S5 orbit rep×義務数・S6 orbit 4,262のcost順フルリスト・protocol）
- path: research/log/2026-11-11-n11-s2-5960-milestone1-manifest.md
  role: log
  note: 実行記録・幾何機械の第三系統検証・外部solver向けプロトコル・K0745→K0746再採番記録
---

# S2 {59,60} milestone-1: greedy先頭2証明書のS6 worklist manifest

S2 {59,60}（best S3 r=61）閉鎖のgreedy先頭2証明書
certA = blockers {5,115}・certB = blockers {27,93}（K0729の順序）に対して、
S5 orbit代表からの子列挙によりS6 orbit worklistを完全列挙した（78 FW oracle条件付き）。

- certA: S5 orbit 54（raw義務 4,795）→ **S6 orbit 2,191**。
  certB: S5 orbit 54（raw義務 4,698）→ **S6 orbit 2,150**。
- S5 orbitの両証明書共通はちょうど2、S6 orbitの共通は79 → **union 4,262**
  （K0725の2系統censusと完全一致の第三の独立再現）。
- 各S6 orbit repの合法手数（＝S7 raw辺数）: min 52 / 中央値 77 / max 93 /
  平均 76.78 / **合計 327,221 raw S7辺**。分布 ≤60: 50件・61-70: 766件・
  71-80: 2,054件・81-93: 1,392件。
- 106 S5 orbit repのhex鍵と義務数、S6 orbit 4,262鍵のcost昇順フルリストを
  manifestとして確定した（外部solverはこれを直接消費できる）。

## solver protocol（証明書の独立検証可能性）

- S6 verdict = WIN_for_mover ⟺ repの合法S7子のうち少なくとも1つがWIN7
  （S7手番側の敗北）と認定済み。WIN証明書は認定済みWIN7子鍵1個のみ提示すればよい。
  LOSS証明書は全合法子の認定を要する。
- merge規則: 同一canonical鍵について2workerのverdictが食い違ったらWIN/LOSS conflict
  として証明書組み立てを停止し、監査する。D4不変性により1 orbit 1 repのみ認定する。
- 幾何機械（整数外接円circle-mask）は verify_conditional_s6_cover_46.py の
  reconstruct不変量（94 / 7,890 / 7,813 / 3,868 / {2:3791,3:77}、priority S4={47,59,60,61}）
  を全て再現し、第三系統の独立検証を与えた。

本計算は78 FW oracleの下の条件付きworklist確定であり、いかなるS6 verdict・
S2・空盤の勝敗も含まない。空盤・二石root {49,60} は **UNKNOWN** のままである。
