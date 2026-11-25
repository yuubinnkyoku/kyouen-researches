---
id: K1156
title: "残余23行の三つの零triple-provider行を行+2点生成で第四の幾何計算により独立再導出"
kind: computation
status: computed
topics: [geometry, certificates, verification]
aliases:
  - fourth independent direct row-plus-two-empty-points reconstruction of the three zero-triple-provider rows in the residual-23 eight-root-cover obstruction
relations:
  - type: verifies
    target: K1147
    note: K1147の8根被覆不可能性証明書が使う3零行の幾何前提を、行+2空点の全生成と直接4×4行列式で再導出し、k_min=2・残余容量19の算術へ接続する
  - type: verifies
    target: K1148
    note: K1148の3行×8³向き和集合とは異なる生成方向で、8候補根・被覆行・安全性分類・共円四点座標を完全照合する
artifacts:
  - path: research/experiments/n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/README.md
    role: source
    note: 方法・零行別集計・信頼境界・再現手順
  - path: research/experiments/n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/scripts/verify_direct_fourth.py
    role: verifier
    note: 12 gateの第四幾何検証器。行+2空点生成・D4正準化・全28子局面・4×4行列式24置換展開
  - path: research/experiments/n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/input/residual23-provider-input.json
    role: source
    note: K1148由来の23行・除外50根・出典pin付き入力fixture
  - path: research/experiments/n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/input/k1148-third-geometry-audit.json
    role: data
    note: K1148第三幾何の固定監査正本。SHA-256 pinで照合
  - path: research/experiments/n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/input/k1147-external-audit.json
    role: data
    note: K1147外部第二検証の固定監査正本。71 gate・零行・全provider最大被覆3の記録を照合
  - path: research/experiments/n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/output/direct-fourth-geometry-audit.json
    role: data
    note: 監査正本。12 gate PASS・SHA-256 c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f
  - path: research/log/2026-11-21-n11-residual23-zero-triple-provider-direct-fourth-geometry.md
    role: log
    note: 実行経緯・初回実装の修正・再現性・制約・解釈境界
  - path: research/log/2026-11-21-n11-residual23-zero-triple-provider-direct-fourth-geometry-single-owner-note.md
    role: log
    note: 着手前の単一オーナー宣言（commit b0db8dfec12b163ec51292922fc5fab4fac3ff66）
  - path: research/experiments/n11-residual23-zero-triple-forbidden-circle-structure-20261121/README.md
    role: source
    note: 14候補出現を3禁止四点・2 D4円軌道へ分類した構造解析
  - path: research/experiments/n11-residual23-zero-triple-forbidden-circle-structure-20261121/scripts/derive_forbidden_circles.py
    role: verifier
    note: Fractionによる円の再導出・D4軌道・中央点通過を検査する標準ライブラリ検証器
  - path: research/experiments/n11-residual23-zero-triple-forbidden-circle-structure-20261121/input/residual23-provider-input.json
    role: source
    note: K1156の固定入力fixture
  - path: research/experiments/n11-residual23-zero-triple-forbidden-circle-structure-20261121/input/k1156-direct-fourth-audit.json
    role: data
    note: K1156第四幾何の固定監査正本
  - path: research/experiments/n11-residual23-zero-triple-forbidden-circle-structure-20261121/output/forbidden-circle-structure.json
    role: data
    note: 2 D4円軌道・10 unsafe出現・4 safe除外出現の監査正本
  - path: research/log/2026-11-21-n11-residual23-zero-triple-forbidden-circle-structure.md
    role: log
    note: 構造解析・再現性・制約・次の判断
scope: >-
  K1147の残余23行8根被覆不可能性証明書が使う3零triple-provider行について、各行に空き2点を加える全C(115,2)生成から8石根を再導出する。各根をD4正準化しC(8,6)=28子局面を再構成し、4×4整数行列式を24置換で展開して共円四点の有無を判定する。K1148の3行×8³向き和集合生成器と既存3×3行列式述語は使用しない。対象は3零行に触れる根のみであり、P'''全providerの再生成、DFPN probe、証明書抽出、receipt fold、S6行閉鎖は含まない。
  追加構造解析では14候補出現（unsafe 10・safe REFUTED-D10除外4）をD4埋込みから再構成し、unsafeの10出現を3正準四点・2 D4円軌道へ分類した。全円が(5,5)を通り、半径二乗13/2・25/2の出現数は各5。3零行はすべて中央点と軸上の連続3点を持つ。検証器SHA-256 45e5d7d61781e96e1e0afff8f457f06ff69a00a2b5e6777dc03d710e2a122951、監査SHA-256 0e16f29b259eac1864ce826324f5a51dfe4d5bd5946a0ea5ef7998daaf39c638。2実行（同一cwd・隔離cwd/PYTHONHASHSEED=random）byte-identical、offset 100のtamperはpinでfail-closed。
evidence: >-
  K1148入力fixture（SHA-256 51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822）、K1148第三幾何監査（526eada2c94457f06a7cf27a86011586e394c342687e539a6b545b42577b9573）、K1147外部監査（17dbd6ab3a9a9b5aef1cf1cf517a5a0fd216dff755f0ed86fcf029e1612cabcb）を固定pinした。各零行につき6,555生成・6,555 D4根、合計19,665生成事象と550,620子局面を検査。三行候補根は4/5/5、和集合8根（共円四点あり5・安全だがREFUTED-D10除外済み3・P''' eligible 0）で、K1148の全8根・被覆行・分類・共円四点座標と完全一致。K1147の71 gateとglobal max-cover-3・算術gateも照合。12 gate PASS、通常・別cwd・PYTHONHASHSEED=randomの3実行がbyte-identical（監査SHA-256 c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f）。fixtureの1 byte改変はpinで検出され、出力未作成。K1147の全provider最大3行被覆とREFUTED-D10除外集合は既存正本から継承し、本検査はその全域を再導出しない。被覆は候補計画の簿記であり、行は1行も閉じない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWN。
---

本項目は、残余23行の3つの零triple-provider行に対する幾何前提の第四再導出を記録する。K1147の8根被覆不可能性算術とK1148の第三幾何を照合し、行+2空点の直接生成・4×4整数行列式で同じ8候補根を再現した。これはゲーム木の勝敗判定ではなく、証明書・receipt・行閉鎖を増やすものでもない。

## 追加構造解析（2026-11-21）

K1156の14候補出現を後解析すると、unsafe 10出現に現れる禁止四点は3種類だが、D4円軌道は2種類だけである。正準四点から得る円は `x²+y²−11x−5y+30=0`、`x²+y²−17x−9y+80=0`、`x²+y²−5x−11y+30=0`。すべて (5,5) を通り、半径二乗は13/2または25/2。最初と3番目は座標交換で同じ軌道に属する。

三つの零行もすべて (5,5) と、その点を中心にした横または縦の連続3点を持つ。unsafe候補の出現数は2軌道で5件ずつ、異なる根数は2個と3個。残るsafe 4出現はREFUTED-D10除外に依存し、幾何だけでは排除されない。

この追加解析はK1156の全数列挙の完全性を引き継ぎ、候補14出現の円を有理数演算で再導出したもの。新規probe・証明書・receipt・行閉鎖はない。