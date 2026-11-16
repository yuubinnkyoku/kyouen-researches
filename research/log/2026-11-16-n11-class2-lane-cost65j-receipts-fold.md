# 2026-11-16：cost-65j fold着地（前提修正付き）— head 1410→1419・9行閉鎖（cost-64×2含む）・WIN7証明書4枚（bits 112/116/118/119）・動機childは既閉鎖と判明（63a bit-97 cross-cover・conflict census 0）

開始時点: cost-65j sweep完了済み（claim v4 `4245cbf0`、65/65候補・17 WIN7-D10・48 REFUTED-D10・0 capped）だがfold未着地。前セッションの計画は「17 WIN receiptsをhead 1410にfoldしてchild（edge 65）を閉じる」前提だった。**v1 fold scriptの初回実行がroot disjointness assertで失敗し、調査の結果この前提そのものが誤りだったことが確定した**（下記）。修正したv2でfold着地。

## 主要発見：動機childはhead 1410で既にsolved

- child `00000000000000809102000080000000`は**cost-63a bit-97 WIN receipt root `00000002000000809102000800000000`（65f bit-79候補と同一D4 orbit）により、2026-11-15のwarm-multiband2/unified-merge foldで閉鎖済み**。当該foldの`marginal_manifest_hexes`はchild行のみ（published record・blob `0830cfc3746baa6ad5b542579dc9d657b61ac72a`で再assert）。
- さらに3つのfold済みrootもchildをcover: cost-72b root `00000000000000809102000082000000`（**65f bit-25 rootとbyte-identical**）・cost-72b root `00000002000000809102000002000000`（bit-91 orbit）・cost-69i root `00000002000000809102000000002000`（bit-101 orbit）。
- **65f/65j sweepはこの4 orbit（bits 25/79/91/101）を全て独立にWIN7-D10と再判定 — WIN/LOSS conflict 0**（65候補全orbit vs 718 folded rootsのcensusで重複はこの4つだけ、残り61 orbitはdisjoint）。
- **第3 class-2 target S5 `00000000000000809102000000000000`自体もhead 1410で残行0**（完全閉鎖済み）。
- 時系列: claim v4の「cheapest remaining unswept child」前提はafter-75c frontier（solved 1062）時点では正しかったが、multiband2 merge・69i・72b fold（いずれも11-15）でchildが閉じた後はstale。sweep自体（batch 8-9・証明書抽出）の成果は無効ではなく、foldの価値が「child閉鎖」ではなく「残存9行閉鎖」に変化した。published cover mapのnoteは「open否かはfold時に決まる」と慎重で、published誤りはなし。

## 実施内容

### 1. fold v2（`scripts/recompute_frontier_cost65j_receipts_20261116.py`・schema v2）
- runpyでcost-60c chain head 1410/174/6438/509109/4711/373023を再現（60c fold scriptがchain全体・75e fold・3出力blobをbyte-identical再assert）。
- 65f+65j sweepを9 raw batch（blob pin済み）から再導出: 65候補・17 WIN7-D10・48 REFUTED-D10（bit-113 transfer込み）・0 capped・402,652,063 nodes（pilots込み）。
- cover map（blob `d6d20e52…`）再assert: 17 receiptsのD4-canonical one-stone deletionsは34 manifest行をcover。**うちhead 1410でopenなのは9行のみ**（25行は既solved、child含む）。
- 4枚のWIN7証明書（bits 112/116/118/119）を再assert（下記3）。
- conflict census・root overlap audit・child既閉鎖のblob-pin再assert・9行の需要（全てc1=0,c2=2,c4=0・dual class-2 parent）を確認。
- **17 receiptsをpublication order（65f昇順→65j昇順）でfold: 9行閉鎖・total marginal 61・marginal_in_manifest 9・zero-mim receipts 8本（bits 15,23,25,66,79,91,101,119）**。全per-receipt marginalをpin。
- **新head 1419/174/6429/508474/4702/372388**（unique_remaining_s6 -9・sum_remaining_cost -635・needed -9/-635・hist c2=2,c4=0: 826→817）。
- per-parent（touched 9個、全class-2）: 共有parent `00000000000000003800000008002000` **51/3564→42/2929**（9行全てを保持していた）・`…08000002` 41/3095→39/2962（2行）・`…08001000` 46/3448→45/3384・`…08400000` 44/3268→43/3197・`…0408000000` 56/4624→55/4550・`…00100008000000` 66/5493→65/5417・`…00400008000000` 56/4444→55/4375・`…438…08000000` 67/5621→66/5547・`…801202000000000100` 60/4939→59/4865。行-母数計18 incidences = 9行×2 parentで整合。
- 上位候補不変: best coverable class-2 3/209（65k/70j/74h STERILE行はopenのまま）・second 5/364・audit-blocked 10/698・best class-4 18/1460。
- 出力3ファイル（**再実行byte-identical確認済み**）: fold JSON（**blob `e8c835840f2fad8ffd9a9a8e6f1a9f5944470524`**・20,641 bytes）・ranking CSV（blob `cbed4d094b87dc4fe2cc48b2db375d7ddb0776c6`・7,535 bytes）・top-candidates CSV（blob `08aaf31892680668e7e292848235a154eb746407`・3,715 bytes・60c/75e版と同一）。

### 2. 閉じた9行（全てdual class-2 demand c1=0,c2=2,c4=0）
`00000000000000043800000008002000`(bit 4)・`00000000000000003800000408002000`(18)・`00000000000000003800000008003000`(**cost-64**, 20)・`00000000000000003800000008002002`(**cost-64**, 21)・`00000000000000003800400008002000`(28)・`00000000000000003800000008002200`(109)・`00000000010000003800000008080000`(112)・`00000000000000003800100008080000`(116)・`00000000000000003800000008480000`(118)。

### 3. WIN7-D10証明書4枚（bits 112/116/118/119・二重検証済み・今回出版）
- manifest: `class2-lane-cost65j-win7-certificates-20261116.json`（**blob `d4981d7e075d8b2bb2e032790cbb95555bdc2b84`**・9,804 bytes）。totals: 4 certs・232,426 rows・36,781,305 extraction nodes・225 sub-roots・winner 313,767・loser 93,295・terminals 79,542・8,381,377 bytes。
- bit 112: 64,020 rows / 8,598,381 nodes / 58 sub-roots。bit 116: 49,082 / 3,238,015 / 56。bit 118: 70,510 / 20,287,890 / 56。bit 119: 48,814 / 4,657,019 / 55。
- **全4枚をpart1of2+part2of2+join receiptで出版**（最大part 1,270,899 bytes = bit 118 part1of2）。公開用split閾値を1,200,000 bytesに設定: 1.75 MiB repo慣例に加え、**公開transport（sandbox経由の単一push）の実用上限約1.2 MBを2026-11-16に観測**したため（bit 116のwhole cert 1,770,063 bytesは1.75 MiB慣例内だがtransport上限を超え、読み込み段階で16 MiB sandboxメモリ制限に到達）。assemble scriptのSPLIT_LIMITを変更して全4枚を2分割で再生成、manifestのper-part blob sha・receipts（md5/sha256/bytes/joined_equals_whole）でcat再構成を保証。
- 全枚: BigInt union 0/0（sub-roots全pass・terminals [13,17]）+ Bareiss全PASS の二重検証。root = child|1<<bit、D4-canonical、rows sorted-unique、root mobilityが合法候補と一致。
- 抽出driver `scripts/cert_driver65j.ts`（60c模倣・v16 engine）・組立/検証 `scripts/assemble_cost65j_certificates_20261116.py`（再実行でbits 112/118のparts/receiptsはbyte-identical再生成を確認済み）。
- **65f 13 receipts（bits 4,15,18,20,21,23,25,28,66,79,91,101,109）はpublished証明書なし**。blob-pin済みv15 raw batch記録 + corpus raw-vs-audit node-sum監査（`f44f9f3a`）+ canonical root verdict cache conflict-0 census（`2d090b49`/`7c99621f`）を証拠にfold（certified:falseと明記）。証明書抽出はoptional follow-up。

### 4. claim更新（v5）
`class2-lane-cost65j-inflight-20261115.json` → v5（**blob `7a4c900710e3ddb34fb9e272e8e673815e13a4f3`**・7,870 bytes）。schema・status更新 + fold section追加（前提修正・head前後・9行・zero-mim・証明書・UNKNOWN guard）。v4全field保持。

## 構造的事実

- **cross-cover receiptのmarginalはlane設計時点から失効し得る**: 63a bit-97 receiptは63a laneの動機とは無関係に本laneのchildを1行で閉じた。lane着手前に「目標行が現在headでopenか」を再確認する運用は既存だが、**sweep完了→foldの間にも他laneのfoldで前提が失効し得る**ため、fold scriptのassert（今回のdisjointness/child-remaining）が最終防壁として機能した。v1の失敗自体が監査の成功例。
- 同一positionが複数laneで独立にWIN7判定され、verdictが完全一致した（bits 25: 65f+72b、79: 65f+63a(bit-97)、91: 65f+72b、101: 65f+69i）。engine v15/v16・depth 10を跨ぐ一致で、verdict cache信頼性の追い証拠。
- 第3 class-2 target S5は「childのsweep」以前に、cross-coverを含む既存receiptsだけで完全閉鎖済みだった。**class-2 targetの残行計数は小さくても、その行をcoverする候補rootの大半が他laneで既に走っている可能性があり、着手前にfolded roots 718とのorbit重複census（今回script化）が最も安い前置検査になる**。
- solved 1419はmanifest被覆の簿記。WIN7証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。REFUTED-D10はLOSS証明ではない。

## 次の状況

- best coverable class-2 S5 `00000000000000801202000000200000` 3/209（65k/70j/74h STERILE行）は不変・open。70j cross-coverはcost-60隣接では失敗済み（bit 119 REFUTED）。65k最安隣接cost 64群・74h最安隣接cost 65が次候補。着手前に718+17=735 folded roots orbit重複censusを必ず実施。
- 69aは並走IN FLIGHT（着手禁止）。K0863 CI refreshは`45e558f3`で着地済み。
- 65f 13 WIN bitsの証明書抽出はoptional follow-up（最重量は既知nodes順に bit 21/20等、cost-64行を直接閉じた2枚が優先）。
- 11x11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。

## 出版完了（2026-11-16、別commit群）

証明書4枚（bits 112/116/118/119）の全8 partファイル・小ファイル一式がmainに着地した。**mainのdirectory listing（GitHub API）で全8 partのgit blob shaがmanifest `d4981d7e` のper-part pinと完全一致を確認**（bit112: `accb6823`/`697b8656`、bit116: `770b4a76`/`6c499b25`、bit118: `8862c7a6`/`6e84559e`、bit119: `e0377882`/`692477b1`）。

- `10b4a515`: 小ファイル一式（receipts script pin更新=claim v5 `7a4c9007`/manifest `d4981d7e`、assemble script SPLIT_LIMIT=1,200,000、fold JSON `e8c83584`、claim v5 rev2、cert receipts 116/119（blob `18d60560`/`c79e5bb3`・各1,246 bytes）、log）
- `aa5cef54`/`0312bcfa`: bit116 part1of2/part2of2
- `fada034f`/`4fbdbe9d`: bit118 part1of2/part2of2
- `5023ab6e`/`9d7b2854`: bit119 part1of2/part2of2
- （bit112 parts `b78bd87f`/`538a4866`・verify records `46b35bc4` は前commit群で着地済み）

**transport観測（実験事実）**: 16 MiB sandbox単一pushは、read_file chunk結合+push_files直列でもcontent約0.88 MB・1.27 MBでプログラム予算超過エラーを常に出すが、**push_files opが"done"記録されていればcommitは着地する**（全6 part pushで再現・失敗なし）。エラー後はlist_commits/directory listingで着地とblob sha照合を必ず行うこと。並走laneとの衝突なし（間に`9bfd18dc` candidate-A budget ladder 2/3が挟まったのみ・パス非交差）。

fold v2のremote-only独立検証は並走laneが`e202661b`で着地済み（2nd TS/BigInt実装）。
