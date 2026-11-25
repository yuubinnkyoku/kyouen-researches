---
id: K1029
title: "head-1410 49-root残余候補の最小分岐7石rootに対するWIN7-D10証明書とreceipt fold"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases: [n11 first residual root WIN7-D10 certificate, 49-root first WIN7 receipt, root 00000000000000821082000010800000 WIN7-D10]
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K0007
  note: ranked AND/OR certificate の構造と検証境界
- type: depends_on
  target: K0863
  note: 49候補rootの公開verdict index非所属判定に使う完全child universe
- type: depends_on
  target: K0783
  note: WIN7 receipt と S6 manifest の簿記規約
- type: supports
  target: K0865
  note: 49-root残余coverの候補1本を証明し、5親targetの2行をreceiptで閉鎖
artifacts:
- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/win7-root-00000000000000821082000010800000-20261119.n11.gz
  role: certificate
  note: 展開後966,579 bytes。SHA-256 5a32d95d0e1bddfeed9e810db4d372d5a9440cde594b12b3d94ae2dd06c02ab8
- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/first-win7-root-evidence-20261119.tar.gz
  role: data
  note: 抽出・検査・receipt fold driver、JSONL、結果JSON、再実行手順を格納
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts
  role: solver
  note: depth-10 runner（Git blob pinは証拠束のreceipt-fold JSONに記録）
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor_exact_v16.ts
  role: source
  note: 戦略証明書extractor（Git blob pinは証拠束のreceipt-fold JSONに記録）
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_win7_certificate_bigint_independent.mjs
  role: verifier
  note: BigInt 3×3余因子展開による独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_bit7_win7_cert.ts
  role: verifier
  note: 4×4 Bareiss行列式による別実装の検査
- path: research/log/2026-11-19-n11-first-residual-root-win7-certificate.md
  role: log
  note: 抽出・独立検査・receipt fold・未解決範囲の記録

scope: >-
  標準11×11の特定7石D4正準root
  00000000000000821082000010800000 に対する先手WIN7-D10。
  47個の合法な後手初手すべてを含み、終局までの戦略をdepth 10以内で与える。
  二石rootや空盤の勝敗は対象外。
evidence: >-
  runner v17のdepth-10 probeはandclose=1/0の両方で後手側loss=true、
  未打切り（392,235/446,745 nodes）。v16 extractorは47応手を完了し、
  616,064 nodes・26,708 unique strategy rows・fbt_drops=0。
  BigInt 3×3余因子展開と4×4 Bareissの独立検査は各47/47、
  消費集合と証明書行の差分は双方0。receiptはS6行4件（target内2件）を閉じ、
  5親targetは97→95行、最小root coverは49→48本（47 pair+1 singleton）。
  5親の完全閉鎖は0。
---

## 命題・範囲

7石root 00000000000000821082000010800000 は、標準11×11の通常ルールで
先手勝ちである。WIN7-D10証明書は47個の合法な後手初手を全て覆い、
各枝の終局をdepth 10以内に保証する。証明書の26,708行は、二方式の独立検査で
到達・消費される戦略行集合と完全一致する。

このrootは49本のhead-1410残余候補のうち、合法次手数47で最小の候補だった。
開始時の公開verdict indexには対応するchild orbitがなく、未判定だった。

## 現在の根拠と限界

探索はrunner v17（depth 10、cap 950,000）で行い、andclose=1/0の両probeが
後手側loss=trueで未打切り。pilot_d6 controlは双方3,402 nodesで一致した。
v16 extractorは47応手を全て処理し、総616,064 nodes、26,708 unique strategy rows、
fbt_drops=0、終局石数13〜17の証明書を出力した。

BigInt 3×3余因子展開検査ではroot安全性・合法次手47・47 subrootsを確認し、
証明書行26,708と消費行集合が完全一致（missing=0, extra=0）。
4×4 Bareiss検査も47 subroots PASS、60,884 visited states、9,942 terminals、
54,552 opponent reply edges、39,307 consumed records / 26,708 unique、
union差分0。証明書SHA-256は
5a32d95d0e1bddfeed9e810db4d372d5a9440cde594b12b3d94ae2dd06c02ab8。

receipt foldは4つのS6行（edge cost 262）を閉じ、そのうち2行が5親target内。
5親すべてで2行ずつ減ったが、完全閉鎖された親は0。
manifest bookkeepingは solved_s6 1608→1612、unique remaining S6 6240→6236、
remaining S5 orbit 173のまま、remaining cost 493965→493703。
open class demandは4,524行・cost 358,685で不変。

5親targetは97→95行、候補coverは49→48 root（47 pair + 1 singleton）。
下界48とwitness 48が一致するため、この残余coverは最小。
ただし、これは候補root coverの最小性であって、残りrootの勝敗証明ではない。
manifestのsolved_s6数はreceipt bookkeepingであり、ゲーム状態の勝敗確定数ではない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWN。
5親の完全閉鎖も0。REFUTED-D10はLOSSではない。
