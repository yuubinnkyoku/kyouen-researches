---
id: K1129
title: 残余41行のWIN8-D10 receipt fold root 08d10000（fold20・第27 receipt・10番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold20 WIN8 receipt fold root 08d10000
  - K1121証明書の五親frontierチェーンへのfoldと残余41→38行
  - FOLD_PREVERIFIED_CHAIN rerun-gate再設計の第2適用機（直前機pristine再実行）
relations:
  - type: depends_on
    target: K1121
    note: WIN8-D10証明書（root 00000000000000003800000008d10000・28,328行 1,026,202 bytes・SHA-256 8513e366…・並走レーン出版）と19 gate監査正本（SHA-256 0088ebab…）。g01 K1091 master SHA pin edd7ac84…・g05 mobility 50・g06 uncapped probes 564,695/673,870〔andclose1/andclose0〕・terminal石数[14,18]・g07主張3行・g08 probe再現 4/2/2・g13 nodes A1 2,428,240/B 1,748,509・g16 miss 0/extra 0・g19 K1097 footprint intrinsic == claimed == 3行の全gateを本機械で再検証
  - type: depends_on
    target: K1128
    note: fold19正本（残余41 baseline・SHA-256 c02d9a54…）。fold20機械はfold19出版機（SHA-256 51442d96…）をpristineのまま隔離W複写の下で1回再実行し、出版正本とbyte-identicalであることをgateしてからfold19レコードをchainingした。fold18 preverified rerun・reverse patch・K1120 gate群はこのrerunの内部で推移的に再検証される
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張3行（intrinsic == claimed == 3行・49行exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1091
    note: 掃引のroot 08d10000 probe記録（両AND順序uncapped 564,695/673,870・loss=true・terminal石数[14,18]）と主張3行の主張源（g01 master SHA pin edd7ac84…）
artifacts:
  - path: research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/README.md
    role: source
    note: 入力pin・直前機pristine再実行設計・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/scripts/fold_win8_root08d10000.py
    role: verifier
    note: 純Python・乱数なし・1,055行・約4.8秒/実行。チェーン全段frontier再計算・fold19 pristine rerun gate・K1121/K1091/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/scripts/build_fold20.py
    role: generator
    note: fold19出版機（SHA pin 51442d96…）からの変換生成スクリプト（全置換出現回数assert・stale定数grep・py_compile）
  - path: research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/output/win8-root08d10000-receipt-fold-20261120.json
    role: data
    note: fold20正本（status fold-complete・SHA-256 76fd255b…・24,684 bytes・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold20-win8-root08d10000-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold20-win8-root08d10000-single-owner-note.md
    role: log
    note: 単一オーナー宣言（先行出版）
  - path: research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md
    role: log
    note: FOLD_PREVERIFIED_CHAIN rerun-gate再設計の採用ノート（本実験の設計根拠）
---

# 残余41行のWIN8-D10 receipt fold root 08d10000（fold20・第27 receipt）

K1121のWIN8-D10証明書（root `00000000000000003800000008d10000`・28,328行・SHA-256 `8513e366…`・並走レーンが抽出・三重検証・出版）を、五親S6 frontier receiptチェーンの第27 receiptとしてfoldした。fold19正本（残余41 baseline）からの続き。

## 主要結果

- **receipt は open 8 行を閉じた**: K1091/K1121/K1097 主張 3 行（5親target内）`00000000000000003800000008011000`（cost 74・unswept・c2需要行）・`00000000000000003800000008500000`（cost 75・unswept・c2×2需要行）・`00000000000000003800000008900000`（cost 76・unswept・c2/c4需要行）+ **target 外 open 5 行** `00000000000000003800000000c10000`（cost 80）・`00000000000000003800000000d00000`（cost 83）・`00000000000000003800000008410000`（cost 70）・`00000000000000003800000008810000`（cost 72）・`00000000000000003800000008c00000`（cost 69）〔いずれもunswept・同じrootのC(8,6)部分集合幾何に内在〕。余剰5行は主張から分離記録（fail-closed設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 599・5親112行target 71 → **74**・残余 41 → **38 行**・frontier 6,152/487,418 → **6,144/486,819**・solved S6 1,696 → **1,704**・parent行incidence 11,711 → **11,701**（影響4 parent・class 4を2・class 2を2・完全閉鎖0）・s6_needed_by_open_classes 4,460 → **4,452**・cost_needed_by_open_classes 353,866 → **353,267**。
- **FOLD_PREVERIFIED_CHAIN再設計の第2適用機で、rerun gateがさらに簡素化された**: 直前機（fold19出版機）は改変もpreverified写しも不要で、**pristineのまま**隔離W複写の下で1回再実行し出力SHA-256を出版正本と照合するだけになった。fold19出版機自身が採用設計のPREVERIFIEDスイッチを持つためである（fold18までは出版後にスイッチを持たずpreverified写しを要した）。fold18 preverified rerun・reverse patch・K1120 gate群はfold19 rerunの内部で推移的に再検証される。実測約4.8秒/実行（fold19 pristine rerun ≈3.0秒を含む）。
- K1121監査19 gateを本機械で全再検証（g01 K1091 master SHA pin `edd7ac84…`・g05 mobility 50・g06 uncapped probes 564,695/673,870・terminal石数[14,18]・g07 3行定数gate・g13 nodes A1 2,428,240/B 1,748,509・g16 miss 0/extra 0・g19 footprint claimed == intrinsic == 3行・証明書全文byte検証 1,026,202 bytes/28,328行/third_method集計 terminal 15,513・visited 83,544・winner 53,570・loser 14,461・応手辺 72,930）。
- rootの6石部分幾何28 canonical行の分類: open-frontier 8（本receiptで閉鎖）・not-in-worklist 20・closed-before-this-receipt 0。
- win16候補は 7 → **6 根**（主張 18 → **15 行**）。残余23行掃引計画は不変（全win16主張と不交差を機械再確認）。
- 正本（SHA-256 `76fd255bf16f0e434d15579cf148015bd564929e85910172f0a0ef87015842a2`）は同一cwd 2回 + 別W複写・別プロセス 1回の3実行でbyte-identical（GATE FAILED 0・49 input pin〔12 blob SHA-1 + 37 SHA-256〕全て検証）。

## 解釈規約

fold は行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残余 38 行レーンでは、K1123（root `00000000020809002000480100000`・3行・fresh-probe基盤）・K1124（root 80880200）・K1125（root 840500）など出版済み・.fresh掃引系の証明書がfold21以降の候補である（着手時に単一オーナー宣言を要する）。
