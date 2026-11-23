# Part CP completion: batch-30 (closure class 34269) drive-1 — 4キー wave完走 (ac001..ac004)・残50キー fileless UNPROBED (2026-11-23)

Part CP drive-1 wave完結。publish-then-execute規約どおり、宣言 `research/log/2026-11-23-part-cp-batch30-class34269-drive1-declaration.md` (commit `189a2e8e…`・observed HEAD-before-push `8b75b786…`・fetch-back byte一致 sha256 `f9a5eee7…`) → A scaffold `281d58e6…` (73 files) → B outputs `05a5ac94…` (9 files・observed HEAD `a5a159d7…` = Part CI checkpoint 1/3、非接触) → 本完了log。**verdict不消費・11×11 UNKNOWN担保不変**。

## 選定記録 (batch-30 = closure class 34269)

- 起点cache: Part CO adoption後merged canonical cache 6,301行 (sha `854800f3…`) + update8 receipts (`b658290a…`)。選定前の機械再導出はpublished CO reaudit (`9d3965d9…`) とclosure table全808行で不一致0。WIN候補64キー (batch-29側WIN33 pin dict + batch-28 row-audit WIN 35行・重複4) はすべて未消費。
- first-clean = **rank 36 class 34269** (unknown 54・groups [(12,108)]・WIN64共通部分0・対30 packet衝突0・quarantine 0/54)。rank 21 class 12643はwin反駁 (batch-21 a003の未消費WIN {115192}を含む) で選定外。rank 35 class 2251はbatch-29全54キーpkt (Part CI進行中)。rank 37 class 34948はpkt {415128} (継承pin)。runner-up rank 38 class 5804。
- 54キー ac001..ac054 (batch-keys.json sha `79fbd166…`・maker `make_batch30_keys.py` sha `61fab4f7…` fail-closed全gate PASS・byte-stable x2)。

## 成果

1. **val-gate fresh 4/4 node-exact** (宣言後・本host fresh実行・published baseline 4組はbyte-copy): at2m 2キー result 0 / budget 2,000,000 exhaustion (nodes 2,000,000 x2)・first-15m 3,651,923・second-15m 5,040,200・`# replay_done` x4 (truncationなし)・nodesすべてpublished baseline完全一致 (wall_s比較外)。
2. **drive-1 wave: probed 4 = WIN 2・LOSS 2・EXHAUSTED 0・fileless 50・MISMATCH 0**。すべて2-pass fresh-cold node-exact (PASS = p1/p2 replay行のbudget/result/nodes完全一致)。
   - ac001 PASS result **2 (LOSS)** nodes 5,635,468
   - ac002 PASS result **1 (WIN)** nodes 10,752,246
   - ac003 PASS result **1 (WIN)** nodes 8,036,766
   - ac004 PASS result **2 (LOSS)** nodes 5,816,333
   - 事前登録どおり**distinct WIN 2到達でwave停止** (WIN-HALT)。ac005..ac054はfileless UNPROBED (継続は別宣言drive-2 WIN-CONTINUE)。
3. **出版コミット** (fetch-back照合): A 73/73 scripts 4 + input 55 + val-gate 12 + README + MANIFEST 72 pins (GitHub APIサイズ全一致・MANIFEST内shaはローカル実測と全一致)・B 9/9 (下記pin表・fetch-backサイズ全一致)。

## output sha pin表 (B commit `05a5ac94…`・全9ファイル)

| file | sha256 |
| --- | --- |
| output/status.log | `43fcad174e7d3ec4bbc8a9724e764fd93b5d6cfce80e64921d77a76ae8b2360c` |
| output/raw/ac001.p1.out | `1bef2dc2477f36fa21eee3f48438f2792b3f386915753f32f6c4f89573a12df7` |
| output/raw/ac001.p2.out | `bde8b2360a65a1424678e42876fb13ef8bc5964087156e96582e2c1c1fe0083e` |
| output/raw/ac002.p1.out | `e58cc0618d2c1c38e33e464fd98d89b956c7f7ff0674ebbfd6f352401add2311` |
| output/raw/ac002.p2.out | `ad06a109627d5a998f02cb3723f2b20aa844d6216ebfe84277568f2b3e0748aa` |
| output/raw/ac003.p1.out | `c585df3bf5c570de19453a861c5b011469f6613b746c3732fcdf177c9358e135` |
| output/raw/ac003.p2.out | `0f886d38a51c402949ff363ea673464103bc8268abc168d4f06be0dc50703028` |
| output/raw/ac004.p1.out | `4572f41d891fa8e60d88233ded91b46837842d9a6ed85b7d8aa2ae9fc6038d36` |
| output/raw/ac004.p2.out | `ed39eb755506661d4091ac37c68bc76b8559516ad4590bde86e075daa9cd1c5d` |

status.logは9行 (重複3行を含むまま出版・下記誠実記録)。p1/p2間のbyte差 (例: ac002 316/314) はwall_sの桁数のみ (ac002 p1 wall_s 113 vs p2 54・replay行のbudget/result/nodes/legal等は完全一致= node-exact gate PASS・wall_sは規約どおり比較外)。

## 誠実記録 (incidents)

1. **session-local `drive1_local_step.sh` v1 のdone抽出regexバグ (solver再実行0回・evidence無傷)**: v1のstatus.log done抽出は `PASS acNNN` パターンを想定していたが、実際の行は `acNNN PASS` 形式だったため、完了済みキーペア (ac001/ac002) が重複して再invokeされた。結果: (a) **pinned runner guard (output/raw/acNNN.p{1,2}.out存在検知) によりsolverの再実行は0回** (evidenceは各キー1回実行のまま完全無傷)、(b) status.logに重複3行追記 (上記9行のうち3行)、(c) 重複カウントによるWIN集計の誤読で1回だけ正常タイミングより早いhalt判定 (結果的にWIN-HALT 2の事前登録条件はac003で正しく充足し、最終verdict集計に影響なし)。**v2 (sha `e7b627a8…`) はキー単位のdedup駆動WIN集計に修正済みでkitに出版**。重複行は出版を維持 (append-only規約)。
2. B commit直前にHEADが `281d58e6` → `a5a159d7` (Part CI checkpoint 1/3・batch-29 class 2251) に進んだ。パス衝突なし (非接触) を機械確認してからpushし、B commitメッセージにobserved HEAD明記。
3. 実行session中にsandbox環境のリセット・応答喪失が発生したが、batch-30 kit作業dir (input/output/val-gate全ファイル) は無傷で、上記pin表どおり。A scaffold pushは応答喪失後にlist_commitsで成否を確認してから再送した (73/73)。

## 解釈ガード (不変)

- ac002/ac003のWIN 2行・ac001/ac004のLOSS 2行は**honest labelのみ** (unconsumed・採用判断はscrutiny owner C++第二実装 gateのまま・本レーンは代行しない)。canonical cache (Part CO merged 6,301行 `854800f3…`) への書込は一切なし。closure table不変。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 34269 (54キーすべて) はどの時点でもUNKNOWNのまま。** nodes数・wall秒数を勝敗として読まない。
- EXHAUSTED 0 (budget 15M内で全4キー決着)。fileless 50キーは未probe (= UNKNOWN)。

## レジューム (次回の着手前に必ず最新main再取得・hourly並走注意)

- **次回最有力: drive-2 (WIN-CONTINUE) 宣言** — 残ac005..ac054完走には別の短い単一オーナー宣言 (publish-then-execute) が必須。実行はdrive1_local_step.sh v2 (`e7b627a8…`) を使用 (v1は使わない)。1 invocationで約2キー・50キーで約25 invocationを見積もり、checkpointer途中打ち切り時は成果物がある分だけhonest出版。
- 併走確認: (a) Part CI (batch-29 class 2251) checkpoint 1/3が`a5a159d7`で進行中・続きは宣言側セッション所有 (停滞時のみtakeover規約)、(b) Part CG (aa006/aa007 third-impl) は18:01Z宣言 `d5e9acc2` から停滞ならtakeover規約、(c) batch-28の7-LOSS行adoption Part (aa015/aa017/aa018/aa023/aa024/aa029/aa036・pinned merger `90711961…` 経由) は誰も着手していなければNEXT。
- batch-30の54キーが全てprobedになった暁には、WIN行/LOSS行のrow-audit (Part CN先例 `row_audit_batch28_full_v2.py` 型・win-halt 2行ペイロード照合) とclosure class 34269の簿記更新が別drive完走Partの傘下で必要。
