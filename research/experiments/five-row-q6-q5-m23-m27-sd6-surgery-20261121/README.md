# five-row-q6-q5-m23-m27-sd6-surgery-20261121

高速レーン・単一オーナー実験（宣言: `research/log/2026-11-21-five-row-q6-q5-m23-m27-sd6-surgery-single-owner-note.md`,
commit `ac118f45`, 2026-11-21T21:32Z）。**COMPLETED — 両キャンペーン完全負（局所）**。

## 目的

公開済みの五行前線 witness に対する sd≤2 negative を (≤3追加, ≤3削除) クラスまで拡張し、
前線盤での有界近傍を完全列挙する:

1. **(5,6)** 対象 5x23、シード = 公開 24石 m=22 witness（K0852・rows [4,5,5,5,5]）
2. **(5,5)** 対象 5x27、シード = 公開 19石 m=26 witness（five-row-q5-m26-extend-20261115・rows [3,4,4,4,4]）

## 機械と較正

- `surgery4.js`（md5 `7dc40fc0f08150692d64241d0c6c4029`・`sat.js` `0cc6021a4e523a0d7f4d5e0f5f5d40c`・
  `census4_check.js` `dadbeae1b02ad2a9650c6ce86021fb9c`）：four-row-q4-m35-surgery-20261115 から
  取得し md5 検証。列挙クラスは
  **{(A,R): |A|≤3, |R|≤3, R ⊆ A後の deficit 曲線上の石, |S∪A\R| ≤ targetMax}**
  （削除は deficit 曲線上の石に限り全 deficit を被覆。deficit 曲線外の自由削除は機械設計により
  スコープ外であり、その不在は主張しない）。
- targetMax = 満杯−1（q6: 24 = 5·5−1、q5: 19 = 5·4−1）により emit された maximal 配置は自動的に行欠損。

### 受入ゲート（全て PASS・`output/`）

- **C4 census 完全性**: (5,12,6)=212 / (5,15,5)=629 / (5,23,6)=996 / (5,27,5)=2355 曲線、
  両方向差集合 0（sat.js 全三点組 ≡ buildCensus4）。
- **シード健全性**: 両シードがホーム盤で sat.js `verifyConfig` PASS + census-free 独立 Python
  Fractions 検証器（`verify_general.py`・円の母点ベクトル誤りを訂正し tamper で陰性確認済み）PASS。
  追加の `safety_only.js`（sat.js primitives のみで safety を検査）も SAFE。
- **改ざん対照**: r=5 円 (中心 (5,5)) 上の 6点/5点合成配置 → 3系統すべて UNSAFE/FAIL。
- **not-maximal 対照**: 有効シードを広い対象盤に置くと `not-maximal` で FAIL（セル (22,0)/(26,0)）。
- **自己補完陽性対照**: シード先頭2石を除いた minus2 シードから (2,2) 予算でホーム盤手術 →
  q6: 公開 witness を正確に再発見（+近傍3つ、計4 witness）; q5: 公開 witness を
  唯一の witness として正確に再発見。優先枝刈りを通した機械が witness を見逃さないことの
  end-to-end 検証。

## 配置グリッドと矩形対称性

宣言グリッド: 各シードの bbox 鏡像 4種（id/H/V/HV）× 対象盤に収まる全平行移動
（5x23: offX 0..2 の 12配置、5x27: offX 0..7 の 32配置）。

**対称性簡約（補題・全称）**: 矩形の対称群 {id, y→4−y, x→m−1−x, 両方} は手術列挙クラス・
census・safety・maximality を不変に保つ。span s の bbox 鏡像では
**id@t = H@t、id@t = V@(m−s−t) = HV@(m−s−t)** が石集合として一致し、
12/32配置は 3類/8類に崩縮する（`output/symmetry_classes.txt`・assertion 検証済み）。
本実験は**全配置を実行**してこれを機械レベルでも検証した: 全 44 実行で
nRmLeaves/nP/nPpruned/nSafe/nMaximal/nWitness/nEmpty/nTprime がクラス内4実行すべて一致
（`output/class_consistency.txt`・11/11 クラス）。failStats の帰属順のみ列挙順依存で差異。

## 結果 — 完全負（不在主張ではない）

全 44 実行、`nWitness = 0`。合計 **174,178,268 final-state leaves**、すべて `nSafe = nRmLeaves`
（枝刈り L1〜L3 は safe 側で保存的）、`nMaximal = 0`。

### (5,6) 5x23（targetMax 24・census 996曲線）

| クラス | メンバー | nRmLeaves | nSafe | nMaximal | nWitness |
|---|---|---|---|---|---|
| t=0 | id@0, H@0, V@2, HV@2 | 5,162,142 | 同 | 0 | 0 |
| t=1 | id@1, H@1, V@1, HV@1 | 5,130,368 | 同 | 0 | 0 |
| t=2 | id@2, H@2, V@0, HV@0 | 5,175,265 | 同 | 0 | 0 |

計 61,871,100 leaves（12実行）。T′: t=0 {(22,0)}・t=1 {(0,0)}・t=2 {(0,0),(1,0)}（いずれも
シード bbox 外縁の未遮断セル）。

### (5,5) 5x27（targetMax 19・census 2355曲線）

| クラス | メンバー | nRmLeaves | nSafe | nMaximal | nWitness |
|---|---|---|---|---|---|
| t=0 | id@0, H@0, V@7, HV@7 | 3,522,581 | 同 | 0 | 0 |
| t=1 | id@1, H@1, V@6, HV@6 | 3,479,683 | 同 | 0 | 0 |
| t=2 | id@2, H@2, V@5, HV@5 | 3,432,887 | 同 | 0 | 0 |
| t=3 | id@3, H@3, V@4, HV@4 | 3,348,135 | 同 | 0 | 0 |
| t=4 | id@4, H@4, V@3, HV@3 | 3,517,536 | 同 | 0 | 0 |
| t=5 | id@5, H@5, V@2, HV@2 | 3,491,656 | 同 | 0 | 0 |
| t=6 | id@6, H@6, V@1, HV@1 | 3,691,525 | 同 | 0 | 0 |
| t=7 | id@7, H@7, V@0, HV@0 | 3,592,789 | 同 | 0 | 0 |

計 112,307,168 leaves（32実行）。

**系（導出・列挙クラスに関して全称）**: m=22 種（q6）・m=26 種（q5）の全 bbox 配置に対し、
(≤3追加, ≤3削減deficit被覆) の手術クラス内に 5x23/5x27 の deficient-maximal 配置（|F|≤24/19）
は存在しない。既存の sd≤2 negative（q6: 552,000 配置・q5: 4,651,200 編集）を sd≤(3,3) に拡張。
**5x23/5x27 全体の不在主張ではない**（deficit 曲線外の自由削除・|A|>3 の遠距離・
全く別種の配置は対象外）。M_{5,6} ∈ [23,249]・M_{5,5} ∈ [27,336] は不変。

## 決定論性

- id@0（q6）を2回実行: 全論理値が一致（差分は `elapsedMs` のみ）。
- これは環境リセット前の以前の実行（21:39Z・5,162,142 leaves @ 37.8s）とも
  leaf 数が一致、リセットを跨いだ再現。
- 各クラス4実行の全 key invariant 一致が独立の再現×4 を与える（44実行全体で冗長検証）。
- `output/records.jsonl`: 44実行の集計。生 JSONL は `output/campaign_q{6,5}/*.jsonl`
  （witness 行なし・summary 行のみ）。

## 成果物

- `scripts/`: surgery4.js, sat.js, census4_check.js（main から md5 検証取得）+ この実験の
  ラッパー（sat_verify.js = verifyConfig CLI, safety_only.js = safety のみ検査,
  verify_general.py = 独立 Python Fractions 検証器, gen_images.py = bbox 鏡像生成）。
- `seeds/`: seed_5x22_q6.json（K0852 witness）, seed_5x26_q5.json（m=26 witness）,
  *_minus2.json（自己補完対照用）, img_q6m22_{id,H,V,HV}.json, img_q5m26_{id,H,V,HV}.json
  （bbox正規化鏡像）, tamper_*.json（改ざん対照）。
- `output/`: census4_gates.txt, controls.txt, symmetry_classes.txt, class_consistency.txt,
  records.jsonl, selfcomplete_q{6,5}.jsonl, campaign_q6/（12 jsonl）, campaign_q5/（32 jsonl）。
- 生実行コマンド: `node scripts/surgery4.js 5 6 23 seeds/img_q6m22_id.json 3 3 24 <offX>` 等。

## スコープと次の課題

- この負は上記列挙クラスに関する局所命題。5x23/5x27 自体は open のまま
  （class-split レーン・SAT 前線の対象外資源）。
- 補論: sd≤(4,3)/(3,4) 部分クラス、および m=21（q6の3変種を含む）/m=25 種由来の
  異シード手術が、もし witness が遠距離ジャンプ構造（先行の sd≥14/≥15 観測）に
  反して近傍にあるなら効く候補。これらは今回の宣言スコープ外なので次レーンが宣言油田。
