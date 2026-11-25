# 6×24 q=6 witness band extension — class-split SAT（2026-11-21/22 高速レーン）

単一オーナー宣言: `research/log/2026-11-21-six-row-q6-m24-class-split-single-owner-note.md`（commit `12012dd3`）。

## 主張

1. **6×24 整数格子盤（q=6・q点共円/共線禁止・標準ルール）に行欠損の極大安全配置が存在する**:
   29石・行構成 [5,4,5,5,5,5]（class {1}・欠損行1）と 29石・行構成 [5,5,4,5,5,5]（class {2}・欠損行2）
   の2個の witness を SAT で発見・decode した。
2. したがって **(6,6) の witness 帯は m=24 まで伸び、M_{6,6} ∈ [25, 495]**（下界 24→25 の更新。
   上界は K0318 代入 U=495〔K0806〕不変）。K0815 dai-6 の 6×23 witness chain を1幅延長。
3. 2 witness は 6×24 矩形上の D4+平行移動の意味で既知の 6×23 witness（K0818 正氏対照
   `positive_control_6x23_class1_witness.json`）とも互いにも非合同（石集合正規化比較・機械確認）。
4. witness 側の追加構造観測: 両 witness の bbox 幅は22で、正規化後の純並進配置は
   6×22 / 6×23 / 6×24 の3幅すべてで極大安全（R(S)=24・crosscheck で 6×23 t=1 を Fraction 系で陽性再検証・
   同時に 6×25 の追い出し〔not maximal (22,1)〕も一致）。R>24 への純並進被覆はなし。
5. 6×25 は未決着: class {1}/{2} とも plain 250s と krow固定（k=4）260s で INDET
   （1,222,228 / 1,207,894 / 1,126,385 / 1,294,221 conflicts）。**不在主張はしない**（他33クラス未走査）。

## 被覆と走査状況

走査は行鏡映正準欠損クラス分割（K0818/K0819 と同一機材・全63非空クラスを35正準代表で被覆）。
宣言は全35クラスの完全判定を目標としたが、**class {2}（404,422 conflicts・95s）と
class {1}（1,837,912 conflicts・232s）が SAT で witness を発見した時点で主張（下界更新）が確定**したため、
残り32クラスの UNSAT 判定（6×24 の不在証明。宣言スキップ項3）は不要となり実行していない
（{012345} は 120s INDET 924,268 conflicts の honest negative を記録）。
M は「width ≥ m で witness 不在」が初めて成り立つ m なので、SAT 1件で下界が 25 に確定する。

## 機材と pin

- `scripts/sat3.js` sha256 `e04581eb…fbfc`（six-row-q8-m20-class-split-20261114 版・m19 版と byte 同一確認済み）
  + `sat2.js` `14ceb854…7da9` + `sat.js` `fcc0cfd8…dac1`（K0810 core・main から取得し sha256 照合）
- kissat 4.0.4 公式 `kissat-4.0.4-linux-amd64`（arminbiere/kissat rel-4.0.4・
  sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`）
- `scripts/translate_census2.py`: witness 石集合の抽象曲線（石対の直線・石三つ組の円・整数正規化キーで
  dedupe）→ BLOCKED cell 集合を1回前計算し、平行移動 covariant に幅別極大性を判定する高速 census。
  曲線は verify_py の列挙と同一原理（安全: 全曲線 ≤5石・maxOnCurve=5 を確認）。
- `scripts/verify_py_lib.py`: `verify_py.py`（K0818 版 Fraction 検証器）の import-safe 化
 （`if __name__ == '__main__'` ガードのみ追加・関数本体 byte 同一）。
- CNF は保存せず（容量削減・K0818 先例）。`node sat3.js 6 24 6 --class=D out.cnf` で決定的再生成可能。
  meta json に vars=48,720 / clauses=170,698（6×24）・vars=53,532 / clauses=187,522（6×25 plain
  ・krow固定版はそれぞれ meta 参照）を記録。

## 検証プロトコル（すべて PASS のみ本主張）

1. **census gate**: `buildCensus` 曲線数が published アンカー
   (5,12,6)=212 / (5,15,5)=629 / (5,23,6)=996 / (5,27,5)=2355 に 4/4 MATCH
   （五行 2026-11-21 レーンと共通アンカー）。6×24 q=6 = 2,088 曲線・6×23 = 1,890。
2. **陽性対照（bit-exact アンカー×2実行）**: 6×23 q=6 class{1} SAT・conflicts **77,932** が
   K0818 `positive_control_6x23_class1.txt` と bit 一致（実行環境リセットを挟んで2回とも同一）。
   decode 石集合が出版 witness（29石 rows [5,4,5,5,5,5]・modelVars 44,244）と完全一致。
3. **陰性対照**: 2×9 q=4 class{0} UNSAT・conflicts 517（M_{2,4}=9 と整合・2回とも bit 一致）。
4. **witness 2系統検証**: (a) sat.js verifyConfig（decode 内蔵・整数）ok、(b) verify_py.py Fraction 系
   `safe_maximal` True ok 29（両 witness）。**tamper 対照**: 1石を (23,0) に移動した石集合は
   Fraction 系で False 'unsafe 6'（q=6 円が生成）→ 検証器は fail loudly。extended 入力・結果は
   `witness/extended_verify_input.json`。
5. **合同性分類**: K1206 教訓に従い「新規 witness」主張の前に D4像+全並進 embedding で
   6×23 witness・相互の石集合比較を実施 → 非合同（結論: 2配置とも新規の石集合）。
6. **決定性**: 6×24 class{1} 2回とも SAT 1,837,912 conflicts・class{2} 2回とも SAT 404,422 conflicts
   （実行環境リセット挟み込み）。陽性・陰性対照も上記どおり2回一致。
7. **高速並進 census の交差検証**: translate_census2.py の判定を verify_py（Fraction）と
   4点で照合: (a) 6×24 home 2件（Fraction 主検証そのもの）・(b) 6×23 t=1 陽性一致・
   (c) 6×25 t=0 陰性一致（not maximal (22,1) 同一理由・`witness/crosscheck_*.json`）。

## 記録

- `output/records.jsonl`: 9行（6×24: {012345} INDET・{2} SAT×2run・{1} SAT×2run /
  6×25: {1} plain INDET・{2} plain INDET・{1} k4 INDET・{2} k4 INDET）。
- 生ログ: `output/c6x24q6_{1,2,0_1_2_3_4_5}.txt`・`output/c6x25q6_{1,2}.txt`・
  `output/c6x25q6_1_x--krow=1:4.txt`・`output/c6x25q6_2_x--krow=2:4.txt`。
- witness: `witness/w6x24_class1.json`・`witness/w6x24_class2.json`（decode+verify 検証込み）・
  `witness/census_class{1,2}.json`（並進census）・`witness/pub_6x23_witness.json`（出版正本のpin・787B）。

## 誤り是正（honest erratum）

1. **driver tag衝突バグ**: run_class.sh 初版は --krow 追加引数を TAG に反映せず、既存 plain CNF を
   再利用して再実行した（records に一時的に `extra:"--krow"` の誤ラベル行が混入・CNF は plain と同一）。
   誤ラベル行は records.jsonl から除外し、driver は追加引数を TAG に接尾する版へ修正した
   （00:11 の krow行は修正版・別CNF・tag接尾付き）。00:05 の `c6x25q6_{1,2}.txt` は
   この事故で plain CNF の誤ラベル再実行（260s cap・1,139,126/1,207,894...内1つは cap 到達値）として
   残置・records の plain 行（250s cap）と軌跡同一で wall-time 差のみ。
2. **低速検証器の落とし穴**: 初版 translate_census.py（Fraction 全走査）は1件あたり数十秒で
   300s bash cap を超え実行環境リセットを起こした。translate_census2.py（BLOCKED 前計算・整数）
   に置換し、全成果物は knowledge kit 直下に退避する設計に変更した上で再構築（成果の喪失なし・
   kit は生リセットを1回経験済みで全ファイル残存を確認）。

## 範囲と限界

- 有限機械計算。census は all-triples 構成で完全（chord-pair の不完全性問題は不発生）。
  「6×24 witness-free」などの不在主張は本実験の対象外（むしろ witness が見つかった）。
- M_{6,6} の確定には 6×25..494 の持続性判定（class-split 完全掃引の重装備）が残る。
- 6×25 の {1}/{2} INDET は cap 付き honest negative で不在を意味しない。残り33クラスは未走査。
- 標準 11×11 空盤・二石root・S2・class 1/2/4 は非接触（UNKNOWN のまま）。
  nodes数・conflicts数を勝敗として読まない。

## 再現

```sh
# census gates
node -e "...buildCensus anchors..."   # scripts/sat3.js 起動に同じ sat2.js/sat.js を同dirに
# 1クラス走査（CNF生成→kissat→JSONL追記）
bash scripts/run_class.sh 6 24 6 "1" 260 <absoutdir>
# witness decode
node scripts/sat3.js decode 6 24 6 output/c6x24q6_1.txt --json=witness.json
# 並進census
python3 scripts/translate_census2.py witness/w6x24_class1.json 6 70
```
