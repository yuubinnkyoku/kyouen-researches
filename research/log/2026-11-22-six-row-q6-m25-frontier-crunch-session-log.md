# 6×25 q=6 frontier crunch — session log（2026-11-22・中断レーンの採用セッション）

元宣言: `2026-11-22-six-row-q6-m25-single-owner-note.md`（commit `2c3254ef9f`・2026-11-22T00:26Z・
宣言時 HEAD `30c1d67cbd61a3896338c44e9f471376eaa33f39`）。
採用宣言: `2026-11-22-six-row-q6-m25-adopt-single-owner-note.md`（commit 本出版列の先頭・01:52Z）。

本 log は元宣言が予定した path に採用セッションが執筆した。元セッションの実行記録（00:21-00:52Z）は
kit `_q66-m25-crunch-kit`〔records.jsonl 7行・enc metas・out ログ・staged witness〕と本実験dirの
採用ファイル（verbatim）で保持する。採用セッションは元セッションの証跡に加えて、較正から独立再検証
まで全工程を自環境で実行した。

## 採用時の観察（2026-11-22T01:36Z）

- main HEAD: `2b7b4dbecb`（n11 s4bd merge addendum・01:33Z）。6×25 を含む出版・CSV 更新なし
  （CSV (6,6) 行は K1215 版のまま `25..495`）。
- kit `_q66-m25-crunch-kit`: records 7行（00:31:55Z class{1} krow=1:0 INDET・00:34 class{0} INDET・
  00:36 class{3} INDET・00:39 class{4} INDET・00:41 class{5} INDET・00:43 {0..5} INDET・
  00:47:37Z class{2} SAT 3,574,244 conflicts）+ rerun log（00:52:05Z）+ staged witness
  `w6x25_class2.json`（00:47:50Z）。
- 中断元セッションの宣言済み成果出版の Window は 00:52Z 以降 44 分以上開いており、採用規約
 （(6,5) 6×31 の `bc11e28b` 前例）に従い引き取りを開始。

## 採用セッションの実行（01:36-01:5xZ・HEAD `2b7b4dbecb` 時点の main から K1215 機材を取得）

1. **機材 pin 取得**: K1215 出版正本（`six-row-q6-m24-class-split-20261121`）の scripts 7件を
   commit 固定 raw URL で取得し MANIFEST.sha256 と全件照合（7/7 byte 一致）。kit の sat.js/sat2.js/
   sat3.js が出版 pin と byte 同一であることも確認。kissat 4.0.4 官 sha256 `21da5d984e38…` 照合。
2. **census gates**: (5,12,6)=212/(5,15,5)=629/(5,23,6)=996/(5,27,5)=2355 が 4/4 MATCH・
   6×23=1,890・6×24=2,088（K1215 同一）・6×25 = 2,302（新アンカー記録）。
3. **陽性対照**: 6×23 q=6 class{1} → SAT 77,932 conflicts。model v-line 全数が出版アンカーと
   byte-identical・decode JSON が出版 witness（sha256 `76656499…`）と byte-identical。
4. **陰性対照**: 2×9 q=4 class{0} → UNSAT 517 conflicts（M_{2,4}=9 と整合・タイミング行のみ差）。
5. **主インスタンス再構築**: `sat3.js 6 25 6 --class=2 --krow=2:4 --minpos=11` CNF 再生成が
   中断レーン CNF と sha256 一致（`46c485af…`）。**run3 コールドラン: SAT・conflicts 3,574,244・
   model が中断 pair（run1/run2）と byte-identical** → 決定性3連。
6. **2系統検証**: verifyConfig ok 29石 rows [5,5,4,5,5,5]・verify_py（Fraction）True ok 29。
   tamper 4種（石移動×2・石削除・石追加）すべて期待どおり FAIL。アンカー3 witness（6×24×2・6×23）
   も Fraction 系で True ok 29。decode JSON は staged witness と byte-identical。
7. **合同性**: 新 witness は 6×23 witness・K1215 6×24 class{1}/{2} のいずれとも非合同
  （D4+並進正規化・新規石集合）。
8. **並進 census**: bbox 23・maxOnCurve 5・R(S)=25（widths 23,24,25 被覆・firstFail 26）。
   Fraction 系との交差検査 4点（23t0 陽性・24t1 陽性・24t0 陰性 (23,2)・26t0 陰性 (23,2)）一致。
9. **出版**: 分割 push（宣言→実験 part→大ログ→MANIFEST→K1217→CSV→knowledge README bullet）。
   各 push 前に最新 main を再取得し、path 競合・HEAD 移動を確認する。

## 主張の帰結

- **6×25 witness（29石・class{2}・行構成 [5,5,4,5,5,5]）の存在** → **M_{6,6} ∈ [26, 495]**
 （下界 25→26・上界 U=495 不変）・6×26 が新 frontier。
- INDET 7行（class{1} krow=1:0・{0}/{3}/{4}/{5}/{0..5} plain・前レーンの class{1}/{2} plain+krow固定）
  は cap 到達 honest negatives で不在を意味しない。
- 6×24 t=1 embedding が6×24 class{2} と非合同な第3の石集合として同時に 6×24 witness 側にも
  新規観測を与えるが、6×24 の下界はすでに K1215 で決着済みのため書類上の影響なし。

## 知見

- krow 分解+minpos=11 の H-split が plain の 250-260s INDET 壁（3.5M conflicts 級）を実質 3.6M
  conflicts 内の SAT に変換。人数固定と左端ピンの組合せが class{2} には決定的に効いた（class{1} の
  krow=1:0 は 260s で 5.07M conflicts INDET・残る krow=1:1..1:3 未実行）。6×26 以降の追い込みも
  同型の分解（krow+minpos）から始めるのが定石候補。
- 採用再現の手順（pin 取得→較正→CNF 再生照合→コールドラン→2系統検証）は中断 staged witness の
 正当性を外部環境から再構成可能で、(6,5) 前例同等に機能した。

## 標準盤への非接触

標準 11×11 空盤・二石 root・S2・class 1/2/4 は本レーン非接触で UNKNOWN のまま。
conflicts 数・nodes 数を勝敗として読まない。
