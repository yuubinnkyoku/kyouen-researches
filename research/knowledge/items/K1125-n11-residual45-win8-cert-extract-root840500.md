---
id: K1125
title: 残余45行レーン WIN8-D10証明書抽出 root 840500（三重検証・19 gate・replace16掃引正本probe pin・残余候補3根の最終根）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 840500
  - K1089 replace16掃引系8石root（bit 8・mobility 58・probe合計 1,614,800）の完全勝利戦略29,468行（K1125）
relations:
  - type: depends_on
    target: K1089
    note: 残余72行 replace16 depth-10掃引正本（SHA-256 808fbda1…）の出版値（andclose1 736,409・andclose0 878,391・どちらもuncapped loss=true・[14,18]）と主張被覆3行をg01/g06/g07/g08でpin・照合
  - type: depends_on
    target: K1097
    note: win16 footprint（root 840500: claimed == intrinsic == 3行）をg19で照合
  - type: depends_on
    target: K1124
    note: 機材系譜の直接の親（抽出器・BigInt検証器・Bareiss検証器・監査機械が同一bytes・root定数のみ差し替え）。K1124でのK1089 replace16正本per_root probe pin再発見の訂正を継承
  - type: depends_on
    target: K1122
    note: fold18完了後の残余45行レーンで着手。主張3行はfold18閉鎖4行（3 claimed+1 extra）と着手前機械照合でdisjoint・fold18正本residual_row_hex_after 45行に3行とも現存
artifacts:
  - path: research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/certs/win8-root-00000000000000801202000000840500-20261120.n11
    role: certificate
    note: 1,067,425 bytes・29,468行・SHA-256 21ad6195…
  - path: research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 06c65f76…）
  - path: research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/scripts/cert_extractor_win8_root840500.ts
    role: source
    note: K1124抽出器のroot引数・filename guard差し替え版（探索核同一bytes・差分root hex定数3箇所のみ）
  - path: research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/scripts/assemble_win8_audit_root840500.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・K1124機械のroot定数差し替え版（出現回数assert・AST検証・旧定数残存grep 0）
  - path: research/experiments/n11-residual45-win8-cert-extract-root840500-20261120/scripts/gen_root_legal_moves.py
    role: source
    note: root初手58手の独立再導出（純Python整数3×3余因子幾何）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000801202000000840500-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 1d968ac4・最終根として先行出版）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000801202000000840500.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 840500 証明書抽出・三重検証

単一オーナー宣言ノート（commit `1d968ac4`・先行出版）の下で、
fold18/K1122直後の残余45行レーンにおいて、K1089 replace16 depth-10掃引正本
（SHA-256 `808fbda1…`）が両AND順序 uncapped（andclose1 736,409・andclose0 878,391・
どちらも loss=true）で WIN8-D10 candidate として確定済みの 8石root
`00000000000000801202000000840500`（石 [8,10,18,23,49,57,60,71]・quadruple-free
（順列展開厳密零判定70組全非零）・D4正準・loser初手58手）に対して、
完全勝利戦略証明書の盲抽出と三重検証を行った。**本根はK1089掃引正本per_root
辞書に出版probe pinを持つ残余候補3根の最後の未抽出根であり、本項で3根
（20809002=K1123並走・80880200=K1124本レーン・840500=K1125本レーン）の
抽出・出版がすべて完了する。**

選定: K1124で訂正済みのとおりK1089 replace16掃引正本のper_root辞書には
残余候補3根すべての uncapped loss=true [14,18] probe pinが存在し、
fresh-probe プロトコル拡張は不要。並走出版済みの 8180010・20809002
（K1123）と本レーン出版済みの 80880200（K1124）を除けば唯一の未抽出根が
本根（probe総nodes 1,614,800）であったためK1124の「次の一手」どおり宣言・着手した。
主張3行 `00000000000000801202000000800100`・`00000000000000801202000000800400`・
`00000000000000801202000000840000` はfold18/K1122閉鎖4行と着手前の機械照合で
disjointであり、fold18正本の残余45行 `residual_row_hex_after` に3行とも現存する。

**結果**: 証明書 29,468行・1,067,425 bytes（SHA-256
`21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc`）。
抽出は A1（初手毎58プロセス・xargs -P 4・総nodes 2,310,103・最大初手
209,633〔move 112〕・fbt_drops 0）・A2（完全再実行・初手単位 node-exact一致
〔58/58〕・rows byte-identical）・B（単一プロセス・総nodes 1,984,636
〔memo効果〕・戦略行不変）の3実行で行集合が完全一致（A1/A2組立cmp一致・
B sort -u行集合cmp一致）。三重検証（TS BigInt 3×3余因子・TS Bareiss 4×4・
python第三方法全木再走査）が visited 59,990・winner-to-move 38,458・
loser-to-move 11,722・loser応手辺 52,360・終端 9,810（全てloser-stuck）・
終端石数 [14,18]・consumed union 29,468 == 証明書行29,468
（missing 0/extra 0）の全数値で一致。Bareiss root-check: stones 8・
loserMobility 58。監査機械（K1124機械のroot定数差し替え版・g01 K1089正本
SHA pin・g05 mobility 58・g07主張3行・g08 bit 8 probe再現 node-exact・
g19 K1097 footprint三点一致を含む）は**19/19 gate PASS**（同一cwd 2回+
別cwd別プロセス1回〔EXPERIMENT_ROOT〕で監査JSON byte-identical・SHA-256
`06c65f76…`）。probe再現（runner v17 git blob `c132cc64…`・child=root−bit 8
= `00000000000000801202000000840400`・両順序×2回・pilot_d6 4剤）は
K1089出版値とnode-exact一致（736,409/878,391・[14,18]）。

主張3行は K1097 win16 footprint（intrinsic == claimed）とも一致した（g19）。
残余45行レーンでの receipt fold は別工程・別宣言である
（fold19は並走がroot `00000000000000801212000001009000`×K1119証明書で宣言済み
commit `3a23ccf3`）。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない（本抽出は行を
1つも閉じない）。REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として
読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**
