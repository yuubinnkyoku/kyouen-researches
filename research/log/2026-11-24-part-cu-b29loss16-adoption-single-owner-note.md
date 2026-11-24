# 2026-11-24 Part CU 単一オーナー宣言: batch-29 (class 2251) 16-LOSS canonical adoption 着手 — publish-then-execute

## レーン

batch-29 (class 2251, ab001..ab054) の現行証拠に対する **loss-only canonical adoption** の計画・実行・出版を単一オーナーとして着手する。

- 対象行: drive-1 takeover checkpoint 1/3 で2-pass node-exact に解決した16キー ab001..ab016 (全て result 2 = LOSS, budget 15M, nodes合計 57,463,971, status.log 16行全PASS)。
- BASE: Part CO canonical chain cache `854800f38349...` (6,301行, 158 WIN / 6,143 LOSS) とその reaudit 出力 (Part COの全体検証済み)。
- 増分: 上記16行のみ。BASE不在・非quarantine・canonical-safe を宣言前探査で機械確認済み (增量 = BASE + 16行 = 6,317行, 158 WIN / 6,159 LOSS)。
- batch-29 は **PARTIALLY probed**: 38キー ab017..ab054 は fileless UNPROBED で verdict を一切主張しない。**class 2251 は解放されない** (unknown cost children 54 -> 38)。probed集合上では full == loss (WIN行もEXHAUSTED行も1行も観測されていない) だが、batch全体の完全性は主張しない。
- verdict不消費。WIN行採用はscrutiny owner C++ pin `9193f5b6...` 専権 (batch-14residual q042 / batch-26 l028 / batch-28 35-WIN precedents)。**11×11 空盤は UNKNOWN のまま**。

## ラベルの経緯 (誠実記録)

本レーンは前回セッションで「Part CT」ラベルの使用を機械確認して予約していたが、並走セッションが 2026-11-24T00:02:51Z に別レーン (batch-28 class 5343 最終残EXHAUSTED aa050 の 30M reprobe) で Part CT を宣言・着手したため、ラベル空間の混同を避けて **Part CU** に変更した (observed HEAD `d06c4d92`; CU未使用は commit 全検索で機械確認済み)。レーン本体 (batch-29 / class 2251 adoption) への対抗宣言・接触はないことを同一HEADで機械確認した。

類似レーンの非接触確認: Part CS (batch-28 EXHAUSTED 4行 25M reprobe, 完了), Part CT (batch-28 aa050 30M reprobe, 着手), Part CR (batch-30 drive-1 third-impl, 完了), batch-30 drive-2 (宣言 `7aaa0525` のまま停滞, 非接触), K1274/K1275 (z=6/z=7 スライス, 高速レーン, 非接触)。

## 事前開示: 宣言前探査 (このsessionで実施済み)

1. batch-29 kit完全性: MANIFEST 71ファイル全sha一致 (kit MANIFEST `7c12423364a29284...`), status.log 16行全PASS (sha `6b877344b9abea34...`), raw在庫は ab001..ab016×{p1,p2} の32ファイルのみ (38 filelessキーにrawなし), takeover val-gate 4パターン×3ホスト (published-baseline / batch29-host / takeover-host) node-exact 4/4: (0, 2000000)×2, (2, 3,651,923), (2, 5,040,200)。
2. BASE (Part CO reaudit outputs) の再現: CO refresh script を本環境で再実行し `refresh-summary 4727fb2b991d...` / `closure-classes 9d3965d94db9...` / `per-root-coverage 8e6fb981ee63...` がbyte一致することを確認 (出版環境と機械等価)。
3. Part CU toolchain実装と予備実行: increment maker / byte-clone merger / refresh fork / delta extractor を作成し、本session tree上で maker・merger (selftest PASS + merge×3 byte同一)・refresh (出力byte一致)・extractor (全gate PASS, 2回実行で同一sha) を実行済み。これらの実行は sprerve として宣言値の観察に使われたものであり、公式実行は下記プロトコルで別treeから再実行しbyte一致を要求する。

## 事前開示pin (公式実行はこれらとbyte一致を要求; PART CU改訂後の現行値)

- increment: `bab011e376090f9f4732d63f0084f326ba72dada5cf699d5aabc7e014c29ae24` (16行)
- increments-manifest: `f9f58ee101d53f0598ee01c5c54d5b277797a9e882cfb478ab7f7b3010e191e0` (schema `b29loss16-increments-manifest-v1`, adopted_loss 16 / win 0 / exhausted 0 / fileless 38, full_packet_eq_loss_only=true with rationale, win_scenario_exists=false)
- merged cache: `30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4` (260,590B; 6,317行; 158 WIN / 6,159 LOSS; merger `907119610034...` selftest PASS)
- merge-audit run1/2/3: すべて `8f611fe171f0b34c813035e4cf0ff59447f2419909cbe9fceff1f7d7cb1c8252` (同一sha)
- reaudit outputs: refresh-summary `b60d71a29730f19a589a065b446664a80bdf1008e8493b25c7e11f43e8246543` / closure-classes `3019d37f72ac6a46672f0fd027eae1c42c708f6e68d082925d85243d64195754` / per-root-coverage `61dbd39af70405d69c808c65e31a57ea10393f66bd0f3c59100e7a4ef035a081` / probe-worklist `0d7474e1adfbdbc8db438605e3e36310c1d8e656ab8c92899183f29b870a931c` (worklistは体積の関係でcommitしないがshaで宣言し、refresh script再実行で誰でも再生成・照合可能)
- decomp-deltas: `3274a297f497360bea4e61eaa50c8c62cd0c22e0ec600940afddfc4409c69eaf` (schema `n11-b29loss16-adoption-decomp-deltas-v1`)
- 実験dir: `research/experiments/n11-centralreply-class2251-loss16-adoption-reaudit-20261123/` (scripts 4本 = maker `ba698098779c...` / merger `907119610034...` / refresh `4db0f7744e6e...` / extractor `34e3a9c795f5...`)
- batch-29入力: batch-keys `330c0b9f3166...` / status.log `6b877344b9abea34...` / kit MANIFEST `7c12423364a29284...` (いずれも既出版・変更せず)

## 宣言値 (機械観察済み, 公式実行で再照合)

- class_status_counts: excluded 390 / excluded_now 23 / free_now 38 / unknown 34,498 (両側とも不変; excluded_now flipなし; newly freeなし)
- closure表: class 2251 unknown_now 54 -> 38 (rank 35 -> 4)。他のunknown_now変化は holder のみ: 1181 (102 -> 101, rank 602 -> 568), 1182 (104 -> 103, rank 684 -> 661), 11426 (60 -> 59, rank 190 -> 152)。stable-unknown rank churn 125 (分布: unknown 122 / excluded_now 3, holderなし)。left {1945, 19645} / entered {386, 1044} (tie-swap, 同rank・同unknown集計; 機械観察)。anchors 23101 (1,1) / 1849 (2,1) / 16757 (3,29) 完全安定。行数 808 -> 808。
- metrics: joint greedy 38,310 -> 35,691; probe worklist 64,828 -> 64,809 (class 2251 serving rows 54 -> 38; 採用16キーは scenario worklist から消滅); group best options 2,119 (不変); update8 は不変 (resolved 141 / remaining 31,718; 採用16 s5 index は update8 baseline requirement と交差なし — 機械観察として記録); PRG (per-root greedy union) movers: root 16 (2,971 -> 2,970), root 37 (4,001 -> 3,852); roots_summary_moved 空; root 27 baseline 119/119 不変。
- holder union 48 (class 2251 own 16, 他47クラス own 1ずつ; membership: 15キー 4, ab010 3)。
- 既定のfail-closed gate群: status log (16行 strict PASS row, final `2026-11-23T21:52:15Z ab016 PASS 15000000,2,4258557`, ts window 21:43:13Z..21:52:15Z), manifest整合, val-gate 3ホスト byte比較, raw 2-pass一致 (16キー, node-exact, 合計57,463,971), increment == 16行ちょうど, scenario == BASE+16行, verdict counts 158/6,143 -> 158/6,159, fileless 38キーの increment/BASE/scenario/receipt 不在, transition全安定, closure/per-root/worklist 検証, ボード再検証込みstatus再計算 == 出版値。

## 実行プロトコル (この宣言の出版後に公式実行する; 全段階でbyte一致を要求)

1. **maker ×4**: スクラッチtree上で `make_increments_b29loss16.py` を4回実行し、毎回 increment `bab011e376090f9f...` / manifest `f9f58ee101d53f05...` とbyte一致。
2. **merger**: `s5_union_merge.py selftest` PASS + merge ×3 (merged cache `30ddad9dc0add7e2...` / audit `8f611fe171f0b34c...` ×3 同一)。
3. **refresh ×3 + 隔離実行**: `refresh_adoption_b29loss16.py` を3回 + 隔離実行 (`env -i`, 別tree, `PYTHONHASHSEED=random`) の計4回、出力4ファイルが宣言sha (`b60d71a29730...` ほか) とbyte一致。
4. **extractor ×4 + 隔離実行**: `compare_deltas_b29loss16_adoption.py` を4回 + 隔離実行、毎回全gate PASS かつ decomp-deltas `3274a297f497360b...` とbyte一致。
5. **tamper battery** (fail-closed捕捉を各1回以上確認, probe後は復元してclean pass再確認): (a) raw verdict flip (ab001 p1 result 2->1), (b) raw nodes drift (ab002 p2 nodes+1), (c) 隔離raw (ab010 p2のみ改変 → 2-pass mismatch), (d) kit MANIFEST 1行破壊, (e) BASE cache 1行改変 + merge (WIN/LOSS conflict or manifest cross-gate), (f) increment 1行 tamper + extractor, (g) manifest loss sha 再pin偽造 (verdict 1行書き換え) + extractor, (h) forged WIN行 increment混入 + merger (non-LOSS verdict gate), (i) filelessキー increment注入 + extractor, (j) status.log 1行改変 (nodes drift) + extractor, (k) val-gate takeover-host 1行改変 + extractor, (l) filelessパターン: scenario cacheへfilelessキー偽装挿入 (fileless gate)、 {m} refresh summary 1数値改変 (metric pin) + extractor, {n} closure csv 1行 rank改変 + extractor。
6. **出版 A-E** (main直接, 5 commit): A) scripts 4本, B) increment + manifest + merge-audits ×3, C) merged cache, D) reaudit outputs 3つ + decomp-deltas, E) README + MANIFEST-sha256 (出版対象明示リスト機械生成)。各commit後に commit-pinned raw URL で sha256 照合 (fetch-back検証)。

競合・対抗宣言・取得失敗が起きた場合は押し進げず、状況を記録して次回実行に回す。

## honest 事項

- 前sessionで extractor雛形の jsreplay pin を手転写した際に無効文字を混入し maker が fail-closed ABORT した。修正は機械抽出・機械置換で行った (本Partの成果物に手転写pinは残っていない; 全pinは filler script `sup/fill_extractor...` 系の機械抽出による。filler自体は実験ではなく本sessionの産物として completion logに開示)。
- batch-29 throughput: 採用16行で class 2251 の required probe set の 16/54 が消費され、closure rank 35 -> 4。残り38キーの解決 (別drive, 別宣言) が class 2251 解放の必要条件。
- このadoptionは update8 requirement を1つも解決しない (機械観察; scheduling別計算は改善)。

**11×11 空盤の勝敗は UNKNOWN のままである。**
