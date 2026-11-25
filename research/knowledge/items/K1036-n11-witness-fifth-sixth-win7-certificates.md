---
id: K1036
title: "head-1410残余28-root witnessからの第5・第6 WIN7-D10証明書"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - n11 witness fifth/sixth WIN7-D10 certificates
  - root 00000000000000805202080001000000 WIN7-D10
  - root 00000000040000801202000080100000 WIN7-D10
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
- type: depends_on
  target: K1035
  note: 同一28-root witness内の先行WIN7-D10 receipt（root C）と2 REFUTED候補
- type: supports
  target: K0865
  note: 5親target残余に対応しうる新しいWIN7-D10 receipt候補2件（manifest foldは未実施）
artifacts:
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000000000805202080001000000-20261119.n11
  role: certificate
  note: 第5証明書。2,017,673 bytes・55,859行（header 2行+行55,857）・SHA-256 69589e76e5d2e5f22e6992929f38d9fd67f07ce1bd9fe9e3f971d32bdd635a49
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000040000801202000080100000-20261119.n11
  role: certificate
  note: 第6証明書。1,117,575 bytes・30,986行（header 2行+行30,984）・SHA-256 5289f152e88072d716f22d42414222162facb7486d07fd024b61fdc50ddef885
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/fifth-sixth-witness-win7-certificates-summary-20261119.json
  role: data
  note: 機械可読サマリ。抽出・検証統計、入力pin、gzip指紋、receipt/fold境界、UNKNOWN guard
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000000000805202080001000000-extraction-progress-20261119.jsonl
  role: data
  note: 54応手の残存可能な進捗log（nodes/terminal_range/fbt_drops毎）
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000040000801202000080100000-extraction-progress-20261119.jsonl
  role: data
  note: 55応手の進捗log
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000000000805202080001000000-independent-verification-20261119.json
  role: verifier-output
  note: BigInt 3×3余因子展開検証（54/54 subroots PASS）
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000040000801202000080100000-independent-verification-20261119.json
  role: verifier-output
  note: BigInt検証（55/55 subroots PASS）
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000000000805202080001000000-bareiss-subroots-20261119.jsonl
  role: verifier-output
  note: 4×4 Bareiss整数行列式検証のsubroot別統計（54 subroots）
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000040000801202000080100000-bareiss-subroots-20261119.jsonl
  role: verifier-output
  note: 同上（55 subroots）
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/scripts/extract_root_rec_20261119.mjs
  role: source
  note:抽出driver。生存手規約の独立recheckつき・resumable・決定的
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/scripts/verify_win_roots_rec_20261119.mjs
  role: verifier
  note: 二重独立検証driver。BigInt/Bareiss・状態流量一致・union監査の全gate
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/scripts/gen_legal.mjs
  role: source
  note: 合法応手リスト生成器（数え53/54/55 gate）
- path: research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/witness-win-roots-legal-move-lists-20261119.json
  role: data
  note: 3 rootの合法初手リスト（生存手規約・数 53/54/55）
- path: research/log/2026-11-19-n11-fifth-sixth-witness-win7-certificates.md
  role: log
  note: 抽出・二重独立検証・環境消失からの決定的再現・出版の全経緯
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor_exact_v16.ts
  role: source
  note: Git blob 5518d375fc6b4a7a14c22a1a65586f0c1c5731c0・extractBatch engine
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_win7_certificate_bigint_independent.mjs
  role: verifier
  note: Git blob 62b5d9413daafb172f6e10249976ee6808f7b454・BigInt 3×3余因子展開
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_bit7_win7_cert.ts
  role: verifier
  note: Git blob 2960afabdf7c1a7012d223974b65f1423e6890da・4×4 Bareiss
scope: >-
  標準11×11の特定7石D4正準root 00000000000000805202080001000000
  （第5）と 00000000040000801202000080100000（第6）に対する先手WIN7-D10。
  各rootの合法な後手初手全て（54/55）を含み、終局までの戦略をdepth 10以内で与える。
  二石root・空盤・クラス全体の勝敗は対象外。
evidence: >-
  K1033のREFUTED除外後の63 eligible candidate poolから選定された28-root witness
  （53行）の未試験候補のうち2 rootを、生存手規約（root stonesの任意3点と共円・
  共線になる空点は違法）で合法初手を数え54/55、昇順でextractor v16を
  blind（killTable空）完走した。第5rootは5,121,073 nodes・55,857 unique
  strategy rows・fbt_drops=0・終局石数13〜17、第6rootは931,581 nodes・
  30,984 rows・fbt_drops=0・終局石数13〜17。
  BigInt 3×3余因子展開と4×4 Bareissの独立検査は各54/54・55/55 subroots PASS、
  消費状態の和と証明書行集合の差分0（第5: consumed 82,983 records→55,857 unique、
  第6: 42,537→30,984）、状態流量一致（第5: 127,080 states・16,170 terminals・
  124,176 opponent edges、第6: 66,292・10,905・59,089）。
  再現性: epoch-1の計算成果は出版前に実行環境消失で失われたが、epoch-2は同engine
  blob（5518d375…）・同手順・昇順応手・killTable空で1から再実行し、証明書の
  SHA-256（69589e76…・5289f152…）と gzip -n -9 指紋（247,265 bytes/aeafc6a4…・
  139,336 bytes/592dd6aa…）がepoch-1の記録値と完全一致した。
  出版は .n11 テキストを正本とする（gzip binaryはpush transport
  で破損するため出版せず、指紋のみsummaryに記録）。receipt fold（manifest）は
  未実施のため、K1033のfrontier簿記（5親target累計21/112行・残91行）は不変。
  同一witnessのK1035（root C）以外の残り候補の勝敗は本項目では判定しておらず
  UNKNOWN。REFUTED-D10はdepth-10内の先手勝ちなしであり親局面のLOSS証明ではない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWN。
---
