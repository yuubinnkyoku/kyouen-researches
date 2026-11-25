# Part EG 宣言: closure class 34908 b33-win-6 残 unconsumed WIN 6行 (af029/af047/af050/af053/af023/af048) 第三実装交叉検証

- 2026-11-25T08:16Z (declaration authoring time; commit timestampはGitHub側)
- 単一オーナー宣言・publish-then-execute。本宣言以降、下記scopeの作業は本レーンの単一オーナーが行う。
- 観測 HEAD-before-push: `7e4113461b3fab56633f6008ed1853b91c438e6f` (2026-11-25T08:08:42Z)
- 実験dir: `research/experiments/n11-centralreply-closure-b33win6-thirdimpl-20261125/`

## 対象と非対象

- 対象: closure class 34908 のうち、Part EE wave F reaudit closure table で確定した **残6つの
  unconsumed probe-level WIN行** (class 34908 unknown children の完全集合):
  af029 [1152921504607895553,68720525312] (s5 900646・nodes 4,862,485・budget 15M batch-33) /
  af047 [1152921504607895809,68719476736] (s5 961976・nodes 9,841,975・15M) /
  af050 [1152921504607899649,68719476736] (s5 962386・nodes 7,311,834・15M) /
  af053 [1152921504606852096,17660905521152] (s5 962470・nodes 5,182,129・15M) /
  af023 [1152921504607895553,68719478784] (s5 810351・nodes 28,933,179・budget 30M Part EA reprobe) /
  af048 [1152921508902862849,68719476736] (s5 962172・nodes 17,816,616・30M Part EA reprobe)。
  **af023/af048 の15M再実行は禁止** (b33 15Mでは EXHAUSTED 確定済み・published verdictは30M WIN)。
  また af029 は30M anchor条件 (Part EA anchor pair・result WIN・nodes 4,862,485・15M行と同一nodes)
  でも二重再現する (G2c)。
- 第三実装 (third_impl.js・非df-pn AND/OR minimax) による verdict 一致 (三実装交叉検証:
  jsreplay runner系×2 + third_impl.js) と本host pinned-replica 2-pass fresh-cold の
  node-exact 再現を検証する。
- 非対象: Part EF batch-38 (class 30345 rank 12・49キー fresh probe・inc1〜inc3出版済み ai001〜ai021)
  は**別実行が所有**・一切触れない。K1316 (z=12 predecl) も別実行が所有・触れない。
  adoption は行わない (verdict不消費)。merger `90711961…` は adoption Part 専権で本Partでは使わない。
- 対抗宣言の機械確認: 観測HEAD (7e411346) までで、実験dir
  `n11-centralreply-closure-b33win6-thirdimpl-20261125` は未存在、Part EG を名乗る
  declaration/completion log は未存在、"b33win6" に交差する単一オーナー宣言なし
  (直近の宣言は Part EE wave F 完了log・Part EF batch-38 4 commits・K1316 5 commits で、
  いずれも本scopeと交差しない)。

## 事前登録 pin 群 (scaffold commit の内容)

scripts 7 (adapted 4 + pinned byte-clone 3):

- `make_kit_eg.py` sha256 `c2f4f88bd4c3283b47dd2f5bd77e7840b65e3c680c2257dd1ce4d9b955b4d0e9`
  (CZ maker適応・G1 pin層全sha照合 / G2 字段交叉 (CSV×batch-keys×reprobe-keys・af029はEA anchor
  roster経由) / G3 status行照合 / G4 raw第一走路解析 / G5 merged cache would-be行不在+同pair衝突
  ゼロ+af034採用行1回 positive control / G6 EE manifest flags / G7 budget map / G8 idempotency
  guard。maker実行×3 byte同一)
- `audit_eg.py` sha256 `b7a4bb367b23f767e8046545604e89ce9eb7ad216242c4718282e07edf4b054b`
  (CZ audit 3c95e32f 適応・宣言済みdeltaは下記「declared deltas」・G1-G7 213 gates)
- `run_replica_eg.sh` sha256 `55286b9e9883aab5b26b159b7bfd6752430e2167220f73ef2a24d55c22dba917`
  (CZ runner cb909064 適応・declared deltaは per-key budget whitelist map
  (af029/af047/af050/af053→15M・af023/af048→30M・af029-30m→30M) とそのコメント・
  実行はtimeout 260 wrap済み)
- `run_thirdimpl.sh` sha256 `a0b77d8330c696a5a7da2883d49110ae8703dc1673be10d3a9972ea53c885a41` (CW版byte-clone)
- `third_impl.js` `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998` (pinned byte-clone)
- `jsreplay.js` `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` (pinned byte-clone)
- `verify_tbl_eg.js` sha256 `df62a9b978d35c2dd05ba90da736a8be1fc439b1fb8b471345ef740653d3b7ea`
  (CZ verify_tbl.js c8c52528 のfork・declared deltaは require path のみ
  './jsreplay.js' (kit-local byte-clone 84585617)・ロジック無変更)

input 11: rows.json
`799d9faf191c5a7c1bfc164f4a2df46df91b4a01f02ce0e458718b7d2782c19b`
(schema `n11-centralreply-closure-b33win6-thirdimpl-input-v1`・consumed_into_canonical_cache=false・
unadopted_win_rows=true・canonical_cache_sha256_unchanged=fc3e4ac9) + 6 targets + anchors k02a/l1a +
negatives ng1/ng2 の10 input CSV (maker G0/G2 が published と byte一致を機械検証):
af029 `b5500b8d98cd3cbef56f6177245d8e3c21c31081f2252c6454f1aee73ce30c10` /
af047 `24cc1aa00849f6b74c7f976b46903874321aac981f62dd542e51948a3f351418` /
af050 `3bc623db974bc6285c575b8575a75510c3e9f1909a650a4969e214225e507729` /
af053 `b30a43a948945d7b49946c28dec20b5859aac1003d522f042cfff4d1225d989e` /
af023 `0ba31256582eae15cc80fb2bdbfe56a140533828cdab7a05eeef6ca1089a1c08` /
af048 `d619dcd7d47d7b65f1c4325d99b69211826eb83732c3eb475f14ea4f9f973422` /
k02a `b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887` /
l1a `e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a` /
ng1 `8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09` /
ng2 `f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc`。

sources 27 (commit-pinned raw fetch・全sha宣言pin群と同一):
- b33 (batch-33 class-34908 drive 15M・実験 `n11-centralreply-closure-class34908-batch33-20261124`):
  raw 12 (6キー×p1/p2・後述PIN_RAW) + status.log
  `1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52` (making 47行) +
  batch-keys.json `8a863381454fcfec3cb190db7130ce6801accf56170ee3a1b944402491fecbaa`。
- ea (Part EA b33exh5 reprobe 30M・実験 `n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125`):
  raw 8 (af029 anchor pair・af023/af048 reprobe・af001 anchor provenance) + status.log
  `db7c7017d7bfeef2d0c17c646b22f77b8bfd52a66796433b86e88444741c0438` +
  reprobe-keys.json `3744b522346b00108f66991cd4009943af84344ab388431652783fbf8227a663`。
- ee (Part EE af034loss1 adoption core・読み取り専用):
  merged canonical cache
  `fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f` (277,578 bytes・6,666 s5verdict行
  = base cecc1a0f 6,665 + 採用済 af034 60M LOSS 1行・WIN 158/LOSS 6,508) +
  increment `cc9c474627ec8f6fc98c0ebeb7600707021e8cd598b3be6799d39c104289e162` +
  increments-manifest `0ad3469ede4bfbddaee21d12dbab97f7e0babdbe5cbaba8cc7a6f2f41d0d22c9`
  (schema `af034loss1-increments-manifest-v1`・loss_ids [af034]・win_scenario_note は6キーを
  全て名指しで列挙・batches[0].anchor_ids に af029 がanchor provenanceとして正規存在)。

raw pins 16 (b33比較対照 8 + EA 30M比較対照 8):
b33: af029.p1 `6bd7a2ac37cccd8a387d6b505112c1a93b712e8d41b43467fa0844ce64ec0036` /
af029.p2 `b6abaa6384ee93c890cadd350f2f844889f3ee42110935a366af7893a2030e0b` /
af047.p1 `8fd62fdd27d10235b4ba67c6f43cfeb4fe5f494559544119d4f0339223a7b8c6` /
af047.p2 `ae4719e8c8a0a7abd72cec6f4e013c1e576c7627100de95b55ba34c364b694a4` /
af050.p1 `3ea4f644ca19186f0a56ae25f79ef0ccc8b608b5ef64045bc052a488cae9b1d7` /
af050.p2 `43a5b71ca57d2a2601f82b7ec35980b0761dc315e8093f3c9ae603cd8d4ca5a6` /
af053.p1 `fce95ca8921357641f477a01483fbd4c35e6f183a25c8d741657dec645f78533` /
af053.p2 `920b1029500e93532238d03d07e89fdf091ffecd2481cab56f7dd032b5f645b7`。
(b33の af023/af048 raw は EXHAUSTED provenance として kit に同梱するが verdict 比較対照ではない:
af023.p1 `225b4d6526f1f8c5b6a6dafe6b5b359df4718c6b6b958147582ead3c14b5e33a` /
af023.p2 `fc86c52502e08f04dd2a7d35d257021d808f1a3652f1ed758f91ac3c3954e17f` /
af048.p1 `95c30994057c5017b5e3f153fea9432c21ca7d9da119ff1181ffee95805ce2a4` /
af048.p2 `25fa2c2279eadd297b488d2156dfac9ee5c9abbb06e0026bfc878aaf4fce6450`。)
ea 30M: af023.p1 `fe118851a927944328a62387d0410a596713c87f1360dda662c97f87913c1dbe` /
af023.p2 `af02e38b07a7f1da9af28c0af7985eaa0cdd97ec2884298ede3a831b19c9198b` /
af048.p1 `ae8df6ad6f922669f285f1c2a20d7fa09453c2ef38f64f1b4b878c3034e9d07a` /
af048.p2 `e2056ca26533124e20d3538eebc5e6c4b752be21b92e9e3780c5a0040f0bb620` /
af029-30m.p1 `1726ecb6d8199d612130d3c2cae12b176102fef0468263cbc1397f525eb0aa66` /
af029-30m.p2 `c937f8964385b2e4c74c1f1d417cdb113b2548dca33c3e0604facea7d9c905a6`。
ea anchor provenance: af001.p1 `c2bc73f6a5d88720e33fc3fb498ab16f2d541d7cad62248ef8d04b5f9351381d` /
af001.p2 `e4614f6bd7d4f20cfdd7dba3362e6db52328827a120b9d379fdd2accbdbf1681`。

val-gate 8 (CW kit不変再利用):
at2m-s5-1152921504606851072-536870946.input.csv
`ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348` /
at2m-s5-1152921504606851072-536870946.published-baseline.out
`6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c` /
at2m-s5-1188950301626860544-536870912.input.csv
`56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62` /
at2m-s5-1188950301626860544-536870912.published-baseline.out
`eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24` /
first-15m-s5-1152921504606851072-536870946 (input同sha) baseline.out
`8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591` /
second-15m-s5-1188950301626860544-536870912 (input同sha) baseline.out
`91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb`。

## declared deltas (CZ maker/audit からの、宣言時点で確定している差分)

1. targets: CZ single ab028 WIN行 → EG 6行 (b33 15M 4行 + EA 30M 2行)。replica budget gateは
   per-key budget map (af029/af047/af050/af053→15M・af023/af048→30M) に置換。
2. G2c (新規): af029 二重再現 gate。同キーを15M (batch-33行) と30M (Part EA anchor行) の両条件で
   再現し、両方が published result=1・nodes=4,862,485 に node-exact であることを要求。
3. PIN_RAW 16本 (CZ 2本→16本): b33 8 + EA af023/af048 4 + EA af029-30m 2 + EA af001 2。
4. G6 unadopted-corroboration: CZ Part CU 出版物 → EG Part EE af034loss1 adoption 出版物
   (merged 6,666行・increment・manifest)。would-be行不在は (a) 完全な s5verdict 行一致と
   (b) same-(lo,hi) pair 行不在の二重 gate。採用済 af034行 (`s5verdict,1152921504607911937,
   68719476736,5,2,32012059`) が merged cache にちょうど1回だけ存在する positive control
   (absence gate が vacuous pass しない担保)。manifest 側は targets が全 adopted/win/probed id list
   に出現しないこと (af029 の batches[0].anchor_ids 出現は宣言済み例外・provenanceで採用listではない)。
5. status battery: CZ raw status-line照合 → EG は G4 で raw 第一走路解析 (SSOT=raw) を採用、
   status.log は provenance として kit 同梱のみ。
6. verify_tbl.js → verify_tbl_eg.js: require path を kit-local './jsreplay.js' に修正
   (ロジック無変更)。
7. EXP/SCHEMA/rows-schema 文字列を EG 実験名に更新。

## 事前実行済み (本宣言の前に行った機械検証・全部local)

- maker `make_kit_eg.py`: gates PASS ×3 実行で全出力 byte同一 (rows.json は 799d9faf で確定)。
- maker tamper battery **10/10 捕捉・battery後 kit完全復元 (diff 空)**:
  pin層 (pin・batch-keys nodes改竄・b33 status行改竄・merged cache forge行追記・manifest loss_ids
  追記) は全て pin gate が rc=1 捕捉。semantic層 (同一変異を pin 更新して実施) も全て
  対応 gate が rc=1 捕捉。batteryは pristine copy から復元する方式 (出版kitは不変)。
- audit `audit_eg.py` smoke (合成データ kit・出版kitに触れない・宣言に開示):
  - 全出力を rows.json の pin 値から合成し、negatives ng1/ng2 は**本物の pinned third_impl.js を
    実行**して正規 GATE_FAIL 行 (`legal count mismatch: derived=87 declared=88` /
    `stone count mismatch: bits=5 declared=6`) を得た (host node v22.20.0 で kit scripts が実行可能な
    ことも実証)。
  - **ALL 213 GATES PASS・rc=0** (audit run ×3、audit-summary.json 28,887 bytes が3回byte同一)。
  - audit tamper battery **20/20 を期待gate名通りに捕捉** (全件 rc=1):
    t01 pin-third_impl.js / t02 pin-rowsjson / t03 pin-jsreplay / t04 csv-legal /
    t05 rules-mismatch / t06 replica-det / t07 verdict-vs-published /
    t08 budget-map (af023 30M→15M 擬態を schema gate が捕捉) / t09 af029-30m-nodes /
    t10 target-divergence (third result 2/clean → verdict-agree gate が DIVERGENCE として捕捉) /
    t11 target-det / t12 target-quads / t13 anchor-expansions / t14 neg-msg /
    t15 valgate-node-exact / t16 pin-merged / t17 semantic row-absent (全 pin copy を緩和した上で
    merged cache 内 WIN行を af029 would-be行と差し替え → row-absent gate が捕捉) /
    t18 manifest note 欠落 / t19 manifest probed_ids 追加 / t20 replica quads header。
    battery後 pristine 再実行 rc=0 green。
- run_thirdimpl.sh の dry-shape 確認 (rows.json presence grep・CSV shape gate・budget引数固定
  --cap=300000000 --wallcap=240 --memo-power=22)。

## 既知の環境制約 (誠実記録)

- 本sandboxに g++ が存在せず、パッケージ導入も禁止 ("Package installation is forbidden in this
  sandbox") のため、scrutiny owner C++ 第二実装 gate `9193f5b6…` は本レーンでは実行不可能
  (Part DU等と同一障害)。したがって本Partの「第三実装」は JS (third_impl.js) であり、
  採用 (adoption) はこれを以って行わない。採用は C++ gate 通過後の別 adoption Part 専権。

## protocol (publish-then-execute・E1-E9)

- E1: rules gate — `node scripts/verify_tbl_eg.js` → `output/rules-gate.txt`
  (要 `replica quads 95670 mine quads 95670` + `mismatches 0`)。
- E2: val-gate fresh 4本 (budget 2M/2M/15M/15M・host出力 `val-gate/<key>.eg-host.out`)。
  published baseline と node-exact (wall_s以外全字段)。1本でも不一致 → hard-stop。
- E3: negatives ng1/ng2 → GATE_FAIL (`legal count mismatch` / `stone count mismatch`)。
  GATE_FAILでない → hard-stop。
- E4: anchors k02a/l1a a/b det-pair (expansions 9,106,337 / 7,660,202・ttHits 4,991,527 /
  3,951,175 は published pinと一致必須)。不一致 → hard-stop。
- E5: replica 6キー×2-pass fresh-cold (`run_replica_eg.sh`・budgetはper-key map) +
  af029-30m 2-pass。p1==p2 determinism + published raw (PIN_RAW) と result/nodes 一致
  (node-exact)。不一致 → hard-stop・記録。
- E6: third-impl targets 6キー×2 run (a/b・`run_thirdimpl.sh`
  --cap=300000000 --wallcap=240 --memo-power=22)。det-pair + verdict agree (expect WIN=1)。
  af023は1run ~210s 見込み。runlimit (wall-inconclusive) は NOT a verdict。
- E7: audit `audit_eg.py` ×3 byte-identical (stdout + output/audit-summary.json)。
  ALL GATES PASS 必須。FAIL → 成果はFAILとして記録・出版 (押し通さない)。
- E8: audit tamper battery 数件を実 kit 上で実施し復帰 green を完了logに記録
  (宣言済み smoke battery 20/20 は synthetic kit によるもので、実kit上の少数复抽出確認とする)。
- E9: 出版 (outputs: status.log / replica / targets / anchors / negative / rules-gate.txt /
  audit-summary.json×3) → README + MANIFEST-sha256 → 完了log
  (`research/log/2026-11-25-part-eg-b33win6-thirdimpl-completion.md`)。
  fetch-back byte検証を全出版物に実施 (HEAD sha固定raw URL)。

## stop rules

- いずれかの gate で GATE FAIL または MISMATCH → その時点で実行停止し、観測を誠実に記録して
  出版 (verdict不消費)。特に replica の p1/p2 不一致・published との不一致は chain 訂正レーン
  候補の証拠として保存。
- third-impl verdict が published WIN と一致しない場合 → **採用も被覆も一切行わず** divergence
  証拠として記録 (three-implementation corroboration 不成立の誠実報告)。
- push競合・同時書き込み・取得失敗 → 無理に押し進めず状況を簡潔に記録して次回実行に回す。
- 実行環境リセット等のインフラ事故 → published scaffold から kit 復元し sha 検証の上やり直し。
- **af023/af048 を15Mで再実行しない** (published verdict は30M WIN)。runnerがこの条件を強制する。

## 主張の限定

- 本Partは交叉検証のみ。**verdict不消費**: 対象6行は honest WIN labels のままで、adoption は
  scrutiny owner C++ 第二実装 gate `9193f5b6…` 通過後・pinned merger `90711961…` 経由の
  別 adoption Part 専権。
- 閉鎖・被覆・secured・root勝敗の主張はしない。class 34908 自体は6 unconsumed WIN children を
  残したまま (本Partで1行も消費しない)。
- **標準11×11空盤・19 central-reply roots・二石root・S2・class 1/2/4/30345/34908 (全キー) は
  本Partの前後を通じてすべてUNKNOWNのまま。** nodes数・expansions数・ttHits数を勝敗や距離として
  読まない。途中結果から勝敗を断定しない。
