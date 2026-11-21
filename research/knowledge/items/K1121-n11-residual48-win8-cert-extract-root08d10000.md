---
id: K1121
title: 残余48行レーン WIN8-D10証明書抽出 root 08d10000（三重検証・19 gate・出版probe記録を持つ最安価未着手根）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 08d10000
  - K1091掃引系8石root（bit 16・mobility 50・probe合計 1,238,565）の完全勝利戦略28,328行（K1121）
relations:
  - type: depends_on
    target: K1091
    note: 残余72行 replace15 depth-10掃引の出版値（andclose1 564,695・andclose0 673,870・どちらもuncapped loss=true・[14,18]）と主張被覆3行をg01/g06/g07/g08でpin・照合
  - type: depends_on
    target: K1097
    note: "win16 footprint（root 08d10000: claimed == intrinsic == 3行）をg19で照合"
  - type: depends_on
    target: K1119
    note: 機材系譜の直接の親（抽出器・BigInt検証器・Bareiss検証器・監査機械が同一bytes・root定数のみ差し替え・K1091正本pinも同一）
  - type: depends_on
    target: K1118
    note: fold17完了後の残余48行レーンで着手。主張3行はfold17閉鎖7行（3 claimed+4 extra）と着手前機械照合でdisjoint・fold17正本residual_row_hex_after 48行に3行とも現存
  - type: depends_on
    target: K1120
    note: 直前の並走抽出（root 00901010・残余48レーン）。本抽出と同時進行・別root
artifacts:
  - path: research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/certs/win8-root-00000000000000003800000008d10000-20261120.n11
    role: certificate
    note: 1,026,202 bytes・28,328行・SHA-256 8513e366…
  - path: research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 0088ebab…）
  - path: research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/scripts/cert_extractor_win8_root08d10000.ts
    role: source
    note: K1119抽出器のroot引数・filename guard差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/scripts/assemble_win8_audit_root08d10000.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・K1119機械のroot定数差し替え版
  - path: research/experiments/n11-residual48-win8-cert-extract-root08d10000-20261120/scripts/gen_root_legal_moves.py
    role: source
    note: root初手50手の独立再導出（純Python整数3×3余因子幾何）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000003800000008d10000-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit b25b42af・先行出版）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000003800000008d10000.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 08d10000 証明書抽出・三重検証

単一オーナー宣言ノート（commit `b25b42af92622f02ef4c9a3151c80c2ea7bfa1f8`・先行出版）の
下で、K1091（残余72行 replace15 depth-10掃引）が両AND順序 uncapped（andclose1
564,695・andclose0 673,870・どちらも loss=true）で WIN8-D10 candidate として確定した
8石root `00000000000000003800000008d10000`（石 [16,20,22,23,27,59,60,61]・
quadruple-free・D4正準・loser初手50手）に対して、完全勝利戦略証明書の盲抽出と
三重検証を行った。fold17/K1118 直後の残余48行レーンで、抽出・fold済み9根・
並走抽出済み（K1120 root 00901010）を除く候補のうち、**出版probe記録（掃引正本pin）を
持ち、かつprobe両順序合計が最小（1,238,565）の根**である（主張3行）。出版probe
記録を持たない `00000000000020809002000480100000`（793,616・fresh-probe基盤という
プロトコル拡張が必要）よりも本根を優先して着手した。本rootの主張3行は
fold17閉鎖7行（K1118・3 claimed+4 extra）と着手前の機械照合でdisjointであり、
fold17正本の残余48行 `residual_row_hex_after` に3行とも現存する。

**結果**: 証明書 28,328行・1,026,202 bytes（SHA-256
`8513e36613c2676fb82816f47a1ecdda674264eedb9c583dae2616346f4000d2`・3実行
byte-identical）。抽出は A1（初手毎50プロセス・総nodes 2,428,240・最大初手
137,713〔move 2〕・fbt_drops 0）・A2（完全再実行・初手単位 node-exact一致・
rows byte-identical）・B（単一プロセス・総nodes 1,748,509〔memo効果〕・
戦略行不変）の3実行で行集合が完全一致。三重検証（TS BigInt 3×3余因子・
TS Bareiss 4×4・python第三方法全木再走査）が visited 83,544・
winner-to-move 53,570・loser-to-move 14,461・loser応手辺 72,930・
終端 15,513（全てloser-stuck）・終端石数 [14,18]・consumed union 28,328 ==
証明書行28,328（missing 0/extra 0）の全数値で一致。Bareiss root-check:
stones 8・loserMobility 50。監査機械（K1119機械のroot定数差し替え版・
g01 K1091正本SHA pin〔K1119と同一正本SHA edd7ac84…〕・g05 mobility 50・
g07主張3行〔gate名は3行版〕・g08 bit 16 probe再現 node-exact・g19 K1097
footprint三点一致を含む）は**19/19 gate PASS**（同一cwd 2回+別cwd別プロセス1回
で監査JSON byte-identical・SHA-256 `0088ebab…`）。probe再現（runner v17 git blob
`c132cc64…`・child=root−bit 16・両順序×2回・pilot_d6 4剤）はK1091出版値と
node-exact一致（564,695/673,870）。

主張3行 `00000000000000003800000008011000`・`00000000000000003800000008500000`・
`00000000000000003800000008900000` は K1097 win16 footprint（intrinsic == claimed）
とも一致した（g19）。残余48行レーンでの receipt fold は別工程・別宣言である。

K番号はpush前の再取得で最新main（K1120 root 00901010・並走出版）を確認し、
**K1121**を取得した。抽出未着手・未宣言のWIN8候補は残り4根
（`…840500`〔probe合計 1,614,800・K1119 log掲載値〕・`…81800010`〔1,937,200・
同左〕・`…80880200`〔1,287,426・同左〕・`00000000000020809002000480100000`
〔793,616・同左〕・主張12行）で、いずれも着手時に単一オーナー宣言を要する
（80880200・208090020004は掃引正本にprobe出版記録がなく、着手時にfresh-probe
基盤のプロトコル拡張の検討を要する）。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない（本抽出は行を
1つも閉じない）。REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として
読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**
