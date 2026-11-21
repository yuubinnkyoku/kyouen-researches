# 単一オーナー宣言: six-row (6,6) m=24 class-split 完全掃引 — 6×24 行欠損極大安全配置の存在判定（2026-11-21 高速レーン）

- 宣言時刻: 2026-11-21T23:50Z 前後
- 宣言時 HEAD: `64f2d6490814f3e85f48962786a82fe20e3f4e22`
- 実験 dir: `research/experiments/six-row-q6-m24-class-split-20261121/`
- セッション log: `research/log/2026-11-21-six-row-q6-m24-class-split-session-log.md`

## 位置づけ

K0815 は (6,6) の deficient 極大 witness を 6×23 まで拡張（29石 rows 5,4,5,5,5,5・8変種+分離1類）し、
`results/fixed-width/mwq_stabilization.csv` の (6,6) 行は **M_{6,6} ∈ [24, 495]**（上界は K0318 代入 U=495）・
「6x24 unresolved（kissat def-mode 260s not absence）」としている。6×24 のクラス分割掃引は
一度も実行されていない（Class 単位の非存在計算がない）。

本レーンは K0818/K0819 と同一の機材・同一の被覆論で **6×24 q=6 の全 35 正準行鏡映欠損クラス**を走査し、
6×24 の行欠損極大安全配置の存在/不在を機械的に判定する。

## スコープ（fail-closed）

1. 対象は 6×24 q=6 標準ルール盤のみ。行鏡映 y→5−y 正準欠損クラス 35 個
   （63 非空部分集合の鏡映簡約代表）を `sat3.js --class=D` で走査。
   それぞれのインスタンスは「rows∈D は ≤4 石（¬rowGe）、rows∉D はちょうど5石（rowGe）」+ 安全 + 極大。
2. {0} / {1}（および280s cap で収束しないその他の難クラス）は `--krow=y:k`（k=0..4）×
   `--minpos=p`（p ≤ floor((m−1)/2)=11・H 鏡映による sound split）へ分解して再走査可。
   難クラスには `--lex=H` 交差符号化再検査（H は class 保存で健全・V/HV は不使用）。
3. 主張の形式:
   - 全 35 クラス UNSAT ⇒ **6×24 に行欠損の極大安全配置は存在しない**（満容量 6×5=30石のみ）。
     M_{6,6} ∈ [24,495] は **{24} ∪ [26,495]** に細分化（K0821-audit 規約: M=25 は
     witness-free な幅 24 に witness を要求するので除外）。有限機械検証であり数論的証明ではない。
   - いずれかのクラス SAT ⇒ witness を decode し verifyConfig + Python Fraction 2系統で検証、
     **M_{6,6} ≥ 25**（下界のみ更新・CSV の M 列は同様に更新）。
   - 一部クラスが cap 内で決着しない場合、決着したクラスのみを scoped negative として記録し、
     6×24 の不在主張はしない（INDET 誠実記録・残は次回レーンへの引き継ぎ）。
4. CSV は判定結果に応じて (6,6) 行の note のみ追記更新（M 列・source は bounds 行の運用に従い
   下界が動いた場合のみ变更。下界不変の UNSAT 完結時は note 追記のみ）。
5. 11×11 空盤・二石 root・S2・class 1/2/4 は非接触（本レーンは 6×24 に限定）。

## 受入条件

1. **機材 pin（main から取得し sha256 照合）**: `sat3.js` sha256 `e04581eb9a252464d41503488c76ff742bc2306a2ae0e9a9c5c24e113933fbfc`
   （six-row-q8-m20-class-split-20261114 版 = m19 版と byte 同一を確認済み）・
   `sat2.js` `14ceb85414b56b1dd89a74c9a00fe29169ff19095da1df2a57b7f6606317da9e`・
   `sat.js` `fcc0cfd8bfc7497390369111a5523547c3873435336fdf21d60b39d66cf5dac1`・
   `verify_py.py` `0c21377650c63fb8d9bbd2506b4f5b817bc29c2ad216589e8fa3510667b9267e`。
   kissat 4.0.4 は公式リリース `kissat-4.0.4-linux-amd64.zip`（arminbiere/kissat rel-4.0.4・
   sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`）。
2. **陽性対照（bit-exact アンカー）**: 6×23 q=6 class{1} SAT・conflicts **77,932**（K0818
   `positive_control_6x23_class1.txt`）が同じ CNF から bit 一致で再現し、decode した witness 石集合が
   出版 `positive_control_6x23_class1_witness.json`（29石 rows 5,4,5,5,5,5）と一致すること。
3. **陰性対照**: 2×9 q=4 class{0} UNSAT（M_{2,4}=9 と整合・conflicts 517 前後）。
4. **census gate**: `buildCensus` の all-triples 曲線数が既知の published アンカー
   (5,12,6)=212 / (5,15,5)=629 / (5,23,6)=996 / (5,27,5)=2355 を再現すること
   （sat.js census のエンコーダ横断整合・q=6 family で同一実装系の five-row 2026-11-21 レーンと共通アンカー）。
5. **決定性**: 最難クラス（と指定した代表）は2回実行で conflicts 数一致。
6. **検証**: SAT witness が見つかった場合 `sat3.js decode` + `verify_py.py`（Fraction）2系統 PASS・
   tamper 陰性対照が両系統で FAIL すること。

## 並走との disjoint

- five-row (5,4) m=45 witness hunt（`59b1251aa7` 宣言・`research/experiments/five-row-q4-band-45plus-20261121/`）
- five-row q6/q5 m=23/m=27 sd≤(4,3)/(3,4) partial sweep（`0b2a6466fa` 宣言）
- n11 third-implementation bank full-band recalibration（`451e0fe8e4` 宣言）
- seven-row q4 band m69+ batch 2（`0265c39b00` / `c476182ae8`）

いずれも 6×24/q=6 に非接触。本宣言の対象は単一オーナー（本レーン）が独占する。
