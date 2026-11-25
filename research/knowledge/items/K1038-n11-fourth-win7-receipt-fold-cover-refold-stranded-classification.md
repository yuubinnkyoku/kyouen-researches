---
id: K1038
title: "第4 WIN7-D10証明書のreceipt fold・5親target 23/112更新とstranded 40行の構造分類"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - n11 fourth WIN7 receipt fold into the base fold chain
  - five-parent target 23/112 after the fourth receipt
  - stranded 40-row structural vs plan-dependent classification
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K0007
  note: ranked AND/OR certificateの構造と検証境界
- type: depends_on
  target: K0865
  note: head-1410の5親targetとS6 receipt簿記
- type: depends_on
  target: K1033
  note: base→first→second/third fold連鎖・117root候補プール・旧38 stranded
- type: depends_on
  target: K1035
  note: 第4 WIN7-D10証明書と28-root witnessのcompanion REFUTED 2
- type: supports
  target: K0865
  note: 5親target 21/112→23/112行の被覆簿記更新（行のLOSS証明ではない）
artifacts:
- path: research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/scripts/fold_fourth_win7_receipt_20261119.mjs
  role: source
  note: fold機械。全ピン入力をGit blob SHA-1で照合し、ライブ証明書再検証とWIN/LOSS衝突scanの後でのみreceiptを書く
- path: research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/scripts/refold_cover_after_fourth_receipt_20261119.mjs
  role: source
  note: REFUTED除外後の5親target再々解決機。stranded構造分類（structural / plan-dependent / alternate-matching被覆可能性）を含む
- path: research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/output/fourth-win7-root-receipt-fold-20261119.json
  role: data
  note: fold実行の機械可読結果。frontier 6,229→6,226行・493,184→492,970・solved 1,622・parent incidence 11,855
- path: research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/output/fourth-win7-independent-verification-rerun-20261119.json
  role: data
  note: 本環境でのBigInt・Bareiss両検証器によるライブ再検証。K1035出版値と完全一致
- path: research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/output/refuted-excluded-cover-refold-after-fourth-receipt-20261119.json
  role: data
  note: 残余89行の再解決とstranded 40行の構造分類（36 structural・4 plan-dependent）
- path: research/log/2026-11-19-n11-fourth-win7-receipt-fold-cover-refold-stranded-classification.md
  role: log
  note: fold・再解決・分類の全経過とK1033解釈のerratum
scope: >-
  標準11×11 head-1410の5親target 112行のうち第4 WIN7-D10 receipt
  （root 00000000000000801202060001000000）による2行閉鎖の簿記反映と、
  K1035 verdict（WIN 1・companion REFUTED-D10 2）を含むREFUTED除外後の
  残余89行の候補被覆再解決・stranded 40行の構造分類。
  二石root・空盤・クラス全体の勝敗は対象外。
evidence: >-
  開始時main cc8be6d6。全入力（worklist・ledger・census・base/global/cost
  fold群・first fold tarball・49-cover・head1476 verdict join・
  cost78c/79c/73j・48-root sweep・second/third fold・28-root cover resolve・
  witness probes・証明書gzip・runner/extractor/両検証器）をraw CDNから
  commit pinで取得しGit blob SHA-1をNode cryptoで照合、全一致。
  まず証明書を本環境で独立再検証（gzip SHA-256 f9bf9b24…9f91・展開後
  1,843,284 bytes・SHA-256 f3fcf274…94bae。BigInt 3×3余因子と4×4 Bareissの
  両方式で53/53 subroots PASS・消費集合union差分0・状態流量101,663 states・
  16,052 terminals・91,807 loser edges・終局石数13〜17。K1035の出版値と
  完全一致）。fold機械はbase→first→second/thirdの既存fold連鎖を全ピン再
  計算で再構成し、出版verdict全域（282 REFUTED/159 WIN、K1035分を除く）
  をjoinしてWIN/LOSS衝突0を確認した上で第4receiptをfoldした。結果:
  S6行3行閉鎖（5親target 2行 00000000000000801202020001000000・
  00000000000000801202040001000000＋非target 1行
  00000000000000801202060000000000）、closed edge cost 214、frontier
  6,229→6,226行・493,184→492,970、solved S6 1,619→1,622、parent行
  incidence 11,859→11,855（parent 00000000000000003800000009000000が25→23・
  00000000000000801202020000000000が44→42）。fold・refold各3回実行
  （別cwd含む）で出力byte-identical。K1035のWIN 1とcompanion REFUTED 2
  を加えた再々解決: 117root poolはREFUTED 53・WIN receipt 4を除き
  eligible 60候補、残余89行のうちpair edge 41・singleton行12・最大
  マッチング23＋singleton 3でwitness 26 root（lower bound 45）、未試験
  witness 26 root。旧38 stranded全行はstranded維持、K1035 companion
  REFUTEDにより新規2行がstranded（いずれも旧providerの1つが同REFUTED
  rootで、うち1行は代替eligible providerをもつが本計画では外れる
  plan-dependent）となり、stranded計40行。各行を構造分類した結果、
  36行はstructural（残余
  eligible候補に被覆providerなし。候補拡張またはdepth>10探索が必要。
  数学的閉鎖不能証明ではない）、4行
  （00000000000000043800000008080000・00000000000000801202000001000200・
  00000000000020003800000048000000・00000000000040809002000000100000）は
  plan-dependent: eligible pair候補が存在して被覆するが、本最大マッチング
  計画では外れ、頂点除去再計算（subgraph最大マッチング+1=全体最大）に
  よる代替最大マッチング被覆可能性判定でも被覆不可（inessential vertex）
  である。ただし候補自体がWIN7-D10になれば閉じ得る。この分類により
  K1033項の「38行stranded＝当該プール内のいかなるdepth-10候補でも
  閉じ不可」の解釈は過大だったことが確定した。strandedは「本最大
  マッチング計画で被覆されなかった」ことのみを意味し、数学的閉鎖不能
  証明ではない。同日並走のK1036（commits 52f5914482・f1a8dedbd0・
  970d714f93、本項HEAD cc8be6d6の後続出版・items/K1036-n11-witness-fifth-sixth-win7-certificates.md）は、本refoldの
  witness 26 rootに含まれる第5root 00000000000000805202080001000000
  （55,857行）と第6root 00000000040000801202000080100000（30,984行）の
  WIN7-D10証明書を抽出・双検証した（本項出版時点で両receiptのfoldは
  未実施）。本項のverdict join・frontierはcc8be6d6のピンに固定であり、
  これらのverdict・receiptは含まない。幾何forecast（本項refold残余89行
  に対する純D4計算、証明ではない）: 第5rootは 00000000000000805202000001000000 を、第6rootは
  00000000020000809002000040000000 を各1行覆い、両行とも本計画で
  witnessを割り当て済みの非stranded行である。両receipt fold後は本項の
  簿記23/112から25/112（残余87行）へ進む見込み。REFUTED-D10はその7石rootから深さ10以内の先手勝ちが
  存在しないという判定であり、親局面のLOSS証明ではない。標準11×11
  空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWN。
---
