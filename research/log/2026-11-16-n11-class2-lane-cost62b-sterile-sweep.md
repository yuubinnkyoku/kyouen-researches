# 2026-11-16：cost-62b sweep完走 — 62/62 REFUTED-D10・**STERILE**・cross-cover根2本（bits 21, 109）ともREFUTEDで70j行cross-cover失敗（負の事実）・head 1410不変

開始時main: `05cc8bdb`（cost-60c fold・head 1410）。本レーンのclaimはcommit `911d35e6`（IN FLIGHT v1 + prep script）で先行push済み。

## 実施内容

### 1. 対象選定と事前検証（claimの事前計算を履行）
best coverable class-2 S5 `00000000000000801202000000200000`（3行/209・全行STERILE）の70j行 `00000000000000801282000000200000` cross-cover続行。70j-childのone-stone-replacement隣接open行のうち、cost-60c（ REFUTED済みcross-cover bit 119）の次に安い未sweep隣接がcost 62（child `00000000000000801282020000000000`・dual demand c1=1,c2=1,c4=0・lift parents = class-2 `00000000000000801202020000000000` 49/3360〔lift 55〕と class-1 `00000000000000801082020000000000` 73/5489〔lift 57〕）。**着手前事前計算（前回60cの教訓の履行）: 62合法候補のうちcross-cover根はbit 21（root `00000000000000801282020000200000`）とbit 109（root `00002000000000801282020000000000`）の2本** — 60c（bit 119のみ）の2倍の好条件でsweep着手を決定。

### 2. sweep完走（v16・depth 10・cap 1e9・10バッチ・4並列）
- **62/62・0 WIN7-D10・62 REFUTED-D10・0 capped・総nodes 34,617,690**。pilot d6 10×3402（全batch loss=false）。terminal [13,17]（bit 12のみ[15,17]）・andclose全true。heaviest: bit114 1,701,321 / bit105 1,699,567 / bit43 1,562,851 / bit52 1,402,441 / bit32 1,345,798 / bit45 1,310,282。
- **cross-cover根2本ともREFUTED-D10** → 70j行はこの隣接経由でも閉鎖せず。**cost-60c bit 119 REFUTEDと合わせ、70j-childの最安2隣接（cost 60・62）のcross-cover機会はすべて尽きた**（負の実験的事実のみ・LOSS証明ではない）。
- 運用メモ: 初回waveはrunner CLIの`--cap`デフォルト950,000で実行してしまい6候補がcapped判定となったため、cap 1e9で全バッチをやり直した（当初バッチは破棄・成果物は最終実行のみ）。バックグラウンド`&`チェーンは`cd`が先頭ジョブにのみ効くためサブシェル`( cd … && node … ) &`必須（3ジョブが`/home/user`でMODULE_NOT_FOUNDになったのを復旧）。

### 3. 検証体制
- determinism rerun（batch5・fresh process）: verdicts/nodes/capped/terminalStoneRange全てnode-exact一致（ms以外）。
- v15交差（単一foreground invocation・pilot d6 5949）: cross-cover根21/109・最重量114/105・bit0の5アンカー全てloss=false一致（v15 nodes: 482,514/1,777,172/4,680,094/4,078,878/925,470）。
- **独立監査 `scripts/audit_cost62b_raw_sweep_20261116.py`**（stdlibのみ・Bareiss整数行列式・D4正準化・CSV解析を独立実装・repo engine不使用）: 62候補独立再列挙bit-exact・10バッチ構成（明示bitリスト）どおり・6 deletion D4正準化再導出（lift 55→class-2 parent・lift 57→class-1 parent bit-exact・他4 deletion 41/49/60/71はhead-1410 ranking CSV上に不存在=closed orbit）・両open parentをhead-1410 ranking CSVで検証（2,49,3360 / 1,73,5489）・MS5 S6 manifestでのchild行（cost 62・class bitmask 3）確認・**cross-cover関係の独立再導出（62候補×7 deletionのcanonical coversでちょうどbits 21, 109）**・全assert一発通過・再実行byte-identical（audit JSON md5 `d8d875f3…`）。

### 4. 結論 — STERILE・foldなし・head不変
- **cost-62b childはSTERILE**: 62合法根のどれもdepth-10 WIN7 receiptを産まない → このS6行は自出行のsweepからは閉鎖不能（NOT a LOSS proof）。証明書0・fold材料なし・**canonical head 1410/174/6438/509109/4711/373023不変**（両open parentがchild行を保持）。
- claim `class2-lane-cost62b-inflight-20261116.json`はv2（completed STERILE）に更新。

## 構造的事実

- best coverable class-2 S5（3/209）の3 STERILE行のうち、**70j行のcross-coverはcost-60隣接（bit 119 REFUTED）とcost-62隣接（bits 21, 109 REFUTED）の両方で失敗**。70j行はopenのまま（70j erratumの通り他childのreceiptからのcross-coverで閉鎖され得るので「永久に不可能」ではない）。次の隣接候補は65k-child（最安隣接cost 64群）・74h-child（最安cost 65 `00000000000000805222000000000000`）の近傍。
- 60cと62bで、70j-childの最安2つのone-stone-replacement隣接が両方STERILEかつcross-cover根REFUTEDという強い負のパターンが確定。ただしSTERILE行のcross-coverは「他のchildのWIN7 receiptのmarginal」経由なら今も可能で、次は65k/74h近傍のsweepでWIN7が出た場合のmarginal経由を狙う。

## 次の状況

- canonical head **1410**不変。76c claim（1407基準）・76d/77e fold（1405基準）はin-flightのまま・着手禁止。76d/77e fold着地時は1410 headとのreconciliation foldが必要（root disjointness対60c rootをassert）。
- 次の自レーン候補: 65k-child最安隣接cost 64群・74h-child最安隣接cost 65 `00000000000000805222000000000000`。着手前にcovers事前計算で70j/65k/74h行をcoverする合法rootの有無を確認してからclaim。
- **solved 1410はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。11x11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま**。
