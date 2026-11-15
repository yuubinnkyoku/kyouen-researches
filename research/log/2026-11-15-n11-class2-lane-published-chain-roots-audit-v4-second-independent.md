# 2026-11-15：published fold-chain全root監査のv4拡張（第二独立実装） — 77d/merged/79a/80d endpoint・canonical line 1305までexactly-once・bit-78重複rootの簿記統制

開始時状況: canonical head **1305/6542/516793/4812/380516**（cost-80d receipts fold・head JSON blob `289c9337`）。同一日の第二独立検証（4 fold全統制PASS・12成果物byte-identical・[検証log](./2026-11-15-n11-class2-lane-cost77d-merged75d77d-79a-folds-second-verification.md)）に続き、published-fold-chain全root監査の第二独立実装（v2・endpoint 75d・91 pins・569 roots）を**v4に拡張**した。

## 成果1：監査corpusを80d endpointまで機械拡張 — 全統制PASS

`audit_published_chain_roots_second_independent_20261115.py`（v2・published-files-only・runpy鎖もsolved-set再構築も使わない方針）をベースに `audit_published_chain_roots_second_independent_v4_20261115.py` を作成し、以下を拡張:

- **git blob pins 91→95**: cost-77d（`d19c96b7`）・merged 75d+77d（`97130384`）・cost-79a（`7dea99ff`）・cost-80d（`289c9337`）の4 head JSONをpin追加（71c/70f/73g/70gの4 unpinnedは従来どおりcomputed sha記録）
- **root inventory 569→587**: 4 headのaddition recordsをcorpusに追加し、累積inventoryと各foldのown-branch累積を再照合 — 77d lane-local **577**（565+12・12 rootsすべて77c branchで新規）・merged **580**（569+11）・79a **583**・80d **587**、document-order累積はbit-78重複（75d bit-92とraw同一）を除き**580→587**、全own-branch claimと一致
- **D4 orbit構造**: 587 roots / **576 distinct orbits / 11 twin pairs**（twin pair数不変 — 新18 rootsはすべて新orbitでpairを作らない）
- **per-record geometry**: receipt records 464件・group records 40件・**anomalies 0**（77d 12+merged 11+79a 3+80d 4の全新recordがpopcount7・covers7・marginal⊂covers・mim一致・d4_canonical_hex一致）
- **head arithmetic 73 heads・anomalies 0**: 4新headはいずれもsequential-fold-union（77d: delta 9 = mim総和9 = union9 / merged: 6/6/6 / 79a: 2/2/2 / 80d: 1/1/1）、baseline quoteはすべてmatched（77d→77c 1290・merged→75d 1296・79a→merged 1302・80d→79a 1304）、quote erratumは既知の70f 1件のみ
- **child-closure bookkeeping 28 heads**: 77d（bit7）・79a（bit9）・80d（bit48）の閉鎖記録とtotals宣言の整合、mergedはchild closure不主張（warm-hygiene・closes 0件）と整合
- **convention-external receipts 1件**: v2と同一の既知entry（75c cost72_fold・orbit-twin True）

出力: [v4 audit JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-second-independent-audit-v4-20261115.json)（**AUDIT PASSED**・2回実行byte-identical・md5 `364b95e1…`）。v2 JSONは不変のまま残存。

## 成果2：canonical line 1233→1305のhex-level exactly-once — 72行すべて単一claim

CANONICAL_LINEをmerged 75d+77d（key `cost77d_addition`・11 receipts・**75d receiptsの再掲なし**）・79a・80dの3エントリに延長し、**1233 baselineから1305 endpointまでのmanifest hex 72行すべてがcanonical line上でちょうど1回だけmarginalとしてclaimされる**ことを確認（mim総和72 = distinct 72 = 1305-1233・multi_claims 0）。lane-local 77d head（1299）はcanonical line外（marginalはmerged foldが1296 baselineにrebase）。

## 成果3：bit-78重複rootのexactly-once簿記統制（新設）

v2にはなかった明示的統制を追加:

- **root同一性**: 77d bit-78 root == 75d bit-92 receipt root（raw-hex完全一致）
- **covers**: 同一rootのdeletion orbitは**77d child `00000000100000801202000000200000` と75d child `00000000000040801202000000200000` の両軌道をカバー**
- **逐次marginal規約の解明（実験的事実）**: 同一root・同一1290 baselineでも、両headのmarginal recordは1行ずつ異なる。理由は**marginalがpublication orderの逐次差分**だから — 77dはbit-7が先に77d childを閉じ（当該行がbit-78のmarginalから消える）、75dはbit-12が先に75d childを閉じる。差分行を除くmarginal（`00000000000000003800400008004000`）は両recordで一致
- **canonical line上のclaim源**: 77d bit-78 recordの2つのmanifest marginalsはcanonical line上でどちらも75d headから**ちょうど1回ずつ**claimされる（共有hexは75d bit-92、75d-child hexは75d bit-12）
- **inventory**: bit-78 rootは75d経由でちょうど1回inventoryに入り、77dの再掲は新規inventory rootを1つも追加しない（77dのnew rootsは11）

## 成果4：80d endpoint・79a/80d claim crosscheck

- endpoint_80d: head 1305/6542/516793/4812/380516・receipts 4・child closed by bit-48
- 80d completed claim（`class2-lane-cost80d-inflight-20261115.json`）: chain_head_before 1304/…→after 1305/…・publication order [48,61,81,96]・head JSON blob `289c9337` + 8033 bytes byte-exact
- 79a completed claim: 1302→1304・[9,50,64]・child closed by bit-9・head JSON blob pin一致

## 解釈境界（重要）

- solved 1305はmanifest被覆の簿記であり、いずの局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1305**。80d以降のsweep/fold（並走laneがcost-82cをIN FLIGHTで実行中）にも同じ監査パターンを適用可能（pins追加・own_claim/own_baseline・CANONICAL_LINE・endpoint差し替えのみで機械拡張できる）。
- v1系script（`audit_published_chain_roots_independent_20261115.py`・v3拡張済）の80d endpointへの追従拡張は次回以降の課題。

詳細: [v4 audit script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_chain_roots_second_independent_v4_20261115.py)、[v4 audit JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-second-independent-audit-v4-20261115.json)、[v2監査（前回）](./2026-11-15-n11-published-fold-chain-audit-second-independent-verification.md)、[4 fold第二独立検証（同日）](./2026-11-15-n11-class2-lane-cost77d-merged75d77d-79a-folds-second-verification.md)。
