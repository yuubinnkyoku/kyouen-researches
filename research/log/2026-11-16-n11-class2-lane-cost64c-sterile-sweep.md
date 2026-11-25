# 2026-11-16：cost-64c sweep完走 — 64/64 REFUTED-D10・**STERILE**・cross-cover根3本（70j bits 111/119・65k bit 119・bit 119は両行を同時coverする唯一根）すべてREFUTEDで65k/70j両行のcross-cover失敗（負の事実）・head 1410不変

開始時main: `07b3cbcf`（cost-62b STERILE着地）。本レーンのclaimはcommit `d5d3d532`（IN FLIGHT v1 + prep script + STERILE-rows neighbor analysis）で先行push済み。

## 実施内容

### 1. 対象選定 — STERILE-rows neighbor analysis（新規script `analyze_sterile_rows_neighbors_20261116.py`・出版済み）
best coverable class-2 S5 `00000000000000801202000000200000`（3行/209・全行STERILE）の3 STERILE行（65k/70j/74h）のone-stone-replacement隣接open行をhead 1410で全系列挙: **65k 55 open（53 unswept・最安64群6件）/ 70j 113 open（108 unswept・最安64）/ 74h 73 open（71 unswept・最安66群2件）**。cost ≤ 70全候補のcovers事前計算の結果、**cost 64 child `00000000000000003800000008002020`**（dual demand c1=1,c2=1,c4=0・parents: class-2 `…03800000008002000` 51/3564〔lift 5〕+ class-1 `…03800000000002020` 74/5785〔lift 27〕・stones [5,13,27,59,60,61]）が**65k/70j両childの最安未sweep隣接**かつ**64合法候補中bit 111とbit 119が70j行を、bit 119が65k行も同時にcoverする**（1 receiptで2 STERILE行閉鎖の可能性）→sweep着手。

### 2. sweep完走（v16・depth 10・cap 1e9・8バッチ・4並列）
- **64/64・0 WIN7-D10・64 REFUTED-D10・0 capped・総nodes 46,148,506**。pilot d6 8×3402（全batch loss=false）。terminal全件[13,17]・andclose全true。heaviest: bit113 2,540,082 / bit79 2,137,917 / bit80 2,076,976 / bit12 1,997,132 / bit70 1,860,840 / bit74 1,719,749。
- **cross-cover根3本すべてREFUTED-D10**: bit 111（654,732 v16 / 2,049,140 v15 nodes）・bit 119（301,375 v16 / 735,484 v15）。bit 119は65k行+70j行の両方をcoverする唯一根だったがREFUTED → **1 receiptで65k/70j両STERILE行を閉じる唯一の機会が消えた**（負の実験的事実のみ・LOSS証明ではない）。
- determinism rerun（batch5・fresh process）: node-exact一致（ms以外）。v15交差（単一foreground invocation・pilot d6 5949）: bits 111/119/113/79/0の5アンカー全てloss=false一致。

### 3. 独立監査 `audit_cost64c_raw_sweep_20261116.py`（stdlibのみ・byte-identical再実行・audit JSON md5 `3f65896a…`）
64候補独立再列挙bit-exact・8バッチ明示bitリスト検証・6 deletion D4正準化再導出（lift 5→class-2 parent・lift 27→class-1 parent bit-exact・13/59/60/61はclosed orbit・head-1410 ranking CSV検証 2,51,3564 / 1,74,5785）・MS5 manifest行（cost 64・class bitmask 3）・**cross-cover関係の独立再導出（64候補×7 deletionのcanonical coversで70j [111,119]・65k [119]）**・全assert一発通過。

### 4. 結論 — STERILE・foldなし・head不変
- **cost-64c childはSTERILE**（NOT a LOSS proof）。証明書0・fold材料なし・**canonical head 1410/174/6438/509109/4711/373023不変**（両open parentがchild行を保持）。
- claim `class2-lane-cost64c-inflight-20261116.json`はv2（completed STERILE）に更新。

## 構造的事実

- best coverable class-2 S5（3/209）の3 STERILE行のcross-cover負の事実が累積: **70j行 = cost-60隣接（bit 119）・cost-62隣接（bits 21, 109）・cost-64隣接（bits 111, 119）の6根すべてREFUTED**（70j-childの最安3隣接はcross-cover機会を使い切り）。**65k行 = 最安隣接cost-64cのbit 119 REFUTED**（65k-childの残りcost-64隣接5件とcost-66+が残る）。74h行は未着手（最安cost-66群が残る）。
- 3 STERILE行のいずれもopenのまま（70j erratumの通り、他のchildのWIN7 receiptのmarginal経由のcross-coverは今も可能）。

## 次の状況

- canonical head **1410**不変。次の自レーン候補: 65k-childの残るcost-64隣接5件（`…03800000008002002`〔covers 65k bit 119〕・`…03800000008003000`〔bit 119〕・`…0380000000a002000`〔bit 119〕・`…00403800000008002000`〔bit 119〕・`…8012020a000000800000`〔bit 109〕）か74h-child最安cost-66群（`…8012260000000000000`〔bit 109〕・`…8052220000000000000`〔bit 109〕）。いずれもcovers事前計算済み（neighbor analysis JSON出版済み）。
- **solved 1410はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。11x11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま**。
