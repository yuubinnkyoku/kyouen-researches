---
id: K1122
title: 残余48行のWIN8-D10 receipt fold root 00901010（fold18・第25 receipt・8番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold18 WIN8 receipt fold root 00901010
  - K1120証明書の五親frontierチェーンへのfoldと残余48→45行
relations:
  - type: depends_on
    target: K1120
    note: WIN8-D10証明書（root 00000000000000801202000000901010・13,422行 484,892 bytes・SHA-256 d6745edb…・本レーン出版）と19 gate監査正本（SHA-256 ea6f1945…）。g07主張3行・g05 mobility 45・g06 uncapped probes 240,848/198,622・g13 nodes 631,539/524,342・g16 miss 0/extra 0・g19 K1097 footprint三点一致の全gateを本機械で再検証
  - type: depends_on
    target: K1118
    note: fold17正本（残余48 baseline・SHA-256 1175244d…）。fold18機械はfold17出版機械を隔離W複写でbyte-identical再実行した上でfold17レコードをchainingした
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張3行（intrinsic == claimed == 3行・49行exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1095
    note: 掃引のroot 00901010 probe記録（両AND順序uncapped 240,848/198,622・loss=true・terminal石数[14,18]）と主張3行の主張源（g01 master SHA pin 335eca5e…）
artifacts:
  - path: research/experiments/n11-residual48-win8-receipt-fold-root00901010-20261120/README.md
    role: source
    note: 入力pin・方法・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual48-win8-receipt-fold-root00901010-20261120/scripts/fold_win8_root00901010.py
    role: verifier
    note: 純Python・乱数なし・1,000行。チェーン全段frontier再計算・fold11〜17再実行gate・K1120/K1095/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual48-win8-receipt-fold-root00901010-20261120/output/win8-root00901010-receipt-fold-20261120.json
    role: data
    note: fold18正本（status fold-complete・SHA-256 18b543c4…・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold18-win8-root00901010-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold18-win8-root00901010-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit b5e1d5f6・先行出版）
---

# 残余48行のWIN8-D10 receipt fold root 00901010（fold18・第25 receipt）

K1120のWIN8-D10証明書（root `00000000000000801202000000901010`・13,422行・SHA-256 `d6745edb…`・本レーンが前段実行で抽出・三重検証・出版）を、五親S6 frontier receiptチェーンの第25 receiptとしてfoldした。fold17正本（残余48 baseline）からの続き。

## 主要結果

- **receipt は open 4 行を閉じた**: K1120/K1095/K1097 主張 3 行（5親target内）`00000000000000003800100008002000`（cost 74・unswept・c2×2）・`00000000000801202000000101000`（cost 71・unswept・c2×2）・`00000000000801202000000900000`（cost 68・unswept・c2×2）+ **target 外 open 1 行** `00000000000801202000000100010`（cost 81・unswept・c2×2・同じrootのC(8,6)部分集合幾何に内在）。余剰1行は `extra_s6_rows_not_in_target` として機械が分離記録（fail-closed設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 294・5親112行target 64 → 67・残余 48 → 45 行・frontier 6,161/488,094 → **6,157/487,800**・solved S6 1,687 → 1,691・parent行incidence 11,729 → 11,721（影響4 parent・いずれもclass 2: 15→14〔1行〕・19→17〔2行〕・59→57〔2行〕・37→34〔3行〕・完全閉鎖0）・s6_needed_by_open_classes 4,469 → 4,465・cost_needed_by_open_classes 354,542 → 354,248。
- fold17出版機械を隔離W複写（FOLD17_W）でbyte-identical再実行してから接続した（出版正本SHA-256 `1175244d…` と一致gate・fold16→fold15→…→fold11再帰rerunを含め8機連鎖rerun）。
- K1120監査19 gateを本機械で全再検証（g01 K1095 master SHA pin `335eca5e…`・g05 mobility 45・g06 uncapped probes 240,848/198,622〔andclose1/andclose0〕・terminal石数[14,18]・g07 3行定数gate・g13 nodes 631,539/524,342・g16 miss 0/extra 0・g19 footprint claimed == intrinsic == 3行・証明書全文byte検証 484,892 bytes/13,422行/third_method集計 terminal 4,336・visited 30,999・winner 20,028・loser 6,635・応手辺 28,516）。
- rootの6石部分幾何28 canonical行の分類: open-frontier 4（本receiptで閉鎖）・not-in-worklist 23・closed-before-this-receipt 1（`00000000000000003800000008003000`・K1096/fold11閉鎖済み）。
- win16候補は 9 → 8 根（主張 25 → 22 行）。残余23行掃引計画は不変（全win16主張と不交差を機械再確認）。
- 正本（SHA-256 `18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026`）は同一cwd 2回 + 別W複写・別プロセス・別HOME 1回の3実行でbyte-identical（GATE FAILED 0・約186秒/実行・43 input pin全て検証）。

## 解釈規約

fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

残余 45 行レーンでは、K1119（主張4行）・K1121（root `…8d10000`・主張3行・いずれも residual-45 内で open）の証明書の receipt fold（fold19 候補）と、抽出未着手・未宣言の WIN8 候補 3 根（`…840500`〔probe合計 1,614,800〕・`…80880200`〔1,287,426・掃引正本に出版probe記録なし〕・`00000000020809002000480100000`〔793,616・同・fresh-probeプロトコル拡張が必要〕・並走レーンが root `…0438…8180010`〔1,937,200〕の抽出を宣言済み）が着手時に単一オーナー宣言を要する未着手領域。
