# 単一オーナー宣言: 4行 q=6 witness-free band 第5次延伸 (m=35)

- 宣言時刻: 2026-11-28T00:30Z（本ファイル出版コミット時）
- 宣言時 HEAD: 最新 main 再取得後に記録（出版 commit に同じ）
- 先行 kit: `research/experiments/four-row-q6-q7-frontier-20261121/`（README「次の作業」が
  q=6 m=35 以降の掃引を明示的にレジューム課題としている・m=30..34 は第2..4次延伸で掃引済み）。
  本宣言の検索時点で m=35 を掃引する宣言・kit は main に存在しない（four-row q6 m35 の
  commit 検索 0 件）。m23 class-split レーン・m24 (4,5) レーン・3行 q4 m30 レーン・
  m>=32 jig レーン・6x26 四レーン・8x26 レーン・n11 コスト系には不参入。

## 予定する作業（publish-then-execute・本宣言以降に実行）

1. (4,35,6) def-mode（行欠損極大の非存在）を genfast3 census + pinned kissat 4.0.4 で
   2 回実行し、UNSAT かつ conflicts bit-exact を要求する。SAT の場合は witness を
   3 系統検証（sat.js verifyConfig / verify_witness.py / verify3.py）して出版する。
2. UNSAT なら witness-free band は 16..35 に伸び、M_{4,6} = 16 or ∈ [36,103] に尖鋭化。
   実行時間が許せば m=36 を同様に掃引（第6次延伸として同一 kit に追記）。
   sec_cap は null（上限なし・nohup 単独実行で bash 実行時間上限を回避）。
3. verdict は records 追記（append_records 型の fail-closed gate）で正本化し、
   K1177 に追記する。witness-free 主張は有限機械掃引のみに基づき、全称 tail は
   K0318 (U_{4,6}=103) による既存の上界引用のまま。

## 較正（宣言前に実施・開示）

- pinned kissat 4.0.4 linux-amd64 md5 `3a5eba830aa6008a604fcc9bbe99a325` を再取得し一致。
- genfast3.js md5 `12c2bd9cb3b24887fc3896f7ea9bcadf`（four-row-q7-stabilization-closure
  正本）・sat2.js md5 `282ae832efa0080127c6c153e65e1c3c`・sat.js md5
  `0cc6021a4e523a0d7f4d5ea0f5f5d40c`（four-row-q6-q7-frontier 正本）を再取得し一致。
- (4,33,6) def CNF 再生成 md5 `bf058f40f6bd70a4f00ddfdf72f01f72` が出版較正 pin
  （q6ext4/calib_4x33q6_genfast3.json）と byte 一致（generator gate）。
- (4,34,6) def CNF 再生成（md5 `1f58cdfc895ef4de493528ebf40d33f2`）を pinned kissat で
  再実行し、出版 solve log（UNSAT・conflicts 4,480,309・process-time 311.94s）との
  conflicts bit-exact を親band対照として要求（宣言後に完了確認して開示）。
- (4,35,6) CNF 生成 meta: curves 1128 / vars 24,908 / clauses 86,625・gen 0.1s。

## 器材 pin

genfast3.js `12c2bd9cb3b24887fc3896f7ea9bcadf` + core sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c` /
sat2.js `282ae832efa0080127c6c153e65e1c3c`・kissat 4.0.4 linux-amd64 md5 `3a5eba830aa6008a604fcc9bbe99a325`。

## 同一性・不参入

- 4行 (4,5) m23/m24 レーン・q=4 m35 レーン・3行 q=4 (m30 SAT / m>=32 jig) レーン・
  5行・6行・7行・8行各レーン・n11 コスト系・ultra-cheap 系に不参入。
- conflicts 数は勝敗ではなく bookkeeping。**verdict NOT consumed・標準 11x11 空盤・
  19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は
  全時点 UNKNOWN。**
- push 競合・取得失敗時は無理せず記録して次回の実行に回す。
