# 単一オーナー宣言: 7行 q=4 witness band の幅69+ 延伸（全基底 2-for-2 近傍完全列挙・holes 拡張・チェーン続行）

- 宣言時刻: 2026-11-21T20:40Z
- 宣言時 HEAD: `94fe399ca64b6bcd6ae497e1fe8dc4601702ff18`
- レーン: 高速レーン（自実行）
- 前段: K0827 は現在 **M_{7,4} ∈ [69, 1929]**（witness band m=4..68・上界は K0068 の T_7 = 1929）。
  幅68は seven-row-q4-witness-band-60plus-20261121（同日第二バッチ）が全199基底の fresh 2-for-2
  完全列挙で一意 witness を発見済み。同 README/K0827 が明記した次の実行可能課題
  「**幅69 witness 探索（3-for-3 近傍・seeded SA・frontier の breadth 拡大・holes モード併用）**」のうち
  「全199基底による breadth 拡大 fresh 2-for-2」と「holes モード併用」を本宣言の対象として取得する。
  （幅68 witness 単一基数の fresh 2-for-2 = 0件は既刊 `stats_69.json` のとおり・未実施は残り198基数分。）

## 対象・手段（すべて有限的な witness 存在探索のみ）

1. **既刊全199基底（anchors + 幅61..67 チェーン witness・正準化重複除去済み pool）に対する
   fresh 2-for-2 完全列挙**を幅 69 で実行する。列挙器は pinned `enum_two.js`
   （`seven-row-q4-witness-band-60plus-20261121/scripts/`・出版計数較正済み）を byte 不変で使用する。
   事前較正（本セッション実施済み・出版値と完全一致）: base53@57 = 1,436,643 / 60,921 / 2、
   幅68 witness@69（fresh）= 2,141,205 / 199,290 / 0（`stats_69.json` bit-exact）。
2. **holes モード 2-for-2**（fresh の真上位集合・除去石位置の再充填を許す）を同じく幅 69 で全基底に実行する。
3. 併せて **1-for-0**（19石型 [3,3,3,3,3,2,2] の直接極大性判定・両欠損行の全空セル被覆）を全基底で判定する。
4. witness が発見された場合のみ、**チェーン続行**（fresh 2-for-2・frontier cap 10・greedy 幅順で
   幅 70+ への反復）を出版済みチェーン policy と同一手法で行う。
5. 発見 witness は **空列延伸可能性**（free-column extension）も機械確認する。

## 受入条件（本レーンの出版は以下を満たす場合のみ）

1. pinned 原版（`seven-row-q4-witness-band-60plus-20261121/` 全ファイル・`seven-row-q4-width59-two-swap-20261115/`）
   は 1 byte も変更しない。新規ツール・出力は新規実験 dir
   `research/experiments/seven-row-q4-witness-band-69plus-20261121/` のみに置く。既存実験 dir への追記はしない。
2. witness の独立性: pinned `verify_witnesses.py`（正規化整数直線・円方程式・新規一般化ファイル）と
   pinned `verify_third.py`（素朴 4x4 行列式第三系・新規一般化ファイル）の2系統で
   safe + 極大 + 行欠損を検証する。浮動小数点は使わない。負対照（1石摂動 → not-maximal）も検証する。
3. 主張は「有限幅の witness による下界更新」のみ。**幅69以上のいかなる不存在主張もしない**。
   2-for-2（fresh/holes 併用・全199基底）の 0件結果は列挙範囲を明記した honest negative として記録する。
   M_{7,4} の上界 1929 は不変。witness band の幅単調性は主張しない。3-for-3 以上は本宣言の対象外。
4. K0827 の更新（title の band 上端と artifacts・追記）は幅 69 以降の witness が独立検証を通過した場合のみ行う。
   不発の場合は session log に honest negative として残し、K0827 と knowledge README は更新しない。
5. 他レーンの着手宣言ファイルに触れない。four-row q5 m23（`d6b478ba`）・four-row q6 reconcile（`df64d850`）・
   six-row q4 m47（`ad2c411d`）・s12/s13 layer-3（`c75ae49d`）・(5,4) m41（`cdd3b80e`）・
   six-row m25/31/22（`5bf4c7a5`）・n11 系・K1058 はすべて非接触。
6. 出版は part 分割・各回 fetch-back byte 照合（commit 固定・blob sha1 両側再計算）。
   push 直前に必ず最新 main を再取得し、push 競合・同時書き込み・取得失敗時は無理せず状況を記録して次回へ回す。
7. 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は本レーンと無関係で UNKNOWN のまま。
   nodes・conflicts・候補数を勝敗として読まない。

## 想定する成果物

- 新規実験 dir: README（結果・方法・較正・限界・再現手順）、scripts/（公平な bundle: sweep 幅69 driver、
  holes/1-for-0 拡張、検証器一般化）、output/（per-base 列挙結果 JSONL・witness JSON・検証 JSON・honest negatives）。
- 進展があった場合: K0827 更新（追記 + title）+ 研究ログ（session log）+ knowledge README の
  固定幅bullet の M_{7,4} 区間表記の最小限更新。不発の場合: session log のみ。
