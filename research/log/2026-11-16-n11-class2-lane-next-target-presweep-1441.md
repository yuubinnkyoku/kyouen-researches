# 2026-11-16：head-1441 next-target事前スイープcensus（presweep v4）— lane verdict harvest 4300 canons・conflicts 0・次の最安open行は`00000000000000801202010000800000`（cost 65・59 open・6 transfers）・3行はsweep不要のfully determined・11×11はUNKNOWN

開始時main: `f14f8bdb`（cost-64g fold着地・並走のindependent verification 2 commits `1b0bd2cf`/`6c2693f3`は取り込み済みで本レーンのパスと無競合）。前回のfoldでcanonical headは**1441/174/6407/506945/4680/370859**に前進したため、慣例どおり次のsweep対象を決めるためのhead-1441版presweep census（v4）を作成した。前回のpresweep v3（head 1438・blob `47174799`）の直接後継で、方法は同一のrunpy chain再現。

## 方法の要点（v3からの1つの違い）

公開済みcost-64g fold script `recompute_frontier_cost64g_receipts_20261116.py`（blob `97371b42`）はfold状態を`main()`内に持つため、v3のような`run_path`からの直接の状態取得ができない。そこでそのscript自身がstep 1で実行するのと同じ再現手順をcensus側で実行した: 公開済みcost-64f fold script（blob `522069ff`）をrunpyでhead 1438（1435 baseline含む全assert再実行）まで再現し、その上で**cost-64g receipt fold（bit 89 root `00000000020100003800000008080000`）をcensus内で再導出**し、fold scriptに出版済みの全pinと照合した: marginal 6のうちmanifest内3行のhex列（child `00000000000100003800000008080000` + cost-69行 + cost-65行）・demand histogram（c2=2,c4=0 802→801など）・5開親の(rows, edge cost) delta・parent-row incidences 7・edge cost delta 465・新head 1441。さらにfold script（`97371b42`）・fold JSON（`aff79002`）・claim v3（`125a728e`）の3 blobをhard-assertし、fold JSONの`cost64g_additions_on_cost64f_1438`（bit 89・marginal_manifest_hexes）が再導出と一致することを確認。receipt rootsは760+1=**761/747 D4 canons**（conflict censusどおりfold済み760とbit 89 rootは互いに素）。

## harvest（lane verdict census）

- **distinct verdict canons 4300 = WIN7-D10 430 + REFUTED-D10 3870・conflicts 0**。v3（4241/429/3812）からの増分は**+59 = 64g claim v3の1 WIN + 58 swept REFUTED**（5 transferred bits 5/29/104/111/119はv3時点で既に他sweep由来でharvest済みのため重複計上なし）。
- glob harvest `class2-lane-cost*.json`に加え、64d/64e/64f/**64g**の4組の公開raw batchをbit-exactで再検証: 64d 23 WIN/41 REFUTED・64e 0 WIN/60 REFUTED・64f 3 WIN/56 REFUTED swept・**64g 1 WIN/58 REFUTED swept（claim v3 `125a728e`対照・5 pre-sweep transfers含む・batch bit lists 8×8−5=59 bitの恒等式ごとassert）**。64gもclaim自体がglob harvestで64候補全判定（1+63）を追加済みで、59 swept-bit canonは全てclaim-harvested verdictsとcross-agree（新規追加0・0 conflict）。

## family census（head 1441）

- **class-2直接開親 `00000000000000403800000008000000`（P_PARENT）**: 18行/occurrences 1287・distinct open 1131・sum open after census **1261**（v3と全て不変・64g foldの7 incidencesは本親を含まない）。
- **shared開親 `00000000000000003800000008002000`（SH_PARENT）**: **30→29行**（64g child行のfold除去）・occurrences **2081→2017**・distinct open **1414→1355**・sum open after census **1733→1652**・distinct harvested 278→298。
- **fully determined rows 3行**（v3と同一・候補全bitがharvest済みのためsweep不要）: cost-64 `00000000000000003800000008002020`（64c STERILE行）・cost-64 `0000000000000000380000000a002000`（64e行）・cost-65 `00000000020000801202000000200000`。**いずれもREFUTED-D10 verdictの被覆であってmanifest上の閉鎖ではなくLOSS証明ではない**点はv3と同じ注意。

## 次のsweep対象（cheapest-first・open bits昇順）

| # | 行 (s6_hex) | parent | cost | demand | open | transfers |
|---|---|---|---|---|---|---|
| 1 | `00000000000000801202010000800000` | SH | 65 | c2=2 | **59** | 6 |
| 2 | `00000000000000a09002000080000000` | SH | 65 | c2=2 | 59 | 6 |
| 3 | `00000000000000003800000008002008` | SH | 66 | c2=1 | 59 | 7 |
| 4 | `00000000020000801202000000100000` | SH | 66 | c2=1 | 59 | 7 |

- **推奨: `00000000000000801202010000800000`**（presweep v3時点でもcost-64g childに次ぐ最安open行で、64g foldは本行を閉じていないためそのまま浮上）。bit tableでは65候補中6 bitがharvested_refuted転送済み（bits 35/50/51/55/64/109・root canonはcensus JSONに全列記）で、sweepすべきopen bitは59。
- rankingの(parent,row)対応はfamily_census側を正としcross-productしない（`parent_mapping_correction`はv3 blob `47174799`をsupersedeとして継承・12 entries全一致assert）。

## 解釈上の注意

**本censusはsearch-plan bookkeepingのみで、engine searchは1手も走らせておらず、verdictを作っておらず、行を閉じていない。solved 1441はmanifest被覆の簿記。WIN7証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明。REFUTED-D10 3870件はLOSS証明ではなく深さ10内的反証のみ。fully determined行もSTERILEもLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4はいずれもUNKNOWN。**

## 成果物

- census script: [next_target_presweep_head1441_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/next_target_presweep_head1441_20261116.py)（2回実行で出力2ファイルともbyte-identical・全assert PASS・所要~11.5秒/回・head-1438 chain runpy + 64g fold再導出を出版pin全件と照合）
- census JSON: [class2-lane-next-target-presweep-1441-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-presweep-1441-20261116.json)（149,684 B）
- rows CSV: [class2-lane-next-target-rows-1441-20261116.csv](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-rows-1441-20261116.csv)（両親47行+見出し）

## 次の候補（着手前に最新mainのin-flight確認が必須）

- 推奨行 `00000000000000801202010000800000`の59 open bitsを8 batch慣例（v16 engine・pilot gate 3,402 nodes）でsweep。IN FLIGHT claimを先に出してから着手し、並走laneの時間毎実行とのバッティングは最新mainの`class2-lane-cost*-inflight-*.json`で回避する（並走のin-flight 69a `00000000000000801222000000800000`・76c `00000000000010000809092000001000000`とは別行）。
- 59 bit中のWIN bitが見つかった場合のみ、証明書抽出→claim完了化→fold（head 1441→1441+k）。REFUTEDのみならNOT-STERILE記録に留めhead不変。
