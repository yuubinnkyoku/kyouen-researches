# 2026-11-16：head-1438 next-target事前スイープcensus（presweep v3）— lane verdict harvest 4241 canons・conflicts 0・次の最安open行は`00000000000100003800000008080000`（cost 64・59 open・5 transfers）・3行はsweep不要のfully determined・11×11はUNKNOWN

開始時main: `5152c1d0`（並走のREMO lane K0874 2 commits `7a81d6e7`/`5152c1d0`は本レーンのパスと無競合）。前回のcost-64f fold着地（`2d3052df`）でcanonical headは**1438/174/6410/507143/4683/371057**に前進したため、cost-64d/census系の慣例どおり次のsweep対象を決めるためのhead-1438版presweep censusを作成した。前回のpresweep v2（head 1435・blob `59d42a6b`）の直接後継で、方法は同一: 公開済みfold script `recompute_frontier_cost64f_receipts_20261116.py`（blob `522069ff`）をrunpyで丸ごと再現（1435 baseline含む全assert再実行）し、そのchain上でlane verdict harvest・family census・bit tableを再導出する。

## harvest（lane verdict census）

- **distinct verdict canons 4241 = WIN7-D10 429 + REFUTED-D10 3812・conflicts 0**。v2（4182/426/3756）からの増分は**+59 = 64f claim v5の3 WIN + 56 swept REFUTED**（5 transferred bits 21/35/55/64/109はv2時点で既に他sweep由来でharvest済みのため重複計上なし）。
- glob harvest `class2-lane-cost*.json`に加え、64d/64e/64fの3組の公開raw batchをbit-exactで再検証: 64d 23 WIN/41 REFUTED（claim v4対照）・64e 0 WIN/60 REFUTED（claim v2 `55c51c92`対照・4 pre-sweep transfers含む）・**64f 3 WIN/56 REFUTED swept（claim v5 `b43303e8`対照・5 pre-sweep transfers含む・batch bit lists 8×8+3=59 bitの恒等式ごとassert）**。64fはclaim自体がglob harvestで64候補全判定（3+61）を追加済みで、59 swept-bit canonは全てclaim-harvested verdictsとcross-agree（新規追加0・0 conflict）。
- 今回のscript修正（出版前の品質保証）: 初版の64f検証assertが`legal_candidates(child) − transferred == swept`を主張して失敗した。正しい恒等式は`swept ∪ win ∪ transferred == candidates`（swept 56 + WIN 3 + transferred 5 = 64・batch 59 bit = swept ∪ win）。64eはWIN 0のため`− transferred`だけで成立していた式の、WINビットがある場合への一般化。修正後に全assert PASS。

## family census（head 1438）

- **class-2直接開親 `00000000000000403800000008000000`（P_PARENT）**: 18行/occurrences 1287・distinct open 1131・sum open after census **1261**（v2と全て不変・64f foldの7 incidencesは本親を含まない）。
- **shared開親 `00000000000000003800000008002000`（SH_PARENT）**: **31→30行**（64f child行のfold除去）・occurrences **2145→2081**・distinct open **1473→1414**・sum open after census **1813→1733**・distinct harvested 259→278。
- receipt rootsは**757/743 → 760/746 canons**（64fの3 WIN receipts）。
- **fully determined rows 3行**（v2と同一・候補全bitがharvest済みのためsweep不要）: cost-64 `00000000000000003800000008002020`（64c STERILE行）・cost-64 `0000000000000000380000000a002000`（64e行）・cost-65 `00000000020000801202000000200000`。**いずれもREFUTED-D10 verdictの被覆であってmanifest上の閉鎖ではなくLOSS証明ではない**点はv2と同じ注意。

## 次のsweep対象（cheapest-first・open bits昇順）

| # | 行 (s6_hex) | parent | cost | demand | open | transfers |
|---|---|---|---|---|---|---|
| 1 | `00000000000100003800000008080000` | SH | 64 | c2=2 | **59** | 5 |
| 2 | `00000000000000801202010000800000` | SH | 65 | c2=2 | 59 | 6 |
| 3 | `00000000000000a09002000080000000` | SH | 65 | c2=2 | 60 | 5 |
| 4 | `00000000000000003800000008002008` | SH | 66 | c2=1 | 60 | 6 |

- **推奨: `00000000000100003800000008080000`**（64f claim target_contextのrunner-upどおり）。bit tableでは64候補中5 bitがharvested_refuted転送済み（bits 5/29/104/111/119・root canonはcensus JSONに全列記）で、sweepすべきopen bitは59。
- rankingの(parent,row)対応はfamily_census側を正としcross-productしない（v2の`parent_mapping_correction`を継承・12 entries全一致assert）。

## 解釈上の注意

**本censusはsearch-plan bookkeepingのみで、engine searchは1手も走らせておらず、verdictを作っておらず、行を閉じていない。solved 1438はmanifest被覆の簿記。WIN7証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明。REFUTED-D10 3812件はLOSS証明ではなく深さ10内的反証のみ。fully determined行もSTERILEもLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4はいずれもUNKNOWN。**

## 成果物

- census script: [next_target_presweep_head1438_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/next_target_presweep_head1438_20261116.py)（2回実行で出力2ファイルともbyte-identical・全assert PASS・所要~12秒/回・runpy対象は公開fold script blob `522069ff`で出版scriptとの整合を自動維持）
- census JSON: [class2-lane-next-target-presweep-1438-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-presweep-1438-20261116.json)（140,478 B）
- rows CSV: [class2-lane-next-target-rows-1438-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-rows-1438-20261116.csv)（両親48行+見出し）

## 次の候補（着手前に最新mainのin-flight確認が必須）

- 推奨行 `00000000000100003800000008080000`の59 open bitsを8 batch慣例（v16 engine・pilot gate 3,402 nodes）でsweep。IN FLIGHT claimを先に出してから着手し、並走laneの時間毎実行とのバッティングは最新mainの`class2-lane-cost*-inflight-*.json`で回避する。
- 59 bit中のWIN bitが見つかった場合のみ、証明書抽出→claim完了化→fold（head 1438→1438+k）。REFUTEDのみならNOT-STERILE記録に留めhead不変。
