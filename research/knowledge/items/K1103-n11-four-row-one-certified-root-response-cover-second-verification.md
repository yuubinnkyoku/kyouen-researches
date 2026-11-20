---
id: K1103
title: 残余72行の4親行に対するK1096単独証明根・二手応答被覆の独立第二検証
kind: verification
status: verified
topics: [search-methods, certificates, geometry]
aliases:
  - K1096-only four-row WIN8 two-ply response-cover second verification
  - 4親行の304初手義務をK1096の8被覆と148追加根で完全分割する最小幾何計画
relations:
  - type: depends_on
    target: K1096
    note: 唯一の証明書検証済み固定根。既存三重検証の証明自体は本項で再実行せず、証明書と監査正本のhashを固定
  - type: depends_on
    target: K1102
    note: K1097第4ラウンド再解決の独立第二検証。K1097の候補・REFUTED集合に対する別経路の出典確認
artifacts:
  - path: research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/output/residual72-unsafe-classification-add2stones-20261120.json
    role: data
    note: 4親行が属する残余72行とadd-two-stones基礎censusの固定入力
  - path: research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json
    role: data
    note: 既知WIN8候補16根・REFUTED-D10 50根の固定入力
  - path: research/experiments/n11-win8-four-row-one-certified-root-response-cover-20261120/README.md
    role: source
    note: 149根最小応答被覆の対象・入力pin・再現方法・解釈上の制限
  - path: research/experiments/n11-win8-four-row-one-certified-root-response-cover-20261120/scripts/verify_one_certified_root_response_cover_20261120.mjs
    role: verifier
    note: Node.js標準機能のみ。4×4 Bareiss、全2石追加、D4、初手義務と完全被覆を独立再導出
  - path: research/experiments/n11-win8-four-row-one-certified-root-response-cover-20261120/output/one-certified-root-response-cover-second-verification-20261120.json
    role: data
    note: 19 gates、148追加根と296義務の一回ずつの被覆、全入力hash pin
  - path: research/log/2026-11-20-n11-win8-four-row-one-certified-root-response-cover-second-verification.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-win8-four-row-one-certified-root-response-cover-second-verification-single-owner-note.md
    role: log
    note: K1097独立検証・別root証明書抽出との作業範囲分離
  - path: research/experiments/n11-win8-four-row-two-ply-response-cover-20261120/output/selected-response-cover-plan.json
    role: data
    note: 既存MILP計画。K1095を固定証明根から追加候補へ再分類する際の147根の出典
scope: >-
  K1085 residual72から選ばれた4つの6石S6親行について、全合法初手304個を
  8石safe rootによる二手応答で覆う幾何計画を独立検証する。K1096 root
  00000000000000003800000008003180だけを証明書検証済み固定根とし、K1095
  root 0000000800000000380000000810000aはWIN8-D10候補だが証明書未抽出のため
  追加候補へ移す。残る296義務に対する全9,488非固定候補の被覆数が各2で
  あること、K1095候補と既存147根の計148根が296義務を重複なく一度ずつ覆う
  ことを検査する。対象はこの4親行・この二手応答方式・既知REFUTED-D10除外後の
  safe8候補宇宙に限る。S6行のゲーム理論的値や11×11全体の勝敗は判定しない。
evidence: >-
  4親行の合法初手数は79/82/69/74、合計304。各親行の全26,220 unordered
  2点追加を4×4整数行列式のBareiss消去で検査し、safe raw extension 9,744、
  safe8 D4軌道9,490を再構築した。K1097の既知WIN8候補との交差はK1096と
  K1095の2根、既知REFUTED-D10 50根との交差は1根であり、使用可能軌道は
  9,489。K1096の既存証明書（SHA-256
  1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c・
  34,529戦略行）と既存18/18監査をhash pinし、同根の被覆8義務を再導出した。
  K1096を除く296義務について全9,488候補の被覆数は例外なく2。したがって
  追加根の下界は148。K1095候補rootと既存計画147根は296義務を重複なく
  完全被覆し、下界を達成する。総149根はこの構成の最小値。Node v20.19.2で
  19/19 gates PASS、同一作業場所の再実行と別作業場所の再実行を含む3回の
  出力JSONはbyte-identical（SHA-256
  0352b72e78d806984f1331cdc33a79f8a6f6a9dd6e822e18a216023a21479d22）。
  K1096の証明自体は再検証していない。K1095は候補、他147根はsafe8候補のみ。
  新規probe・証明書抽出・receipt foldはなく、4親行はすべてopenのまま。
---

## 結論

この4親行に対する二手応答被覆では、K1096 rootだけを証明書検証済み固定根とし、追加で148根を証明する必要がある。296個の残義務を全ての非固定候補がちょうど2個ずつ覆うため、148根が下界であり、K1095候補rootと既存147根がその下界を達成する。K1096を含む総数149根が、この構成での最小値となる。

## 証明状態の区別

- K1096 root: 既存の三重検証済み証明書。今回の検査では証明書bytesと既存監査をhash pinしただけで、戦略木の検証を再実行していない。
- K1095 root: WIN8-D10候補。証明書未抽出・未検証であり、追加根148本のうちの1本。
- 他147根: safe8候補のみ。WIN/LOSS verdictも証明書もない。

したがって、148追加根がすべて独立検証済みWIN8証明書になり、応答戦略を正しくfoldするまでは4つのS6親行を閉じられない。今回S6行は1行も閉じていない。

**標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4はUNKNOWNのまま。**
