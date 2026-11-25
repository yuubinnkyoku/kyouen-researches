# Part CL 宣言 (2026-11-23): batch-28 (closure class 5343) drive-2 LOSS行 aa003 第三実装交叉検証 + 本host pinned-replica 2-pass再現 + Part CH採用row補強 (publish-then-execute)

単一オーナー: n11中央応答レーン (長期レーン本セッション)。対抗宣言なし
(push直前の最新main直近コミットを機械grepし、aa003 第三実装/thirdimpl-loss/
Part CL を主張するcommitなしを確認済み)。observed HEAD-before-push は
commit messageに記録する。

## 1. スコープ

Part CD (batch-28 drive-2) で出版された **LOSS行 aa003** (key
(1152921504741064704, 4228)・s5 104943・membership 3・legal 86・replay
result 2・nodes 4,070,373・2-pass node-exact) に対して:

1. **pinned第三実装** (非df-pn AND/ORミニマックス `third_impl.js`
   `08ea958f…`) によるverdict-level交叉検証 (2-run determinism pair)、
2. **本host pinned-replica (`jsreplay.js` `84585617…`) 2-pass fresh-cold再現**
   (published raw fields との node-exact一致。aa003の最初の独立セッション再現)、
3. **Part CH採用rowとのbyte同一性機械ゲート** (aa003のLOSS rowはPart CHで
   pinned fail-closed merger `90711961…` 経由でcanonical cache 6,294行
   `3124461b…` に採用済み。本実験が交叉検証するrowが採用rowと
   byte同一であることをmerged cache / increment `dc857bfd…` /
   increments-manifest `017c7c30…` の3ソースで機械gateする)。

**verdict不消費** (新規の採用・解放・閉鎖は一切ない。aa003の採用は本実験に
先行する別宣言Part CHが完了済み)。閉鎖・被覆・secured・root勝敗の主張は
しない。WIN 4行 (aa001/aa002/aa006/aa007) はhonest labelのまま (aa006/aa007は
Part CG宣言済みレーン所有・本Partは非接触)。aa008/aa009 (Part CJ drive-3出版WIN行・本Partは非接触) を含め
WIN行はすべてhonest labelのまま。EXHAUSTED 2行 (aa004/aa005) はhonest
UNKNOWNのまま。batch-29 (Part CI)・batch-28 fileless残キー (Part CK drive-4
宣言済み) は並走所有で非接触。

## 2. 事前機械確認 (read-only・正直開示)

publish-then-execute規約に対する正直開示として、**read-only解析
(kit取得・published sourcesのsha256検証・maker実行・input/rows.json機械導出)
は本宣言の出版前に本hostで機械実施済み**である (Part CI宣言と同じ開示形式)。
solver実行 (rules gate / val-gate / negatives / anchors / replica / third-impl
targets / audit) は宣言後にのみ実行する。

機械確認済み:

1. **sources byte-pin 10/10**: Part CD drive-2正本
   `research/experiments/n11-centralreply-closure-class5343-batch28-drive2-20261123/`
   (MANIFEST 96行) から batch-keys-cd `af19208f…`・status-cd.log
   `343097c2…`(17行)・row-audit-cd `3e86a32b…`・README-cd `338fc136…`・
   raw aa003.p1 `9fff0eea…` / aa003.p2 `a1edb177…`・published-input aa003
   `95abcd03…`。Part CH正本
   `research/experiments/n11-centralreply-class5343-loss1-adoption-reaudit-20261123/`
   (MANIFEST 14行) から merged canonical cache `3124461b…` (6,294 s5verdict行)・
   increment `dc857bfd…`・increments-manifest `017c7c30…`。Part BF anchor/
   negative基底CSV 4件 (provenance chain AR→BF→BK→BM→BS→BV→BW→BX→BY→CC→CK)。
   すべてcommit-pinned raw fetch後にpublished MANIFEST文字列と機械照合
   (手転写shaの転写ドリフトを自らの制作過程で1件検出し機械置換で解消・
   この事故自体もrun logに誠実記録する)。
2. **maker `make_inputs_ck.py` `177c4409…` 全gate PASS・4回実行byte一致**
   (CL-SCAFFOLD battery: status-cd 17行構成gate = PASS 7 (win 4 =
   aa001 13,183,855 / aa002 6,527,041 / aa006 14,303,810 / aa007 13,483,540・
   loss 1 = aa003 4,070,373・exhausted 2 = aa004/aa005 15,000,000) + WIN-HALT 4行
   2-line pair + EXHAUSTED 2行 + TRUNCATED-RETRY 4行・row-audit-cd battery
   (probed 7・loss_rows [aa003]・win_rows [aa001,aa002,aa006,aa007]・
   exhausted [aa004,aa005]・fileless 47 = aa008..aa054完全list・mismatch 0)・
   README-cd文言battery・raw 2-pass field一致gate・**採用row byte同一性gate**
   (merged cache内 `s5verdict,1152921504741064704,4228,5,2,4070373` が
   全6,294行中ちょうど1回・同key競合rowゼロ・incrementは同1行のみ・
   increments-manifest の loss_ids/total_nodes/base 6293/absent-hits 0/
   merger pin/quarantine 0/full != loss すべて機械照合))。
3. **input/rows.json** `6e3049a1…` (schema
   `n11-centralreply-closure-b28drive2loss-thirdimpl-input-v1`・targets 1件
   (aa003・replica_result 2・replica_nodes 4070373・expect_third 2)・anchors
   k02a (expect 1・exp 9,106,337・ttH 4,991,527) / l1a (expect 2・exp
   7,660,602・ttH 3,951,175)・negatives ng1 (legal+1) / ng2 (stones改竄)・
   `consumed_into_canonical_cache: false` +
   `adopted_before_this_experiment_by_part_ch: true`)。
   input CSV 5件はpublished pinsとbyte同一 (aa003 `95abcd03…`・k02a
   `b6174a3f…`・l1a `e13d2a6c…`・ng1 `8e64b9ad…`・ng2 `f19cd5a3…`)。

## 3. kit (scripts 6・全件byte-pin)

- `third_impl.js` `08ea958f…` (published Part CCからのpin再利用・一切変更なし)
- `verify_tbl.js` `c8c52528…` (同上)
- `jsreplay.js` `84585617…` (pinned replica・同上)
- `run_thirdimpl.sh` `a0b77d83…` (同上・1 solver/1 row/1 process)
- `make_inputs_ck.py` `177c4409…` (published Part CC maker `8255d0ad…`からの
  deltaはsources切替 (Part CB→Part CD/CH) とLOSS行battery・採用row batteryの
  追加のみ・gate骨格不変)
- `audit_ck.py` `edf0ae7c…` (published Part CC audit.py `b7cfb0ce…`からのdeltaは
  EXP/SCHEMA/rows-schema文字列・target-count明細 (1 LOSS行)・文言、および
  新規gate block **G6 (採用row補強)** と **G7 (val-gate 4/4 node-exact)** のみ。
  G0-G5のgate logicは不変)

## 4. 実行protocol (宣言後・逐次・1 solver/1 row/1 process)

1. **rules gate**: `node scripts/verify_tbl.js` 期待「replica quads 95670 mine
   quads 95670 / triples checked 195044 mismatches 0」。失敗ならhard-stop。
2. **val-gate fresh 4本** (jsreplay --exact-replay・budget 2M×2 / 15M×2) →
   published baseline (`6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`) との
   node-exact比較 (wall_s除く)。期待: at2m 2本 = (result 0, nodes 2,000,000)
   exhaustion×2・15m 2本 = (result 2, nodes 3,651,923) と (result 2, nodes
   5,040,200)。比較はaudit G7でも機械gateする。
3. **negatives**: run_thirdimpl.sh ng1/ng2 → 期待GATE_FAIL (rc=1・legal count
   mismatch / stone count mismatch)。
4. **anchors**: k02a/l1a × (a,b) 計4 run → published expansions/ttHits一致
   (det-pair必須)。
5. **targets pinned-replica 2-pass fresh-cold** (aa003 × p1/p2・budget 15M) →
   published raw fields (result 2・nodes 4,070,373) との node-exact一致。
   published wall 51/49s。
6. **targets third_impl 2-run pair** (aa003 × (a,b)・cap 300,000,000・wallcap
   240・memo-power=22) → determinism (a==b) と published replica_result 2との
   **verdict agreement** (reason clean必須)。third-implのexpansions値は
   事前予想しない (出版後に実測を記録する)。
7. **audit**: `python3 scripts/audit_ck.py` 3回実行byte一致
   (audit-run1/2/3.txt + audit-summary-run1/2/3.json + audit-summary.json)。
   期待全gate PASS (CC版のG0-G5相当+G6採用row gate群+G7 val-gate gate群)・
   verdict agreement 1/1 (third=2 replica=2)。
8. **maker tamper battery** (scratch /tmp copy上・8種): T1 raw aa003.p1 nodes+1・
   T2 row-audit probed 7→8・T3 README-cd aa003 LOSS文言反転・T4 status-cd
   aa003 verdict 2→1・T5 published-input aa003 legal 86→85・T6 BF anchor k02a
   lo+1・T7 batch-keys aa003 s5_index 104943→104944・T8 merged cache採用row
   result 2→1。各tamperに適用実効性assert・maker ABORT (rc!=0) 検出後に
   scratch復元。実験dir bytes不変を検証。
9. **audit tamper battery** (scratch copy上・4種): T1 audit pin反転
   (PIN_THIRD末尾1桁) → pin-third gate fail・T2 targets aa003.a expansions+1
   → det-pair/expansion gate fail・T3 input CSV aa003 legal 86→87 → G0
   input-matches-rows fail・T4 scratch merged-cache採用row nodes+1 → G6
   adopt-merged-cache-row fail。clean control PASS・実験dir bytes不変。
10. **出版**: A scaffold (scripts 6 + input 6 + sources 14 + val-gate 8) →
    B outputs (rules-gate + val-gate this-host 4 + replica 2 + negatives 2 +
    anchors 4 + targets 4 (a/b) + audit 7 + status.log) → C README +
    MANIFEST-sha256 → 完了log (Part CH形式・独立logファイル)。全files
    commit-pinned raw URL fetch-back byte照合・branch path URL (CDN stale)
    は使わない。push直前に毎回最新mainを再取得し、並走コミットとの
    fast-forward競合はrefetch後の再 pushで解消 (内容衝突は本Part対象
    ファイルの不変を確認してから)。
11. **誠実記録**: 事前登録からの逸脱・no-op probe・再実行はすべてstatus.log
    とrun logに正直に記録する。

## 5. 事前登録stop rules

- replica MISMATCH (published raw fieldsとのresult/nodes不一致) はhard-stop・
  即時honest記録。
- third_impl DIVERGENCE (2-run非決定性) や WALL-INCONCLUSIVE (cap 300M/
  wallcap 240到達) はevidenceとして記録するがverdictには変換しない。
- EXHAUSTEDなし ( replicasはbudget 15M内でpublished nodesに一致するはず)。

## 6. 解釈ガード (route statementのみ)

- 第三実装のclean verdictがpublished replica verdict (result 2 = LOSS行) と
  一致すること、および本host replicaがpublished nodes 4,070,373を2-passで
  完全再現することは、**Part CHで採用済みのcanonical cache最新rowに対する
  three-implementation corroboration** (verdict-level文献) である。採用・
  解放・閉鎖の新規主張は一切ない。canonical cache 6,294行 `3124461b…` は
  read-only不変。
- WIN 4行 (aa001/aa002/aa006/aa007) の採用判断は引き続き scrutiny owner
  C++第二実装 gate pin `9193f5b6…` 待ち (本レーンは代行しない・aa006/aa007は
  Part CGレーンが第三実装検証宣言済み)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・
  aa003を含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・
  expansions数・ttHits数・wall秒数を勝敗として読まない。被覆・secured・
  root勝敗の主張はしない。WIN/LOSS採用は別adoption Part (pinned merger
  `90711961…` 経由) のみ。
