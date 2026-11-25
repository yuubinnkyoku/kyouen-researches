# Part DG 宣言: batch-28 (class 5343) b28-win46 thirdimpl queue registry P3パッケージ8行 (aa052/aa044/aa041/aa048/aa026/aa039/aa043/aa045) 第三実装交叉検証

- 2026-11-24T05:11Z (declaration authoring time; commit timestampはGitHub側)
- 単一オーナー宣言・publish-then-execute。本宣言以降、下記scopeの作業は本レーンの単一オーナーが行う。
- 観測 HEAD-before-push: `26fc5352219252b661ae7bd01301fd1658c29de1` (2026-11-24T05:03:54Z・Part DF A2 sources 39。
  直前の `2245e85e` (05:03:24Z・Part DF A1)・`59b6540f` (05:01:52Z・Part DF宣言) からも本Part scopeは非接触)
- 実験dir: `research/experiments/n11-centralreply-closure-b28p3win8-thirdimpl-20261124/`

## 対象と非対象

- 対象: batch-28 (closure class 5343・54キー aa001..aa054) のうち、b28-win46 thirdimpl queue registry
  (実験 `n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124`・**REVISION 3** 出版
  `43932d74`・queue-registry.json `334f6209d0628cdf8f5c997e92bc5e5e63ae7f450345dc1a8393488941f1f6e9` /
  README-queue `4b20c6a0f98b399dcbfd86386134cab9d1258a7dbcb1690387dcb2f46d1a793e`) 上の **open 25 WIN行のうち
  P3パッケージ8行** (est昇順・registry packages P3): aa052 [1152921504606851072,4228] /
  aa044 [1152921521786716160,4228] / aa041 [1171516445255794688,8] / aa048 [1152921504615235584,4228] /
  aa026 [1171516445255794688,32] / aa039 [1152921504606846984,4228] / aa043 [1152921513196781568,4228] /
  aa045 [1152921642045800448,4228]。全て drive-4/drive-5 experiment
  (`n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123`) の 15M-probe (budget 15,000,000)
  で解決した honest WIN labels (rc=1・pinned nodes 8,976,982〜12,371,943・合計 **85,844,795**・
  est_crossimpl_2pass合計 **202,593,715**)。aa026 のみ drive-4 決定 (2026-11-23T18:06:17Z)・決定的2行
  (PASS/WIN-HALT) は drive-5 logでも byte同一 (cross-log二重正本)。残り7キーは drive-5 決定
  (aa041 19:01:10Z / aa039 18:57:46Z / aa043 19:04:21Z / aa044 19:07:39Z / aa045 19:08:16Z /
  aa048 19:14:28Z / aa052 19:21:40Z)。第三実装による verdict 一致 (三実装交叉検証: jsreplay runner系×2 +
  third_impl.js) と本host pinned-replica 2-pass fresh-cold (budget 15M) の node-exact 再現を検証する。
- 非対象: **Part DE (P1パッケージ8行・完了 `1eead030`)・Part CX (claimed5行5つ・完了 `46687096`)・
  Part DF (P2パッケージ8行・宣言 `59b6540f`・scaffold A1/A2出版済み) が対象とする行・kit・出版物に一切
  触れない**。P4パッケージ (aa011/aa054/aa022/aa034/aa037/aa032/aa028/aa021/aa050) と tier-L LOSS 7行
  (第三実装optional redundancy) も本宣言の外。adoption は行わない (verdict不消費)。
- 対抗宣言の機械確認: 観測HEADまでのrepo commit全列で「Part DG」は0件 (GitHub search_commits API機械確認
  total_count=0)・`research/log/2026-11-24-part-dg-b28p3win8-thirdimpl-{declaration,completion}.md` と
  実験dir `n11-centralreply-closure-b28p3win8-thirdimpl-20261124/` は共に未存在 (API個別確認)。
  registry rev3 で thirdimpl_claimed_win は 0・P3 8キーとも state=open・label=WIN・pinned nodes が機械一致、
  queue registry 自身は「どのpackageも予約しない」を明記。乱数・時刻に依存する実験はtrace内では全て決定的
  (pinned jsreplay)。

## 本レーンに固有の経緯 (誠実記録)

1. **P2 kit pre-emption incident (peer-laneとの重複回避)**: 本レーンは先に Part DF として P2パッケージ8行の
   kit を maker・audit・runner・sources・input まで準備したが、push 直前の最新main再取得で、並走レーンが
   `59b6540f` (05:01:52Z) で P2 scope の単一オーナー宣言を、`2245e85e` (05:03:24Z)・`26fc5352`
   (05:03:54Z) で scaffold/sources 出版を完了済みと判明した。よって P2 kit は**未出版のまま破棄**し
   (P2 draftの内容を1 byteも出版していない)、即座に P3 パッケージへ pivot した。未出版 P2 draftの
   DE適応delta群は本P3 kit製作に再利用した。
2. **registry rev3 pin修正 (出版前の検出)**: sources 取得時に取得経路で生じた余分なtrailing byteにより
   一時的に sha256 `38c1e7c6…` の queue-registry.json copy を保持していたが、出版正本 (commit
   `43932d74` 公開・observed HEAD `26fc5352` で再fetchし sha256 一致を確認) の
   `334f6209d0628cdf8f5c997e92bc5e5e63ae7f450345dc1a8393488941f1f6e9` と maker pin gate が一致しない
   ことを宣言前のmachine-checkで検出し、出版bytesで上書き・`PIN_QREG_JSON` を修正した
   (maker/auditの sha は修正後のものを本宣言でpin)。誤pinのまま出版・実行した事実はない。

## 事前登録 pin 群 (scaffold A1/A2 commitの内容)

scripts 7 (adapted 4 + pinned byte-clone 3):

- `make_inputs_dg.py` sha256 `d3fefbcae37de53700f9e58a08f95890c0267760ec0a211d1940ab1f01fcf917`
  (DE maker `b67b4d15` 適応系譜 (DF maker `a3c6e8e1` と同一派生)・targets P3 8行・registry rev3 pinは
  上記修正後。maker実行 ×2 **byte-stable PASS**・gates PASS)
- `audit_dg.py` sha256 `e3a1c74f88d1eb8061d9ee85622266194a3688a0d23fa575b18852b5c55f4be3`
  (CX audit `87152e94`・DE audit `a57e220c`・DF audit `76934660` と同一G-gate系譜からのadapt・
  target-count 8・P3-package文言・PIN_RAW_DG 16件・`.dg-host.out` suffix・registry-rev3 context note)
- `run_replica_dg.sh` sha256 `de1d1fbcddc4b8264622cd4db007fe756be70a70565b988d24c64b2140e1f9b1`
  (published DE runner `3e4263ccc9a309e749b4308d2fa71de49252e7f06f92efc3f85196c9b2e288a6` と比較して
  **header comment のみ rewritten**・`set -u` 以降のbodyはbyte不変 (diff機械確認)・budget 15Mも不変)
- `run_thirdimpl.sh` `a0b77d8330c696a5a7da2883d49110ae8703dc1673be10d3a9972ea53c885a41` (CW版byte-clone) /
  `third_impl.js` `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998` (pinned byte-clone) /
  `verify_tbl.js` `c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251` (pinned byte-clone) /
  `jsreplay.js` `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` (pinned byte-clone)

input 13: `rows.json` `22de9dd76e0647049c280a64a959c745fed578f9e9c13bc0ca3b3ea37a7ec531`
(schema `n11-centralreply-closure-b28p3win8-thirdimpl-input-v1`・maker 2回実行byte-stable) +
8 targets (aa026 `ea6a0309…` / aa039 `3fc74b00…` / aa041 `cad9fbe4…` / aa043 `8f75aec9…` /
aa044 `6c292559…` / aa045 `f8a22a39…` / aa048 `3f544138…` / aa052 `36213ee6…`) +
anchors k02a `b6174a3f…` / l1a `e13d2a6c…` + negatives ng1 `8e64b9ad…` / ng2 `f19cd5a3…` の
input CSV (publishedとbyte一致をmakerが機械検証)。

val-gate 8: at2m-s5-1152921504606851072-536870946×2 + at2m-s5-1188950301626860544-536870912×2 +
first/second-15m 各input+baseline (CW kitから不変再利用・inputs `ecc0299b…`/`56aacb71…`・
baselines `6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`)。**本Partではval-gate 8ファイルを
A1 scaffold commitにkit内filesとして出版し kitをself-containedにする** (CW/DE/DF kitでは
出版を必須としなかった点の、本Part固有の改善)。host出力は `.dg-host.out` として生成。

sources 39 (commit-pinned raw fetch・全sha本宣言のpin群と同一): raw 16 / published-input 8 /
published-input-bf 4 (k02a/l1a/ng1/ng2・Part BF chain byte-clone) / status-drive4.log
`598174447fa878c2e0a6d6db6f892c5c279063174d763746456476e3051633f8` (61行) / status-drive5.log
`ca1e98ccd952b29e8295147add50e6b4a3ff3732748bf544b9c3a7018d495df0` (109行) / batch-keys-b28.json
`af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5` / queue-registry.json (rev3)
`334f6209d0628cdf8f5c997e92bc5e5e63ae7f450345dc1a8393488941f1f6e9` / README-queue.md (rev3)
`4b20c6a0f98b399dcbfd86386134cab9d1258a7dbcb1690387dcb2f46d1a793e` / canonical-cache-co-merged-b28loss7.cache
`854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d` (6,301行) / increment-b28loss7.cache
`bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382` (7行) / increments-manifest-co.json
`b47e07ca90b0166d22c681a3136a60500d7a4f8671b1e77b656a1b34c7c02192` / canonical-cache-db-merged-b29loss37.cache
`04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556` (6,354行・現canonical chain head) /
increment-b29loss37.cache `85bd44693edfd862a7cf74fc10414978fcf248dcef684a821b487f9757b443cc` (37行) /
increments-manifest-db.json `1b51f30dabed6f4df435a3a034e1b5b9c2f405c75ebdcd918c0e256f2812d25a`。

raw 16 pins (決定ドライブ側正本):
aa026.p1 `a840e6adaff2fe7f6a75901af549a00dda2f6b4958e6fb4c99bcd4180053485e` /
aa026.p2 `0516453f389b2445dfd52dfd8f12b93e7d069c59001c27b1d1af0f14cd9b52fb` /
aa039.p1 `0ad0f4c908c08d4c167c2b06a5f4b9ab62e197280076d341c8029b4ca7a25f55` /
aa039.p2 `11b19ad3ad4b8f5868945af7b7149230053b8cbb568c5cfb83934f2d0e0784a07` /
aa041.p1 `27d4773048a16452e7c9376bc4c5471026fb9f6c4d5d9ed60f44c95a6493d13c` /
aa041.p2 `21b7d4a59256df3feb2f80f40732e116492514582a69a893034ce648790979ae` /
aa043.p1 `993a4c63efe12dcb9cea57487dcb5ac8ae28017d082df92be86a01c55c508e29` /
aa043.p2 `5e13b6a8e778ee5a769f426a35841cfecf3a468cfb76f7ef863247efddd99ea3` /
aa044.p1 `6dfeca0516f7cf669928cf8ee3bbd991bbf53ea8aa60aae13383dc8cd2e49a0a` /
aa044.p2 `1997e95d1d025db661a514c46f8bd69e9875e68bec01bd91511ae943e0facdab` /
aa045.p1 `7b26841abdda851f96b49799f6f27b69a93f774115cde6edb34c3afb18078931` /
aa045.p2 `390eac7d1bc99aa95d5001fac421ef696f3ad64192ad987a0099491f5c250327` /
aa048.p1 `476a4b69d2ac765fb33ea0349f970424220b9687a268959d0c4c099c436a54cc` /
aa048.p2 `c87a36bd88c4e82e325aca0373c81cdb3fd0d4948e021f1315d5ce7510a029c0` /
aa052.p1 `444c57061ddebad4e530fd132375f8e4c3089513c37d65c85e82530aa7434718` /
aa052.p2 `fa82d65af269be476a14d77b75281272a08ac5e2123c810327059b39b76443bd`。

## declared deltas (DE/DF maker-audit系譜からの、宣言時点で確定している差分)

1. targets: DE P1 / DF P2 8行 → **DG P3 8行** (drive-4/5 15M solved WIN行・est昇順・pinned nodes合計
   85,844,795・est 2-pass合計 202,593,715)。replica budget 15M 不変 (published drive probe条件)。
   **P2→P3 pivotに伴い、本makerは一度も出版されていないDF未発表稿を経由していない**: makerの直接の
   系譜は DE maker `b67b4d15` 適応 (P2→P3 targets差し替え + registry pin修正)。
2. status battery: drive4/drive5 両logの種別行数は DE/DFから不変 (drive-4 61行 PASS 31/WIN-HALT 18/
   EXHAUSTED 6/P1-TRUNCATED-RETRY 1/P2-TRUNCATED-RETRY 5・drive-5 109行 PASS 54/WIN-HALT 35/
   EXHAUSTED 11/P1-TRUNCATED-RETRY 1/P2-TRUNCATED-RETRY 7・既知junk行 `P1-FAIL ` 1行は非verdict)。
   決定的 PASS行 + WIN-HALT行をbattery化: aa026 18:06:17Z (drive-4決定) / aa041 19:01:10Z /
   aa039 18:57:46Z / aa043 19:04:21Z / aa044 19:07:39Z / aa045 19:08:16Z / aa048 19:14:28Z /
   aa052 19:21:40Z (drive-5決定7キー)。**cross-log gate (DF宣言の drive-4決定5キー版と対になる
   本Part版): drive-4決定のaa026は決定的2行が drive-5 logでもbyte同一であることを機械検証**。
3. queue registry battery: rev3 (`334f6209…`)。P3 keys == 8キー、各キー decisive row rc=1/budget 15M/
   nodes == pinned、thirdimpl state == open、state counts (win 46 / done 21 / claimed 0 / open 25)、
   P3 pinned_nodes_total 85,844,795 == sum of pinned nodes・est_crossimpl_2pass_total 202,593,715。
   README-queue 記述句 battery (P3 8行列挙・pinned計 85,844,795 nodes・verdict不消費・package不予約・
   11×11 UNKNOWN)。
4. unadopted battery (DE/DF adaptation継承・文言はP3-packageに): 8 targets は CO-time 15M solved
   WIN であるため、CO manifest の win_ids / unadopted_win_ids / node-exact unadopted_win_rows /
   probed_ids / resolved_ids への presence が必須で、exhausted_excluded_ids・loss_ids・
   adopted_loss_ids・already_adopted_ids・fragment_ids への absence が必須。現head証明はDE/DFと同一:
   DB merged cache (6,354行) にも CO cache (6,301行) にも対象行は存在しない (二重 verdict不消費 gate)・
   両 increment 行にも存在しない。三点一致 cross-artifact gate (drive decisive nodes == CO
   unadopted_win_rows nodes == queue registry pinned nodes) は8キー全てで機械検証済み (maker gates PASS)。
5. rules-gate: verify_tbl.js は pinned jsreplay (84585617 byte同一) を参照して TBL/Triples 一致を
   機械検証 (quads 95,670 / mismatches 0)。

## 事前実行済み (本宣言の前に行った機械検証・全部local)

- maker `make_inputs_dg.py` (修正後): gates PASS ×2 **byte-stable** (stdout同一)。
- tamper battery **8/8 捕捉・clean control PASS**: byte層 6/6 (T1 raw aa052.p1 nodes+1 → raw pin gate /
  T2 batch-keys aa052 legal+1 → batch-keys gate / T3 queue-registry P3 keys swap aa052→aa001 → qreg pin
  gate / T4 CO manifest loss_ids+aa052 → manifest gate / T5 DB cache forge行append → cache gate /
  T6 drive-5 aa052 WIN-HALT行削除 → status pin gate) は全て rc=1・期待ABORT文言で捕捉。
  semantic層 2/2 (scratch makerで該当pinのみ更新して実施): S-a qreg P3 swap aa052→aa001 は pin更新を
  通過した後に P3-package roster gate が rc=1 捕捉 / S-b CO manifest loss_ids+aa052 は pin更新を通過
  した後に unadopted loss_ids gate が rc=1 捕捉。復帰後 clean maker green (rc=0・stdout は事前の clean
  run と byte 一致)・kit全対象 sources sha が pinに復帰したことを事後照合。
- registry rev3 (`334f6209…`) と README-queue (`4b20c6a0…`) が観測HEAD `26fc5352` で byte 不変であること
  を commit-pinned raw fetch で機械確認済み (sha256再計算一致)。

## 実行protocol (宣言後・publish-then-execute・solver実行はこの後)

- D1: rules gate — `node scripts/verify_tbl.js` → `output/rules-gate.txt`
  (要 `replica quads 95670 mine quads 95670` + `mismatches 0`)。
- D2: val-gate fresh 4本 (budget 2M/2M/15M/15M・host出力 `val-gate/<key>.dg-host.out`)。
  published baseline と node-exact (wall_s以外全字段)。1本でも不一致 → hard-stop。
- D3: negatives ng1/ng2 → GATE_FAIL (`legal count mismatch` / `stone count mismatch`)。
  GATE_FAILでない → hard-stop。
- D4: anchors k02a/l1a a/b det-pair (expansions 9,106,337 / 7,660,202・ttHits 4,991,527 / 3,951,175 は
  published pin と一致必須)。不一致 → hard-stop。
- D5: replica 8キー×2-pass fresh-cold (budget 15M・`run_replica_dg.sh`・inner timeout 260・
  1キー1 invocation・pass分離を許可・4並列上限)。p1==p2 determinism + published raw (PIN_RAW_DG) と
  result/nodes 一致 (node-exact)。不一致 → hard-stop・記録。
- D6: third-impl targets 8キー×2 run (a/b・`run_thirdimpl.sh`)。det-pair + verdict agree
  (expect WIN=1)。third-impl node数は実装依存のため pinned nodes との直接比較はしない
  (verdict一致のみ主張)。
- D7: audit `audit_dg.py` ×3 byte-identical (stdout + output/audit-summary.json)。
  ALL GATES PASS 必須。1 gate でも FAIL → 成果はFAILとして記録・出版 (押し通さない)。
- D8: audit tamper battery 4種 (replica raw nodes+1 → verdict-vs-published gate / target third-impl
  result反転 → det-pair or verdict-agree gate / anchor expansions改竄 → anchor gate / rows.json
  replica_nodes改竄 → verdict gate)。全捕捉と復帰greenをlogに記録。
- D9: 出版 B (outputs: status.log / targets 16 / anchors 4 / negative 2 / replica 16 / val-gate host 4 /
  rules-gate / audit-summary + audit runログ×3) → C (README最終 + MANIFEST-sha256) → 完了log
  (`research/log/2026-11-24-part-dg-b28p3win8-thirdimpl-completion.md`)。fetch-back byte検証を全出版物に
  実施。**queue registry rev4 bookkeeping (P3 8行 claimed→done) はDF executor側のP2反映更新と
  競合する可能性があるため、実行時点の最新registry状態を確認し、競合時は更新を見送り状況を記録して
  次回合流とする** (bookkeeping-only・verdict不消費)。

## stop rules

- いずれかの gate で GATE FAIL または MISMATCH → その時点で実行停止し、観測を誠実に記録して
  出版 (verdict不消費)。D5 の p1/p2 不一致・published との不一致は chain 訂正レーン候補の
  証拠として保存。
- third-impl runlimit (wall-inconclusive) → そのキーは honest record (NOT a verdict)・
  再実行は別declaration。
- 実行環境リセット等のインフラ事故 → published scaffold から kit復元して sha検証の上やり直し
  (published evidence だけが証拠の設計)。
- 対象8キーの第三実装verdictがpublished WINと一致しない場合 → **採用も被覆も一切行わず**
  divergence証拠として記録 (three-implementation corroboration不成立の誠実報告)。
- push競合・同時書き込み・取得失敗 → 無理に押し進めず状況を記録して次回実行に回す。

## 主張の限定

- 本Partは交叉検証のみ。**verdict不消費**: 対象8行は honest WIN labels のままで、adoptionは
  scrutiny owner C++第二実装 gate `9193f5b6…` 通過後、pinned merger `90711961…` 経由の別adoption
  Part 専権。
- 閉鎖・被覆・secured・root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 (54キーすべて・P3の8キー含む) は本Partの前後を通じてすべてUNKNOWNのまま。**
  nodes数・expansions数・ttHits数を勝敗や距離として読まない。
