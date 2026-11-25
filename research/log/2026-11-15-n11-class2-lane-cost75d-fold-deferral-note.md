# 2026-11-15：cost-75d receipts foldの延期 — 実行環境outage（fold入力は全件main検証済み・v15 pinned record出版）

cost-75d（第二coverable class-2 target S5 00000000000000801202000000200000 のcost-75 child 00000000000040801202000000200000・WIN7-D10 bits [12,40,92,111]・証明書4件239,868行8,654,219 bytes・第二検証3幾何系PASS済み）のreceipts foldは、本セッションでは**実行環境outageのため未実施**（head 1280のまま）。並走cost-76b fold（head 1277→1280）は既に着地しており、foldは新canonical head 1280/6567/518678/4837/382401（76b head JSON blob 0c357597…・6,899 B）へのrebase必須。

## 本セッションに確定した事実

- **fold入力の全件main検証（remote）**: 4証明書（bit12 1,126,030 B・bit40 1,885,065 B・bit92 2 parts 1,362,476/1,357,271 B・bit111 3 parts 975,616/974,906/972,855 B）、consumed dumps、bit{N}.bigint.json（union 0/0・terminal [13,17]）、bit{N}.tsverify.json、bit{N}.cert-receipt.json、split manifests（74g形式・join==whole）、raw batches 1-10（pilot 3402×10・候補75 exactly-once・総nodes 143,552,593）、v16 determinism rerun（batch5 node-exact）、legal-moves.json。独立監査 class2-lane-cost75d-raw-sweep-independent-audit-20261115.json と第二検証（3幾何系）も参照。
- **covers事前検証（独立TS計算・76b root72のpublished marginals 6/6一致で模型検証済み）**: 4 rootのcoversは各7軌道・pairwise重複はchild orbit 00000000000040801202000000200000 のみ（全4組で共通・公開順最初のbit12で閉鎖予定）・和集合25軌道・76b marginal 11 hexとの交差0。fold時のraw marginalは 25 − |union ∩ s_1280|、in-manifest marginalはそのうちmanifest被覆分（child含む・値はcanonical fold scriptで確定）。
- **v15 cross-engine check pinned recordの出版**（commit 2e733c3c）: 12 records（pilot 5949×3・WIN nodes 1,406,438/7,087,163/16,644,786/10,234,430・REFUTEDアンカー bits 0/2/4/6/86 nodes 407,624/3,150,598/1,532,737/604,694/11,782,891）。元ローカルJSONLが未pushだったため、喪失リスクに対する保険として公開。ローカル原本が残っていればfold scriptは原本を優先し本recordと照合。

## 次回の実行手順（確定事項のみ）

1. 最新main再取得・76b head 1280（blob 0c357597…）がcanonicalであることをassert（並走77a fold着地済みならそのheadへrebase）。
2. fold script recompute_frontier_cost75d_receipts_20261115.py（76b script recompute_frontier_cost76b_receipts_20261115.py の構成踏襲）: (1) 76b scriptをrunpyで再実行しhead 1280 + 3出力blob（head JSON 0c357597… 6,899 B・ranking CSV 25e4cd03… 7,539 B・top-candidates CSV 5f16284c… 7,847 B）をbyte-identical assert（merged 1277はrunpy鎖で再帰的に再現） (2) claim内容検証 + childが1280で genuinely remaining（parent1 16行/1249・lift 78・他5削除軌道閉行・demand c1=0,c2=1,c4=0） (3) raw batchesからsweep再導出（WIN [12,40,92,111]・71 REFUTED・0 capped・143,552,593 nodes・roots == child|1<<bit・pilot 3402×10・det rerun batch5 node-exact・v15アンカー） (4) 証明書bytes検証（part glob join==whole・split manifests・bigint/tsverify/consumed・sub-roots 55/60/66/61・rows 31,181/52,198/75,290/81,199） (5) 4 root vs 550 folded roots（548+76b 2）のraw+D4 disjointness (6) 公開順 [12,40,92,111] fold・childはbit12で閉鎖・set等式 s_after == s_1280 ∪ covers(4 roots)・parent1は16/1249→15/1174・全開親の喪失行⊆covers(4 roots) (7) 出力3件 + claim v2 retire（76b claimのfold record形式）。
3. 3回連続実行byte-identical確認後にpush、log・K0783追記・workflowトリガー行・Knowledge更新。

## 境界

foldは公開receiptの帳簿更新であり勝敗判定ではない。solved 1280はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。
