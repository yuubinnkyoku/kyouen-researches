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
