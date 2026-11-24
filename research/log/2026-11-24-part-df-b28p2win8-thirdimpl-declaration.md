# Part DF 宣言: batch-28 (class 5343) b28-win46 thirdimpl queue registry P2パッケージ8行 (aa014/aa049/aa051/aa019/aa013/aa020/aa010/aa040) 第三実装交叉検証

- 2026-11-24T05:0xZ (declaration authoring time; commit timestampはGitHub側)
- 単一オーナー宣言・publish-then-execute。本宣言以降、下記scopeの作業は本レーンの単一オーナーが行う。
- 観測 HEAD-before-push: `aebb22011cb47e2e993d5a99cad4a9e522b42462` (2026-11-24T05:00:11Z・K1281 README append。
  直前観測 `5d914700` (04:57:48Z・K1281 knowledge昇格) からも本Part scopeは非接触変化なし)
- 実験dir: `research/experiments/n11-centralreply-closure-b28p2win8-thirdimpl-20261124/`

## 対象と非対象

- 対象: batch-28 (closure class 5343・54キー aa001..aa054) のうち、b28-win46 thirdimpl queue registry
  (実験 `n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124`・**REVISION 3** 出版
  `43932d74`・queue-registry.json `334f6209…` / README-queue `4b20c6a0…`) 上の **open 25 WIN行のうち
  P2パッケージ8行** (est昇順): aa014 [1171516445255811072,0] / aa049 [1152921504623624192,4228] /
  aa051 [1152921504673955840,4228] / aa019 [1171516445322903552,0] / aa013 [1171516445255802880,0] /
  aa020 [1171516453845729280,0] / aa010 [1171516445255794720,0] / aa040 [1152921504606846992,4228]。
  全て drive-4/drive-5 experiment
  (`n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123`) の 15M-probe (budget 15,000,000)
  で解決した honest WIN labels (rc=1・pinned nodes 7,263,370〜8,916,641・合計 **64,713,638**・
  est_crossimpl_2pass合計 152,724,187)。aa010/aa013/aa014/aa019/aa020 は drive-4決定、
  aa040/aa049/aa051 は drive-5決定 (各targetの決定ドライブ側rawが正本)。
  第三実装による verdict 一致 (三実装交叉検証: jsreplay runner系×2 + third_impl.js) と本host
  pinned-replica 2-pass fresh-cold (budget 15M) の node-exact 再現を検証する。
- 非対象: **Part DE (P1パッケージ・完了 `1eead030`)・Part CX (claimed5行・takeover完了 `46687096`)
  が交叉検証した16行には一切触れない**。P3/P4パッケージは本宣言の外。adoption は行わない
  (verdict不消費)。
- 対抗宣言の機械確認: 観測HEADまでの commit 列・log/experiments dir一覧で scope と交差する
  単一オーナー宣言は存在しない (「Part DF」は repo commit 全列で0件・API機械確認。CX完了後の
  registry rev3 で thirdimpl_claimed_win は 0・8行とも state=open・label=WIN・pinned nodes が
  機械一致、queue registry 自身は「どのpackageも予約しない」を明記)。乱数・時刻に依存する
  実験はtrace内では全て決定的 (pinned jsreplay)。

## 事前登録 pin 群 (scaffold A commitの内容)

scripts 6 (adapted 3 + pinned byte-clone 3):

- `make_inputs_df.py` sha256 `a3c6e8e15f0ffa2a7819824c9721ec6c54b5be6a613278a7f40fc811e69d41c7`
  (DE maker `b67b4d15` 適応・適応時に DE由来の残留参照 `QREG_P1_TOTAL` → `QREG_P2_TOTAL` (1箇所・
  ABORT文言含む) を修正、それ以外は declared deltas のみ。maker実行 ×2 **byte-stable PASS**・
  gates PASS・rows.json `e184c50bc62c39aee0dc13b80fa4caecb6aa943ecd4d89996084d8bfdfbb8e8a`)
- `run_replica_df.sh` sha256 `73f09f38b3f53b4e77907a6867d9f9bc4bd44fb47e8adf97e965b27c469d4ec8`
  (published DE runner `3e4263cc` と比較して **header comment のみ rewritten**・set -u 以降のbodyは
  byte不変 (機械確認)・budget 15Mも不変)
- `run_thirdimpl.sh` sha256 `a0b77d8330c696a5a7da2883d49110ae8703dc1673be10d3a9972ea53c885a41` (CW版byte-clone)
- `third_impl.js` `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998` (pinned byte-clone)
- `verify_tbl.js` `c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251` (pinned byte-clone)
- `jsreplay.js` `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` (pinned byte-clone)
- `audit_df.py` は本宣言後・solver実行前に scaffold として出版し、その sha256をscaffoldの
  README/MANIFEST に固定する (本宣言時点では maker pin群のみ先行固定。これは DE/CXと異なる点で、
  auditは CX audit `87152e94`・DE audit `a57e220c` の同一G-gate系譜からのadaptで、
  target-count 8・P2-package文言・PIN_RAW_DF 16件・`.df-host.out` suffix への差分は宣言済みである)。

input 13: rows.json (上記 sha・schema `n11-centralreply-closure-b28p2win8-thirdimpl-input-v1`) +
8 targets + anchors k02a/l1a + negatives ng1/ng2 の input CSV (publishedとbyte一致をmakerが機械検証)。

sources 39 (commit-pinned raw fetch・全sha本宣言のpin群と同一・raw 16 + published-input 8 +
published-input-bf 4 + top-level 11): raw 16 (8キー×p1/p2・後述) / published-input 8 /
published-input-bf 4 (k02a/l1a/ng1/ng2・Part BF chain byte-clone) / status-drive4.log
`598174447fa878c2e0a6d6db6f892c5c279063174d763746456476e3051633f8` (61行・PASS 31/WIN-HALT 18/
EXHAUSTED 6/P1-TRUNCATED-RETRY 1/P2-TRUNCATED-RETRY 5) / status-drive5.log
`ca1e98ccd952b29e8295147add50e6b4a3ff3732748bf544b9c3a7018d495df0` (109行・PASS 54/WIN-HALT 35/
EXHAUSTED 11/P1-TRUNCATED-RETRY 1/P2-TRUNCATED-RETRY 7/既知junk行 `P1-FAIL ` 1行は非verdict・
battery除外) / batch-keys-b28.json
`af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5` / queue-registry.json (rev3)
`334f6209d0628cdf8f5c997e92bc5e5e63ae7f450345dc1a8393488941f1f6e9` / README-queue.md (rev3)
`4b20c6a0f98b399dcbfd86386134cab9d1258a7dbcb1690387dcb2f46d1a793e` /
canonical-cache-co-merged-b28loss7.cache
`854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d` (6,301行) /
increment-b28loss7.cache `bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382` (7行) /
increments-manifest-co.json `b47e07ca90b0166d22c681a3136a60500d7a4f8671b1e77b656a1b34c7c02192` /
canonical-cache-db-merged-b29loss37.cache
`04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556` (6,354行・現canonical chain
head) / increment-b29loss37.cache
`85bd44693edfd862a7cf74fc10414978fcf248dcef684a821b487f9757b443cc` (37行) /
increments-manifest-db.json `1b51f30dabed6f4df435a3a034e1b5b9c2f405c75ebdcd918c0e256f2812d25a`。

raw 16 pins (決定ドライブ側):
aa010.p1 `46ad686fcdf168a21c3092c51a914d58278810350ac88133383b4a667a9dda3f` /
aa010.p2 `583e384ae8a89bd39b2107814aa658d6dd0087f514819a458666c4332e2daf50` /
aa013.p1 `46364e9b15d04f69a9a7c70920c7e60f4a137ce336c50db6da0b1db4b9339a7c` /
aa013.p2 `b808f09ee700f3ffd82b0afd9e9ce5c844f4b910e85260ef429671cafe47b9d0` /
aa014.p1 `376e9f9247b4921ef317dcb0863ef8007e836787d6c0e2a43ab72f0bcffbb04e` /
aa014.p2 `552b04a28e818992ad7e4e431ca2436b7918b7e1cff8e21f417a3c23fe69ca84` /
aa019.p1 `6756b354bc9d7d7549f569a74cf4f159a9d1685d94ee87a99be8d94d8d46d50f` /
aa019.p2 `9928b935a176b5358141ecfb22688d402106433b0f11ed7a95f4e7bef139901c` /
aa020.p1 `8a9f52cb5bef1e0c96fb6de086219c4d951cbe3f5d163e0a2be71ba80d71fc83` /
aa020.p2 `23f7ab72be0eb460657c0a23cdc21796bc33eec0cbb4b2ac0ff1836bd4553e28` /
aa040.p1 `b39ae7d69d25742b15f90fb2b1b05f301bfb475eea0c881f65fd7a0cab68880b` /
aa040.p2 `30b2c76bd013c007851cf5d16eedb612429e2dcb689e9ad1ba1022edebaa0cbb` /
aa049.p1=p2 `b9680389f3f51c87fd98c16895845e4c14ffec98a4d0e3db692508c9944ef377` /
aa051.p1=p2 `297a5ecbcf1b75b4eff730c97ee91bf00dfa5a2bbbbc046c58d3acd3676ff9c1`。

input pins: aa010 `57d26666de50eef29c2e50f077ada80d88757aa4abce258a8b4ed4f05defa262` /
aa013 `72799af6218b8df6451c3e2a952697aed02bed683baed709605020600c934be3` /
aa014 `759bc705b8be234a7799b890a2ee2a16dd99b057a950cad05e106a1a679f9283` /
aa019 `09def748c9625cf2d95b4fcdeda2bc71512e7f1300c3783adda0c97ebbbb65c2` /
aa020 `415df65147d625fbc3013cc538c027e527f3c8ca94489c2c45a1976a6c1443df` /
aa040 `96c6de4d970ba19e916948c2ef17079dcd7cd7e2eb29af3431537737f2eb26a3` /
aa049 `4c9dd91cc9d9666f4da2c7374820f2ed9a587a343c3fad03bdadc744683e2b1e` /
aa051 `9e46be8be959b92ed02402921e4777d62b7b0d5f4cf340f22750faa861e58e96`。
k02a `b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887` /
l1a `e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a` (anchors・published anchor
CSVとbyte一致) / ng1 `8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09` /
ng2 `f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc` (negatives・Part BF chain
byte一致)。

val-gate 8 (CW kit不変再利用・at2m-s5-1152921504606851072-536870946×2・
at2m-s5-1188950301626860544-536870912×2・first/second-15m 各input+baseline・
shaはmaker PIN_VALGATE がverify): input `ecc0299b…`/`56aacb71…`・baselines `6e902ab1…`/
`eeafe3ac…`/`8035fe54…`/`91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814966de1fb`。

## declared deltas (DE maker b67b4d15/-audit a57e220c からの、宣言時点で確定している差分)

1. targets: DE P1 8行 → **DF P2 8行** (drive-4/5 15M solved WIN行・est昇順・pinned nodes合計
   64,713,638・est 2-pass合計 152,724,187)。replica budget 15M 不変 (published drive probe条件)。
2. status battery: drive4/drive5 両logの種別行数は DEから不変。決定的 PASS行 (timestamp込みの正確な
   行文字列をpin) + WIN-HALT行をbattery化: aa010 17:45:22Z/aa013 17:48:22Z/aa014 17:50:43Z/
   aa019 17:54:40Z/aa020 17:57:42Z (drive-4)、aa040 19:00:53Z/aa049 19:13:52Z/aa051 19:17:09Z
   (drive-5)。**cross-log gate (DF新規・宣言済み)**: drive-4決定の5キー (aa010/aa013/aa014/aa019/
   aa020) は決定的2行が drive-5 logでもbyte同一であることを機械検証 (両ドライブが同じ行を報告した
   ことの二重正本化)。
3. queue registry battery: rev3 (`334f6209…`)。P2 keys == 8キー、各キー decisive row rc=1/
   budget 15M/nodes == pinned、thirdimpl state == open、state counts (win 46 / done 21 /
   claimed 0 / open 25)、P2 pinned_nodes_total 64,713,638 == sum of pinned nodes・
   est_crossimpl_2pass_total 152,724,187。README-queue 記述句 battery (P2 8行列挙・
   pinned計 64,713,638 nodes・verdict不消費・package不予約・11×11 UNKNOWN)。
4. unadopted battery (DE adaptation継承・文言はP2-packageに): 8 targets は CO-time 15M solved
   WIN であるため、CO manifest の win_ids / unadopted_win_ids / node-exact unadopted_win_rows
   (result 1・pinned nodes・two_pass_node_exact true) / probed_ids / resolved_ids への presence が
   必須で、exhausted_excluded_ids・loss_ids・adopted_loss_ids・already_adopted_ids・fragment_ids
   への absence が必須。現head証明はDEと同一: DB merged cache (6,354行) にも CO cache (6,301行)
   にも対象行は存在しない (二重 verdict不消費 gate)・両 increment 行にも存在しない・batch-29 scope
   の DB manifest 全文に対象キーidは出現しない。三点一致 cross-artifact gate (drive decisive
   nodes == CO unadopted_win_rows nodes == queue registry pinned nodes) は8キー全てで機械検証済み
   (maker gates PASS)。
5. rules-gate: verify_tbl.js はローカル knowledge lane kit の jsreplay (84585617 byte同一) を参照
   して TBL/Triples 一致を機械検証 (quads 95,670 / mismatches 0)。

## 事前実行済み (本宣言の前に行った機械検証・全部local)

- maker `make_inputs_df.py`: gates PASS ×2 **byte-stable** (stdout同一・rows.json `e184c50b…`
  両回byte一致)。tamper後の修復分 (QREG_P2_TOTAL fix) を含む最終makerに対して実施。
- maker tamper battery **15/15 捕捉・clean control PASS・kit inventory不変**:
  byte層 B1-B10 (raw p1 nodes+1 / drive-4 decisive nodes+1 / drive-5 WIN-HALT行削除 /
  batch-keys legal+1 / CO increment forge行追記 / CO manifest loss_idsへaa014追記 / DB manifest
  全文へaa019出現 / DB cache forge行追記 / queue-registry P2 keys swap (aa010→aa001) /
  README-queue 計数文言+1) は全てsource sha pin層でrc=1捕捉。semantic層 S1-S5 (同一変異を
  scratch maker内でpin更新して実施): raw nodes改竄 → 2-pass determinism gate / drive-4
  decisive行改竄 → decisive-line gate / CO manifest loss_ids追記 → loss_ids gate / DB cache
  forge → s5verdict行数 gate / qreg P2 swap → P2 roster gate、全てrc=1捕捉・期待文言一致。
  復帰後 clean maker green (rc=0)・kit全ファイル sha 不変を事後照合。
- registry rev3 (`334f6209…`) と README-queue (`4b20c6a0…`) が観測HEAD `5d914700` で byte不変
  であることを commit-pinned raw fetch で機械確認済み。

## 実行protocol (宣言後・publish-then-execute・solver実行はこの後)

- D1: rules gate — `node scripts/verify_tbl.js` → `output/rules-gate.txt`
  (要 `replica quads 95670 mine quads 95670` + `mismatches 0`)。
- D2: val-gate fresh 4本 (budget 2M/2M/15M/15M・host出力 `val-gate/<key>.df-host.out`)。
  published baseline と node-exact (wall_s以外全字段)。1本でも不一致 → hard-stop。
- D3: negatives ng1/ng2 → GATE_FAIL (`legal count mismatch` / `stone count mismatch`)。
  GATE_FAILでない → hard-stop。
- D4: anchors k02a/l1a a/b det-pair (expansions 9,106,337 / 7,660,202・ttHits 4,991,527 /
  3,951,175 は published pin と一致必須)。不一致 → hard-stop。
- D5: replica 8キー×2-pass fresh-cold (budget 15M・`run_replica_df.sh`・inner timeout 260・
  1キー1 invocation・pass分離を許可)。p1==p2 determinism + published raw (PIN_RAW_DF) と
  result/nodes 一致 (node-exact)。不一致 → hard-stop・記録。
- D6: third-impl targets 8キー×2 run (a/b・`run_thirdimpl.sh`)。det-pair + verdict agree
  (expect WIN=1)。third-impl node数は実装依存のため pinned nodes との直接比較はしない
  (verdict一致のみ主張)。
- D7: audit `audit_df.py` ×3 byte-identical (stdout + output/audit-summary.json)。
  ALL GATES PASS 必須。1 gate でも FAIL → 成果はFAILとして記録・出版 (押し通さない)。
- D8: audit tamper battery 4種 (replica raw nodes+1 → verdict-vs-published gate /
  target third-impl result反転 → det-pair or verdict-agree gate / anchor expansions改竄 →
  anchor gate / rows.json replica_nodes改竄 → verdict gate)。全捕捉と復帰greenをlogに記録。
- D9: 出版 B (outputs: status.log / targets 16 / anchors 4 / negative 2 / replica 16 / val-gate
  host 4 / rules-gate / audit-summary + audit runログ×3) → C (README最終 + MANIFEST-sha256) →
  完了log (`research/log/2026-11-24-part-df-b28p2win8-thirdimpl-completion.md`) →
  queue registry rev4 bookkeeping (P2 8行 thirdimpl claimed→done・done 21→29・claimed→0・
  open 25→17・rev3→rev4の純bookkeeping更新)。fetch-back byte検証を全出版物に実施。

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
  class 5343 (54キーすべて・P2の8キー含む) は本Partの前後を通じてすべてUNKNOWNのまま。**
  nodes数・expansions数・ttHits数を勝敗や距離として読まない。
