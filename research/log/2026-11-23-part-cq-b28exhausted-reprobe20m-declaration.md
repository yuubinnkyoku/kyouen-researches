# Part CQ 宣言 (2026-11-23): batch-28 (class 5343) EXHAUSTED 11行の高budget (20M) 再probe — 別宣言条件 — publish-then-execute

単一オーナー: n11中央応答レーン (長期レーン・本セッション本host)。対抗宣言なし
(push直前 2026-11-23T22:3xZ の最新main直近15コミットに EXHAUSTED再probe / 高budget
再probe / 20M / 20000000 / Part CQ の言及ゼロを機械確認済み・observed HEAD
`70181517` 2026-11-23T22:33:41Z「K1274 fast lane 宣言」。Part CI takeover
(batch-29 class 2251・checkpoint 1/3 `a5a159d7`)・Part CP batch-30 drive-2
(class 34269・宣言 `7aaa0525`)・Part CG re-takeover (aa006/aa007 thirdimpl・
scaffold `447ff294` outputs `486c1a6a` 出版済み) はいずれも他セッション所有で非接触)。

## 0. 本Partの位置づけ (新規の独立Part・takeoverではない)

batch-28 (closure class 5343) は Part CN で全54キーprobed (WIN 35 / LOSS 8 / EXHAUSTED 11
/ mismatch 0・published row-audit `00c32383…`) が確定済みで、Part CH (aa003) + Part CO
(7行) の計8 LOSS行はcanonical採用済み (base cache 6,301行 `854800f3…`)。残る未解決キーは
**WIN 35行 (scrutiny owner C++第二実装 gate `9193…` 専権・本レーン非接触) と
EXHAUSTED 11行 (honest UNKNOWN)** である。EXHAUSTED行の高budget再probeは Part CN/CO および
Part CI takeover宣言・Part CP宣言の不接触条項すべてに「EXHAUSTED行の高budget再probe
(別宣言条件)」として一貫してopenで列挙されており、本宣言まで誰も着手していない。
本Partはこのopen項目を、**新条件 budget 20,000,000** で実行する。

**no-15M-re-search規約との関係 (最重要の設計境界)**: published runnerの完全性guardが
明記するとおり「COMPLETED exhaustion行のno-15M-re-search規約」は15M同一条件の再実行を
禁止する。本Partは15M条件を一切再実行しない。20M (15Mの1.333...倍) は異なる条件であり、
各局の探索は最初の15Mノード分も含めて確定的に同一系列を辿る (budgetは上限のみ)。
結果が result 0 (20M枯渇) なら引き続き honest UNKNOWN であり、20M条件の
same-condition再probeは以後も行わない。

## 1. スコープ

- 対象: published batch-28 full row-audit
  (`n11-centralreply-closure-class5343-batch28-rowaudit-full-v2`・output/row-audit.json
  sha256 `00c323835f9ebc048b6ffea81a8fd556e3e8146adf1c562c34aa89d9d7bb69c0`)
  の exhausted_rows 11行: **aa004 / aa005 / aa021 / aa028 / aa030 / aa031 / aa032 /
  aa035 / aa047 / aa050 / aa053** (この鍵集合はPart CQのmakerにfail-closedピン済み。
  選定の余地なし・cherry-pick不可能)。
- 各キーを budget 20,000,000 で2-pass fresh-cold (p1/p2別々のcold起動) probeする。
- **verdict不消費**: probeのWIN/LOSS行はhonest labelのまま。canonical adoptionは
  別adoption Part (pinned fail-closed merger `90711961…`) 経由のみ。WIN行の採用判断は
  引き続き scrutiny owner C++第二実装 gate (`9193…`) 専権 (本レーンは代行しない)。
  閉鎖・被覆・secured・root勝敗の主張はしない。
- canonical cache (Part CO merged 6,301行 `854800f3…`) への書込は一切しない
  (read-only不変)。closure table不変。reaudit/簿記更新はprobe完了後の別工程の判断。

## 2. 宣言前機械確認 (read-only・本host・正直開示)

solver実行 (val-gate fresh・anchor・reprobe probe) は本宣言の出版後にのみ行う。
以下はすべて出版前に取得した機械データである。

1. **published kit byte-pin再検験**: jsreplay.js `84585617…` / runbatch.sh `f591f8c2…` /
   batch-28 packet batch-keys.json `af19208f…` / 13対象キーinput CSV 13件のsha256が
   published Part CN MANIFEST-sha256.txtと完全一致 (検証26/26)。対象22 pass raw
   (EXHAUSTED 11キー×2) および anchor基準4件 (aa036/aa046×2) もpublished MANIFEST pinと
   完全一致 (検証26/26)。EXHAUSTED 11行のpublished replay行はすべて
   `budget=15000000,result=0,nodes=15000000` でrow-audit文面と整合。
2. **EXHAUSTED鍵集合の機械再導出**: published CN status.log (`ca1e98cc…`, append-only
   正本・`P1-FAIL ` junk行を含むが verifier行照合は無視) からEXHAUSTED行を抽出すると
   上記11行と完全一致。published row-audit.json `00c32383…` の exhausted_rows とも完全一致。
3. **base-cache不在**: Part CO merged canonical cache (6, canonical verdict行 6,301・
   sha256 `854800f3…`・WIN 158 / LOSS 6,143) に対し11キーの (lo, hi) ヒットは
   **0/11** (全キー未解決のまま・採用による重複なし)。
4. **派生runnerの機械検証**: published runbatch.sh (`f591f8c2…`) との `diff` は
   **EXACTLY 1行** (`BUDGET=15000000` → `BUDGET=20000000`)・sha256
   `c5e86d49bc851f7e511e811bef5052d4634adfbbdf85a1224d101638db284a90`。
   stop rules (WIN rc=45 / MISMATCH rc=42・hard-stop / p1,p2 fail rc=43,44)・完全性guard
   (`# replay_done`なしpassはtruncatedとしてsidecar化しfresh-cold再実行)・
   2-pass fresh-cold設計はすべて不変。
5. **makerのbyte-stability**: make_reprobe_keys.py (fail-closed・G1-G5ゲート) を
   通常環境と隔離環境 (env -i・別HOME・PYTHONHASHSEED=random) で実行し
   input/reprobe-keys.json は2回ともbyte-identical (sha256
   `e8961c7ed02fbf1bfad51e33d2f757a6c0ade0b605371cf030b1a16c153ac466`)。
   なおmaker開発中にanchor 1件 (aa046.p1) のpin手転写1文字脱字をfail-closedゲートが
   即捕捉した (MANIFEST抽出値で機械修正・手転写禁止の再確認)。

## 3. kit設計 (実験dir)

`research/experiments/n11-centralreply-class5343-b28exhausted-reprobe-20261123/`:
scripts (jsreplay byte-clone / runbatch byte-clone〔参照〕/ runbatch_b28exh20m.sh
最小派生 / make_reprobe_keys.py / cq_local_step.sh / audit_cq.py)・input (13 CSV
byte-clone + batch-keys-b28.json byte-clone + reprobe-keys.json生成物)・sources
(anchor基準 published raw 4件)・val-gate (published 4組 + fresh host出力)・
output (status.log append-only / raw / audit.json)。MANIFEST-sha256 (全ファイル) は
scaffold出版後に同梱。

## 4. 事前登録: 実行protocol・stop rules・安全規則

1. **val-gate fresh 4** (sanctioned: at2m×2 budget 2,000,000 / 15m×2 budget 15,000,000・
   published baselines byteピン): 本host freshで4/4 node-exact (result・nodes・replay_done。
   wall_s比較外) を必須とする。不一致ならhard-stop (出版物は宣言+当該失敗記録のみ)。
2. **anchors (derived-runner 20M end-to-end gate)**: aa036 (published LOSS・nodes 955,659・
   result 2) と aa046 (published WIN・nodes 2,185,149・result 1) をderived runner
   (budget 20M) で2-pass実行し、result・nodesがpublished値と完全一致することを必須とする
   (budgetは上限のみゆえ探索は同一・nodes不変のはず。budget flag列 (f5) のみ
   20000000に変わる)。不一致ならhard-stop。
3. **11キーの再probe**: cq_local_step.sh (single worker・1 invocationで先頭の未了キーを
   1つ) で aa004..aa053 (reprobe-keys.json順) を順次実行。各workerは `timeout 260` 内側
   (外側呼び出し295s・Part CN運用知見継承)。
   - **WIN-CONTINUE事前登録** (Part CE/CK/CN先例): runner内蔵stop rulesは不変・
     orchestration層のみ rc=45後も継続する。11キー完走を目指す。
   - **MISMATCH (rc=42) はhard-stop**: その時点のevidenceをhonest出版して終了。
   - **EXHAUSTED-at-20M (result 0)**: honest UNKNOWN・継続。
   - **WINDOW-EXCEEDED事前登録**: 同一passのTRUNCATED-RETRYが2回 (260s窓に20M passが
     入らない) のキーはskipし honest unresolved-in-window として監査に記録する
     (無限retry防止。将来の別Part条件 (窓/budget設計変更) に委ねる)。
   - truncated sidecarはpublished runner guardが `.truncated.HHMMSS.out` にrename・
     すべて出版 (append-only規約)。
4. **audit**: audit_cq.py (fail-closed) で (a) 11キーrow監査 (両pass replay_done・
   p1/p2 fields一致〔wall_s除く〕・budget列20000000・key/lo/hi/legal一致・
   result妥当性〔0→nodes==20M / 1・2→nodes<=20M〕・quads header 95670・status.log
   照合)、(b) anchors・(c) val-gate fresh 4・(d) rules gate (全outのquads 95670)、
   (e) WINDOW-EXCEEDED/unprobed帳簿、を検証し output/audit.json
   (schema `n11-centralreply-c5343-b28exh-reprobe20m-audit-v1`) を生成。
   3回実行byte-identicalを必須とし、tamper電池 (p2 nodes改変→p1/p2不一致捕捉 /
   result反転→status照合捕捉 / replay_done削除→truncated捕捉 / registry budget改変→
   registry gate捕捉 / clean control PASS) を実施して各probe復元byte検証する。
5. **出版**: A scaffold (kit) → B outputs (status.log + raw sidecars込み + val-gate
   fresh + audit.json) → C README最終版 + MANIFEST-sha256 → 完了log。すべて
   fetch-back byte照合。

## 5. 期待機械簿記 (事前登録)

probe結果によって class 5343 の unknown帳簿が変化しうるが、**本宣言は結果非予告**であり
いかなる勝敗も宣言しない。全キー20M枯渇なら11キーともUNKNOWN不変で「20Mでも枯渇」という
honest実験事実として出版する。nodes数・wall秒数を勝敗として読まない。

## 6. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・EXHAUSTED 11行・
WIN 35行・採用済みLOSS 8行を含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
nodes数・wall秒数を勝敗として読まない。WIN採用はscrutiny owner C++第二実装 gate
(`9193…`) 通過後の別adoption Part (pinned merger `90711961…` 経由) のみで、
本レーンは代行しない。閉鎖・被覆・secured・root勝敗の主張はしない。

## 7. 不接触

Part CI takeover (batch-29 class 2251・進行中) のdir・outputs・進行、Part CP batch-30
(class 34269・drive-2宣言済み) のdir・outputs・進行、Part CG re-takeover
(aa006/aa007 thirdimpl・outputs出版中) のdir・outputs・進行、batch 1..30各published dir
(不変)、BASE caches (`3124461b…` 6,294行 Part CH merged・`854800f3…` 6,301行 Part CO
merged) read-only不変、fast lane (K1274 min>=5 z=6宣言など)・finite-field lane・
inversive lane・19root計画、WIN 64 unconsumed候補の採用状態、scrutiny owner C++
gate (`9193…`) 専権事項、他バッチEXHAUSTED行の再probe (本宣言はbatch-28の11行のみ)。
