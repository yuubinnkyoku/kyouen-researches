# 研究log: fold20 WIN8-D10 receipt fold root 08d10000（2026-11-20）

単一オーナー宣言（commit `71b9d0798c`・先行出版）に基づく実行記録。
前段: 同一レーン実行で fold19（K1128・root `1009000`・残余 45 → 41）を出版（commits `c3be4c79b6` → 修理 repush `a715c0e5ef` → part2 `800005c6a9` → item/log `01ed89c2c9` → index `d135212715`）。本 fold は並走レーン出版の K1121 証明書（root `00000000000000003800000008d10000`・28,328 行 1,026,202 bytes・SHA-256 `8513e366…`・19 gate 監査正本 `0088ebab…`・実験 `n11-residual48-win8-cert-extract-root08d10000-20261120`・出版 commit `1137901d95`）の receipt fold であり、fold19 正本（残余41 baseline）の続きに接続する。第27 receipt・10番目の WIN8 receipt fold。

## 事前検証と設計決定

1. **K1121 材料の取得と pin 突合**: 並走レーン出版の K1121 監査正本（SHA-256 `0088ebab040a29e608c987fb8ae866abf59253d60455b0d2ca6b6ef963170940`）と証明書本体（`8513e366…`・28,328 行・1,026,202 bytes）を W に配置し、19 gate の全 detail（g01 K1091 master pin `edd7ac84…`・g05 mobility 50・g06 uncapped probes andclose1 564,695 / andclose0 673,870〔loss=true・終端石数 [14,18]〕・g07 主張3行 `…08011000`/`…08500000`/`…08900000`・g08 probe 再現 pilot_d6 4, reproduced 2/2・g13 nodes A1 2,428,240 / B 1,748,509・g16 miss 0/extra 0・g19 K1097 pin `2896deb0…`・third_method〔root 先手 50・terminal 15,513・visited 83,544・winner 53,570・loser 14,461・応手辺 72,930〕）を取得時点で機械読み込みした。
2. **主張 3 行の residual41 内 open 性の事前確認**: K1121 主張 3 行が fold19 正本の five_parent_target_after.residual_row_hex_after（41 行）に全て含まれること、fold19 の閉鎖 5 行と不交差であることを事前機械確認した（fold19 機の receipt 適用で失われる行はない）。
3. **隔離 W（W20）の構築**: fold19 系譜の W（fold19 正本・出版機 pristine・全 chain 入力）を複写し、fold19 正本・K1121 監査正本・K1121 証明書本体の 3 ファイルを追加配置。49 input pin（12 blob SHA-1 + 37 SHA-256）を機械実行時に全照合（bad=0）。fold19 出版機は「採用設計の PREVERIFIED スイッチ組み込み済み・デフォルト実行 ≈3.0 秒」であるため、preverified 写し・reverse patch 機構は本 fold では不要と判断した。
4. **fold20 機の生成**: `build_fold20.py`（全置換が出現回数 assert で機械検証・stale 定数 grep・stale k1119/k1120 行の allowlist 検査・py_compile・ast 解析）で fold19 出版機（SHA-256 `51442d96…`）から変換生成（1,055 行・約4.8秒/実行）。変換内容: (a) header/env/OUT/ROOT_HEX/CERT_RELPATH 差し替え (b) PIN256 に fold19 正本・K1121 監査・K1121 証明書の 3 pin 追加（計 37 SHA-256 pin）(c) fold18 preverified rerun gate を fold19 chaining + **fold19 pristine rerun gate** に置換（隔離 W 複写・FOLD19_W・出力 SHA が fold19 正本 pin `c02d9a54…` と一致で gate・失敗時 fail-close）(d) K1119 gate ブロックを K1121 ブロックに全面差し替え（全定数は K1121 監査正本から機械取得）(e) open41/residualSet41 適用・solved 基準 1,696・closedAllNew 基準 71・残の会計 41−3・win16 7→6 根/18→15 行 (f) closedHistorical に rows19 を追加 (g) K1119/K1120 の残存参照は allowlist（PIN256 2 pin ずつ・推移的再検証を示す controls 行）のみ。
5. **転写ミス検査**: 今回はclaims_record等の説明文字列について、root 08d10000 の K1097 footprint は intrinsic == claimed == 3 行が正しく、fold19 機由来の定数（4 行版）は変換スクリプトの rep で解消済み。出版前レビューで stale 定数 grep・allowlist 外の k1119/k1120 行が 0 であることを機械検証した。

## 結果

- receipt は **open 8 行**を閉じた:
  K1091/K1121/K1097 主張 3 行（target 内）`00000000000000003800000008011000`（cost 74・unswept・c2 需要行）・`00000000000000003800000008500000`（cost 75・unswept・c2×2 需要行）・`00000000000000003800000008900000`（cost 76・unswept・c2/c4 需要行）+
  **target 外 open 5 行** `00000000000000003800000000c10000`（cost 80）・`00000000000000003800000000d00000`（cost 83）・`00000000000000003800000008410000`（cost 70）・`00000000000000003800000008810000`（cost 72）・`00000000000000003800000008c00000`（cost 69）〔いずれも unswept・同じrootのC(8,6)部分集合幾何に内在〕。
  余剰5行は主張から分離して正確に記録した（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 599・5親 target 71 → **74/112**・残余 41 → **38** 行・frontier 6,152/487,418 → **6,144/486,819**・solved S6 1,696 → 1,704・incidence 11,711 → 11,701（影響4 parent・class 4 を 2・class 2 を 2・完全閉鎖0）・s6_needed 4,460 → 4,452・cost_needed 353,866 → 353,267。
- 6石部分幾何28行: open-frontier 8（本receiptで閉鎖）・not-in-worklist 20・closed-before-this-receipt 0。
- win16 候補 7 → **6 根**（主張 18 → 15 行）。残余23行掃引計画は不変（全win16主張と不交差を機械再確認）。
- 出力 SHA-256 `76fd255bf16f0e434d15579cf148015bd564929e85910172f0a0ef87015842a2`（24,684 bytes）。
  同一 cwd 2回 + 別 W 複写・別プロセス 1回の 3 実行で byte-identical（GATE FAILED 0）。実行ログ自体も 2・3 回目は byte-identical（stdout 完全決定性）。
- 計測: 1 実行（49 pin 照合・チェーン全段 frontier 再計算・fold19 pristine rerun〔fold18 preverified rerun を含む〕含む全 gate）**約4.8 秒**。採用設計の系譜がfold20でも数秒/実行を維持した。

## rerun-gate 再設計の変遷としての意義

fold19（第1適用機）では出版済み前段機（fold18）が採用設計前の旧機であったため preverified 写し（marker-reversible patch・reverse patch 検証）を要した。fold20（第2適用機）では直前機（fold19）自身が採用設計の PREVERIFIED スイッチを持つため、**出版機を pristine のまま再実行するだけ**でよいことが実証された。以降の receipt fold（fold21+）はこの簡素構成を踏襲できる（各機が自身の PREVERIFIED スイッチを持つため）。推移的検証の層構造も正本に記録した（fold18 preverified rerun・K1120 gate 群は fold19 rerun の内部で再検証され、fold20 正本の controls に明記）。

## K1129 採番の 3 点確認

最新 main（HEAD `d120517aa1`）で (1) recent commits の最大 K 採番 K1128（fold19 item）・K1127（y=7 族）であること (2) knowledge README に K1129 の言及なし (3) items dir に K1129 接頭辞項目なし、を確認し、K1129 を fold20 item に採番した。fold20/residual38 を巡る並走声明は単一オーナー宣言（`71b9d0798c`）のみ。

## 解釈規約（不変）

fold は行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 はこの8石rootのゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
