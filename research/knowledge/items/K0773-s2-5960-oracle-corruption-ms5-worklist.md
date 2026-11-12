---
id: K0773
title: milestone1-4オラクルhex配列の転写破損6件を機関特定（61 blocker過大計上の原因確定）・未知S5 196のうち10個はK0675 LOSS子で即SECOND_WIN・milestone-5残worklist 7,867 orbit/615,497 cost manifest生成
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0766
  note: orbit-level（全D4像）blocker縮小110→102閉鎖/8残・方向規約（W4(S4)=∃FIRST_WIN S5子）を
    引き継ぎ、削減前会計 7,880/616,491 と本項の独立会計が完全一致した
- type: depends_on
  target: K0675
  note: 94五石位置オラクル（78 FW+16 SW・3,868 S6 sweep・14 LOSS S6）を正として全 会計を実行
- type: depends_on
  target: K0757
  note: published milestone-4 ladder（61 blocker・43,375 orbit census）はconcrete-level照合+
    配列破損に基づく歴史的会計として置き換えられる
- type: depends_on
  target: K0762
  note: cert73_regen_audit.tsの配列破損を特定したが、同監査のpublished結果（pass）は
    破損エントリに非感受性のため無傷
artifacts:
- path: research/experiments/n11-s2-5960-milestone5-20261112/scripts/orbit_ms5_worklist.ts
  role: source
  note: 94オラクル鍵+14 LOSS S6鍵を埋込み（s5_verdicts.json由来・自己assert 78+16/3,868/14）、
    orbit-level blocker特定・196 S5会計・settled-10判定・7,867/615,497 manifest生成を
    再実行する自己完結TS検証script（anchor不一致でthrow）
- path: research/experiments/n11-s2-5960-milestone5-20261112/output/ms5_closure_summary.json
  role: data
  note: 全anchor（sweep 3,868・110/102/8・196/17,524/479/13/10・7,880/616,491 crosscheck・
    7,867/615,497）・類別未解決S5数・first-strike最安候補表
- path: research/experiments/n11-s2-5960-milestone5-20261112/output/ms5_s5_worklist.json
  role: data
  note: 196未知S5 orbit（類bit・raw義務・unjudged子数・judged LOSS子有=即SECOND_WIN・cost）
- path: research/experiments/n11-s2-5960-milestone5-20261112/output/ms5_s6_manifest.csv
  role: manifest
  note: "旧単一csv（supersededの索引）。7,867行の実体は同ディレクトリのms5_s6_manifest_part1..6.csv（各49,873バイト、part6のみ49,683）"
- path: research/log/2026-11-12-n11-s2-5960-orbit-ms5-manifest.md
  role: log
  note: 実行記録・K0766との並走と独立一致・配列破損のforensics・実装教訓
scope: S2 {59,60}の残worklistのorbit-level再構成とオラクル配列破損の機関特定。blocker/S2/空盤の勝敗判定は含まない。
evidence: >-
  (1) repo配列の破損特定: milestone4_worklist.ts（=milestone1-4系の生成機関）のfwHex/swHexを
  K0675 records（s5_verdicts.json）の正規化94鍵と全照合した結果、ms4は5件
  （fw[16] {21,59,71,72,73}・fw[17] {22,59,71,72,73} は内容不一致、fw[75] {37,47,48,49,57}・
  fw[76] {38,47,48,49,57} は32文字桁消失で×16³回復={49,59,60,61,69}/{50,59,60,61,69}、
  sw[12] {31,47,48,49,57} はSW記録{31,59,60,61,69}に未対応）、cert73_regen_audit.tsは6件
  （上記+fw[77] {39,47,48,49,57} →×16³={51,59,60,61,69}）がrecordsと不一致と機関特定した。
  有効エントリ+回復で94記録鍵（78 FW+16 SW）を過不足なく説明する。
  欠落FW記録 {21,47,59,60,61}/{22,47,59,60,61}/{49,59,60,61,69}/{50,59,60,61,69} はいずれも
  S3 {59,60,61}を含み、concrete-level fcはD4像を照合しないこと（102 vs 49閉鎖の主因）に加えて
  これらのextras {21,47}/{22,47}/{49,69}/{50,69} を喪失していた。published 61 blockerの
  過大計上の原因はこの2つの重畳と確定した。cert73監査のpublished passは破損エントリに
  非感受性のため無傷（破損配列のまま再現することも確認）。
  (2) 未知S5会計: 8 blockerの子のうちオラクル非含有のS5 orbitは196（raw義務17,524）、
  うち479子インスタンスはK0675 sweep 3,868で判定済み（13 LOSS-for-moverインスタンス）。
  verdict規約（FIRST_WIN ⟺ 全子WIN-for-mover・s5_verdicts.py機関verbatim+94/94クロス集計で
  K0675内部整合を確認）により、10 S5 orbitは∃judged LOSS子で即SECOND_WIN確定し
  worklistから除去できる。
  (3) milestone-5 manifest: 残worklistは7,867 S6 orbit / 615,497 S7合法辺cost
  （削減前の全未知S5起点会計は7,880/616,491でK0766の独立会計と完全一致）。
  first-strike最安候補は類{5,115} 5,128・{27,93} 4,368・{23,31,89,97} 5,178 S7辺で、
  類ごとに1 S5の全子WIN検証から閉鎖を狙える。
---

# milestone-5: 配列破損の機関特定とS2 {59,60}残worklistのorbit-level再構成

## 発見1: オラクルhex配列の転写破損（milestone1-4の61 blocker過大計上の原因）

milestone1-4系（milestone4_worklist.ts・cert73_regen_audit.ts）が埋め込む
fwHex/swHex配列をK0675 recordsと全照合（正規化94鍵・8 D4像込み）したところ、
次の6エントリがrecordsと一致しない:

| file | entry | 格納値 | 桁数 | records側の正 |
|------|-------|--------|------|--------------|
| ms4 | fw[16] | {21,59,71,72,73} | 35 | {21,47,59,60,61} |
| ms4 | fw[17] | {22,59,71,72,73} | 35 | {22,47,59,60,61} |
| ms4 | fw[75] | {37,47,48,49,57} | 32 | {49,59,60,61,69}（×16³回復） |
| ms4 | fw[76] | {38,47,48,49,57} | 32 | {50,59,60,61,69}（×16³回復） |
| ms4 | sw[12] | {31,47,48,49,57} | 32 | SW {31,59,60,61,69}（回復不能・記録側特定） |
| cert73 | fw[77] | {39,47,48,49,57} | 32 | {51,59,60,61,69}（×16³回復・cert73のみ） |

有効72+15エントリと回復5件で94記録鍵を過不足なく説明する（cert73はfw[77]破損分
{51,59,60,61,69}が欠ける）。32文字エントリはhex桁消失、35文字のfw[16]/[17]は
 plausible-but-wrong位置への置換と特徴づけられる。

影響: concrete-level fcは生の配列一致のみでD4像を照合しない（主因: 110合法S4子中
102がorbit-levelで閉鎖できるのに49しか閉鎖できなかった）うえ、破損により4件のFW記録
（いずれもS3 {59,60,61}を含む）のextras {21,47}/{22,47}/{49,69}/{50,69}を喪失した。
published ladderの61 blockerはこの2つの重畳による過大計上であり、K0766の8 blocker
（3 V4類）に置き換えられる。cert73監査のpublished passはpb.get(73)が破損エントリに
非感受性のため無傷。

## 発見2: 未知S5 196の会計と10個の即SECOND_WIN

8 blocker {5,23,27,31,89,93,97,115}（3類）の子のうちオラクル94位置に含まれない
S5 orbitは196（類別: {5,115}=52・{27,93}=53・{23,31,89,97}=97・重複6）。
raw義務17,524のうち479子インスタンスはK0675 sweep（3,868 S6）で判定済みで、
うち13インスタンスがLOSS-for-mover。verdict規約（FIRST_WIN ⟺ 全子WIN-for-mover）により
**10 S5 orbitは∃judged LOSS子で即SECOND_WIN**（10個の残子は計算不要）。

## 発見3: milestone-5 manifest（7,867 orbit / 615,497 cost）

settled-10を除いた残worklistは **7,867 S6 orbit / 615,497 S7合法辺cost**
（ms5_s6_manifest.csv・cost昇順・類bit列付き）。削減前の全未知S5起点会計
（7,880/616,491）はK0766の独立な4代表起点会計と**完全一致**しており、
両会計の正当性を相互検証する。

first-strike: 各類で最も安いS5候補1個の全子WIN検証は
{5,115}: 5,128 / {27,93}: 4,368 / {23,31,89,97}: 5,178 S7辺。
blocker閉鎖（∃FIRST_WIN S5子）は類ごとに1個のS5がFWならば成立するため、
adaptive coordinatorはmanifest全体（615k辺）より先に合計~15k辺の候補から
始められる。

## 2026-11-12 erratum: manifest分割

初回反映の単一CSV（ms5_s6_manifest.csv）はsandbox取得経路の~64KB上限で1,683行
（cost≤72）まで切れていた。ローカル正本（298,963 bytes・7,867行）と行単位照合の上、
6 part（part1..6・各1,312行＋末尾1,307行・ヘッダ付き）に分割して再pushし、
各行数・先頭行・末尾行・全バイト数を検証した。単一csvは指置きファイルに置換した。

## 未解決・レジューム

- 7,867 S6の外部solver消化（cost昇順またはfirst-strike起点）→ S5 verdict →
  3類blocker閉鎖 → S3 {59,60,61} proven-first → S2 {59,60}判定。
- verdictはすべてK0675の監査済みオラクルに条件付き。
- generated viewsの再生成は本反映と別コミット（CI/別環境）で行うこと。

11×11空盤・二石root {49,60}・S2 {59,60} は **UNKNOWN** のままである。
本項はいかなる勝敗も判定しない。
