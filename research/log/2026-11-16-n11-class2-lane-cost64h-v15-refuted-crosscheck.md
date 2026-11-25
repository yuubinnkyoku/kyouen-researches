# 2026-11-16：cost64h 41 REFUTED-D10 bitのv15 cross-engine検証 — 41/41 verdict一致（WIN対照2 bit node-exact・pilot 5/5）

開始時main: `c8a658f8`（fold receipt未着地）。並走が出版したcost64hのv15 crosscheck（`class2-lane-cost64h-v15-crosscheck-20261116.jsonl`）は**23 WIN bitのみ**をカバーしており、41 REFUTED-D10 bitはv15 cross-engine確認がまだない層だった。本セッションで**41 REFUTED-D10 bit全てをv15 runner（blob `8744fc65…`）で再実行**し、verdict-level cross-engine一致を確認した。

## 結果

- **41/41 REFUTED-D10 bit: v15で loss=false・capped=false**（v16出版verdictとcross-engine一致・capは1e9明示）。v15 nodes総和 **57,767,631**（情報pin・v16の47,017,565とはengine相違により一致を期待しない）。
- **WIN対照 2 bit（4, 120）**: v15再実行が出版済みv15 crosscheckと**node-exact一致**（3,555,878 / 4,836,378・loss=true・uncapped）。同一engine同一入力の決定的再現を対照として確認。
- **pilot_d6 control 5/5**（worker a-e各1・loss=false・nodes=5949・uncapped）。v16 pilot（nodes=3402）とnodesが異なるのはengine相違によるもので、controlの意味（既知P-positionの正しいloss=false判定）は両engineで保たれている。
- 実行は5 worker（41 bitをa-dに分割、WIN対照をeに配置）・各worker cap 1e9・depth 10・andclose。
- 検証JSON checks **C1-C8全PASS**: 41 bit存在一意・v15全41 loss=false/uncapped・v16出版も同・bit集合等価・pilot 5/5・WIN対照node-exact・node_sum pin・engine pin。

## 意味

- 並走のv15 WIN crosscheck（23 bit）と本検証（41 REFUTED bit + 対照）により、**cost64h sweepの全64 bitが二つの独立実装（v15/v16）でverdict一致**した。WIN 23 bitは両engine間で、REFUTED 41 bitも両engine間で、WIN対照2 bitは同一engine内でnode-exact再現も確認済み。
- v16全量独立再実行（`17ab4b4b…`・64/64 node-exact）と合わせ、cost64h（child `00000000000000403800000008100000`・claim v2 blob `68e48780…`）は **(1) v16 fresh-environment全量再実行、(2) v15 cross-engine verdict一致** の二重の独立確認を持つ。fold receipt着地後のagreement checkerの入力verdictはこの二重検証の上に乗る。

## 出版

- v15生データ 5本: `class2-lane-cost64h-v15-refuted-crosscheck-{a..e}-20261116.jsonl`（worker a-d=41 refuted bits、e=win対照+pilot。blob pinsはverification JSONに記載）。
- 検証JSON: `class2-lane-cost64h-v15-refuted-crosscheck-verification-20261116.json`（per-bit v15/v16 verdict比較・win対照detail・checks C1-C8）。
- 検証script: `verify_cost64h_v15_refuted_crosscheck_20261116.py`（5本のv15 JSONL・v16出版raw batch 1-8・出版v15 crosscheckを読み、assert内蔵・全チェック再計算）。

## 信頼境界

- cross-engine一致は**同じゲーム木の異なる実装**によるverdict再現であって、出版verdictを超える新規verdictは作らない。両engineが共通の誤った仮定（AND/OR关门・depth解釈等）を共有する可能性は、この比較では排除されない（それは証明書の独立検証・pilot controlの役割）。
- REFUTED-D10はLOSS証明ではない。WIN7-D10証明書は個別7石rootから深さ10以内の先手勝ちのみを証明する。
- solved（head 1452・prereg投影1472を含む）はmanifest被覆の簿記であり、勝敗の確定ではない。
- 標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4 はいずれも **UNKNOWN** のまま。

## 再現

```sh
for w in a b c d e: node --experimental-strip-types scripts/class4_child1_runner.ts \
  --child 00000000000000403800000008100000 --bits <worker w bits> \
  --depth 10 --cap 1000000000 --andclose 1
python scripts/verify_cost64h_v15_refuted_crosscheck_20261116.py
```

worker分割: a=[1,2,3,5,14,16,18,21,23,25,29] b=[34,35,43,45,46,53,54,66,69,82] c=[85,86,87,88,92,95,96,97,98,99] d=[102,103,105,106,107,108,111,112,115,117] e=[4,120]
