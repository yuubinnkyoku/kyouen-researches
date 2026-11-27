# 七行 q=4 幅70 holes two-edit 延伸 — 完了ログ (2026-11-27)

単一オーナー宣言 `2026-11-27-seven-row-q4-w70-holes-single-owner.md`
（宣言時 HEAD `02e40e9e`）の下で publish-then-execute により実施した、
幅69 完全 two-edit 近傍掃引（K0827 追記 2026-11-27）の幅70 holes 延伸。

## 結果（全て有限観測・局所負記録）

- **w70 holes 2-for-2 全199基底完全掃引**: 448,782,213 row-capacity 候補 /
  48,971,845 safe / **0 safe maximal row-deficient**（run1 集計・run2 と
  199/199 レコード一致（ms 除く））。holes は fresh の真上位集合のため、
  同じ基底の幅70 fresh 2-for-2 負も従属する。
- **D4鏡像×並進census（幅70目標）**: 並進被覆最大幅は変わらず **67**
  （幅65チェーン基底）・幅70を被覆する純並進 witness なし（0 hits）。
- **M_{7,4} ∈ [69, 1929] 不変**・csv 不更新・不在主張なし・前線 7×69。

## 較正・検証（全て機械生成・all_pass true）

1. pinned base53 7×57 fresh: 1,436,643/60,921/2 出版値完全再現。
2. 幅68 witness 基底の幅69 fresh: 2,141,205/199,290/0 出版 stats_69 と同一。
3. 陽性対照: 23 個の w65 基底の幅68 fresh でちょうど3基底がちょうど1件・
   すべて出版の唯一の幅68 witness と同一。
4. 機械交差照合: 出版済み幅69 holes 記録 199/199 の完全コールド再現
   （tag/sig/rcc/safe/shape_errors/maximal 全一致・総計
   435,695,973/45,368,697/0 も再現）。
5. 決定性: 幅70 holes 2全走 199/199 一致（ms 除く）。
6. tamper: 基底石1つ移動・1つ削除とも fail-closed（`unsafe base`）。

## 正直な開示

- 環境 reset 2 回（作業 tree を消した。知識マウント
  `_w70holes/` に再構築し、bases/enum/census は main から再 fetch して
  sha256 pin（`d8e977ec…` / `ab58c34a…`）を再検証した。出版内容への
  影響なし）。
- 初版 driver の wall-budget bug（タイマーを基底ごとにリセットするため
  予算が発火せず、1 invocation が shell timeout で 98 レコード書き込み後
  kill された）。修正は「基底間でどこで止まるか」のみを変え、列挙には
  一切触れない。当該 98 レコードは resume でそのまま run1 に再利用され、
  run2 全走との一致で検証済み。
- 計算は宣言後・出版前に実行（宣言は publish-then-execute 方式）。

## 次の実行可能課題（このレーンの引継ぎ）

- 幅69 witness の seeded SA 探索（幅68 witness seed・別 seed 群）。
- 3-for-3 近傍（fresh・幅69）: 計算量は 2-for-2 の ~50-100 倍見込みで
  重い。構造枝刈りなしでは長期レーン行き。
- 幅70 holes を幅71 へ延伸するか、frontier breadth 拡大（新 seed 系統）。
- `results/fixed-width/mwq_stabilization.csv` は不更新のまま。

**標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手
{100,108}・S2・全 closure class は全時点 UNKNOWN・verdict 不消費・
counters は bookkeeping。**
