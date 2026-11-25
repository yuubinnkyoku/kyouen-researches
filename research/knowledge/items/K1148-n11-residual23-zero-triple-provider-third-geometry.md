---
id: K1148
title: 残余23行の三行被覆根を第三の幾何計算で再導出し、3つの零provider行を候補根8個まで分解
kind: verification
status: verified
topics: [search-methods, certificates, geometry, verification]
aliases:
  - third independent geometric reconstruction of residual-23 triple providers
  - exact candidate-root explanation of the three zero-triple-provider rows in P-triple-prime
relations:
  - type: verifies
    target: K1097
    note: P‴上の残余23行三行provider数297・行別件数23値・零行3件を、D4向き三行和集合と4×4置換展開行列式による別経路で再導出する
  - type: verifies
    target: K1147
    note: K1147が記録したprovider件数・availability総和891・零行3件を、provider幾何の第三実装で検査する。K1147全体の再検証ではない
  - type: depends_on
    target: K1102
    note: 残余23行・REFUTED-D10除外根・既存行別availabilityの出典と比較対象
artifacts:
  - path: research/experiments/n11-residual23-zero-triple-provider-third-geometry-20261120/README.md
    role: source
    note: 906,752向き組の全数列挙、423候補根、297provider、零行候補8根の分類と解釈境界
  - path: research/experiments/n11-residual23-zero-triple-provider-third-geometry-20261120/scripts/audit_zero_triple_providers.py
    role: verifier
    note: 4×4行列式の24置換展開を用いる独立有限監査。既存3×3判定器・23行+2点生成器を呼ばない
  - path: research/experiments/n11-residual23-zero-triple-provider-third-geometry-20261120/input/residual23-provider-input.json
    role: data
    note: K1097/K1102/8根判定正本から転記した23行・除外50根・比較用行別件数。出典SHA-256を内包
  - path: research/experiments/n11-residual23-zero-triple-provider-third-geometry-20261120/output/third-geometry-audit.json
    role: data
    note: 第三実装の全12 gate、全23行availability、零行の8候補根と共円四点証人
  - path: research/log/2026-11-20-n11-residual23-zero-triple-provider-third-geometry.md
    role: log
    note: 発見順・再現性・出典pin・非主張の記録
scope: >-
  K1097/K1147の残余23行P‴における三行provider母集団と、三つの零provider行の有限幾何を検査する。
  23行から3行を選ぶ全1,771組・各D4向き8^3通りを列挙し、和集合サイズ8の候補根を抽出。
  4×4行列式の24置換展開で安全性を判定し、除外50根を差し引いて297 providerと行別件数を再導出する。
  これは候補root被覆の有限簿記であり、ゲーム木の勝敗・receipt・S6行閉鎖を主張しない。
evidence: >-
  906,752向き組の和集合サイズは8..14で8未満0。サイズ8の3,384向き組から423 D4正準根を得て、
  各根のC(8,6)=28子を再正準化すると全てちょうど3残余行を被覆した。4×4行列式を24置換で
  展開して安全316・unsafe107、うち安全だがREFUTED-D10除外済み19、P‴の三行provider297を得た。
  行別availabilityは既存判定正本の23値と完全一致し総和891=3×297。零行3件の候補根数は4/5/5、
  和集合は8根で、5根は共円四点を含み、3根は安全だが除外50根に含まれる。別cwd・HOME・
  PYTHONHASHSEEDの3実行で監査JSONがbyte-identical。入力fixtureは固定転記であり、検証器は
  元正本を実行時取得しない。
---
