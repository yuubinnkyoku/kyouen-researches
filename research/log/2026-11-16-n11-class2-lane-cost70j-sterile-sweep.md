# 2026-11-16：cost-70j sweep完走 — best coverable class-2 S5の全残行STERILE確定（負の構造的事実）・独立audit公開・claim引退

開始時main: `f0c9a005`（本レーンのcost-70j claim公開。その後並走の `ab7046e8`/`ab9ecae2`〔K0832レーン・workflow〕と `39a5ad18`〔S6-child overlap audit・別実験dir〕が着地、いずれもパス非競合）。対象はcost-70j（child `00000000000000801282000000200000`・**best coverable class-2 candidate S5 `00000000000000801202000000200000` のcost-70行**・head 1407基準・dual demand c1=1,c2=1 — class-2 S5 3/209〔lift 55〕+ class-1 S5 `00000000000000801082000000200000` 75/5971〔lift 57〕の両方の行）。

## 実施内容

### 1. sweep完走（9バッチ・4並列・約2.5分）
- v16 engineで全70 legal candidatesを実行: **70/70 REFUTED-D10・0 WIN7-D10・0 capped・総nodes 53,890,941**。pilot 9×3402（全batch d6制御 loss=false）・terminal全[13,17]・andclose全true。
- heaviest: bit9 5,928,340 / bit92 5,321,927 / bit114 3,568,157 / bit4 2,995,745 / bit76 2,249,653 / bit42 2,038,300。
- **決定性再実行**（batch5 bits 52,54,67,72,73,74,75,76・fresh process）: verdicts/nodes/capped/terminalStoneRange全てnode-exact一致（ms以外）。
- **v15交差**（class4_child1_runner.ts・独立engine）: 最重量REFUTEDアンカー bits 9/92/114 → 全て loss=false（nodes 10,628,438/9,924,059/6,397,886・pilot d6 5949 loss=false・単一foreground invocation）。v16と判定一致。

### 2. 独立audit（`scripts/audit_cost70j_raw_sweep_20261116.py`・stdlibのみ・出力 `class2-lane-cost70j-sweep-audit-20261116.json`）
- Python標準ライブラリのみ・Bareiss整数行列式・floatなし・repo engine不使用。raw batch 9本+determinism+v15の11 artifactから集計を再導出（70候補・0 WIN・70 REFUTED・0 capped・53,890,941 nodes・9 pilots 3402）。
- legal候補70件を独立再列挙 → claimとbit-exact一致。determinism batch5 node-exact・v15アンカー3件の合法性と判定一致を確認。
- 6つのone-stone deletion D4正準化を独立再導出: del55 → best coverable class-2 S5 `00000000000000801202000000200000`・del57 → class-1 S5 `00000000000000801082000000200000` がbit-exact一致。他4 deletion（21/49/60/71 → `…03800000008000020`/`…801280000000200000`/`…800282000000200000`/`…012820000000200000`）は6 distinct orbitで、公開済みhead-1407 ranking CSV上に存在しない（= closed S5 orbit）。
- 両open parentをhead-1407 ranking CSV（class-2: 2/3/209・class-1: 1/75/5971）とtop-candidates CSVで独立検証。**class-2 parentの残3行がちょうどcost-65k・70j・74hであることをCSVから直接確認**。
- audit script再実行byte-identical（audit JSON md5 `654db415c669cf622cd6121b879d95f2`・script md5 `4576f8d8226ce003b88f722614b197f5`）。全assert一発通過。

### 3. 出版（commit `3409383e`・全14ファイル着地確認）
- raw batch 1–9 JSONL・determinism rerun・v15 crosscheck・audit JSON・audit script・更新claim（schema v2 completed-STERILE）を一括push。既存claimキー全保持、`sweep_results`/`raw_artifacts`/`independent_audit`/`completion_note`/`frontier_impact_note`/`next_action` 追加。

## 構造的事実（本成果の核心）

**best coverable class-2 candidate S5 `00000000000000801202000000200000`（3行/209）の全3残行がSTERILE確定**:
- cost-65行 `00000000020000801202000000200000`（65k sweep: 65/65 REFUTED-D10）
- cost-70行 `00000000000000801282000000200000`（本70j sweep: 70/70 REFUTED-D10）
- cost-74行 `00000000000000889002000000000800`（74h sweep: 74/74 REFUTED-D10）

このS5は**depth-10 WIN7 receiptでは閉鎖不能**（いかなる追加D10 sweepでも閉じない行が存在しない）。3行/209のedge costは、depth-10超の証拠（各行のdepth>10反証か同値の不変条件）が存在しない限りreceipt機構から永久に到達不能。dual class-1 parent（75/5971）もこの行をreceipt-closable行として失う。

これは**負の実験的事実・構造的事実であってLOSS証明ではない**。REFUTED-D10は「その7石rootから10手以内の先手勝ちが存在しない」ことのみを意味する。frontier計数は不変（head 1407/174/6441/509300/4711/373023・solved 1407はmanifest簿記）。

## 次の状況

- 次のcoverable class-2 candidateは第二候補S5 `00000000000000801202000040000000`（5行/364）だが、残行のうち64/71はSTERILE済み・76cはin-flight（着手禁止）・76d/77eは並走fold-pending → **現時点で本レーンが着手可能なunclaimed coverable class-2行は存在しない**。
- 76d/77e foldの着地後に1407とのreconciliation foldが必要（root disjointness対75eの4 rootをassert）。
- 11x11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。

## 正誤（erratum・同日セッション内訂正）

初版のlog本文・audit JSON `structural_consequence`・claim v2 `completion_note` に書いた「**receipt機構から永久に到達不能（permanently unreachable by the receipt mechanism）**」は**過大な主張だった**。正しくは:

- STERILE行（自出行のsweepが0 WIN7-D10）も、**他のchildのsweepで得られたWIN7 receiptのcross-cover（marginal）で閉鎖され得る**。これはfold機構の標準経路で、先例が複数ある:
  - cost-70g child は head 1249 で **cost-70f bit-84 receiptのcross-cover**で閉鎖（"child already closed at head 1249 (cost-70f bit-84 cross-cover)"）。
  - cost-75e bit-10 のin-manifest marginal `00000000000000801202000000000201` は**2つのopen parentの行を同時に**閉鎖した。
- したがって確定するのは「**このS5は自出行のsweepからはreceiptを一切産まない = own-row-coverableカテゴリからの離脱**（この点でaudit-blocked S5 `00000000000000809082000000000000`〔10/698〕と同カテゴリ）」まで。3行の閉鎖は今後cross-coverまたはdepth-10超の証拠に全面的に依存するが、「永久に不可能」ではない。
- 訂正反映: audit JSON/scriptは `structural_consequence` のみ修正して再生成（v1→v2差分は当該テキストのみをdiff確認。数値・assert・交差検査は全て不変。audit JSON md5 `654db415…`→`11cf0f70…`・script md5 `4576f8d8…`→`01466f22…`）。claimは schema v3 に更新（`erratum_note` 追加・既存キー全保持）。

solved 1407はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEは自出行からの閉鎖不能の表明でLOSS証明ではない。11x11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4はいずれもUNKNOWN。
