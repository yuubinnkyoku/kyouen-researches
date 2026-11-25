# 2026-11-15：published fold-chain全root監査のv9拡張（第一実装） — 84a/62a endpoint・canonical line 1326までexactly-once・616 roots

開始時状況: canonical head **1326/6522/515251/4792/378974**（cost-62a receipts fold・head JSON blob `3989e9dd`・9434 bytes）。[監査v8+agreement v5再現検証](./2026-11-15-n11-published-audit-v8-agreement-v5-reproduction.md)と[84a+62a fold第二独立検証](./2026-11-15-n11-class2-lane-cost84a-62a-fold-second-verification.md)（いずれもcommit `6d52031a`/`b4cf26cc` 着地済み）の後、fold chain末端の検証体制が揃ったため、published-fold-chain全root監査の第一実装（v8・endpoint 83d・104 pins・606 roots）を**v9に拡張**した。作業開始時点で並走のIN FLIGHTはcost-58c（第二候補S5 cost-58行・着手禁止）。

## 成果1：監査corpusを84a/62a endpointまで機械拡張 — 全統制PASS

`audit_published_chain_roots_independent_20261115.py`（published-files-only・runpy鎖もsolved-set再構築も使わない方針）をv8からv9へin-place拡張（30 anchored edits・各anchorの出現回数assert付き）し、以下を追加:

- **git blob pins 104→106**: cost-84a head JSON（`f5624e99f8603ea612a862ed63539011989b5506`・7935 bytes）とcost-62a head JSON（`3989e9ddfa43d0951a9a58c10919ce5087eb8733`・9434 bytes）をPOST70E_PINSに追加（26 base + 52 chain + 28 post-70e）
- **root inventory 606→616**: 84a headの `cost84a_addition` 4 records（bits 1/62/70/90）と62a headの `cost62a_addition` 6 records（bits 7/15/35/76/81/98）をcorpusに追加し、累積inventoryとown-branch累積（606+4=610@84a・610+6=616@62a）を再照合 — **616 roots / 605 distinct D4 orbits / 11 twin pairs**（10新rootsはすべて新orbitでpairを作らない・`matches_published: true`・new_orbits_added 4+6）
- **per-record geometry**: receipt records **493件**・group records 40件・**anomalies 0**（84a/62aの10新recordがpopcount7・covers7・marginal⊂covers・mim一致・d4_canonical_hex一致）・published hex errataは既知のcost63cd 1件のみ
- **head arithmetic 80 heads・anomalies 0**: 84a head・62a headとも**sequential-fold-union**（84a: delta 4 = sum_mim 4 = union_mim 4・62a: delta 8 = sum_mim 8 = union_mim 8）。baseline quoteは84aが83d frontier（1314/6533/516061/4803/379784）に・62aが84a frontier（1318/6530/515822/4800/379545）に**matched_published_state**・prose pointerも一致、quote erratumは既知の70f 1件のみ
- **child-closure bookkeeping 35 heads**: 84a headのchild閉鎖宣言（child `00000000000040809002000000000800`・closing bit-1・declared_by_totals 1）と62a headのchild閉鎖宣言（child `00000000040000003800000008100000`・closing bit-7・declared_by_totals 7）の整合
- **canonical line 1233→1326のhex-level exactly-once**: CANONICAL_LINEにcost84a_addition・cost62a_additionを追加し、**93 hexすべてがちょうど1回だけmarginalとしてclaimされる**ことを確認（mim総和93 = distinct 93 = 1326-1233・multi_claims 0）

## 成果2：84a/62a endpoint・claim crosscheck

- **endpoint_cost84a**: head 1318/6530/515822/4800/379545・receipts 4・child closed by bit-1・publication order [1,62,70,90]・blob `f5624e99`。completed claim fold record（`class2-lane-cost84a-inflight-20261115.json` blob `69cc4379`）: head transition 1314→1318・receipts 4・total_marginal 20・in-manifest 4・zero-mim [70]・head JSON blob + 7935 bytes byte-exact
- **endpoint_cost62a**: head 1326/6522/515251/4792/378974・receipts 6・child closed by bit-7・publication order [7,15,35,76,81,98]・blob `3989e9dd`。completed claim fold record（`class2-lane-cost62a-inflight-20261116.json` blob `8fb55e35`）: head transition 1318→1326・receipts 6・total_marginal 32・in-manifest 8・zero-mim [35]・head JSON blob + 9434 bytes byte-exact
- 実装上の追加: 62aのclaim fileはlanding laneの20261116 date suffix規約のため、ENDPOINT_CHECKSループに `CLAIM_NAME_OVERRIDES`（62a→`class2-lane-cost62a-inflight-20261116.json`）を導入。claim crosscheckは15件（13+2）

出力: [v9 audit JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-independent-audit-v9-20261115.json)（**AUDIT PASSED**・2回実行byte-identical・md5 `a2ba852197bde40c7499898a9426418d`・git blob `c199accf`・110,137 bytes）。v8 JSONは不変のまま残存。実行はfresh codeload mirror（HEAD `315005c3`・全成果物extract後・84a/62a head/claimはfetch時git blob sha照合済み）上で実施。

## 解釈境界（重要）

- solved 1326はmanifest被覆の簿記であり、いずれの局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 第二実装audit v9（新規file）とdual implementation agreement v6（84a/62a pair・AUDIT_PINS 12→14）は同一実行で実施（それぞれ別log参照）。
- 並走のcost-58c sweep着地後は、v10拡張（endpoint 58c）と58c fold第二独立検証が次回の定型。第二target S5 `00000000000000801202000000200000` は3行/209で全残行REFUTED-D10のためdepth-10 receiptでは閉鎖不能。

詳細: [v9 audit script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_chain_roots_independent_20261115.py)（in-place・72,898 bytes・blob `76c65fa3`）、[v8監査（前回）](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v8-first-implementation.md)、[84a+62a fold第二独立検証（同日）](./2026-11-15-n11-class2-lane-cost84a-62a-fold-second-verification.md)。
