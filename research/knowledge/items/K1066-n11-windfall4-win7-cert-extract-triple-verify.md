---
id: K1066
title: "resolve6 windfall 4 WIN7-D10 rootの証明書抽出と三重独立検証（cost65h child bit 40/43/99/118・blind抽出・fbt_drops 0・2回実行byte一致・TS Bareiss 4x4 union完全一致・python exact Bareiss 全展開・BigInt 3x3独立検証・runner v16 node-exact再現1,105,860/3,269,824/1,114,855/2,307,338）。4根はcertificate-backed receipt候補になったがfold前なので78行は1行も閉じない"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - certificate extraction (blind, empty kill table, repo-verbatim extractor exact ms23) of the four resolve6 windfall WIN7-D10 roots covering 4 of the 78 residual rows
  - triple independent verification of each certificate (TS number Bareiss 4x4 sub-root decomposition with exact union audit; pure-python exact Bareiss full replay; BigInt 3x3 cofactor independent verifier), all 50 gates fail-closed pass
  - fresh repo-verbatim runner v16 (depth 10, andclose=1, cap 1e9) re-solve node-exact with the published raw batch bit lines and the in-batch pilot_d6 control (loss=false, 3,402 nodes)
  - receipt candidates upgraded from single-order pending-win to certificate-backed pending-fold (no row closed yet; the 39-root live witness plan still independently covers all 78 residual rows)
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K0863
  note: cost-lane corpus体系（class2-lane-cost65h raw batch3/4/7/8とlane sweep正本）が出典
- type: depends_on
  target: K1063
  note: resolve6正本（SHA-256 e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a）のwin_cover_detail.evidenceがwindfall 4根の出典・被覆行の正本
artifacts:
- path: research/experiments/n11-residual78-windfall4-cert-extract-20261120/README.md
  role: data
  note: 実験README（抽出方式・検証3系統・結果表・解釈規約・次の一手）
- path: research/experiments/n11-residual78-windfall4-cert-extract-20261120/scripts/cert_driver_windfall.ts
  role: verifier
  note: blind抽出driver（kill table空・moves 48/58/52/56・fbt_drops 0で全move ok・uncapped・fatal時は出力拒否）
- path: research/experiments/n11-residual78-windfall4-cert-extract-20261120/scripts/build_verify_record_20261120.py
  role: verifier
  note: fail-closed記録組立（全50 gateをartifactsから再計算・2回実行byte一致・出力SHA-256 a3ca1b3dfd2fcdbd28fc88a6f993c4ff5ad81ee92d4a22800ff2f6477c476feb）
- path: research/experiments/n11-residual78-windfall4-cert-extract-20261120/output/windfall4-cert-triple-verification-20261120.json
  role: data
  note: 検証正本（4根×抽出/検証/runner再現の全成果物とgate。certs/*.n11のmd5/sha256記録）
- path: research/experiments/n11-residual78-windfall4-cert-extract-20261120/certs/win7-root-00000000000000803202010000001000-20261120.n11
  role: proof
  note: bit 40証明書（31,189行・SHA-256 02778cf535bb3a269496f8b1cf0064fbadeb3b302bc4476d6b2d1c391bc37a34）
- path: research/experiments/n11-residual78-windfall4-cert-extract-20261120/certs/win7-root-00000000000000803202080000001000-20261120.n11
  role: proof
  note: bit 43証明書（51,767行・SHA-256 27e60fdca5eeed3fb1c188edd35a2d6ba3212df2b16cd309f4247b902e366d7b）
- path: research/experiments/n11-residual78-windfall4-cert-extract-20261120/certs/win7-root-00000008000000803202000000001000-20261120.n11
  role: proof
  note: bit 99証明書（36,625行・SHA-256 04f545c8861015ff15ba8506322b9e78574cd523c54100d9bff424cd587f59ed。raw rootはD4非正準形でcanonical 00000000000000803800000008001200との写像をgate検証済み）
- path: research/experiments/n11-residual78-windfall4-cert-extract-20261120/certs/win7-root-00400000000000803202000000001000-20261120.n11
  role: proof
  note: bit 118証明書（55,838行・SHA-256 05356cbc162adc318b9c208e607ebff872deda1d266541b1585b83ea7a38cdf5。raw rootはD4非正準形でcanonical 00000000010000803800000008100000との写像をgate検証済み）
scope: >-
  resolve6 windfall 4 WIN7-D10 rootの証明書抽出・三重独立検証・runner v16
  node-exact再現まで。証明書はroot行=raw root（child c65h + bit 40/43/99/118）
  で出版。これらを入力とするreceipt fold・残余78行の閉鎖計上・39 live
  witness掃引・二石root・空盤の勝敗確定は対象外。
evidence: >-
  （1）出典: resolve6正本（SHA-256 e85d4bfb…）のwin_cover_detail.evidence
  から4根のcanonical root・被覆行・raw batch provenance（batch3/4/7/8の
  bit行: loss=true・uncapped・terminalStoneRange [13,17]・andclose=true、
  pilot_d6対照行 loss=false 3,402 nodes・bit 43は別プロセス再現3,269,824）
  を取得。(child, bit)=(c65h, 40/43/99/118)のraw root = c65h|1<<bit を
  再構築し、D4正準形写像がevidence rootと一致することをgate検証
  （bit 40/43はraw root自身が正準形、bit 99/118は非正準形の写像を記録）。
  （2）抽出: repo-verbatim extractor exact ms23（FBS=1<<20・MS=1<<23・
  CAP=1e9）を盲（kill table空）で全legal loser first-move
  （48/58/52/56手・独立列挙legal_candidates.pyと一致）にわたり実行。
  fbt_drops=0・全move ok・uncapped・terminal石数[13,17]。抽出ノード数は
  3,074,926/7,700,023/3,355,354/6,137,302。**2回実行で証明書byte-identical・
  ノード数完全一致**。行数は31,189/51,767/36,625/55,838。
  （3）独立検証1: verify_bit7_win7_cert.ts（number Bareiss 4x4・sub-root
  分解・全loser reply展開・terminalは全てloser-stuck）。root checkは
  7石・loser mobility 48/58/52/56（独立列挙と一致）。全sub-root PASS・
  consumed union == strategy rows 完全一致（missing 0/extra 0）。
  （4）独立検証2: verify_cost71c_win7_bareiss_independent.py（純python・
  exact整数Bareiss・rootから全subtreeを全loser reply展開で再帰検証）。
  全PASS・union完全一致・terminal {13,15,17}・visited winner states
  119,199/194,299/144,796/190,971。
  （5）独立検証3: verify_win7_certificate_bigint_independent.mjs（BigInt
  3x3 cofactor・117pool系譜と同一方式）。全PASS・rows sorted unique・
  union完全一致・terminal [13,17]・root_safe true。
  （6）runner v16再現: repo-verbatim runner（depth 10・andclose=1・
  cap 1e9）で4 bitをfresh再解。ノード数1,105,860/3,269,824/1,114,855/
  2,307,338が出版raw bit行と完全一致（loss=true・uncapped・
  terminalStoneRange [13,17]）。pilot_d6対照 loss=false 3,402 nodes合格。
  （7）記録: fail-closed builderが全50 gateをartifactsから再計算して
  windfall4-cert-triple-verification-20261120.jsonを組む。2回実行
  byte-identical（SHA-256 a3ca1b3d…）。全50 gate PASS。
  （8）解釈規約: 証明書の主張は各7石rootのgame-theoretic値のみ
  （second mover to moveでoriginal first mover必勝・全terminal loser
  stuck 13-17石）。**残余78行はどの行も閉鎖しない**。閉鎖計上は本項の
  証明書を入力として消費するreceipt fold記録が別途必要。foldまで4被覆行
  はpending-win扱い。39 live witness計画は78行を独立に完全被覆。pn/dnや
  solved数を勝敗として読まない。
  **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**
---

## 詳細

K1063（resolve6）が「windfall」として出典つきで確定した4 WIN7-D10 root
について、resolve6自身が課した条件（証明書抽出 + BigInt 3x3 / Bareiss 4x4
独立二重検証）を実行した。抽出は盲（kill table空）で行い、抽出器の自己検証
（全move ok・uncapped・fbt_drops 0）に加えて3系統の独立検証器で全て検証。
さらに抽出の再実行がbyte-identicalであること、runnner v16によるfresh再解
が出版rawバッチ行のノード数と完全一致することを確認した。

4根は「単一順verdictのpending receipt候補」から「三重検証済み証明書裏付き
のreceipt候補（fold前）」に昇格した。被覆4行の閉鎖計上にはfold機械の入力
chain再構築を含むreceipt fold記録が別途必要。詳細は
[実験](../../experiments/n11-residual78-windfall4-cert-extract-20261120/README.md)・
[研究ログ](../../log/2026-11-20-n11-residual78-windfall4-cert-extract.md)。
