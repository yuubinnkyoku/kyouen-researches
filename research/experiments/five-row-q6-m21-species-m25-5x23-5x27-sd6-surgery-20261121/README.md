# five-row-q6-m21-species-m25-5x23-5x27-sd6-surgery-20261121

高速レーン・単一オーナー実験（宣言: `research/log/2026-11-21-five-row-q6-m21-species-m25-5x23-5x27-sd6-surgery-single-owner-note.md`,
commit `5c4cfca9`, 2026-11-21T22:21Z）。**COMPLETED — 両キャンペーン完全負（局所）**。
親実験 `five-row-q6-q5-m23-m27-sd6-surgery-20261121`（commit `c2010307`・m=22/m=26 種）
の witness 種拡張版。

## 目的

親実験で「m=22 witness（q6）・m=26 witness（q5）」に対して取った sd≤6 bounded surgery
負を、前線の**全公開 witness 種**に拡張する:

1. **(5,6)** 対象 5x23、シード = 公開 m=21 witness 種 3種:
   K0815 24石 5x21 witness（seed_w56_21）+ 公開 sd≤2 変種
   （varA: (10,2)→(11,2), varB: (10,2)→(12,2), `verify_variants_5x21.json`）。
2. **(5,5)** 対象 5x27、シード = 公開 m=25 19石 witness（`five-row-q5-m26-extend-20261115` w25）。

これにより 5x23/5x27 前線盤の sd≤(3追加,3削除) 近傍は、公開済みの全五行前線種
（m=22, m=21×3, m=26, m=25）を網羅したことになる。

## 機械と較正

- `surgery4.js`（md5 `7dc40fc0f08150692d64241d0c6c4029`）+ `sat.js`
  （`0cc6021a4e523a0d7f4d5e0f5f5d40c`）+ `census4_check.js`
  （`dadbeae1b02ad2a9650c6ce86021fb9c`）: 親実験と同一 binaries（md5 検証）。
  列挙クラスも同一: **{(A,R): |A|≤3, |R|≤3, R ⊆ deficit 曲線上の石, |S∪A\R| ≤ targetMax}**
  （削除は deficit 曲線上の石に限る。deficit 曲線外の自由削除はスコープ外、不在は主張しない）。
- targetMax = 満杯−1（q6: 24 = 5·5−1、q5: 19 = 5·4−1）。

### 受入ゲート（全て PASS・`output/`）

1. **census gates 再実行**（宣言条件2）: (5,23,6)=996 / (5,27,5)=2355 曲線、
   両方向差 0（`census4_gates.txt`）。親実験の 4 ゲート値と一致。
2. **シード健全性**（宣言条件1）: 4 種すべてホーム盤で sat.js `verifyConfig` PASS +
   独立 Python Fractions 検証器 `verify_general.py` PASS + `safety_only.js` SAFE
   （`seedverify.txt`・12チェック）。
3. **自己補完陽性対照**（宣言条件3）: 各種の minus-2 シード（ホーム盤・(2,2) 予算）で
   公開 witness 集合を再発見（`selfcomplete.txt`・`selfcomplete_seed_*.jsonl`）。
   見つかった witness 数は m21_m21: 1 / varA: 2 / varB: 2 / m25: 2 で、
   全ケースで元種を正確に含む（exact-orig=True の機械検証）。
   優先枝刈りを通した機械が公開 witness を見逃さないことの end-to-end 検証。
4. **来歴・構成検査**（`provenance.txt`）: seed_w56_21.json / verify_variants_5x21.json /
   w25.json は raw main 取得と byte-identical。種構成（正規化一致・スワップ座標）と
   全 16 鏡像ファイルを機械再計算で検証。

## 配置グリッド: 宣言からの訂正

宣言ノートは "3 classes for 5x23 span-21 seeds" と記したが、これは**誤り**:
m=21 witness 種の実際の bbox 幅は **18**（x∈[0,17]、w25 側は幅 20 のまま）であり、
5x23 に収まる平行移動は offX = 0..5 の **6 类**（m=22 種の span 21/3 类と混同した
ドラフト時の計算誤り）。本実験は宣言 3 类のスーパーグリッドである**完全 6 类**
を実行した（fail-closed 規則上、部分グリッドで負を出版するより完全掃引が正しい）。
q5 は宣言通り span 20 → offX 0..7 の 8 类。

**対称性クラス roster**（`output/symmetry_classes.txt`・全称 assertion 検証）:
span s、盤幅 m で class t = {id@t, H@t(rowFlip), V@(m−s−t)(colFlip), HV@(m−s−t)}
（石集合としての盤対称一致。5x23/s=18 は m−s=5、5x27/s=20 は m−s=7）:
- q6: 3種 × 6クラス。交差確認は m21_m21 class t=0 の 4 メンバー全実行。
- q5: 1種 × 8クラス。交差確認は m25 class t=0 の 4 メンバー全実行。
選定配置 3種+1種の代表点実行と各キャンペーン 1 クラスの全メンバー一致で
親実験の矩形対称性簡約（4:1）を新しい span でも機械検証。

## 結果 — 完全負（不在主張ではない）

全 32 実行（q6 21 = 3種×6代表 + 交差3、q5 11 = 8代表 + 交差3）、`nWitness = 0`、
`nMaximal = 0`、全実行で `nSafe = nRmLeaves`。合計 **162,581,176 final-state leaves**
（q6 108,861,233 / q5 53,719,943）。

### (5,6) 5x23（targetMax 24・census 996曲線）— nRmLeaves / nMaximal=0 / nWitness=0

| 種 \ offX | t=0 | t=1 | t=2 | t=3 | t=4 | t=5 | 小計 |
|---|---|---|---|---|---|---|---|
| m21_m21 | 5,095,913 | 5,038,121 | 4,985,291 | 5,019,705 | 5,060,022 | 5,095,421 | 30,294,473 |
| m21_varA | 5,265,165 | 5,206,935 | 5,156,064 | 5,187,340 | 5,225,708 | 5,256,699 | 31,297,911 |
| m21_varB | 5,383,934 | 5,324,310 | 5,273,046 | 5,300,139 | 5,335,318 | 5,364,363 | 31,981,110 |

交差確認（m21_m21 class t=0: H@0, V@5, HV@5）: 各 5,095,913 = id@0 と完全一致
（nP/nPpruned/nEmpty/nTprime も一致）。q6 計 108,861,233 leaves。

種間で leaf 数は単調: m21_m21 < varA < varB（約 +2.4%..+5.7%）。
nP は全配置・全種で 125,671 固定（P 候補集合のサイズは石数と行プロファイルで決まり、
deficit 構造の平行移動不変性の反映）。

### (5,5) 5x27（targetMax 19・census 2355曲線）— nRmLeaves / nMaximal=0 / nWitness=0

| offX | t=0 | t=1 | t=2 | t=3 | t=4 | t=5 | t=6 | t=7 | 小計 |
|---|---|---|---|---|---|---|---|---|---|
| m25 | 4,920,056 | 4,901,060 | 4,869,582 | 4,844,006 | 4,843,832 | 4,840,212 | 4,860,541 | 4,880,486 | 38,959,775 |

交差確認（class t=0: H@0, V@7, HV@7）: 各 4,920,056 = id@0 と完全一致。
q5 計 53,719,943 leaves。nP は全配置で 260,246 固定。

**系（導出・列挙クラスに関して全称）**: 公開済みの全五行前線 witness 種
（m=22〔親実験〕, m=21 original・varA・varB〔本実験〕; m=26〔親実験〕, m=25〔本実験〕）
の全 bbox 配置に対し、(≤3追加, ≤3削減deficit被覆) の手術クラス内に
5x23/5x27 の deficient-maximal 配置（|F|≤24/19）は存在しない。
**5x23/5x27 全体の不在主張ではない**（deficit 曲線外の自由削除・|A|>3 の遠距離・
全く別種の配置は対象外）。M_{5,6} ∈ [23,249]・M_{5,5} ∈ [27,336] は不変
（csv の note/source 列のみ拡張）。

witness jump の先行観測（m22 witness と m21 種の sd≥14、m26/m25 間 sd≥15）とも整合:
前線種の近傍は引き続き空。

## 決定論性

- m21_m21 id@0: 前セッション（22:26Z・セッション中断時）の実行 5,095,913 と
  本セッション再実行 5,095,913 が完全一致（セッションまたぎの再現）。
- m25 id@0: 2 回実行で leaf 数一致。
- 交差クラスの 4 メンバー一致が独立の再現×4 を与える。
  （差分は elapsedMs と failStats 帰属列挙順のみ、いずれも設計通り。）
- `output/records.jsonl`: 34 実行の集計（内 2 実行は決定性ダブル、集計 `<double: true>`）。

## 成果物

- `scripts/`: surgery4.js, sat.js, census4_check.js（親実験と同一 md5）+
  sat_verify.js, safety_only.js, verify_general.py, gen_images.py（親実験から継承）+
  check_symmetry.py（対称性 assertion）, aggregate.py（records/class_consistency 生成）,
  make_manifest.py（manifest 生成）。
- `seeds/`: 4 種 + *_minus2.json（自己補完対照用）+ 16 img_seed_*.json
  （bbox正規化鏡像）+ 来歴正本 3 件（seed_w56_21.json, verify_variants_5x21.json, w25.json）。
- `output/`: census4_gates.txt, seedverify.txt, provenance.txt, symmetry_classes.txt,
  class_consistency.txt, records.jsonl, selfcomplete.txt + selfcomplete_seed_*.jsonl ×4,
  q6camp/（22 jsonl: 21 実行 + 1 決定性ダブル）, q5camp/（12 jsonl: 11 実行 + 1 ダブル）。
- 生実行コマンド: q6 `node scripts/surgery4.js 5 6 23 seeds/img_seed_m21_m21_id.json 3 3 24 <offX>`、
  q5 `node scripts/surgery4.js 5 5 27 seeds/img_seed_m25_q5_id.json 3 3 19 <offX>`、
  交差 `... img_seed_m21_m21_H.json 3 3 24 0` / `... img_seed_m25_q5_V.json 3 3 19 7` 等。
  `python3 scripts/check_symmetry.py && python3 scripts/aggregate.py` で検証・集計再現。

## スコープと次の課題

- この負は上記列挙クラスに関する局所命題。5x23/5x27 自体は open のまま
  （class-split / SAT レーンの対象）。
- これで「全公開前線種 × 全 bbox 配置 × sd≤6（deficit 制限）」が五行前線 2 盤で
  完走した。残る高速価値は (a) sd≤(4,3)/(3,4) 部分クラス（nP ~125,671 → ~4倍、
  単発 2-3分予想）・(b) deficit 制限なしの自由削除クラス（機械拡張が必要）。
- m21 種・m25 種の新しい負は「前線 witness 間の jump ≥14 石」先行観測（親実験の
  m22/m21 間 sd≥14・m26/m25 間 sd≥15 測定）を sd≤6 近傍の全域で裏付ける:
  連続幅 witness は近傍手術では飛び出せない。
