---
id: K1123
title: 残余48行レーン WIN8-D10証明書抽出 root 208090020004（fresh-probe基盤第1例・三重検証・19 gate・probe総nodes 793,616最小）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 208090020004
  - fresh-probe基盤（掃引正本pinなし）WIN8-D10証明書抽出の第1例（K1123）
relations:
  - type: depends_on
    target: K1089
    note: replacement16掃引で本rootがWIN8-D10候補として確定（K1091/K1095掃引正本per_rootに記録なし）
  - type: depends_on
    target: K1097
    note: win16 footprint（root 208090020004: claimed == intrinsic == 3行）をg07/g19で照合
  - type: depends_on
    target: K1119
    note: 機材系譜とprobe pinの両親（fresh-probe総nodes 793,616の出版記録・研究log git blob 51bad3fa…をg01/g02でpin・抽出器はroot引数のみ差し替え）
  - type: depends_on
    target: K1118
    note: fold17直後の残余48行レーンで着手（宣言はfold18出版前）
  - type: depends_on
    target: K1122
    note: 実行中に並走が出版したfold18（残余48→45）。主張3行はfold18正本の残余45行内でopen（g19）
artifacts:
  - path: research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/certs/win8-root-00000000000020809002000480100000-20261120.n11
    role: certificate
    note: 855,258 bytes・23,621行・SHA-256 b8145352…
  - path: research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 6ea634c9…）
  - path: research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/scripts/cert_extractor_win8_root20809002000480100000.ts
    role: source
    note: K1121抽出器のroot引数・filename guard差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/scripts/assemble_win8_audit_root208090020004.py
    role: verifier
    note: 第三方法監査機械・fresh-probe基盤gate再構成版（g01/g02=K1119 log pin・g06/g08=fresh-probe・g07/g19=K1097 footprint・g19にfold18残余45行open検査を含む）
  - path: research/experiments/n11-residual48-win8-cert-extract-root208090020004-20261120/scripts/gen_root_legal_moves.py
    role: source
    note: root初手54手の独立再導出（純Python整数3x3余因子幾何）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000020809002000480100000-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit e75c65b4・先行出版）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000020809002000480100000.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 208090020004 証明書抽出・三重検証（fresh-probe基盤第1例）

単一オーナー宣言ノート（commit `e75c65b47632398474797de40922acad043cf560`・先行出版）の
下で、K1089 replacement16掃引が WIN8-D10 candidate とした 8石root
`00000000000020809002000480100000`（石 [20,31,34,49,60,63,71,77]・quadruple-free・
D4正準・loser初手54手）に対して、完全勝利戦略証明書の盲抽出と三重検証を行った。
本rootはK1091掃引正本 per_root（15根）・K1095掃引正本 per_root（12根）のいずれにも
probe記録がなく（K1089系）、**出版probe記録を持たない未着手・未宣言候補の中で
probe総nodesが最小**（K1119研究log出版値 793,616）である。掃引正本pinの代わりに
K1119研究log（git blob `51bad3fa…`・SHA-256 `4d11ca89…`）の出版値をpinし、本実験の
fresh-probe（runner v17・child=root−bit 20・両AND順序×2回・pilot_d6 4剤）が
andclose1 350,792 / andclose0 442,824・合計 793,616 をnode-exact再現した。
**fresh-probe基盤のプロトコル拡張を適用した第1例**であり、以後の同系根
（80880200・840500）の抽出はこの基盤を踏襲できる。

**結果**: 証明書 23,621行・855,258 bytes（SHA-256
`b8145352cc1d8e21247595bdaedcb123c8e34cf0fb476502a561b46a106f701e`・3実行
byte-identical）。抽出は A1（初手毎54プロセス・総nodes 3,009,765・最大初手
165,221〔move 117〕・fbt_drops 0）・A2（完全再実行・初手単位 node-exact一致・
rows byte-identical）・B（単一プロセス・nodes 3,009,765・A1と同一会計・K1109 root
9090022と同型）の3実行で行集合が完全一致。三重検証（TS BigInt 3x3余因子・
TS Bareiss 4x4・python第三方法全木再走査）が visited 49,094・winner-to-move 31,623・
loser-to-move 9,955・loser応手辺 43,650・終端 7,516（全loser-stuck）・終端石数
[14,18]・consumed union == 23,621 == 証明書行（missing 0 / extra 0）の全数値で一致。
Bareiss root-check: stones 8・loserMobility 54。監査機械はfresh-probe基盤gate再構成版で
**19/19 gate PASS**（同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical・
SHA-256 `6ea634c9fdd005626904669e08cb7139e59e78120a0b8c9e1dd48fde0b70ddf0`）。

主張3行 `00000000000000801202040000001000`・`00000000000000801202040000800000`・
`00000000000020809002000080000000` は K1097 win16 footprint（intrinsic == claimed）
と一致し（g07/g19）、実行中に並走が出版したfold18/K1122（残余48→45）の閉鎖4行
（3 claimed + 1 extra）と完全にdisjointで、fold18正本の残余45行内でopenである（g19）。

K番号はpush前の再取得で最新main（K1122 fold18出版後）を確認し、**K1123**を取得した。
残余レーンの未着手・未宣言WIN8候補は本抽出と並走宣言（80880200: de0a505bc8・
81800010: bda9e5b2c4）の後に `…840500`（probe総nodes 1,614,800・K1119 log出版値）の
1根のみが残る。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない（本抽出は行を
1つも閉じない）。REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として
読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**
