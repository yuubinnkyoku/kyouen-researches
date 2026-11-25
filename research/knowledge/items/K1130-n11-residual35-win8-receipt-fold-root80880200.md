---
id: K1130
title: 残余38行のWIN8-D10 receipt fold root 80880200（fold21・第28 receipt・11番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold21 WIN8 receipt fold root 80880200
  - K1124証明書の五親frontierチェーンへのfoldと残余38→35行
  - FOLD_PREVERIFIED_CHAIN rerun-gate再設計の第3適用機（直前機pristine再実行）
relations:
  - type: depends_on
    target: K1124
    note: WIN8-D10証明書（root 00000000000000801202000800880200・25,783行 934,278 bytes・SHA-256 eca214f0…・19 gate監査正本SHA-256 422e6109…）。g01 K1089 master SHA pin 808fbda1…・g02/g03 runner v17 blob pin c132cc64…・g05 mobility 46・g06 uncapped probes 618,359/669,067〔andclose1/andclose0・loss=true・terminal石数[14,18]〕・g07主張3行・g08 probe再現 pilot_d6 4・g13 nodes A1 1,670,778/B 1,383,269・g16 miss 0/extra 0〔third_method terminal 9,204・visited 57,636・winner 37,121・loser 11,311・応手辺 52,219〕・g17三方法集計一致・g19 K1097 footprint intrinsic == claimed == 3行の全gateを本機械で再検証
  - type: depends_on
    target: K1129
    note: fold20正本（残余38 baseline・SHA-256 76fd255b…）。fold21機械はfold20出版機（SHA-256 9e141d4a…）をpristineのまま隔離W複写の下で1回再実行し、出版正本とbyte-identicalであることをgateしてからfold20レコードをchainingした。fold19 rerun gate・K1121 gate群はこのrerunの内部で推移的に再検証される
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張3行（intrinsic == claimed == 3行・49行exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1089
    note: 掃引のroot 80880200 probe記録（両AND順序uncapped 618,359/669,067・loss=true・terminal石数[14,18]）と主張3行の主張源（g01 master SHA pin 808fbda1…）
artifacts:
  - path: research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/README.md
    role: source
    note: 候補選定（K1123/K1124/K1125機械比較）・入力pin・直前機pristine再実行設計・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/scripts/fold_win8_root80880200.py
    role: verifier
    note: 純Python・乱数なし・1,099行・約6.8秒/実行。チェーン全段frontier再計算・fold20 pristine rerun gate・K1124/K1089/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/scripts/build_fold21.py
    role: generator
    note: fold20出版機（SHA pin 9e141d4a…）からの変換生成スクリプト（全置換出現回数assert・stale定数grep・py_compile・転写ミス3件を生成段階で捕捉修正）
  - path: research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/output/win8-root80880200-receipt-fold-20261120.json
    role: data
    note: fold21正本（status fold-complete・SHA-256 9a4da2f6…・26,113 bytes・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold21-win8-root80880200-receipt-fold.md
    role: log
    note: 候補比較・発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold21-win8-root80880200-single-owner-note.md
    role: log
    note: 単一オーナー宣言（先行出版）
  - path: research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md
    role: log
    note: FOLD_PREVERIFIED_CHAIN rerun-gate再設計の採用ノート（本実験の設計根拠）
---

# 残余38行のWIN8-D10 receipt fold root 80880200（fold21・第28 receipt）

K1124のWIN8-D10証明書（root `00000000000000801202000800880200`・25,783行・SHA-256 `eca214f0…`）を、五親S6 frontier receiptチェーンの第28 receiptとしてfoldした。fold20正本（残余38 baseline）からの続き。

## 主要結果

- **receipt は open 8 行を閉じた**: K1089/K1124/K1097 主張 3 行（5親target内）`0000000000000000380000000a002000`（cost 64・unswept・c2×2需要行）・`00000000000000801202000000800200`（cost 74・unswept・c2×2需要行）・`00000000000000801202000000880000`（cost 67・unswept・c2×2+c4×2需要行）+ **target 外 open 5 行** `00000000000000801002000000880200`（cost 76・c4×2）・`00000000000000801002000800080200`（cost 72・c4×2）・`00000000000000801002000800880000`（cost 63・c4×2）・`00000000000000801202000000080200`（cost 78・c2×2+c4×2）・`00000000000000801202000800000200`（cost 82・c2×2）〔いずれもunswept・同じrootのC(8,6)部分集合幾何に内在〕。余剰5行は主張から分離記録（fail-closed設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 576・5親112行target 74 → **77**・残余 38 → **35 行**・frontier 6,144/486,819 → **6,136/486,243**・solved S6 1,704 → **1,712**・parent行incidence 11,701 → **11,683**（影響7 parent・class 4を3・class 2を3・class 6を1・完全閉鎖0）・s6_needed_by_open_classes 4,452 → **4,444**・cost_needed_by_open_classes 353,267 → **352,691**。
- **FOLD_PREVERIFIED_CHAIN再設計の第3適用機**: 直前機（fold20出版機 SHA-256 9e141d4a…）をpristineのまま隔離W複写の下で1回再実行し出力SHA-256を出版正本（76fd255b…）と照合するだけの簡素gateを3回連続で達成した。fold19 rerun gate・K1121 gate群はfold20 rerunの内部で推移的に再検証される。実測約6.8秒/実行（fold20 pristine rerun 約4.8秒を含む）。
- K1124監査19 gateを本機械で全再検証（g01 K1089 master SHA pin `808fbda1…`・g02/g03 runner v17 blob pin `c132cc64…`・g05 mobility 46・g06 uncapped probes 618,359/669,067・terminal石数[14,18]・g07 3行定数gate・g13 nodes A1 1,670,778/B 1,383,269・g16 miss 0/extra 0・g17 Bareiss 46 subroot三方法一致・g19 footprint claimed == intrinsic == 3行・証明書全文byte検証 934,278 bytes/25,783行/third_method集計 terminal 9,204・visited 57,636・winner 37,121・loser 11,311・応手辺 52,219・合法手46独立再導出）。
- rootの6石部分幾何28 canonical行の分類: open-frontier 8（本receiptで閉鎖）・not-in-worklist 19・closed-before-this-receipt 1。
- win16候補は 6 → **5 根**（主張 15 → **12 行**）。残余23行掃引計画は不変（全win16主張と不交差を機械再確認）。
- 正本（SHA-256 `9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39`）は同一cwd 2回 + 隔離W複写・別cwd・別HOME 1回の3実行でbyte-identical（GATE FAILED 0・52 input pin〔12 blob SHA-1 + 40 SHA-256〕全て検証）。

## 解釈規約

fold は行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残余 35 行レーンでは、K1123（root `00000000020809002000480100000`・open 4行・fresh-probe基盤）と K1125（root `00000000000000801202000000840500`・open 6行）が fold22 以降の候補である（着手時に単一オーナー宣言を要する）。

