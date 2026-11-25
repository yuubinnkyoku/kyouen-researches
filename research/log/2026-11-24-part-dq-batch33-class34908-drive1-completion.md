# Part DQ 完了ログ: batch-33 (closure class 34908) 54-key probe drive-1 — WIN-HALT 到達 (2026-11-24)

Part DQ 宣言 (`2026-11-24-part-dq-batch33-class34908-drive1-declaration.md`
`c8388b719e`) に基づく batch-33 probe の drive-1 が**事前登録済み終点
(distinct WIN 2行観測による WIN-HALT wave halt) に到達**したので完了を
記録する。実験dir:
`research/experiments/n11-centralreply-closure-class34908-batch33-20261124/`
(README・MANIFEST-sha256.txt・output/status.log・raw 47キー分・val-gate)。

## 最終集計 (status.log 正本から機械導出)

- probe 完了 47/54キー: **LOSS 41** / **WIN 2 (af029 s5 900646 nodes
  4,862,485・af047 s5 961976 nodes 9,841,975・いずれも 2-pass
  fresh-cold node-exact)** / **EXHAUSTED 4 (af003 153030・af023 810351・
  af034 93060・af039 950512・各 15,000,000 = honest UNKNOWN)**
- **UNPROBED 7 (af048..af054)**: wave halt 時点の残キー。af048 は
  p1 pass のみ完走 (`af048.p1.out` 出版済み)・p2 truncated・verdictなし。
- MISMATCH 0・worker timeout 2件 (af008, af039 p2) は pinned runner
  guard で自動再実行し解消。truncated 生pass 2ファイルは保管出版。
- 全出版物 fetch-back 機械検証 byte 一致 (171ファイル MANIFEST 収録)。

## 経過の正直開示

1. wave 1..12・各最大2キー・2 worker (2-core・repo規約内)。
2. **環境reset事故 1件**: af031 完了直後に sandbox 実行環境が reset され
   ローカル作業dir消失。main 増分出版 (inc1..inc3) から kit・status.log・
   raw を byte 復元 (runbatch `f591f8c2` / batch-keys `8a863381` /
   maker `5d65addd` pin 再照合) し、af030/af031 を fresh-cold 再実行で
   result・nodes 完全再現 (reset前後同一値)。**増分出版設計のreset耐性が
   実地で機能した**。以後 inc4・inc5 でさらに8+10キー分を保全。
3. af029 WIN を inc3 で即時出版・af047 WIN で wave halt (rc=45)・inc5 出版
   (af047.halt と af048 部分完走を正直記録)。
4. 増分 commit: inc1 `7324bb17` / inc2 `77c4f245` / inc3 `25522df3` /
   inc4 `bd013154` / inc5 `e39c5ff4`。

## verdict の取り扱い (規約どおり・不変)

- 41 LOSS行・2 WIN行・4 EXHAUSTED行は **honest label のまま不消費**。
  canonical adoption・closure table 再導出・reaudit は別 Part (Pinned
  merger `90711961…` 経由)。WIN行 scrutiny は C++ 第二実装 `9193f5b6…`
  専権。closure table membership 変動 (flips/newly_free) は別 reaudit。
- EXHAUSTED 4行の高budget再probe・UNPROBED 7キーの継続probe は次回以降の
  新宣言必須 (batch-33 drive-2 等として条件を再登録できる)。
- **標準11×11空盤・19 central-reply roots・二石root・S2・class 8730 /
  5804 / 34269・class 34908 を含む全クラスは全時点で UNKNOWN**。
  nodes数は bookkeeping。
