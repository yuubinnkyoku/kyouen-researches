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
- 並走との不接触: 本b
atchキーは19-root計画universe由来であり、
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
  全キー
は正本merged cache（5,924行・sha256 `8a721a18...`）に存在しないことを
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

- 対象: `resea
rch/experiments/n11-centralreply-closure-class12264-batch5-20261122/`。
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
  7,660,602 expansions) の本ホスト再現がpub
lished値と完全一致、negative
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
  LOSS5,787・衝突0・sha256 `88ef4388d727bf1b1da8a9a1be350479ab481870ff2da
e2d34f6f70c6d892a9a`。
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
  (P4 = 4 WIN行のみ / P17 = batch12264のf-LOSS 17
行のみ / P21 = 21 LOSS行のみ)。
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
LOSS-only / full の機械分解・加法性を測定で
確認）をbatch 6とjoint設定
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
  sha256 `84585617...`, 2-pass fresh
 cold, budget 15M, mismatch→HARD-STOP
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
  状態はmerge cacheからのderive
d class statusであり、**標準11×11空盤・19
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
  (宣言前にlatest mainを再取得しcl
ass2634実験目录の不在を確認済み)。
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
- 本amendment observed H
EAD-before-push: `0fddb890` (Part O実験3コミット
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
- 本a
mendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

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


## Part R (verifier, amendment 2026-11-22): batch 9 (class 1518) j033 if-adopted decomposition - read-only planning, verdicts not consumed

batch 9 (Part Q) は事前登録のWIN-HALT規則により j033 (2-pass node-exact
result 1, 4,718,280 nodes, s5_index 69347, key `[1153484455030030336, 0]`,
legal 80, probe_order 364) で停止した。Part H-bis / Part J と同一の手法
(WIN-only / LOSS-only / full の機械分解・加法性測定) をbatch-9の33行
(32 LOSS + 1 WIN) に適用し、scrutiny owner向けの採用帰結を出版する。
verdictは一切消費しない。

- 対象: `research/experiments/n11-central-reply-class1518-win-j033-ifadopted-20261122/`。
  3シナリオ (PWINJ033 = j033 WIN行のみ / PLOSS32 = 32 LOSS行のみ /
  PFULL33 = 検査済み全33行)、増分はpublished batch-9 rawからfail-closed生成
  (2-pass node-exact・legal/key照合込み、sha256は実験README記載)。mergeは
  published mergerで正本5,975行 (`a998f4c0...`) + 増分・衝突0・重複0
  (5,976 / 6,007 / 6,008行)。refreshはpublished scriptのbyte-copy
  (差分3行: depth行・cache path行・sha pin行、diff検証済み) を各シナリオ
  2回実行し全4出力がbyte-identical (6/6 runs)。root {X,60,27} baseline
  119/119 free thirds不変。
- delta抽出は `compare_batch9_deltas.py` が機械ゲート: 依存graphから機械
  特定した s5 69347 cost-child保持クラス {1518, 4843} (両者base-unknown) が
  PWINのclosure-classes unknown変化行集合と完全一致、PFULLとPLOSSの
  per-class unknown差分行 (−1) も同一集合、excluded_now +2、per-root free
  coverageは全シナリオでbaselineと完全一致、を検証して失敗なし。
- 測定 (baseline対比, machine-verified): PWINJ033 = excluded 23→25 (+2,
  classes 1518自己 + 4843) / unknown 34,502→34,500 / update8 remaining
  31,836不変・win-hit 0 (j033はupdate8 win-hit群を持たない、g018の
  4群と対照的) / joint greedy 35,857→35,856 (−1) / worklist 65,155→
  65,153 (−2)。PLOSS32 = excluded不変 / resolved 23→24 (j016 → s5 69330) /
  remaining −1 / joint greedy → 35,235 (**−622, closure grindでは初の
  greedy削減**・batch-5 f-packetの+1,372やbatch-6の中立と対照的; 主因は
  root 15 −75とroot 26 −72) / worklist −44。PFULL33 = excluded +2 /
  resolved +1 / remaining −1 / greedy −622 / worklist −46 (**加法的: −2−44
  = −46**; greedyはWIN側−1がLOSS側集合に包含されsub-additive by 1)。
- class-1518 scheduling: PLOSS32でclass 1518のunknownは51→19・closure
  rank 1 (次キーj033)、PFULL33ではunknown 18・rank 1 (次キーj034, s5 69348)。
  いずれの採用シナリオでも、未着手のbatch-9残り (j034-j051の18キー) を含む
  class 1518完走がranking上最安の次手になる。class 4843はPWIN下でunknown
  58→57・rank 123→97。
- 主張と消費規則: verdict不消費・閉鎖・被覆・root主張なし (Part Jの単独
  if-adopted解析と同一規約)。3つのscenario cacheはanalysis-only成果物で
  canonicalではない。j033のWINは引き続きscrutiny owner待ち (採用ゲートは
  C++第二実装 pin `9193f5b6...` 前例・本環境では実行不能のまま)。
  third-impl (Part K/O/P方式) によるj033の交叉検証は本セッションでは
  未実施。標準11×11空盤・19 central-reply roots・class 1518/2634は
  UNKNOWNのまま。nodesを勝敗として読まない。
- transport: 各シナリオのprobe-worklist (~3.7MB, regenerable) は再出版
  しない (総量は各refresh-summary.jsonに記録)。
- 並走との不接触: 進行中のbatch 8 (Part N, class 2634) のファイルには
  一切接触しない。batch-9実験 (Part Q, commit `a321bfb2`まで) のpublished
  ファイルは修正しない。同一スコープの宣言がmainに存在する場合は着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part S: 出版状態検証 — transport破損疑いの撤回 + ワークスペースリセット記録 (2026-11-22)

- 前セッション末尾に、file_system.read_file のコンテンツ返却チャンク
  (累積約2000文字境界) への改行挿入挙動を観測したことから、
  「readAllで読んでpushした23ファイルのpublished blobが破損した」との疑いが
  生じ、修復コミットが計画されていた。本セッションでこれを検証した。
- 検証方法: push前のローカル正本 (消失前) から計算済みの git blob sha1
  (sha1("blob <len>\0" + content)) 32値と、GitHub get_file_contents が返す
  blob SHA を全32ファイルで照合した。結果: **32/32 完全一致。破損は
  最初から存在せず、疑いを撤回する**。追加で README.md と
  output/decomp-deltas-batch9.json は本文sha256照合でもbyte完全一致
  (`ff7b7dd9...` / `48ae2717...`)。コミット統計の行数 (+5977 等) も
  ローカル正本の wc -l と全件一致していた (行途中への改行挿入があれば
  増加するはずだった)。
- 教訓 (read-pathの事実として残す): read_fileのチャンク境界挙動は確認済みの
  読み取り側の挙動であり、publish-pathではなかった。両者を混同して推測を
  確定扱いにしたのが誤りだった。出版blobの検証は今後
  (a) get_file_contents の "SHA: <blob sha1>" 表示とローカル
  sha1("blob %d\0"+content) の照合、または (b) commit固定raw URL +
  sha256sum、で行う (両プロトコルは本環境で実証済み)。
- ワークスペースリセット: 本セッション中に実行環境がリセットされ、
  /home/user/work 配下のローカル作業ツリー (if-adopted作業一式) が消失した。
  影響はなし — batch-9正本raws (j001-j033) は kit batch1518/ ミラーが保持、
  if-adopted成果32ファイルはpublished正本から抽出しsha256全件一致 (32/32) を
  再確認のうえ kit batch1518-ifadopted/ へミラーした
  (MANIFEST-sha256.txt 34行付き)。repoが正本であるspecに変化はない。
- 状況はすべて不変: verdict不消費。j033 WINはscrutiny owner待ち。
  j034-j051 (18キー) 未着手。標準11x11空盤・19 central-reply roots・
  class 1518/2634 (batch-8/batch-9) はすべて UNKNOWN のまま。
  nodesを勝敗として読まない。
- 本amendment observed HEAD-before-push: `b8374c416ed39815231e29f3afa92ec192834d98`
  (K1058 small-boardレーン)。コミットメッセージにも同じHEADを記録する。


## Part T (verifier, amendment 2026-11-22): batch 9 j033 third-implementation cross-verification (declared before execution)

batch 9 (Part Q) はWIN-HALT (j033) で停止し、Part Rのif-adopted解析は出版済み。
Part K/O/Pの前例に従い、batch-9のwin行 j033 (2-pass node-exact result 1, 4,718,280
nodes, s5_index 69347, key `[1153484455030030336, 0]`, legal 80, probe_order 364) と
層化LOSS spot 3行 (j001 / j016 / j027 — replica nodes 7,908,824 / 9,112,205 /
1,255,316 でbatch-9 nodes幅をほぼ全幅) を第三実装 (`third_impl.js` pin
`08ea958f...`) でverdict-level交叉検証する。**verdict不消費・採用判断は
引き続きscrutiny owner (C++第二実装 gate pin `9193f5b6...` 前例・不変)。**

- 対象: `research/experiments/n11-centralreply-closure-batch9-j033-thirdimpl-20261122/`。
  target 4行 (j033 WIN + j001/j016/j027 LOSS)・anchor 2行 (k02a/l1a, Part G/K/O/P
  と同一のpublished第三実装値 9,106,337/4,991,527 と 7,660,602/3,951,175)・
  negative 2行 (ng1/ng2)。入力はpublished batch-9 raw (kit鏡像はrepo正本と
  byte一致を機械確認の上使用) から `make_inputs_batch9.py` がfail-closed導出
  (手転写ゼロ・raw 2-pass一致assert・key/legalをpublished batch-keys.json
  およびstatus.logと機械照合)。
- 前提ゲート (いずれも必須・fail-closed): script pin 3種 (`08ea958f...` /
  `c8c52528...` / `84585617...`)、rule-engine gate (verify_tbl: quads 95,670 ==
  replica / triples 195,044 mismatches 0)、anchor 2行の本ホスト再現がpublished
  値と完全一致、negative 2種の文言一致GATE_FAIL。手法: 1行1プロセス、cap 300M
  expansions、wallcap 240s、1行2回 (a/b) determinism、audit.py 2回実行byte一致。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・verdict不消費。j033のWINは
  引き続きscrutiny owner待ち。標準11x11空盤・19 central-reply roots・class
  1518/2634は本検証のどの時点でもUNKNOWNのまま。nodes/expansionsを勝敗として
  読まない。
- 並走との不接触: batch-9由来キーのみを対象とし、進行中のbatch 8 (Part N,
  class 2634) のscopeと無関係。同一スコープの宣言がmainに存在する場合は着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part U (prober, amendment 2026-11-22): batch-8 takeover - 中断した宣告セッションを kit mirror からresume (事前登録・verdict不消費)

batch 8 (Part N, class 2634, rank 7) は2026-11-22T06:10:23Zにscaffold
(README + scripts 2点 + 51 inputs + batch-keys.json + val-gate 4入力と
宣告ホスト由来4出力) が出版された後、mainへの新規出版が2時間以上途絶え、
kit mirror (`_19root-refresh-kit/batch2634/`) も06:54:32Z (status.log 25行
= i001-i025、i026.p1 は完全・i026.p2 は実行中断由来のheader-only 211B)
で静止している。batch 1-7が走行中もchunk pushを続けた運用と整合しない
ため、宣告実行セッションは i026 の第2 pass 直前に消失したと判定し、
本セッションがbatch 8を引き継ぐ (takeover)。後発2セッション (07:26Z
verifier / 07:33Z batch-9宣告) はいずれもbatch 8をin-flightとして不接触
だった。

takeover開始前に機械検証済みの証拠 (本セッション・read-only):
1. kit `scripts/jsreplay.js` はpin `845856175d...` とbyte一致、published
   batch-8 `scripts/jsreplay.js` とも0 diff。
2. kit input `i001..i051.input.csv` をi→hに改名した51本はpublished
   `input/h001..h051.input.csv` と51/51 byte一致。kit版batch-keys.jsonの
   keys は (s5_index, lo, hi, legal, membership_class_count) でpublished版と
   51/51 ordered一致 (key_id命名 i/h・probe_order 332-382 vs 281-331・
   rank 8 vs 7・mask転記 [...]182144 vs [...]182000 はメタデータ差異。
   canonical選択メタデータはpublished batch-keys.json (後者) であり、
   51/51のworklist (sha256 `ca3ee3bc...`) 行一致はbatch-9セッションが
   機械検証済み)。
3. kit raws i001-i025: 25/25で2-pass node-exact (budget 15M)・key/legal
   全行照合 (i002は15M budget枯渇 result 0 = honest UNKNOWN、status.log上
   PASS = 2-pass node-exact)。
4. 残り h027-h051 を含む51キーはcanonical merged cache (5,975行
   `a998f4c0...`) に不在 (0 hits、本セッションで再照合)。
5. val-gate 4/4 node-exact を本 (takeover) ホストで再現 (at2m result
   0/2,000,000 ×2、15m result 2/3,651,923 と result 2/5,040,200)。
6. 交差host確認: h001 (h002は枯渇行なので触れない) を本ホストで2 fresh
   cold pass再実行 → LOSS 2 / 4,231,707 nodes が両passとも宣告ホスト生値
   とnode-exact一致。
7. rescue: 宣告ホストの i026.p1 (完全・LOSS 2 / 4,284,312 nodes) はkitが
   保持、repo出版時に `output/rescue-declaring-host/` に保存する
   (i026.p2の枯損分もそのまま保存し、補完はしない)。

本amendment (takeover) の事前登録:
- h026 は本ホストで2 fresh cold passを最初から実行する (protocolは
  i026のstatus行が存在しないため、status.log上は本ホスト行のみを記載)。
  h027-h051 の25キーもPart Nと同一の順序・手順で実行。
- 手法・停止規則・消費規則はPart B-Nと全部同一 (pinned replica
  `jsreplay.js` `84585617...`, 2-pass fresh cold, budget 15M,
  mismatch→HARD-STOP rc=42, result 1→WIN-HALT rc=45, 枯渇=UNKNOWN)。
  h002のUNKNOWN行は宣告ホスト記録のまま引き継ぎ、15M同条件の再探索は
  行わない (budget昇格は将来の新規宣言による)。
- 出版: 宣告ホスト実行分 (h001-h025 = kit i001-i025の改名・内容無改変)
  と本ホスト実行分 (h026-) をすべて `output/raw/` に出版。
  output/status.log はkitの25行 (元タイムスタンプ保持) + 本ホスト行の
  追記とし、実行hostの帰属はREADMEに明記する。
- 主張の範囲: coverage・closure・rootを一切主張しない。h002がUNKNOWNの
  ため51キー完了でもbatch 8単体ではclass 2634の閉鎖資格は生じない
  (h002のbudget昇格は別宣言)。WINを得た場合はそのキーで停止し
  if-adopted解析に回す。2-pass LOSS行のみをfail-closed increment cache
  候補として出版してよいが、merge + refresh再監査は本amendmentの
  scope外である (merge + refresh再監査は将来の別宣言に回す)。
- 並走との不接触: batch-9 (Part Q/R/T) のファイルには一切触れない。
  進行中の他レーンとpath衝突しない。実行時にtakeover宣言・batch-8行
  出版がmainに存在する場合は着手しない。
- **class 2634・19 central-reply roots・標準11×11空盤はUNKNOWNのまま。
  nodes数・pass数を勝敗として読まない。**
- 本amendment observed HEAD-before-push: `9f06b2b2b5a770aab414f6c80eb6fe1201d1c1c6`
  (commit messageにも記録)。

## Part T 出版status update (2026-11-22, verifier)

Part T (batch-9 j033 第三実装交叉検証) は実行・出版済み。宣言通り
verdict不消費・verdict-level文献作成のみ (採用判断は引き続きscrutiny
owner、C++第二実装 gate pin `9193f5b6...` 前例・不変)。

- 実行結果: target 4行すべてclean・a/b 2回同一 (result/expansion/ttHits/
  reason)。**j033 WIN一致** (第三実装 5,392,392 expansions vs replica
  df-pn 4,718,280 nodes)、j001/j016/j027 LOSS一致 (9,103,477 / 10,556,205 /
  1,401,488 expansions)。anchors k02a (WIN 9,106,337/4,991,527) と l1a
  (LOSS 7,660,602/3,951,175) はpublished第三実装値とnode-exact一致。
  negative ng1/ng2は文言一致GATE_FAIL。rules gate (quads 95,670・triples
  195,044 mismatches 0) PASS。audit.py (fail-closed, 2回byte一致) は
  **71/71 gates PASS・divergence 0・wall-inconclusive 0**。
- 入力はpublished batch-9正本 (commit `a321bfb2` のraws 8件・batch-keys.json
  `8f2035d1...`・status.log) から `make_inputs_batch9.py` がfail-closed導出
  (raw 2-pass node-exact assert・batch-keys・status.logのPASS行照合込み、
  手転写ゼロ)。repo取得物とkit鏡像は10/10 byte一致で確認済み。
- 出版: `n11-centralreply-closure-batch9-j033-thirdimpl-20261122`
  commits `1ebf75e1` (scaffold 16: README + pinned scripts 4種はpublished
  Part P実験とbyte一致 + audit.py/make_inputs_batch9.py batch-9適用版 +
  machine-derived inputs) → `c98ad197` (targets 8) → `eae66b36` (anchors 4 +
  negative 2 + rules-gate + status.log + audit-summary.json + MANIFEST)。
  fetch-back: commit固定raw URL + sha256sumで**34/34 files byte一致**。
- 観測: 本status pushのretry中に、main上のnoteへ並走セッションによる
  Part U (batch-8 takeover宣言) の追記を確認した。batch-9由来キーのみを
  扱う本実験のscopeとは不衝突。batch-8実験 (Part N/U) のファイルには
  一切接触していない。
- 状況はすべて不変: verdict不消費。j033のWIN (b018/d002/e002/f017/g018と
  同様) はscrutiny owner待ち。batch-9残りj034-j051 (18キー) 未着手。
  標準11x11空盤・19 central-reply roots・class 1518/2634はすべてUNKNOWNの
  まま。nodes/expansionsを勝敗として読まない。
- 本status update observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。

## Part V (verifier, amendment 2026-11-22): batch-8 (class 2634) h045 if-adopted 分解 - WIN-only / LOSS-43-only / full-44 の3シナリオ (verdict不消費)

Part U が事前登録した「WINを得た場合はそのキーで停止し if-adopted解析に
回す」の履行、および Part U の「merge + refresh再監査は将来の別宣言」の
別宣言として、Part H-bis / Part J (batch-6 g018) / Part R (batch-9 j033)
と同一手法のmachine-separated what-if分解を本セッションで宣言・実行・
出版した。対象はbatch-8 (class 2634) のWIN-HALT h045
(s5_index 103558, key `[4035225266258182144, 64]`, legal 85, probe_order
325, result 1, nodes 6,366,900, 2-pass node-exact; Part U takeover分)。
base = Part M canonical re-audit (merged cache 5,975行 `a998f4c0...`)。

- base control (cross-host再現): pinned Part M script (sha256
  `0bc10a05...`) を本takeoverホストで2回再実行し、4出力は両run間で
  byte一致、さらに3出力 (refresh-summary / closure-classes / per-root-
  coverage) はpublished Part M正本とbyte一致。probe-worklist (非出版,
  3.77MB) はsha256 `ca3ee3bc...` を記録。実験
  `n11-class2634-base-control-20261122` (commit `242c1de7`, 7 files,
  fetch-back 7/7 byte一致)。
- increments (fail-closed, `make_increments_batch8.py`): raw 2-pass
  node-exact全行照合、h002 (15M枯損 UNKNOWN, s5 11390) は全incrementから
  除外、WIN行はh045のみ。probed-44rows (sha `356b62a7...`) /
  winh045-only (`7a5e0549...`) / loss43-only (`73f01e74...`)。
  published mergerで衝突0 merge: 5,976行 WIN159/LOSS5,817
  (`1b84db11...`) / 6,018行 WIN158/LOSS5,860 (`0020b89d...`) / 6,019行
  (`9235e547...`)。3行差分refresh scriptをシナリオごとに2回実行し
  6/6 run byte一致。
- 実験 `n11-central-reply-class2634-win-h045-ifadopted-20261122`
  (commit `edd58822`, 32 files, fetch-back 32/32 byte一致;
  probe-worklist.csv 3本は非出版慣行)。compare script
  (`compare_deltas_batch8.py`) はgraph + update8 receipt + scenario
  cacheからrefreshのclass-status意味論 (free候補へのBoard fail-closed
  検証込み) を忠実に再実行し、BASE + 3シナリオの全class_status_countが
  published summaryと一致することを、delta報告の前にfail-closedで門が
  開く形で保証している。
- 機械検証済みの分解結果 (delta: PW045 / PLOSS43 / PFULL44 vs base):
  excluded_now 23 -> 25/23/25. **WIN-only flipは exactly 2 class =
  {2634, 5632}** (graph上s5 103558をcost childに持つ全class、
  membership_class_count 2 と3経路で一致: 再計算flip集合、PFULL44-
  PLOSS43差集合、graph走査)。2634自身のself-exclusion (g018の5473・
  j033の1518と同型)、peer 5632 (base unknown 102 -> このWIN 1つで
  excluded。未解決子が残っていても、published refresh意味論ではWIN
  cost childがあればexcluded_now)。
- update8 (frozen joint plan refresh): batch-9 j033 (win-hit 0) と違い
  **h045のWINはfrozen planにhitする - exactly 1 group** (root-49 group
  `{first 49, reply 60, third 71, fourth 57}`, class 2634がserve、
  unknown_s5_children 51)。remaining 31,836 -> 31,786 (-50; 103558自身の
  resolution +1 とwin-hit group権利落ちの49の合成)、resolved 23 -> 24。
  LOSS43は純加算 (+43 resolved / -43 remaining、43指数は全てbaseline
  requirement内)。FULL44 -51/+44 は単純加算にならない (group-level
  意味論として期待通り)。
- joint greedy: **LOSS43で 35,857 -> 34,906 (-951)** - 測定史上最大の
  greedy削減 (batch-9 loss32の-622、batch-5の+1,372)。最大のper-root
  moverはroot 49 (2,891 -> 2,803, -88)。WIN-onlyのgreedy効果は-1で
  FULL44に完全に包含 (greedy sub-additive by 1、Part Rと同型)。
  worklist deltaは完全加算: -1 (WIN) + -45 (LOSS) = -46 (FULL)。
- class 2634の残: PLOSS43で unknown 51 -> 8 (rank 7 -> 1)、FULL44で
  unknown 7 (rank 1)。残キー = h002 (同条件再探索禁止) + h046-h051
  (s5 103559-103564, 未着手)。PW045のworklistは2634の他50キーを
  excluded classのまま残す (worklistはexcluded classを刈らない;
  free coverageになり得ない行のscheduling bookkeepingのみ)。
  free_now 34 (Board検証34/34) ・全rootのfree coverage・達成済みclosure
  は全シナリオで不変 (machine gate)。
- 不変事項: **verdict不消費**。h045のWINは7番目のunconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045) としてscrutiny owner
  (C++第二実装 gate pin `9193f5b6...`) 待ち。**標準11x11空盤・19
  central-reply roots・class 2634/1518はすべてUNKNOWNのまま。** nodes数
  を勝敗として読まない。第三実装 (Part K/O/P/T流) によるh045 spot
  verificationは本amendmentでは実行しておらずopen。
- 本amendment observed HEAD (実験出版commit): `edd5882267c02768fcab3e1c50ca690bfb81af2c`。
  note本体push直前にmainの最新を再取得して確認する。

## Part W (verifier, amendment 2026-11-22): batch-8 h045 第三実装 spot verification - Part V の open 宣言の履行 (verdict不消費)

Part V が出版時にopen宣言した「batch-8行 (h045 WIN + 層化LOSS rows)
の第三実装 (Part K/O/P/T流) spot verification」を、Part V出版の直後に
同一セッションで実行・出版した (個別の事前宣言なし。Part Vのsession
logにopen宣言が記録済みであり、出版時点でmain上に同scopeの対抗宣言が
存在しないことをlist_commits で確認した上で着手)。実験
`research/experiments/n11-centralreply-closure-batch8-h045-thirdimpl-20261122/`
(3 commits: scaffold `b31abeeb` + targets `c5ebc2fc` + verification
tail `a1ba4ccf`, 34 files, fetch-back 34/34 byte一致)。scripts 6
(third_impl.js pin `08ea958f...` / verify_tbl.js `c8c52528...` /
jsreplay.js `84585617...` / run_thirdimpl.sh `a0b77d83...` /
make_inputs_batch8.py / audit.py, schema `batch8-h045-thirdimpl-audit-v1`)。
inputs 9: targets 4 (h045 WIN行 + h018/h025/h026層化LOSS行) +
anchors 2 (k02a/l1a, published Part T実測値とのcross-run) +
negatives 2 (ng1/ng2, GATE_FAIL文言照合用) + rows.json。sourcesは
published commit `1f127fb8` からcommit-pinned raw CDNで取得
(batch-keys sha `5c42a950...`)。

- 機械結果 (14 solver runs, 最大4並列, a/b 2-pass): **h045 WIN 1 =
  7,348,868 expansions / 4,145,900 ttHits** (a/b同一; replica df-pn
  WIN 6,366,900 nodes とverdict一致)。h018 LOSS 2 (1,756,741 /
  1,066,681)・h025 LOSS 2 (13,169,795 / 7,161,043)・h026 LOSS 2
  (4,938,236 / 2,884,833)。anchors k02a WIN 9,106,337 / 4,991,527・
  l1a LOSS 7,660,602 / 3,951,175 はpublished Part T実測値と完全一致。
  negatives ng1/ng2はGATE_FAIL文言一致。runlimit/wall-inconclusive 0。
- rules gate: quads 95,670 == replica・triples 195,044・mismatch 0。
- audit: **71/71 gates PASS**、2回実行でbyte一致
  (audit-summary.json sha `3accd540...`)。MANIFEST 33 entries
  (sha `f32ef88c...`)。
- 意味: 7つのunconsumed closure WIN (b018 / d002 / e002 / f017 /
  g018 / j033 / h045) の**全てが第三実装によるspot検証済み**になった
  (前6個はwin-thirdimpl-reverify + j033 Part T、h045が本Part W)。
  ただし**verdict不消費は不変**。scrutiny owner (C++第二実装 gate
  pin `9193f5b6...`) 待ち。**標準11x11空盤・19 central-reply roots・
  class 2634/1518はすべてUNKNOWNのまま。** nodes/expansions数を
  勝敗として読まない。
- 本Part Wのobserved HEAD (出版3 commits直後): `a1ba4ccff58c6e00640cbecaef4da0e5d956f327`。
  note本体push直前にmainの最新を再取得して確認する。

## Part X (prober, amendment 2026-11-22): batch 10 (class 8784, rank 9) 宣言 - 反駁証拠のない次位clean候補をbatch-7 protocolで開始

batch 8 (Part N/U, class 2634) はWIN-HALT (h045; if-adoptedはPart V・第三実装
spot検証はPart W)、batch 9 (Part Q, class 1518) はWIN-HALT (j033; if-adoptedは
Part R・第三実装はPart T)。batch実績は9バッチ中7 WIN-HALT + 2 clean
(23963/10324)。Part M closure rankingでrank 1-8はすべて反駁証拠保持
(16757: b018, 20421: d002, 30345: b018のs5 528497, 16371: e002, 12264: f017,
5473: g018, 2634: h045, 1518: j033) のため、反駁証拠のない次候補として
reaudit closure-classes rank 9 のクラス8784に着手する (安価側WIN密集の
実測傾向はPart Vまでで11ショット Warning なし・scheduling quantityとして
選定は不変)。

- 対象: `research/experiments/n11-centralreply-closure-class8784-batch10-20261122/`。
  graph class index 8784, mask `[6052837899186012160, 0]` の未確定canonical
  S5子52件 (m001-m052。'i'はbatch-8宣告ホスト由来命名として使用回避、
  'k'/'l'はsixth-cost k行・第三実装anchor k02a/l1aとの読み衝突回避のため
  skip)。reaudit正本probe-worklistのprobe_order 383-434 (serving_class=8784・
  Board再計算合法手数固定・first=16/third=58を含む5グループ担当)。
- 宣言前fail-safe機械確認 (本ホスト・fail-closed): (1) Part M refresh機材
  (published script sha256 `0bc10a05...`) をpublished pinned inputs
  (dependency-graph `54f9c364...`・merged cache `a998f4c0...`・update8 plan
  `b658290a...`・board `954d3a10...`・policy `78655e94...`・quarantine
  `81d23160...`) から再実行し、closure-classes.csv・refresh-summary.json・
  per-root-coverage.csvの3成果物がpublished Part M bytesとbyte一致、
  probe-worklist.csv (65,155行) はsha256
  `ca3ee3bc7772ff38462cb60fc41ab4570cb236a880213322de230410fa550e80` で
  Part N/Q記載値と一致 (cross-host byte-exact再現)。(2) 全52キーは正本
  merged cache (5,975行・sha256 `a998f4c0...`) に不在 (0 hits)。(3)
  quarantine registry (sha256 `81d23160...`・active 2件) とのkey対照
  0 hits (両方向)。
- val-gate: published two-target-design 4行を本ホストで再現、4/4 node-exact
  (at2m result 0/2,000,000 ×2、15m result 2/3,651,923 と result 2/5,040,200)。
- 手法・停止規則・消費規則: Part B-Qと全部同一 (pinned replica
  `jsreplay.js` sha256 `845856175d...`・batches 1-9とbyte-identical、
  2-pass fresh cold、budget 15M、mismatch→HARD-STOP rc=42、WIN→HALT rc=45、
  枯渇=UNKNOWN、消費はfail-closed merger経由のみ、本batch単体では閉鎖・
  被覆・secured主張なし)。実行並列は本ホスト最大4 worker (probe_order順の
  4キーwave実行・WIN報告wave完了後は新規キー着手なし・同一wave内の
  in-flight完了行は誠実開示、batch-5 f018先例)。
- 主張の範囲: 本batchはcoverage・closure・rootを一切主張しない。WIN-HALT
  (rc=45) が発火した場合はそのkeyで停止しif-adopted解析に回す (予登録
  stop rule)。全52本LOSSでも消費はfail-closed increment merge + refresh
  再監査まで行わない。**class 8784・19 central-reply roots・標準11×11空盤は
  UNKNOWNのまま。nodes数・pass数を勝敗として読まない。**
- 並走との不接触: batch-8 (Part N/U/V/W)・batch-9 (Part Q/R/T) のpublished
  ファイルには一切接触しない。同一スコープの宣言がmainに存在する場合は
  着手しない (宣言直前に最新mainを再取得・class8784実験dirの不在・Part X
  採番の未使用を確認済み)。
- 本amendment observed HEAD-before-push: `b7b798b96c224eacd03b587eaf9356409ec86b5c`
  (Part W出版後・n7 K1058レーンの修正コミット直後のmain。commit messageにも記録)。
- 追加fail-safe (出版直前): class 8784のmaskはPart M refresh再生成の
  closure-classes.csv rank 9行 (class_lo 6052837899186012160 / hi 0 /
  unknown_now 52 / first 16 / third 58 / groups 5) と正本一致を確認。
  batch-keys.jsonの52キー (s5_index/lo/hi/legal/membership_class_count/
  probe_order 383-434) はworklist正本行と52/52完全一致。keys.jsonの
  class_mask表示 `...2000` はECMAScript float64パースの表示丸めであり、
  生テキストは正本値 `...2160` (改修不要)。scaffold構成: input/
  batch-keys.json (sha256
  `a1401ee2769f3943f993527dd4934ce82e99c6d55ee27a13cf74b1b417148ebf`)
  + m001-m052.input.csv 52本 (target行: id,stones,lo,hi,legal固定形式) +
  scripts/jsreplay.js (pin) + scripts/runbatch.sh (published batch-9と
  byte-identical) + output/val-gate/ (published 4入力 + 本ホスト4出力) +
  README。output/raw/・output/status.logは実行後にchunk出版する。

## Part X 出版status update (2026-11-22, prober): batch 10 完走 - 52/52 全LOSS (3度目のclean batch)

- 実行結果 (machine-verified): m001-m052全52キー、budget 15M・2-pass fresh
  cold、全キーPASS (budget,result,nodes の2-pass完全一致)、**全52行
  result 2 (LOSS)**。WIN-HALT (rc=45) なし・mismatch (rc=42) なし・
  枯渇 (result 0) なし。nodes幅 1,552,890 (m019, s5 263430) -
  8,133,535 (m010, s5 243538)、52キー合計 177,295,361 (p1参照)。
  batch実績は10バッチ中7 WIN-HALT + 3 clean (23963/10324/8784) となった。
- 観測 (誠実記録・解釈なし): m014/m015 (3,801,379)・m027/m028 (3,162,294)・
  m030/m031 (2,277,181) の3組がprobe_order隣接の**別キー**で同一ノード数。
  いずれも (s5,lo,hi,legal) は別キーで、各ペアとも2-pass node-exact gateを
  個別に通過している。
- 実行形態: 2-coreホスト、宣言通り最大4 worker、probe_order順4キーwave
  (`scripts/runner-all.sh`、resume-safe・rc>=42で新規wave着手禁止・
  in-flight完了は誠実開示)。m001-m012はforeground wave、m013-m052は
  detached runner (wall 09:33:01Z-10:06:29Z、中断含む)。
- 環境事故の誠実開示: 早期のforeground 2-wave試行中に240s bash timeoutで
  実行環境が破棄され、当時のローカル出力 (最大12キー分、未出版) が消失。
  published宣言commit `ab8641f...` からscaffoldをbyte-exact再取得して
  全キー最初からやり直した。**m001はリセット前に一度完了していた
  4,038,249 nodes (result 2) を、リセット後のfresh cold再実行で
  node-exact同一値として再現** (cross-restart node-exact reproduction)。
  出版されたrawsはすべてリセット後の実行分。
- 出版: raws 104ファイルを3 chunk commitsに分割出版 (m001-m018=36・
  m019-m036=36・m037-m052=32、fetch-back 104/104 byte-exact in
  commit-pinned raw URL検証)。status.log (65行)・runner-all.sh・
  README Result節を本status commitで出版。**class 8784・19 roots・
  標準11×11空盤はいかなる時点でもUNKNOWNのまま。nodes数を勝敗として読まない。**
- 消費は未実行 (予登録通り)。52 LOSS行はfail-closed increment候補として
  Part Y宣言の下でのみ消費される。

## Part Y (verifier, declaration 2026-11-22): batch 10 (class 8784) increment merge + refresh再監査 - Part C/Mと同一の閉鎖機構

batch 10 (Part X) は52/52全LOSSで完走した。Part C (23963→33番目free)・
Part M (10324→34番目free) と同一の閉鎖機構で消費・再監査を宣言する。

- 対象: `research/experiments/n11-central-reply-8784-closure-reaudit-20261122/`。
- 対象: increment 52行はpublished batch-10 rawからfail-closed生成
  (2-pass (result,nodes,legal) 一致・key (lo:hi) とs5/legalの
  batch-keys.json照合assert込み、published rawの再取得とsha照合の上)。
  mergeはpublished `s5_union_merge.py` (selftest PASS) で正本5,975行
  (`a998f4c0...`) + 52行 → 出力はpublish時にsha記載、衝突0・重複0が
  fail-closed gate。
- refreshはpublished script `refresh_19root_frontier.py` (sha256
  `0bc10a05...`) のbyte-copy (cache pin行のみ変更・diff検証)、他の
  pinned inputs 5種 (dependency-graph `54f9c364...`・update8 plan
  `b658290a...`・board `954d3a10...`・policy `78655e94...`・quarantine
  `81d23160...`) はpublished正本sha一致、**2-run全出力byte-identical**
  gate。baseとしてPart M published 3成果物 (closure-classes.csv・
  refresh-summary.json・per-root-coverage.csv) との追加差分比較を行う。
- 事前登録の判定規則: refresh再実行でclass 8784がunknown 52→0かつ
  excluded流入なし (WIN 0行消費のため) の場合、Board検証
  free候補として扱う。free_now 34→35は board_verification 35/35・
  rejected 0 の場合のみ主張する。**WIN行は1行も存在しないため
  excluded_nowは不変であることが機械的に要求される** (違反=HARD-STOP・
  即中止・訂正はscrutiny owner判断)。root第三手被覆の増分・update8
  remaining/resolved・joint greedy・worklist総量はrefresh-summaryから
  測定として記録する。
- 主張と消費規則: 消費するのはbatch 10の52 LOSS行のみ。7 WIN
  (b018/d002/e002/f017/g018/j033/h045) は引き続きscrutiny owner待ちで
  不消費。class 8784のfree状態 (成立した場合) はmerge cacheからの
  derived class statusであり、**標準11×11空盤・19 central-reply rootsは
  引き続きUNKNOWN**。nodesを勝敗として読まない。
- transport: probe-worklist (~3.7MB) は再出版しない (pinned inputs +
  scriptからbyte-identical再生成可能、総量はrefresh-summary.jsonに記録)。
- 並走との不接触: batch-10由来キーのみ。同一スコープの宣言がmainに
  存在する場合は着手しない。
- 本宣言のobserved HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part Y 出版status update (2026-11-22, verifier): class 8784 消費完了 - 35番目のBoard検証free class確定

Part Y宣言 (本note Part Y節) に基づき消費・再監査を実行・出版した。

- increment (fail-closed, `make_increment_batch10.py`): published batch-10
  raws (chunk commits `7b8790ab`/`736a4f11`/`354524de` から再取得・
  実行ホスト正本と104/104 byte一致を再確認) + published
  batch-keys.json (`a1401ee2...`) から52行を機械生成。全ゲート通過
  (ルールゲート行`forbidden quadruples: 95670`両pass存在・stones=5/
  is_or=0/budget=15M・2-pass (budget,result,nodes) 一致・全行result 2・
  legal/key照合)。increment sha256 `f500610a55802e7f67eecb06d9d31e3462
  761cbb61a746bbd46a4e63ad2cc652`。
- merge (published merger, selftest PASS): 正本5,975行 (`a998f4c0...`) +
  52行 → **6,027行 (WIN 158 / LOSS 5,869)・衝突0・重複0・nodes不一致0**。
  新merged cache sha256 `95e868d6762925b9a27ad963a825a9ad4fd5131a864eb82
  fac0db77d7acdb326` (247,267 bytes)。canonical input pathからのmerge再実行
  で出力sha同一 (決定性確認)。
- refresh (published scriptのbyte-copy、差分3行 = docstringのcache系列行・
  CACHE path行・sha pin行、scenario script sha256 `88671526...`): **2回実行
  の全4出力がbyte-identical** (closure-classes `61943b85...`・
  per-root-coverage `33f01a0c...`・refresh-summary `25987add...`・
  probe-worklist 65,154行 `1807e4d2...`)。
- 事前登録判定ゲート (すべてPASS・machine-verified):
  **(1) class 8784 = Board検証済み35番目のfree class** (free_now 34→**35**、
  board_verification 35/35・rejected 0、8784はunknown閉鎖rankingから消失)。
  **(2) excluded_now 23不変** (WIN 0行消費の機械的要求)。unknown class総数
  34,502→34,501 (unknown→freeは8784の1クラスのみ)。**(3) 実被覆増分**:
  root 38のfree第三手 **10→13 (+3)**・root 16 **12→14 (+2)**
  (per-root-coverage.csv)。**(4) update8**: remaining_now 31,836→**31,784
  (−52)** (resolved 23→**75**、52 keys全てbaseline requirement内・
  groups_free_now 122→**127** (+5)、per-root remaining: root 16 −104・
  root 38 −156)。**(5) scheduling量**: joint greedy 35,857→**35,242 (−615、
  測定史上3番目のgreedy削減: h045 LOSS43の−951・j-loss32の−622に次ぐ)**、
  worklist 65,155→65,154、nonfree best-option groups 2,132→2,127。
- 次のfirst clean candidate: renewed closure rankingでrank 1-8は不変
  (全て反駁証拠保持: 16757: b018, 20421: d002, 30345: s5 528497,
  16371: e002, 12264: f017, 5473: g018, 2634: h045, 1518: j033)、
  **rank 9 class 8106** `[1152926194711134208, 0]` (unknown 52,
  first=14/third=58, 4 groups)。
- 出版: 実験 `n11-central-reply-8784-closure-reaudit-20261122`
  commit `79cfa66a` (9 files: README + scripts 3 + increment + merge-audit
  + closure-classes + per-root-coverage + refresh-summary) + commit
  `5a6e0528` (新merged cache 1 file)。fetch-back: 10/10 byte一致
  (commit固定raw URL)。probe-worklist (3.77MB, regenerable) は非再出版
  (shaはREADME記載)。
- 不変事項: **verdict不消費**。7つのunconsumed closure WIN (b018/d002/
  e002/f017/g018/j033/h045) はscrutiny owner待ち (C++第二実装 gate pin
  `9193f5b6...`前例)。消費したのはbatch-10の52 LOSS行のみ。
  **標準11×11空盤・19 central-reply rootsは引き続きUNKNOWN。**
  class 8784のfreeはmerged cache由来のderived class statusであり、
  勝敗主張ではない。nodesを勝敗として読まない。
- 本status update observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録 (Part Y実験出版 `5a6e0528` 直後のmain)。

## Part Z (prober, amendment 2026-11-22): batch 11 (class 8785, renewed rank 8) 宣言 - Part Y statusのrank記載修正とともに、反駁証拠のない次位clean候補をbatch-7 protocolで開始

batch実績は10バッチ中7 WIN-HALT + 3 clean (23963/10324/8784 = 33・34・35番目free)。
Part Yにより新正本merged cache 6,027行 (sha256 `95e868d6...`) が確定した。
次候補の選定に先立ち、**Part Y status updateのrank記載に対するerratumを本宣言に
記録する**: 同statusの「次のfirst clean candidate: renewed closure rankingで
rank 1-8は不変 (全て反駁証拠保持: 16757: b018, 20421: d002, 30345: s5 528497,
16371: e002, 12264: f017, 5473: g018, 2634: h045, 1518: j033)、rank 9 class 8106」
というrank読みは、published Part Y closure-classes.csv (sha256 `61943b85...`) の
renewed rankingと一致しない。実際のrenewed rankingは rank 1-7が反駁証拠保持
(16757: b018, 20421: d002, 30345: b018 cost child保持, 16371: e002,
12264: f017, 5473: g018, 2634: h045)、**rank 8 = class 8785** (unknown 51。
Part M baseではrank 15 / unknown 52だったが、batch-10の52-LOSS増分の消費で
unknown子が1つ解決され上位に移動したもの)、rank 9 = 1518 (j033)、
rank 10 = 8106 である。「rank 1-8不変」はrank 1-7についてのみ成立し、
rank 8は1518から8785に変化している。8106の「rank 9」はこのslide誤読由来である。

- 本ホストでの機械検証 (宣言前・fail-closed): (a) published renewed
  closure-classes.csv rank 8行 = class 8785 `[1224979373522681856, 1]`・
  unknown 51・first=16/third=104・groups 1 (Part Y正本出力とbyte一致)。
  (b) 7つのunconsumed WINキー (b018 `[1153204079095189504, 65536]` /
  d002 `[3461016313634230272, 131072]` / e002 `[1153765929805414400, 16]` /
  f017 `[1188950301625810945, 70368744177666]` / g018 `[1734519175235239936, 0]` /
  j033 `[1153484455030030336, 0]` / h045 `[4035225266258182144, 64]`) の
  いずれもclass 8785の51未確定子に不在 (cost child / refuted-quarter対照
  0 hits。b018のキーは16757∩30345 worklist行共通部分として独立再導出し
  確認)。class 8106の52子にも0 hits (referenced: 8785完了後の次候補は
  renewed rank 10 class 8106)。participatingするのはcost child関係のみで、
  クラス選定はscheduling quantityである。
- 予登録選定規則 (「in flightでもWIN-HALTでもなく反駁証拠 (refuted-quarter)
  を持たない最初のclean candidate」) に従い、renewed rankingのfirst clean
  candidateは **rank 8 class 8785** (unknown 51) であり、batch 11はこれに
  着手する。Part Yのprose誤記はクラスstatus・verdict・被覆主張には一切
  影響しない (クラスstatusはrefresh機構からのderiveであり、機構・出力は
  publishedのまま正しい。誤っていたのは手書き要約のrank読みのみ)。
- 対象: `research/experiments/n11-centralreply-closure-class8785-batch11-20261122/`。
  graph class index 8785, mask `[1224979373522681856, 1]` の未確定canonical
  S5子51件 (z001-z051。接頭辞zはbatch 1-10の命名系列衝突回避、bookkeeping
  のみ)。Part Y re-audit正本probe-worklist (65,154行、sha256
  `1807e4d21f6fb757ea21850c6bda4d822cb76ac59abfa9bcd1cc7b53bd7055ef`、
  Part Y status記載値と一致) の `serving_class=8785` 行 (probe_order
  332-382・Board再計算合法手数固定・first=16/third=104の1グループ担当)。
  本宣言セッションはPart Y refresh機材のfull再実行は行っていない
  (Part Y出版時に2-run byte-identical検証済み)。51行はbatch-keys.jsonに
  全行publishedしており、正本cache・update8機構に対して独立照合可能。
- 宣言前fail-safe機械確認 (本ホスト・fail-closed): (1) 正本merged cache
  (6,027行・sha256 `95e868d6...`) に51/51 keys不在 (0 hits)。(2) quarantine
  registry (sha256 `81d23160...`・active 2件) とのkey対照 0 hits (両方向)。
  (3) 51キー重複なし。(4) renewed closure-classes rank 8行との正本一致。
  (5) 7 WINキーのcost-child対照 0 hits (上述)。
- val-gate: published two-target-design 4行を本ホストで再現、4/4 node-exact
  (at2m result 0/2,000,000 ×2、15m result 2/3,651,923 と result 2/5,040,200。
  本ホストのfresh出力4件はscaffoldのoutput/val-gate/に固定)。
- 手法・停止規則・消費規則: Part B-Xと全部同一 (pinned replica
  `jsreplay.js` sha256 `845856175d...`・batches 1-10とbyte-identical、
  2-pass fresh cold、budget 15M、mismatch→HARD-STOP rc=42、WIN→HALT rc=45、
  枯渇=UNKNOWN、消費はfail-closed merger経由のみ、本batch単体では閉鎖・
  被覆・secured主張なし)。実行並列は本ホスト最大4 worker (probe_order順の
  4キーwave実行・WIN報告wave完了後は新規キー着手なし・同一wave内の
  in-flight完了行は誠実開示、batch-5 f018先例)。
- 主張の範囲: 本batchはcoverage・closure・rootを一切主張しない。WIN-HALT
  (rc=45) が発火した場合はそのkeyで停止しif-adopted解析に回す (予登録
  stop rule)。全51本LOSSでも消費はfail-closed increment merge + refresh
  再監査まで行わない (将来のverifier宣言)。**class 8785・19 central-reply
  roots・標準11×11空盤はUNKNOWNのまま。nodes数・pass数を勝敗として読まない。**
- 並走との不接触: batch-8 (Part N/U/V/W)・batch-9 (Part Q/R/T)・batch-10
  (Part X/Y) のpublishedファイルには一切接触しない。同一スコープの宣言が
  mainに存在する場合は着手しない (宣言直前に最新mainを再取得・class8785
  実験dirの不在・Part Z採番の未使用を確認済み)。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part Z publication status update (2026-11-22, prober): batch 11 (class 8785) WIN-HALT at z003 - 宣告セッション消失後のtakeover出版 (verdict不消費)

batch 11 (Part Z, class 8785, renewed rank 8) は宣告セッション (RUNNER-START
2026-11-22T10:32:08Z, host `f80d796a...`, 2 cores) で実行され、第一wave
(z001-z004) 中に**事前登録のWIN-HALT規則 (rc=45) が z003 (s5_index 198530,
key `[1225542323476103168, 1]`, legal 82, probe_order 334): result 1 (WIN),
11,601,265 nodes, 2-pass fresh cold node-exact** で発火した (2026-11-22T
10:36:40Z)。同一waveのin-flightキー3本は完了・誠実開示 (z001 LOSS
3,146,511 / z002 LOSS 2,256,914 / z004 LOSS 6,424,054、いずれも2-pass
node-exact)。4/51 probed、z005-z051は未着手。宣告セッションはWIN-HALT後、
rows・status・result欄を一切出版しないまま消失した (scaffoldは宣言commit
`3cc96099`の30ファイル止まり: README + batch-keys.json + z001-z028 inputs +
val-gate inputs。batch 1-7が走行中もchunk pushを続けた運用と不整合) ので、
batch 8 (Part U) と同一基準で宣告ホスト消失と判定し、本takeoverセッションが
証拠をrescue・検証・出版した。

takeoverホスト (本セッション, host `d3578b9e...`) での出版前機械検証
(fail-closed, すべて機械実行):
1. kit mirrorからrescued 8 raws (z001-z004 p1/p2): quads gate行 (95,670)
   存在・2-pass (budget, result, nodes) 一致・rescued status.logのPASS行
   との一致、すべて確認。
2. 出版済みbatch-keys.json (blob `a5d3193a02dd...`, 51キー) は宣告セッション
   kit copyとbyte一致。51キーはPart Y re-audit正本worklist (65,154行,
   sha256 `1807e4d2...`) のserving_class=8785行 (probe_order 332-382) と
   51/51完全一致・input CSV一致51/51・重複なし。
3. 51キーは正本merged cache (6,027行, sha256 `95e868d6...`) に不在 (0 hits)。
   quarantine registry (2 active entries) とのkey対照0 hits (両方向)。
4. 7つのunconsumed WINキー (b018/d002/e002/f017/g018/j033/h045) はclass
   8785の51子にもclass 8106の52子にも不在 (cost child対照 0 hits。b018の
   キーは16757∩30345 worklist行共通部分として独立再導出一致)。
5. Part Y status updateのrank誤記 (「rank 9 = 8106」) はPart Z宣言の
   erratum通り: published renewed closure-classes (sha256 `61943b85...`) は
   rank 8 = 8785 (unknown 51)・rank 9 = 1518 (j033)・rank 10 = 8106。
6. val-gate 4/4 を本ホストで再現 (at2m result 0/2,000,000 x2、15m result
   2/3,651,923 と result 2/5,040,200)。宣告ホストrescued出力4件とも一致。
7. **交差host再現 (pinned replica `jsreplay.js` `84585617...`, fresh cold)**:
   rescued全4キーを本ホストで2-pass再実行し、すべて宣告ホスト生値と
   node-exact一致: z003 WIN 1 / 11,601,265 (両pass)、z001 LOSS 3,146,511
   (両pass)、z002 LOSS 2,256,914 (両pass)、z004 LOSS 2 / 6,424,054
   (両pass)。再現生値は `output/raw/z00X.pN.takeover.out`・
   `output/val-gate/*.takeover.out` として宣告ホスト分とともに出版、
   `output/status.takeover.log` に本ホストのscheduleを記録。

batch実績は11バッチ中8 WIN-HALT + 3 clean (23963/10324/8784 = 33・34・35番目
free)。z003は**8番目のunconsumed closure WIN** (b018/d002/e002/f017/g018/
j033/h045/z003)。verdict不消費・scrutiny owner (C++第二実装 gate pin
`9193f5b6...`) 待ち。z003の第三実装spot検証 (Part K/O/P/T/W流) は未実施・
将来のverifier宣言。if-adopted分解 (Part V/R流) も未実施・別宣言。
次候補: 8785はrefutation evidence保持 (z003)、1518も保持 (j033) なので、
renewed ranking上の次のfirst clean candidateは**rank 10 class 8106**
(mask `[1152926194711134208, 0]`, unknown 52, 4 groups)。

**class 8785・19 central-reply roots・標準11×11空盤はいかなる時点でも
UNKNOWNのまま。nodes数・pass数を勝敗として読まない。**
## Part AA (verifier, amendment 2026-11-22): batch 11 z003 third-implementation cross-verification (declared before execution)

batch 11 (Part Z, class 8785, renewed rank 8) は事前登録のWIN-HALT規則により
z003 (2-pass node-exact result 1, 11,601,265 nodes, s5_index 198530, key
`[1225542323476103168, 1]`, legal 82, probe_order 334; 宣告ホスト値はtakeover
ホストfresh cold 2-passでcross-host node-exact再現済み・published) で停止した。
Part K/O/P/T/Wの前例に従い、batch-11のWIN行 z003 と、probed LOSS全3行
(z001/z002/z004 — batch-11は4/51 probed (z005-z051未着手) のため、既存
バッチの「層化3行サンプル」ではなく第一wave検査済み全行を対象とする) を
第三実装 (`third_impl.js`, pin sha256 `08ea958f...`) でverdict-level交叉
検証する。**verdict不消費・採用判断は引き続きscrutiny owner (C++第二実装
gate pin `9193f5b6...` 前例・不変)。**

- 対象: `research/experiments/n11-centralreply-closure-batch11-z003-thirdimpl-20261122/`。
  target 4行 (z003 WIN + z001/z002/z004 LOSS)・anchor 2行 (k02a/l1a, Part
  G/K/O/P/T/Wと同一のpublished第三実装値 9,106,337 expansions/4,991,527
  ttHits と 7,660,602/3,951,175)・negative 2行 (ng1/ng2)。入力はpublished
  batch-11 raw (宣告ホスト p1/p2 8件 + takeoverホスト .takeover.out 8件、
  commit `12be47c7`/`40e02623`からcommit-pinned raw CDN取得) から
  `make_inputs_batch11.py` がfail-closed導出する (手転写ゼロ・宣告ホスト
  raw 2-pass一致assert・takeover rawとの2-host一致assert・status.logと
  status.takeover.logの照合・key/legalをpublished batch-keys.json (sha256
  `8ef22069...`, commit `3cc96099` 正本) と機械照合)。sourcesは再出版しない。
- 前提ゲート (いずれも必須・fail-closed): script pin 3種 (`08ea958f...` /
  `c8c52528...` / `84585617...`)、rule-engine gate (verify_tbl.js: quads
  95,670 == replica / triples 195,044 mismatches 0)、anchor 2行の本ホスト
  再現がpublished値と完全一致、negative 2種 (ng1/ng2) の文言一致
  GATE_FAIL。手法: 1行1プロセス、cap 300M expansions、wallcap 240s、
  1行2回 (a/b) determinism gate (result/expansion/ttHits/reason同一必須)。
  wall超過 (runlimit) はhonest wall-inconclusiveとして記録し検証主張と
  しない。cleanなverdict一致のみ文献として記録する。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・verdict不消費。
  z003のWINは8番目のunconsumed closure WIN (b018/d002/e002/f017/g018/
  j033/h045/z003) として引き続きscrutiny owner待ち。
  標準11x11空盤・19 central-reply roots・class 8785は本検証のどの時点でも
  UNKNOWNのまま。z005-z051は未着手のまま。nodes/expansionsを勝敗として
  読まない。
- 並走との不接触: batch-11由来のpublishedキーのみを対象とし、他レーン・
  進行中の実験と無関係。同一スコープの宣言がmainに存在する場合は着手
  しない (宣言直前に最新mainを再取得・同scope対抗宣言なしを確認済み)。
- 本amendment observed HEAD-before-push: `2da303db469683819954820bd832c2f51e096510`
  (batch-11 takeover出版完了 (Part Z status update + session log
  continuation 14) 直後のmain。commit messageにも記録)。

## Part AA 出版status update (2026-11-22, verifier): batch 11 z003 第三実装交叉検証 実行・出版済み - 8つのunconsumed WIN全て第三実装検証済みに

Part AA宣言 (本note Part AA節・commit `1d750f19`) に基づき実行・出版した。
宣言通りverdict不消費・verdict-level文献作成のみ (採用判断は引き続き
scrutiny owner、C++第二実装 gate pin `9193f5b6...` 前例・不変)。

- 実行結果 (machine-verified): target 4行すべてclean・a/b 2回実行で同一
  (result/expansion/ttHits/reason)。**z003 WIN一致** (第三実装 13,781,596
  expansions / 7,500,476 ttHits vs replica df-pn WIN 11,601,265 nodes・
  cross-host node-exact済みの宣告ホスト値とtakeoverホスト値の双方と一致)、
  z001/z002/z004 LOSS一致 (第三実装 3,594,991 / 2,547,371 / 7,426,794
  expansions vs replica 3,146,511 / 2,256,914 / 6,424,054 nodes)。
  anchors k02a (WIN 9,106,337 expansions / 4,991,527 ttHits) と l1a
  (LOSS 7,660,602 / 3,951,175) は本ホスト再現値がpublished第三実装値
  (Part G/K/O/P/T/W) と完全一致。negative ng1/ng2は文言一致GATE_FAIL。
  rules gate (quads 95,670 == replica / triples 195,044・mismatch 0) PASS。
  audit.py (fail-closed, schema `batch11-z003-thirdimpl-audit-v1`, 2回実行
  byte一致) は **71/71 gates PASS・divergence 0・wall-inconclusive 0**。
- 入力はpublished batch-11正本 (宣告ホスト p1/p2 raw 8件 + takeoverホスト
  `.takeover.out` 8件、chunk commits `12be47c7`/`40e02623`からcommit-pinned
  raw CDNで取得・sha256全件照合の上) から `make_inputs_batch11.py` が
  fail-closed導出 (両host分の2-pass (budget,result,nodes) 一致assert・
  RUNNER-STOP/RUNNER-EXIT由来行の存在assert・status.logと
  status.takeover.logの照合・published batch-keys.json (sha256
  `8ef22069...`, commit `3cc96099`正本) とのkey/legal機械照合・手転写ゼロ)。
- 出版: `research/experiments/n11-centralreply-closure-batch11-z003-thirdimpl-20261122/`
  commits `1d750f19` (本note Part AA宣言amendment) → `28b23f14`
  (scaffold 16 files: README + pinned scripts 6 + machine-derived inputs 9) →
  `fea875eb` (targets a/b 8) → `f2a8fa48` (anchors 4 + negative 2 + rules-gate
  + status.log + audit-summary.json + MANIFEST, 10 files)。fetch-back: commit固定raw
  URL + sha256sumで**34/34 files byte一致**を確認済み。sourcesは再出版なし
  (published raws由来・READMEにsha記載)。
- 意味: 8つのunconsumed closure WIN (b018/d002/e002/f017/g018/j033/h045/
  z003) の**全てが第三実装によるverdict-level交叉検証済み**になった
  (前6個はwin-thirdimpl-reverify (Part G) + Part P + Part T (j033) +
  Part W (h045)、z003が本Part AA)。ただし**verdict不消費は不変**。
  z003のWINは引き続きscrutiny owner待ち。z005-z051は未着手のまま。
  **標準11x11空盤・19 central-reply roots・class 8785は本検証のどの時点でも
  UNKNOWNのまま。nodes/expansions数を勝敗として読まない。**
- open items (将来の別宣言で実施): z003 if-adopted分解 (Part V/R流・
  refresh機材はPart Y pinned scenario script `88671526...` / base cache
  `95e868d6...` 系列)・次batch候補 = renewed rank 10 class 8106
  `[1152926194711134208, 0]` (unknown 52)。
- 本status update observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。

## Part AB (verifier, amendment 2026-11-22): batch 11 (class 8785) z003 if-adopted 分解 - WIN-only / LOSS-only / full の3シナリオ (verdict不消費・別宣言の履行)

Part Z status update が open item として挙げた「z003 if-adopted分解 (Part V/R流)」の
実行宣言である (Part AAの第三実装交叉検証は published済みのため、z003の
verdict-level補強は全て揃った状態で本分解に着手する)。手法・規約は
Part H-bis / Part J / Part R / Part V と完全同一 (machine-separated
WIN-only vs LOSS-only vs full what-if)。**verdictは一切消費しない。**

- 対象: `research/experiments/n11-centralreply-class8785-win-z003-ifadopted-20261122/`。
  3シナリオ: PWINZ003 = z003 WIN行のみ (s5 198530, key
  `[1225542323476103168, 1]`, result 1, 11,601,265 nodes) / PLOSS3 =
  z001/z002/z004の3 LOSS行のみ / PFULL4 = probed全4行。batch 11は
  4/51 probed (z005-z051未着手) のため、probed全行 = 第一wave 4行が
  分解対象の全行である。
- 前提確認 (宣言前に本ホストで機械実施・fail-closed): (1) Part Y pinned
  inputs 6種をrepo正本 (commit `0a369d6c`固定raw) から取得しsha256全件一致
  (dependency-graph `54f9c364...`・正本merged cache 6,027行 `95e868d6...`・
  update8 plan `b658290a...`・board `954d3a10...`・policy `78655e94...`・
  quarantine `81d23160...`)。(2) Part Y scenario script (sha256
  `88671526...`) をbase controlとして本ホストで2回再実行、全4出力が
  run間でbyte-identical、かつclosure-classes.csv・per-root-coverage.csv・
  refresh-summary.jsonの3成果物がpublished Part Y正本とbyte一致、
  probe-worklist.csvはsha256 `1807e4d2...` (65,154行、Part Y/Z記載値)
  と一致 (cross-host byte-exact再現)。
- 増分 (fail-closed, `make_increments_batch11.py`): published batch-11 raw
  (宣告ホスト p1/p2 8件・takeoverホスト `.takeover.out` 8件、chunk commits
  `12be47c7`/`40e02623`からcommit-pinned raw CDN取得・sha全件照合の上) から
  機械生成。両host分の2-pass (budget,result,nodes) 一致assert・published
  batch-keys.json (sha256 `8ef22069...`) とのkey/legal照合・z003は result 1・
  他3行は result 2 を要求 (手転写ゼロ)。増分は
  PFULL4 (4行) / PWINZ003 (1行) / PLOSS3 (3行) の3本。
- merge: published `s5_union_merge.py` (selftest PASS) で正本6,027行
  (`95e868d6...`) + 増分。衝突0・重複0・nodes不一致0をfail-closed gateとする。
  シナリオcache 3本 (6,028/6,030/6,031行) は**analysis-only成果物で
  canonicalではない**。
- refresh: Part Y scenario script (`88671526...`) のbyte-copy
  (差分3行: docstringのcache系列記述行・CACHE path行・CACHE sha pin行、
  diff検証で検証)、各シナリオ2回実行、全4出力がbyte-identicalであること、
  root {X,60,27} baseline 119/119 free thirdsが不変であることをgateとする。
- delta: `compare_deltas_batch11.py` (published batch-8版 compare scriptの
  batch-11適用版) がgraph + update8 receipt + scenario cacheからrefreshの
  class-status意味論 (free候補へのBoard fail-closed検証込み) を忠実に再実行し、
  BASE + 3シナリオの全class_status_countがpublished summaryと一致することを
  delta報告の前にfail-closedで門を開ける。cost-child保持クラス集合の
  graph走査による独立再導出・WIN-only flip集合の対照・加法性測定を含む。
- 主張と消費規則: verdict不消費 (z003を含む8つのunconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003) は引き続きscrutiny owner
  (C++第二実装 gate pin `9193f5b6...` 前例) 待ち)・閉鎖・被覆・root主張なし。
  **標準11x11空盤・19 central-reply roots・class 8785 (z003未採用ゆえ
  unknown 51維持)・class 8106は本分解のどの時点でもUNKNOWNのまま。
  nodes数を勝敗として読まない。** scenario cacheの採用・廃棄はscrutiny
  owner の判断であり、本レーンはcanonical cacheを書き換えない。
- transport: 各シナリオのprobe-worklist (~3.8MB, regenerable) は再出版しない
  (sha256はREADMEに記載)。
- 並走との不接触: batch-11由来のpublishedキーのみを扱う。進行中の他レーン
  (eight-row (8,12)など) のファイルには一切接触しない。同一スコープの宣言が
  mainに存在する場合は着手しない (宣言直前に最新mainを再取得・同scope対抗
  宣言なしを確認済み)。
- 本amendment observed HEAD-before-push: `3de9544503f672489149b577a6c6acb0404aff02`
  (eight-row (8,12) takeover 4コミット目 (sweep shard 1/3) 直後のmain。commit messageにも記録)。

## Part AB 出版status update (2026-11-22, verifier): batch 11 z003 if-adopted 分解 実行・出版済み - 分解8指標は全機械ゲート通過・joint greedyに非加法的 +797 を測定 (verdict不消費)

Part AB宣言 (本note Part AB節・commit `a081823a`) に基づき base control・
3シナリオ分解・公開・fetch-back検証まで完走した。verdict不消費は不変。

- Base control (cross-host再現): 実験
  `research/experiments/n11-class8785-z003-base-control-20261122/`
  (commit `36ac2359`, 7 files, fetch-back 7/7 byte一致)。pinned inputs 6種を
  repo正本からfetchしsha256全件一致 (graph `54f9c364...`・正本cache 6,027行
  `95e868d6...`・update8 `b658290a...`・board `954d3a10...`・policy
  `78655e94...`・quarantine `81d23160...`) の上で、Part Y scenario script
  (sha256 `88671526...`, published正本とbyte一致) を2回実行し、全4出力が
  run間byte-identical、closure-classes.csv・per-root-coverage.csv・
  refresh-summary.jsonの3成果物が**published Part Y正本とbyte一致**、
  probe-worklist.csv (65,154行) はsha256 `1807e4d2...` でPart Y/Z記載値と
  一致 (cross-host byte-exact再現)。
- 実験: `research/experiments/n11-centralreply-class8785-win-z003-ifadopted-20261122/`
  (commit `7f698e9a`, 32 files, fetch-back 32/32 byte一致)。
  増分3本 (published batch-11 raw両host分からfail-closed生成。4-way
  (宣告p1/p2 + takeover p1/p2) 全面一致・status.log PASS行照合・
  batch-keys照合込み・sha256 full-4 `2778d392...` / win-z003 `32c582c1...` /
  loss3 `939f8deb...`)。merge 3本 (published merger, selftest PASS,
  衝突0・重複0): 6,028行 WIN159/LOSS5,869 `3fcdbfd0...`・6,030行 WIN158/
  LOSS5,872 `ba08f924...`・6,031行 WIN159/LOSS5,872 `c5044be8...`。
  シナリオrefresh (Part Y scriptのbyte-copy、差分docstring 2行 + ROOT行 +
  CACHE行 + sha pin行、diff検証) は各2回実行し6/6 run byte-identical、
  root {X,60,27} baseline 119/119・per-root free coverage全シナリオ同一。
- 分解結果 (machine-verified, `compare_deltas_batch11.py` 全gate PASS:
  BASE+3シナリオのclass_status_count再計算がpublished summaryと完全一致、
  `output/decomp-deltas-batch11.json` sha256 `99c744b9...`):
  - **excluded_now flips: PWINZ003 = PFULL4 はちょうど3クラス
    {5307, 5748, 8785}** (graph上s5 198530のcost-child_holder、
    membership_class_count 3と3経路一致)。8785 self-exclusionは
    g018/5473・j033/1518・h045/2634と同型。PLOSS3 flips空 (gate)。
  - class 8785 unknown_now: **51 → 50 / 48 / 47** (WINのみ−1・LOSSのみ−3・
    full −4、加法性gate)。
  - **update8: z003のWINはちょうど5 groupにhit (すべてserving class 5748,
    s4_mask `[1225542048598196224, 1]`、各group unknown_s5_children 58)**。
    newly resolved baseline requirement: PWINZ003 `{198530}` (z003自身)・
    PLOSS3 `{211089}` (z004)・PFULL4 `{198530, 211089}`。remainingは
    −58 / −1 / −58 で**ぴったり1だけsub-additive**: s5 211089 (z004) は
    class 5748のcost childでもあることをgraph走査で機械確認しており、
    fullでは同s5の単独解決が win-hit群のunknown-set dropに包含されるため。
    z001/z002 (s5 86114/100564) はupdate8 baseline requirement外。
  - **joint greedy: 35,242 → 35,241 / 35,241 / 36,039 (WINのみ−1・
    LOSSのみ−1・full +797) - 本packetでは非加法**。per-root
    greedy_union_sizeの変化はroot 49のみ (2,890 → 2,899 / 2,899 / 2,946、
    +9/+9/+56。他18 rootは全シナリオbyte-同一)。group_best_options_nonfree
    は2,127で全シナリオ不変。root 49のper-root増分を超えるunion増大は
    greedy選択列の再選択滝 (option swap) 由来のscheduling量効果であり、
    被覆でもverdictでもない。Part V (h045: full == loss-only −951)・
    Part R (j033: greedy sub-additive by 1) と対照的な方向の測定値。
  - worklist 65,154 → 65,152 / 65,150 / 65,148 (−2−4=−6 完全加法)。
    free_now 35・excluded_count 390不変・root被覆は全シナリオでbase同一
    (gate)。
- scrutiny owner向け測定 (解釈なし): z003 WINのみ採用はexcluded +3・
  unknown −3・remaining −58・win-hit 5 groupを計画コストほぼ中立 (greedy
  −1) でもたらす。+797のgreedy増大は**LOSS 3行との合同採用時に限って**
  発生する (f-batch (Part H-bis +1,372) と同様、LOSS完備の性質)。z003の
  verdictは引き続き不消費・scrutiny owner (C++第二実装 gate pin
  `9193f5b6...` 前例) 待ち。
- 不変事項: z005-z051未着手。**標準11x11空盤・19 central-reply roots・
  class 8785 (canonical cache上はunknown 51のまま)・class 8106は本分解の
  どの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。** scenario
  cache 3本はanalysis-only成果物でcanonicalではない。
- transport: 各シナリオのprobe-worklist (~3.8MB, regenerable) は再出版
  なし (sha256は実験README記載: BASE `1807e4d2...`・PWINZ003 `82dbd775...`・
  PLOSS3 `ec123c74...`・PFULL4 `2ac35775...`)。
- open items (将来の別宣言): 次batch候補 = renewed rank 10 class 8106
  `[1152926194711134208, 0]` (unknown 52) の宣言・実行。
- 本status update observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。

## Part AC (prober, amendment 2026-11-22): batch 12 (class 8106, renewed rank 10) 宣言 - 反駁証拠のない次位clean候補をbatch-7 protocolで開始

batch実績は11バッチ中8 WIN-HALT + 3 clean (23963/10324/8784 = 33・34・35番目free)。
Part ABの分解出版後、renewed closure ranking (Part Y正本 closure-classes.csv,
sha256 `61943b85...`) で rank 1-8はすべて反駁証拠保持 (16757: b018, 20421: d002,
30345: b018のs5 528497, 16371: e002, 12264: f017, 5473: g018, 2634: h045,
8785: z003)、rank 9 = 1518 (j033保持) のため、反駁証拠のないfirst clean
candidateとして **rank 10 class 8106** (mask `[1152926194711134208, 0]`,
unknown 52, first=14/third=58, 4 groups) に着手する。

- 対象: `research/experiments/n11-centralreply-closure-class8106-batch12-20261122/`。
  graph class index 8106 の未確定canonical S5子52件 (n001-n052。接頭辞nは
  batch 1-11およびanchor行 (k02a/l1a) の命名系列との衝突がなく、bookkeeping
  のみ)。Part Y re-audit正本probe-worklist (65,154行、sha256
  `1807e4d21f6fb757ea21850c6bda4d822cb76ac59abfa9bcd1cc7b53bd7055ef`) の
  `serving_class=8106` 行 (probe_order 434-485・Board再計算合法手数固定。52行
  すべてclosure group first=14/third=58所属・classがserveする4グループの
  うちこのgroupに残存unknown子が集中)。52行はbatch-keys.jsonに
  全行published (正本cache・update8機構に対して独立照合可能)。
- 宣言前fail-safe機械確認 (本ホスト・fail-closed): (1) 実行環境リセットにより
  ローカル作業ツリーを失ったため、pinned inputs 6種 (dependency-graph
  `54f9c364...`・正本merged cache 6,027行 `95e868d6...`・update8 plan
  `b658290a...`・Board `954d3a10...`・policy `78655e94...`・quarantine
  `81d23160...`) をrepo正本 (commit `0a369d6c` 固定raw) から再取得しsha256
  全件一致を確認の上、published Part Y scenario script (sha256 `88671526...`)
  を2回再実行してclosure-classes.csv・per-root-coverage.csv・
  refresh-summary.jsonの3成果物がpublished Part Y正本とbyte一致、
  probe-worklist.csv (65,154行) はsha256 `1807e4d2...` でPart Y/Z記載値と
  一致することをcross-host byte-exactで再確認した (worklistの全52行抽出は
  この再生成正本から行った)。(2) 52/52キーは正本merged cache (6,027行・
  sha256 `95e868d6...`) に不在 (0 hits)。(3) quarantine registry
  (sha256 `81d23160...`・active 2件) とのkey対照 0 hits (両方向)。
  (4) 52キー重複なし・closure-classes rank 10行 (class 8106・mask
  `[1152926194711134208, 0]`・unknown 52・first 14/third 58) と正本一致。
  (5) 8つのunconsumed WINキー (b018/d002/e002/f017/g018/j033/h045/z003) は
  class 8106の52子に不在 (cost-child対照 0 hits、Part Z記載の機械確認と同一
  結果)。
- val-gate: published two-target-design 4行を本ホストで再現、4/4 node-exact
  (at2m result 0/2,000,000 ×2、15m result 2/3,651,923 と result 2/5,040,200。
  本ホストのfresh出力4件はscaffoldのoutput/val-gate/に固定)。
- 手法・停止規則・消費規則: Part B-Zと全部同一 (pinned replica `jsreplay.js`
  sha256 `845856175d...`・batches 1-11とbyte-identical、2-pass fresh cold、
  budget 15M、mismatch→HARD-STOP rc=42、WIN→HALT rc=45、枯渇=UNKNOWN、
  消費はfail-closed merger経由のみ、本batch単体では閉鎖・被覆・secured主張
  なし)。実行並列は本ホスト最大4 worker (probe_order順4キーwave実行・
  WIN報告wave完了後は新規キー着手なし・同一wave内のin-flight完了行は誠実開示、
  batch-5 f018先例)。
- 主張の範囲: 本batchはcoverage・closure・rootを一切主張しない。WIN-HALT
  (rc=45) が発火した場合はそのkeyで停止しif-adopted解析に回す (予登録
  stop rule)。全52本LOSSでも消費はfail-closed increment merge + refresh
  再監査まで行わない (将来のverifier宣言)。**class 8106・19 central-reply
  roots・標準11×11空盤はUNKNOWNのまま。nodes数・pass数を勝敗として読まない。**
- 並走との不接触: batch-8 (Part N/U/V/W)・batch-9 (Part Q/R/T)・batch-10
  (Part X/Y)・batch-11 (Part Z/AA/AB) のpublishedファイルには一切接触しない。
  同一スコープの宣言がmainに存在する場合は着手しない (宣言直前に最新mainを
  再取得・class8106実験dirの不在・Part AC採番の未使用を確認済み)。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミット
  メッセージに記録。

## Part AC 出版status update (2026-11-22, prober): batch 12 (class 8106) WIN-HALT x2 at n005/n006 - 同一wave内で2つのWINを検出 (8/52 probed・verdict不消費)

Part AC宣言 (本note Part AC節・commit `609e9137`) に基づき、宣言・scaffold出版
(d333bb2c, 65 files, fetch-back 65/65 byte一致)・実行・出版までを同一セッションで
完走した。**verdict不消費は不変。**

- 実行結果 (machine-verified): 52キー中 **8キー (n001-n008)** をprobe
  (probe_order順4キーwave, 本ホスト `8c50fb9e...` 2 core・最大4 worker・
  budget 15M・2-pass fresh cold)。全完了キー2-pass node-exact、
  determinism mismatch (rc=42) 0・budget枯渇 (result 0) 0。
  **wave 2で事前登録WIN-HALT規則 (rc=45) が2キーで発火**: 
  **n006 (s5_index 219608, key `[1152926194711134208, 128]`, legal 78,
  probe_order 439): result 1 (WIN), 3,695,373 nodes** および
  **n005 (s5_index 188395, key `[1153489144664555520, 0]`, legal 82,
  probe_order 438): result 1 (WIN), 12,863,268 nodes**。両キーとも
  2-pass node-exact。同一wave内のin-flight残キーは完了・誠実開示
  (n007 LOSS 2,905,330 / n008 LOSS 3,442,689)。wave 1の4キーは全てLOSS
  (n001 6,471,615 / n002 3,083,301 / n003 4,560,719 / n004 3,710,926)。
  n009-n052 (44キー) は未着手のまま。**同一バッチ内で2つのWINが検出された
  のはclosure grind初。**
- n006のkeyはclass 8106のmask `[1152926194711134208, 0]` と同じloを持ち、
  hiのみ128が立つ正規子である (n007 `[...4210, 0]`・n008 `[...4212, 0]` と
  probe_orderで隣接する系統。観測の記録であり解釈を含まない)。
- n005/n006は**9番目と10番目のunconsumed closure WIN**
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006) として
  scrutiny owner (C++第二実装 gate pin `9193f5b6...` 前例) 待ち。
  第三実装交叉検証 (Part G/K/O/P/T/W/AA流) は未実施・将来のverifier宣言。
  if-adopted分解 (Part V/R/AB流, WIN-only / LOSS-only / full の8行分解)
  も未実施・別宣言。**class 8106 (2 WIN子を含むが採用は未決)・19
  central-reply roots・標準11×11空盤はいかなる時点でもUNKNOWNのまま。
  nodes数を勝敗として読まない。**
- 8106の52子に9-10 WIN移行前の8 WINキーが不在 (0 hits) であることは宣言時
  fail-safe (5) で機械確認済み。batch実績は **12バッチ中9 WIN-HALT +
  3 clean** (23963/10324/8784 = 33・34・35番目free)。安価側WIN密集の実測
  傾向 (12ショットで2 WIN/1バッチ) はPart H-bis以来のscheduling測定値と
  して累積され、クラスstatusには影響しない。
- 次候補: 8106がn005/n006の反駁証拠を保持するため、renewed rankingの
  次のfirst clean candidateは **rank 11 class 16930**
  (`[1152921504875282432, 272]`, unknown 52, first=26/third=70, 3 groups,
  worklist 52行 = probe_order 486-537)。10-WINキーと16930の52 worklist子の
  対照は0 hits (本statusの機械確認)。宣言時には他のfail-safeとともに
  再確認する。
- 出版: 実験 `n11-centralreply-closure-class8106-batch12-20261122/
  commits `609e9137` (note Part AC宣言) → `d333bb2c` (scaffold 65 files,
  fetch-back 65/65 byte一致) → `eca35f3c` (chunk 1/2: n001-n004 raws 8件,
  fetch-back 8/8) → `ace92d84` (chunk 2/2: n005-n008 raws 8件 + status.log,
  fetch-back 9/9) → `68f2c699` (README Result節)。宣言・scaffold出版前に
  実行環境リセットでワークスペースを喪失したため、Part Y pinned inputs
  6種をrepo正本 (commit `0a369d69` 固定raw) から再取得し (sha256全件一致)、
  published Part Y scenario script (`88671526...`) を2回再実行、全4出力が
  run間byte-identical・3成果物がpublished Part Y正本とbyte一致・worklist
  (65,154行) がsha256 `1807e4d2...` で正本記載値と一致することを
  cross-hostで再確認した上で52キーを抽出した (Part AB base controlと
  同一の再現手順)。kit mirror `_19root-refresh-kit/batch8106-n/` は
  input/scripts/val-gate/raws/status/READMEを保持。
- transport: probe-worklist (~3.8MB, regenerable) は再出版しない
  (shaは実験README・base controlの記載通り)。
- 並走との不接触: batch-11 (Part Z/AA/AB) 以前の全publishedファイルには
  一切接触していない (宣言直前の最新main再取得で確認)。
- 本status update observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。


## Part AD (verifier, amendment 2026-11-22): batch 12 (class 8106) n005/n006 第三実装交叉検証 (declared before execution)

batch 12 (Part AC, class 8106, renewed rank 10) は同一wave内の2キーで事前登録のWIN-HALT規則
(rc=45) が発火して停止した: **n006 (s5_index 219608, key `[1152926194711134208, 128]`, legal 78,
probe_order 439): result 1 (WIN), 3,695,373 nodes** および **n005 (s5_index 188395, key
`[1153489144664555520, 0]`, legal 82, probe_order 438): result 1 (WIN), 12,863,268 nodes**
(いずれも2-pass fresh cold node-exact・published chunk commits `eca35f3c`/`ace92d84`)。
Part K/O/P/T/W/AAの前例に従い、batch-12の両WIN行 n005/n006 と、probed LOSS全6行
(n001/n002/n003/n004/n007/n008 — batch-12は8/52 probedのため、Part AAと同一規則で
検査済み全行が対象) を第三実装 (`third_impl.js`, pin sha256 `08ea958f...`) でverdict-level
交叉検証する。**verdict不消費・採用判断は引き続きscrutiny owner (C++第二実装 gate pin
`9193f5b6...` 前例・不変)。**

- 対象: `research/experiments/n11-centralreply-closure-batch12-wins-thirdimpl-20261122/`。
  target 8行 (n005 WIN + n006 WIN + n001/n002/n003/n004/n007/n008 LOSS)・anchor 2行
  (k02a/l1a, Part G/K/O/P/T/W/AAと同一のpublished第三実装値 9,106,337 expansions/
  4,991,527 ttHits と 7,660,602/3,951,175)・negative 2行 (ng1/ng2)。入力はpublished
  batch-12 raw (8キー×p1/p2の16ファイル、chunk commits `eca35f3c`/`ace92d84`から
  commit-pinned raw CDN取得) から `make_inputs_batch12.py` がfail-closed導出する
  (手転写ゼロ・2-pass (budget, result, nodes) 一致assert・status.logのPASS 8行照合・
  `n005 WIN-HALT`/`n006 WIN-HALT`停止行とRUNNER-STOP/RUNNER-EXIT行の存在assert・
  key/legalをpublished batch-keys.json (sha256 `de55df83...`, scaffold commit
  `d333bb2c` 正本) と機械照合・導出input CSVがpublished batch-12 input CSV 8本と
  byte一致することをassert)。sourcesは再出版しない。
- 前提ゲート (いずれも必須・fail-closed): script pin 3種 (`08ea958f...` / `c8c52528...` /
  `84585617...`)、rule-engine gate (verify_tbl.js: quads 95,670 == replica / triples
  195,044 mismatches 0)、anchor 2行の本ホスト再現がpublished値と完全一致、negative 2種
  (ng1/ng2) の文言一致GATE_FAIL。手法: 1行1プロセス、cap 300M expansions、wallcap
  240s、1行2回 (a/b) determinism gate (result/expansion/ttHits/reason同一必須)。
  wall超過 (runlimit) はhonest wall-inconclusiveとして記録し検証主張としない。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・verdict不消費。n005/n006のWINは
  9番目・10番目のunconsumed closure WIN (b018/d002/e002/f017/g018/j033/h045/z003/
  n005/n006) として引き続きscrutiny owner待ち。標準11x11空盤・19 central-reply roots・
  class 8106は本検証のどの時点でもUNKNOWNのまま。n009-n052 (44キー) は未着手のまま。
  nodes/expansionsを勝敗として読まない。
- 並走との不接触: 対象はpublished batch-12由来キーのみ (chunk commits `eca35f3c`/
  `ace92d84`・scaffold `d333bb2c`・status.log) で、他レーン (r=9 crosscheck・eight-row等)
  ・進行中の実験と無関係。同一スコープの宣言がmainに存在する場合は着手しない
  (宣言直前に最新mainを再取得・同scope対抗宣言なし・Part AD採番未使用を確認済み)。
- 本amendment observed HEAD-before-push: 9759774ba3765531329f71a5b09a2180e8283a0e
  (commit messageにも記録)。

## Part AE (probe-batch owner, amendment 2026-11-22): batch 13 (class 16930, renewed rank 11) 宣言 (verdict不消費・実行前に宣言)

batch 12 (Part AC, class 8106) は事前登録のWIN-HALT規則により n006/n005 の2 WINで停止し
(rank 10に反証証拠が付いた。batch-12の8 probed行の第三実装交叉検証は別所有者のPart AD
宣言 (`33657c94`, 対象 `batch12-wins-thirdimpl-20261122`) のスコープであり本宣言は接触しない)。
事前登録の選択規則 (反証証拠なし・in flightなし・WIN-HALTなしの最初のclean候補) で、renewed
rank 1-9は全て反証証拠持ち (16757: b018, 20421: d002, 30345: b018 cost child s5 528497,
16371: e002, 12264: f017, 5473: g018, 2634: h045, 8785: z003, 1518: j033)、rank 10 (8106) は
Part ACでWIN-HALT済み。よって**renewed rank 11 class 16930** (mask
`[1152921504875282432, 272]`, unknown 52, first 26 / third 70, groups 3) をbatch 13として宣言する。

- 対象: `research/experiments/n11-centralreply-closure-class16930-batch13-20261122/`。
  keys 52件 p001-p052 (probe_order 486-537), Part Y worklist (65,154行, sha `1807e4d2...`)
  の `serving_class=16930` 行から機械抽出。batch-keys.json sha256
  `c6c56a1a0552b8a87d1e1f5f9e0d6c3955cf1f58a85ef6726317d17846a0a2c7`。
- 宣言前fail-safe (全て本実行内に機械実施・全PASS): (1) canonical merged cache 6,027行
  (sha `95e868d6...`) に52/52不在・0 hits、(2) quarantine registry (sha `81d23160...`,
  active 2) 両方向0 hits、(3) 52キー重複なし、(4) closure-classes.csv rank 11行 = class
  16930 (`[1152921504875282432, 272]`, unknown 52, first 26 / third 70, groups 3) published
  Part Y正本とbyte一致 (closure-classes / per-root-coverage / refresh-summary 3点とも
  commit `7eb9ab70` 時点のmain正本とbyte一致を再確認)、(5) 10 WINキー
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006) 交叉0 hits、(6) probe_order連続
  486-537・全行 class_unknown_now=52。
- worklist再生成: 本workspace系譜のPart Y再生成 (run1/run2 byte一致, sha `1807e4d2...`,
  published正本とcross-host byte一致, batch-12 Part AC scaffold READMEに記録済み) を再検証
  の上再利用 (再実行 不要・再出版しない)。
- protocol (事前登録・batch 12と同一): pinned replica `jsreplay.js` (sha `84585617...`),
  1キー2 fresh cold pass, budget 15,000,000, determinism mismatchでHARD-STOP (rc=42),
  WIN検出でWIN-HALT (rc=45, 同wave内in-flightは完了まで開示), 最大4 worker (2-core host,
  実行並列はdeterminismに影響しない: 全passがshare_tt=0 fresh cold process),
  resume-safe runner, honest negative (result 0 = UNKNOWN)。
- validation gate (実行前に本ホストでfresh再現・4/4 node-exact): at2m result 0/2,000,000
  ×2, 15m result 2/3,651,923 / result 2/5,040,200。
- 主張と消費規則: 本batchはverdict不消費。WIN行はunconsumed closure WIN (今後の採用判断は
  scrutiny owner, C++第二実装 gate 前例・不変)。標準11x11空盤・19 central-reply roots・
  class 16930は本batchのどの時点でもUNKNOWNのまま。nodesを勝敗として読まない。
  batch選択はscheduling quantityでありverdictではない。
- 並走との不接触: Part AD (別所有者) を始め他レーンのpublishedファイルには一切接触しない。
  宣言直前に最新mainを再取得し、同scope対抗宣言なし・`batch13` dir不在・Part AE採番未使用
  を確認済み。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part AD 出版status update (2026-11-22, verifier): batch 12 n005/n006 第三実装交叉検証 実行・出版済み - 10のunconsumed WIN全て第三実装検証済みに (verdict不消費)

Part AD宣言 (本note Part AD節・commit `33657c94`) に基づき実行・出版した。
宣言通りverdict不消費・verdict-level文献作成のみ (採用判断は引き続き
scrutiny owner、C++第二実装 gate pin `9193f5b6...` 前例・不変)。

- 実行結果 (machine-verified): target 8行すべてclean・a/b 2回実行で同一
  (result/expansion/ttHits/reason)。**n005/n006 WIN一致** (n005: 第三実装
  15,280,890 expansions / 8,220,782 ttHits vs replica df-pn WIN 12,863,268
  nodes; n006: 4,233,764 / 2,394,370 vs 3,695,373 nodes)、
  n001-n004/n007/n008 LOSS一致 6/6 (第三実装 7,693,366 / 3,554,378 /
  5,243,307 / 4,271,858 / 3,359,814 / 3,976,246 expansions vs replica
  6,471,615 / 3,083,301 / 4,560,719 / 3,710,926 / 2,905,330 / 3,442,689
  nodes)。anchors k02a (WIN 9,106,337 expansions / 4,991,527 ttHits) と
  l1a (LOSS 7,660,602 / 3,951,175) は本ホスト再現値がpublished第三実装値
  (Part G/K/O/P/T/W/AA) と完全一致。negative ng1/ng2は文言一致GATE_FAIL。
  rules gate (quads 95,670 == replica / triples 195,044・mismatch 0) PASS。
  audit.py (fail-closed, schema `batch12-wins-thirdimpl-audit-v1`, 2回実行
  byte一致) は **111/111 gates PASS・divergence 0・wall-inconclusive 0**。
- 入力はpublished batch-12正本 (raw 8キー×p1/p2 16件・status.log、chunk
  commits `eca35f3c`/`ace92d84`からcommit-pinned raw CDN取得) から
  `make_inputs_batch12.py` がfail-closed導出 (2-pass (budget,result,nodes)
  一致assert・status.logのPASS 8行照合・`n005 WIN-HALT`/`n006 WIN-HALT`
  停止行とRUNNER-STOP/RUNNER-EXIT行の存在assert・published batch-keys.json
  (sha256 `de55df83...`, scaffold commit `d333bb2c`正本) とのkey/legal機械
  照合・導出input CSVがpublished batch-12 input CSV 8本とbyte一致する
  ことのassert・手転写ゼロ・全ゲート通過)。
- 出版: `research/experiments/n11-centralreply-closure-batch12-wins-thirdimpl-20261122/`
  commits `4e9c525f` (scaffold 20 files: README + pinned scripts 6 +
  machine-derived inputs 13、pinned scripts 4種はpublished Part AA bytesと
  blob同一性確認) → `d44fcfb4` (targets a/b 16) → `d25a0db9` (anchors 4 +
  negative 2 + rules-gate + status.log + audit-summary.json + MANIFEST,
  10 files)。fetch-back: commit固定raw URL + cmpで**全46 files byte一致**・
  MANIFEST-sha256.txt記載45エントリが45/45 sha256一致を確認済み。
  sourcesは再出版なし (published raws由来・READMEにsha記載)。
- 意味: 10つのunconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006) の**全てが第三実装に
  よるverdict-level交叉検証済み**になった (前6個はwin-thirdimpl-reverify
  (Part G) + Part P + Part T (j033) + Part W (h045)、z003がPart AA、
  n005/n006が本Part AD)。ただし**verdict不消費は不変**。n005/n006のWINは
  引き続きscrutiny owner待ち。n009-n052 (44キー) は未着手のまま。
  **標準11x11空盤・19 central-reply roots・class 8106は本検証のどの時点でも
  UNKNOWNのまま。nodes/expansions数を勝敗として読まない。**
- open items (将来の別宣言で実施): n005/n006 if-adopted分解 (Part V/R/AB流・
  8 probed行のWIN-only / LOSS-only / full)・次batch候補 = renewed rank 11
  class 16930 `[1152921504875282432, 272]` (unknown 52)。
- 本status update observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。

## Part AE (probe-batch owner, status update 2026-11-22): batch 13 (class 16930) WIN-HALT x2 公表 (verdict不消費)

batch 13 (class 16930, renewed rank 11) は宣言 (`72608b64`, fetch-back byte一致, note全体sha
`42e8770a...`)・scaffold (`90ee1c87`, 65/65 fetch-back byte一致, batch-keys.json sha
`c6c56a1a...`)・val-gate (本ホストfresh再現4/4 node-exact: at2m result 0/2,000,000 ×2, 15m
result 2/3,651,923 / result 2/5,040,200) の後、runner 2026-11-22T12:16:52Z開始。
**4/52 probedで事前登録WIN-HALT規則 (rc=45) が発火**し 12:21:20Z停止 (2-coreホスト, 最大4 worker):

- **p003 WIN: result 1, 2-pass fresh cold node-exact, 7,489,274 nodes, key
  `[3458764514088976384, 272]`, legal 81, s5_index 203419, probe_order 488**
- **p002 WIN: result 1, 2-pass fresh cold node-exact, 10,770,254 nodes, key
  `[1153484454828703744, 272]`, legal 85, s5_index 185003, probe_order 487**
- 同wave内 in-flight完了 (誠実開示, batch-5 f018先例): p001 LOSS 4,631,275 nodes / p004 LOSS
  2,291,059 nodes。determinism mismatch (rc=42) なし・budget枯渇 (result 0) なし。
  p005-p052 (48キー) は未着手のまま。

p002/p003は**11番目・12番目のunconsumed closure WIN**
(b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003)。verdictは不消費・採用判断は
scrutiny owner (C++第二実装 gate pin `9193f5b6...` 前例) 待ち。2 WINはclass 16930の
all-LOSS closure routeへの反証証拠としてのみ記録し、class status自体はUNKNOWN・refresh機構
由来のまま。batch実績: 13バッチ 11 WIN-HALT + 3 clean (23963/10324/8784 = 33/34/35番目Board検証free)。

出版: 宣言 `72608b64` → scaffold `90ee1c87` → raws chunk `b4b55ec8` (9/9 fetch-back byte一致) →
README Result `f5df3cbf` (fetch-back byte一致)。次のfirst-clean候補: renewed rank 12 class
23101 (`[1152921504892059648, 16]`, unknown 52, 宣言時fail-safe再実行前提)。第三実装交叉検証
(p002/p003 + LOSS 2行) と if-adopted decomposition は将来宣言待ち。

運用上の開示 (並走衝突の記録と機械照合): 本実行は compaction 前に batch-12 n005/n006
第三実装交叉検証 (Part ADと同scope) を実行済みだったが、最新main再取得で**別所有者のPart AD
宣言 (`33657c94`, 対象 `batch12-wins-thirdimpl-20261122`) を検出**し、規則「同一スコープの
宣言がmainに存在する場合は着手しない」に従い**本インスタンスの重複実行結果は出版せず撤退**
した (kit mirror `batch8106-n-thirdimpl` に保全)。撤退後に機械照合した結果、Part ADは
`4e9c525f`/`d44fcfb4`/`d25a0db9` で完走・出版済み (46 files fetch-back byte一致・111/111
gates PASS) であり、本インスタンスのaudit-summaryがPart AD出版のaudit-summary
(`d25a0db9`) と**全8 target行 (replica_result, third_result, third_expansion,
third_ttHits) で完全一致**した (第三実装のcross-host reproducibility の追加corroboration
として記録。verdict処理には無関係・不変にUNKNOWN)。テンプレート警告 (将来のverified文献作成時
向け): Part AA雛形からaudit.pyを複製した場合、`EXP`/schema文字列が `batch11-z003` のまま
残りaudit-summary.jsonが実験を誤標識することがある (本実行のローカルコピーで実際に検出・
修正済み。Part AD出版版は `batch12-wins-thirdimpl-audit-v1` に正しく書き換えられている)。

標準11x11空盤・19 central-reply roots・class 16930は本batchのどの時点でもUNKNOWNのまま。
nodesを勝敗として読まない。本status update observed HEAD-before-push: コミットメッセージに記録。

## Part AF (probe-batch owner, amendment 2026-11-22): batch 14 (class 23101, renewed rank 12) 宣言 (verdict不消費・実行前に宣言)

batch 13 (Part AE, class 16930) はWIN-HALT x2 (p003/p002) で停止し、rank 10・11に反証証拠が
付いた (batch-12のPart AD第三実装・batch-13の2 WINの交叉検証は将来宣言待ち)。事前登録の
選択規則で、renewed rank 1-9は全て反証証拠持ち (16757: b018, 20421: d002, 30345: b018
cost child s5 528497, 16371: e002, 12264: f017, 5473: g018, 2634: h045, 8785: z003,
1518: j033)、rank 10 (8106) はPart AC、rank 11 (16930) はPart AEでWIN-HALT済み。よって
**renewed rank 12 class 23101** (mask `[1152921504892059648, 16]`, unknown 52, first 24 /
third 28, groups 3) をbatch 14として宣言する。

- 対象: `research/experiments/n11-centralreply-closure-class23101-batch14-20261122/`。
  keys 52件 q001-q052 (probe_order 538-589), Part Y worklist (65,154行, sha `1807e4d2...`)
  の `serving_class=23101` 行から機械抽出。batch-keys.json sha256
  `dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f`。
- 宣言前fail-safe (全て本実行内に機械実施・全PASS): (1) canonical merged cache 6,027行
  (sha `95e868d6...`) に52/52不在・0 hits、(2) quarantine registry (sha `81d23160...`,
  active 2) 両方向0 hits、(3) 52キー重複なし、(4) closure-classes.csv rank 12行 = class
  23101 (`[1152921504892059648, 16]`, unknown 52, first 24 / third 28, groups 3) published
  Part Y正本とbyte一致、(5) 12 WINキー
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003) 交叉0 hits、
  (6) probe_order連続538-589・全行 class_unknown_now=52。
- protocol (事前登録・batch 12/13と同一): pinned replica `jsreplay.js` (sha
  `84585617...`), 1キー2 fresh cold pass, budget 15,000,000, determinism mismatchで
  HARD-STOP (rc=42), WIN検出でWIN-HALT (rc=45, 同wave内in-flightは完了まで開示),
  最大4 worker (2-core host), resume-safe runner, honest negative (result 0 = UNKNOWN)。
- validation gate (実行前に本ホストでfresh再現・4/4 node-exact): at2m result 0/2,000,000
  ×2, 15m result 2/3,651,923 / result 2/5,040,200。
- 主張と消費規則: 本batchはverdict不消費。WIN行はunconsumed closure WIN (採用判断は
  scrutiny owner, C++第二実装 gate pin `9193f5b6...` 前例・不変)。標準11x11空盤・19
  central-reply roots・class 23101は本batchのどの時点でもUNKNOWNのまま。nodesを勝敗と
  して読まない。batch選択はscheduling quantityでありverdictではない。
- 並走との不接触: Part AD (別所有者) を始め他レーンのpublishedファイルには一切接触しない。
  宣言直前に最新mainを再取得し、同scope対抗宣言なし・`batch14` dir不在・Part AF採番未使用
  を確認済み。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part AG (verifier, declaration 2026-11-22): batch 13 (class 16930) p002/p003 第三実装交叉検証 (verdict不消費・実行前に宣言)

batch 13 (Part AE, class 16930, renewed rank 11) は4/52 probedで事前登録WIN-HALT規則が
同一wave内で2回発火し (p003: 2-pass fresh cold node-exact result 1, 7,489,274 nodes /
p002: result 1, 10,770,254 nodes; 同waveの in-flight p001/p004 は誠実開示済み LOSS)、
p002/p003 が11番目・12番目のunconsumed closure WINとして残っている (採用判断は
scrutiny owner, C++第二実装 gate pin `9193f5b6...` 前例・不変)。Part AEのstatus
updateが「第三実装交叉検証 (p002/p003 + LOSS 2行) は将来宣言待ち」と掲げた本件を、
Part G/K/O/P/T/W/AA/AD と同一規約で単一オーナーとして宣言する。
**verdict不消費・検証はverdict-level文献作成のみ。**

- 対象: `research/experiments/n11-centralreply-closure-batch13-wins-thirdimpl-20261122/`。
  target = batch-13のprobed全行4件: WIN 2行 (p002, p003) + LOSS 2行 (p001, p004)。
  anchors k02a (WIN, legal 87, 期待 9,106,337 expansions / 4,991,527 ttHits) と
  l1a (LOSS, legal 116, 期待 7,660,602 / 3,951,175) は本ホスト再現、negatives
  ng1 (legal+1) / ng2 (stones+1) は文言一致GATE_FAIL必須。
- sources (再出版せず・commit-pinnedに取得): published batch-13 raws 8件
  (p001-p004 x p1/p2, chunk commit `b4b55ec8`)・status.log (同chunk)・
  batch-keys.json (sha256 `c6c56a1a0552b8a87d1e1f5f9e0d6c3955cf1f58a85ef6726317d17846a0a2c7`,
  scaffold `90ee1c87`)・published input CSV 4件。`make_inputs_batch13.py` (Part AD版を
  adapt・schema/EXP文字列は `batch13-wins-thirdimpl` に書き換え・Part AE警告対応) が
  fail-closed導出: 2-pass一致assert・status.log PASS行・`p003 WIN-HALT`/`p002 WIN-HALT`
  停止行・RUNNER-STOP/RUNNER-EXIT行の存在assert・class_index 16930 assert・
  導出input CSVがpublished input CSVとbyte一致するassert・手転写ゼロ。
- 手法: pinned `third_impl.js` (sha256 `08ea958f...`)・1行1プロセス・
  `--cap=300000000 --wallcap=240 --memo-power=22`・1行2回 (a/b) determinism gate
  (result/expansion/ttHits/reason 同一必須)・rule-engine gate (`verify_tbl.js`:
  quads 95,670 == replica / TBL==wob mismatches 0) をtarget走行前に実施。
  2-coreホストで最大2並列。wall超過 (runlimit) はhonest wall-inconclusive と
  して記録し検証主張としない。cleanな不一致はdivergence evidence として記録
  するが本レーンはverdictを書き換えない。
- 主張と消費規則: verdict不消費 (採用は引き続き scrutiny owner・不変)。
  標準11x11空盤・19 central-reply roots・class 16930は本検証のどの時点でも
  UNKNOWNのまま。nodes/expansions数を勝敗として読まない。
- 並走との不接触: batch 14 (Part AF, class 23101) のprobe中ファイル・他レーンの
  publishedファイルには一切接触しない。宣言直前に最新mainを再取得し、同scope
  (batch13第三実装)対抗宣言なし・`batch13-wins-thirdimpl` dir不在・Part AG採番
  未使用を確認済み。同一スコープの宣言がmainに存在する場合は本宣言を破棄
  して着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。
