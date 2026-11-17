# 2026-11-17 n11 class2-lane: cost73k claim v1 (census v6 runner-up)

## Context

長期レーン(n11 class2-lane)セッション。前回までに cost71e / cost72d /
cost63cd再生成 / cost72d bytes再検証 / cost72d証明書11本のBigInt独立
再検証 (commit a02b8ac0) を出版済み。並走レーンは census v6
(commit 5ea4def9) → cost73j claim v1 (460fbfc0) → cost73j sweep完走
(8484b092: 16 WIN7-D10 + 57 REFUTED-D10, 0 capped, 168,445,380 nodes)
まで出版済みで、73j証明書は抽出中 (main未出版)。cost73i証明書も
引き続きmain未出版。cost64h receipt fold着地済み (head 1452→1472) で、
76c→66i→66j→69j→71e→72d→73i→73j のfold chainは並走管理のまま
着手禁止。

## What was done

1. **census v6 script の独立再現**: published census v6 script
   (blob 91c89fa4) を92入力ファイル (79 harvest sources + 20 raw
   batch pins + 13 direct load_out pins、全blob sha照合) と共に
   ローカルでverbatim実行し、全published assert がPASS、
   出力がpublished v6 JSON とbyte-identical (md5 6d33e2f6...) である
   ことを確認。
2. **cost73k claim v1**: census v6 runner-up
   `00000000000000801206000000000400` (cost 73, demand c2=2,
   stones [10,49,50,57,60,71]) の fresh 73-bit depth-10 sweep を
   claim。**67 open + 6 confirmation bits**:
   - REFUTED-D10転送予測: bit 23 = pre-64h harvest,
     bit 34 = cost72d, bit 53 = cost66i, bit 107 = cost71e
   - **WIN7-D10転送予測 (2件)**: bit 26 = cost73i,
     bit 55 = cost69j — 本familyで初めてWIN転送を含むconfirmation
     batch。root_canonは全6件独立再計算で確認
     (bit 26 canon `00000000000000801206000004000400` = 73i bit 110
     のWIN、bit 55 canon `00000000000000801286000000000400` = 69j
     bit 110 のWIN)
   - legal 73 == edge cost (legal_candidates.py 独立列挙一致)
   - cost73kは本childの最初のclaim (既存cost73/73a-h/73i/73jは別child、
     raw-CDN probeでcost73kファイル群は全て404)

## Findings

- census v6 ranking は cost 73/73/73/74/75/78/79/79/79/80。
  選択行73jは並走がclaim済みのため、runner-upの73kが本レーンの
  最安未掃引未主張行。
- 73kの6 confirmation bitsのうち2 bits (26, 55) はWIN7-D10転送で
  ある。この2 rootの証明書は転送元lane (73i/69j) のfold待ちで
  あるため、本レーンのsweep後の証明書抽出対象は「open bits由来の
  WIN bits + confirmation再実行でWINとなった2転送bit」となり、
  重複証明書を避けるためmanifestでは転送元とcanon照合を行う。

## Interpretation guard

WIN7-D10証明書は個別7石rootのdepth-10内先手勝ちのみを証明する。
REFUTED-D10はLOSS証明ではない。solved 1472はmanifest被覆の簿記で
ある。claim v1はいかなる行も閉じない。receipt foldは
76c→66i→66j→69j→71e→72d→73i→73j の順で並走管理下に保留中。
11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
いずれも UNKNOWN のまま。

## Sweep complete (claim v2, same session)

1. **fresh v17 73-bit depth-10 sweep 完走** (9 batches = 8 sweep +
   1 confirmation, 全バッチpilot d6 = 3,402 nodes exact):
   - **25 WIN7-D10** [0,7,11,14,15,26,35,39,41,44,55,58,62,73,76,87,
     89,94,95,97,98,103,105,112,117] + **48 REFUTED-D10**, 0 capped
   - candidate nodes 128,861,941 (+9 pilots)。本family史上最多の
     WIN数 (73j 16, 73i 12, 71e 13, 72d 11)。
   - **6/6 confirmation bits はcensus v6 overlay予測どおり**:
     REFUTED (23/34/53/107) + **WIN (26=73i bit110, 55=69j bit110)**
     — 本family初のWIN転送を含むconfirmation batch。
     bit 53 = cost66i bit 10 とraw-identical (node数39,808も同一)。
2. **determinism**: batch 1-4は初回起動の事故による重複実行で
   2回完全実行され全フィールド同一 (非ms)。batch 7 (最重) と
   batch 9 (confirmation) は改めて別プロセスで再実行し全フィールド
   同一。計6バッチ分の再実行確認。
3. **v15 cross-engine**: 25 WIN bits全てを4 chunkで再実行し
   25/25 loss=true (pilot 5949 ×4 exact)。v15 nodes計116,892,833。
4. **stdlib raw audit** (`audit_cost73k_raw_batches_20261117.py`):
   全チェックPASS (claim v1 blob pin・転送canon 6/6・衝突0・
   raw batch pin 9/9)。2回実行byte-identical (md5 f42f5554...)。
   出力: `class2-lane-cost73k-raw-sweep-audit-20261117.json`。
5. **claim v2** (blob 3e24e27c): sweep complete・証明書pending。
   25 WIN roots → blind抽出予定 (bits 26/55 は73i/69j laneの
   bit 110とcanon同一のためmanifestにd4_canon_rootを記録し重複
   可視化)。

## Interpretation guard (sweep complete時点でも不変)

WIN7-D10証明書は個別7石rootのdepth-10内先手勝ちのみを証明する。
REFUTED-D10はLOSS証明ではない。solved 1472はmanifest被覆の簿記で
ある。本sweepはいかなるmanifest行も閉じない。receipt foldは
76c→66i→66j→69j→71e→72d→73i→73j の順で並走管理下に保留中。
11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
いずれも UNKNOWN のまま。

## Concurrent-claim incident and disposition (same session, later)

1. **並走sessionとの同時claim事故**: 本sessionのclaim v1
   (3b474b11, 02:19:06Z, census v6 rank-2基拠) のpush直後、
   同一の毎時並走実行が census v7 (bdd394a9) と **同一childの
   claim v1 (a0987c37, 02:29:31Z, census v7 rank-1基拠)** を出版し、
   同一path `class2-lane-cost73k-inflight-20261117.json` を
   上書きした (現main上のclaim blob = a24d3557, confirmation 7 bits
   [14,23,26,34,53,55,107], census v7の73j完了を反映)。
   並走のcoordination noteは本sessionのclaimを参照していなかった。
2. **判断**: 指示に従い同時書き込みを無理に押し進めない。本sessionの
   raw batch 9ファイル・audit JSON・claim v2 (3e24e27c) の出版を
   取りやめ、**並走のclaim (a24d3557) を行のcanonicalなin-flight
   claimのまま残す**。代わりに一意名の
   `class2-lane-cost73k-concurrent-session-sweep-record-20261117.json`
   を出版して、完走済みsweepの全数値 (25 WIN / 48 REFUTED / 0 capped、
   全73 bitのper-bit {loss,nodes,batch}、controls、7/7 confirmation
   agreement、非出版raw batchのmd5) をmain上に保存した。
3. **7/7 confirmation agreement**: 並走のcensus v7 claimが予測する
   7 confirmation bits (14=73j bit110 WIN転送を含む) は、本sessionの
   fresh v17 sweep (bit 14はbatch 1でopen bitとして走査済み) の
   結果と全て一致。census v6基拠の6 bitsも6/6一致。
4. **raw出版の担当**: 73k行のraw batch・audit・証明書出版は並走lane
   担当のまま。次回以降、並走がraw sweep audit / claim v2を出版した
   時点で、このconcurrent-recordとのcross-lane agreement check
   (verdict集合・per-bit nodes一致・confirmation outcomes) を
   cost-60c/63hの先例形式で実行・出版する。
5. **解釈ガード不変**: 本記録はいかなる行も閉じない。11×11空盤・
   二石root・S2・class 1/2/4 は UNKNOWN のまま。
