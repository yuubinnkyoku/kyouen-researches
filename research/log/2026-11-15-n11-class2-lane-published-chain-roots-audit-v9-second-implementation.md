# 2026-11-15：published fold-chain全root監査のv9拡張（第二実装・新規file） — 84a/62a endpoint・102 pins・616 roots

第一実装のv9拡張（[第一実装log](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v9-first-implementation.md)）に続き、第二独立実装をv8（1,553行・100 pins・606 roots）から**v9に拡張**した。v6→v7→v8と同じく拡張は新規file `audit_published_chain_roots_second_independent_v9_20261115.py`（1,668行）として作成し、v8 fileは不変のまま残存。第一実装のv9出力は見ずに、v8第二実装の構造とpublished 84a/62a成果物（head JSON blob `f5624e99`/`3989e9dd`・claim blob `69cc4379`/`8fb55e35`）のみから拡張した（29 anchored edits・各anchorの出現回数assert付き）。

## 成果1：第二実装corpusを84a/62a endpointまで機械拡張 — 全統制PASS

- **git blob pins 100→102**: cost-84a head（`f5624e99…`）とcost-62a head（`3989e9dd…`）をPOST70E_PINSに追加（26 base + 52 chain + 24 pinned post-70e・71c/70f/73g/70gの4 unpinnedは従来どおりcomputed sha記録）
- **root inventory 606→616**: own_claim 606+4=610@84a・610+6=616@62a・own_baseline 84a→83d・62a→84aを追加し、累積inventoryとown-branch累積を再照合 — **616 roots / 605 distinct D4 orbits / 11 twin pairs**（84a/62aの4+6新rootsはfold script内でD4-disjointnessがassert済みのためtwin-pair countは11不変）
- **per-record geometry**: receipt records 493件・group records 40件・anomalies 0・published hex errataはcost63cd 1件のみ
- **head arithmetic 80 heads・anomalies 0**・quote erratum 70f 1件・pointer-differs 74g 1件
- **child-closure 35 heads**・**canonical line 1233→1326 exactly-once**（mim 93 = distinct 93 = 1326-1233・multi 0）

## 成果2：section 8i/8j — 84a/62a endpoint + claim crosscheck

- **8i endpoint_84a**: head 1318/6530/515822/4800/379545・receipts 4・child closed by bit-1。claim（`class2-lane-cost84a-inflight-20261115.json`）fold record: status completed・head transition 1314→1318・receipts_folded 4・publication_order [1,62,70,90]・child_orbit_closed_by_bit 1・total_marginal 20・in-manifest 4・zero-mim [70]・head JSON blob + 7935 bytes byte-exact
- **8j endpoint_62a**: head 1326/6522/515251/4792/378974・receipts 6・child closed by bit-7。claim（`class2-lane-cost62a-inflight-20261116.json`）fold record: status completed・head transition 1318→1326・receipts_folded 6・publication_order [7,15,35,76,81,98]・child_orbit_closed_by_bit 7・total_marginal 32・in-manifest 8・zero-mim [35]・head JSON blob + 9434 bytes byte-exact

出力: [v9 second-implementation audit JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-second-independent-audit-v9-20261115.json)（**AUDIT PASSED**・2回実行byte-identical・md5 `8558a07cd7ac475a6859c4b09fbd09e1`・git blob `c9c1eb07`・109,775 bytes）。v8 JSONは不変のまま残存。

## 第一実装v9との全共通統制一致（事前確認）

本拡張の実行前に、第一実装v8との全共通control一致がv8時点で確立済みであることに加え、v9出力同士の全substantive control（cumulative 28 heads逐行・616/605/11・receipt 493/group 40・arith 80 heads/classification counts・canonical 1233..1326・child-closure 35・bit-78 bookkeeping）が一致することを、[agreement v6](./2026-11-15-n11-published-fold-chain-dual-implementation-agreement-v6-84a-62a-pair.md)の機械照合で確認。

## 解釈境界（重要）

- solved 1326はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold着地時はv10拡張（新規file）が定型。並走cost-58c IN FLIGHTのため着手禁止。

詳細: [v9 second-implementation script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_chain_roots_second_independent_v9_20261115.py)（93,441 bytes・blob `3216df36`）、[v8第二実装（前回）](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v8-second-independent.md)、[第一実装v9（同日）](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v9-first-implementation.md)。
