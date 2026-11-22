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


## Part H (verifier, amendment 2026-11-22): joint 4-WIN adoption IF-ADOPTED analysis - read-only planning cost, verdicts not consumed

- 対象: `research/experiments/n11-central-reply-joint-4win-adoption-ifadopted-20261122/`。
  closure batch 1/3/4/5の未消費パケット25行 (4 WIN: b018/d002/e002/f017 +
  21 LOSS) を**まとめて採用した場合**のwhat-if分析。4つの単独IF-ADOPTED
  解析 (既出版) と同型のrefresh pipelineだが、merge対象を正本5,924行cache
  (sha256 `8a721a18...`) + 25行一括incrementとする。
- 手法: incrementはpublished batch rawから `scripts/make_joint_increment.py`
  が機械導出 (2-pass node-exact pinned-replicaチェック込み)。mergeは
  published `s5_union_merge.py` (selftest PASS含む) で5,949行・WIN162/
  LOSS5,787・衝突0・sha256 `88ef4388d727bf1b1da8a9a1be350479ab481870ff2dae2d34f6f70c6d892a9a`。
  refreshはpublished scriptのbyte-copy、cache pinのみ変更 (diff検証済)、
  2-run byte一致、root {60,27} baseline 119/119 free thirds fail-closed。
  delta抽出は `compare_joint_deltas.py` が機械ゲート: **加法性**
  (joint delta == 4単独deltaの和、11指標・0失敗)、win-hit class集合
  一致 (joint == union: 16757/20421/12264、e002はempty)、per-root free
  coverage不変、を検証。
- 結果 (machine-verified): excluded_now 23→**37** (非重複和+14)、
  free_now 33 不変、unknown 34,503→34,489、update8 remaining 31,838→
  **31,709** (加法的: -29-49+0-51)、win-hit 15 groups (16757:5 roots
  36/48, 20421:4 roots 12/37, 12264:6 roots 0/5)、joint greedy 35,617→
  **36,984** (**+1,367**; f017単独 +1,372より5安い=一括が単独採用より
  5だけ計画コストが安い)、probe worklist総量 65,213→65,183。
  合同採用はf017のroot 0/5 flipが支配的で**frozen 19root計画をscheduling
  levelで難しくする**という決定に資する測定値である。
- 重要な制約: `closure-classes.csv` はscheduling量でありclass statusを
  運ばない。合同採用下のranking上位は反駁クラスが占める (rank1-5 =
  16757/12264/20421/16371/30345)ので、**最初のclean候補はrank6 class
  5473** (`1158058422931816448:0`, unknown 51, first=26/third=59,
  4 groups)。廉価側は反駁quartetで食い尽くされており、blind batchは
  51-unknown scaleでWIN-denseが続くことを想定すべき測定値が出た。
- 主張と消費規則: 本分析もverdict不消費・閉鎖・被覆・root主張なし
  (単独解析4種と同一)。5,949行cacheはanalysis-only成果物でcanonical
 ではない。11x11空盤・19 central-reply roots・全クラスはUNKNOWNのまま。
  nodes/expansionsを勝敗として読まない。
- transport: `probe-worklist.csv` (~3.7MB) は運送上再出版しない
  (pinned入力からdeterministicに再生成可能、総量はrefresh-summary.json
  に記録、READMEに開示済み)。
- 並走との不接触: 既存4単独解析の拡張で、他レーンのclaim集合と無関係。
  同一スコープの宣言がmainに存在する場合は着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。


## Part H-bis (verifier, amendment 2026-11-22): packet WIN-vs-LOSS decomposition - RETRACTS Part H's mechanism attribution, verdicts not consumed

- 対象: 2実験。
  `research/experiments/n11-central-reply-packet-minus-f017-ifadopted-20261122/`
  (P24: 25行パケットからf017 WIN行のみを除いた24行シナリオ) および
  `research/experiments/n11-central-reply-packet-win-vs-loss-decomposition-ifadopted-20261122/`
  (P4 = 4 WIN行のみ / P17 = batch12264のf-LOSS 17行のみ / P21 = 21 LOSS行のみ)。
  いずれも正本5,924行cache (sha256 `8a721a18...`) へのmerge + published
  refresh pipeline (selftest PASS・2-run byte一致・root {60,27} 119維持)。
  増分はpublished 25行packet increment (sha256 `d49e2824...`) からの機械
  分解/機械除隊 (f017およびf-rowのkeyはkit rawからfail-closed再導出)。
- **正誤 (RETraction)**: Part Hが記載した「joint greedy +1,367の原因は
  f017採用 (root 0/5 flip) が支配的」という機構帰属は本分解で機械反駁
  され、撤回する。訂正版: 4 WIN**のみ**採用ではgreedyは**−1** (plan-cost
  中立)、f-batchの17 LOSS行**のみ**で**+1,372**、f017 WINを除いたpacket
  (P24) でもfull packet (P25) と同一の**36,984**。per-root free coverageは
  全シナリオでbaselineと同一 (flipは一度も起きていない。「root 0/5 flip」
  はupdate8 win-hit groupのindex誤読)。f017単独シナリオの+1,372もその
  incrementに含まれる17 f-LOSS行の効果であり、WINの効果ではない。
- 機械検証済みの分解表 (baseline対比): P4 = excluded 37 (+14) /
  unknown 34,489 (−14) / update8 remaining 31,709 (−129) / win-hit 15
  groups (16757:5, 20421:4, 12264:6) / greedy 35,616 (−1) / worklist
  65,208 (−5)。P17 = excluded 23 (不変) / remaining −17 / resolved +17 /
  greedy 36,989 (+1,372)。P21 = greedy 36,985 (+1,368) / remaining −20 /
  resolved +20。P24 = excluded 34 (+11) / remaining −95 / win-hit 9 /
  greedy 36,984。加法性: 9指標中8つで delta(P25) == delta(P4)+delta(P21)
  (機械ゲート)。唯一の例外はupdate8 remaining (−129−20=−149≠−129、
  WIN側解決がLOSS側を_Exactly 20_だけ包含、機械検証)。
- 決定に資する要約: (1) 4 WINの採用可否は**計画コストと分離して**判断
  できる。WINのみ採用はWIN側便益のすべて (excluded +14, unknown −14,
  remaining −129, win-hit 15) を計画コストほぼゼロ (−1) でもたらす。
  (2) +1,367はbatch12264のf-LOSS完備の性質であり、どのWINの消費決定にも
  依存しない。(3) class status (excluded/free/unknown) は**WINのみ**
  駆動であり、LOSS行はscheduling option pool (resolved/worklist/greedy)
  のみを動かす。
- closure ranking: 全packetシナリオで先頭5位は反駁quartet+30345、
  first clean candidateはrank6 class 5473 (`1158058422931816448:0`,
  unknown 51) で不変。
- 主張と消費規則: verdict不消費・閉鎖・被覆・root主張なし。4つの
  scenario cache (P4 5,928行/P17 5,941行/P21 5,945行/P24 5,948行) は
  analysis-only成果物でcanonicalではない。11x11空盤・19 roots・全クラス
  はUNKNOWNのまま。nodes/expansionsを勝敗として読まない。
- transport: 各シナリオのprobe-worklist (~3.7MB) は再出版しない
  (pinned入力から再生成可能、総量は各refresh-summary.jsonに記録)。
- 並走との不接触: 既存Part Hのシナリオ拡張のみで、他レーンのclaim集合と
  無関係。同一スコープの宣言がmainに存在する場合は着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。


## Part I (solver, amendment 2026-11-22): closure class 5473 exact-S5 probe batch 6

batch5 (Part F) もWIN-HALT (f017) で停止した。Part H-bisの合同分解解析に
より、closure候補表 rank 1-5 はどの採用シナリオでも反駁証拠保持
(16757: b018, 20421: d002, 30345: b018のs5 528497, 16371: e002,
12264: f017) であり、first clean candidate は reaudit closure-classes
rank 6 のクラス5473であることが確定している。安価側WIN密集
(5バッチ中4 WIN-HALT) の実測傾向とスコアリング再考推奨はPart H-bisで
記録済みだが、rank 1-5が反駁証拠保持である以上、バッチ選択はscheduling
quantityとして反駁証拠のない次候補クラス5473に着手する。

- 対象: `research/experiments/n11-centralreply-closure-class5473-batch6-20261122/`。
  graph class index 5473, mask `[1158058422931816448, 0]` の未確定canonical
  S5子51件（g001-g051、reaudit正本probe-worklistのprobe_order 230-280順・
  Board再計算合法手数固定、root first=26/third=59を含む4グループ担当・
  unknown_now 51）。fail-safe機械確認: (1) reaudit worklist再生 — pinned
  inputs + `refresh_19root_frontier.py` により `probe-worklist.csv`
  (65,213行) はpublished reaudit出力とbyte-identicalに再現、
  (2) 全51キーは正本merged cache（5,924行・sha256 `8a721a18...`）に
  存在しない (0 hits)、(3) quarantine registry (sha256 `81d23160...`)
  とのkey対照 0 hits。
- 手法・停止規則・消費規則: Part B-Fと同一 (pinned replica `jsreplay.js`
  sha256 `84585617...`, 2-pass fresh cold, budget 15M, mismatch→HARD-STOP
  rc=42, WIN→HALT rc=45, 枯渇=UNKNOWN, 消費はfail-closed merger経由のみ、
  本batch単体では閉鎖・被覆・secured主張なし)。val-gate 4/4 node-exactは
  本ホストで本session中に再現済み (batch5 val-gateと同一4入力行: at2m×2
  result 0/2,000,000、15m result 2/3,651,923 と result 2/5,040,200)。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。


## Part J (verifier, amendment 2026-11-22): batch-6 g018 if-adopted decomposition + joint 5-WIN packet - read-only planning, verdicts not consumed

batch6 (Part I) はWIN-HALT (g018) で停止した。5つの未消費closure WIN
(b018/d002/e002/f017/g018) がある状態で、Part H-bisの手法（WIN-only /
LOSS-only / full の機械分解・加法性を測定で確認）をbatch 6とjoint設定
の双方に適用し、scrutiny owner向けの採用帰結を出版する。verdictは一切
消費しない。

- 対象1: `research/experiments/n11-central-reply-class5473-win-g018-ifadopted-20261122/`。
  3シナリオ (PWIN18=g018 WINのみ / PLOSS17=17 LOSSのみ / PFULL18=全18行)、
  増分はbatch6 rawからfail-closed生成、merge衝突0、各シナリオrefresh
  2回byte-identical、root {60,27} 119/119不変。測定: WINのみ採用で
  excluded 23→27 (4クラス 4889/4892/5473/5501, s5 184684保持)・update8
  remaining 31,838→31,787 (root26 -102 / root49 -102)・win-hit 4群 (全部
  class 5473経由)・**joint greedy全シナリオで35,617不変** (batch 6は
  計画コスト中立・f-batchと対照的)。LOSS行はresolved (+17) とworklist
  (−20) のみ加法的に動かす。remainingのWIN側包含 (−51+−17 = −51) は
  Part H-bisと同型。
- 対象2: `research/experiments/n11-central-reply-joint-5win-adoption-ifadopted-20261122/`。
  PJ5WIN (canonical + 4-WIN増分 + g018 WIN-only, 5,929行) とPJ5FULL
  (P25 packet cache + batch6 18行, 5,967行)。5 WINのみ: excluded 41
  (+18加法的)・remaining 31,658 (−180 = −129−51加法的)・win-hit 19群
  (16757:5/20421:4/12264:6/5473:4加法的)・greedy 35,616 (−1で中立)。
  43行フル: greedy 36,984 (Part H packetと同値・batch6行は追加増なし、
  H-bisの帰属をjoint設定で確認)。worklist 65,163 (−50加法的)。
- 採用規則は不変: WIN行の採用判断はscrutiny owner (C++第二実装 pin
  `9193f5b6...` 前例)。本レーンはいかなるverdictも消費しない。
  標準11×11空盤・19 root・全クラスは引き続きUNKNOWN。


## Part K (verifier, amendment 2026-11-22): batch 6 g018 third-implementation cross-verification

batch 6 (Part I) は事前登録のWIN-HALT規則により g018 (2-pass node-exact
result 1, 5,936,863 nodes, s5_index 184684, key `[1734519175235239936, 0]`)
で停止した。Part Gの前例に従い、batch 6のwin行 g018 と層化LOSS spot 3行
(g001/g011/g016) を第三実装 (`third_impl.js` pin `08ea958f...`) で
verdict-level交叉検証する。**verdict不消費・採用判断は引き続きscrutiny owner
(C++第二実装 gate pin `9193f5b6...` 前例・不変)。**

- 対象: `research/experiments/n11-centralreply-closure-batch6-g018-thirdimpl-20261122/`。
  target 4行 (g018 WIN + g001/g011/g016 LOSS)・anchor 2行 (k02a/l1a,
  Part Gと同一のpublished第三実装値 9,106,337/4,991,527 と
  7,660,602/3,951,175)・negative 2行 (ng1/ng2)。入力はpublished batch6 raw
  由来のrows.json + input CSVで機械固定 (fail-closed・keyの手転写なし)。
- 手法: Part Gと完全同一 (script pin 3種同一、1行1プロセス、cap 300M、
  wallcap 240s、a/b 2回determinism、rules-gate quads 95,670/triples
  195,044 mismatch 0、audit.py fail-closed 2回byte一致)。
- 結果 (machine-verified): **audit 71/71 gates PASS (2回byte一致)**。
  anchor両行はpublished値と完全一致。target 4行は全行clean・a/b同一・
  verdict一致 (g018 WIN 6,776,591 expansions / g001 LOSS 4,143,095 /
  g011 LOSS 9,926,469 / g016 LOSS 1,690,556)。negative 2行は文言一致の
  GATE_FAIL。wall-inconclusive 0行。
- 運用上の開示: 本cross-verificationはPart G宣言時には未存在のbatch 6を
  対象とするため、Part G宣言の目的外である。実行は同一レーンでverdict
  不消費のverifier作業として完了した後、本amendment (Part K) を出版時に
  追記して記録範囲を確定した。11x11空盤・19 central-reply roots・全クラスは
  本検証のどの時点でもUNKNOWNのまま。nodes/expansionsを勝敗として読まない。
- transport: 対象はpublished batch6 raw由来のみで、他レーンのclaim集合と
  無関係。同一スコープの宣言がmainに存在する場合は着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。


## Part L (solver, amendment 2026-11-22): closure class 10324 exact-S5 probe batch 7

batch 6 (Part I) も事前登録のWIN-HALT規則により g018 (2-pass node-exact
result 1, 5,936,863 nodes) で停止し、closure候補表 rank 1-6 はすべて反駁証拠保持
(16757: b018, 20421: d002, 30345: b018のs5 528497, 16371: e002, 12264: f017,
5473: g018) となった。反駁証拠のない次候補として reaudit closure-classes
rank 7 のクラス10324に着手する。5バッチ中5 WIN-HALTの実測傾向とスコアリング
再考推奨はPart H-bisで記録済みだが、rank 1-6が反駁証拠保持である以上、
バッチ選択はscheduling quantityとして反駁証拠のない次候補に着手する。

- 対象: `research/experiments/n11-centralreply-closure-class10324-batch7-20261122/`。
  graph class index 10324, mask `[1152921504607191040, 0]` の未確定canonical
  S5子51件（h001-h051、reaudit正本probe-worklistのprobe_order 281-331順・
  Board再計算合法手数固定、root first=14/third=16を含む4グループ担当・
  unknown_now 51）。fail-safe機械確認: (1) 使用するprobe-worklist・
  closure-classes はpublished reaudit出力とbyte-identical (sha256
  `cbea9e79...`・両コピー一致)、(2) 全51キーは正本merged cache（5,924行・
  sha256 `8a721a18...`）に存在しない (0 hits)、(3) quarantine registry
  (sha256 `81d23160...`・active 4件) とのkey対照 0 hits。
- 手法・停止規則・消費規則: Part B-Iと同一 (pinned replica `jsreplay.js`
  sha256 `84585617...`, 2-pass fresh cold, budget 15M, mismatch→HARD-STOP
  rc=42, WIN→HALT rc=45, 枯渇=UNKNOWN, 消費はfail-closed merger経由のみ、
  本batch単体では閉鎖・被覆・secured主張なし)。val-gate 4/4 node-exactは
  本ホストで本session中に再現済み (batch6 val-gateと同一4入力行: at2m×2
  result 0/2,000,000、15m result 2/3,651,923 と result 2/5,040,200)。
- 並走との不接触: 本batchキーは19-root計画universe由来であり、他レーンの
  claim集合と機械的にdisjoint (merged cache不在確認済み)。同一スコープの
  宣言が既にmainにある場合は本宣言を破棄して着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。


## Part M (verifier, amendment 2026-11-22): batch 7 (class 10324) increment merge + free re-audit - class 10324 certified as the 34th free class

batch 7 (Part L) は51/51全LOSS (2-pass node-exact, WIN-HALTなし・枯渇なし) で
完走した。Part C (23963) と同一の閉鎖機構で消費・再監査を行う。

- 対象: `research/experiments/n11-central-reply-10324-closure-reaudit-20261122/`。
  increment 51行 (sha256 `39b975e8...`) はpublished rawからfail-closed生成
  (2-pass (result,nodes,legal) 一致・key一致assert込み)。mergeはpublished
  `s5_union_merge.py` (selftest PASS) で正本5,924行 (`8a721a18...`) + 51行 →
  **5,975行 (WIN 158 / LOSS 5,817)・衝突0・重複0**、出力sha256
  `a998f4c0b13383cb50bbbdb60761182722ba45280fd585739ad5d08bc182ed1b`。
  refreshはpublished scriptのbyte-copy (cache pin 2行のみ変更・diff検証済)、
  他のpinned inputs 5種は正本sha一致、**2-run全出力byte-identical**。
- 結果 (machine-verified): **class 10324 = Board検証済み34番目のfree class**
  (`free_now` 33→34、`board_verification` 34/34・rejected 0、`unknown`
  34,503→34,502、excluded系は不変=新規WIN流入なし)。root第三手被覆は
  **244→248** (root 14: 6→8、root 16: 10→12)。update8 `remaining_now`
  31,838→31,836 (−2、新規resolved 2件 = batch7のh043 (s5 362082) と
  h051 (s5 362090))、`win_hit_groups` 空のまま。scheduling量: joint greedy
  35,617→35,857 (+240、LOSS側option-pool効果・Part H-bisのf-batchと同方向)、
  probe worklist 65,213→65,155 (−58)、closure rankingから10324は全面消失・
  反駁証拠のない首位候補は**rank 7 class 2634** (`[4035225266258182144, 0]`、
  unknown 51)。
- 消費と主張の範囲: 消費したのはbatch 7の51 LOSS行のみ。b018/d002/e002/
  f017/g018の5 WINは引き続きscrutiny owner待ちで不消費。Class 10324のfree
  状態はmerge cacheからのderived class statusであり、**標準11×11空盤・19
  central-reply rootsは引き続きUNKNOWN**。nodesを勝敗として読まない。
- transport: probe-worklist (~3.7MB) は再出版しない (pinned inputs + script
  からbyte-identicalに再生成可能、総量はrefresh-summary.jsonに記録)。
- 並走との不接触: batch7由来キーのみ。同一スコープの宣言がmainに存在する
  場合は着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。


## Part N (prober, amendment 2026-11-22): batch 8 (class 2634, rank 7) declared - next clean candidate opened under the batch-7 protocol

Part Mのclosure rankingで反駁証拠のない首位候補となったrank 7 class 2634
(mask `[4035225266258182144, 0]`、unknown 51、1 group first=49/third=71) を
batch 7 (Part L) と同一の予登録protocolで着手する。

- 対象: `research/experiments/n11-centralreply-closure-class2634-batch8-20261122/`。
  keys 51本 (h001-h051) はPart M refresh再生成worklist (65,155行、sha256
  `ca3ee3bc...`、worklist自体はregenerableのため未再出版) の
  `serving_class=2634` 行 (probe_order 281-331) で、batch-keys.jsonに全行
  published (正本cache・update8機構に対して独立照合可能)。
- fail-safe (宣言前に機械照会済み): (1) canonical merged cache 5,975行
  (`a998f4c0...`) に51/51 keys不在 (0 hits); (2) quarantine registry
  (`81d23160...`) のactive 2件とのkey対照0 hits (hi=128の
  10448914085452972032:128はquarantineの10448351135499552768:128とは別key);
  (3) solverはpinned replica `jsreplay.js` (`845856173d...`、batches 1-7と
  byte-identical)、budget 15M・2-pass fresh cold・node-exact gate。
- val-gate: published two-target-design 4行を本ホストで再現、4/4 node-exact
  (at2m result 0/2,000,000 ×2、15m result 2/3,651,923 と result 2/5,040,200)。
- **erratum (batch-7 README)**: 宣言時のfail-safe記載「quarantine 4 active
  entries」は、pinned registry (`81d23160...`、published bytes確認済み) の
  実際の内容である**2 active entries**への誤記。key対照0 hitsの結論に影響
  なし。batch-7 READMEの当該行をerratum明記付きで訂正し、本Part Nにも記録する。
- 主張の範囲: 本batchはcoverage・closure・rootを一切主張しない。WIN-HALT
  (rc=45) が発火した場合はそのkeyで停止しif-adopted解析に回す (予登録
  stop rule)。全51本LOSSでも消費はfail-closed increment merge + refresh
  再監査まで行わない。**class 2634・19 roots・標準11×11空盤はUNKNOWN**。
- 並走との不接触: 同一スコープ宣言がmainに存在する場合は着手しない
  (宣言前にlatest mainを再取得しclass2634実験目录の不在を確認済み)。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part O (verifier, amendment 2026-11-22): batch 7 (class 10324) 第三実装交叉検証の出版 - 閉鎖済みevidence bundleへのpost-hoc補強 (verdict不消費)

repo 404障害 (2026-11-22 ~04:52Z) 中にkit lettering "Part M"・タイムスタンプ
2026-11-22T05:58Z で事前登録されたbatch-7全51行の第三実装交叉検証を
`research/experiments/n11-centralreply-closure-class10324-batch7-thirdimpl-reverify-20261122/`
として出版する。repo letteringでは Part M がbatch-7 closure merge + re-auditに、
Part N がbatch 8 (class 2634) に使用済みのため、本amendmentをPart Oとして
採番した (kit lettering "Part M" → repo Part O の写像は実験READMEにも開示)。

- 成果 (machine-verified・verdict不消費): 第三実装 (`third_impl.js` pin
  `08ea958f...`) によるbatch-7全51行のverdict-level交叉検証。51/51行で
  published pinned-replica verdict (result 2 LOSS) と第三実装verdictが一致
  (third実装expansions 2,436,068-8,744,134、a/b 2-run determinism identical)。
  出版セッションによる出版前機械再照合: input rows.jsonのreplica (result,nodes)
  はpublished batch-7 status.logと51/51行完全一致・key (lo:hi) はbatch-keys.json
  と51/51一致・script pin 3種 (`08ea958f...`/`c8c52528...`/`84585617...`) は
  published実験群とbyte一致・MANIFEST 174/174 OK。
  anchor 2行 (k02 WIN 9,106,337 expansions/4,991,527 ttHits・l1 LOSS
  7,660,602/3,951,175) はpublished第三実装値と完全一致、negative gate 2種
  (ng1/ng2) は文言一致のGATE_FAIL、rules gate (quads 95,670・triples 195,044
  mismatch 0) PASS、audit.py 541/541 gates PASS (2回実行byte一致)、
  wall-inconclusive 0行。
- 出版時の位置づけ: staging時点ではbatch-7のmerge + re-auditは未出版だったが、
  出版時点でnote Part Mとしてmainに存在する (class 10324 = Board検証34番目
  free class・正本cache 5,975行 `a998f4c0...`)。よって本amendmentは閉鎖済み
  class 10324のevidence bundleに対するpost-hocなcross-implementation
  corroborationであり、採用規則・証明責任に変更を与えない。
- 主張の範囲: verdict不消費・閉鎖・被覆・root主張なし。5つの未消費WIN
  (b018/d002/e002/f017/g018) はscrutiny owner待ちのまま。標準11×11空盤・
  19 central-reply roots・全closure classはUNKNOWNのまま。nodes/expansionsを
  勝敗として読まない。
- 並走との不接触: batch-7由来キーのみを対象とし、進行中のbatch 8 (Part N,
  class 2634) のscopeと無関係。同一スコープの宣言がmainに
  存在する場合は着手しない。
- 本amendment observed HEAD-before-push: `0fddb890` (Part O実験3コミット
  `eb061b60`/`0dfdc4df`/`0fddb890` 直後のmain)。

## Part P (verifier, amendment 2026-11-22): batch 2 (class 23963, 最初のfree class) 消費済み48行の第三実装交叉検証 (verdict不消費・事後補強)

class 23963 (batch 2, Part C) は48/48全LOSS (2-pass node-exact, budget 15M) で
完走し、fail-closed merge + refresh再監査により最初のBoard検証free class
(33番目) として閉鎖・消費済み。Part G (batches 1/3/4/5)・Part K (batch 6)・
Part O (batch 7全51行) に続き、**消費済みevidence bundleに対する事後の
cross-implementation補強**として、batch 2の48行 (c001-c048) を第三実装
(`third_impl.js` pin `08ea958f...`) でverdict-level交叉検証する。Part Oと
完全同一の規約・前提ゲート・停止規則を用いる。

- 対象: `research/experiments/n11-centralreply-closure-class23963-batch2-thirdimpl-reverify-20261122/`。
  target 48行 (c001-c048, published正本rawでは全行result 2 LOSS・2-pass
  node-exact)・anchor 2行 (k02a/l1a, Part G/K/Oと同一のpublished第三実装値
  9,106,337/4,991,527 と 7,660,602/3,951,175)・negative 2行 (ng1/ng2)。
  入力はpublished batch-2 raw (kit鏡像はrepo正本とbyte一致を機械確認の上
  使用) から `make_inputs_batch2.py` がfail-closed導出 (手転写ゼロ・
  raw 2-pass一致assert・key/legalをpublished batch-keys.jsonと機械照合・
  replica verdictは全行LOSS 2を要求)。
- 前提ゲート (いずれも必須・fail-closed): script pin 3種 (`08ea958f...` /
  `c8c52528...` / `84585617...`)、rule-engine gate (verify_tbl.js: quads
  95,670・triples 195,044 mismatches 0)、anchor 2行の本ホスト再現が
  published値と完全一致、negative 2種の文言一致GATE_FAIL。
- 手法: 1行1プロセス、cap 300M expansions、wallcap 240s、1行2回 (a/b)
  のdeterminism gate (result/expansion/ttHits/reason同一必須)。
  wall超過 (runlimit) はhonest wall-inconclusiveとして記録し検証主張と
  しない。
- **消費済み注意**: 23963の48行は既に正本cacheへ消費済み。本検証のcleanな
  verdict一致はevidence bundleの事後補強文献のみを作成する。cleanな
  不一致 (divergence) が発生した場合はdivergence evidenceとして記録する
  が、verdict・正本cacheを本検証で書き換えない (訂正は別個のfail-closed
  手続き + scrutiny owner判断を要する)。
- 主張の範囲: verdict不消費・閉鎖・被覆・rootの新主張なし。標準11×11
  空盤・19 central-reply roots・全closure classはUNKNOWNのまま。
  nodes/expansionsを勝敗として読まない。
- 並走との不接触: batch-2由来のpublishedキーのみを扱い、進行中のbatch 8
  (Part N, class 2634) と無関係。同一スコープの宣言がmainに存在する場合は
  着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part P 出版status update (2026-11-22, verifier)

Part P (batch 2 / class 23963 消費済み48行の第三実装交叉検証) は実行・出版
済み。本amendmentの宣言通りverdict不消費・事後補強文献のみ。

- 実行結果: 48行すべてa/b 2回実行byte一致。third-impl expansions
  636,315〜4,341,425 (replica df-pn nodes 579,880〜3,815,424)。anchors
  k02a (WIN 9,106,337/4,991,527) と l1a (LOSS 7,660,602/3,951,175) は本
  ホスト再現値がpublished第三実装値と完全一致 (node-exact)。negative
  ng1/ng2 は文言一致GATE_FAIL。audit.py (fail-closed, 2回実行byte一致)
  は **511/511 gates PASS、48/48 LOSS verdict一致、divergence 0、
  wall-inconclusive 0**。
- 出版: `n11-centralreply-closure-class23963-batch2-thirdimpl-reverify-20261122`
  commits a84f8254 (scaffold 63 files) → cb739fcd (targets 96 files) →
  dbd7c5c2 (anchors 4 + negative 2 + audit-summary.json)。fetch-back:
  commit-pinned raw URL + cmp で 166/166 files のbyte一致を確認済み。
- sources/: published batch-2 raws 96をrepo正本から再取得し96/96でbyte
  一致を機器確認の上使用。batch-keys.json (sha256 `3b37c923...`) は非再
  出版・READMEにsha記載。
- verdict・正本cacheへの影響なし。標準11×11空盤・19 central-reply
  roots・全closure classはUNKNOWNのまま。nodes/expansionsを勝敗として
  読まない。

## Part Q (prober, amendment 2026-11-22): batch 9 (class 1518, rank 8) declared - 進行中でない次位のclean candidateをbatch-7 protocolで開始

Part Mのclosure rankingで、進行中のbatch 8 (Part N, class 2634, rank 7)を除く
反駁証拠のない首位候補であるrank 8 class 1518 (mask `[1152921505076609024, 0]`、
unknown 51、1 group first=26/third=28)をbatch 7 (Part L) と同一の予登録protocol
で着手する。

- 対象: `research/experiments/n11-centralreply-closure-class1518-batch9-20261122/`。
  keys 51本 (j001-j051) はPart M refresh再生成worklist (65,155行、sha256
  `ca3ee3bc7772ff38462cb60fc41ab4570cb236a880213322de230410fa550e80`、worklist
  自体はregenerableのため未再出版) の `serving_class=1518` 行 (probe_order
  332-382) で、batch-keys.jsonに全行published (正本cache・update8機構に対して
  独立照合可能)。宣言前に本ホストでPart M refresh機材を再実行し、
  closure-classes.csv・refresh-summary.json・per-root-coverage.csvの3成果物が
  published Part M bytesとbyte一致 (fail-closed)・worklist shaがPart N記載値と
  一致することを確認済み。
- fail-safe (宣言前に機械照会済み): (1) canonical merged cache 5,975行
  (`a998f4c0...`) に51/51 keys不在 (0 hits); (2) quarantine registry
  (`81d23160...`) のactive 2件とのkey対照0 hits (両方向); (3) solverはpinned
  replica `jsreplay.js` (`845856173d...`、batches 1-8とbyte-identical)、
  budget 15M・2-pass fresh cold・node-exact gate。
- val-gate: published two-target-design 4行を本ホストで再現、4/4 node-exact
  (at2m result 0/2,000,000 ×2、15m result 2/3,651,923 と result 2/5,040,200)。
- 主張の範囲: 本batchはcoverage・closure・rootを一切主張しない。WIN-HALT
  (rc=45) が発火した場合はそのkeyで停止しif-adopted解析に回す (予登録
  stop rule)。全51本LOSSでも消費はfail-closed increment merge + refresh
  再監査まで行わない。**class 1518・19 roots・標準11×11空盤はUNKNOWN**。
- 並走との不接触: 進行中のbatch 8 (Part N, class 2634) には一切手を触れない。
  観測として、published batch-8 batch-keys.jsonのclass_mask下位bitに十進転記
  drift (...182000 vs canonical ...182144) を検出したが、51 keys自体はcanonical
  worklist行と51/51で一致しており、本batchはこれをbatch-9 READMEの
  non-interference noteに記録するのみでbatch-8ファイルを修正しない。
  同一スコープの宣言がmainに存在する場合は着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。
