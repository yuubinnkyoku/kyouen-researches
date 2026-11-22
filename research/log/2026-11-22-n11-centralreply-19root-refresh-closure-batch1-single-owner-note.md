# 単一オーナー宣言: n11 中央応答19root計画リフレッシュ + closure class 16757 バッチ1 (2026-11-22)

このnoteは2つのスコープを単一オーナーで宣言する。以後の同時間帯ランが同じスコープを二重に着手しないこと。

## 觀測されたHEAD (宣言時)

本noteのpush直前に最新mainを再取得し、そのHEADをcommit messageに記録する
(pushを実行するセッションが記録する)。branch / PR は作らない。

## Part A (read-only): 19root joint-plan refresh

`research/experiments/n11-central-reply-19root-frontier-refresh-20261122/`。
solver探索なし・verdict不消費・新規主張ゼロの計画・監査計算。入力は
published正本のsha固定 (dependency-graph.json.gz, merged chain cache
`4fee9d5e...`, update8 plan, independent.py `954d3a10...`, s5_evidence_policy
`78655e94...`, quarantine registry `81d23160...`)。中央応答19 root
(K0415の残存初手軌道) の第三手被覆・frozen update8計画の残要件・
closure候補表を現行chain cache相手に再計算する。未知S5はすべてUNKNOWNのまま。

## Part B (solver): closure class 16757 exact-S5 probe batch 1

`research/experiments/n11-centralreply-closure-class16757-batch-20261122/`。

- 対象: Part Aのclosure候補表首位クラス (graph class index 16757,
  mask `[1153204079095185408, 65536]`) の未確定canonical S5子48件。
  キー一覧は `input/batch-keys.json` (sha256 `2aaccc941d7aec35c416b27d5cdd10f7fbb82c9801bcf560b61e20be88c331f8`,
  48キー)。全キーは現行merged cacheに存在せず (機械確認済み)・quarantine登録なし
  (機械確認済み)・Board再計算の合法手数をinputに固定。
- 手法: pinned replica `jsreplay.js` (sha256 `84585617...`) による
  2-pass fresh cold replay、budget 15,000,000、1 solver / 1 row / 1 process、
  publish=ALL、exact-order=count、workerは最大2 (2-core host)。
  実行前にpublished two-target-design 4行のval-gateを本環境で再現すること
  (kit `input/val-gate` 手順、node数一致が必須)。
- 停止規則 (事前登録) :
  1. determinism mismatch → 即時HARD-STOP (rc=42)、以後のキー着手不可。
  2. WIN (result 1) 発見 → 即時HALT (rc=45)。当該キーのrawは誠実ラベルで記録し、
     batchは停止。WINは本レーンでは採用しない (verdict不消費・scrutiny owner待ち)。
  3. budget枯渇 (result 0) → honest UNKNOWN。15M同条件の再探索は禁止。
     次ラダー (budget昇格) は将来の新規宣言が必要。
- 消費規則: 2-pass一致かつresult 2 (LOSS) のキーのみ、fail-closed union merger
  によるincrement cache候補として出版してよい (published chain cacheとの
  WIN/LOSS conflict gate必須)。本batch単体ではroot被覆・クラス閉鎖・
  第三手securedの主張をしない (クラス閉鎖の判定・被覆監査は後続の
  refresh再実行+独立監査が行う)。
- 並走との不接触: 本batchキーは19-root計画universe由来であり、
  {60,27}系レーン (sixth-cost, s4bd, thirdimpl bank, win7/win8 chains) の
  claim集合と機械的にdisjoint (merged cache不在確認済み)。同一スコープの
  宣言が既にmainにある場合は本宣言を破棄して着手しない。

## 資源・記録

CPU並列は最大2 worker。中間成果は各chunk後にknowledge kitミラー
(`/home/user/knowledge/kyouen-research/_19root-refresh-kit/`) へ退避し、
repoへのcheckpoint pushは小分けに行う (大ファイルは1コミット1ファイル)。
  標準11×11空盤・19root ({X,60} 各root)・当該S4 classの閉鎖は本宣言の
どの時点でもUNKNOWNのまま。nodes数・pass数を勝敗として読まない。


## Part C (solver, amendment 2026-11-22): closure class 23963 exact-S5 probe batch 2

batch 1 (Part B) は事前登録のWIN-HALT規則により b018 (2-pass node-exact result 1,
3,549,602 nodes) で停止した。これによりクラス16757の全子LOSS閉包ルートは反駁され、
closure候補表の次位クラスにピボットする。

- 対象: `research/experiments/n11-centralreply-closure-class23963-batch-20261122/`。
  closure候補表class_rank 2 (graph class index 23963, mask
  `[1152921504673955840, 67109888]`) の未確定canonical S5子48件。
  キー一覧は `input/batch-keys.json` (48キー、worklist `probe-worklist.csv` の
  probe_order順、Board再計算の合法手数固定)。全キーは現行merged cache
  (`4fee9d5e...`, 5,857行) に存在しないことを機械確認済み (0 hits)。
  quarantine登録はrefreshの同policy処理済み。
- 手法・停止規則・消費規則: Part Bと同一 (pinned replica `jsreplay.js`
  sha256 `84585617...`, 2-pass fresh cold, budget 15M, mismatch→HARD-STOP rc=42,
  WIN→HALT rc=45, 枯渇=UNKNOWN, 消費はfail-closed merger経由のみ、
  本batch単体では閉鎖・被覆・secured主張なし)。
- 本amendment observed HEAD: `33a4d70365883e5d0293ecee400b8d09735301db`
  (batch 1 WIN-HALT出版後のmain)。


## Part D (solver, amendment 2026-11-22): closure class 20421 exact-S5 probe batch 3

batch 2 (Part C) は48/48全LOSSで完走し、クラス23963はfail-closed merge + refresh再監査
(`research/experiments/n11-central-reply-23963-closure-reaudit-20261122/`)
でBoard検証free（32→33番目）として閉鎖資格確定。次の正規all-LOSS候補として
reaudit closure-classes.csv rank 2 のクラス20421に着手する。

- 対象: `research/experiments/n11-centralreply-closure-class20421-batch-20261122/`。
  graph class index 20421, mask `[1155173304420536320, 131072]` の未確定canonical
  S5子49件（d001-d049、reaudit probe-worklistのprobe_order順・Board再計算合法手数固定）。
  全キーは正本merged cache（5,924行・sha256 `8a721a18...`）に存在しないことを
  機械確認済み (0 hits)。quarantine登録はrefreshの同policy処理済み。
- 手法・停止規則・消費規則: Part B/Cと同一 (pinned replica `jsreplay.js`
  sha256 `84585617...`, 2-pass fresh cold, budget 15M, mismatch→HARD-STOP rc=42,
  WIN→HALT rc=45, 枯渇=UNKNOWN, 消費はfail-closed merger経由のみ、
  本batch単体では閉鎖・被覆・secured主張なし)。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。


## Part E (solver, amendment 2026-11-22): closure class 16371 exact-S5 probe batch 4

batch 3 (Part D) は事前登録のWIN-HALT規則により d002 (2-pass node-exact
result 1, 5,359,994 nodes) で停止し、if-adopted解析
(`research/experiments/n11-central-reply-20421-win-d002-ifadopted-20261122/`)
を公開した。closure候補表上位はWIN子保持で反駁済み (16757: b018, 20421: d002,
30345: b018のs5 528497をcost childとして保持) のため、反駁証拠のない
最初の正規候補として re-audit closure-classes rank 4 のクラス16371に着手する。

- 対象: `research/experiments/n11-centralreply-closure-class16371-batch4-20261122/`。
  graph class index 16371, mask `[1153202979851993088, 16]` の未確定canonical
  S5子50件（e001-e050、reaudit正本probe-worklistのprobe_order順・Board再計算
  合法手数固定、root first=26/third=50グループ担当）。全キーは正本merged cache
  （5,924行・sha256 `8a721a18...`）に存在しないことを機械確認済み (0 hits)。
- 手法・停止規則・消費規則: Part B/C/Dと同一 (pinned replica `jsreplay.js`
  sha256 `84585617...`, 2-pass fresh cold, budget 15M, mismatch→HARD-STOP rc=42,
  WIN→HALT rc=45, 枯渇=UNKNOWN, 消費はfail-closed merger経由のみ、
  本batch単体では閉鎖・被覆・secured主張なし)。val-gate 4/4 node-exactは
  本ホストで本session中に再現済み (batch4 val-gateに同outputを固定)。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。


## Part F (solver, amendment 2026-11-22): closure class 12264 exact-S5 probe batch 5

batch 4 (Part E) は事前登録のWIN-HALT規則により e002 (2-pass node-exact
result 1, 14,112,632 nodes) で停止した（if-adopted解析
`research/experiments/n11-central-reply-16371-win-e002-ifadopted-20261122/` 出版済み）。
closure候補表 rank 1-4 はいずれも反駁証拠保持 (16757: b018, 20421: d002,
16371: e002, 30345: b018のs5 528497) のため、反駁証拠のない次候補として
reaudit closure-classes rank 5 のクラス12264に着手する。

- 対象: `research/experiments/n11-centralreply-closure-class12264-batch5-20261122/`。
  graph class index 12264, mask `[1152921504606848033, 0]` の未確定canonical
  S5子51件（f001-f051、reaudit正本probe-worklistのprobe_order順・Board再計算
  合法手数固定、root first=0/third=5を含むグループ群担当・graph cost size 52中
  51 unknown）。全キーは正本merged cache（5,924行・sha256 `8a721a18...`）に
  存在しないことを機械確認済み (0 hits)。
- 手法・停止規則・消費規則: Part B/C/D/Eと同一 (pinned replica `jsreplay.js`
  sha256 `84585617...`, 2-pass fresh cold, budget 15M, mismatch→HARD-STOP rc=42,
  WIN→HALT rc=45, 枯渇=UNKNOWN, 消費はfail-closed merger経由のみ、
  本batch単体では閉鎖・被覆・secured主張なし)。val-gate 4/4 node-exactは
  本ホストで本session中に再現済み (batch5 val-gateに同outputを固定)。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。


## Part G (verifier, amendment 2026-11-22): closure WINs third-implementation cross-verification

batch5 (Part F) はWIN-HALT (f017) で停止した。現時点で4つのWIN
(b018/d002/e002/f017, いずれも2-pass node-exact・pinned jsreplay replica @15M)
がscrutiny ownerの採用判断待ちで未消費。事前登録の採用ゲートはC++第二実装
(`cpp/solvers/kyouen_dfpn_root.cpp` pin `9193f5b6...`) だが本レーン環境は
コンパイラなし・パッケージ導入禁止のため実行不能のまま。前例
(`research/experiments/n11-sixthcost-third-implementation-verdict-reverification-20261121/`)
に従い、第三実装 (third implementation) (非df-pn AND/ORミニマックス `third_impl.js`,
pin sha256 `08ea958f...`) によるverdict-level交叉検証を、採用判断の追加
補強材料として実行する。**verdict不消費・採用判断は引き続きscrutiny owner。**

- 対象: `research/experiments/n11-centralreply-closure-wins-thirdimpl-reverify-20261122/`。
  4 WIN行 (b018/d002/e002/f017) の全行再検証 + 未消費LOSS行の層化サンプル
  spot検証10行 (d001/d003/d004/e001/f001/f005/f009/f013/f016/f018)。
  入力はpublished batch rawから `scripts/make_inputs.py` で機械導出
  (fail-closed・手転写ゼロ・source raw自体の2-pass node-exactチェック込み)。
- 前提ゲート (いずれも必須・fail-closed): script pin 3種 (third_impl
  `08ea958f...` / verify_tbl `c8c52528...` / jsreplay replica `84585617...`)、
  rule-engine gate (verify_tbl.js: quad 95,670 == replica / TBL==wob
  mismatches 0)、anchor行 (k02 WIN 9,106,337 expansions / l1 LOSS
  7,660,602 expansions) の本ホスト再現がpublished値と完全一致、negative
  gate 2種 (legal+1, stones+1 → GATE_FAIL)。
- 手法: 1行1プロセス、cap 300M expansions、wallcap 240s、1行2回 (a/b)
  のdeterminism gate (result/expansion/ttHits/reason 同一必須)。
  wall超過 (runlimit) はhonest wall-inconclusive として記録し検証主張と
  しない。cleanなverdict一致のみ「第三実装verdictがpublished replica
  verdictと一致した」という文献として記録する。cleanな不一致はdivergence
  evidenceとして記録するが、本レーンではverdictを書き換えない。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・verdict不消費
  (採用は引き続きscrutiny owner・C++ゲート先行・不変)。11x11空盤・19
  central-reply roots・クラス閉鎖・第三手被覆は本検証のどの時点でも
  UNKNOWN/不変。nodes/expansionsを勝敗として読まない。
- 並走との不接触: 対象キーはclosure grindバッチ1-5のpublished raw由来で、
  他レーン (six-row/seven-row/five-row/SAT系) のclaim集合と無関係。
  同一スコープの宣言がmainに存在する場合は着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。


## Part G addendum (verifier, amendment 2026-11-22): extend the LOSS spot sample to all unconsumed rows

Part G の10行層化サンプルは全行verdict一致で完了した (audit 171/171 gates)。
未消費パケット (4 WIN + 21 LOSS) の第三実装被覆を完全にするため、
残る11行 (f002/f003/f004/f006/f007/f008/f010/f011/f012/f014/f015) も
同一手法 (pinned third_impl.js・1行1プロセス・2-run determinism・
同一audit gate群) で検証する。verdict不消費・閉鎖・被覆・root主張なしは
Part Gと完全に同一。入力はpublished batch5 rawから機械導出
(make_inputs.pyのLOSS対象を21行全数に拡張)。
- 本addendum observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。
