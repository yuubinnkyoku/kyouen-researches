# 2026-11-27 (6,6) 6x26 class {0} krow/minpos decomposition: 単一オーナー宣言 (高速レーン)

## Status

- 宣言時 HEAD: `fe07ef8d` (2026-11-27T14:54:37Z)。着手前に最新 main を再取得済み。
- 単一オーナー宣言 (publish-then-execute)。本宣言より先の測定は 1 件も実行していない。
  事前に実施したのは器材較正のみ (下記「事前較正の開示」)。

## 前線の位置づけ

- **M_{6,6} ∈ [26, 495]**、前線 6x26 (K1217 witness 帯 m=5..25・6x26 は未解決)。
- kit `six-row-q6-m26-class-split-20261127` (commit `c4d2e9dbb0`) は class {2}
  krow=2:4 minpos 10..13 を 272s cap で 4 INDET (honest negative) で完了し、
  そのレジュームは「class {1} krow 分割・残クラス未走」を登録済み。
- 並走 lane との不交差:
  - class {2} minpos-REST (宣言 `e61acf82`・P∈{0..9,14..22})
  - class {1} krow=1:4 minpos P=0..11 全列挙 (宣言 `f9a982d2`・H鏡映で class {4} も被覆)
  - 6x23 q7 系2 lane (`f43cd66b`/`a8075223`)・REMO cap16 (`7a100862`)・
    4行 m24 lane (`855f52d8`)・W_24 dodecad (`05b3aa52`)
  - いずれも本宣言 (class {0}) には触れない。

## 本宣言

**6x26 q=6 class {0} (欠損行 = 行0のみ = 最上段エッジ行) を krow=0:4
(行0ちょうど4石・単一欠損 29石族) で固定し、minpos (行0の最左石位置) を
P=0..11 で完全に分割掃引する** (12 disjoint sub-instances)。

- sound H-split: 行0の4石 x1<x2<x3<x4 (xi∈0..25) に対し
  min(x1, 25−x4) ≤ 11 が常に成立する (x4 ≥ x1+3 より x1 ≥ 12 なら
  25−x4 ≤ 10) ので、P=0..11 は H鏡映合同類を除いた全列挙。
- V鏡映 (行反転) で class {0} ≡ class {5} であり、本掃引は行5エッジ行族も被覆。
- 残る未掃引 (本宣言対象外): multi-deficiency class・krow k≤3 の深欠損族・6x27。

## 器材

- `sat3.js`/`sat2.js`/`sat.js`: m26 class-split kit 出版 byte (sha256
  `e04581eb…`/`14ceb854…`/`fcc0cfd8…`)。宣言前に sha 照合済み。
- kissat 4.0.4 公式 linux-amd64 (sha256
  `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93e1`)。
  宣言前に sha 照合済み (公式 release asset zip sha256 `63282e51…` から展開)。
- CNF は再生成 (size policy・非出版)。生ログ・records.jsonl・meta json を出版。
- 1 probe = 1 kissat invocation・272s cap (SIGTERM)・最大2並走 (2-core)。

## 事前較正の開示 (宣言前実施・目標測定なし)

- エンコーダ決定性: 6x26 q=6 class{2} krow=2:4 minpos=11 の CNF 再生成で
  meta (vars 58,722 / clauses 205,674) が出版値と一致。
- class{0} krow=0:4 のエンコード動作確認 (minpos=11/22 で生成)。
  目標 sub-instance の SAT/UNSAT 判定は 1 件も実行していない。

## 較正 (事前登録・宣言後実行)

- 陽性対照: 6x25 q=6 class {2} krow=2:4 minpos=11 は出版値
  **SAT 3,574,244 conflicts の bit-exact 再生**を合格条件とする
  (m26 kit `output/r6x25q6_c2k4p11.txt`・K1217)。
- 追加観察 (対照に準ずる bookkeeping): 6x25 q=6 class {0} krow=0:4
  minpos=11 の 1 probe。既知幅 (m=25) に対する class {0} の応答記録であり、
  M_{6,6} の下界には影響しない (M ≥ 26 は既知)。

## 受入条件

1. 陽性対照 bit-exact 再生。
2. 全12 probe は各 272s cap・kissat 1走ずつ。
3. SAT の場合: witness 復号 + `verifyConfig` (sat.js) と fresh Fraction 検証器
   `verify_frac.py` (sha256 `837fe24b…`) の二系統 PASS + 負制御
   (1石除去で非極大・1石追加で拒否) + cold pair 再現。
4. INDET は honest negative (不在主張でない)。

## 判定

- **SAT なら M_{6,6} ∈ [27, 495] に前線更新**・witness を出版。
- 全 INDET なら M_{6,6} ∈ [26, 495] 不変・前線 6x26 のまま
  (class {0} エッジ行単一欠損族の cap 内 honest negative)。

## Not claimed

- 個別 INDET は不在主張でない。multi-class・krow k≤3・6x27 は対象外。
- (6,q≠6)・w 行族・Grundy・11×11 は一切不消費 (全時点 UNKNOWN)。
  verdict 不消費・conflicts は bookkeeping。
