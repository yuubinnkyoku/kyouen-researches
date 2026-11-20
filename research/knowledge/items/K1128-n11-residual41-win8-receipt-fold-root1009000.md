---
id: K1128
title: 残余45行のWIN8-D10 receipt fold root 1009000（fold19・第26 receipt・9番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold19 WIN8 receipt fold root 1009000
  - K1119証明書の五親frontierチェーンへのfoldと残余45→41行
  - FOLD_PREVERIFIED_CHAIN rerun-gate再設計の最初の適用機
relations:
  - type: depends_on
    target: K1119
    note: WIN8-D10証明書（root 00000000000000801212000001009000・16,262行 587,989 bytes・SHA-256 b4dd1e06…・並走レーン出版）と19 gate監査正本（SHA-256 4696ce14…）。g01 K1091 master SHA pin edd7ac84…・g05 mobility 44・g06 uncapped probes 192,365/229,502〔andclose1/andclose0〕・terminal石数[14,18]・g07主張4行・g08 probe再現 4/2/2・g13 nodes A1 865,602/B 712,106・g16 miss 0/extra 0・g19 K1097 footprint intrinsic == claimed == 4行の全gateを本機械で再検証
  - type: depends_on
    target: K1122
    note: fold18正本（残余45 baseline・SHA-256 18b543c4…）。fold19機械はfold18出版機をmarker-reversible preverified写し（SHA-256 d342f1f8…・reverse patch で出版機 dcdfbf92… と厳密一致）として隔離W複写の下で1回再実行し、出版正本とbyte-identicalであることをgateしてからfold18レコードをchainingした
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張4行（intrinsic == claimed == 4行・49行exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1091
    note: 掃引のroot 1009000 probe記録（両AND順序uncapped 192,365/229,502・loss=true・terminal石数[14,18]）と主張4行の主張源（g01 master SHA pin edd7ac84…）
artifacts:
  - path: research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/README.md
    role: source
    note: 入力pin・FOLD_PREVERIFIED_CHAIN設計・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/fold_win8_root1009000.py
    role: verifier
    note: 純Python・乱数なし・1,028行・約3.0秒/実行。チェーン全段frontier再計算・fold18 preverified rerun gate・K1119/K1091/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/build_fold19.py
    role: generator
    note: fold18出版機（SHA pin）からの変換生成スクリプト（全置換出現回数assert・stale定数grep・py_compile）
  - path: research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/fold_win8_root00901010_preverified.py
    role: verifier
    note: fold18出版機のmarker-reversible preverified写し（SHA-256 d342f1f8…・FOLD_PREVERIFIED_CHAIN=1でのみrerun gate群をスキップ・デフォルトは完全連鎖と同一）
  - path: research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/make_preverified_patch.py
    role: generator
    note: preverified写しの自動生成とreverse patch検証
  - path: research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/output/win8-root1009000-receipt-fold-20261120.json
    role: data
    note: fold19正本（status fold-complete・SHA-256 c02d9a54…・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold19-win8-root1009000-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold19-win8-root1009000-single-owner-note.md
    role: log
    note: 単一オーナー宣言（先行出版）
  - path: research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md
    role: log
    note: FOLD_PREVERIFIED_CHAIN rerun-gate再設計の採用ノート（本実験の設計根拠）
---

# 残余45行のWIN8-D10 receipt fold root 1009000（fold19・第26 receipt）

K1119のWIN8-D10証明書（root `00000000000000801212000001009000`・16,262行・SHA-256 `b4dd1e06…`・並走レーンが抽出・三重検証・出版）を、五親S6 frontier receiptチェーンの第26 receiptとしてfoldした。fold18正本（残余45 baseline）からの続き。

## 主要結果

- **receipt は open 5 行を閉じた**: K1091/K1119/K1097 主張 4 行（5親target内）`00000000000000003800200008001000`（cost 72・unswept・c2×2）・`00000000000000003800200009000000`（cost 78・unswept・c2×2）・`00000000000801212000000001000`（cost 78・unswept・c2×2）・`00000000000801212000001000000`（cost 74・unswept・c2×2）+ **target 外 open 1 行** `00000000000801212000000008000`（cost 80・unswept・c2×2・同じrootのC(8,6)部分集合幾何に内在）。余剰1行は主張から分離記録（fail-closed設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 382・5親112行target 67 → **71**・残余 45 → **41 行**・frontier 6,157/487,800 → **6,152/487,418**・solved S6 1,691 → **1,696**・parent行incidence 11,721 → **11,711**（影響4 parent・いずれもclass 2・完全閉鎖0）・s6_needed_by_open_classes 4,465 → **4,460**・cost_needed_by_open_classes 354,248 → **353,866**。
- **FOLD_PREVERIFIED_CHAIN rerun-gate再設計（採用ノート commit fbea3ecc）の最初の適用機**: rerun gateは「直前機のみ1回再実行」とし、fold11〜17機の再帰rerun連鎖を削除、上流はSHA pin + チェーン全段frontier再計算で検証。fold18出版機は改変せず、marker-reversibleなpreverified写し（reverse patchで出版機SHAと厳密一致を検証）を通す。実測で旧fold18機の約186秒/実行に対し本機は**約3.0秒/実行**（preverified fold18 rerun含む）で、旧機の所要時間のほぼ全てが再帰rerun連鎖のオーバーヘッドだったことが確定した。
- K1119監査19 gateを本機械で全再検証（g01 K1091 master SHA pin `edd7ac84…`・g05 mobility 44・g06 uncapped probes 192,365/229,502・terminal石数[14,18]・g07 4行定数gate・g13 nodes A1 865,602/B 712,106・g16 miss 0/extra 0・g19 footprint claimed == intrinsic == 4行・証明書全文byte検証 587,989 bytes/16,262行/third_method集計 terminal 5,783・visited 37,696・winner 24,352・loser 7,561・応手辺 34,261）。
- rootの6石部分幾何28 canonical行の分類: open-frontier 5（本receiptで閉鎖）・not-in-worklist 23・closed-before-this-receipt 0。
- win16候補は 8 → **7 根**（主張 22 → **18 行**）。残余23行掃引計画は不変（全win16主張と不交差を機械再確認）。
- 正本（SHA-256 `c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae`）は同一cwd 2回 + 別W複写・別プロセス 1回の3実行でbyte-identical（GATE FAILED 0・46 input pin〔12 blob SHA-1 + 34 SHA-256〕全て検証）。

## 解釈規約

fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残余 41 行レーンでは、未 fold の出版証明書 K1121（root `…08d10000`・主張 3 行・residual-45 内で open を fold18 が確認済み）をはじめ、出版済み WIN8 候補残根の証明書（fold20 候補・着手時に単一オーナー宣言を要する）の receipt fold が次段の未着手領域である。
