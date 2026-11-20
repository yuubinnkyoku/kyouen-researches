---
id: K1117
title: 残余55行レーン WIN8-D10証明書抽出 root 22081000（三重検証・19 gate・歴代最小mobility 39）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 22081000
  - 残余55行WIN8候補最安価8石root（mobility 39）の完全勝利戦略9,460行（K1117）
relations:
  - type: depends_on
    target: K1095
    note: 代替12根 depth-10掃引の出版値（andclose1 126,683・andclose0 137,565・どちらもuncapped loss=true・[14,18]）と主張被覆3行をg01/g06/g07/g08でpin・照合
  - type: depends_on
    target: K1097
    note: win16 footprint（root 22081000: claimed == intrinsic == 3行）をg19で照合
  - type: depends_on
    target: K1113
    note: 機材系譜の直接の親（抽出器・BigInt検証器・Bareiss検証器・監査機械が同一bytes・root定数のみ差し替え）
  - type: depends_on
    target: K1115
    note: fold15完了後の残余55行レーンで着手。主張3行はfold15正本の残余55行に含まれる
  - type: depends_on
    target: K1116
    note: 実行中に並走が出版したfold16。本rootの主張3行はfold16閉鎖5行と着手前に機械計算済みのdisjoint
artifacts:
  - path: research/experiments/n11-residual55-win8-cert-extract-root22081000-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual55-win8-cert-extract-root22081000-20261120/certs/win8-root-00000000000000801202000022081000-20261120.n11
    role: certificate
    note: 341,498 bytes・9,460行・SHA-256 f62f6704…
  - path: research/experiments/n11-residual55-win8-cert-extract-root22081000-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 3d97ac6d…）
  - path: research/experiments/n11-residual55-win8-cert-extract-root22081000-20261120/scripts/cert_extractor_win8_root22081000.ts
    role: source
    note: K1113抽出器のroot引数・filename guard差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual55-win8-cert-extract-root22081000-20261120/scripts/assemble_win8_audit_root22081000.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・K1113機械のroot定数差し替え版・g19継承（len 3行）
  - path: research/experiments/n11-residual55-win8-cert-extract-root22081000-20261120/scripts/gen_root_legal_moves.py
    role: source
    note: root初手39手の独立再導出（純Python整数3×3余因子幾何）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root801202200022081000-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 22eb87df・先行出版）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root801202200022081000.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 22081000 証明書抽出・三重検証

単一オーナー宣言ノート（commit `22eb87dfaf19bd1518c195976d33b16319d8cf49`・先行出版）の
下で、K1095 代替12根 depth-10 掃引が両AND順序 uncapped（andclose1 126,683・
andclose0 137,565・どちらも loss=true）で WIN8-D10 candidate として確定した
8石root `00000000000000801202000022081000`（石 [12,19,25,29,49,57,60,71]・
quadruple-free・D4正準・loser初手39手 = 歴代抽出根最小mobility）に対して、
完全勝利戦略証明書の盲抽出と三重検証を行った。fold15/K1115 直後の残余55行レーンで、
抽出・fold済み6根・並走抽出宣言済み2根（`…8180000`・`…0810000a`）を除く
**最安価の未着手根**である（probe両順序合計 264,248 最小・mobility 39最小・主張3行）。
着手時にfold16は並走の宣言済み着手中で、本rootの主張3行はfold16閉鎖5行（主張4行+
余剰1行）と着手前の独立計算でdisjointを確認済みだったため、fold16の成否に依らず
抽出・検証を実施した（実行中にfold16はK1116として出版された。主張3行は
残余51行のままopen）。

**結果**: 証明書 9,460行・341,498 bytes（SHA-256
`f62f6704a0d9a1366d333529dd9e742813fe87814f3857a00406d6cfc87f3c8f`・3実行
byte-identical）。抽出は A1（初手毎39プロセス・総nodes 731,232・最大初手
54,999〔move 76〕・fbt_drops 0）・A2（完全再実行・初手単位 node-exact一致・
rows byte-identical）・B（単一プロセス・総nodes 534,121〔memo効果〕・
戦略行不変）の3実行で行集合が完全一致。三重検証（TS BigInt 3×3余因子・
TS Bareiss 4×4・python第三方法全木再走査）が visited 23,542・
winner-to-move 15,228・loser-to-move 5,032・loser応手辺 22,031・
終端 3,282（全てloser-stuck）・終端石数 [14,18]・consumed union 9,460 ==
証明書行9,460（missing 0/extra 0）の全数値で一致。監査機械（K1113機械のroot定数
差し替え版・g01 K1095正本SHA pin・g05 mobility 39・g07主張3行・g08 bit 12 probe再現
node-exact・g19 K1097 footprint三点一致を含む）は**19/19 gate
PASS**（同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical・SHA-256
`3d97ac6d…`）。probe再現（runner v17 git blob `c132cc64…`・child=root−bit 12・
両順序×2回・pilot_d6 4剤）はK1095出版値とnode-exact一致。

主張3行 `00000000000000003800000808001000`・`00000000000000801202000000081000`・
`00000000000000801202000020001000` は K1097 win16 footprint（intrinsic == claimed）
とも一致した（g19）。残余51行レーンでの receipt fold は別工程・別宣言である。

K番号はpush前の再取得で最新main（K1116のfold16直後）を確認し、**K1117**を取得した。
抽出未着手・未宣言のWIN8候補は残り7根（`…08d10000`・`…840500`・`…901010`・
`…80880200`・`…1009000`・`00000000000020809002000480100000`・`00000000000000043800000008180010`・
主張25行）で、いずれも着手時に単一オーナー宣言を要する。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない（本抽出は行を
1つも閉じない）。REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として
読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**
