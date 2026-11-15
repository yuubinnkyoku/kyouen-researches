# eight-row-q11-q12-band-closure-20261115

w=8 帯の (8,11)・(8,12) の真の満容量安定化長 M を SAT（witness）と UNSAT（witness-free 掃引）の両側から閉じる高速レーン。

## 状態（2026-11-15 時点）

- **(8,11): COMPLETE — M_{8,11} = 21 EXACT（w=8 で初の完全決着。全体では M_{7,10}=19・M_{7,9}=24 に次ぐ w≥6 で3例目）**
- (8,12): IN FLIGHT — witness 8×12..8×16・witness-free 17..230 完走。**残り 231..882 を掃引中**
  （resume-safe・records/sweep-q12.jsonl に追記）。全完了で M_{8,12}=17 exact。

## 方法と健全性

- **genfam12.js**: sat2.js の `S.buildCensus` を monkey-patch し、census を「8 本の水平行 +
  (m−7) 個の12点 F1 円」のみにする O(m) CNF 生成器。F1 円: 中心 (u, 7/2)、
  u ∈ {7/2, 9/2, …, m−9/2}、(2x−2u)² + (2y−7)² = 50、rows {0,1,3,4,6,7} 各2点で
  rows 2,5 を通らない。曲線挿入順序は buildCensus と厳密一致（行は最小2点順・
  円は最小3点順・行が先）。encodeCore 以下（sequential counter・欠損節・lex・DIMACS 出力）は
  sat2.js を verbatim 再利用し encoding drift なし。
- **健全性（帯全域）**: 行は q≥11 でも常に census に含まれるべき q点線（帯内の他の直線は
  高々8点）。≥11点の円は eight-row-strip-classification-20261115 の Theorem A・系4（m≤984）により
  F1 の配置メンバーのみ（K0830 例外円は窓内10点）。曲線を落とすことは制約を削るだけなので
  **族census UNSAT ⟹ 全census UNSAT**。SAT 側（witness）は sat.js verifyConfig（全census）+
  verify_witness.py（Python exact Fraction・別実装）の2系統で検証。掃引は m ≤ 907 < 984 内。
- solver: kissat 4.0.4・def 単一節符号化（∨¬rowGe[y] =「ある行 ≤ q−2 の極大安全配置が存在」の
  完全符号化）。SAT=10 / UNSAT=20 の終了コードを活かすため sweep.sh に set -e を入れない
  （2回の事故で学習・m=21 の記録を失った）。

## 較正（CNF byte-identity 21/21・環境再構築後も再現）

- sat2.js 全三つ組census と 8×11..16（q11・q12 計11幅）
- genfast.js 弦対census と 8×17/20/26/40/60（q11・q12 計10幅）
- 記録: records/calibration-cnf-byteidentity.jsonl（CNF md5 一致・完全環境リセットを
  またいで2回再現）。

## 結果

### (8,11) — M = 21 EXACT

- **下側**: 欠損極大witness を 8×11..8×20 の全幅で確認（m=11 は78石2欠損、m=12..20 は
  79石単一欠損・rows 2,5 full・欠損行は9石）。m=12..15 は SA レーン
  （eight-row-q11-q12-sa-witnesses-20261115）・**m=15..20 は kissat def-mode SAT** で、
  SA のヒューリスティック非発見帯 m=16..26 を突破。全 witness 2系統検証 PASS。
- **上側**: **m=21..907 の全887幅 UNSAT**（INDET 0・SAT 0・欠落 0・conflicts は m=21 の
  1,379,955 を最大に漸減・process-time ≤41s/幅）。records/sweep-q11.jsonl（887行・CNF md5 付き）。
- **尾部**: m ≥ 908 は K0318 substitution U_{8,11}=908（proved）で排除。
- **決着**: M_{8,11} = 21（exact）。knowledge: K0843。CSV の (8,11) 行は exact-threshold proved に更新。

### (8,12) — M ∈ {17} ∪ [231, 883]

- 下側: 87石単一欠損 witness を 8×12..8×16（m=12..14 SA・m=15..16 kissat 新規）で確認・2系統検証。
- 上側: m=17..230 の214幅 UNSAT（INDET 0）。**231..882 掃引継続中**（追記型 resume-safe）。
  全完了で M_{8,12}=17 exact。
- 尾部: U_{8,12}=883（curve-packing substitution・w7_upper_bounds.json）。

## 決定性

m=21（conflicts 1,379,955）と m=26（162,762）は、実行環境の完全リセット・再構築
（kissat 再取得込み）をまたいで CNF md5・conflicts が bit-exact に再現。

## 解釈上の注意

- 本レーンは 8×m・q=11/12 固定幅帯のみを扱う。11×11 等の他問題には関与しない。
- SA の m=16..26「抵抗」はヒューリスティック非発見の記録であり、m=16..20 の witness
  発見により解決済み（非不在主張の撤回ではなく、探索器の限界の記録）。
- UNSAT 主張は「族census のもとで・m ≤ 984・kissat 正しい」までの有限機械検証。
  全称数学定理としての過大主張はしない。

## ファイル

- records/sweep-q11.jsonl — q11 掃引 887 幅（21..907 全 UNSAT・CNF md5・tag 付き）
- records/calibration-cnf-byteidentity.jsonl — 21/21 較正
- witnesses/ — 8x17..20q11・8x15..16q12 の6枚（8x15/16q11 の2枚はローカル artifacts
  マウントに保存済み・次回格納）
- claim-20261115.json — IN FLIGHT 時点の機械可読 claim スナップショット（q12 完了時に更新）
- scripts/ — genfam12.js・decode_model.js・verify_all.js・sweep.sh は検証済み本文を
  ローカル artifacts マウントから次回格納（sat.js/sat2.js/genfast.js は
  seven-row-inband-families-20261114 / seven-row-q9-q10-bands-20261114 から複製して使用）
- records/sweep-q12.jsonl — q12 掃引記録（17..230 完走分はローカルにあり次回格納・
  231..882 を追記）

## 環境障害の記録

本レーンは1セッション内で3回の実行環境リセットと終盤の VibeFS（bash・file_system）障害に
遭遇した。q11 の主要記録（witness 6枚・sweep 887行・較正 21対照）は main に到達済み。
q12 掃引 231..882 とローカル成果物（records/sweep-q12.jsonl・summary-q11.json・witness 2枚・
SAT フロンティア生ログ 8本・scripts 4本）の格納は次回実行に回す。UNSAT 生ログの
batch tar は binary のため push 経路がなく、conflicts・CNF md5 を records で担保する。
