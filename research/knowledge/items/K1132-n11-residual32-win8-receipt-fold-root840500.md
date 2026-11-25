---
id: K1132
title: 残余35行のWIN8-D10 receipt fold root 840500（fold22・第29 receipt・12番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold22 WIN8 receipt fold root 840500
  - K1125証明書の五親frontierチェーンへのfoldと残余35→32行
  - FOLD_PREVERIFIED_CHAIN rerun-gate再設計の第4適用機（直前機pristine再実行・repo出版入力のみからの隔離W再構築）
relations:
  - type: depends_on
    target: K1125
    note: WIN8-D10証明書（root 00000000000000801202000000840500・29,468行 1,067,425 bytes・SHA-256 21ad6195…・19 gate監査正本SHA-256 06c65f76…）。g01 K1089 master SHA pin 808fbda1…・g05 mobility 58・g06 uncapped probes 736,409/878,391〔andclose1/andclose0・loss=true・terminal石数[14,18]〕・g07主張3行・g08 probe再現 pilot_d6 4・g13 nodes A1 2,310,103/B 1,984,636・g16 miss 0/extra 0〔third_method terminal 9,810・visited 59,990・winner 38,458・loser 11,722・応手辺 52,360〕・g17三方法集計一致〔Bareiss 58 subroot〕・g19 K1097 footprint intrinsic == claimed == 3行の全gateを本機械で再検証
  - type: depends_on
    target: K1130
    note: fold21正本（残余35 baseline・SHA-256 9a4da2f6…）。fold22機械はfold21出版機（SHA-256 44399cc5…）をpristineのまま隔離W複写の下で1回再実行し、出版正本とbyte-identicalであることをgateしてからfold21レコードをchainingした。fold20 rerun gate・K1124 gate群はこのrerunの内部で推移的に再検証される
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張3行（intrinsic == claimed == 3行・49行exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1089
    note: 掃引のroot 840500 probe記録（両AND順序uncapped 736,409/878,391・loss=true・terminal石数[14,18]）と主張3行の主張源（g01 master SHA pin 808fbda1…）
artifacts:
  - path: research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/README.md
    role: source
    note: 候補選定（K1123/K1125機械比較・fold21閉鎖との不交差）・入力pin・直前機pristine再実行設計・隔離W再構築・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/scripts/fold_win8_root840500.py
    role: verifier
    note: 純Python・乱数なし・1,148行・約8.1秒/実行。チェーン全段frontier再計算・fold21 pristine rerun gate・K1125/K1089/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/scripts/build_fold22.py
    role: generator
    note: fold21出版機（SHA pin 44399cc5…）からの変換生成スクリプト（全置換出現回数assert・stale定数grep・py_compile・PIN256 43件/PINS 12件の件数assert）
  - path: research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/output/win8-root840500-receipt-fold-20261120.json
    role: data
    note: fold22正本（status fold-complete・SHA-256 f6e011f4…・25,349 bytes・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold22-win8-root840500-receipt-fold.md
    role: log
    note: 隔離W再構築・候補比較・実行・再現・K1132採番3点確認・限界の研究記録
  - path: research/log/2026-11-20-n11-fold22-win8-root840500-single-owner-note.md
    role: log
    note: 単一オーナー宣言（先行出版・commit 29e6195803）
---

# 残余35行のWIN8-D10 receipt fold root 840500（fold22・第29 receipt）

K1125のWIN8-D10証明書（root `00000000000000801202000000840500`・29,468行・SHA-256 `21ad6195…`）を、五親S6 frontier receiptチェーンの第29 receiptとしてfoldした。fold21正本（残余35 baseline）からの続き。

## 主要結果

- **receipt は open 6 行を閉じた**: K1089/K1125/K1097 主張 3 行（5親target内）`00000000000000801202000000800100`（cost 75・unswept・c2×2需要行）・`00000000000000801202000000800400`（cost 74・unswept・c2×2需要行）・`00000000000000801202000000840000`（cost 73・unswept・c2×2需要行）+ **target 外 open 3 行** `00000000000000801202000000000500`（cost 87・c2×2）・`00000000000000801202000000040100`（cost 89・c2×2）・`00000000000000801202000000040400`（cost 86・c2×2）〔いずれもunswept・同じrootのC(8,6)部分集合幾何に内在〕。余剰3行は主張から分離記録（fail-closed設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 484・5親112行target 77 → **80**・残余 35 → **32 行**・frontier 6,136/486,243 → **6,130/485,759**・solved S6 1,712 → **1,718**・parent行incidence 11,683 → **11,671**（影響4 parent・すべてclass 2〔`…3800000008002000` 14→11・`…801202000000000100` 51→48・`…801202000000000400` 47→44・`…801202000000040000` 69→66〕・完全閉鎖0）・s6_needed_by_open_classes 4,444 → **4,438**・cost_needed_by_open_classes 352,691 → **352,207**。
- **FOLD_PREVERIFIED_CHAIN再設計の第4適用機**: 直前機（fold21出版機 SHA-256 44399cc5…）をpristineのまま隔離W複写の下で1回再実行し出力SHA-256を出版正本（9a4da2f6…）と照合するだけの簡素gateを達成。fold20 rerun gate・K1124 gate群はfold21 rerunの内部で推移的に再検証される。実測約8.1秒/実行（fold21 pristine rerun 約6.8秒を含む）。
- **隔離Wをrepo出版入力のみから再構築**: 実行環境リセットで前段の隔離W（W21）を失ったが、chain入力一式（12 blob pin + 40 SHA-256 pin・fold18/19/20/21出版機・fold18 preverified写し）をrepoから再取得してW22を再構築し、fold21出版機が出版正本とbyte-identicalな出力を再現することを確認してからfold22を生成した。重要証拠が再現不能なローカル状態に依存しないことの実証例。
- K1125監査19 gateを本機械で全再検証（g01 K1089 master SHA pin `808fbda1…`・g05 mobility 58・g06 uncapped probes 736,409/878,391・terminal石数[14,18]・g07 3行定数gate・g13 nodes A1 2,310,103/B 1,984,636・g16 miss 0/extra 0・g17 Bareiss 58 subroot三方法一致・g19 footprint claimed == intrinsic == 3行・証明書全文byte検証 1,067,425 bytes/29,468行/third_method集計 terminal 9,810・visited 59,990・winner 38,458・loser 11,722・応手辺 52,360・合法手58独立再導出）。
- rootの6石部分幾何28 canonical行の分類: open-frontier 6（本receiptで閉鎖）・not-in-worklist 22・closed-before-this-receipt 0（fold21閉鎖8行との不交差と整合）。
- win16候補は 5 → **4 根**（主張 12 → **9 行**）。残余23行掃引計画は不変（全win16主張と不交差を機械再確認）。
- 正本（SHA-256 `f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488`）は同一cwd 2回 + 隔離W複写・別cwd・別HOME 1回の3実行でbyte-identical（GATE FAILED 0・55 input pin〔12 blob SHA-1 + 43 SHA-256〕全て検証）。

## 解釈規約

fold は行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残余 32 行レーンでは、K1123（root `00000000020809002000480100000`・fold21適用後 open 4行〔主張3+余剰1〕・cost 321・fresh-probe基盤gates）が fold23 の第一候補である（着手時のfold22適用後再分類と単一オーナー宣言を要する）。fold22 の閉鎖 6 行と K1123 の 6 石部分幾何 28 正準行の交差は fold22 適用後に再計算する。
