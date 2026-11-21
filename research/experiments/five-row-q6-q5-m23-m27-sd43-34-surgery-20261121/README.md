# five-row-q6-q5-m23-m27-sd43-34-surgery-20261121

高速レーン・単一オーナー実験（宣言: `research/log/2026-11-21-five-row-q6-q5-m23-m27-sd43-34-surgery-single-owner-note.md`,
commit `0b2a6466`, 2026-11-21T22:45Z）。**COMPLETED — 両予算・両キャンペーン完全負（局所）**。

## 目的

完了済みの sd≤(3,3) 前線手術キャンペーン（commit `c2010307`,
`five-row-q6-q5-m23-m27-sd6-surgery-20261121`）を隣接する有界編集クラスへ拡張する:

1. **(≤4追加, ≤3削除)**: maxP=4, maxRm=3
2. **(≤3追加, ≤4削除)**: maxP=3, maxRm=4

シード・対象盤・targetMax は親実験と同一:
- `(5,6)` 対象 5x23、シード = 公開 24石 m=22 witness（K0852）、targetMax=24
- `(5,5)` 対象 5x27、シード = 公開 19石 m=26 witness、targetMax=19

列挙クラスの意味は親実験と同一（削除は deficit 曲線上の石に限り全 deficit を被覆。
自由削除・deficit 曲線外はスコープ外。全域不在主張ではない）。

## 機械と較正

- `surgery4.js`（md5 `7dc40fc0f08150692d64241d0c6c4029`・`sat.js` `0cc6021a4e523a0d7f4d5e0f5f5d40c`・
  `census4_check.js` `dadbeae1b02ad2a9650c6ce86021fb9c`）: 親実験の pin と同一 byte（md5 再検証）。
- **C4 census gates**: (5,12,6)=212 / (5,15,5)=629 / (5,23,6)=996 / (5,27,5)=2355、両方向差集合 0
  （`output/census4_gates.txt`）。
- **シード健全性**: 両シードがホーム盤（5x22/5x26）で `sat_verify.js` PASS + `safety_only.js` SAFE +
  独立 Python Fractions 検証器 `verify_general.py` PASS。
- **改ざん対照**: 合成 6点/5点円配置 → 3系統すべて UNSAFE/FAIL。
- **not-maximal 対照**: ホーム盤のシードを対象盤に置くと `not-maximal` FAIL
  （セル (22,0)/(26,0)）。targetMax−1 設計どおり。
- **自己補完陽性対照**: minus2 シードから (2,2) 予算ホーム盤手術で q6=4 witness
  （公開 witness 含む）/ q5=1 witness（公開 witness ちょうど）を再発見
  （`output/selfcomplete_q{6,5}.jsonl`・親実験の結果に一致）。

## 配置グリッド: 対称性クラス代表のみ

親実験で全配置レベル機械検証済みの矩形対称性クラス縮約補題
（span s の bbox で id@t = H@t、id@t = V@(m−s−t) = HV@(m−s−t)、予算非依存）により、
5x23 は 3類（id@t, t=0..2）、5x27 は 8類（id@t, t=0..7）の**クラス代表のみ**を実行。
補題は各キャンペーン各予算で1メンバーの交差検証（q6: V@2〔クラス t=0〕・q5: HV@7〔クラス t=0〕）
で鍵不変量一致を再確認し、代表 1実行は決定論性再実行で論理値一致を確認した
（`output/class_consistency.txt`・全8組 consistent・nP/nPpruned/nRmLeaves/nSafe/nMaximal/nWitness/nEmpty/nTprime）。

## 結果 — 完全負（不在主張ではない）

全 22 クラス代表 + 4 交差検査 + 4 決定論性再実行 = 30 実行、すべて `nWitness = 0`・`nMaximal = 0`
（枝刈りは safe 側で保存的・`nSafe = nRmLeaves`）。クラス代表合計 **348,154,586 final-state leaves**
（(4,3): 64,886,186 / (3,4): 284,268,400）。

### (5,6) 5x23（targetMax 24・census 996 曲線）

| 予算 | t=0 | t=1 | t=2 | total | witness |
|---|---|---|---|---|---|
| (4,3) | 8,283,468 | 8,283,718 | 8,328,833 | 24,896,019 | 0 |
| (3,4) | 32,446,931 | 32,238,048 | 31,829,950 | 96,514,929 | 0 |

(4,3) 実行 55-60s。nP は 125,671 → **2,786,101**（第4追加点で C(91,⋅) 帯に拡大・
枝刈り L1-L3 が 95.4% を safe 側で刈る）。(3,4) 実行 222-242s。nP は (3,3) と同じ 125,671 だが nPpruned は 59,642 → 59,159
（pAddOK 枝刈り条件 cnt+addCnt+1−maxRm≤q−1 が maxRm に依存するためで設計どおり）。
nRmLeaves は (3,3) id@0 の 5,162,142 に対し 6.29×（32,446,931）。

### (5,5) 5x27（targetMax 19・census 2355 曲線）

| 予算 | t=0..7 leaves | total | witness |
|---|---|---|---|
| (4,3) | 4,926,346 / 4,891,725 / 4,841,399 / 4,691,040 / 4,716,575 / 4,782,933 / 4,933,936 / 5,206,213 | 39,990,167 | 0 |
| (3,4) | 22,588,388 / 22,657,314 / 22,745,123 / 22,835,504 / 24,566,687 / 24,098,226 / 25,155,549 / 23,106,680 | 187,753,471 | 0 |

(4,3) 実行 49-54s・nP = 260,246 → 7,385,056（×28.4）。(3,4) 実行 209-262s（nP/nPpruned は maxP 不変のため (3,3) と同一の 260,246/125,585）・nRmLeaves は (3,3) id@0 の 3,522,581 に対し 6.41×。

### 系（列挙クラスに関して全称）

m=22 種（q6）・m=26 種（q5）の全 bbox 配置（対称性クラスを法として代表が全クラスを被覆）に対し、
(≤4追加, ≤3削除deficit被覆) と (≤3追加, ≤4削除deficit被覆) の手術クラス内に
5x23/5x27 の deficient-maximal 配置（|F|≤24/19）は存在しない。親実験の sd≤(3,3) negative を
sd≤(4,3) ∪ sd≤(3,4) に拡張。**それでも 5x23/5x27 全体の不在主張ではない**
（自由削除・遠距離編集・別種の配置は対象外）。**M_{5,6} ∈ [23,249]・M_{5,5} ∈ [27,336] は不変**。

予算1段増あたりの増幅の実測（親→今回）: 第4追加点で nP ×22.2（q6: 125,671→2,786,101）〜
×28.4（q5: 260,246→7,385,056）、第4削除レベルで nRmLeaves ×6.3-6.4。次段 (4,4)/(5,3)/(3,5) は nRmLeaves ×6.3・nP ×20-60 の
積で単発 40-80 分級となり、本レーンの単発壁（~262s）の向こう側。

## 運用上の正直面

- `(3,4) q5 id@5` の1回目の実行はインフラ障害（Koyeb remote command sync 失敗・ラン自体は無関係）
  で失われた。同一コマンドを fresh に再実行して完走（invariant はクラス内で独立に整合）。
- 全 (3,4) 実行は 209-262s で、wall budget 262s 内に収まった（budget-limited INDETERMINATE なし）。

## 決定論性

- 各キャンペーン各予算で代表 id@0 を2回実行し、全論理不変量一致（`output/class_consistency.txt`
  の rerun-vs-original 4組。差分は elapsedMs のみ）。
- 交差検査 4 組（V@2 q6・HV@7 q5・両予算）も id@0 と全論理不変量一致で、
  対称性補題が予算 (4,3)/(3,4) でも成り立つことを機械確認。

## 生コマンド

```
node scripts/census4_check.js 5,12,6 5,15,5 5,23,6 5,27,5
node scripts/sat_verify.js 5 22 6 seeds/seed_5x22_q6.json
node scripts/safety_only.js 6 seeds/seed_5x22_q6.json
python3 scripts/verify_general.py 5 6 seeds/seed_5x22_q6.json
node scripts/surgery4.js 5 6 22 seeds/seed_5x22_q6_minus2.json 2 2 24    # self-completion ctrl
node scripts/surgery4.js 5 6 23 seeds/img_q6m22_id.json 4 3 24 0          # q6 (4,3) class rep t=0
node scripts/surgery4.js 5 6 23 seeds/img_q6m22_id.json 3 4 24 1          # q6 (3,4) class rep t=1
node scripts/surgery4.js 5 6 23 seeds/img_q6m22_V.json 4 3 24 2          # q6 crosscheck V@2
node scripts/surgery4.js 5 5 27 seeds/img_q5m26_id.json 4 3 19 7          # q5 (4,3) class rep t=7
node scripts/surgery4.js 5 5 27 seeds/img_q5m26_HV.json 3 4 19 7          # q5 crosscheck HV@7
python3 scripts/aggregate_sd43.py                                          # records.jsonl + class_consistency.txt
```

## 成果物

- `scripts/`: 上記マシン群 + `aggregate_sd43.py`（fail-closed 集計・全30 jsonl が summary 行ちょうど
  1行であること・witness 行ゼロ・交差検査/再実行不変量一致を assert）。
- `seeds/`: 親実験と同一の 14 ファイル（生 witness 2・minus2 2・bbox 鏡像 8・tamper 2）。
- `output/`: census4_gates.txt, controls.txt, selfcomplete_q{6,5}.jsonl,
  sweep43/{q6,q5}/, sweep34/{q6,q5}/（クラス代表+交差検査+再実行 jsonl 計30）,
  records.jsonl, class_consistency.txt。
- `manifest.json`: 全収録ファイルの sha256。
