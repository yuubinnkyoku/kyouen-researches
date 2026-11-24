# Part DE 宣言: batch-28 (class 5343) b28-win46 thirdimpl queue registry P1パッケージ8行 (aa046/aa016/aa025/aa033/aa027/aa038/aa012/aa042) 第三実装交叉検証

- 2026-11-24T03:11Z (declaration authoring time; commit timestampはGitHub側)
- 単一オーナー宣言・publish-then-execute。本宣言以降、下記scopeの作業は本レーンの単一オーナーが行う。
- 観測 HEAD-before-push: `ae589e1859bbd8f49ee5018f430575b775d81de6` (2026-11-24T03:01:52Z)
- 実験dir: `research/experiments/n11-centralreply-closure-b28p1win8-thirdimpl-20261124/`

## 対象と非対象

- 対象: batch-28 (closure class 5343・54キー aa001..aa054) のうち、b28-win46 thirdimpl queue registry
  (実験 `n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124`・出版 `69e391a3`)
  上の **open 33 WIN行のうち P1パッケージ8行** (est昇順): aa046 [1152921779484753920,4228] /
  aa016 [1171516445255860224,0] / aa025 [1171516720133701632,0] / aa033 [1171516445255794688,128] /
  aa027 [1171516445255794688,64] / aa038 [1152921504606849024,4228] / aa012 [1171516445255798784,0] /
  aa042 [1152921504606847008,4228]。全て drive-4/drive-5 experiment
  (`n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123`) の 15M-probe (budget 15,000,000)
  で解決した honest WIN labels (rc=1・pinned nodes 2,185,149〜5,800,791・合計 31,778,254)。
  第三実装による verdict 一致 (三実装交叉検証: jsreplay runner系×2 + third_impl.js) と本host
  pinned-replica 2-pass fresh-cold (budget 15M) の node-exact 再現を検証する。
- 非対象: claimed 5行 (aa005/aa030/aa031/aa047/aa053・Part CX 宣言 `1300c10d`) には**一切触れない**
  (CX outputs は現時点で未出版・takeover規約時刻 2026-11-24T04:19:31Z 未到達のため再取得も不可)。
  P2/P3/P4パッケージは本宣言の外。adoption は行わない (verdict不消費)。
- 対抗宣言の機械確認: 観測HEADまでの commit 列で scope と交差する単一オーナー宣言は存在しない
  (Part CX は claimed5のみ・Part DC は batch-29・K1278 は strip理論)。queue registry 自身は
  「どのpackageも予約しない」を明記しており、本宣言がそれに従う最初の P1 package 実施宣言である。

## 事前登録 pin 群 (scaffold A commitの内容)

scripts 7 (adapted 4 + pinned byte-clone 3):

- `make_inputs_de.py` sha256 `b67b4d151887ba8661713f72f4ce6226b31dfea44e1563906d9fb199bdc78802`
  (CX maker 7abf48c5 適応・宣言済みdeltaは下記「declared deltas」・maker実行 ×2 byte-stable 確認済み)
- `audit_de.py` sha256 `a57e220c06465c519585911a3fb5dee7ec7e9a580164fd72265300c3a2773ccf`
  (CX audit 87152e94 適応・G6 id-list battery の batch-28 WIN targets への
  declared DE adaptation を含む)
- `run_replica_de.sh` sha256 `3e4263ccc9a309e749b4308d2fa71de49252e7f06f92efc3f85196c9b2e288a6`
  (published CX runner 6d05701c との non-comment diff は budget 20M→15M の1行のみ・機械diff確認済み)
- `run_thirdimpl.sh` sha256 `a0b77d8330c696a5a7da2883d49110ae8703dc1673be10d3a9972ea53c885a41` (CW版byte-clone)
- `third_impl.js` `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998` (pinned byte-clone)
- `verify_tbl.js` `c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251` (pinned byte-clone)
- `jsreplay.js` `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` (pinned byte-clone)

input 13: rows.json (maker 2回実行byte-stable)
`ce3d562b90e4a53ef0e442cf7aa091d3a50aeed230794ea89cc74b785b5c5b83`
(schema `n11-centralreply-closure-b28p1win8-thirdimpl-input-v1`) + 8 targets + anchors k02a/l1a +
negatives ng1/ng2 の input CSV (publishedとbyte一致をmakerが機械検証)。

sources 41 (commit-pinned raw fetch・全sha本宣言のpin群と同一):
raw 16 (8キー×p1/p2: 決定ドライブ側の正本) / published-input 8 /
published-input-bf 4 (k02a/l1a/ng1/ng2・Part BF chain byte-clone) / status-drive4.log
`598174447fa878c2e0a6d6db6f892c5c279063174d763746456476e3051633f8` (61行) /
status-drive5.log `ca1e98ccd952b29e8295147add50e6b4a3ff3732748bf544b9c3a7018d495df0` (109行・junk行
`P1-FAIL ` 1行は既知非verdict行としてbattery除外) / batch-keys-b28.json
`af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5` /
queue-registry.json `8c4216c68366c6a63e426ee36234b68955ef6f3a873429b0baa207f6dfc66592` /
README-queue.md `00d1062ec195362575dcfa19289b5b49d690dbc48cf808af39fac5abf91ba213` /
canonical-cache-co-merged-b28loss7.cache
`854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d` (6,301行) /
increment-b28loss7.cache
`bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382` (7行) /
increments-manifest-co.json
`b47e07ca90b0166d22c681a3136a60500d7a4f8671b1e77b656a1b34c7c02192` /
canonical-cache-db-merged-b29loss37.cache
`04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556` (6,354行・現canonical chain head) /
increment-b29loss37.cache
`85bd44693edfd862a7cf74fc10414978fcf248dcef684a821b487f9757b443cc` (37行) /
increments-manifest-db.json
`1b51f30dabed6f4df435a3a034e1b5b9c2f405c75ebdcd918c0e256f2812d25a`。

raw 16 pins (決定ドライブ側):
aa012.p1 `5de8cab7c5aab351891fc54ec502db20b04c4aabcf2cc4e943595835270419af` /
aa012.p2 `298c3e4554a5cdeea778d5607e6bc7de897bd15831ec6613477364ca351f6f85` /
aa016.p1 `944d0283d65dd0da83a935e334bd84d0648d03e23a60a22a187989295348a46e` /
aa016.p2 `15a3aed9e5472cadd0c68b6e83ae2745708308110971cdbece890ff2879874f3` /
aa025.p1 `bcb1255792373b1a7c6bc6320b72d10d09b297be85db7f9ecbd71d3bcc1e3644` /
aa025.p2 `b13e30bbfd12ee629e03a33876c8f00d844a94a564daae4a4f833154a6c40086` /
aa027.p1 `82c83500334ab8e8417a499da181f75735b4e32b4d556ec1796fef0a3a1e98ff` /
aa027.p2 `b4ca598493e901d84f7a02037bd38625cc9034a094c5c6017eb8aa37687b860e` /
aa033.p1 `6c17ed481989b4059131e06c8e1a477d5619a14b986aa73346e5e081d2bd29c9` /
aa033.p2 `6c17ed481989b4059131e06c8e1a477d5619a14b986aa73346e5e081d2bd29c9` /
aa038.p1 `af554be977777d080160f70eb0234f4036c4aceb204a99a1349e16f5413d6e6e` /
aa038.p2 `be48f875fb572fd6976a80754932226e1e5da08bb8435c19544754c296f561d6` /
aa042.p1 `539da11ffe1d9c604d04d63795bf18960742fdf958a28679e5dcdf681fef97a5` /
aa042.p2 `539da11ffe1d9c604d04d63795bf18960742fdf958a28679e5dcdf681fef97a5` /
aa046.p1 `002812fb2b2583b134516cc69745d67df0ac9b24604b3c4fe0d5d0ec5d13ec2b` /
aa046.p2 `f9787a6bb4171e56d54e0bcee8314d37e43edc60ee6ac4ec85db9617b154c445`。

val-gate 8 (CW kit不変再利用・shaはmakerがverify):
at2m-s5-1152921504606851072-536870946.input.csv
`ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348` /
at2m-s5-1152921504606851072-536870946.published-baseline.out
`6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c` /
at2m-s5-1188950301626860544-536870912.input.csv
`56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62` /
at2m-s5-1188950301626860544-536870912.published-baseline.out
`eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24` /
first-15m-s5-1152921504606851072-536870946.input.csv (同上input sha) /
first-15m-s5-1152921504606851072-536870946.published-baseline.out
`8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591` /
second-15m-s5-1188950301626860544-536870912.input.csv (同上input sha) /
second-15m-s5-1188950301626860544-536870912.published-baseline.out
`91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb`。

## declared deltas (CX 7abf48c5/-audit 87152e94 からの、宣言時点で確定している差分)

1. targets: CX claimed5 (CQ 20M再probe行) → DE P1 8行 (drive-4/5 15M solved WIN行)。replica budget
   gate 20000000 → 15000000 (published drive probe 条件)。
2. status battery: status-cq.log (25行) → status-drive4.log (61行) + status-drive5.log (109行)。
   drive4: PASS 31 / WIN-HALT 18 / EXHAUSTED 6 / P1-TRUNCATED-RETRY 1 / P2-TRUNCATED-RETRY 5。
   drive5: PASS 54 / WIN-HALT 35 / EXHAUSTED 11 / P1-TRUNCATED-RETRY 1 / P2-TRUNCATED-RETRY 7 /
   既知junk行 `P1-FAIL ` 1 (非verdict・除外)。各targetの決定的 PASS行 (timestamp込みの正確な行文字列を
   pin) + WIN-HALT行をbattery化。aa012/aa016/aa025/aa027 は両ドライブlogでbyte同一行 (cross-log gate)。
3. queue registry battery (新規): P1 keys == 8キー、各キー decisive row rc=1/budget 15M/nodes ==
   pinned、thirdimpl state == open、state counts (win 46 / done 8 / claimed 5 / open 33)、
   P1 pinned_nodes_total 31,778,254 == sum of pinned nodes。
4. unadopted battery (DECLARED DE adaptation): CX では targets は CO-time EXHAUSTED だったため
   exhausted_excluded_ids 内 presence が正しい姿だったが、DE targets は **CO-time で 15M solved WIN**
   であるため逆になる: targets は CO manifest の win_ids / unadopted_win_ids / node-exact
   unadopted_win_rows (result 1・pinned nodes・two_pass_node_exact true) / probed_ids /
   resolved_ids に presence が必須で、exhausted_excluded_ids・loss_ids・adopted_loss_ids・
   already_adopted_ids・fragment_ids への absence が必須。加えて新しい現head証明: DB merged
   cache (6,354行・04b0a239) にも CO cache (6,301行・854800f3) にも対象行は存在しない (二重
   verdict不消費 gate)、両 increment 行にも存在しない、batch-29 scope の DB manifest 全文に
   対象キーidは出現しない。さらに drive decisive nodes == CO unadopted_win_rows nodes ==
   queue registry pinned nodes の三点一致 cross-artifact gate。
5. rules-gate: verify_tbl.js はローカル knowledge lane kit の jsreplay (84585617 byte同一) を参照
   して TBL/Triples 一致を機械検証 (quads 95,670 / mismatches 0)。

## 事前実行済み (本宣言の前に行った機械検証・全部local)

- maker `make_inputs_de.py`: gates PASS ×2 byte-stable (stdout同一)。
- maker tamper battery **14/14 捕捉・復帰green**:
  byte層 T1-T9 (raw nodes改竄 / drive4 nodes改竄 / drive5 WIN-HALT行削除 / batch-keys s5_index改竄 /
  CO incrementへのforge行追記 / CO manifest loss_idsへaa046追記 / DB manifestへのaa046出現 /
  queue-registry P1 keys swap / DB cacheへのforge行追記) は全てsource sha pin層でrc=1捕捉。
  semantic層 S1-S5 (同一変異をpin更新して実施): raw nodes改竄 → parse_raw gate / drive4 decisive行
  改竄 → decisive-line gate / CO manifest loss_ids追記 → loss_ids gate / DB cache forge →
  row-count gate / qreg P1 swap → P1 roster gate、全てrc=1捕捉。復帰後 maker green (rc=0)。
  battery後 maker sha が battery前と同一 (b67b4d15) であることを確認。

## protocol (publish-then-execute・D1-D9)

- D1: rules gate — `node scripts/verify_tbl.js` → `output/rules-gate.txt`
  (要 `replica quads 95670 mine quads 95670` + `mismatches 0`)。
- D2: val-gate fresh 4本 (budget 2M/2M/15M/15M・host出力 `val-gate/<key>.de-host.out`)。
  published baseline と node-exact (wall_s以外全字段) であること。1本でも不一致 → hard-stop。
- D3: negatives ng1/ng2 → GATE_FAIL (`legal count mismatch` / `stone count mismatch`)。GATE_FAILで
  ない → hard-stop。
- D4: anchors k02a/l1a a/b det-pair (expansions 9,106,337 / 7,660,202・ttHits 4,991,527 /
  3,951,175 は published pin と一致必須)。不一致 → hard-stop。
- D5: replica 8キー×2-pass fresh-cold (budget 15M・`run_replica_de.sh`)。p1==p2 determinism +
  published raw (PIN_RAW_DE) と result/nodes 一致 (node-exact)。不一致 → hard-stop・記録。
- D6: third-impl targets 8キー×2 run (a/b・`run_thirdimpl.sh`)。det-pair + verdict agree
  (expect WIN=1)。third-impl node数は実装依存のため pinned nodes との直接比較はしない
  (verdict一致のみ主張)。
- D7: audit `audit_de.py` ×3 byte-identical (stdout + output/audit-summary.json)。
  ALL GATES PASS 必須。1 gate でも FAIL → 成果はFAILとして記録・出版 (押し通さない)。
- D8: audit tamper battery 4種 (a: replica raw nodes+1 → G2b verdict-vs-published gate /
  b: target third-impl result反転 → det-pair or verdict-agree gate / c: anchor expansions改竄 →
  anchor gate / d: rows.json replica_nodes改竄 → verdict gate)。全捕捉と復帰greenをlogに記録。
- D9: 出版 B (outputs: status.log / targets 16 / anchors 4 / negative 2 / replica 16 /
  rules-gate / audit-summary + audit runログ×3 / val-gate host 4) → C (README最終 +
  MANIFEST-sha256) → 完了log (`research/log/2026-11-24-part-de-b28p1win8-thirdimpl-completion.md`)。
  fetch-back byte検証を全出版物に実施。

## stop rules

- いずれかの gate で GATE FAIL または MISMATCH → その時点で実行停止し、観測を誠実に記録して
  出版 (verdict不消費)。D5 の p1/p2 不一致・published との不一致は chain 訂正レーン候选の
  証拠として保存。
- third-impl runlimit (wall-inconclusive) → そのキーは honest record (NOT a verdict)・
  再実行は別declaration。
- 実行環境リセット等のインフラ事故 → published scaffold から kit復元して sha検証の上やり直し
  (published evidence だけが証拠の設計)。
- 対象8キーの第三実装verdictがpublished WINと一致しない場合 → **採用も被覆も一切行わず**
  divergence証拠として記録 (three-implementation corroboration不成立の誠実報告)。

## 主張の限定

- 本Partは交叉検証のみ。**verdict不消費**: 対象8行は honest WIN labels のままで、adoptionは
  scrutiny owner C++第二実装 gate `9193f5b6…` 通過後、pinned merger `90711961…` 経由の別adoption
  Part 専権。
- 閉鎖・被覆・secured・root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 (54キーすべて・対象8キー含む) は本Partの前後を通じてすべてUNKNOWNのまま。**
  nodes数・expansions数・ttHits数を勝敗や距離として読まない。
