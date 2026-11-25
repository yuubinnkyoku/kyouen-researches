# 研究log: fold22 WIN8-D10 receipt fold root 840500（2026-11-20）

単一オーナー宣言（commit `29e6195803`・先行出版）に基づく実行記録。
前段: 同一レーン実行で fold21（K1130・root `80880200`・残余 38 → 35）を出版（commits `7dfe1005` → part2 `eba6e55c` → part3 `0f3021cd` → index `aad742c7`）。本 fold は出版済みの K1125 証明書（root `00000000000000801202000000840500`・29,468 行 1,067,425 bytes・SHA-256 `21ad6195…`・19 gate 監査正本 `06c65f76…`・実験 `n11-residual45-win8-cert-extract-root840500-20261120`）の receipt fold であり、fold21 正本（残余35 baseline）の続きに接続する。第29 receipt・12番目の WIN8 receipt fold。

## 実行環境リセットと隔離 W の再構築

本実行は途中で実行環境がリセットされ、前段実行で構築していた隔離 W（W21）が失われた。しかし本レーンの設計により
chain 入力一式はすべて repo に出版済みであるため、(1) fold21 出版機が持つ PINS（12 blob SHA-1）+ PIN256（40 SHA-256）を
`ast.literal_eval` で正本から直接パースし、(2) W 相対パス → repo 出版パスの対応表に従って raw で全ファイル再取得し、
(3) fold18/19/20 出版機・fold18 preverified 写し（fold19 出版実験 `n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/` 配下・
SHA-256 pin と照合）も再配置して、W22 を再構築した。再構築 W22 上で fold21 出版機を pristine 実行し、
出力が出版 fold21 正本（`9a4da2f6…`）と byte-identical（約 6.8 秒・52 pin 全照合）であることを最初に確認した。
重要証拠が再現不能なローカル状態に依存しないことの実証例である。

## 事前検証と設計決定

1. **fold21 baseline の確定**: 上記のとおり再構築 W22 上で fold21 出版機（SHA-256 `44399cc5…`）を再実行し、出版正本と byte-identical であることを確認してから着手した。
2. **候補機械比較（単一オーナー宣言ノートに記録・fold23 以降の選定基準としても記録）**: fold21 適用後 open 6,136 行 / 486,243 cost に対して出版済み WIN8 候補 K1123（root `00000000020809002000480100000`）・K1125（root `00000000000000801202000000840500`）の 6 石部分幾何 28 正準行を機械分類した。K1123 は open 4 行（主張 3 + 余剰 1・cost 321）・K1125 は **open 6 行（主張 3 + 余剰 3・cost 484・影響 4 親すべて class 2）**。fold21 の閉鎖 8 行は両根と不交差（closed-by-fold21 0・機械確認）。frontier 削減最大として K1125 を fold22 に選定した。
3. **K1125 材料の取得と pin 突合**: K1125 監査正本（SHA-256 `06c65f7611b7fea17131d5e13b28792aee1b7d723e7b8cdb1cb3b54012282886`）と証明書本体（`21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc`・29,468 行・1,067,425 bytes・raw 取得時 SHA 照合）を W22 に配置し、19 gate の全 detail（g01 K1089 master pin `808fbda1…`・g05 mobility 58・g06 uncapped probes andclose1 736,409 / andclose0 878,391〔loss=true・終端石数 [14,18]〕・g07 主張 3 行 `…801202000000800100`/`…801202000000800400`/`…801202000000840000`・g08 probe 再現 pilot_d6 4, reproduced 2/2・g13 nodes A1 2,310,103 / B 1,984,636・g16 miss 0/extra 0〔third_method terminal 9,810・visited 59,990・winner 38,458・loser 11,722・応手辺 52,360〕・g17 Bareiss 58 subroot 三方法一致・g19 K1097 pin `2896deb0…`・footprint claimed == intrinsic == 3 行）を取得時点で機械読み込みした。
4. **主張 3 行の residual35 内 open 性の事前確認**: K1125 主張 3 行が fold21 正本の residual 35 行に全て含まれること、fold21 の閉鎖 8 行と不交差であることを事前機械確認した。
5. **fold22 機の生成**: `build_fold22.py`（全置換が出現回数 assert で機械検証・stale 定数 grep・py_compile・ast 解析）で fold21 出版機（SHA-256 `44399cc5…`）から変換生成（1,148 行・約 8.1 秒/実行）。変換内容: (a) header/env/OUT/ROOT_HEX/CERT_RELPATH 差し替え (b) PIN256 に fold21 正本・K1125 監査・K1125 証明書の 3 pin 追加（計 43 SHA-256 pin・12 blob pin と合わせ 55 pin） (c) fold20 rerun gate 部を fold21 chaining + **fold21 pristine rerun gate** に置換（隔離 W 複写・FOLD21_W・出力 SHA が fold21 正本 pin `9a4da2f6…` と一致で gate・失敗時 fail-close） (d) K1124 gate ブロックを K1125 ブロックに全面差し替え（全定数は K1125 監査正本から機械取得） (e) open35/residualSet35 適用・solved 基準 1,712・closedAllNew 基準 77・残の会計 35−3・win16 5→4 根/12→9 行 (f) closedHistorical に rows21 を追加 (g) stale 定数検査の誤陽性 1 件（`FOLD21_W' は fold21 rerun gate の W21X 隔離複写が合法使用）を生成段階で修正。K1124 の残存参照は fold21 rerun gate 推移的再検証用 pin・controls 行のみ（allowlist）。

## 結果

- receipt は **open 6 行**を閉じた:
  K1089/K1125/K1097 主張 3 行（target 内）`00000000000000801202000000800100`（cost 75・unswept・c2×2 需要行）・`00000000000000801202000000800400`（cost 74・unswept・c2×2 需要行）・`00000000000000801202000000840000`（cost 73・unswept・c2×2 需要行）+
  **target 外 open 3 行** `00000000000000801202000000000500`（cost 87・c2×2）・`00000000000000801202000000040100`（cost 89・c2×2）・`00000000000000801202000000040400`（cost 86・c2×2）〔いずれも unswept・同じrootのC(8,6)部分集合幾何に内在〕。
  余剰 3 行は主張から分離して正確に記録した（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 484・5親 target 77 → **80/112**・残余 35 → **32** 行・frontier 6,136/486,243 → **6,130/485,759**・solved S6 1,712 → 1,718・incidence 11,683 → 11,671（影響 4 parent・すべて class 2〔`…3800000008002000` 14→11・`…801202000000000100` 51→48・`…801202000000000400` 47→44・`…801202000000040000` 69→66〕・完全閉鎖 0。parent-delta 計 12 == incidence 減分）・s6_needed 4,444 → 4,438・cost_needed 352,691 → 352,207。
- 6石部分幾何28行: open-frontier 6（本receiptで閉鎖）・not-in-worklist 22・closed-before-this-receipt 0（fold21 閉鎖 8 行との不交差と整合）。
- win16 候補 5 → **4 根**（主張 12 → 9 行）。残余23行掃引計画は不変（全win16主張と不交差を機械再確認）。
- 出力 SHA-256 `f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488`（25,349 bytes）。
  同一 cwd 2 回 + 隔離 W 複写・別 cwd・別 HOME 1 回の 3 実行で byte-identical（GATE FAILED 0）。実測 8.0〜8.1 秒/実行（fold21 pristine rerun 約 6.8 秒を含む全 gate）。

## FOLD_PREVERIFIED_CHAIN の変遷としての意義

fold20（第2適用機）が「出版機を pristine のまま再実行」を初達成し、fold21（第3適用機）が隔離環境で再現、
fold22（第4適用機）は chain 入力を repo 出版物のみから再構築した隔離 W でも直前機 pristine 再実行 gate が
そのまま成立することを示した。fold23 以降も直前機 pristine 再実行のみの gate でよい。

## K1132 採番の 3 点確認

最新 main（HEAD `f5467450f6` 時点で確認・push 直前に再確認）で (1) recent commits の最大 K 採番 K1131（two-token y=7 族 item・高速レーン）であること (2) code search で K1132〜K1136 の出現 0 件 (3) knowledge README に K1132 の言及なし、を確認し、K1132 を fold22 item に採番した。高速レーンの y=8 宣言（`2026-11-20-two-token-y8-parametric-allz-single-owner-note.md`）は仮番号を使用しない方針を明記しており(push 直前に空き確認)、fold22/root 840500 に関する並走声明は本レーンの単一オーナー宣言（`29e6195803`）のみ。

## 解釈規約（不変）

fold は行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 はこの8石rootのゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
