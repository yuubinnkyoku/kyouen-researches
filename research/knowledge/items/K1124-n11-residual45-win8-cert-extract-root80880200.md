---
id: K1124
title: 残余45行レーン WIN8-D10証明書抽出 root 80880200（三重検証・19 gate・replace16掃引正本probe pinの再発見による最安価未宣言根）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 80880200
  - K1089 replace16掃引系8石root（bit 9・mobility 46・probe合計 1,287,426）の完全勝利戦略25,783行（K1124）
relations:
  - type: depends_on
    target: K1089
    note: 残余72行 replace16 depth-10掃引正本（SHA-256 808fbda1…）の出版値（andclose1 618,359・andclose0 669,067・どちらもuncapped loss=true・[14,18]）と主張被覆3行をg01/g06/g07/g08でpin・照合。K1121「80880200は出版probe記録なし」という記載の訂正源
  - type: depends_on
    target: K1097
    note: "win16 footprint（root 80880200: claimed == intrinsic == 3行）をg19で照合"
  - type: depends_on
    target: K1121
    note: 機材系譜の直接の親（抽出器・BigInt検証器・Bareiss検証器・監査機械が同一bytes・root定数のみ差し替え）
  - type: depends_on
    target: K1122
    note: fold18完了後の残余45行レーンで着手。主張3行はfold18閉鎖4行（3 claimed+1 extra）と着手前機械照合でdisjoint・fold18正本residual_row_hex_after 45行に3行とも現存
artifacts:
  - path: research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/certs/win8-root-00000000000000801202000800880200-20261120.n11
    role: certificate
    note: 934,278 bytes・25,783行・SHA-256 eca214f0…
  - path: research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 422e6109…）
  - path: research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/scripts/cert_extractor_win8_root80880200.ts
    role: source
    note: K1121抽出器のroot引数・filename guard差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/scripts/assemble_win8_audit_root80880200.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・K1121機械のroot定数差し替え版
  - path: research/experiments/n11-residual45-win8-cert-extract-root80880200-20261120/scripts/gen_root_legal_moves.py
    role: source
    note: root初手46手の独立再導出（純Python整数3×3余因子幾何）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000801202000800880200-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit de0a505b・先行出版・K1089 replace16正本pinの再発見とK1121記載の訂正を明記）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000801202000800880200.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 80880200 証明書抽出・三重検証

単一オーナー宣言ノート（commit `de0a505bc8332b748a9f0622f26b1846224bf00b`・先行出版）の
下で、fold18/K1122直後の残余45行レーンにおいて、K1089 replace16 depth-10掃引正本
（SHA-256 `808fbda1…`）が両AND順序 uncapped（andclose1 618,359・andclose0 669,067・
どちらも loss=true）で WIN8-D10 candidate として確定済みの 8石root
`00000000000000801202000800880200`（石 [9,19,23,35,49,57,60,71]・quadruple-free・
D4正準・loser初手46手）に対して、完全勝利戦略証明書の盲抽出と三重検証を行った。

**選定の訂正**: 先行するK1121のREADME・研究ログは「80880200・20809002は掃引正本に
出版probe記録がなく fresh-probe基盤のプロトコル拡張を要する」と記載していたが、
K1089 replace16掃引正本のper_root辞書には残余候補3根（80880200: 618,359/669,067・
20809002: 350,792/442,824・840500: 736,409/878,391）すべての uncapped
loss=true probe pinが存在した（本項の先行出版宣言ノートで訂正を明記）。
並走が抽出宣言済みの 8180010・20809002 を除けば最安価な未宣言根
（1,287,426 < 840500の1,614,800）として本根を着手した。主張3行
`0000000000000000380000000a002000`・`00000000000000801202000000800200`・
`00000000000000801202000000880000` はfold18/K1122閉鎖4行と着手前の機械照合で
disjointであり、fold18正本の残余45行 `residual_row_hex_after` に3行とも現存する。

**結果**: 証明書 25,783行・934,278 bytes（SHA-256
`eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf`・3実行
byte-identical）。抽出は A1（初手毎46プロセス・総nodes 1,670,778・最大初手
193,088〔move 98〕・fbt_drops 0）・A2（完全再実行・初手単位 node-exact一致・
rows byte-identical）・B（単一プロセス・総nodes 1,383,269〔memo効果〕・
戦略行不変）の3実行で行集合が完全一致。三重検証（TS BigInt 3×3余因子・
TS Bareiss 4×4・python第三方法全木再走査）が visited 57,636・
winner-to-move 37,121・loser-to-move 11,311・loser応手辺 52,219・
終端 9,204（全てloser-stuck）・終端石数 [14,18]・consumed union 25,783 ==
証明書行25,783（missing 0/extra 0）の全数値で一致。Bareiss root-check:
stones 8・loserMobility 46。監査機械（K1121機械のroot定数差し替え版・
g01 K1089正本SHA pin・g05 mobility 46・g07主張3行・g08 bit 9 probe再現
node-exact・g19 K1097 footprint三点一致を含む）は**19/19 gate PASS**
（同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical・SHA-256 `422e6109…`）。
probe再現（runner v17 git blob `c132cc64…`・child=root−bit 9・両順序×2回・
pilot_d6 4剤）はK1089出版値とnode-exact一致（618,359/669,067）。

主張3行は K1097 win16 footprint（intrinsic == claimed）とも一致した（g19）。
残余45行レーンでの receipt fold は別工程・別宣言である
（fold19は並走がK1119×fold root宣言済み commit `3a23ccf3`）。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない（本抽出は行を
1つも閉じない）。REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として
読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**

