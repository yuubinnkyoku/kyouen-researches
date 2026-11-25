# batch-38 第二実行環境検証 (n11 central-reply closure class 30345) 2026-11-25

単一オーナー Part EF（`research/experiments/n11-centralreply-closure-class30345-batch38-20261125/`・
2026-11-25 宣言 `16d7336e`）が main に出版した probe 証拠に対する、**別サンドボックス実行
（長期レーン・本検証実験）による独立再現検証**。verdict は一切消費しない
（WIN 行は scrutiny-owner C++ gate `9193f5b6…` 専権のまま・EXHAUSTED は honest UNKNOWN 継続）。
標準 11×11 空盤は **UNKNOWN のまま**。

## スコープと状態（本 run の最終版・wave V1）

- 対象: published batch-38 inc1–inc5（ai001..ai043・43キー・86 pass）。
- **本 run で完結した検証 scope は inc1–inc3 相当の 21キー（42 pass）**:
  fresh 再実行 node-exact 42/42（下記 §方法 6）。証拠は本ディレクトリの
  `output/raw/`（42件）と `output/status.log`（21キー分の本検証 PASS 行）。
- inc4–inc5 相当の 22キー（ai022..ai043・44 pass）の fresh 再実行は
  **実行環境の長時間 unavailable により中途で中断**した（ローカルで
  ai040/ai041/ai030/ai038/ai023/ai024 の 6キー node-exact 一致まで到達したが
  未出版のため証拠ではない）。**次回実行は wave V2 として published bytes
  から再構成のうえ 22キーを全面 fresh 再実行し**、この README（スコープと
  状態を最終版に更新）・MANIFEST-sha256・完了 log を追記出版する。
- 取得基準 HEAD: scripts/sources/val-gate/input は `7e411346`、
  inc4/5 の raws・status は `d4a1792c`（21キー分は両 HEAD で同一 byte）。

## 方法（全て main published bytes からの取得のみ・ローカル遺物不使用）

1. **キット byte 再構成**: scripts 4 本が宣言 pin と sha256 一致
   （jsreplay `84585617…`・runbatch `f591f8c2…`・drive38 fork
   `2bd91341…`・maker `9b117808…`）。sources 9 件も pin 一致（canonical cache `fc3e4ac9…`・
   closure-classes `27e00b0d…`・prior-probe-universe `6deee846…`・
   quarantine `81d23160…`・refresh-summary `6af660a1…`・worklist-extract
   `7fe55513…`・freshness-ranks1to12 `e5f51717…`・batch1-packet 2件）。
   input 50 件（ai001..ai049 + batch-keys-b38.json `29807104…`）・
   published raws 93 件（正規 86 + truncated sidecar 7）・status.log を取得。
2. **出版 maker をそのまま再実行**（隔離 tree・post-reset 環境で実施）:
   fail-closed gates G1–G7 + G3b ALL GATES PASS・再生成 49 input CSV と
   batch-keys-b38.json は published bytes と **49/49 + keys byte-identical**。
   fresh-frontier 選定（rank 12・50子 = 1 dual-class b018 不消費 + 49 fresh・
   ranks 1–11 fresh 0）が第二環境で完全再生。
3. **val-gate 4/4 node-exact**（本環境 fresh 実行・published baseline 対照）:
   2M×2（result 0・nodes 2,000,000）+ 15M×2（result 2・3,651,923 / 5,040,200）。
   wall_s のみ運用情報差（決定性比較から除外・出版 precedent どおり）。
4. **出版 evidence 内部整合** (`wrapper/crosscheck_published.py`・fail-closed):
   raws 86 件 × status PASS 行 43 の全突合 **0 件問題**（budget/result/nodes
   完全一致・p1/p2 同一・`# replay_done`・`# forbidden quadruples: 95670`・
   header 一定）・truncated sidecar 7 件は全て replay_done 欠落で
   TRUNCATED-RETRY 行 7 件と 1:1。
5. **fresh 再実行（主計算）**: published bytes そのままの pinned
   `runbatch.sh`（byte 変更なし）を 1 invocation = 1 key で起動する
   `wrapper/wrapper_worker.sh`（drive38 の WIN-CONTINUE worker semantics を
   再現・pinned script は無改変）で 2 worker（2-core host）実行。
   比較は `wrapper/compare_verify.py`（replay 行の wall_s 以外全
   フィールド + forbidden-quadruples header。fail-closed: 1 row でも不一致・
   欠落があれば rc=1・MY-RUN-MISSING 検出で割付漏れを機械捕捉）。
6. **inc1–inc3 21キー結果（post-reset fresh・最終）**: **42/42 pass
   node-exact（bad=0・0 MISMATCH・0 未完）**。ラベル分布一致: WIN 8
   （ai002/ai003/ai005/ai006/ai010/ai013/ai014/ai017・不消費）・LOSS 12・
   EXHAUSTED 1（ai007・honest UNKNOWN）。

## honest incidents（本実行内の失敗の全記録・出版証拠への影響ゼロ）

1. **サンドボックス環境リセット**: 検証中に環境リセットが発生し工作 dir を
   全喪失（Part EE wave F と同一障害モード）。リセット前に実施済みだった
   val-gate/maker/21キー再実行は**証拠として採用せず**（repo precedent:
   pre-reset 未出版 run は証拠扱いしない・Part EF inc3 の扱いと同一）、
   published bytes + sha pin からの再構成（raw curl のみ）で全工程を
   post-reset にやり直した。所要は再構成 ~3分 + val-gate ~1.5分 +
   21キー再実行 ~37分。
2. **worker 割付漏れ 3件（pre-reset ai008・post-reset ai003/ai018）**:
   割付表作成時のケアレスミス。いずれも `compare_verify.py` の
   MY-RUN-MISSING 検出（fail-closed）で即捕捉し fresh 実行で一致。
   **全キー網羅は比較機の fail-closed 検出に頼るのが有効**という再実証。
3. **runbatch 起動形態の誤り（検証開始直後に自己検出・pre-reset）**:
   複数キーを 1 invocation に渡すと WIN rc=45 で残キーが打ち切られる
   （drive38 は 1 invocation ≤ 2 key 前提）。per-key wrapper 構成に
   全面やり直し（pinned script 無改変）。
4. **比較スクリプトの wall_s フィールド index 誤り（pre-reset）**:
   field 9 = index 7 の取り違えで一時 42 row 誤 FIELDDIFF。修正後 42/42 OK。
5. **/proc pattern 誤 kill（pre-reset）**: 停止処理の文字列一致が実行中
   ツール自身の command text を捕まえ自己 kill。以後先頭一致 match に限定。
6. **実行環境の長時間 unavailable（本 run の終了要因）**: inc4–inc5 相当
   22キーの再実行中に失速し retry でも復帰しなかった。wave V1 は
   この時点で出版済み（commit-pinned raw fetch-back 51/51 一致）だったため
   出版証拠は完全・中断した未出版分を捨てるだけで済んだ
   （**成果は出版してから次の計算に着手する**運用の実証）。

## 標準担保

- **標準 11×11 空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・16371/20421/34908/30345 は全時点で UNKNOWN のまま。**
  nodes 数は bookkeeping・勝敗・被覆・secured coverage の主張はしない。
- 本検証は verdict を 1行も採用しておらず、closure 表・adoption には
  一切影響しない。WIN 行の消費判定は Part EG（JS 第三実装交叉検証・宣言
  `2a46008a`・完了 `4a753f52`・6/6 third-impl verdict agree + 実装同行）
  と scrutiny-owner C++ gate `9193f5b6…` が所有（本検証は未消費のまま）。
