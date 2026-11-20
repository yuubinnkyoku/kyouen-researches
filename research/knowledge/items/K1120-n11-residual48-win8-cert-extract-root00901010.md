---
id: K1120
title: 残余48行レーン WIN8-D10証明書抽出 root 00901010（三重検証・19 gate・K1095最安価未着手根）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 00901010
  - K1095候補8石root（bit 4・mobility 45）の完全勝利戦略13,422行（K1120）
relations:
  - type: depends_on
    target: K1095
    note: 代替12根 depth-10掃引の出版値（andclose1 198,622・andclose0 240,848・どちらもuncapped loss=true・[14,18]）と主張被覆3行をg01/g06/g07/g08でpin・照合
  - type: depends_on
    target: K1097
    note: win16 footprint（root 00901010: claimed == intrinsic == 3行）をg19で照合
  - type: depends_on
    target: K1117
    note: 機材系譜の直接の親（抽出器・BigInt検証器・Bareiss検証器・監査機械が同一bytes・root定数のみ差し替え）
  - type: depends_on
    target: K1116
    note: fold16完了後の残余51行で主張3行がopenであることを確認（fold16閉鎖5行とdisjoint）
  - type: depends_on
    target: K1118
    note: fold17完了後の残余48行レーンで着手。主張3行はfold17閉鎖7行（3 claimed+4 extra）と着手前機械計算でdisjoint・fold17正本residual_row_hex_after 48行に3行とも現存
artifacts:
  - path: research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120/certs/win8-root-00000000000000801202000000901010-20261120.n11
    role: certificate
    note: 484,892 bytes・13,422行・SHA-256 d6745edb…
  - path: research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 ea6f1945…）
  - path: research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120/scripts/cert_extractor_win8_root00901010.ts
    role: source
    note: K1117抽出器のroot引数・filename guard差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120/scripts/assemble_win8_audit_root00901010.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・K1117機械のroot定数差し替え版
  - path: research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120/scripts/gen_root_legal_moves.py
    role: source
    note: root初手45手の独立再導出（純Python整数3×3余因子幾何）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root801202000000901010-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit f08f2ca1・先行出版。直前c9013521はplaceholder誤pushの記録で1分以内に置換修復）
  - path: research/log/2026-11-20-n11-residual48-win8-cert-extract-root00901010.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 00901010 証明書抽出・三重検証

単一オーナー宣言ノート（commit `f08f2ca106041b827659f28c4c7201f73f2bcb05`・先行出版）の
下で、K1095 代替12根 depth-10 掃引が両AND順序 uncapped（andclose1 198,622・
andclose0 240,848・どちらも loss=true）で WIN8-D10 candidate として確定した
8石root `00000000000000801202000000901010`（石 [4,12,20,23,49,57,60,71]・
quadruple-free・D4正準・loser初手45手）に対して、完全勝利戦略証明書の盲抽出と
三重検証を行った。fold17/K1118 直後の残余48行レーンで、抽出・fold済み7根・
並走抽出宣言済み根（`…1009000`〔93f56291・着手中〕・`…8180000`〔4496c888〕・
`…0810000a`）を除く**最安価の未着手根**である（probe両順序合計 439,470・主張3行）。
本rootの主張3行は fold16（K1116・閉鎖5行）・fold17（K1118・閉鎖7行=3 claimed+
4 extra target外）のいずれの閉鎖行とも着手前の独立計算でdisjointであり、
fold17正本の残余48行 `residual_row_hex_after` に3行とも現存する。
宣言ノート出版（04:39Z頃）直前にはfold17（K1118・`e24c2927`）が出版されていた
ため、実験名・残余表記は残余48行レーンとしている。

**結果**: 証明書 13,422行・484,892 bytes（SHA-256
`d6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1`・3実行
byte-identical）。抽出は A1（初手毎45プロセス・総nodes 631,539・最大初手
113,339〔move 118〕・fbt_drops 0）・A2（完全再実行・初手単位 node-exact一致・
rows byte-identical）・B（単一プロセス・別cwd・総nodes 524,342〔memo効果〕・
戦略行不変）の3実行で行集合が完全一致。三重検証（TS BigInt 3×3余因子・
TS Bareiss 4×4・python第三方法全木再走査）が visited 30,999・
winner-to-move 20,028・loser-to-move 6,635・loser応手辺 28,516・
終端 4,336（全てloser-stuck）・終端石数 [14,18]・consumed union 13,422 ==
証明書行13,422（missing 0/extra 0）の全数値で一致。監査機械（K1117機械のroot定数
差し替え版・g01 K1095正本SHA pin・g05 mobility 45・g07主張3行・g08 bit 4 probe再現
node-exact・g19 K1097 footprint三点一致を含む）は**19/19 gate
PASS**（同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical・SHA-256
`ea6f1945…`）。probe再現（runner v17 git blob `c132cc64…`・child=root−bit 4・
両順序×2回・pilot_d6 4剤）はK1095出版値とnode-exact一致（198,622/240,848）。

主張3行 `00000000000000003800100008002000`・`00000000000801202000000101000`・
`00000000000801202000000900000` は K1097 win16 footprint（intrinsic == claimed）
とも一致した（g19）。残余48行レーンでの receipt fold は別工程・別宣言である
（fold18候補）。

運用記録: 宣言ノートの初回push（commit `c9013521`）でrun_typescriptの実行
再評価に伴い内容文字列を失いplaceholderを出版してしまった（数十秒〜1分で
全文置換修復・commit `f08f2ca1`）。また機材のroot差し替えを手書きhexで行うと
先行ゼロ落ち（29文字hex）による滑り違いがあり得ることを確認し、
「JSON正本の鍵から文字列をプログラム的に取って置換する」手順に切り替えた
（詳細は研究log）。証明書フォーマットの `{32}` 正規表現・root行照合が
fail-closedに機能する構造であることも確認した。

K番号はpush前の再取得で最新mainを確認したところ、着手中に並走レーンが
root `…1009000` の抽出を **K1119** として出版していた（commits `3645dea19a`〜
`f56f5aff5b`・04:41Z・16,262行・残余48とは別root）のため、衝突側再採番規約により
**K1120** を取得した（README grep K1120 0件）。

抽出未着手・未宣言のWIN8候補は残り5根
（`…08d10000`〔probe 564,695/673,870〕・`…08180010`〔882,327/1,054,873〕・
`…0840500`〔736,409/878,391〕・`…80880200`・
`00000000020809002000480100000`・主張15行）で、いずれも着手時に
単一オーナー宣言を要する（`…80880200`と`00000000020809002000480100000`の
probe nodesはK1089一次正本のprobe-recordsに数値未収録・着手前に再計算を要する）。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold は別工程であり、行の閉鎖claimは本項では行わない（本抽出は行を
1つも閉じない）。REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として
読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**
