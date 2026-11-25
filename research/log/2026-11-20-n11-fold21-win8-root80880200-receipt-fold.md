# 研究log: fold21 WIN8-D10 receipt fold root 80880200（2026-11-20）

単一オーナー宣言（commit `e0c028a78c`・先行出版）に基づく実行記録。
前段: 同一レーン実行で fold20（K1129・root `08d10000`・残余 41 → 38）を出版（commits `07904ecdfa` → part2 `1bae3daa` → part3 `35d5fb80` → index `536c01ae`）。本 fold は出版済みの K1124 証明書（root `00000000000000801202000800880200`・25,783 行 934,278 bytes・SHA-256 `eca214f0…`・19 gate 監査正本 `422e6109…`・実験 `n11-residual45-win8-cert-extract-root80880200-20261120`）の receipt fold であり、fold20 正本（残余38 baseline）の続きに接続する。第28 receipt・11番目の WIN8 receipt fold。

## 事前検証と設計決定

1. **fold20 baseline の確定**: fold20 出版機（SHA-256 `9e141d4a…`）を隔離 W 複写で再実行し、出力 SHA-256 が出版 fold20 正本（`76fd255b…`）と byte-identical であることを確認してから着手した。
2. **候補機械比較（fold22 以降の選定基準としても記録）**: fold20 適用後状態に対して出版済み WIN8 候補 K1123（root `00000000020809002000480100000`）・K1124（root 80880200）・K1125（root `00000000000000801202000000840500`）の 6 石部分幾何 28 正準行を機械分類した。K1123 は open 4 行（主張 3 + 余剰 1・cost 321）・K1124 は **open 8 行（主張 3 + 余剰 5・cost 576・影響 7 親で class 2/4/6 混在）**・K1125 は open 6 行（主張 3 + 余剰 3・cost 484）。frontier 削減最大として K1124 を fold21 に選定した。
3. **K1124 材料の取得と pin 突合**: K1124 監査正本（SHA-256 `422e61095e80ee5ea6a52278e2ba52bb18d4ea301cab4c26e1e45d9c9701f172`）と証明書本体（`eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf`・25,783 行・934,278 bytes）を W に配置し、19 gate の全 detail（g01 K1089 master pin `808fbda1…`・g02/g03 runner v17 blob pin `c132cc64…`・g05 mobility 46・g06 uncapped probes andclose1 618,359 / andclose0 669,067〔loss=true・終端石数 [14,18]〕・g07 主張 3 行 `…380000000a002000`/`…801202000000800200`/`…801202000000880000`・g08 probe 再現 pilot_d6 4, reproduced 2/2・g13 nodes A1 1,670,778 / B 1,383,269・g16 miss 0/extra 0〔third_method terminal 9,204・visited 57,636・winner 37,121・loser 11,311・応手辺 52,219〕・g17 Bareiss 46 subroot 三方法一致・g19 K1097 pin `2896deb0…`・footprint claimed == intrinsic == 3 行）を取得時点で機械読み込みした。
4. **主張 3 行の residual38 内 open 性の事前確認**: K1124 主張 3 行が fold20 正本の residual 38 行に全て含まれること、fold20 の閉鎖 8 行と不交差であることを事前機械確認した。
5. **隔離 W（W21）の構築**: fold20 系譜の W（fold20 正本・出版機 pristine・全 chain 入力）を複写し、fold20 正本・K1124 監査正本・K1124 証明書本体の 3 ファイルを追加配置。52 input pin（12 blob SHA-1 + 40 SHA-256）を機械実行時に全照合（bad=0）。
6. **fold21 機の生成**: `build_fold21.py`（全置換が出現回数 assert で機械検証・stale 定数 grep・py_compile・ast 解析）で fold20 出版機（SHA-256 `9e141d4a…`）から変換生成（1,099 行・約6.8秒/実行）。変換内容: (a) header/env/OUT/ROOT_HEX/CERT_RELPATH 差し替え (b) PIN256 に fold20 正本・K1124 監査・K1124 証明書の 3 pin 追加（計 40 SHA-256 pin）(c) fold19 chaining 部を fold20 chaining + **fold20 pristine rerun gate** に置換（隔離 W 複写・FOLD20_W・出力 SHA が fold20 正本 pin `76fd255b…` と一致で gate・失敗時 fail-close）(d) K1121 gate ブロックを K1124 ブロックに全面差し替え（全定数は K1124 監査正本から機械取得）(e) open38/residualSet38 適用・solved 基準 1,704・closedAllNew 基準 74・残の会計 38−3・win16 6→5 根/15→12 行 (f) closedHistorical に rows20 を追加 (g) 転写ミス 3 件（print 行の k1121 アンカー残存・retired_root_predecessor hex 32 桁化・fold20 record パス出現回数 7 の assert）を生成段階で捕捉修正。K1119/K1121 の残存参照は allowlist（PIN256 pin・推移的再検証を示す controls 行）のみ。

## 結果

- receipt は **open 8 行**を閉じた:
  K1089/K1124/K1097 主張 3 行（target 内）`0000000000000000380000000a002000`（cost 64・unswept・c2×2 需要行）・`00000000000000801202000000800200`（cost 74・unswept・c2×2 需要行）・`00000000000000801202000000880000`（cost 67・unswept・c2×2+c4×2 需要行）+
  **target 外 open 5 行** `00000000000000801002000000880200`（cost 76・c4×2）・`00000000000000801002000800080200`（cost 72・c4×2）・`00000000000000801002000800880000`（cost 63・c4×2）・`00000000000000801202000000080200`（cost 78・c2×2+c4×2）・`00000000000000801202000800000200`（cost 82・c2×2）〔いずれも unswept・同じrootのC(8,6)部分集合幾何に内在〕。
  余剰 5 行は主張から分離して正確に記録した（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 576・5親 target 74 → **77/112**・残余 38 → **35** 行・frontier 6,144/486,819 → **6,136/486,243**・solved S6 1,704 → 1,712・incidence 11,701 → 11,683（影響 7 parent・class 4 を 3・class 2 を 3・class 6 を 1・完全閉鎖 0。parent-delta 計 18 == incidence 減分）・s6_needed 4,452 → 4,444・cost_needed 353,267 → 352,691。
- 6石部分幾何28行: open-frontier 8（本receiptで閉鎖）・not-in-worklist 19・closed-before-this-receipt 1。
- win16 候補 6 → **5 根**（主張 15 → 12 行）。残余23行掃引計画は不変（全win16主張と不交差を機械再確認）。
- 出力 SHA-256 `9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39`（26,113 bytes）。
  同一 cwd 2 回 + 隔離 W 複写・別 cwd・別 HOME 1 回の 3 実行で byte-identical（GATE FAILED 0）。実測 6.5〜6.8 秒/実行（fold20 pristine rerun 約 4.8 秒を含む全 gate）。

## FOLD_PREVERIFIED_CHAIN の変遷としての意義

fold19（第1適用機）は前段機 fold18 が旧設計であったため preverified 写し（marker-reversible patch・reverse patch 検証）を要した。fold20（第2適用機）は直前機（fold19）が自前の PREVERIFIED スイッチを持つため「出版機を pristine のまま再実行」を初達成した。fold21（第3適用機）はこの簡素構成が DOM・HOME・cwd を変えた隔離環境でもそのまま再現することを示し、以降の receipt fold（fold22+）は直前機 pristine 再実行のみの gate でよいことが確定した。

## K1130 採番の 3 点確認

最新 main（HEAD `e0c028a78c`・自レーンの単一オーナー宣言）で (1) recent commits の最大 K 採番 K1129（fold20 item）・K1127/K1128 であること (2) code search で K1130・K1131 の出現 0 件 (3) knowledge README に K1130 の言及なし、を確認し、K1130 を fold21 item に採番した。fold21/residual35 を巡る並走声明は単一オーナー宣言（`e0c028a78c`）のみ。

## 解釈規約（不変）

fold は行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 はこの8石rootのゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
