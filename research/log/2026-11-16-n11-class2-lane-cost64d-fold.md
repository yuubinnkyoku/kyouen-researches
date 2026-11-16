# 2026-11-16：cost-64d fold着地 — 23 WIN7-D10 receiptsをhead 1419へfold・**新canonical head 1435/174/6413/507337/4686/371251** — 全chain再現+証明書23枚再検証+conflict census 0・11×11はUNKNOWN

開始時main: `b3cfd4ac`（高速レーンのK0869/K0870統合直後・class2-lane経路への競合なし）。本レーンは前回完了済みのcost-64d sweep（64候補・WIN7-D10 23・REFUTED-D10 41・capped 0・`f38be6d6`）とwin23証明書出版（`9f4684ad`）を受け、**foldを`recompute_frontier_cost64d_receipts_20261116.py`新規作成で着地**した。claimはv4（fold complete・blob `e3cf7378`）へ更新（v3の全欄保存）。

## foldの全容（runpy chain reproduction）

1. **head 1419再現**: 13本の`reconstruct_tmp_*`前提スクリプト（84a→83d〔+second independent〕→83c→83a→69i→62a→58c→63h→63i→63j→65m→67d→70g）を依頼順に実行後、公開済み`recompute_frontier_cost65j_receipts_20261116.py`をrunpy実行。内部で全fold chain（canonical 1405→75e 1407→60c 1410→65j 1419）がbyte-identical再現され、1419出力3 blob（fold JSON `e8c83584`・ranking `cbed4d09`・top-cand `08aaf318`）がpublished版とbyte-identicalなことを`cmp`で確認。
2. **sweep再導出**: 8 raw batch（blob pin全一致）から64候補を再集計 — WIN bits [0,1,2,11,16,30,32,43,53,66,69,75,79,86,92,95,98,106,107,109,111,113,120]・41 REFUTED・0 capped・64,291,757 nodes（pilots 3402×8別）・terminal [13,17]・andclose全。determinism rerun batch5（bits [80,83,85,86,87,88,89,92]）node-exact・v15 crosscheck（pilot 5949・anchors [2,66,87,92,113]）両方向一致。
3. **監査の再主張**: sweep audit（blob `8ebfb721`）の`fold_prep_marginals_at_1419`（per-receiptの1419基準in-manifest marginals・union 16行・投影head 1435）と、独立第3実装marginal audit（blob `734b7879`・mismatches空・per_rootがpublished auditと完全一致）を、covers機構による再導出と突き合わせ全一致。
4. **証明書23枚のbyte再検証**: win23 manifest（blob `244e4b61`）どおり、whole 9枚+split 14枚（part1of2+part2of2+join receipt）のgit blob pin・md5・sorted-unique rows・root行・**root mobility == legal_candidates.py（23/23）**・BigInt union 0/0+Bareiss全PASS記録・fbt_drops 0・fatal nullを再assert。totals 861,439 rows / 69,769,470 extraction nodes / 1,193 sub-roots。
5. **conflict census**: 64候補のD4 orbit全てが1419時点のfolded roots（718@1410 + 65j receipts 17 = 735 receipt roots・distinct 734〔65f bit-25 rootは既fold済みcost-72b rootとbyte-identical〕）と**重複0**。23 WIN rootsは23 distinct D4 orbitsで、全folded rootに対しraw-hex・D4両方でdisjoint。**WIN/LOSS conflict 0**。
6. **childの残存確認**: child `00000000000000403800000008002000`はhead 1419で両開親（P `00000000000000403800000008000000` 24/1704・shared `00000000000000003800000008002000` 42/2929）にedge cost 64・dual demand c1=0,c2=2,c4=0で残存。
7. **fold（publication order = bits昇順・per-receipt marginals全pin）**: **childはbit 0でちょうど1回閉鎖**。zero-marginal receipts 9本（bits 1/11/43/53/66/69/79/98/111）。**total marginal 109 / marginal_in_manifest 16**・set-equality control（s_after == s_1419 ∪ covers(23 roots)）PASS。閉鎖16行はauditのunion_closed_rowsと完全一致し、全行がc1=0・c2>0・c4=0のclass-2需要行。

## 新headとper-parent

- **新canonical head: 1435/174/6413/507337/4686/371251**（1419+16行・6429→6413・508474−1137・4702−16・372388−1137）。hist変化はc2=1,c4=0: 214→212・c2=2,c4=0: 817→803のみ。
- per-parent: shared `…03800000008002000` **42/2929→31/2145**（−784）・target S5 `…40380000000800000` **24/1704→18/1287**（−417）・他11開親が各1–2行喪失（parent-row incidence計30・published監査の投影と全一致）。
- fold後のbest coverable class-2は不変（3/209〔K0863でdepth-10 receipt閉鎖不能確定済み〕・second 5/364）・best class-4不変（18/1460）・audit-blocked不変（10/698）。

## 解釈上の注意

**solved 1435はmanifest被覆の簿記。WIN7証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明。REFUTED-D10 41件はLOSS証明ではなく該当rootの深さ10内的反証のみ。STERILEもLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4、両開親は引き続きUNKNOWN。**

## 成果物

- fold script: [recompute_frontier_cost64d_receipts_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost64d_receipts_20261116.py)（2回実行で出力3ファイルbyte-identical）
- fold JSON: [class-frontier-cost64d-receipts-recompute-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost64d-receipts-recompute-20261116.json)（blob `082aa7f2`）
- ranking CSV: [class-frontier-s5-ranking-after-cost64d-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost64d-receipts-20261116.csv)（blob `130cc5ee`）
- top-candidates CSV: [class-frontier-top-candidates-s6-after-cost64d-receipts-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost64d-receipts-20261116.csv)（blob `838d98a3`）
- claim v4: [class2-lane-cost64d-inflight-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64d-inflight-20261116.json)（blob `e3cf7378`・v3 `9f4684ad`をsupersede・全欄保存）

## 次の候補（着手前にorbit重複censusとpre-sweep audit `6bff7890`/`140e8d28`・orbit-dedup測定 `4caee1a7`の確認が必須）

- P `00000000000000403800000008000000`の次の最安未sweep行（18行残・ranking CSV参照）とshared parent `00000000000000003800000008002000`の31行側の最安行のどちらが最良かは、fold後rankingで再計算してから決定。
- best coverable class-2 3/209（`00000000000000801202000000200000`）はSTERILE行3本で構成されdepth-10 receipt体系では閉鎖不能（K0863）・second 5/364のうち2行はSTERILE。よってclass-2 laneの次の価値あるtargetはP系・shared系のown-closable行が中心。
