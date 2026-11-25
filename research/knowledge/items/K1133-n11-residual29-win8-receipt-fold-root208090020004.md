---
id: K1133
title: 残余32行のWIN8-D10 receipt fold root 208090020004（fold23・第30 receipt・13番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold23 WIN8 receipt fold root 208090020004
  - K1123証明書の五親frontierチェーンへのfoldと残余32→29行
  - 出版済みWIN8証明書receipt foldの最終適用（fold19〜23で枯渇）
  - FOLD_PREVERIFIED_CHAIN rerun-gate再設計の第5適用機
relations:
  - type: depends_on
    target: K1123
    note: WIN8-D10証明書（root 00000000000020809002000480100000・23,621行 855,258 bytes・SHA-256 b8145352…・19 gate監査正本SHA-256 6ea634c9…）。fresh-probe基盤（g01 K1119 provenance log pin git blob 51bad3fac…・sha256 4d11ca89…・g02 published total 793,616・g05 mobility 54・g06 fresh probes 350,792/442,824 sum 793,616・g07主張3行・g08 probe再現 pilot_d6 4・g13 nodes A1/B 3,009,765/3,009,765・g16 miss 0/extra 0〔third_method terminal 7,516・visited 49,094・winner 31,623・loser 9,955・応手辺 43,650〕・g17 Bareiss 54 subroot・g19 K1097 footprint claimed == intrinsic == 3行とfold18正本pin）の全gateを本機械で再検証
  - type: depends_on
    target: K1132
    note: fold22正本（残余32 baseline・SHA-256 f6e011f4…）。fold23機械はfold22出版機（SHA-256 d5721408…）をpristineのまま隔離W複写の下で1回再実行し、出版正本とbyte-identicalであることをgateしてからfold22レコードをchainingした。fold21 rerun gate・K1125 gate群はこのrerunの内部で推移的に再検証される
  - type: depends_on
    target: K1119
    note: fresh-probe provenance log（g01/g02がpinするgit blob 51bad3fac…・sha256 4d11ca89…・出版探査総計793,616の一致源）
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張3行（intrinsic == claimed == 3行・49行exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
artifacts:
  - path: research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/README.md
    role: source
    note: 候補選定（K1123のみ残・fold22閉鎖との不交差）・入力pin・直前機pristine再実行設計・fresh-probe系gate・結果・解釈上の制限
  - path: research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/scripts/fold_win8_root208090020004.py
    role: verifier
    note: 純Python・乱数なし・1,200行・約10.0秒/実行。チェーン全段frontier再計算・fold22 pristine rerun gate・K1123/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/scripts/build_fold23.py
    role: generator
    note: fold22出版機（SHA pin d5721408…）からの変換生成スクリプト（全置換出現回数assert・stale定数grep・py_compile・PIN256 46件/PINS 12件の件数assert）
  - path: research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/output/win8-root208090020004-receipt-fold-20261120.json
    role: data
    note: fold23正本（status fold-complete・SHA-256 04f334ff…・25,106 bytes・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold23-win8-root208090020004-receipt-fold.md
    role: log
    note: 候補選定・実行・再現・K1133採番3点確認・限界の研究記録
  - path: research/log/2026-11-20-n11-fold23-win8-root208090020004-single-owner-note.md
    role: log
    note: 単一オーナー宣言（先行出版 commit 5a7e4f7c・repoファイル名表記の訂正 62375b76/db5be5ad）
---

# 残余32行のWIN8-D10 receipt fold root 208090020004（fold23・第30 receipt）

K1123のWIN8-D10証明書（root `00000000000020809002000480100000`・23,621行・SHA-256 `b8145352…`・fresh-probe基盤）を、
五親S6 frontier receiptチェーンの第30 receiptとしてfoldした。fold22正本（残余32 baseline）からの続き。
出版済みWIN8証明書（K1119/K1121/K1124/K1125/K1123）のreceipt foldは本receiptで完遂した。

## 主要結果

- **receipt は open 4 行を閉じた**: K1123/K1097 主張 3 行（5親target内）
  `00000000000000801202040000001000`（cost 82・unswept・c2×1需要行）・
  `00000000000000801202040000800000`（cost 75・unswept・c2×1需要行）・
  `00000000000020809002000080000000`（cost 75・unswept・c2×2需要行）+
  **target 外 open 1 行** `00000000000020809002000400000000`（cost 89・unswept・c2×1需要行）
  〔いずれも同じrootのC(8,6)部分集合幾何に内在・閉鎖edge cost 321〕。
  余剰1行は主張から分離記録（fail-closed設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 321・5親112行target 80 → **83**・残余 32 → **29 行**・frontier 6,130/485,759 → **6,126/485,438**・
  solved S6 1,718 → **1,722**・parent行incidence 11,671 → **11,666**
  （影響3 parent・すべて class 2〔`…3800000008001000` 9→8・`…3800000008002000` 11→9・`…801202080000000000` 55→53〕・完全閉鎖0・
  parent-delta 計 5 == incidence 減分）・s6_needed_by_open_classes 4,438 → **4,434**・cost_needed 352,207 → **351,886**。
- **FOLD_PREVERIFIED_CHAIN再設計の第5適用機**: 直前機（fold22出版機 SHA-256 d5721408…）をpristineのまま隔離W複写の下で
  1回再実行し出力SHA-256を出版正本（f6e011f4…）と照合するだけの簡素gate。fold21 rerun gate・K1125 gate群はfold22 rerunの内部で
  推移的に再検証される。実測約10.0秒/実行（fold22 pristine rerun 約8.1秒を含む）。
- **K1123監査19 gate（fresh-probe系）を本機械で全再検証**: g01 K1119 provenance log pin（git blob `51bad3fac…`・sha256 `4d11ca89…`）・
  g02 出版探査総計 793,616・g05 mobility 54・g06 fresh probes {andclose1 350,792・andclose0 442,824・sum 793,616}・
  g07 主張3行定数gate・g08 probe再現 pilot_d6 4, andclose 2/2・g13 nodes A1/B 3,009,765/3,009,765・
  g16 miss 0/extra 0〔terminal 7,516・visited 49,094・winner 31,623・loser 9,955・応手辺 43,650〕・
  g17 Bareiss 54 subroot三方法一致・g19 K1097 footprint claimed == intrinsic == 3行（k1097 pin `2896deb0…`・fold18正本pin `18b543c4…`）・
  証明書全文byte検証 855,258 bytes/23,621行/sorted unique/header・root行・row形式・root幾何（8石・quadruple-free・D4正準）・合法手54独立再導出。
- rootの6石部分幾何28 canonical行の分類: open-frontier 4（本receiptで閉鎖）・not-in-worklist 22・closed-before-this-receipt 2。
- win16候補は 4 → **3 根**（主張 9 → 6 行）。残余23行掃引計画は不変（不交差機械再確認）。
- 正本（SHA-256 `04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59`・25,106 bytes）は
  同一cwd 2回 + 隔離W複写・別cwd・別HOME 1回の3実行でbyte-identical（GATE FAILED 0・58 input pin〔12 blob SHA-1 + 46 SHA-256〕全照合）。

## 出版済みWIN8 receipt foldの枯渇と次段

fold19〜fold23で出版済みWIN8証明書5点（K1119・K1121・K1124・K1125・K1123）のreceipt foldが完遂した。
残余29行を閉じるためには新規掃引（depth-10または拡張depth）による新証明書の出版が必要であり、
着手時に単一オーナー宣言を要する。win16残余3根（主張6行）は候補planの観測であり証明書ではない。

## 解釈規約

fold は行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。
REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
