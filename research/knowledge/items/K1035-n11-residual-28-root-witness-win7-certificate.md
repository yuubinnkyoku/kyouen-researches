---
id: K1035
title: "head-1410残余28-root witnessからの第4 WIN7-D10証明書"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - n11 residual 28-root witness WIN7-D10 certificate
  - root 00000000000000801202060001000000 WIN7-D10
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
  note: REFUTED除外後の63候補・28-root witnessと残余行
- type: supports
  target: K0865
  note: 5親target残余のうち2行に対応する新しいWIN7-D10 receipt候補（manifest foldは未実施）
artifacts:
- path: research/experiments/n11-head1410-residual-28-root-witness-win7-20261119/output/win7-root-00000000000000801202060001000000-20261119.n11.gz
  role: certificate
  note: gzip証明書。展開後1,843,284 bytes、SHA-256 f3fcf274ee72d98f4501d104f694d679cd3301e0e161a06a22c191c89ad94bae
- path: research/experiments/n11-head1410-residual-28-root-witness-win7-20261119/output/witness-root-probes-and-certificate-20261119.json
  role: data
  note: probe、抽出、BigInt/Bareiss独立検査、入力pinを含む機械可読結果
- path: research/log/2026-11-19-n11-residual-28-root-witness-win7-certificate.md
  role: log
  note: 28-root witnessの3候補probe、証明書抽出、独立検査と未fold境界
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/five-parent-refuted-excluded-cover-resolve-20261119.json
  role: data
  note: 63 eligible candidatesから選ばれた28-root・53行の候補witness
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts
  role: solver
  note: Git blob c132cc6425eee3feaeef1d697dd74f968cfedb59・depth-10 probe
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor_exact_v16.ts
  role: source
  note: Git blob 5518d375fc6b4a7a14c22a1a65586f0c1c5731c0・WIN7 strategy extraction
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_win7_certificate_bigint_independent.mjs
  role: verifier
  note: Git blob 62b5d9413daafb172f6e10249976ee6808f7b454・BigInt 3×3余因子展開
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_bit7_win7_cert.ts
  role: verifier
  note: Git blob 2960afabdf7c1a7012d223974b65f1423e6890da・4×4 Bareiss
scope: >-
  標準11×11の特定7石D4正準root
  00000000000000801202060001000000 に対する先手WIN7-D10。
  53個の合法な後手初手を全て含み、終局までの戦略をdepth 10以内で与える。
  二石root・空盤・クラス全体の勝敗は対象外。
evidence: >-
  K1033のREFUTED除外後に残る63 eligible candidatesの28-root witnessから選定。
  rootは7石・D4正準・unsafe quadruples 0・合法次手53。
  runner v17のandclose=1/0両順序でloss=true、未打切り
  （3,294,339/3,953,563 nodes）。extractor v16は53応手を完了し、
  5,469,581 nodes・50,941 unique strategy rows・fbt_drops=0。
  BigInt 3×3余因子展開と4×4 Bareissの独立検査は各53/53 subroots PASS、
  消費集合と証明書行の差分0、状態流量（101,663 states・16,052 terminals・
  91,807 opponent edges）も一致、終局石数13〜17。
  証明書のD4 row joinは5親target残余2行
  00000000000000801202020001000000 と
  00000000000000801202040001000000 に対応するが、本項目の出版時点で
  receipt foldは未実施。K1033のfrontier簿記を減らさない。
  同じ28-root witnessの別2候補はREFUTED-D10（depth-10内の先手勝ちなし）だが、
  それらの親局面のLOSS証明ではない。標準11×11空盤・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWN。
---
