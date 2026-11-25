# Part EF batch-38 第二実行環境検証 (wave V1: inc1–inc3 21キー node-exact 完了・inc4–inc5 は環境障害で中断) (2026-11-25)

単一オーナー Part EF（batch-38 = closure class 30345 fresh 49-key probe・
2026-11-25 宣言 `16d7336e`）の inc1–inc3 出版証拠（ai001..ai021・21キー）を
**別サンドボックス実行（長期レーン・本実行）から独立に全件検証し、42/42 pass
node-exact を確認、証拠一式を検証実験として出版した**記録。本実行は EF の
data push を所有実行に譲り検証に転換した（Part EE wave F `dda65bbb` と同じ
価値最大化ルート・single-owner 尊重）。標準 11×11 空盤は **UNKNOWN のまま**。

## 出版 chain

1. **wave V1 commit `614f58ff`**（51 files）: 検証実験
   `research/experiments/n11-centralreply-closure-class30345-batch38-secondenv-verification-20261125/`
   （README + wrapper 3 scripts + val-gate-fresh 4 + output/status.log +
   output/raw 42件 = 本環境 fresh 再実行の第二実行環境 raws・wall_s は
   本環境実測値）。**commit-pinned raw fetch-back 51/51 byte-identical**。
2. **本 commit**: README 改訂（スコープを inc1–inc3 完了・inc4–inc5 中断の
   最終版に確定）+ 本 log。

## 検証結果（全て main published bytes からの再構成のみ）

- キット byte 再構成: scripts 4 + sources 9 + batch1-packet 2 + input 50 が
  宣言 pin と sha256 一致（取得基準 HEAD `7e411346`・inc4/5 raws は
  `d4a1792c`）。
- 出版 maker 再実行（隔離 tree）: G1–G7 + G3b **ALL GATES PASS**・49 inputs +
  batch-keys-b38.json（`29807104…`）byte-identical。fresh-frontier 選定
  （rank 12・ranks 1–11 fresh 0・50子 = b018 prior 1 + fresh 49）完全再生。
- val-gate 4/4 node-exact（2M×2・15M×2）。
- 出版 evidence 内部整合（`wrapper/crosscheck_published.py`）: 86 raws ×
  43 status 行 0 件問題・truncated sidecar 7 は replay_done 欠落で
  TRUNCATED-RETRY 7 行と 1:1。
- **inc1–inc3 21キー fresh 再実行: 42/42 node-exact**（pinned
  `runbatch.sh` byte 変更なし・1 invocation = 1 key wrapper・2 worker。
  WIN 8 不消費・LOSS 12・EXHAUSTED 1 honest UNKNOWN・ラベル分布一致）。
- inc4–inc5 22キー: 再実行は環境障害で中断。**本 run の検証 scope は
  inc1–inc3 まで。ai022..ai043 は本 log では検証済みと数えない。**

## 運用知見（今回 new）

1. **第二実行環境検証の成果物は raw 含めて出版するのがリセット耐性上
   有利**: wave V1 出版後の環境障害（filesystem rollback 失敗・長時間
   unavailable）でも失われたのは未出版の inc4–5 再実行分のみで、
   検証証拠本体は main 上で保全された。検証ログのみ出版していた
   wave F 前例から、証拠粒度を raw まで上げた意義の実証。
2. **割付表の人手作成は欠落がつきもの**: ai008（pre-reset）・ai003/ai018
   （post-reset）の 3件 漏れは常に `compare_verify.py` の MY-RUN-MISSING
   fail-closed 検出で捕捉された。割付は比較機の網羅検出に任せる。
3. **runbatch.sh は 1 invocation = 1 key が正しい使い方**（WIN rc=45 で
   invocation 全体が止まる設計・drive38 の semantics が前提）。
   複数キーを渡す検証構成は WIN で黙って打ち切られる。
4. 環境は 1 run 内で 2 回の障害（リセット・unavailable）に見舞われたが、
   いずれも「published bytes + sha pin からの再構成」で工程を失わず
   再開できた（所要: 再構成 ~3分）。

## レジューム（次回実行・着手前に必ず最新 main 再取得）

1. **本検証実験の wave V2**（最重要・single-owner: 本 secondenv 検証
   実験dir は本実行が owner）: inc4–inc5 22キー（ai022..ai043・published
   @ `d4a1792c` 以降の最新 batch-38 status/raws を再取得して確認）を
   全面 fresh 再実行（per-key wrapper・2 worker・`compare_verify.py` で
   86 row 全突合）し、output/raw 44件 + status 追記 + README（§スコープと
   状態を全 43キー検証完了に更新）+ MANIFEST-sha256 + 完了 log を出版。
   実行時間目安: ~45–50 分（422M nodes・2 worker）。batch-38 inc6
   （ai044–ai049・未出版なら）も含めてよい。
2. Part EF（batch-38 owner 実行）の batch-38 続き・Part EG 完了済み
   （`4a753f52`・6/6 third-impl 一致・verdict 不消費は C++ gate 待ち）・
   Part EH（batch-39・単一オーナー進行中）には関与しない。
3. **標準 11×11 空盤・19 central-reply roots・二石root {49,60}/{59,60}・
   S2 {59,60}・class 1/2/4・16371/20421/34908/30345 は全時点で UNKNOWN の
   まま。nodes は bookkeeping・勝敗・被覆・secured coverage の主張はしない。**
