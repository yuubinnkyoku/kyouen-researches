---
id: K1068
title: "windfall 4 WIN7-D10証明書（K1066）のreceipt fold（第13〜第16）: 基盤fold鎖の全pin再構築・三方covered行一致・frontier 6,209/491,722・5親target 38/112・残余78→74行・4回実行byte一致。11×11空盤・二石rootはUNKNOWNのまま"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - receipt fold of the four K1066 triple-verified windfall WIN7-D10 certificates (thirteenth..sixteenth receipts) into the five-parent S6 frontier chain
  - frontier 6,213/492,021 to 6,209/491,722 (solved S6 1,635 to 1,639); five-parent target 34/112 to 38/112, residual 78 to 74 rows
  - covered-row three-way agreement (D4 images vs canonical frontier vs resolve6 evidence) and full chain pin recomputation fail-closed
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K1063
  note: resolve6正本（SHA-256 e85d4bfb…）がwindfall 4根の出典・被覆行の正本
- type: depends_on
  target: K1066
  note: 三重独立検証済み証明書4枚（検証記録SHA-256 a3ca1b3d…）が本foldの入力。fold記録が存在するまで閉鎖計上しないというK1066の宣言を本項で満たす
- type: depends_on
  target: K1057
  note: 第9〜第12 fold正本・base鎖（head-1410系five-parent chain）の出典
- type: depends_on
  target: K1060
  note: 第9〜第12証明書・fold/resolve5交差監査（第12後frontier 6,213/492,021の出版確認値）
artifacts:
- path: research/experiments/n11-windfall4-receipt-fold-thirteenth-sixteenth-20261120/README.md
  role: data
  note: 実験README（方式・結果表・解釈規約・次の一手）
- path: research/experiments/n11-windfall4-receipt-fold-thirteenth-sixteenth-20261120/fold/fold_thirteenth_sixteenth.py
  role: verifier
  note: "fold機械（全入力pin検証: git blob sha1 12件・sha256 4件・証明書4枚byte照合、chain全ステップfrontier再計算、K1066の50 gate再検、covered行三方一致、fail-closed）"
- path: research/experiments/n11-windfall4-receipt-fold-thirteenth-sixteenth-20261120/fold/output/thirteenth-sixteenth-win7-receipt-fold-20261120.json
  role: data
  note: fold正本（schema n11-windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120-v1・status fold-complete・21,269 bytes・SHA-256 594137b1bd4298b97a560def4920399ac49d7c4bd3e5fbcb54d3e8aa42919873・4回実行byte-identical）
- path: research/log/2026-11-20-n11-windfall4-receipt-fold-thirteenth-sixteenth.md
  role: log
  note: 研究log（経緯・結果・解釈規約・次の一手）
scope: >-
  K1066のwindfall 4 WIN7-D10証明書を入力とするreceipt fold（第13〜第16）
  のみ。残余78行のうち4行の閉鎖簿計上とfrontier・5親target更新、39 root
  live witness計画への影響観測まで。残余74行・二石root・空盤・クラス全体の
  勝敗の確定は対象外。
evidence: >-
  fold機械はW相対入力（git blob SHA-1 pin 12件: worklist 2fee1d07・ledger
  e8785d50・globalFold 753a4bf4・previousCostFold 7e6144cc・
  firstFoldTarball fa5f26a9・census 9c251da3・audit 7cdc7c9e・
  secondThirdFold 7923a0fe・fold4 38715413・fold56 134796a7・
  ninthTwelfthFold 5b1a30f9・fold_fourth_fifth_sixth.py d8068a8e、
  SHA-256 pin 4件: seventh f1baf159・eighth afcf7d0a・resolve6 e85d4bfb・
  K1066検証正本 a3ca1b3d、証明書4枚byte SHA-256 02778cf5…/27e60fdc…/
  04f545c8…/05356cbc…）を全照合してからbase→first→second/third→
  fourth→fifth/sixth→seventh→eighth→ninth-twelfthのfold鎖を毎ステップ
  frontier再計算で再構築し、第12後のfrontier 6,213行/492,021・solved
  S6 1,635がK1057/K1060の出版値と一致することをgateで確認した。
  第13〜第16 receiptの適用では各receiptが (a) fold前状態でopenかつchain
  全体でdisjoint (b) covered行がD4像・canonical frontier・resolve6
  evidence・K1066出版記録の三方一致 (c) 証明書byte sha256一致
  (d) root幾何7石とlegal move数48/58/52/56の独立再列挙一致
  (e) K1066全50 gate再検、の全gateに合格したときのみ閉鎖を計上する。
  第13 bit40 root 00000000000000803202010000001000が行
  00000000000000801202010000001000（cost 64）を、第14 bit43
  00000000000000803202080000001000が行00000000000000801202080000001000
  （cost 79）を、第15 bit99 canonical root 00000000000000803800000008001200
  が行00000000000000003800000008001200（cost 76）を、第16 bit118
  canonical root 00000000010000803800000008100000が行
  00000000010000003800000008100000（cost 80）を各1行閉鎖（各receipt
  extra行0、closed_edge_cost計299）。結果: frontier 6,213行/492,021→
  6,209行/491,722（solved S6 1,635→1,639・s6_needed 4,513→4,509・
  cost_needed 357,882→357,583・parent_row_incidence 11,826→11,818・
  remaining_s5_orbits 173不変）、5親target 34/112→38/112行（残余78→74行、
  74行の完全リストは正本JSONのfive_parent_target_after.
  residual_row_hex_after）、parent_closure fully_closed 0・
  affected_unique_parents 5（各receipt 2親）。39 root live witness計画
  （resolve6・K1059規約）への影響は観測のみ: unaffected 35本・1行のみ
  閉鎖4本・両行閉鎖0本。決定論: stdlibのみ・約15秒・4回実行（別時点・
  別実行を含む）で出力byte-identical（出力SHA-256 594137b1…）。
  解釈規約: foldは行被覆の簿記であり、REFUTED-D10はLOSS証明ではない。
  windfall 4根のWIN7-D10主張は各7石root個別のdepth-10内先手必勝のみ。
  残余74行は未解決。**標準11×11空盤・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
---

## 詳細

K1066が「閉鎖計上は本証明書を入力として消費するreceipt fold記録が別途
必要」と宣言した条件を満たすfold正本が本研究で初めて出版された。fold機械
はK1066出版証明書をbyte照合で入手力とし、fold鎖の各ステップをpin再計算で
再構築、covered行をD4像・canonical frontier・resolve6 evidenceの3系統で
一致確認した上で4 receiptの閉鎖を計上した。windfallで4 witnessの被覆行が
1行に減るため、次の一手は残余74行のpost-fold再解決（resolve7: 最大
matching・singleton候補・witness計画再架構）である。詳細は
[実験](../../experiments/n11-windfall4-receipt-fold-thirteenth-sixteenth-20261120/README.md)・
[研究ログ](../../log/2026-11-20-n11-windfall4-receipt-fold-thirteenth-sixteenth.md)。
