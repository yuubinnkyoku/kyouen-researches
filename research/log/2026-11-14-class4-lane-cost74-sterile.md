# 2026-11-14 class-4 lane: cost-74 child sweep — 3rd sterile child (74/74 REFUTED-D10)

## 成果

- best class-4 blocker-candidate S5 `00000000020000003800000080000000`（after cost-61c+cost-63 frontier: 24 orbit / cost 1934）の
  最安未sweep S6 child `00000000020000003800000080000020`（edge cost 74・demand c1=2,c2=0,c4=3）の
  7石目sweepを完了した。
- **74非退化候補 → 74 REFUTED-D10・WIN7-D10 0件・capped 0件・総 248,858,245 nodes・terminal [13,17]**。
  cost-73（child#6）・cost-74 dual-use（child#8）に次ぐ **3例目の sterile child** で、
  このchild内のどの7石rootからも深さ10以内のWIN7が存在しない。
  c1=2,c4=3 の需要は他rootの証明書で被覆するしかない（frontierのsolved数は不変）。
- record: `output/class4-lane-cost74-sweep-20261114.json`（schema n11-class4-lane-cost74-sweep-20261114-v1・全候補のnodes・制御・interpretation_guard付き）。

## 方法・制御

- v15 engine verbatim（scripts/class4_child1_runner.ts・main の修正済み版をraw取得）をnative Node v22で実行。
  per-candidate freshEngine・close-first AND (depth>=8)・cap 400M・depth 10・pilot d6 制御は全バッチPASS（7/7・nodes=5949）。
- 候補列挙はengine自身のlegalMovesで独立再導出（legal=74・公表edge cost 74と一致）。
- 決定制御: bits 8/10/11/12 は2独立実行（1回は4並行contended・1回はforeground）でnode数完全一致
 （1760183/4661024/4376246/1469198）。最重量4候補 99/51/113/120 は別プロセスfresh再解で
  verdict/nodes/capped node-exact一致（10541668/8365457/8021858/8636284）。

## 運用の事実（この実行環境）

- **background worker（`cmd &`+wait）はコマンド境界でkillされる／waitが戻ってもファイルがまだ無い**ことがある。
  今回4並行を2回試みて、実体はforeground 1本が最速（1候補平均~8s・4並行時はcontendedで1候補~40s）。
  foreground batch（4+16+16+16+17）+ per-batch JSONLで完走した。
- 300秒timeoutは環境ごとリセットされworkspaceが消滅する（既知の再確認・中間成果はバッチ単位でpushする設計が正しい）。

## 影響と次の一手

- class-4 target S5のfrontierは本sweepでは不変（sterile・coversなし）。cost-74 childはsweep済みとして除外され、
  次の最安未sweep class-4 childは cost-74 `00000000020000003800000088000000`（c1=0,c2=1,c4=2）と
  cost-74 `00000000020000003801000080000000`（c1=0,c2=0,c4=3）。
- **11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN**。
  REFUTED-D10は「7石rootから深さ10以内のwinner勝ちの否定」のみで、勝敗の断定ではない。
