---
id: K1119
title: 残余51行レーン WIN8-D10証明書抽出 root 1009000（三重検証・19 gate・probe総nodes 421,867最小）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 1009000
  - 残余51行WIN8候補最安価8石root（probe総nodes 421,867）の完全勝利戦略16,262行（K1119）
relations:
  - type: depends_on
    target: K1091
    note: fold15後残余確定用の代替根 depth-10掃引の出版値（andclose1 192,365・andclose0 229,502・どちらもuncapped loss=true・[14,18]）と主張被覆4行をg01/g06/g07/g08でpin・照合
  - type: depends_on
    target: K1097
    note: win16 footprint（root 1009000: claimed == intrinsic == 4行）をg19で照合
  - type: depends_on
    target: K1117
    note: 機材系譜の直接の親（抽出器・BigInt検証器・Bareiss検証器・監査機械が同一bytes・root定数のみ差し替え）
  - type: depends_on
    target: K1116
    note: fold16完了後の残余51行レーンで着手（着手権は宣言93f56291で確定）
  - type: depends_on
    target: K1118
    note: 実行中に並走が出版したfold17（残余51→48）。本rootの主張4行はfold17閉鎖7行と着手後の機械照合でdisjoint・残余48行内でopen
artifacts:
  - path: research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/certs/win8-root-00000000000000801212000001009000-20261120.n11
    role: certificate
    note: 587,989 bytes・16,262行・SHA-256 b4dd1e06…
  - path: research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 4696ce14…）
  - path: research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/scripts/cert_extractor_win8_root1009000.ts
    role: source
    note: K1117抽出器のroot引数・filename guard差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/scripts/assemble_win8_audit_root1009000.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・K1113機械系譜のroot定数差し替え版・g19継承（len 4行）
  - path: research/experiments/n11-residual51-win8-cert-extract-root1009000-20261120/scripts/gen_root_legal_moves.py
    role: source
    note: root初手44手の独立再導出（純Python整数3×3余因子幾何）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000801212000001009000-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 93f56291・先行出版）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000801212000001009000.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 1009000 証明書抽出・三重検証

単一オーナー宣言ノート（commit `93f56291df82955662017397e2be953b3c01ffd9`・先行出版）の
下で、K1091 掃引（fold15後残余確定用の代替根 depth-10）が両AND順序 uncapped
（andclose1 192,365・andclose0 229,502・どちらも loss=true）で WIN8-D10 candidate
として確定した 8石root `00000000000000801212000001009000`（石
[12,15,24,49,52,57,60,71]・quadruple-free・D4正準・loser初手44手）に対して、
完全勝利戦略証明書の盲抽出と三重検証を行った。fold16/K1116 直後の残余51行レーンで、
抽出・fold済み7根（8003180・8005021・9840004・9090022・8890020・120000038・
22081000/K1117）を除く**最安価の未着手・未宣言根**である（probe両順序合計
421,867 が残り候補中最小・主張4行）。実行中に並走がfold17/K1118（root 22081000の
receipt fold・残余51→48）を出版したが、本rootの主張4行はfold17の閉鎖7行（K1117主張
3行+target外余剰4行）と着手後の機械照合で完全にdisjointであり、残余48行内で
openのままである。

**結果**: 証明書 16,262行・587,989 bytes（SHA-256
`b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c`・3実行
byte-identical）。抽出は A1（初手毎44プロセス・総nodes 865,602・最大初手
73,618〔move 99〕・fbt_drops 0）・A2（完全再実行・初手単位 node-exact一致・
rows byte-identical）・B（単一プロセス・総nodes 712,106〔memo効果〕・
戦略行不変）の3実行で行集合が完全一致。三重検証（TS BigInt 3×3余因子・
TS Bareiss 4×4・python第三方法全木再走査）が visited 37,696・
winner-to-move 24,352・loser-to-move 7,561・loser応手辺 34,261・
終端 5,783（全てloser-stuck）・終端石数 [14,18]・consumed union 16,262 ==
証明書行16,262（missing 0/extra 0）の全数値で一致。Bareiss root-check:
stones 8・loserMobility 44。監査機械（K1113機械系譜のroot定数
差し替え版・g01 K1091正本SHA pin・g05 mobility 44・g07主張4行・g08 bit 12 probe再現
node-exact・g19 K1097 footprint三点一致を含む）は**19/19 gate
PASS**（同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical・SHA-256
`4696ce14…`）。probe再現（runner v17 git blob `c132cc64…`・child=root−bit 12・
両順序×2回・pilot_d6 4剤）はK1091出版値とnode-exact一致。

主張4行 `00000000000000003800200008001000`・`00000000000000003800200009000000`・
`00000000000000801212000000001000`・`00000000000000801212000001000000` は K1097
win16 footprint（intrinsic == claimed）とも一致した（g19）。残余48行レーンでの
 receipt fold は別工程・別宣言である。

K番号はpush前の再取得で最新main（K1118のfold17直後）を確認し、**K1119**を取得した。
抽出未着手・未宣言のWIN8候補は残り5根（`…08d10000`・`…840500`・`…80880200`・
`00000000000020809002000480100000`・`00000000000000043800000008180010`）で、
いずれも着手時に単一オーナー宣言を要する（：901010は並走が宣言済み commit
`c90135217c`・着手中）。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない（本抽出は行を
1つも閉じない）。REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として
読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**
