---
id: K1070
title: "第17 WIN7-D10証明書receipt fold（fold10）: 5親target残余74→72行・frontier 6,209/491,722→6,206/491,497・閉鎖3行（target 2行+target外extra 1行・初のextra行つきreceipt）・40/112閉鎖。証明書本体のrepo出版（21dd2f0e…7c8）と4実行byte-exact合意も確定"
kind: computation
status: computed
topics: [certificates]
aliases:
  - single-owner fold10 execution (declaration note published first, K1069 separation method)
  - seventeenth WIN7 certificate body published in-repo (commit b7a6db5fb0) filling the gap where the 38-gate record pinned the certificate but the experiment dir lacked the file
  - independent byte-exact re-extraction of the seventeenth certificate: 4 runs across 2 lanes agree on sha256 21dd2f0e...
  - K1068-side fold machine has a 1-char typo in its ledger blob pin (0c03cc vs actual 0d03cc); the canonical K1067-side machine agrees with the repo file
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K1069
  note: 39 live witness掃引のWIN7-D10 root 00004000000000821082000000000100（被覆2行）が本foldのreceipt入力
- type: depends_on
  target: K1063
  note: resolve6正本（SHA-256 e85d4bfb…c281a）のwitness_full照合・base frontierチェーン入力
- type: depends_on
  target: K1066
  note: 証明書抽出・三重独立検証規約とwindfall4 fold（fs13正本24db2352…）が前段チェーン
artifacts:
- path: research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/fold_seventeenth.py
  role: verifier
  note: fold10機械（正規K1067側fold_windfall4.pyのチェーン再構築を継承・18入力SHA pin fail-closed）
- path: research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json
  role: data
  note: fold正本（SHA-256 bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a）・2回実行byte-identical
- path: research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11
  role: data
  note: 証明書本体・49,593行・1,791,541 bytes・SHA-256 21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8（commit b7a6db5fb0でrepoに供給・38gate正本のpin充足）
scope: >-
  第17WIN7-D10証明書を前提とする残余S6行の閉鎖簿記（fold10）まで。
  残余72行へのresolve7再照合、depth-saturation audit、二石root・空盤の
  勝敗確定は対象外。閉じた行のゲーム理論的値は主張しない。
evidence: >-
  （1）単一オーナー: K1069で有効だった宣言ノート先行出版方式でfold10着手
  （research/log/2026-11-20-n11-fold10-single-owner-note.md）。並走は
  seventeenth実験を出版済みで、正本がpinする証明書本体がrepoに無い
  状態だったため、本レーンの独立抽出（2回byte-identical）の本体を出版して
  pinを充足した。両レーン計4回の独立抽出がbyte-exact同一SHA
  （21dd2f0e…7c8）で決定論のレーン横断証拠が成立
  （research/log/2026-11-20-n11-seventeenth-cert-body-published.md）。
  （2）機械: 18入力SHA pin（windfall4版と同一の12 blob SHA-1 + fold7/8/resolve6
  の3 SHA-256 + fs13正本・38gate正本・証明書の3 SHA-256）全一致から、
  base 6,259/495,507 → … → ninth-twelfth 6,213/492,021 →
  thirteenth-sixteenth 6,209/491,722（残余74行）のチェーンを再構築し、
  fs13正本のreceipts 4行除去・frontier_after全数値（6,209/491,722・solved
  1,639・incidence 11,818）と完全一致で再現。seventeenth証明書は38gate
  再検証・child=root−bit8数値分解・D4正準形・7石・safe・法定手数60の独立
  再導出（fold_fourth_fifth_sixth.pyのlegal move機構）・ヘッダ・49,591行・
  SHA-256一致をgate。resolve6 witness_full当該rootのrows==被覆主張2行も照合。
  （3）被覆行は8 D4像×121石除去の正準形joinで幾何再導出し、
  5親target 2行（00000000000000821082000000000001〔cost 66〕・
  00000000000000821082000000000004〔cost 73〕）が38gate正本のcoverage
  claimと完全一致。加えてtarget外のextra 1行
  00004000000000003800000100000020（cost 86）がopen集合から発見され、
  windfall4の4receipt（各行1行のみ）と異なり本receiptは3行を閉じた
  初のextra行つきreceiptとなった。閉鎖edge cost 225・影響5parent・
  fully-closed parent 0。frontier 6,209/491,722→6,206/491,497・
  solved S6 1,639→1,642・parent incidence 11,818→11,810・
  5親target 38→40/112・残余74→72行。39-root witness計画の当該rootは
  retired（72行への再解決はresolve7が担当）。
  （4）決定論: 2回実行で正本byte-identical。
  （5）機械pin事故の記録: K1068側fold機械（fold_thirteenth_sixteenth.py）の
  ledger.json blob pinは0c03cc…と1文字タイポでrepo実在版（0d03cc…・
  ファイル編集履歴1コミットのみ）に合わず再実行不能。正規のK1067側機械
  （fold_windfall4.py・fs13正本24db2352…の生成機）のpinは実在版と一致し、
  K1067/K1068二重出版事故の実質影響は「K1068側機械の不良出版」に留まり
  証明の保全性は無事であることを本項で確定した。
  （6）解釈規約: foldは被覆の簿記であり、閉じた行のゲーム理論的値
  （LOSS等）を主張しない。REFUTED-D10はLOSS証明でない。
  **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**
---

## 詳細

seventeenth実験（並走出版・commit 0c1264b228）が38 gateで検証した第17
WIN7-D10証明書を、fold9正規機械のチェーン再構築に継いで第17 receipt
（fold10）として計上した。前段で証明書本体がrepoに存在しない
（正本はpinするがファイルが無い）状態を発見したため、本レーンの独立抽出
（windfall4スクリプト一式・extractor blob c267f260…・60手・4,250,297
nodes・49,591行・fbt_drops 0・2回byte-identical）の本体をcommit b7a6db5fb0
で出版してpinを充足、三重検証数値が38gate正本と全一致したことを確認の上、
単一オーナー宣言ノートを先行出版してfold10を実行した。

結果は**閉鎖3行**: 5親target 2行（82108…0001・82108…0004・幾何再導出で
coverage claimと完全一致）に加え、target外のextra 1行
（00004000000003800000100000020系のD4像から発見）も閉じ、receipt単位の
閉鎖行数としてwindfall4 receipts（各1行）を上回る初の例となった。
frontier 6,209/491,722→6,206/491,497・5親target 40/112・残余74→72行。
残余72行への39-root計画の再解決（resolve7）は次の一手。
詳細は[実験](../../experiments/n11-seventeenth-win7-receipt-fold-20261120/README.md)・
[研究ログ](../../log/2026-11-20-n11-seventeenth-receipt-fold.md)。
