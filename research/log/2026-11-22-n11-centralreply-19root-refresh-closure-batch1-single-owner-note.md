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

## Part AG 出版status update (2026-11-22, verifier): batch 13 p002/p003 第三実装交叉検証 実行・出版済み - 12のunconsumed WIN全て第三実装検証済みに (verdict不消費)

Part AG宣言 (本note Part AG節・commit `e84242c8`・fetch-back byte一致) に基づき実行・
出版した。宣言通りverdict不消費・verdict-level文献作成のみ (採用判断は引き続き
scrutiny owner、C++第二実装 gate pin `9193f5b6...` 前例・不変)。

- 実行結果 (machine-verified): target 4行すべてclean・a/b 2回実行で同一
  (result/expansion/ttHits/reason)。**p002/p003 WIN一致** (p002: 第三実装
  12,593,747 expansions / 7,021,485 ttHits vs replica df-pn WIN 10,770,254
  nodes; p003: 8,626,319 / 4,959,871 vs 7,489,273 nodes)、p001/p004 LOSS一致
  2/2 (5,334,954 / 3,020,029と2,593,393 / 1,571,815 vs replica 4,631,275 /
  2,291,059 nodes)。anchors k02a (WIN 9,106,337 expansions / 4,991,527 ttHits)
  と l1a (LOSS 7,660,602 / 3,951,175) は本ホスト再現値がpublished第三実装値
  (Part G/K/O/P/T/W/AA/AD) と完全一致。negative ng1/ng2は文言一致GATE_FAIL。
  rules gate (quads 95,670 == replica / triples 195,044・mismatch 0) PASS。
  audit.py (fail-closed, schema `batch13-wins-thirdimpl-audit-v1`, 2回実行
  byte一致) は **71/71 gates PASS・divergence 0・wall-inconclusive 0**。
- 入力はpublished batch-13正本 (raw 4キー×p1/p2 8件・status.log、chunk commit
  `b4b55ec8`からcommit-pinned raw CDN取得) から `make_inputs_batch13.py`
  (Part AD版をadapt・schema/EXP文字列はbatch13に書き換え・Part AEテンプレート
  警告対応) がfail-closed導出 (2-pass一致assert・status.log PASS 4行照合・
  `p003 WIN-HALT`/`p002 WIN-HALT`停止行とRUNNER-STOP/RUNNER-EXIT行の存在assert・
  batch-keys.json (sha256 `c6c56a1a...`, scaffold `90ee1c87`正本) との
  key/legal機械照合・class_index 16930 assert・導出input CSVがpublished
  batch-13 input CSV 4本とbyte一致するassert・手転写ゼロ・全ゲート通過)。
- 実行開示 (honesty): runner (`runner-all-thirdimpl.sh`) のnegative 2連結が
  `&&`のため、ng1 (GATE_FAILでrc=1は設計どおり) の時点でng2がrunner内では
  実行されず、runner exit直後に本ホストで単独実行してからauditした (README
  Honesty recordに記載・audit gateは両negativesに文言で照合)。
- 出版: `research/experiments/n11-centralreply-closure-batch13-wins-thirdimpl-20261122/`
  3コミット合计35 files (scaffold: README + pinned scripts 7 + machine-derived
  inputs 9 → targets a/b 8 → anchors 4 + negative 2 + rules-gate + status.log +
  audit-summary.json + MANIFEST 10)。fetch-back: commit固定raw URL + cmpで
  **全35 files byte一致**・MANIFEST-sha256.txt記載34エントリが34/34 sha256一致
  を確認済み。sourcesは再出版なし (published raws由来・READMEにsha記載)。
- 意味: 12つのunconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003) の**全てが
  第三実装によるverdict-level交叉検証済み**になった。ただし**verdict不消費は
  不変**。p002/p003のWINは引き続きscrutiny owner待ち。p005-p052 (48キー) は
  未着手のまま。**標準11x11空盤・19 central-reply roots・class 16930は本検証の
  どの時点でもUNKNOWNのまま。nodes/expansions数を勝敗として読まない。**
- open items (将来の別宣言で実施): batch-13 4 probed行のif-adopted分解
  (Part V/R/AB流・WIN-only p002/p003 / LOSS-only p001/p004 / full 4行)・
  batch-12 8 probed行のif-adopted分解 (n005/n006・Part AD open item)。
  batch 14 (class 23101, Part AF) は並走がprobe継続中で本レーン非接触。
- 本status update observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録。

## Part AH (read-only analysis, declaration 2026-11-22): batch 12 (class 8106) n005/n006 if-adopted 分解 (verdict不消費・実行前に宣言)

Part ADがopen itemとして掲げた「n005/n006 if-adopted分解 (Part V/R/AB流・
8 probed行のWIN-only / LOSS-only / full)」を単一オーナーとして宣言する。
solver探索なし・verdict不消費・新規主張ゼロのwhat-if計画・監査計算。

- 対象 (2実験dir):
  (a) `research/experiments/n11-class8106-n005n006-base-control-20261122/`
      - published Part Y refresh scenario script `refresh_19root_frontier.py`
        (sha256 `88671526...`) を本ホストで2回実行し、3出力をpublished
        Part Y正本 (`n11-central-reply-8784-closure-reaudit-20261122`) と
        byte一致させる (cross-host再現・run間byte一致)。
      - 入力はpublished正本からcommit-pinnedに取得しsha固定: dependency-graph
        `54f9c364...`・merged chain cache 6,027行 `95e868d6...`・update8 plan
        `b658290a...`・Board source `954d3a10...`・evidence policy
        `78655e94...`・quarantine registry `81d23160...`。
      - probe-worklist.csv (65,154行, `1807e4d2...`) は再生成可能なため
        sha記録のみで再出版しない (Part AB流)。
  (b) `research/experiments/n11-centralreply-class8106-win-n005n006-ifadopted-20261122/`
      - increments: batch-12 raw 16件 (p1/p2 x 8キー)・status.log・batch-keys
        (sha `de55df83...`, scaffold `d333bb2c`正本) からfail-closed生成
        (2-pass一致・status PASS行照合・key/legal機械照合・手転写ゼロ。
        batch-12は宣言hostが全行実行のため4-way host交差は不要・3-way
        (p1/p2/status) でfail-closed)。3種: full 8行 (n001-n004/n007/n008
        LOSS + n005/n006 WIN)・win-only 2行 (n005/n006)・loss-only 6行
        (n001-n004/n007/n008)。**win-only 2行はclosure grind初の複数WIN
        increment** (z003の1行を超える)。
      - scenario caches: canonical 6,027行 + increment をpublished union
        merger (fail-closed・WIN/LOSS衝突0・重複0・selftest) でmergeした
        分析用cache 3種 (正本ではない)。
      - scenario refresh: scenario cache向けにadaptしたscenario script
        (docstring・ROOT行・CACHE行・sha pin行のみ変更・diff検証) を各2回
        実行しrun間byte一致を確認。baseline guarantee (root first=27
        119/119 free thirds・per-root free coverage不変) をmachine gateで確認。
      - delta抽出: `compare_deltas_batch12.py` (Part AB版をadapt) が
        excluded_now flip集合 (frozen graphのWIN子保持機械特定)・update8
        newly-resolved indices (increment行にgate)・加法性指標・per-root
        greedy表・win-hit groups群を機械算出し、全class_status_countを
        再実行してpublished summaryと一致をassertしてからdelta報告
        (Board fail-closed free検証込み)。
- 主張と消費規則: 本分解はread-only what-if解析・verdict不消費。n005/n006
  のWINは引き続きscrutiny owner (C++第二実装 gate pin `9193f5b6...` 前例)
  待ち。標準11x11空盤・19 central-reply roots・class 8106 (n009-n052未着手)
  は本解析のどの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。
- 並走との不接触: batch 14 (Part AF, class 23101) のprobe中ファイル・
  publishedファイルには一切接触しない (読み取りのみ)。宣言直前に最新mainを
  再取得し、同scope対抗宣言なし・`n005n006-ifadopted` dir不在・Part AH採番
  未使用を確認済み。同一スコープの宣言がmainに存在する場合は本宣言を破棄
  して着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part AH publication status update (2026-11-22)

Part AH (batch-12 class 8106 n005/n006 if-adopted decomposition) is
**completed and published**. Verdicts are NOT consumed anywhere; the
n005/n006 WINs remain unconsumed closure WINs pending the scrutiny owner
(scratch third-implementation verdict-level cross-verification had already
been recorded, Part AD). The standard 11x11 empty board, the 19
central-reply roots, class 8106 (canonical 52-row universe untouched) and
every other class remain UNKNOWN. Node counts are not verdicts.

Published (all fetch-back verified byte-identical against this host):

* Base control `research/experiments/n11-class8106-n005n006-base-control-20261122/`
  (README, pinned script `88671526...`, 3 outputs, run1/run2 logs, commit
  `9fd7dee5`): Part Y refresh script executed twice on this host, runs
  byte-identical (2/2, run logs sha `9816dfb7...` both), and
  closure-classes `61943b85...` / per-root-coverage `33f01a0c...` /
  refresh-summary `25987add...` are byte-equal to the published Part Y
  canonical re-audit outputs (cross-host reproduction; also byte-equal to
  the batch-11 z003 base control outputs). probe-worklist `1807e4d2...`
  (65,154 rows) recorded, not republished.
* Decomposition `research/experiments/n11-centralreply-class8106-win-n005n006-ifadopted-20261122/`
  (commits `9fd7dee5` scaffold+base, `7ca0c3af` increments+merges,
  `bc97ef35` pwin2, `c2fe5514` ploss6, `3e6c0f89` pfull8+deltas; 38 files
  fetch-back 38/38 byte-identical):
  - increments (3-way fail-closed (p1/p2/status) - batch-12 ran entirely
    on the declaring host, so no 4-way cross-host exists by construction):
    full 8 rows `d1954280...`, win-only 2 rows (n005/n006)
    `dd5fc998...`, loss-only 6 rows `d18ddaf8...`; deterministic 2/2;
    key/legal machine-cross-checked against published batch-keys
    `de55df83...` (52 keys).
  - scenario caches (fail-closed published union merger, selftest PASS,
    WIN/LOSS conflicts 0, duplicates 0): PWIN2 6,029 rows WIN 160 /
    LOSS 5,869 `c13f81d7...`; PLOSS6 6,033 rows WIN 158 / LOSS 5,875
    `898ca5f4...`; PFULL8 6,035 rows WIN 160 / LOSS 5,875 `21bbef33...`.
  - scenario refresh runs: 2 per scenario, all byte-identical (determinism
    6/6); scenario scripts diff-verified 4-hunk copies of the Part Y script.
  - deltas gated by `compare_deltas_batch12.py` -> `decomp-deltas-batch12.json`
    `a4152995...`; the compare script faithfully re-executes the refresh
    class-status semantics (graph + update8 + scenario cache, Board
    fail-closed free verification) and asserts all recomputed
    class_status_counts equal the published summaries for BASE + all 3
    scenarios before emitting any delta. All gates PASS.

Machine-verified decomposition results (deltas vs the Part Y canonical
re-audit; full detail in the experiment README and decomp JSON):

* **excluded_now flips: PWIN2 = PFULL8 = exactly {5007, 5011, 6147, 6166,
  8106}** (23 -> 28), PLOSS6 empty. The 5 flips are the UNION of the two
  WIN holder triples (n005: {5007, 5011, 8106}, n006: {6147, 6166, 8106};
  membership_class_count 3 each; overlap = class 8106 itself; union 5,
  machine-gated three ways: graph holders, membership counts, and the
  flip sets). This is the closure grind's first multi-WIN increment and
  the flip set is union-shaped (3+3 with overlap 1), not additive.
* class 8106 unknown_now: 52 -> 50 (PWIN2) / 46 (PLOSS6) / 44 (PFULL8);
  additivity machine-gated.
* update8: **all 8 probed batch-12 rows are update8 baseline requirements**
  (unlike batch-11 where only z003/z004 were): newly-resolved PWIN2
  {188395, 219608}, PLOSS6 {48210, 75387, 110810, 161205, 232022, 237227},
  PFULL8 all 8 resolved counts 2/6/8 exact. Remaining_now delta
  sub-additive by exactly 6 (-52 / -6 / -52): the class-8106
  excluded_now flip drops the whole 52-member remaining set, subsuming
  the 6 LOSS resolutions.
* win-hit groups: PWIN2 = PFULL8 = 4 groups, all served by class 8106
  (reply 60): first=14 (seconds 58/102) and first=38 (seconds 34/42),
  unknown_s5_children 52 each. Contrast batch-11 z003: 5 groups via peer
  5748 which did NOT self-exclude; here the win-hit holder is the batch
  class itself and doubles as an excluded_now flip.
* joint greedy is additive this time (+52 / 0 / +52 - contrast Part AB's
  +797 cascade), but the per-root individual_greedy_union column is
  NON-additive at root 14 (central first=14: +1 / +7 / +5,
  win+loss=8 != 5); roots 38 (-2/-6/-8) and 49 (-2/0/-2) additive.
  group_best_options_nonfree 2,127 in all four runs. Per-root free
  coverage (free_now/uncovered) identical to base in every scenario;
  root first=27 keeps 119/119 free thirds in all scenarios.
* worklist_total additive: -4 / -7 / -11 (65,154 -> 65,143 under the full
  what-if). Scenario probe-worklists recorded by sha only (PWIN2
  `aea35363...`, PLOSS6 `f9687992...`, PFULL8 `fbf65fe3...`), not
  republished.

Open items for future declarations (unchanged by this update): batch-13
if-adopted decomposition (4 probed rows; the batch-12 item is now CLOSED
by Part AH); batch 14 (Part AF) continues under its own owner. Kit mirror
saved under `batch8106-n005n006-ifadopted/` (plus base-control mirror).
Observed HEAD-before-push for this update is recorded in the commit
message.

## Part AI (read-only analysis, declaration 2026-11-22): batch 13 (class 16930) p002/p003 if-adopted 分解 (verdict不消費・実行前に宣言)

Part ADがopen itemとして掲げ、Part AH status updateで残唯一とした
「batch-13 4 probed行のif-adopted分解」を単一オーナーとして宣言する
（Part V/R/AB/AH流・solver探索なし・verdict不消費・新規主張ゼロの
what-if計画・監査計算）。

- 対象:
  (a) **BASEの再利用（再出版なし）**: 直前に出版した
      `research/experiments/n11-class8106-n005n006-base-control-20261122/`
      の3出力をBASEとして使う。それらはpublished Part Y canonical
      (`61943b85...`/`33f01a0c...`/`25987add...`) とbyte一致が機械検証済み
      であり、batch-13 deltaの基準として同一の正本である。同一bytesの
      3つ目の複製dirは情報を追加しないため出版しない（Part AB/AHの
      base control dirとpure bytes同一・宣言内で機械照合する）。
  (b) 新規実験dir
      `research/experiments/n11-centralreply-class16930-win-p002p003-ifadopted-20261122/`
      - increments: batch-13 published raws 8件 (p001-p004 x p1/p2)・
        status.log（4 PASS行・WIN-HALT x2 p002/p003）・batch-keys
        (sha `c6c56a1a...`, 52キー) からfail-closed生成。**3-way
        (p1/p2/status) 検証**（batch-13は宣言hostのみ実行でtakeover
        passが存在しない、Part AE正本）。3種: full 4行
        (p001/p004 LOSS + p002/p003 WIN)・win-only 2行 (p002/p003)・
        loss-only 2行 (p001/p004)。**2番目の複数WIN increment**。
      - scenario caches: canonical 6,027行 + increment をpublished union
        merger (fail-closed・WIN/LOSS衝突0・重複0・selftest) でmergeした
        分析用cache 3種 (pwin2/ploss2/pfull4、正本ではない)。
      - scenario refresh: scenario cache向けadapt script
        (docstring・ROOT行・CACHE行・sha pin行のみ変更・diff検証) を
        各2回実行しrun間byte一致。per-root free coverage (free_now/
        uncovered) が全rootでBASEと同一であること、root first=27が
        119/119 free thirdsであることをmachine gateで確認。
      - delta抽出: `compare_deltas_batch13.py` (Part AB/AH版をadapt) が
        excluded_now flip集合（frozen graphのp002/p003 cost-child holder
        のunion・membership_class_count 2/4との一致）・update8
        newly-resolved indices（increment行にgate）・加法性指標・
        per-root greedy表・win-hit groups群を機械算出し、全
        class_status_countをBASE+3シナリオで再実行しpublished summaryと
        一致をassertしてからdelta報告（Board fail-closed free検証込み）。
      - 前提知識（宣言時点のfrozen graph由来・計算で再検証する）:
        p002 holder {4903, 16930} (mclass 2)・p003 holder
        {5471, 5513, 5626, 16930} (mclass 4)・overlap = class 16930のみ・
        union 5クラス全status baseline UNKNOWN。
- 主張と消費規則: 本分解はread-only what-if解析・verdict不消費。p002/p003
  のWINは引き続きscrutiny owner (C++第二実装 gate pin `9193f5b6...` 前例)
  待ち（第三実装verdict-level検証はPart AG済み）。標準11x11空盤・19
  central-reply roots・class 16930 (p005-p052未着手) は本解析のどの時点でも
  UNKNOWNのまま。nodes数を勝敗として読まない。
- 並走との不接触: batch 14 (Part AF, class 23101) のprobe中ファイル・
  publishedファイルには一切接触しない (読み取りのみ)。宣言直前に最新mainを
  再取得し、同scope対抗宣言なし・`p002p003-ifadopted` dir不在・Part AI採番
  未使用を確認済み。同一スコープの宣言がmainに存在する場合は本宣言を破棄
  して着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。

## Part AJ (read-only analysis, declaration 2026-11-22): joint unconsumed-rows if-adopted 分解 (batches 1,3,4,5,6,8,9,11,12; verdict不消費・実行前に宣言)

Part AI (batch-13 単独分解) が進行中の間、そのスコープを侵さない規模の補完として、
**9つのWIN-HALTバッチの未消費probed行全体** (batch 13/14を除く) を一括する
joint if-adopted分解を単一オーナーとして宣言する (Part H joint-4WIN / Part J
joint-5WINの直接継承。それらが被覆できなかったWIN j033/h045/z003/n005/n006 を
初めてjointに含める)。solver探索なし・verdict不消費・新規主張ゼロの
what-if計画・監査計算。

- 対象:
  (a) **BASEの再利用（再出版なし）**: published base control
      `research/experiments/n11-class8106-n005n006-base-control-20261122/`
      の3出力 (sha `61943b85...`/`33f01a0c...`/`25987add...` = Part Y canonical)
      をBASEとして使う。本host取得後にsha機械照合する。
  (b) 新規実験dir
      `research/experiments/n11-centralreply-joint-unconsumed-ifadopted-20261122/`
      - increments: 9バッチのpublished raws・status.log・batch-keys から
        fail-closed生成 (`make_increments_joint10.py`):
        **JWIN10** (10 WIN行: b018/d002/e002/f017/g018/j033/h045/z003/n005/n006)・
        **JLOSS141** (141 LOSS行)・**JALL151** (全151 resolved行)。
        batch-11 z-keyはtakeover pass込み**4-way**、他バッチは**3-way
        (p1/p2/status)** node-exact gate。**h002 (batch-8, 15M budget枯損
        result 0) は全incrementから除外し、枯損形状 (result 0, nodes
        15,000,000, 2-pass一致) をgate検証**。151キーは互いにdistinct・
        canonical BASE 6,027行cacheに不在 (0 hits)・quarantine不在・
        batch-keysのlegal/(lo,hi)一致を機械検証。
      - scenario caches: canonical 6,027行 + 各increment をpublished union
        merger (s5_union_merge.py pin `90711961...`・fail-closed・WIN/LOSS
        衝突0・重複0・selftest) でmergeした分析用cache 3種 (正本ではない)。
      - scenario refresh: Part Y refresh script (pin `88671526...`) を
        docstring・ROOT行・CACHE行・sha pin行のみ変更 (4-hunk・diff検証) した
        scenario scriptを各2回実行しrun間byte一致。per-root free coverage
        (free_now/uncovered) が全rootでBASEと同一であること・root first=27
        が119/119 free thirdsであることをmachine gateで確認。
      - delta抽出: `compare_deltas_joint10.py` (Part AB/AH版をadapt) が
        excluded_now flip集合 (10 WINのfrozen graph holder union・各
        batch-keys membership_class_countとの一致の機械特定)・update8
        newly-resolved indices (increment行にgate・期待10/141/151)・9バッチ
        classのunknown_now加法性指標・per-root greedy表・win-hit groups群を
        機械算出し、全class_status_countをBASE+3シナリオで再実行し
        published summaryと一致をassertしてからdelta報告 (Board
        fail-closed free検証込み)。
- 主張と消費規則: 本分解はread-only what-if解析・verdict不消費。10 WINの
  採用判断は引き続きscrutiny owner (C++第二実装 gate pin `9193f5b6...`) 待ち
  (第三実装verdict-level検証は全10 WINともPart G/H/K/O/P/T/W/AA/AD/AG済み)。
  9バッチclassの残りunprobed子 (batch universeからprobed行を除いた集合) は
  本解析のどの時点でもUNKNOWNのまま。標準11×11空盤・19 central-reply rootsも
  UNKNOWN不変。nodes数を勝敗として読まない。
- 並走との不接触: batch-13 (Part AI)・batch-14 (Part AF) のファイルには一切
  接触しない (読み取りのみ)。宣言直前に最新mainを再取得し、同scope対抗宣言なし・
  `joint-unconsumed-ifadopted` dir不在・Part AJ採番未使用を確認済み。
  同一スコープの宣言がmainに存在する場合は本宣言を破棄して着手しない。
- 本amendment observed HEAD-before-push: push時の最新mainをコミットメッセージに記録。

## Part AK (probe-batch owner, amendment 2026-11-22): batch 15 (class 5830, renewed rank 13) 宣言 (verdict不消費・実行前に宣言)

batch 14 (Part AF, class 23101) は並走 operator が実行中 (output には val-gate のみ)。
事前登録の選択規則で、renewed rank 1-12 は反証証拠持ち・WIN-HALT済み・実行中のいずれか
(16757: b018, 20421: d002, 30345: b018 cost child, 16371: e002, 12264: f017, 5473: g018,
2634: h045, 8785: z003, 1518: j033, 8106: n005/n006, 16930: p002/p003, 23101: batch-14 in flight)。
よって **renewed rank 13 class 5830** (mask `[4035788216077385728, 0]`, unknown 52,
groups 2: root 49 third 59 / root 49 third 61) をbatch 15として宣言する。

- 対象: `research/experiments/n11-centralreply-closure-class5830-batch15-20261122/`。
  keys 52件 r001-r052 (probe_order 590-641), Part Y worklist (65,154行, sha `1807e4d2...`) の
  `serving_class=5830` 行から機械抽出。batch-keys.json sha256
  `af3e4c46af0d84bcb248c350283b07e26b901f6e0d196038e24bd1292b133727`。
- worklist再導出: pinned refresh script (`refresh_19root_frontier.py`, sha256 `88671526...` from
  published reaudit8784 dir) を6 pinned inputs (dependency-graph.json.gz `54f9c364...` / merged
  cache 6,027行 `95e868d6...` / repaired-joint-plan-update8.json / independent.py `954d3a10...` /
  s5_evidence_policy.py / quarantine `81d23160...`) に対して本hostで3回実行し、run間byte一致・
  3出力 (closure-classes.csv `61943b85...` / per-root-coverage.csv `33f01a0c...` /
  refresh-summary.json `25987add...`)・probe-worklist.csv (`1807e4d2...`) がpublished Part Y
  canonicalとbyte一致 (published closure-classes.csv正本とのcmpも実施)。
- 宣言前fail-safe (全て本実行内に機械実施・全PASS): (1) canonical merged cache 6,027行
  (sha `95e868d6...`) に52/52不在・0 hits、(2) quarantine registry (sha `81d23160...`,
  active 2キー) 両方向0 hits、(3) 52キー重複なし、(4) closure-classes.csv rank 13行 = class
  5830 (`[4035788216077385728, 0]`, unknown 52, first_group 49/59, groups 2) published
  Part Y正本とbyte一致、(5) 12 WINキー
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003, 各published batch-keys.json
  から機械取得) の(lo,hi)交叉0 hits、(6) probe_order連続590-641・全行 class_unknown_now=52。
  membership_class_count分布 {1:7, 2:15, 3:30}。
- protocol (事前登録・batch 12-14と同一): pinned replica `jsreplay.js` (sha
  `84585617...`), 1キー2 fresh cold pass, budget 15,000,000, determinism mismatchで
  HARD-STOP (rc=42), WIN検出でWIN-HALT (rc=45, 同wave内in-flightは完了まで開示),
  最大4 worker (2-core host), resume-safe runner, honest negative (result 0 = UNKNOWN)。
- validation gate (実行前に本ホストでfresh再現・4/4 node-exact): at2m result 0/2,000,000 x2,
  15m result 2/3,651,923 / result 2/5,040,200 (forbidden quadruples 95,670 一致)。
- 主張と消費規則: 本batchはverdict不消費。WIN行はunconsumed closure WIN (採用判断は
  scrutiny owner, C++第二実装 gate pin `9193f5b6...` 前例・不変)。標準11x11空盤・19
  central-reply roots・class 5830 (および全class) は本batchのどの時点でもUNKNOWNのまま。
  nodesを勝敗として読まない。batch選択はscheduling quantityでありverdictではない。
- 並走との不接触: batch-13 (Part AI)・batch-14 (Part AF)・Part AJのpublished・進行中ファ
  イルには一切接触しない (読み取りのみ)。宣言直前に最新mainを再取得し (observed HEAD
  `5a7ec2a2` 時点でnote末尾はPart AJ宣言のまま)、同scope対抗宣言なし・`batch15` dir不在・
  Part AK採番未使用・note内にclass 5830スコープなしを確認済み。同一スコープの宣言がmain
  に存在する場合は本宣言を破棄して着手しない。
- 本amendment observed HEAD-before-push: push時の最新mainをコミットメッセージに記録。

## Part AK publication status update (2026-11-22, probe-batch owner)

batch 15 (class 5830) は第1wave (probe_order 590-593, r001-r004) で事前登録WIN-HALT規則が
同一wave内で2回発火し停止した (verdict不消費)。

- **r001 (probe_order 590, s5_index 103560, key `[4035788216211603456, 0]`,
  legal 82) result 1 WIN・2,521,302 nodes・2-pass fresh cold node-exact**
  (budget 15,000,000) - **13番目のunconsumed closure WIN**。バッチ先頭キーでの発火。
- **r002 (probe_order 591, s5_index 103561, key `[3603442651849818112, 128]`,
  legal 82) result 1 WIN・5,973,924 nodes・2-pass node-exact** - **14番目の
  unconsumed closure WIN**。3例目の同一wave複数WIN (batch-12 n005/n006・batch-13
  p002/p003に続く)。
- r003 (key `[4035788216077385729, 0]`, legal 97)・r004 (key
  `[1729945206863692800, 128]`, legal 100) はbudget枯損: result 0, nodes
  15,000,000, 2-pass一致。honest UNKNOWN・15M同条件再探索禁止。
- 出力: 実験dir `n11-centralreply-closure-class5830-batch15-20261122/` として
  wave-1 raws 8件 + status.log + README Result節を出版 (commits `d1316b19` /
  `a35fb210`・全fetch-back byte一致)。全4行はbatch-keys.json・worklist行
  (legal/lo/hi) と機械照合済み・p1/p2間 (result, nodes, budget) 一致 (rc=42
  不発火)。
- val-gate: 実行前に本ホストでfresh 4/4 node-exact (at2m 0/2,000,000 x2・
  15m 2/3,651,923 / 2/5,040,200・quads 95,670)。
- r005-r052 (48キー) はWIN-HALT規則により不着手。
- batch実績: 15バッチ → 12 WIN-HALT + 3 clean (23963/10324/8784 = 33/34/35番目の
  Board検証free class)。
- r001/r002の第三実装verdict-level交叉検証 (Part G/K/O/P/T/W/AA/AD/AG規約) と
  if-adopted分解 (Part V/R/AB/AH/AI流) は未着手・将来の別宣言待ち (着手前に
  最新mainで対抗宣言の有無を確認すること)。採用判断は引き続きscrutiny owner
  (C++第二実装 gate pin `9193f5b6...`) 待ち・不変。
- **標準11×11空盤・19 central-reply roots・class 5830 (48キー未着手) 他全classは
  どの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。**

## Part AJ publication status update (2026-11-22)

Part AJ (joint unconsumed-rows if-adopted decomposition of the nine
WIN-HALT batches 1,3,4,5,6,8,9,11,12) is **completed and published**
(commit `7704f5c3`, 26 files, fetch-back sha256-verified 26/26
byte-identical against the publishing host). Verdicts are NOT consumed
anywhere; the ten WINs (b018/d002/e002/f017/g018/j033/h045/z003/n005/
n006) remain unconsumed closure WINs pending the scrutiny owner (C++
second-implementation gate pin `9193f5b6...`; third-implementation
verdict-level cross-verification had already been recorded for all ten,
Parts G/H/K/O/P/T/W/AA/AD/AG). Batch-13 (Part AI), batch-14 (Part AF)
and batch-15 (Part AK) files were never touched (read-only). The
standard 11x11 empty board, the 19 central-reply roots, the unprobed
children of the nine batch classes and every other class remain UNKNOWN
at every point of this decomposition. Nodes are not verdicts.

**Honest correction published by the maker's own fail-closed gate**: the
first increment run ABORTed (`ABORT b001: key already in canonical BASE
cache`). Precise re-measurement of every batch key against the 6,027-row
canonical BASE cache found that exactly **19 batch-1 LOSS rows
(b001..b017, b019, b020) are already inside canonical BASE with
identical verdicts AND identical node counts** (the canonical batch-2/7/10
increments already reached those membership classes); batch-1's WIN b018
is NOT in BASE; the other eight batches have ZERO BASE overlap; no
verdict conflicts exist anywhere. Those 19 rows are excluded from every
increment as pre-consumed duplicates under a stricter gate (verdict AND
node identity, else ABORT). The packet shrank from the declared 151
probed rows (JLOSS141/JALL151 planning labels) to **132 unique-new rows
= 10 WIN + 122 LOSS**; the declaration numbers were planning quantities,
not outcomes. h002 (batch-8 15M exhaustion, result 0) stays excluded
from all increments with its exhaustion shape gate-checked (15M nodes,
2-pass identical); its forbidden re-search is unchanged.

Published contents (`research/experiments/n11-centralreply-joint-unconsumed-ifadopted-20261122/`,
26 files; the three 3.7MB probe-worklists are regenerable from the
published scripts and are not republished, Part AH precedent):

* Corrected maker `scripts/make_increments_joint10.py` (all gates PASS)
  and new `scripts/compare_deltas_joint10.py`; increments
  `output/increment-joint-wins10-IFADOPTED-20261122.cache` `fe2c6f68...` /
  loss122 `e5fe80af...` / all132 `cc841d6e...`, with manifest.
* Scenario caches via the published fail-closed union merger
  (`s5_union_merge.py` pin `90711961...`, selftest PASS, WIN/LOSS
  conflicts 0, duplicates 0): JWIN10 6,037 rows `7881724a...`,
  JLOSS122 6,149 rows `d80ee94b...`, JALL132 6,159 rows `13bfec6e...`,
  each with a merge audit.
* Scenario refresh: Part Y script (pin `88671526...`) adapted in exactly
  4 hunks per scenario (docstring/ROOT/CACHE/sha-pin, diff-verified),
  executed twice each, 6/6 byte-identical runs; per-root free coverage
  (free_now/uncovered) identical to BASE on every root; root first=27
  keeps 119/119 free thirds in every scenario.
* Deltas `output/decomp-deltas-joint10.json` (`24b5aa11...`; all
  recomputed class_status_counts asserted equal to the published
  BASE+scenario summaries before reporting; Board fail-closed free
  verification re-executed per scenario):
  - **JWIN10**: excluded_now 23 -> 53 (+30 flips), unknown 34,501 ->
    34,471. The flip set is machine-measured IDENTICAL to the frozen-graph
    valid holder union of the ten WIN S5 children (30 classes, all
    baseline UNKNOWN, none already excluded_now): each WIN flips its own
    batch class plus its peer cost-child holders; only class 8106 is a
    multi-WIN holder (n005+n006). update8 win_hit_groups 0 -> 29;
    free_now stays 35; root27 stays 119/119.
  - **JLOSS122**: ZERO flips (excluded_now 23, free_now 35, unknown
    34,501, root27 119/119); update8 resolved 75 -> 163 (+88 of the 122
    rows are frozen-baseline requirements), remaining 31,784 -> 31,696;
    joint greedy 35,242 -> 36,201; probe worklist 65,154 -> 65,011.
  - **JALL132**: excluded_now 53 / unknown 34,471 (identical to JWIN10:
    the LOSS rows flip nothing); update8 resolved 75 -> 171 (+96),
    remaining 31,784 -> 31,442; joint greedy 35,242 -> 36,193; worklist
    65,154 -> 64,996. Per-class unknown_now additivity of all nine batch
    classes: True; update8 remaining/joint greedy are honestly
    NONadditive (WIN hits drop whole planned groups while LOSS rows
    resolve single requirements); greedy nonadditive roots (0, 14, 49)
    recorded in the delta JSON, not gated away.

Scheduling reading only (not a verdict): adopting the 122 published
LOSS rows would shrink the frozen update8 requirement by 88 rows and the
worklist by 143 with zero status flips; the ten WINs are worth 30
excluded classes but remain hypothetical. The 11x11 empty board remains
UNKNOWN.

## Part AL (verifier, declaration 2026-11-22): batch 15 (class 5830) r001/r002 第三実装交叉検証 (verdict不消費・実行前に宣言)

batch 15 (Part AK, class 5830, renewed rank 13) は第1wave で事前登録WIN-HALT規則が
同一wave内で2回発火した (r001: s5_index 103560, key `[4035788216211603456, 0]`,
legal 82, result 1 WIN, 2,521,302 nodes / r002: s5_index 103561, key
`[3603442651849818112, 128]`, legal 82, result 1 WIN, 5,973,924 nodes。いずれも
2-pass fresh cold node-exact)。Part G/K/O/P/T/W/AA/AD/AG規約に従い、13番目・
14番目のunconsumed closure WIN r001/r002 を**第三実装** (非df-pn AND/ORミニ
マックス `third_impl.js`, pin sha256 `08ea958f...`) でverdict-level交叉検証する。
**verdict不消費・採用判断は引き続きscrutiny owner (C++第二実装 gate pin
`9193f5b6...`)。**

- 対象: `research/experiments/n11-centralreply-closure-batch15-wins-thirdimpl-20261122/`。
  targets = batch-15のprobed行のうちverdictを有する行 全部 = **r001/r002 の2 WIN行**
  (期待値はpublished replicaどおり WIN 1)。r003/r004 はbudget枯損 (result 0,
  15,000,000, 2-pass) でverdictを持たないため交叉検証の対象外 (honest UNKNOWNの
  まま。第三実装での再探索はbudget昇格に相当し別宣言が必要なため本実験では
  実行しない)。
  - anchors (published第三実装値を本ホストで再現): k02a (WIN, legal 87, 9,106,337
    expansions / 4,991,527 ttHits)・l1a (LOSS, legal 116, 7,660,602 / 3,951,175)。
  - negatives (GATE_FAIL必須): ng1 (k02 legal+1)・ng2 (k02 stones 6)。
  - 入力はpublished batch-15 raws (commit `d1316b19`)・batch-keys.json (sha256
    `af3e4c46...`)・status.log・published input CSV (scaffold `b04969bc`) から
    `scripts/make_inputs_batch15.py` (Part AG版をadapt) で機械導出
    (fail-closed・手転写ゼロ・source raw 2-pass node-exact・status PASS行照合・
    derived-vs-published CSV byte一致)。
- 前提ゲート (fail-closed): script pin 3種 (third_impl `08ea958f...` / verify_tbl
  `c8c52528...` / jsreplay `84585617...`)・rule-engine gate (quads 95,670 ==
  replica・TBL==wob mismatches 0)・anchor本ホスト再現がpublished値と完全一致・
  negatives文言一致GATE_FAIL。
- 手法: 1行1プロセス、cap 300M expansions、wallcap 240s、`--memo-power=22`、
  1行2回 (a/b) determinism gate (result/expansion/ttHits/reason同一必須)。
  wall超過 (runlimit) はhonest wall-inconclusive・検証主張としない。cleanな
  verdict一致のみ文献として記録。cleanな不一致はdivergence evidenceとして
  記録するがverdictは書き換えない。audit.py (schema
  `batch15-wins-thirdimpl-audit-v1`) を2回実行しbyte一致必須。
- 主張と消費規則: 本実験はverdict不消費。r001/r002のWINはunconsumed closure WIN
  のまま (採用判断はscrutinity owner待ち・不変)。標準11x11空盤・19 central-reply
  roots・class 5830 (48キー未着手) はどの時点でもUNKNOWNのまま。nodes/expansionsを
  勝敗として読まない。
- 並走との不接触: batch-13 (Part AI)・batch-14 (Part AF)・Part AJのファイルには
  一切接触しない (読み取りのみ)。宣言直前に最新mainを再取得し (observed HEAD
  `cf485460`・note blob `65e74c00...` 171,198 bytes・記録時点でPart AJ status updateが末尾)、同scope対抗宣言なし・
  `batch15-wins-thirdimpl` dir不在・Part AL採番未使用を確認済み。同一スコープの
  宣言がmainに存在する場合は本宣言を破棄して着手しない。
- 本宣言 observed HEAD-before-push: `cf485460` (2026-11-22T14:47:40Z)。push直前にnote blob再照合し競合時は破棄。


## Part AL publication status update (2026-11-22, verifier owner)

Part AL (batch-15 class 5830 r001/r002 第三実装交叉検証) は**完走・出版済み**
(実験dir `n11-centralreply-closure-batch15-wins-thirdimpl-20261122/` 29ファイル、
commit `ca7ad4fc`、fetch-back 29/29 byte一致・MANIFEST-sha256.txt同梱)。
**verdict不消費**のまま。R003/R004の15M枯損行は再探索しておらず (honest UNKNOWN
のまま・禁止は不変)、r005-r052 (48キー) は未着手のまま。

- 前提ゲート: verify_tbl.js quads 95,670 == replica・ランダム195,044トリプル
  0 mismatch・script 3pin一致 (third_impl `08ea958f...` / verify_tbl
  `c8c52528...` / jsreplay `84585617...`)。
- negatives: ng1 (legal 88 vs derived 87)・ng2 (stones 6 vs bits 5) とも文言
  一致のGATE_FAIL (fail-closed動作)。
- anchors: k02a a/b = WIN, 9,106,337 expansions / 4,991,527 ttHits, clean・
  l1a a/b = LOSS, 7,660,602 / 3,951,175, clean - **いずれもpublished第三実装
  値と完全一致、a/b決定性一致**。
- targets (1行2回 a/b determinism・cap 300M・wallcap 240s・memo-power 22):
  - **r001 `[4035788216211603456, 0]` (legal 82): 第三実装 result 1 WIN・
    2,856,756 expansions・1,684,754 ttHits・clean・a/b同一 (wall 17.34/17.47s)
    → replica verdict (WIN, 2,521,302 nodes @15M) とverdict一致**
  - **r002 `[3603442651849818112, 128]` (legal 82): 第三実装 result 1 WIN・
    6,817,094 expansions・4,153,893 ttHits・clean・a/b同一 (wall 42.37/42.85s)
    → replica verdict (WIN, 5,973,924 nodes @15M) とverdict一致**
  - wall-inconclusive 0件・divergence 0件。13番目・14番目のunconsumed
    closure WINは第三実装verdict-level補強を得た (採用判断は引き続き
    scrutiny ownerのC++第二実装ゲート `9193f5b6...` 待ち・不変)。
- audit: schema `batch15-wins-thirdimpl-audit-v1`、**51/51 gates PASS**・
  2回実行でbyte一致 (audit-summary.json sha256 `c008d74b...`)。
- 誠実記録: runnerの直列`&&`ペアがng1の意図的rc=1で短絡したため、ng2は
  runner直後に同一pinned `run_thirdimpl.sh` 起動で実行した (status.logの
  PARTAL-RUNNER-EXIT後に行が存在・READMEに明記)。
- 標準11×11空盤・19 central-reply roots・class 5830他全classはどの時点でも
  **UNKNOWNのまま**。nodes/expansionsを勝敗として読まない。


## Part AM (solver, declaration 2026-11-22): closure class 10687 exact-S5 probe batch 16 (verdict不消費・実行前に宣言)

batch 15 (Part AK, class 5830) がwave-1でWIN-HALT ×2 (r001/r002) で停止し、r001/r002の
第三実装交叉検証 (Part AL) も51/51 gatesで完了した。Part AF (batch 14, class 23101)
は依然in flight (scaffold + val-gateのみ出版・rawsなし)。renewed closure ranks
1-13はすべて反駁証拠保持・WIN-HALT済み・またはin flight (16757: b018, 20421: d002,
30345: cost child, 16371: e002, 12264: f017, 5473: g018, 2634: h045, 8785: z003,
1518: j033, 8106: n005/n006, 16930: p002/p003, 23101: batch-14 in flight, 5830:
r001/r002) のため、事前登録選択規則 (反駁証拠なし・不在・未着手の最初のclean候補)
により**renewed rank 14 class 10687** (mask `[1224979098661617664, 0]`,
unknown 52, groups served 2 = (root first=16, third=56)と(first=16, third=64)、
still-unknown 52子はすべて(16,56)由来) に着手する。

- 対象: `research/experiments/n11-centralreply-closure-class10687-batch16-20261122/`。
  未確定canonical S5子52件 (t001-t052、renewed re-audit正本probe-worklistの
  probe_order 642-693連続・Board再計算の合法手数固定 76-95)。
  batch-keys.json (schema `n11-centralreply-closure-class10687-batch-input-v1`,
  sha256 `465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e`)は
  pinned正本probe-worklist (sha256 `1807e4d2...`)から機械抽出。Part Y抽出
  (refresh_19root_frontier_extract.py・6 pinned入力sha検証) を本ホストで再実行し
  closure-classes `61943b85...`・per-root-coverage `33f01a0c...`・
  probe-worklist `1807e4d2...`・refresh-summary `25987add...` がpublished
  canonical 4ファイルとcmp byte一致することを確認済み (published再現は3度目
  に続き4度目・全てbyte一致)。served-groups-10687.json (groups (16,56)+(16,64))
  を実験dirに同梱する。
- 前提fail-safe (全て機械確認済み・fail-closed): (1) 全52キーは正本merged cache
  (6,027行・sha256 `95e868d6...`) に(lo,hi)対で0 hit・(2) quarantine registry
  (sha256 `81d23160...`) に0 hit・(3) バッチ内重複なし (52 key_id・52 (lo,hi)対)・
  (4) closure-classes.csv rank-14行 `14,10687,1224979098661617664,0,52,16,56,2`
  byte一致・(5) 過去バッチ鍵集合 (batch 1-15既出版608キー) と(lo,hi)対overlap 0・
  (6) probe_order 642-693連続。
- 方法・停止規則・消費規則: Part B/C/D/E/Fと同一 (pinned replica `jsreplay.js`
  sha256 `84585617...`, 2-pass fresh cold, budget 15M, mismatch→HARD-STOP rc=42,
  WIN→HALT rc=45, 枯損=result 0 honest UNKNOWN・15M同条件再探索禁止, worker最大2,
  4キーwave・resume-safe)。実行前に本ホストでfresh val-gate 4/4 node-exact
  (at2m 0/2,000,000 ×2・15m 2/3,651,923と2/5,040,200・quads 95,670) を
  再現済み (本セッション内 2026-11-22T15:07Z前に実施)。消費はfail-closed merger経由
  のみ・本batch単体ではroot被覆・クラス閉鎖・第三手securedの主張をしない
  (閉鎖判定・被覆監査は後続のrefresh再実行+独立監査が行う)。
- 並走との不接触: 本バッチはclass 10687固有の52キーで、他レーン・他バッチ
  (Part AF/AI/AJ/AK/ALファイル) には読み取り以外接触しない。宣言直前に最新main
  を再取得し (observed HEAD `1976f566`・note末尾はPart AL status update)、
  「Part AM」「batch 16」「class 10687」対抗宣言なし・`class10687-batch16` dir不在
  を確認済み。同一スコープの宣言がmainに存在する場合は本宣言を破棄して着手しない。
- 本宣言 observed HEAD-before-push: push時の最新main HEADをコミットメッセージに
  記録し、push直前にnote blob sha再照合 (現状 `b86f2373...`)。競合時は破棄。
  標準11×11空盤・19 central-reply roots・class 10687はどの時点でもUNKNOWNのまま。
  nodes数を勝敗として読まない。


## Part AI status update (amendment 2026-11-22): if-adopted分解をtakeoverで実行・出版した (verdict不消費)

宣言ホスト (Part AI, note修正コミット `a0cdb0da`, 2026-11-22T13:08Z) は宣言後2時間以上
沈黙した (status updateなし・実験dirなし・kit成果物なし; 柾HEAD `858a4158` 15:18Zと
`ada9bc95` 15:25Zの両時点で実験dir不在を確認)。Part U (batch-8) / Part Z (batch-11) と
同一のtakeover基準 (20分超の沈黙かつ成果出版なし) により、本セッションのホストが
published宣言を変更なしで実行した。対抗宣言・競合なし。verdictは一切不消費。

- 再取得・全ゲートPASS: published batch-13正本10/10 byte一致 (8 raws + status.log +
  batch-keys `c6c56a1a...`, AT `858a4158`)、BASE control refresh 2回実行でpublished
  Part Y canonical 4出力とbyte一致 (5度目のcross-host再現)、increments maker 2回実行
  byte一致 (wins2 `bb238f67...` / loss2 `50c09a06...` / full4 `3a8bcb11...`,
  ゲート: 3-way p1/p2/status一致・BASE重複0・quarantine 0・WIN集合=={p002,p003})、
  sha-pinned union mergerで衝突0・重複0 (6,029/6,029/6,031行, `c180e6d6...` /
  `ac7b6cdd...` / `faacb374...`)、scenario refresh 6/6 byte一致 (直列実行。
  最初の並列起動はOOM-killされ誠実記録、部分出力の流出なし)、delta extractor 2回実行
  byte一致 (`c62cabb4...`, 再計算ゲート: class_status_countsをgraph+update8+cacheから
  再計算しBASE・全シナリオのpublished summaryと一致)。
- 機械測定された分解結果 (decomp-deltas-batch13.json) : **PWIN2** のexcluded_nowは
  23→28、flip集合 == frozen-graph eligible holder union **{4903, 5471, 5513, 5626, 16930}**
  (p002 s5 185003 holders {4903,16930}・p003 s5 203419 holders {5471,5513,5626,16930} (membership 4)・overlapは16930のみ。multi-WIN holderは16930のみ)。unknown 34,501→34,496。
  class 16930のclosure-classes rankは11→5 (unknown 52→50)。**PLOSS2** はflip 0
  (excluded_now 23・free_now 35・unknown 34,501不変)、probe worklist 65,154→65,152。
  **PFULL4** はworklist 65,150 (−4, 加法的)・class 16930 unknown 48。**update8は全シナリオ
  不変** (resolved 75, remaining 31,784, win_hit_groups 0; batch-13はupdate8-neutral)。
  free_now 35とper-root free coverageは全root不変、root 27は119/119。joint greedy
  35,242不変、per-root greedyはroot 26/48が-2/-2/-4加法的。PWIN2とPLOSS2の
  closure-classes.csvが同一bytesなのは構造的理由 (両方2子解消でrank/unknown同値)。
- 出版: 実験dir `research/experiments/n11-centralreply-class16930-win-p002p003-ifadopted-20261122/`
  28ファイル (27 + MANIFEST-sha256.txt) を1コミット `79a7f72d` (2026-11-22T15:34:45Z) で
  mainに反映、fetch-back 28/28 byte一致 (247KB cache 3本を含む)。scenario probe-worklist
  (3.7MB×3) はPart AH/AJ先例どおり不出版 (sha256はREADMEに記録)。
- verdict不消費・解釈ガート不変: p002/p003の採用判断はscrutiny ownerのC++第二実装
  ゲート pin `9193f5b6...` 待ちのまま、p001/p004 LOSS行もcanonical cache外のunconsumed
  evidence。p005-p052 (48キー) は未着手。標準11×11空盤・19 central-reply roots・
  class 16930他全classはどの時点でも**UNKNOWNのまま**。nodes数を勝敗として読まない。
- 本status updateのobserved HEAD-before-push: `e0f26f11` (note blob sha1ロック
  `ac8090f6...` で更新、fetch-backで追記確認)。


## Part AN (read-only analysis, declaration 2026-11-22): closure class 5830 batch-15 r001/r002 IF-ADOPTED分解 (verdict不消費)

batch 15 (Part AK, class 5830) はwave-1でWIN-HALT規則が2回発火して停止した
(r001/r002: 2-pass node-exact result 1, 2,521,302 / 5,973,924 nodes・いずれもlegal 82;
r003/r004は15M budget枯損 = honest UNKNOWN, result 0, nodes==budget)。第三実装verdict-level
交叉検証 (Part AL, 51/51 gates) 出版済み。Part V/R/AB/AH/AI と同一のif-adopted分解を
r001/r002の2 WIN行に読み取り専用で適用する。

- 対象: `research/experiments/n11-centralreply-class5830-win-r001r002-ifadopted-20261122/`。
- 入力はpublished正本のみ: batch-15正本 (8 raws + status.log + batch-keys 52キー) を
  本ホストでmain再取得により10/10 byte再検証済み (実験dir一覧に5830系はbatch-15正本のみ、
  対抗宣言・if-adopted先行dirなしを確認)。BASE = Part AH base control canonical
  (merged cache 6,027行・sha256 `95e868d6...`)。r003/r004枯損行 (result 0) はverdictでは
  ないため型ゲートで除外し、増分はWINのみ2行。PLOSS2/PFULL4相当のシナリオは存在しない
  (解決LOSS行ゼロ; 「全probed行採用」== WIN 2行であることを機械表明する)。
- 方法: Part AI 機材流用 (increments maker adapter、sha-pinned s5_union_merge
  `90711961...` (selftest PASS)、pinned Part Y refresh script の4-hunk adapt
  (docstring/ROOT/CACHE path/CACHE_SHA_EXPECTEDのみ) を2回実行してbyte一致必須、
  delta extractor はclass_status_counts を graph+update8+cache から再計算し
  BASEとシナリオのpublished summary と一致するまでfail-closed)。solver探索なし・
  新規verdictゼロ・canonical cache不変更。
- verdict不消費: r001/r002の採用判断はscrutiny ownerのC++第二実装ゲート pin
  `9193f5b6...` 待ちのまま。r005-r052 (48キー) は不着手。標準11×11空盤・
  19 central-reply roots・class 5830他全classはどの時点でもUNKNOWNのまま。
  nodes数を勝敗として読まない。
- 本宣言 observed HEAD-before-push: push時の最新main HEADをコミットメッセージに記録し、
  push直前にnote blob sha再照合する。競合時は破棄。

### Part AN status update (2026-11-22, declaring host = 本レーンセッション)

宣言どおり完了。実験は単一シナリオ (PWIN2のみ; r003/r004枯損行は型ゲート除外、
「全resolved行採用 == WIN 2行」をmanifestで機械表明) として実行した。

- 出版: 実験dir `research/experiments/n11-centralreply-class5830-win-r001r002-ifadopted-20261122/`
  14ファイル (README + MANIFEST-sha256.txt含む) を1コミット `c37b2790`
  (2026-11-22T15:49:30Z) でmainに反映、fetch-back 14/14 byte一致 (~247KBの
  scenario cache含む)。probe-worklist (3.7MB) はPart AH/AJ先例どおり不出版
  (sha256 `951b8897...` はREADMEに記録)。
- 全ゲートPASS: increments maker 2回byte一致 (2行WIN増分 sha256 `05c10e1f...`);
  sha-pinned s5_union_merge (`90711961...`, selftest PASS) 2回byte一致
  (6,029行・WIN160/LOSS5,869, sha256 `51693301...`); scenario refresh 2回
  直列実行 (66s/61s, batch-13の並列OOM再発防止)・3出力ともbyte一致
  (`496f3761...`/`37223c04...`/`f4256c28...`); delta extractor 3回byte一致
  (`e67df758...`)・BASE/PWIN2両方のclass_status_countsをgraph+update8+cache
  から再計算しpublished summaryと一致させた (fail-closed)。
- 機械測定された分解結果: excluded_nowの翻りは**side class 2634のみ**
  (class 5830はBASEで既にexcluded_now, 57子中5 WIN既存)。flips={2634}は
  eligible holder unionと機械同一。excluded_now 23→24, unknown 34,501→34,500,
  free_now 35不変。class 5830 unknown_now 52→50, class 2634は51→49 (両クラスの
  own membership deltaとも2)。batch-keysのmembership_class_count=1はclosure-scoped
  計数であり、graph s4_cost holders {2634,5830}とはスコープが異なる (両方を
  delta出力に記録、flipはgraph側が支配)。
- update8は正方向に動く (batch-13がupdate8-neutralだったのと対照的): r001/r002
  (s5 103560/103561) はfrozen update8 baseline要件であり、resolved 75→77,
  remaining 31,784→31,734, win_hit_groups 0→1 (最初のwin-hit groupはs4 class 2634,
  root first 49/third 71のgroup)。
- スケジューリング: joint greedy 35,242→35,240, probe worklist 65,154→65,150,
  root 27 (known-loss baseline) は119/119, per-root free coverage列は全root不変,
  individual_greedy_unionの移動はroot (first 49) のみ 2,890→2,888。
- verdict不消費・解釈ガード不変: r001/r002の採用判断はscrutiny ownerのC++第二実装
  ゲート pin `9193f5b6...` 待ちのまま。r005-r052 (48キー) は不着手。r003/r004は
  honest UNKNOWN (result 0, nodes==budget) でありverdictとして読まない。標準11×11
  空盤・19 central-reply roots・class 5830他全classはどの時点でも**UNKNOWNのまま**。
  nodes数を勝敗として読まない。
- 本status updateのobserved HEAD-before-push: `b661405a` (note blob sha1ロック
  `088116b3...` で更新、fetch-backで追記確認)。


### Part AM status update (2026-11-22, declaring host = 本レーンセッション)

宣言 (commit `4386ace3`, observed HEAD-before-push `1976f566`) どおり完了。
batch 16 (class 10687, renewed closure rank 14, mask `[1224979098661617664, 0]`,
unknown 52, groups (16,56)+(16,64)) の52キーを2-pass fresh cold replay
(pinned `jsreplay.js` sha256 `84585617...`, budget 15M, probe_order 642-693)
で全件探索した。

- 結果: **52/52全LOSS (result 2)**。2-pass node-exact (全キーでp1/p2 nodes
  一致)・WIN 0・budget枯損 0・determinism mismatch 0。総ノード数/pass
  168,262,885。行単位機械照合 `output/row-audit.json` (schema
  `n11-centralreply-closure-class10687-batch16-rowaudit-v1`, 52行,
  all_loss_2pass_node_exact=true, sha256 `589c1141...`) でbatch-keys
  (key_id/lo/hi/legal/probe_order) と突合済み。`input/batch-keys.json`
  sha256 `465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e`。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-class10687-batch16-20261122/`
  180ファイル (input 53 = batch-keys + t001-t052 CSV、scripts 4、val-gate 8、
  raw 104 = 完全p1/p2ペア、raw-truncated-hostevent 8、status.log、
  row-audit.json、README.md、MANIFEST-sha256.txt) を3コミットでmainに反映
  (scaffold `14092b5e`、results `0aac7e0c`、README+audit+MANIFEST `d349e8f8`)。
  fetch-back 180/180 byte一致 (publication commit `d349e8f8` 全ファイル
  MANIFEST sha照合)。
- 誠実なhost event記録: 宣言後の実行中にhost環境のリセットが繰り返し背景
  runnerをkillした (truncated断片のタイムスタンプから15:15Z・15:27Z・15:32Zの
  3系統、加えて~15:31Zに`/home/user/work`一掃。status.logのHOST-EVENT行2行と
  WAVE-START/TRUNCATED-RETRY行で記録)。権威状態はknowledge kit checkpointが
  保持した。`runbatch.sh`に`# replay_done`完全性ガードを再実行前に導入し、
  最終7 waveは前景1-wave実行 (`scripts/runwave.sh`) で完走。truncated断片8件
  (いずれもverdict行なし) は`output/raw-truncated-hostevent/`にそのまま公開。
  本batchは枯損行0・resolved完了行の再探索ゼロであるため、truncated passの
  fresh-cold再実行は「同条件15M再探索禁止」の対象外であることをREADMEに明記。
- closure candidate (verdict不消費): 本batch単体ではroot被覆・クラス閉鎖・
  第三手securedを主張しない。52 LOSS行の消費はfail-closed union merger
  (pin `90711961...`) によるpublished increment + refresh再実行・独立監査に
  よってのみ成立し (batch 10/8784, 8784-reaudit先例) 、class 10687の閉鎖資格
  確定はその後。このincrement+reauditは別宣言 (Part AP相当) が必要で、着手前に
  ranks 1-13の最新状況 (batch-15 if-adoptedはPart AN `c37b2790` 出版済み・
  23101 batch-14 in flight) を再確認する。
- verdict不消費・解釈ガード不変: unconsumed closure WIN 14個の採用判断は
  scrutiny ownerのC++第二実装ゲート pin `9193f5b6...` 待ちのまま。標準
  11×11空盤・19 central-reply roots・class 10687他全classはどの時点でも
  **UNKNOWNのまま**。nodes数を勝敗として読まない。
- 本status updateのobserved HEAD-before-push: `c2178ac1` (note blob sha1
  ロック `f36db386...` で更新、fetch-backで追記確認)。


## Part AO (read-only what-if analysis, declaration 2026-11-22): batch-16 (class 10687) 52 LOSS行 IF-ADOPTED increment + scenario refresh分解 (verdict不消費)

batch 16 (Part AM) は52/52全LOSS (2-pass node-exact, 枯損0, WIN 0) で完走・
出版済み (3コミット `14092b5e`/`0aac7e0c`/`d349e8f8` + erratum `572dcbc3`、
fetch-back 180/180 byte一致、Part AM status update `7711aab9`)。
Part AH/AI/AN と同一の機材とfail-closed規約で、batch-16の52 LOSS行すべてを
what-if incrementとして採用する単一シナリオを計算する。

- 対象: `research/experiments/n11-centralreply-class10687-loss52-ifadopted-20261122/`。
- 対象シナリオ: **PLOSS52** = BASE (canonical 6,027行 `95e868d6…`) + batch-16
  52 LOSS行。WIN行ゼロ・枯損行ゼロのため「全probed行採用 == 52 LOSS行」を
  increments manifestで機械表明する (batch-15 Part ANと対称の単一シナリオ構造)。
- 入力: published正本のみ (batch-16 raws 104 = 完全p1/p2ペア + declaring-host
  status.log + batch-keys 52キー sha256 `465cf447…`、各ファイルfetch-back
  byte検証済み)。increments makerは2回実行しbyte一致必須。mergeはsha-pinned
  s5_union_merge (`90711961…`, selftest PASS) を2回実行しbyte一致必須、
  WIN/LOSS conflict 0 gate。scenario refresh はpinned Part Y refresh script
  (`88671526…`) の最小adapt (docstring / scenario cache path / cache sha
  expectationのみ) を2回**直列**実行し (batch-13並列OOM再発防止) 3出力とも
  run間byte一致必須。delta extractorはclass_status_countsをgraph + update8 +
  cacheから再計算し、BASE (published summary `25987add…`) とPLOSS52両方の
  summaryと一致するまでfail-closed。
- verdict不消費・solver探索なし・canonical cache不変更。本分解はwhat-if計画
  数量のみを生む。クラス閉鎖の判定・root被覆監査・第三手securedの主張は行わない
  (それらはPLOSS52計上後のrefresh再実行・独立監査が別途担う)。
- 標準11×11空盤・19 central-reply roots・class 10687他全classはどの時点でも
  **UNKNOWNのまま**。nodes数を勝敗として読まない。
- 本宣言 observed HEAD-before-push: `6af95d9c` (push直前にnote blob sha再照合、
  競合時は破棄し着手しない)。


### Part AO status update (2026-11-22, declaring host = 本レーンセッション)

宣言 (commit `ede3eb42`, observed HEAD-before-push `6af95d9c`) どおり完了。
単一シナリオ **PLOSS52** = BASE (canonical 6,027行 `95e868d6…`) + batch-16
52 LOSS行を計算した (WIN行ゼロ・枯損行ゼロのため「全resolved行採用 == 52 LOSS行」
はmanifestで機械表明済み)。

- 出版: 実験dir `research/experiments/n11-centralreply-class10687-loss52-ifadopted-20261122/`
  16ファイル (scripts 4 = increments maker / sha-pinned union merger `90711961…` /
  delta extractor / adapted scenario refresh (loss52/scripts側), output 6 = 52行増分
  `95345a5b…` + manifest + merge-audit run1/run2 + scenario cache 6,079行
  `342e8683…` + delta JSON `dd6a01ef…`, loss52/output 3 = refresh 3出力,
  README.md, status.log, MANIFEST-sha256.txt) を1コミット `5a5e56d8`
  (2026-11-22) でmainに反映、fetch-back 16/16 byte一致 (commit-pinned raw URL
  →sha256sum照合)。probe-worklist (3.7MB, sha256 `3b28ba59…`) はPart AH/AJ
  先例どおり不出版 (READMEにsha記録)。
- 全二重実行byte一致 (status.logに正本記録): increments maker 2回 (`95345a5b…`)、
  union merge 2回 (selftest PASS・WIN/LOSS conflict 0、`342e8683…`)、
  scenario refresh 2回直列実行 (~60s、4出力ともrun間byte一致:
  `7fd15927…`/`7405699e…`/`ec52a56d…`/worklist `3b28ba59…`)、delta extractor 3回
  (`dd6a01ef…`・全ゲートPASS)。extractorはgraph + update8 + cacheから
  class_status_counts・known-universe数・per-root free被覆を再計算し、BASE
  (published `25987add…`) とPLOSS52両summaryと一致するまでfail-closed。
- 機械測定された分解結果: **flipなし** (zero-WIN増分はflip不可能、
  excluded_now 23不変・flip集合は空と機械検証)。状態遷移台帳: excluded 390・
  excluded_now 23・free_now 35は全行不変、unknown→free_now 1、unknown→unknown
  34,500。**class 10687がwhat-if上でBoard検証free候補化** (free_now 35→36: what-if
  投影であり閉鎖主張ではない)、unknown 34,501→34,500。新規free第三手 {(16,56),(16,64)}
  はbatchのgroups_served_fullと機械一致、per-root被覆の変更行は (central,16) のみ
  (free_now 14→16・uncovered 105→103・不変式free+uncovered==119保持)、root 27
  baselineは119/119不変。increment子を持つ143個のgraph holder classすべてで
  scenario unknown_now == BASE unknown_now - own membership を機械検証
  (class 10661 53→52 own 1、class 10695 own 2でunknown維持)。
  update8は+1要件 (s5 376421: resolved 75→76, remaining 31,784→31,783,
  win_hit_groups 0不変)。スケジューリング数量 (heuristic測定・被覆とは別): joint
  greedy 35,242→38,522 (free化groupの除外による再選択であって被覆後退ではない)、
  worklist 65,154→65,097 (-57)、closure candidate表からclass 10687消滅
  (811→810行)、rank 14行は**class 10661** (mask `[1152921505697431552, 0]`,
  unknown 52, groups (24,30)系) に異動 = 機械特定された次のall-LOSS候補。
- **verdict不消費・閉鎖主張なし**: 52 LOSS行はPart AM証拠のままcanonical cache外。
  class 10687の閉鎖資格確定には、本what-ifとは別にPLOSS52計上後のcanonical
  increment化 + refresh再実行 + 独立監査 (別宣言・Part AP相当) が必要。
  14 unconsumed closure WINの採用判断はscrutiny ownerのC++第二実装ゲート pin
  `9193f5b6…` 待ちのまま。標準11×11空盤・19 central-reply roots・class 10687他
  全classはどの時点でも**UNKNOWNのまま**。nodes数を勝敗として読まない。
- 誤記録の訂正: session log continuation 27 内のbatch-keys sha略記
  `465cf44721a661ce94babeb12...` は写し損じ (正全文は
  `465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e`)。
  同continuationは全文をexperiment README/MANIFESTに正しく指しており、
  主張・照合への影響なし。正本 (batch-16 input/batch-keys.json出版bytes) は
  誤りを含まない。
- 本status updateのobserved HEAD-before-push: `5a5e56d8` (push直前にnote blob
  sha1 `059ba5aa…` を再照合、fetch-backで追記確認。競合時は再fetchして本節を
  追記し直す)。


## Part AP (canonical adoption + reaudit, declaration 2026-11-22): batch-16 (class 10687) 52 LOSS行のcanonical計上 + refresh再実行・独立監査によるclass 10687閉鎖資格確定

batch 16 (Part AM) は52/52全LOSS・枯損0で完走しており、52 LOSS行の消費は
fail-closed union merger経由で合法 (batch-2 23963, batch-10 8784, 10324の
先例どおり、C++第二実装ゲート pin `9193f5b6...` はWIN行採用のみに適用)。
Part AN (batch-15 if-adopted) は出版済みだが本Partでは計上しない。
batch-14 (Part AQ, in flight) とはキー・ファイルが非交差であることを
着手前に再確認する。52 LOSS行すべてを本Partで計上する (WIN行ゼロ・
枯損ゼロはpublished manifestで機械表明済み)。

- 対象: `research/experiments/n11-centralreply-class10687-loss52-adoption-reaudit-20261122/`。
- canonical cache出版 (単一ファイルコミット): published increment
  `95345a5b...` (Part AO `5a5e56d8`) を、BASE canonical 6,027行
  `95e868d6...` (8784-reaudit正本path) にsha-pinned union merger
  (`90711961...`, selftest PASS) でfail-closed mergeした6,079行cache
  (sha256 `342e8683...`・Part AO scenario cacheとbyte同一・merge 2回
  byte一致はPart AOで機械検証済み) を、新path
  `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-20261122.cache`
  として出版する。本reaudit内でincrements maker (`e35b545d...`) と
  mergerを再実行し、published bytes (increment `95345a5b...`, merge結果
  `342e8683...`) とのbyte一致とWIN/LOSS conflict 0を再び機械検証する
  (再導出分はstatus.logに記録、increment/auditの再出版は行わない)。
- refresh再実行 (reaudit本体): pinned Part Y refresh script (`88671526...`)
  のadapt (Part AO adapt `fb846776...` からcache pathとdocstringのみ
  変更、cache sha期待値 `342e8683...` は不変) を2回**直列**実行し、
  4出力ともrun間byte一致必須。closure-classes.csv・per-root-coverage.csv・
  probe-worklist.csvの3出力はPart AOのPLOSS52出力
  (`7405699e...` / `ec52a56d...` / `3b28ba59...`) とbyte一致必須
  (cache bytesが同一のため決定論的。差異があればfail-closed着手停止)。
  refresh-summary.jsonは`pins.merged_cache.path`が新canonical pathに
  変わる1フィールドのみの差分であることを機械diff検証する (他は全行
  byte一致必須)。
- 独立監査 (delta extractor): Part AO extractor
  (`compare_deltas_batch16.py`, `ca2a14f7...`) のadapt (SCEN cache
  path・SCEN summary path/sha・docstring文言・interpretation guardのみ
  変更、再計算gate群は全て不変) を3回実行しbyte一致必須・全gate PASS
  を必須とする: BASE summary (published `25987add...`) 対照、
  graph + update8 + canonical cacheからのclass_status_counts・既知
  universe数・per-root被覆の全再計算一致、class 10687がBoard検証free
  (36番目・free_now 35→36)、closure candidate表からclass 10687消滅
  (811→810行)、per-root変更行は (central,16) のみ (free 14→16, uncovered
  105→103, free+uncovered==119不変)、root 27 baseline 119/119、update8
  +1要件 (s5 376421: resolved 75→76, remaining 31,784→31,783,
  win_hit_groups 0不変)、143 holder classのown-membership算術gate、
  excluded_now flip 0、newly free third手 {(16,56),(16,64)} の
  groups_served_full機械一致。
- 主張 (本Partで確定するもの): **class 10687の閉鎖資格確定**
  (Board検証free・36番目・root 16の2 group secured。23963/8784/10324
  先例と同一の判定形式)。これはcanonical cache上の分類確定のみであり、
  19 rootの勝敗・標準11×11空盤には一切言及しない。
- 標準11×11空盤・19 central-reply roots・class 10687他全classはどの
  時点でも**UNKNOWNのまま**。nodes数・worklist数・greedy数を勝敗として
  読まない。
- 本宣言 observed HEAD-before-push: `a71bef64` (push直前にnote blob
  sha1 `7b14c2ac...` を再照合、競合時は破棄し着手しない)。本Partの
  出版はcanonical cache単独コミット→reaudit実験dirコミットの順で行う。


### Part AP status update (2026-11-22, declaring host = this lane session)

Executed and published exactly as declared (declaration commit `815391db`,
observed HEAD-before-push `a71bef64`, note blob sha1 `34d4c759...` at the
declaration). The canonical adoption consumed exactly the 52 batch-16 LOSS
rows; no WIN row was adopted and no verdict was created. The standard 11x11
empty board, the 19 central-reply roots and every class verdict remain
UNKNOWN throughout; free_now / closure qualification is canonical
classification status, never a win/loss claim.

- Reaudit staging (published for reproducibility): the increments maker is
  the byte-copy re-derivation of the Part AO script and reproduced the
  published increment bytes exactly (increment sha256 `95345a5b...`,
  manifest `28c90ba7...`); the sha-pinned fail-closed union merger
  (`90711961...`, selftest PASS) ran twice byte-identical -> **canonical
  reaudit cache: 6,079 rows (WIN 158 / LOSS 5,921, 249,622 bytes), sha256
  `342e86838e0c2bef915798059cb397f7c91e59c65426bf74db19530ecdd7979e`**,
  byte-identical (cmp) to the Part AO scenario cache; WIN/LOSS conflicts 0,
  duplicates 0; merge-audit run1 == run2 (`b69ea953...`).
- Publication commit `cd00857d`: the single-file canonical reaudit cache
  under `research/experiments/n11-centralreply-class10687-loss52-adoption-reaudit-20261122/output/`
  (fetch-back byte-identical).
- Adoption refresh: `reaudit/scripts/refresh_adoption_10687.py` (docstring +
  cache-path 2-hunk adaptation of the Part AO script, `fb846776...` ->
  `ad3dc0e6...`) run twice serial (~60 s each), 4 outputs byte-identical
  across runs; the three CSV outputs are byte-identical to the Part AO
  outputs (`7405699e...`, `ec52a56d...`, worklist `3b28ba59...`).
  Refresh-summary sha256
  `b278f822627560d7c3945ee0c0aded7de415b6141a69f0f8722e670432fc48da`,
  differing from the Part AO loss52 summary (`7fd15927...`) ONLY in
  `pins.merged_cache.path` (single line, machine-diff-verified).
- Adoption delta extraction: `scripts/compare_deltas_batch16_adoption.py`
  (11-hunk adaptation of the Part AO extractor `ca2a14f7...` ->
  `f78f7e60...`) run three times byte-identical, all gates PASS; output
  sha256
  `70c1b31e783b43e69397a692aea807a460c89f4827b33664a95eeceb31dc6acb`;
  vs the Part AO delta JSON (`dd6a01ef...`) the only differences are the
  three caption columns (schema / scenario / interpretation_guard) and
  pins.scenario_summary_sha256 - every delta value byte-identical.
- Publication commit `20deb45d`: the reaudit experiment directory (13
  files: README, status.log, MANIFEST-sha256.txt, scripts 3 = maker /
  merger / adapted extractor, reaudit/scripts/refresh_adoption_10687.py,
  output merge-audit run1/run2 + decomp-deltas-batch16-adoption.json,
  reaudit/output refresh-summary / closure-classes / per-root-coverage).
  Fetch-back 13/13 byte-identical (MANIFEST cross-checked; the MANIFEST
  itself byte-identical). probe-worklist (3.7 MB) not published (Part AH /
  AO precedent). Latest main at publication time was `20deb45d` itself;
  no parallel push observed.
- Machine-measured canonical consequences (all recomputed from the
  published pinned inputs; Board fail-closed child verification
  re-executed): Board verification free_candidates 36 /
  board_verified_free 36 / rejected {}; **free_now 35 -> 36, unknown
  34,500**; the closure-classes table drops from 811 to 810 rows with class
  10687 absent - **class 10687 is closure-qualified under the canonical
  classification**; its 52 canonical-unknown cost children are exactly the
  52 adopted keys. The only changed per-root coverage row is (central,
  first=16): free 14 -> 16, uncovered 105 -> 103 (free+uncovered==119
  held); root 16 secures the 2 groups {(16,56),(16,64)}; the root 27
  baseline stays 119/119 free thirds. update8 resolved 75 -> 76 (s5
  376421), remaining 31,784 -> 31,783, win_hit_groups 0 unchanged. Joint
  greedy re-selection to 38,522 (scheduling quantity only, not a coverage
  regression). The rank-14 row passes to **class 10661**
  (`[1152921505697431552, 0]`, unknown 52) - the machine-identified
  batch-17 candidate.
- Honesty record: consumed = exactly the 52 batch-16 LOSS rows (canonical
  classification). The 14 unconsumed closure WINs
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002)
  remain scrutiny-owner-blocked (C++ second-implementation gate pin
  `9193f5b6...`) and NO WIN row was adopted; win-hit groups stay 0.
  Nodes/budgets/gates are never verdicts.


## Part AQ (takeover owner, declaration 2026-11-22): batch 14 (class 23101) completion under takeover after declaring-host silence (verdict不消費・実行前に宣言)

Part AF (batch 14, class 23101, renewed rank 12) は2026-11-22T12:26:47Zにscaffold
(`54b7453d`, observed HEAD-before-push `9fe1a6c1`) を出版した後、実行結果を
1行も出版していない。現時点 (16:1xZ) までの沈黙は3時間40分を超え、batch 8/11
takeoverで用いた「宣告hostがrows・statusを出版しないまま20分以上沈黙」基準を
大きく超過する。kit鏡像 (batch23101, published scaffoldと65/65 byte一致) にも
Part AF実行由来のrawは存在せず、rescue対象行はない。以上より、batch-14の残務
(52キー全部) をPart AFの事前登録プロトコルのまま本takeoverセッションで完走する。

- 対象: `research/experiments/n11-centralreply-closure-class23101-batch14-20261122/`
  (Part AF宣言のスコープを引き継ぐ。scaffold/input/scripts/val-gateのpublished
  bytesは一切変更しない。本takeover由来の出力はraws/status.log/README Result)。
- 本takeover hostで宣言前に機械実施した再検証 (全PASS):
  (1) published scaffold 65ファイル == kit鏡像 byte一致 (MANIFEST-sha256.txt
  全行照合)。jsreplay.js sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (pin一致)。(2) canonical merged cache 6,027行 (sha256 `95e868d6…`) に52/52不在
  (0 hits)。(3) quarantine registry (sha256 `81d23160…`, active 2件) とのkey対照
  両方向0 hits。(4) 52キー重複なし。(5) closure-classes.csv (published Part Y正本)
  rank 12行 = class 23101 (`[1152921504892059648, 16]`, unknown 52, first 24 /
  third 28, groups 3)。(6) 12 unconsumed WINキー (b018/d002/e002/f017/g018/j033/
  h045/z003/n005/n006/p002/p003) 交差0 hits (12キーのlo/hi/result=1をpublished
  batch rawsのreplay行から再抽出して照合)。(7) probe-worklist 65,154行
  (sha256 `1807e4d2…`) のprobe_order 538-589 = serving_class 23101・
  class_unknown_now=52全行で、batch-keys 52キーとlo/hi/legal/s5_index完全一致。
  (8) val-gate fresh 4/4 node-exact (at2m 2件 result 0 / nodes 2,000,000、
  15m 2件 result 2 / 3,651,923 / 5,040,200。出力はoutput/val-gate/
  `*.takeover-aq.out` として保存・出版する。forbidden quadruples 95670双方)。
- protocol (Part AF事前登録のまま、変更なし): 2-pass fresh cold replay、budget
  15,000,000、1行1プロセス、p1/p2の (budget,result,nodes) 不一致でHARD-STOP
  (rc=42)、WIN検出でWIN-HALT (rc=45、同一wave内in-flightキーは完了まで開示)、
  resume-safe runner (4キー/wave)、honest negative (result 0 = UNKNOWN)。
- 主張と消費規則: verdict不消費。WIN-HALT行はunconsumed closure WINとして
  15番目以降の候補に加わる (採用判断はscrutiny owner、C++第二実装 gate pin
  `9193f5b6…` 前例・不変)。全LOSS完走の場合の消費 (increment + refresh再監査)
  は別宣言が必要。batch選択・nodes数はscheduling/測定数量でありverdictではない。
  標準11×11空盤・19 central-reply roots・class 23101は本batchのどの時点でも
  **UNKNOWNのまま**。
- 並走との不接触: Part AO (batch-16 if-adopted分解、2026-11-22T16:04:18Z宣言・
  in flight) のスコープ・ファイルには一切接触しない。他レーンのpublished成果
  にも不接触。実行・出版の各段階で最新mainを取り直す。
- 誠実記録: Part AF hostの消失は「沈黙超過からの推定」であり、宣告host側が
  後にrawsを出版してきた場合は本takeover分と著者側で対比検証する (batch 8/11
  と同じ取り扱い)。重複した再探索が発生した場合、13番目のキー以降は本側で
  skipし対照に回すことを優先する。
- 本amendment observed HEAD-before-push: `ede3eb42…` (push直前にnote blob
  sha1を再照合し、競合時は再fetchして本節を追記し直す。同スコープ対抗宣言が
  存在する場合は本takeover宣言を破棄して着手しない)。


### Part AQ status update (2026-11-22, takeover host = 本レーンセッション)

宣言 (commit `398a96ae`, observed HEAD-before-push `ede3eb42`) どおり完了。
batch 14 (class 23101, renewed closure rank 12, mask `[1152921504892059648, 16]`,
unknown 52, groups 3, first 24 / third 28) の52キーをPart AF事前登録プロトコル
のまま本takeoverセッションが実行し、42キー目で事前登録WIN-HALT規則が発火した。

- 結果: **WIN-HALT at q042 (result 1 WIN, 9,149,084 nodes, 2-pass fresh cold
  node-exact)** (s5_index 745184, key `[1152921505747697664, 1032]`, legal 85,
  probe_order 579)。同一wave内in-flightのq039/q040/q041は完了まで開示
  (いずれもLOSS 2-pass node-exact: 2,502,014 / 2,175,857 / 2,514,109 nodes)。
  q043-q052 (10キー) は着手せず (halt規約)。42 probed = 41 LOSS + 1 WIN・
  budget枯損 (result 0) 0・determinism mismatch 0・総ノード数/pass 88,338,850。
- row-audit.json (schema `n11-centralreply-closure-class23101-batch14-rowaudit-takeover-v1`,
  sha256 `cc22a1c8057d06b829060d321edd6e26e016ff7d92bce9c7c66eb4cca5ca24c7`):
  全42行でp1/p2 (budget,result,nodes) 一致、legal/lo/hi/probe_order が
  batch-keys (sha256 `dfde0e90…`) と一致、forbidden quadruples 95,670両pass、
  `# replay_done` 完全性、status.log相互照合、problems空。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-class23101-batch14-20261122/`
  156ファイル (published scaffold 65 + takeover raws 84 (q001-q042のp1/p2) +
  status.log + row-audit.json + val-gate takeover 4 + scripts/runwave-aq.sh +
  README Takeover/Result + MANIFEST-sha256.txt) を4コミットでmainに反映
  (raws chunk1 `21affe23`、raws chunk2 `d064e3aa`、status+audit+val-gate+
  runner `4cf1d248`、README+MANIFEST `7b211d38`)。fetch-back 156/156 byte一致
  (MANIFEST-sha256全照合・publication commit `7b211d38`で全ファイル取得)、
  kit鏡像byte一致。
- 誠実記録 (並走・canonical): 本takeover実行中に並走がPart AO
  (batch-16 if-adopted分解 `5a5e56d8`) とPart AP (batch-16 52 LOSS行のcanonical
  計上 + reaudit。canonical exact-S5 cache 6,027→6,079行 sha256 `342e8683…`、
  class 10687閉鎖資格確定) を完走出版した。Part AO/APスコープへの本側書込みは
  ゼロ。takeover実行後、batch-14の52キー全部 (probed 42・WIN q042含む) が
  新canonical 6,079行cacheに不在 (0 hits) であることを機械再照合済み。
  なお宣言時 (16:11Z) のfail-safe照合は当時正本の6,027行 `95e868d6…` に対して
  実施済みであり、両方のcacheに対して52キー不在は成立している。
- verdict不消費・状態: **q042は15番目のunconsumed closure WIN**
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042)。
  class 23101の「全52子LOSS」閉包ルートは検証済みWIN子で反駁 (このルートに
  関するverdict-level記述のみ。行のゲーム理論的値は判定しない)。採用判断は
  scrutiny owner (C++第二実装 gate pin `9193f5b6…`) 待ち・不変。
  batch実績: 15バッチ → **12 WIN-HALT + 3 clean** (23963/10324/8784 = 33/34/35番目
  free。class 10687は本takeover中に並走Part APで閉鎖資格確定)。
- 標準11×11空盤・19 central-reply roots・class 23101・その全S5子 (未着手
  q043-q052含む) はどの時点でも**UNKNOWNのまま**。nodes数を勝敗として読まない。
- open (着手前に必ず最新mainで対抗宣言確認要): (a) q042の第三実装交叉検証
  (Part G/K/O/P/T/W/AA/AD規約・anchor 2 + negative 2・rules gate)、
  (b) q042単WINのif-adopted分解 (Part V/R/AB/AH/AI/AN流・対抗宣言 grep必須)、
  (c) 41 LOSS行のcanonical計上 + reaudit (Part AP流・別宣言・Part AP採用で
  canonicalが更新されているため増分は新6,079行cacheに対して構築)。
- 本status updateのobserved HEAD-before-push: `7b211d38…` (note blob sha1ロック
  `7bb7a66d…` で更新、fetch-backで追記確認)。


## Part AR (verifier, declaration 2026-11-22): batch-14 q042 WIN + in-wave LOSS 3行の第三実装交叉検証 (verdict不消費・実行前に宣言)

Part AQ (batch-14 takeover) は42キー目で事前登録WIN-HALT規則を発火させた
(q042: 2-pass fresh cold node-exact result 1, 9,149,084 nodes)。Part G/K/O/P/T/W/AA/AD/AG/AL
と同一規約で、q042 WIN行と同一wave内in-flight開示済みのLOSS 3行
(q039/q040/q041) の第三実装verdict-level交叉検証を単一オーナーとして実行する。
**verdict不消費・検証はverdict-level文献作成のみ・採用判断はscrutiny owner。**

- 対象: `research/experiments/n11-centralreply-closure-batch14-q042-thirdimpl-20261122/`。
  targets = batch-14のprobed行から4行: WIN 1行 (q042) + LOSS spot 3行 (q039/q040/q041、
  同wave in-flight開示行。batch-9 Part T (j033 + 3 LOSS spots) と同型の選択)。
  残り38 LOSS行は本実験の対象外 (全行検証が必要な場合は将来の別宣言)。q043-q052 (10キー)
  は未着手のまま着手しない。
- 入力: published正本のみ (batch-14 published raws (takeover由来・publication commit
  `7b211d38`): q039-q042のp1/p2 8ファイル、status.log、batch-keys.json sha256
  `dfde0e90…`、input CSV)。`make_inputs_batch14.py` (batch-15版をadapt・schema文字列は
  `batch14-q042-thirdimpl`) がfail-closed導出: 2-pass一致assert・status.log PASS行・
  `q042 WIN-HALT` 停止行・WAVE-END stop=1行の存在assert・derived CSVがpublished
  input CSVとbyte一致するassert・class_index 23101 assert・手転写ゼロ。
- 手法: pinned `third_impl.js` (sha256 `08ea958f…`)・`verify_tbl.js` (`c8c52528…`)・
  1行1プロセス・`--cap=300000000 --wallcap=240 --memo-power=22`・1行2回 (a/b)
  determinism gate (result/expansion/ttHits/reason 同一必須)・rule-engine gate
  (quads 95,670 == replica / TBL==wob mismatches 0、target走行前に実施)。
  anchors k02a (WIN, legal 87, 期待 9,106,337 expansions / 4,991,527 ttHits) と
  l1a (LOSS, legal 116, 期待 7,660,602 / 3,951,175) は本ホスト再現がpublished値と
  node-exact必須、negatives ng1 (legal+1) / ng2 (stones+1) は文言一致GATE_FAIL必須。
  2-coreホストで最大2並列。wall超過 (runlimit) はhonest wall-inconclusiveとして
  記録し検証主張としない。cleanな不一致はdivergence evidenceとして記録するが
  本レーンはverdictを書き換えない。
- 主張と消費規則: verdict不消費 (採用は引き続きscrutiny owner・C++第二実装 gate pin
  `9193f5b6…` 待ち・不変)。標準11x11空盤・19 central-reply roots・class 23101は
  本検証のどの時点でもUNKNOWNのまま。nodes/expansionsを勝敗として読まない。
- 並走との不接触: Part AO/AP/published成果には一切書込みしない。同一スコープの
  対抗宣言がmainに存在する場合は本宣言を破棄して着手しない。
- 本amendment observed HEAD-before-push: `a54a9402…` (push直前にnote blob sha1
  ロック `a4cd1465…` を再照合、競合時は再fetchして追記し直す)。


### Part AR status update (2026-11-22, verifier host = 本レーンセッション)

宣言 (commit `e640f5b6`, observed HEAD-before-push `a54a9402`, note blob sha1
ロック `a4cd1465…`) どおり完了。batch-14 q042 WIN行と同一wave開示LOSS 3行
(q039/q040/q041) の第三実実装交叉検証を単一オーナーとして実行し、**4/4
verdict一致** (WIN=1, LOSS=3)・wall-inconclusive 0・divergence 0で完走した。

- 入力導出: `scripts/make_inputs_batch14.py` (batch-15 Part AL版をadapt、sha256
  `19c442d18e0a9300cf21424c12ce62cafb61c1b899fed3c111be402a2ae759bb`) が
  published正本 (takeover raws 8 (q039-q042のp1/p2)・status.log・batch-keys.json
  sha256 `dfde0e90…`・published input CSV) からfail-closed導出した (2-pass一致
  assert、status.log PASS行・`q042 WIN-HALT` 停止行・WAVE-END stop=1行の存在
  assert、derived CSV vs published CSV byte一致assert、class_index 23101 assert、
  手転写ゼロ)。初回ABORTはq042 PASS行パースの`toks[3]`インデックスbugで、
  修正後に4 targets + 2 anchors + 2 negativesを生成した。
- 前提ゲート全PASS: rules gate (replica quads 95,670 == third-impl quads
  95,670、triples checked 195,044 / TBL mismatches 0)、script pins 3種
  (third_impl `08ea958f…` / verify_tbl `c8c52528…` / jsreplay `84585617…`)。
  anchors node-exact: k02a WIN 9,106,337 expansions / 4,991,527 ttHits、l1a LOSS
  7,660,602 / 3,951,175 (published値と完全一致)。
- negatives: ng1 (k02のlegal+1, 88 vs derived 87) / ng2 (stones 6 vs 5) ともに
  文言一致でGATE_FAIL、rc=1 (fail-closed設計どおり)。
- 結果 (1行1プロセス・a/b 2回・全行deterministic clean): q042 = 第三実装 **WIN**
  10,728,035 expansions / 5,758,042 ttHits (a 65.14s / b 64.78s)、q039 / q040 /
  q041 = **LOSS** 2,828,518 / 2,425,671 / 2,843,397 expansions (ttHits
  1,663,204 / 1,519,018 / 1,693,916)。4行すべてtakeover replica (jsreplay系)
  verdictとverdict-level一致。nodes/expansionsの差は実装差でありverdictでは
  ない。takeover hostと別のsandboxでの実行によるcross-host cross-implementation
  corroboration。
- verdict-level主張: class 23101の「全52子LOSS」閉包ルートは2実装合意WIN子
  (q042) で反駁 (route statementのみ、採用はscrutiny owner待ち)。
- 監査バッテリ: `scripts/audit.py` (schema
  `n11-centralreply-closure-batch14-q042-thirdimpl-audit-v1`, sha256
  `4bb6266becd294b2e3a01820da2416162e6276c5ff7cb08eee60266036524b95`) が
  **71/71 gates PASS**、2回実行で出力byte同一 (output/audit-summary.json
  sha256 `18125d63a0b6ae0ad22ec58b10c947c945b775d625b8c6889d1c07b0c06a292b`)。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-batch14-q042-thirdimpl-20261122/`
  49ファイルを5コミットでmainに反映 (sources+input `5ad33735` 23ファイル、
  fetch-back転写ミス2件 (status.logのq025行timestamp誤字・ng2 stones) 修正
  `335fc0a1`、scripts `703840f9` 6ファイル (published bytesとsha検証一致の
  複製+audit.pyのbatch-14 schema差替)、outputs `af79f4a1` 18ファイル、README +
  audit-summary.json + MANIFEST-sha256.txt `0f69d03` = publication complete)。
  **fetch-back 49/49 byte一致** (publication commit `0f69d03` で
  MANIFEST-sha256.txt全行sha256照合)。
- 誠実記録 (runner): 最初のnegatives呼び出しはshell cwd grouping bugでng2の
  プロセスが未起動 (`No such file or directory`) だった。絶対pathで再実行し、
  ng1はbyte同一のGATE_FAIL行を再生成したため、status.logにng1重複RUN行が
  残存した。実行と出版に他の逸脱なし。
- verdict不消費・状態: q042は**15番目のunconsumed closure WIN**のまま (b018/
  d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042)。
  batch-14の全probed行 (41 LOSS + q042 WIN) はcanonical 6,079行cache
  (`342e8683…`) に不在 (Part AQ status updateで機械照合済み)。採用判断は
  scrutiny owner (C++第二実装 gate pin `9193f5b6…`) 待ち・不変。
- 標準11×11空盤・19 central-reply roots・class 23101・その全S5子 (未着手
  q043-q052含む) はどの時点でも**UNKNOWNのまま**。nodes/expansionsを勝敗として
  読まない。
- open (着手前に必ず最新mainで対抗宣言確認要): (a) q042単WINのif-adopted分解
  (Part V/R/AB/AH/AI/AN流)、(b) 41 LOSS行のcanonical計上 + reaudit (Part AP流。
  増分は現行canonical 6,079行 `342e8683…` に対して構築)、(c) batch-17
  (class 10661, Part AP再監査rank 14) 宣言。
- 本status updateのobserved HEAD-before-push: `0f69d03…` (note blob sha1
  ロック `8edd32f7…` で更新、fetch-backで追記確認)。


## Part AS (adoption, declaration 2026-11-22): batch-14 (class 23101) 41 LOSS行のcanonical計上 + reaudit (実行前に宣言)

Part AQ (batch-14 takeover) が出版したprobed 42行 (41 LOSS + q042 WIN) のうち
**41 LOSS行 (q001..q041) のみ**を、Part AP (batch-16 52 LOSS行) と同一形式で
canonical exact-S5 verdict cacheへ計上する。**q042 WIN行は採用しない**
(verdict不消費・15番目のunconsumed closure WINのまま・scrutiny owner待ち)。

- 対象: `research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/`。
- 入力はpublished正本のみ: batch-14実験dir (publication commit `7b211d38`) の
  raws 84 (q001-q042のp1/p2)・status.log・batch-keys.json (sha256 `dfde0e90…`)・
  現行canonical 6,079行cache (sha256 `342e8683…`)。maker (Part AP版 `e35b545d…` を
  batch-14にadapt) がfail-closed導出: 41 LOSS行の3-way (p1/p2/status) node-exact
  gate、batch-keys legal/(lo,hi) 照合、q042 WIN行の2-pass検出とincrementからの
  機械除外 (採用増分にWIN行は1行も含めない)、41キーのBASE cache不在 (0 hits)、
  quarantine 0。
- 手法: sha-pinned fail-closed union merger (`90711961…`) でcanonical 6,079行に
  41行をmerge (2回実行・byte一致・WIN/LOSS conflict 0) → **canonical 6,120行**を
  新pathに出版。Part Y refresh script adapt版 (Part AP版 `ad3dc0e6…` からcache
  path/shaと文言のみ変更) を2回直列実行・run間byte一致・root27 119/119 gate。
  delta extractor (Part AP版 `f78f7e60…` をbatch-14にadapt) を3回実行・byte一致・
  全gate PASS (BASE=Part AP reaudit出力、scenario=本reaudit出力、遷移ledger・
  holder own-membership算術・update8増分universe一致・per-root被覆再計算)。
- 主張範囲: canonical cache上の分類のみ。class 23101は採用後もunknown 11子
  (未着手q043-q052 + 未採用q042) を持ちfree_now/excluded_nowのいずれにもならない
  (closure候補表内のunknown減少のみ)。本Part単体ではroot被覆・第三手secured・
  クラス閉鎖の主張をしない。
- verdict不消費: q042 WIN行を含む15 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042)
  は採用判断 scrutiny owner (C++第二実装 gate pin `9193f5b6…`) 待ち・不変。
- 標準11×11空盤・19 central-reply roots・class 23101の全S5子 (未着手q043-q052
  含む) は本Partのどの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。
- 並走との不接触: batch-17 (class 10661) は本Partでは宣言・scaffold・実行ともに
  行わない。Part AQ/ARとpublished成果への書込みはextractor/refreshの読み取り
  のみ。同一スコープの対抗宣言がmainに存在する場合は本宣言を破棄して着手しない。
- 本amendment observed HEAD-before-push: `b394c3ca` (push直前にnote blob sha1
  を再照合し、競合時は再fetchして本節を追記し直す)。
### Part AS status update (2026-11-22, adoption host = 本レーンセッション)

宣言 (commit `5b6af2ed`, observed HEAD-before-push `b394c3ca`, note blob sha1
ロック `7a534356…`) どおり完了。batch-14 (class 23101) の41 LOSS行
(q001..q041) をcanonical exact-S5 verdict cacheへ計上する採用・再監査を
単一オーナーとして実行し、出版まで完了した (full != loss: q042 WIN行は
採用しない・verdict不消費)。

- maker: `scripts/make_increments_batch14.py` (published Part AP版
  `e35b545d…` をbatch-14にadapt) がpublished raws (publication commit
  `7b211d38`) からfail-closed導出。41 LOSS行 increment 3,498 bytes
  sha256 `5194af934a5373823a819ec53178dd008d1c6d5b17488101aa742ca1230d0831`、
  manifest sha256
  `8b5540f9aa1f9bdd40ef73b0353577da3d90c36ea3e43a8586f886e6390fe502`
  (schema `batch14-loss41-increments-manifest-v1`、row_counts 41/0/41/0
  (42 resolved / 52 probed)、unadopted_win_ids == ["q042"]、
  full_packet_eq_loss_only false、win_scenario_exists true)。
  q042の2-pass WIN結果 (result 1, 9,149,084 nodes) はrawから機械再検証のうえ
  incrementから除外。
- merge: sha-pinned fail-closed union merger (`90711961…`, byte-copy pin、
  selftest PASS) でPart AP正本canonical 6,079行 (`342e8683…`) に41行をmerge、
  **canonical 6,120行** (WIN 158 / LOSS 5,962, WIN/LOSS conflict 0,
  duplicates 0, 251,466 bytes, sha256
  `be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685`) を
  新pathに出版。2回実行・byte一致・merge-audit 2回byte一致
  (`54c581ee…`)。
- refresh: adapt版 `reaudit/scripts/refresh_adoption_23101.py` (Part AP版
  `ad3dc0e6…` から3ハンク: docstring文言・canonical cache path・cache sha
  期待値はcacheファイル自体から機械抽出) を2回直列実行、4出力ともrun間
  byte一致: refresh-summary `f2008e70…` / closure-classes `3ee1dbb6…` /
  per-root-coverage `527c7e9a…` / probe-worklist `1c96df05…` (3.7MB、
  Part AH/AO/AP先例どおり不出版・sha記録のみ)。
- delta extractor: `scripts/compare_deltas_batch14_adoption.py` (Part AP版
  `f78f7e60…` をbatch-14にadapt。新規: q042不消費ゲート6面 (increment・
  BASE cache・scenario cache・quarantine・BASE/scenario index_verdict・
  class 23101のscenario-unknown子集合)、zero-WIN partial packetの
  new-free空集合gate、closure表churn観測、q042 rawの2-pass再検証; 再計算
  gate群は全て不変) を3回実行・出力byte同一 (`7155fdaa…`)・全gate PASS。
  BASE (Part AP reaudit正本、publication commit `20deb45d` で取得し
  `b278f822…` / `7405699e…` / `ec52a56d…` とsha検証済み) とscenario両方に
  対してclass_status_counts・既知universe数・per-root被覆の再計算一致を
  fail-closedで保証。
- 結果 (canonical cache上の分類のみ): class 23101のunknown費用子は
  **52 → 11** (残11 = 未採用q042のs5 745184 + 未着手q043-q052の10キー、
  機械一致)。closure候補表 **rank 12 → rank 1** (unknown_now 11)。
  class 23101はfree_now/excluded_nowのいずれにもならない。free_now 36・
  excluded_now 23・unknown 34,500は全域不変・遷移ledger全同一・
  excluded_now flip 0・新規free 0 (いずれもgate済み)。per-root free被覆は
  全19 root不変 (root27 baseline 119/119)。update8 resolved 76 → 79
  (s5 707915/713201/740437、すべてincrement内LOSSとgated)、remaining
  31,783 → 31,780、groups_free 127不変。closure候補表 810 → 809行 (退出7:
  1250/2233/4912/15394/22002/22119/22859、新規6: 21387/21934/22925/23075/
  23102/23283 = 台帳churn)。class 10661はrank 14不変 (batch-17候補)。
  joint greedy 38,522 → 36,726 (-1,796)、probe worklist 65,097 → 64,941
  (-156) (いずれも簿記・被覆変更0)。
- 出版: 実験dir `research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/`
  16ファイルを3コミットでmainに反映 (canonical cache単独 `f03809fa`
  (observed HEAD `7196cbd5`、paged-readで251,466 bytes完全連結・長さ検証)、
  scripts+increment+manifest `5e579b03`、outputs+README+status.log+MANIFEST
  `8c42e44c` = publication complete)。**fetch-back 15/15 byte一致**
  (publication commit `8c42e44c` 固定raw URLでMANIFEST-sha256.txt全行を
  sha256照合)。
- 誠実記録 (runner): extractor初回書き損じ2件 (batch-keysの
  groups_served_full→groups_served_first_seen schema差、replay行の列
  offset誤り) はfail-closed gateが即時捕捉し、修正後3回byte同一で可決。
  sequence中のsha手転写事故なし。
- verdict不消費・状態: q042は**15番目のunconsumed closure WIN**のまま
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042)。
  採用判断はscrutiny owner (C++第二実装 gate pin `9193f5b6…`) 待ち・不変。
  canonical cache上の41 LOSS行の採用は本Partが消費した唯一のverdict。
- 標準11×11空盤・19 central-reply roots・class 23101 (unknown 11子) の
  全S5子はどの時点でも**UNKNOWNのまま**。nodes数・worklist数・greedy数を
  勝敗として読まない。
- open (着手前に必ず最新mainで対抗宣言確認要): (a) q042単WINのif-adopted
  分解 (Part V/R/AB/AH/AI/AN流・新canonical 6,120行 `be9cb24e…` をBASEに
  構築)、(b) batch-17 (class 10661, rank 14, `1152921505697431552,0`,
  unknown 52) 宣言、(c) batch-15等の残るunconsumed WIN群の同形式reaudit。
- 本status updateのobserved HEAD-before-push: `8c42e44c…` (note blob sha1
  ロック `7a534356…` で更新、fetch-backで追記確認)。
## Part AT (verifier, declaration 2026-11-22): q042単WIN行のif-adopted分解 (scrutiny owner向け事前計算・verdict不消費・実行前に宣言)

Part AS (41 LOSS行canonical計上) 完了時点で、batch-14のq042 WIN行
(s5_index 745184, key `[1152921505747697664, 1032]`, result 1,
9,149,084 nodes, 2-pass node-exact, 第三実装一致済み (Part AR)) は
15番目のunconsumed closure WINのまま。採用判断 scrutiny owner (C++第二実装
gate pin `9193f5b6…`) のためのif-adopted分解を、Part V/R/AB/AH/AI/AN/AO流
(b018/d002/e002/r001/r002等のk04 precedent) と同一形式で実行する。
**verdict不消費・本Partは採用を推奨も却下もしない・if-adopted投影を勝敗や
閉鎖主張として読まない。**

- 対象: `research/experiments/n11-centralreply-class23101-q042-ifadopted-20261122/`。
- BASE = 現行canonical 6,120行 (sha256 `be9cb24e…`, publication commit
  `8c42e44c` の `n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/`)。
  q042のkeyはBASEに不在 (Part AS extractorの6面gate済み)。
- 増分 = 単一WIN行 (published batch-14 raws q042.p1/q042.p2, publication
  commit `7b211d38`; makerが2-pass node-exact (result 1, 9,149,084 nodes
  両pass一致) をrawから機械検証し、BASE不在・quarantine不在・canonical key
  形式をgateしてから1行incrementを導出)。
- 手法: sha-pinned fail-closed union merger (`90711961…`, byte-copy pin)
  2回実行・byte一致 → **if-adopted cache 6,121行** (WIN 159 / LOSS 5,962,
  canonicalではなく投影)。refresh script adapt版 (Part AS版 `5992738d…` から
  cache path/sha・文言のみの変更・sha期待値はcache自体から機械抽出) を2回
  直列実行・run間byte一致。delta extractor (Part AS版 `9e885ae0…` をWIN単行
  if-adopted用にadapt: flips == s5 745184をcost childとして持つunknown保持
  クラスの機械計算集合、WIN採用によるfree化は起きえない gate、update8
  win_hit_groups変化の機械抽出・resolved基線不変) を3回実行・byte一致・全gate
  PASS。
- 主張範囲: if-adopted投影上の分類delta (flip集合・win_hit_groups・被覆・
  worklist等の数表) のみ。canonical cacheは本Partで一切変更しない。
- verdict不消費: 本Partが消費するverdictはゼロ (if-adopted cacheはrepoの
  canonical chainではない)。q042はcanonical上も未来の採用判断上もunconsumed。
- 標準11×11空盤・19 central-reply roots・class 23101・全classは本Partの
  どの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。
- 並走との不接触: batch-17 (class 10661) は本Partでは宣言・scaffold・実行ともに
  行わない。Part AS/published成果への書込みは読み取りのみ。同一スコープの
  対抗宣言がmainに存在する場合は本宣言を破棄して着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージ
  に記録 (push直前にnote blob sha1ロック `3c9f42f4…` を再照合し、競合時は
  再fetchして本節を追記し直す)。

### Part AT status update (2026-11-22, verifier host = 本レーンセッション)

宣言 (commit `58938933`, observed HEAD-before-push `2f88a495`, note blob
sha1ロック `9a5dfdb7…`) どおり完了。q042 (s5_index 745184, result 1,
9,149,084 nodes) 単WIN行採用時のif-adopted投影分解を単一オーナーとして
実行し、出版まで完了した (verdict不消費・canonical不変・推奨/却下
いずれでもない)。

- maker: `scripts/make_increment_q042_win.py` (Part AS/Part AP maker系の
  単WIN adapt・WAVE-END正規表現の複数キー並び非対応bugを修正) が
  published batch-14 raws (publication commit `7b211d38`) から2-pass
  node-exact WINを機械検証し、BASE不在 (6,120行)・quarantine不在をgate
  して1行 increment (sha256
  `b4958328270f11b24d3a638e1099a0c6047dbebb242e3116217b0473ef63f9b6`)
  とmanifest (`894e9420…`,
  schema `batch14-q042-win-ifadopted-increment-manifest-v1`,
  ifadopted_only, canonical untouched pin) を導出。
- merge: sha-pinned fail-closed union merger (`90711961…`, byte-copy
  pin, selftest PASS) でcanonical 6,120行 (`be9cb24e…`) + 1 WIN行を
  3回実行・byte一致、**if-adopted cache 6,121行** (WIN 159 / LOSS
  5,962, conflict 0, 251,513 bytes, sha256
  `1434c68bc572a9817eca9c9a4ab442005762339cf539f22cb3acb0b24bc5ffe0a`)
  を生成。merge-audit 3回byte一致 (`e1d11a66…`)。BASE canonicalは
  merge後に再検証してbyte不変 (verdict不消費・repo canonical chain外の
  non-canonical投影)。
- refresh: adapt版 `reaudit/scripts/refresh_q042_ifadopted.py` (Part
  AS版 `5992738d…` から3ハンク) を2回直列実行 (~61s/回)、4出力とも
  run間byte一致: refresh-summary `029cc3b6…` / closure-classes
  `987c4ecb…` / per-root-coverage `ec71c81b…` / probe-worklist
  `af0c28c5…` (不出版・sha記録のみ)。
- delta extractor: `scripts/compare_deltas_q042_ifadopted.py` (Part AS版
  `9e885ae0…` をWIN if-adoptedにadapt。新規: flips == s5 745184の
  BASE-unknownグラフ保持クラスの機械計算集合 (ハードコードなし)、純WIN
  採用の新規freeクラス空集合gate・per-root free/uncovered不変gate・
  新規free第三手空集合gate、23101 flip含有 + scenario-unknown==10
  gate、canonical BASE sha pin、BASE index_verdict不在gate、raw
  2-pass再検証; 再計算gate群は全て不変) を3回実行・出力byte同一
  (`8e6ce1c6…`)・全gate PASS。
- 結果 (投影上の分類台帳deltaのみ): **flips = 4クラス
  [23092, 23101, 23115, 23938]**、すべてs5 745184を費用子に持つ
  BASE-unknown保持クラスでunknown→excluded_now遷移。**この4クラスの
  全LOSS閉包ルートはWIN子で永久反駁** (route statement)。excluded_now
  23→27 / unknown 34,500→34,496 / free_now 36不変・遷移台帳は上記4+
  同一遺移のみ (gate済み)。class 23101のscenario-unknown子は**10個**
  (未着手q043-q052側10キー 745455..745465、WIN子はunknown境界から
  消失)。closure候補表809行不変・churnなし (退出0/新規0)・23101は
  rank 1のまま (表はprobing-worklist viewであり、flipは
  class_status_countsと遷移台帳で記録)。per-root free/uncoveredは
  全19 root不変 (root27 baseline 119/119、変更行0・新規free第三手0、
  いずれもgate)。per-root greedyはroot 24のみ-1 (2,785→2,784、簿記)。
  update8 resolved 79不変・remaining 31,780不変・groups_free 127不変・
  win_hit_groups []不変 (**s5 745184はupdate8 baseline requirement外
  と機械判明**)・lost [] (gate)。joint greedy 36,726→36,725・probe
  worklist 64,941→64,940 (いずれも-1・簿記)。
- 出版: 実験dir
  `research/experiments/n11-centralreply-class23101-q042-ifadopted-20261122/`
  16ファイルを3コミットでmainに反映 (if-adopted cache単独 `59fe5654`
  (observed HEAD `58938933`、paged-readで251,513 bytes完全連結・長さ/
  eol/末尾検証)、scripts+increment+manifest `f0a45654` (observed HEAD
  `59fe5654`)、outputs+README+status.log+MANIFEST `175864a5` (observed
  HEAD `f0a45654`) = publication complete)。**fetch-back 15/15 byte一致**
  (publication commit固定rawのMANIFEST全行sha256照合)。kit mirror
  `_19root-refresh-kit/batch23101-q042-ifadopted/` (16ファイル・sha全
  一致・worklist 3.6MBは不採録)。
- verdict消費: **ゼロ**。q042はcanonical上も未来の採用判断上も**15番目
  のunconsumed closure WINのまま** (b018/d002/e002/f017/g018/j033/
  h045/z003/n005/n006/p002/p003/r001/r002/q042)。canonical cacheは
  6,120行 `be9cb24e…` 不変。標準11×11空盤・19 central-reply roots・
  class 23101・未着手q043-q052他全classはどの時点でもUNKNOWNのまま。
  nodes数を勝敗として読まない。WIN行採用は引き続きscrutiny ownerの
  C++第二実装ゲート (`9193f5b6…`) 待ち。
- 本status updateのobserved HEAD-before-push: `ee3b6f7325d6d4ae697f93d1f4c520dfd06f59f3` (note blob sha1
  ロック `9a5dfdb7…` で更新、fetch-backで追記確認)。

## Part AU (solver-declaration + scaffold, declaration 2026-11-22): closure class 10661 exact-S5 probe batch 17 (実行前に宣言・本Partはscaffold出版まで・verdict不消費)

Part AT (q042 if-adopted投影) 完了時点で、Part AS reaudit closure候補表
 rank 1 (class 23101) はin-flight (未着手q043-q052の10キー + 未採用
q042)、rank 2-13 (16757, 20421, 16371, 30345, 12264, 5473, 2634, 8785,
1518, 8106, 16930, 5830) はいずれもunconsumed closure WIN子を費用子に
持ち全LOSS閉包ルート反駁済み (route statement)。**反駁証拠のない最初の
候補 = rank 14 class 10661** (mask `[1152921505697431552, 0]`・unknown
52子・closure groups (24,30)+(24,90)・機械再計算一致) にbatch 17として
着手を宣言する。

- 対象: `research/experiments/n11-centralreply-closure-class10661-batch17-20261122/`。
  **本Partは宣言+scaffold出版まで**。probe実行は本宣言後のセッションが
  最新mainで対抗宣言を確認のうえ着手する。
- キー: Part AS reaudit probe-worklist (sha256 `1c96df05…`) の
  `serving_class == 10661` 行52件 (probe_order 600..651連続・key ids
  **u001..u052**・batch 1-16のid空間と無衝突)。
- machine gates (`scripts/make_batch17_keys.py`・3回実行byte一致・
  batch-keys.json sha256 `db762175…`): canonical BASE `be9cb24e…`
  (6,120行) に0/52 hits、quarantine 0/52、canonical-safe 52/52、
  mask_to_index == s5_index 52/52、全s5_indexがclass 10661のgraph cost子
  (cost 53子中52未確定・graph status unknown(1))、未採用q042 WIN子
  (s5 745184) はキー不在、**batch 1-16 (b/c/d/e/f/g/h/j/m/z/n/p/q/r/t
  計813キー・16ファイルsha固定) と重複0**、Board(11) legal再計算が
  worklist legal 72..97と52/52一致、closure rank 14行とre-derived
  group-best view (809候補) のrank/groups一致。
- 実行protocol (事前登録・実行セッション遵守): pinned replica
  `jsreplay.js` (`84585617…` byte-copy) 2-pass fresh cold・budget
  15M・1 solver/1 row/1 process・publish=ALL・worker最大2・実行前に
  val-gate 4行をhost再現。停止規則: mismatch→HARD-STOP rc=42・
  WIN→HALT rc=45 (WINは誠実ラベルのみ・**本レーンでは採用しない**・
  verdict不消費・scrutiny owner待ち)・枯損→honest UNKNOWN
  (15M同条件再探索禁止)。消費規則: 2-pass LOSS行のみ、後続の別宣言
  adoption Partでsha-pinned fail-closed merger (`90711961…`) 経由で
  canonical計上可。本batch単体では閉鎖・被覆・secured主張なし
  (refresh再実行+独立監査の仕事)。
- verdict不消費: 本Partが消費するverdictはゼロ。canonical cacheは
  6,120行 `be9cb24e…` 不変。15 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/
  r002/q042) はscrutiny owner (C++第二実装 gate pin `9193f5b6…`)
  待ち・不変。
- 標準11×11空盤・19 central-reply roots・class 10661 (unknown 52子)・
  全52キーは本Partのどの時点でもUNKNOWNのまま。nodes数・legal数を勝敗
  として読まない。
- 並走との不接触: batch-17 scopeの対抗宣言がmainにないことはpush直前に
  確認済み (note内の10661言及はすべて候補参照のみ)。同一スコープの
  宣言が既にmainにある場合は本scaffoldを破棄して着手しない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミット
  メッセージに記録 (push直前にnote blob sha1ロック `f34401cd…` を再
  照合し、競合時は再fetchして本節を追記し直す)。

### Part AU status update (2026-11-22, execution host = 本レーンセッション)

宣言 (commit `adc4358a`, scaffold `62b60a07`, note blob sha1ロック
`f34401cd…`) どおり、宣言後の別セッション (本execution host) が最新mainで
対向宣言を確認したうえで batch-17 を実行し、出版まで完了した
(verdict不消費)。

- 実行: pinned replica `jsreplay.js` (`84585617…` byte-copy) 2-pass fresh
  cold・budget 15M・worker最大2 (2-key wave)。**52/52キーすべて LOSS
  (result 2)**・WIN 0・枯損 0・mismatch 0。総ノード数
  **196,536,452/pass** (nodes range 1,651,860 .. 14,967,263。u031は
  14,967,263 nodes で予算直下のLOSS確定)。
- これは完走17バッチ目・clean全LOSSバッチとしては
  23963/10324/8784/10687 に次ぐ**5バッチ目** (クラス10661)。
- val-gate: 実行直前に本hostで4/4 node-exact (at2m 0/2,000,000 ×2・
  15m `(2, 3651923)`/`(2, 5040200)`・禁止四角 95,670)。
- host event (誠実記録): 実行中にsandbox環境リセットが4回発生し、
  書きかけpass 5個 (u017.p2, u018.p2, u027.p2, u031.p2, u033.p2) が
  不完全断片化。完全性ガードが `# replay_done` 不在を検出して
  `output/raw-truncated-hostevent/` に隔離し、該当passをfresh coldで
  再実行。断片はどれもverdict行を持たず、完了済みrowの再探索は一切
  行っていない (batch-16と同種のhost event)。
- row-audit.json (schema
  `n11-centralreply-closure-class10661-batch17-rowaudit-v1`, sha256
  `c19e768f…`): 全52行をrawから機械再検証 (p1==p2 node-exact・budget内・
  result 2・input行照合・status.log照合)。PASS。
- runner差分の開示: `scripts/runbatch.sh` (sha256 `f591f8c2…`) はpublished
  batch-16正本のbyte-copyに、15M枯損行 (jsreplayは枯損時もexit 0) をPASS
  と誤記録しないhonest exhaustionラベル1箇所を加えた (本バッチでは
  枯損0のため未発火)。`scripts/runwave.sh` (`8efd78c2…`) は2-key wave。
  いずれもMANIFEST sha固定。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-class10661-batch17-20261122/`
  を4コミットでmainに反映: commit A `2e035ed7` (observed HEAD
  `c15d4813`、runner scripts + this-host val-gate 8ファイル + 統合status.log)
  / commit B `2266f8c7` (observed HEAD `2e035ed7`、raw u001..u052
  104ファイル) / commit C `54d2b0ee` (observed HEAD `2266f8c7`、
  hostevent断片5ファイル) / commit D `ffc09de1` (observed HEAD
  `54d2b0ee`、row-audit.json + README実行結果節 + MANIFEST-sha256
  177行) = publication complete。**fetch-back 177/177 byte一致**
  (publication commit `ffc09de1` 固定raw URLでMANIFEST全行sha256照合)。
- verdict消費: **ゼロ**。52 LOSS行のcanonical計上は、別宣言のadoption
  Partでsha-pinned fail-closed union merger (`90711961…`) 経由でのみ
  行う (canonical 6,120行 `be9cb24e…` 不変・本batch単体では閉鎖・
  被覆・secured主張なし)。15 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/
  r002/q042) はscrutiny owner (C++第二実装 gate pin `9193f5b6…`) 待ち・
  不変。
- 標準11×11空盤・19 central-reply roots・class 10661 (unknown 52子)・
  全52キーは本Partのどの時点でもUNKNOWNのまま。nodes数・legal数を勝敗
  として読まない。
- 本status updateのobserved HEAD-before-push:
  `ffc09de14d353bb985bdce8d3cad629d5ffc9714` (note blob sha1ロック
  `14794159…` で更新、fetch-backで追記確認)。

## Part AV (adoption, declaration 2026-11-22): batch-17 (class 10661) 52 LOSS行のcanonical計上 + reaudit (実行前に宣言)

Part AU (batch-17 execution, publication complete at `ffc09de1`・root status.log
hygiene除去 `4741a92f`) が出版したprobed 52行のうち、**52 LOSS行 (u001..u052、
WIN-HALT 0・枯損 0・clean全LOSSバッチ)**を、Part AP/AS (batch-16/14
52/41 LOSS行) と同一形式で canonical exact-S5 verdict cache へ計上する。
batch-17にはWIN行もexhaustion行も存在しないため、WIN除外機構と枯損取り扱いは
「不在のgate」として機械検証する (採用増分にWIN行・exhaustion行は1行も含めない)。

- 対象: `research/experiments/n11-centralreply-class10661-loss52-adoption-reaudit-20261122/`。
- 入力はpublished正本のみ: batch-17実験dir (publication commit `ffc09de1`)
  の raws 104 (u001-u052のp1/p2、全行 `# replay_done` 完了)・merged
  `output/status.log` (宣言文+実行記録・sha256 pub MANIFEST固定)・
  batch-keys.json (sha256 `db762175…`)・row-audit.json (`c19e768f…`)・
  hostevent隔離断片5 (verdict行なし)・現行canonical 6,120行cache
  (sha256 `be9cb24e…`)・Part AS reaudit 4出力 (refresh-summary `f2008e70…`・
  closure-classes `3ee1dbb6…`・per-root-coverage `527c7e9a…`・
  probe-worklist `1c96df05…`)。
- maker (Part AS版 `make_increments_batch14.py` をbatch-17にadapt) が
  fail-closed導出: 52 LOSS行の3-way (p1/p2/status.log PASS行) node-exact
  gate・batch-keys legal/(lo,hi) 照合・WIN/exhaustion不在gate・52キーの
  BASE cache不在 (0 hits)・quarantine 0・batch-17全体像 (probed set
  =={u001..u052}、WAVE-END rows、row-audit 52行一致) の機械検証。
- 手法: sha-pinned fail-closed union merger (`90711961…`) でcanonical 6,120行に
  52行をmerge (3回実行・byte一致・WIN/LOSS conflict 0 gate) →
  **canonical 6,172行**を新pathに出版。Part AS refresh script adapt版
  (cache path/sha・文言のみ変更) を2回直列実行・run間byte一致。
  delta extractor (Part AS版 `compare_deltas_batch14_adoption.py` を
  batch-17にadapt: BASE=Part AS reaudit出力、scenario=本reaudit出力) を3回
  実行・byte一致・全gate PASS。
- 主張範囲: canonical cache上の分類のみ。**class 10661 (52子) が採用後に
  free_now (Board検証free class) になるかどうかはreauditの機械計算に委ね、
  宣言時点では断定しない** (52/52の全子LOSS計上後のclass_status遷移は
  refreshが決定する)。本Part単体ではroot被覆・第三手secured・クラス閉鎖の
  主張をしない。
- verdict不消費 (WIN側不変): batch-17にWIN行は存在しない。15 unconsumed
  closure WIN (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/
  r001/r002/q042) は採用判断 scrutiny owner (C++第二実装 gate pin
  `9193f5b6…`) 待ち・不変。
- 標準11×11空盤・19 central-reply roots・class 10661以外の全class・未知の
  全S5子は本Partのどの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。
- 並走との不接触: batch-18の選定・他バッチの宣言・実行は本Partでは行わない。
  published成果への書込みは本Partの新規実験dirのみ。同一スコープの対抗宣言が
  mainに存在する場合は本宣言を破棄して着手しない。
- 本amendment observed HEAD-before-push: `4741a92f` (push直前にnote blob
  sha1 (`e0a4f154…`) を再照合し、競合時は再fetchして本節を追記し直す)。

## Part AW (solver, amendment 2026-11-22): closure class 23101 batch-14 residual 10 keys q043..q052 exact-S5 probe (実行前に宣言・本セッションが実行host・verdict不消費)

batch 14 (Part AQ takeover) は事前登録のWIN-HALT規則により q042 (2-pass
node-exact result 1, 9,149,084 nodes) で停止し、残10キー q043..q052 は
未着手のまま残った (Part AT/AS/AU resumeのopen item)。Part AS計上後の
class 23101はcanonical上unknown 11子 = 未採用q042 WIN + 未着手10キー
(s5_index 745455..745465のうち10個・published batch-14 batch-keys.jsonの
probe_order 580..589)。本Partはこの残10キーの列挙probeを実行前に単一
オーナーとして宣言する。

- 対象: `research/experiments/n11-centralreply-closure-class23101-batch14-residual-20261122/`。
- キー: published batch-14 batch-keys.json (sha256 `dfde0e90…`) の
  q043..q052。input CSVはpublished正本のbyte-copy (batch-14 publication
  commit `7b211d38`のMANIFEST sha固定・10/10のsha256一致をmakerが検証)。
- machine gates (maker fail-closed): 現行canonical 6,120行 (sha256
  `be9cb24e…`) に10キー不在 (0/10 hits)・quarantine registry (sha256
  `81d23160…`) 0/10・batch-17 batch-keys (sha256 `db762175…`) との
  s5_index交積0・published batch-14 status.log/row-auditのprobed set ==
  {q001..q042} で残キー集合がpublished key集合のちょうど補集合
  {q043..q052}。
- 手法: pinned replica `jsreplay.js` (sha256 `84585617…` byte-copy) による
  2-pass fresh cold replay・budget 15,000,000・1 solver / 1 row / 1
  process・publish=ALL・worker最大2 (2-key wave)。実行前にpublished
  two-target-design 4行のval-gateを本hostで再現 (node数一致が必須)。
- 停止規則 (事前登録。batch-14/16/17からの差分はWIN行の扱いのみ):
  1. determinism mismatch → 即時HARD-STOP (rc=42)、以後のキー着手不可。
  2. budget枯損 (result 0) → honest UNKNOWN。15M同条件の再探索は禁止。
     次ラダー (budget昇格) は将来の新規宣言が必要。
  3. WIN (result 1) → **HALTせず続行する** (publish=ALL・誠実WINラベル
     WIN-CONTINUE・verdict不消費)。理由: class 23101の全子LOSS閉包
     ルートはq042 WINで既に反駁済み (route statement) なのでWIN-HALTは
     新しいルート情報を買わず、残キー集合の全列挙がWIN/LOSSいずれの
     分岐でもclass 23101のunknown子数を最小化するから。2-pass
     node-exactのWIN行は16番目以降のunconsumed closure WIN候補として
     誠実記録され、採用判断は引き続きscrutiny owner (C++第二実装 gate
     pin `9193f5b6…`) 待ち。
- 消費規則: 本Partのverdict消費はゼロ。LOSS行のcanonical計上は別宣言の
  adoption Part (Part AS/AV流・sha-pinned fail-closed merger `90711961…`
  経由) が行う。そのadoption PartのBASEはPart AVが計上するcanonical
  6,172行 (batch-17計上後) を用いる (本PartはPart AVの成果物には一切
  触れない・非接触)。
- 本Part単体ではroot被覆・クラス閉鎖・第三手securedの主張をしない
  (閉鎖判定・被覆監査は後続のrefresh再実行+独立監査の仕事)。
- verdict不消費 (WIN側不変): 本Part実行開始時点の15 unconsumed closure
  WIN (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/
  r001/r002/q042) はscrutiny owner待ち・本Partでは採用も却下もしない。
- 標準11×11空盤・19 central-reply roots・class 23101 (unknown 11子)・
  10キーは本Partのどの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。
- 並走との不接触: Part AV (batch-17 class 10661 adoption+reaudit、宣言
  commit `340abef3`) とは非接触 (本Partはbatch-14由来キーのみを対象とし、
  batch-17成果物・canonical cache・refresh出力に一切書込まない)。
  同一スコープの対抗宣言がmainに存在する場合は本宣言を破棄して着手しない。
- 本amendment observed HEAD-before-push: `3542315d` (push直前にnoteの
  blob sha1ロックを再照合し、競合時は再fetchして本節を追記し直す)。

### Part AW status update (2026-11-22, execution host = 本レーンセッション)

宣言 (commit `da131f10`) どおり、宣言後に本実行hostが最新mainで対抗宣言を確認
したうえで batch-14 residual 10キーを実行し、出版まで完了した (verdict不消費)。

- 実行: pinned replica `jsreplay.js` (`84585617…` byte-copy) 2-pass fresh
  cold・budget 15M・worker最大2。**10/10キーすべて LOSS (result 2)**・WIN 0・
  枯損 0・mismatch 0。総ノード数 **23,252,550/pass** (range 557,594 .. 8,353,244・
  最大はq049 8,353,244)。事前登録どおりWIN行はWIN-CONTINUE誠実ラベルで
  継続のはずだったが、WINは一堂に出現せず (WIN 0)。
- 誠実記録: 実行は`runbatch.sh`を2-key並列foregroundで運転した (`runwave.sh`
  wrapperは同protocolのまま本バッチサイズでは不要・status.log RUNNER-NOTE行と
  READMEに開示)。
- val-gate: 実行直前に本hostで4/4 node-exact (at2m 0/2,000,000 ×2・15m
  `(2, 3651923)`/`(2, 5040200)`・禁止四角 95,670)。host interruptionなし
  (truncated pass 0)。
- maker gates: `make_residual_keys.py` G1-G7全PASS・3回実行byte一致
  (canonical 6,120行 `be9cb24e…` 0/10 hits・quarantine `81d23160…` 0/10・
  batch-17 batch-keys `db762175…` とのs5_index交積0・published batch-14
  row-audit `cc22a1c8…` の unprobed_keys == {q043..q052} 機械一致)。
- runner差分の開示: `runbatch.sh` (sha256 `989e359c…`) はpublished batch-17
  正本 (`f591f8c2…`) からWIN時のHALT exit 45を誠実WIN-CONTINUEラベル+
  継続に置き換えたPart AW宣言済み差分のみ・`runwave.sh` (`885830d0…`) は
  done-setにWIN-CONTINUEを追加した同差分のみ。`jsreplay.js`はbyte同一
  (`84585617…`)。いずれもMANIFEST sha固定。
- row-audit.json (schema `n11-centralreply-closure-class23101-batch14residual-
  rowaudit-v1`, sha256 `6b40b131…`): 全10行をrawから機械再検証 (p1==p2
  node-exact・budget内・result 2・input/batch-keys/status.log照合・全pass
  `# replay_done` 完了) PASS・3回実行byte一致。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-class23101-batch14-residual-20261122/`
  48ファイルを3コミットでmainに反映: commit A `a5b514d7` (scaffold:
  runner scripts + maker + inputs + 本host val-gate + 統合status.log) /
  commit B `ecfe258d` (raw q043..q052 20ファイル) / commit C `cb94f808`
  (row-audit.json + README + MANIFEST-sha256 48行) = publication complete。
  **fetch-back全byte一致** (publication commit `cb94f808` 固定rawでMANIFEST
  全行sha256照合48/48)。
- verdict消費: **ゼロ**。batch-14キー集合 (class 23101費用子52中、未着手
  だった残10キー) の列挙は本laneの証拠上これで完結 (Part AQ 42行 + 本Part
  10行)。10 LOSS行のcanonical計上は別宣言のadoption Partが行う (**BASEは
  Part AV計上後のcanonical 6,172行**・sha-pinned fail-closed merger
  `90711961…` 経由・Part AV出版後に着手可能)。そのadoption Part完了後、
  class 23101のcanonical上unknown費用子は未採用q042 WIN 1子のみになる
  見込み (route statement・閉鎖・被覆主張ではない)。q042採用判断は引き続き
  scrutiny owner (C++第二実装 gate pin `9193f5b6…`) 待ち。
- 標準11×11空盤・19 central-reply roots・class 23101 (現行canonical
  6,120行上unknown 11子)・10キーは本Partのどの時点でもUNKNOWNのまま。
  nodes数を勝敗として読まない。

## Part AX (verifier, amendment 2026-11-22): batch-14 residual (class 23101) q043..q052 + batch-17 (class 10661) budget-edge 3行の第三実装交叉検証 (実行前に宣言・verdict不消費)

単一オーナー宣言 (Part G/K/O/P/T/W/AA/AD/AG/AL/AR流 third-implementation
cross-verification)。Part AW (batch-14 residual 10キー) とbatch-17 (Part AU)
の計上対象行うち計算量上位のエッジ行を、pinned第三実装
(non-df-pn AND/OR minimax `third_impl.js`, sha256 `08ea958f…`) で
verdict-level再検証し、literature側の追加独立証拠とする。**verdict不消費**
(採用判断はscrutiny owner C++第二実装 gate pin `9193f5b6…`のまま)。

- 対象13行 (すべてpublished 2-pass fresh-cold node-exact・result 2 LOSS・
  budget 15,000,000内):
  - Part AW正本 (publication commit `cb94f808`, 実験dir
    `n11-centralreply-closure-class23101-batch14-residual-20261122/`):
    q043 (2,573,254) / q044 (1,855,550) / q045 (1,028,674) / q046 (1,101,099) /
    q047 (557,594) / q048 (2,860,377) / q049 (8,353,244) / q050 (2,178,945) /
    q051 (1,451,266) / q052 (1,292,547)。
  - batch-17正本 (publication commit `ffc09de1`, 実験dir
    `n11-centralreply-closure-class10661-batch17-20261122/`) のエッジ3行:
    **u031 (14,967,263 nodes・予算直下のmax-nodes行・後述のP2 retryを含む)** /
    u033 (7,806,486・P2 retry) / u038 (6,589,964)。いずれもPart AV
    (batch-17 class 10661 52-LOSS adoption+reaudit) の計上対象行集合の要素
    であり、本PartはPart AVの実行・出版・reaudit成果物には一切触れない
    (verdict-level literatureのみ・非接触)。
- 入力は機械導出のみ (`scripts/make_inputs_ax.py`, Part AR makerのadapt):
  published raws (q 20ファイル + u 6ファイル) の2-pass node-exact /
  `# replay_done` / budget内 / result 2 / legal・lo・hi照合・published
  row-audit (`6b40b131…` / `c19e768f…`) の行表との機械一致・published
  status.logのPASS行照合 (AW: 10 PASS全result 2・VAL-GATE 4/4・
  WAVE-END stop=0。b17: EXECUTION-COMPLETE 52/52 LOSS・u031/u033
  P2-TRUNCATED-RETRY誠実行5件のうちu031/u033を含む・fired HARD-STOP 0)・
  batch-keys (b14 `dfde0e90…` 52キー / b17 `db762175…` 52キー) の
  probe_order照合 (q043..q052 = 580..589連続・u031/u033/u038 =
  630/632/637)・derived-vs-published input CSV byte-equality (13 target +
  2 anchor + 2 negative、anchor/negativeはpublished Part AR実験dirの
  CSVとbyte一致)。3回実行・byte一致。
- anchors (published第三実装値を本hostで再現): k02a WIN (legal 87)
  9,106,337 expansions / 4,991,527 ttHits、l1a LOSS (legal 116)
  7,660,602 / 3,951,175。negatives (fail-closed必須): ng1 = k02 legal+1、
  ng2 = k02 stones 6。
- method: 1 row = 1 solver = 1 process、cap 300,000,000拡張、wallcap 240s、
  `--memo-power=22`、各target/anchor 2回 (a/b) determinism gate。
  rules engine gate: `verify_tbl.js` replica quads 95,670 == third-impl
  quads 95,670・195,044 triples mismatch 0。audit battery `audit.py`
  (schema `n11-centralreply-closure-b14res-b17edge-thirdimpl-audit-v1`)
  2回実行byte一致。
- 事前登録の誠実ラベリング: third-impl verdictがpublished replica
  (expected 2)と一致せずcleanで終わった場合は**DIVERGENCE**として記録
  (agree gate FAIL・隠さない)。wall (240s)到達で終了した行は
  **WALL-INCONCLUSIVE** (verdictではない)。いずれの場合もverdict消費・
  canonical更新は行わない。
- host: Part AWと同一sandbox host (2 cores、solver最大2並列)。
  本Partは単一host内のcross-implementation corroboration (Part ARは
  cross-host + cross-implementation。どちらもliterature)。
- 消費規則: 本Partのverdict消費はゼロ。canonical cache (6,120行
  `be9cb24e…`・Part AV出版後は6,172行) には書込まない。15 unconsumed
  closure WIN (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/
  p003/r001/r002/q042) は採用判断 scrutiny owner 待ち・不変。
- 本Part単体ではroot被覆・クラス閉鎖・第三手securedの主張をしない。
- 標準11×11空盤・19 central-reply roots・class 23101・class 10661・
  全13キーは本Partのどの時点でもUNKNOWNのまま。nodes数・expansions数を
  勝敗として読まない。
- 対抗宣言チェック: observed HEAD `29897108` 時点で同一スコープ
  (batch-14 residual / batch-17 edge rowsの第三実装交叉検証) の対抗宣言は
  mainに存在しない (直近commit列挙と本noteのgrepで確認)。push直前にnote
  blob sha1ロックを再照合し、競合時は再fetchして本節を追記し直す。

## Part AY (solver-declaration + scaffold, declaration 2026-11-22): closure class 16131 exact-S5 probe batch 18 (実行前に宣言・本Partはscaffold出版まで・verdict不消費)

**base独立性**を明記した上でbatch 18を宣言する。本宣言の正本baseは
**published** canonical exact-S5 verdict cache (6,120行, sha256 `be9cb24e…`,
Part AS adoption出力・main上の正本)。Part AV (batch-17 class 10661
52-LOSS adoption + reaudit, 宣言 `340abef3` 19:20:42Z, 本宣言時点でmain未出版)
の成果物には一切依存しない・読まない・書かない。機械事実: batch-17キーは
class 10661の費用子でありclass 16131の費用子と交わらないため、
**class 16131のunknown費用子53件はpublished base (6,120行) とPost-AV base
(6,172行) のどちらでも同一集合として定まる** (本レーンの機械導出で両方向を照合)。

- 選定: published base再導出closure候補表 (809候補) のrank 1-13 (23101,
  16757, 20421, 16371, 30345, 12264, 5473, 2634, 8785, 1518, 8106, 16930,
  5830) はいずれも再導出unknown費用子と15 unconsumed closure WIN子の交差が
  非空で全LOSS閉包ルート反駁済み (route statement。class 23101の残10キー
  q043-q052はPart AW (batch-14 residual) で列挙probe済み・adoption待ち)。
  rank 14 (class 10661) はWIN交差をもたないが52 unknown子すべてがpublished
  batch-17 packetでprobe済み (52/52 two-pass LOSS・adoptionは別宣言Part AV
  が保留中・同budgetの再probeは規則上禁止・着手対象として空)。
  **rank 15 class 16131 (mask `[1154047404513693696, 64]`・unknown_now 53子・
  graph cost 53子すべて未確定・closure groups (12,50)+(12,70)+(48,20)+
  (48,72)+(48,100)・機械再計算一致) が反駁証拠がなく・既probe子を持たない
  最初の候補**。次点はrank 16 class 16513 (unknown 53)。
- 対象: `research/experiments/n11-centralreply-closure-class16131-batch18-20261122/`。
  **本Partは宣言+scaffold出版まで**。probe実行は本宣言後のセッション (本セッションを
  含む) が最新mainで対抗宣言を確認のうえ着手する。
- キー: published canonical base (6,120行・sha `be9cb24e…` 固定) + pinned graph
  + update8 receipts による機械再導出 (graph cost子 ∩ canonical不在の53件、
  s5_index升順にkey ids **v001..v053**、batch 1-18のid空間と無衝突、worklist転写ゼロ)。
  本レーンはAV reaudit worklist由来キー (probe_order 600..652) との機械照合も
  済み (key_id→(lo,hi,s5,legal,membership) 53/53同一)。
- machine gates (`scripts/make_batch18_keys.py`・3回実行byte一致・全出力re-read
  durability gate込み): canonical BASEに0/53 hits、quarantine 0/53、
  canonical-safe 53/53、mask_to_index == 導出s5_index 53/53、全s5_indexが
  class 16131のgraph cost子、**15 unconsumed closure WIN子はキー不在 (全15子を
  published batch packetから再導出・graph mask_to_indexで照合・canonical不在も
  gate)**、**batch 1-17 + batch-14 residual (18 packet・計875行・sha固定) と重複0**
  (cross-packet共有位置簿認)、Board(11) legal再導出53/53 (legal 74..97・値は
  Board再導出であってworklist転写ではない)、membership_class_countもgraph cost
  関係から再導出53/53、再導出closure表 (809候補) のrank 1..16表・rank14完全probe
  gate・rank 15 = 16131のrank/groups一致。
- 実行protocol (事前登録・実行セッション遵守): pinned replica `jsreplay.js`
  (`84585617…` byte-copy) 2-pass fresh cold・budget 15M・1 solver/1 row/1 process・
  publish=ALL・worker最大2・実行前にval-gate 4行をhost再現。停止規則:
  mismatch→HARD-STOP rc=42・WIN→HALT rc=45 (WINは誠実ラベルのみ・**本レーンでは
  採用しない**・verdict不消費・scrutiny owner待ち)・枯損→honest UNKNOWN
  (15M同条件再探索禁止)。消費規則: 2-pass LOSS行のみ、後続の別宣言adoption Partで
  sha-pinned fail-closed merger (`90711961…`) 経由でのみ行う (canonical cacheは
  本batch単体では不変・閉鎖・被覆・secured主張なし)。15 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042) は
  scrutiny owner (C++第二実装 gate pin `9193f5b6…`) 待ち・不変。
- 標準11×11空盤・19 central-reply roots・class 16131 (unknown 53子)・全53キーは
  本Partのどの時点でもUNKNOWNのまま。nodes数・legal数を勝敗として読まない。
- 併走との不接触: Part AV (batch-17 adoption) が出版/接管いずれになった場合も
  本Partのキー集合・gateは不変 (base独立性)。Part AX (batch-14 residual +
  batch-17 edge行の第三実装交差検証) ともスコープ非接触 (対象行集合が異なる)。
  他レーン (y13/y14 two-token・K1058系) とは無接触。同一スコープの対抗宣言がmainに
  存在する場合は本宣言を破棄して着手しない。
- 本amendment observed HEAD-before-push: `0c9707ad3525674070d3ea7f287f2fd5f91fc826` (push直前にnote blob
  sha1ロックを再照合し、競合時は再fetchして本節を追記し直す)。

### Part AX status update (2026-11-22, execution host = 本レーン continuing session)

宣言 (commit `9771aa5b`) どおり、宣言後に本hostが対象13行をpinned第三実装で解き、
出版まで完了した (verdict不消費)。Part AY (batch-18 class 16131、宣言 `6cde1b0`)
は本Partの後 declaration されたが、両宣言どおりスコープ非接触を確認済み
(対象行集合が異なる・本Partはbatch-17/batch-14 published rowにのみ依存)。

- 実行: pinned `third_impl.js` (`08ea958f…`)・1 row = 1 solver = 1 process・
  cap 300,000,000拡張・wallcap 240s・`--memo-power=22`・全target/anchor 2回 (a/b)。
  **13/13 target すべて clean LOSS (result 2)** で、published replica verdict
  と13/13一致 (Part AW q043..q052 10行 + batch-17 budget-edge u031/u033/u038 3行・
  u031はbudget直下14,967,263 nodes行の第三実装再現)。a/b pair全員
  result/expansion/ttHits/reason同一 (determinism gate PASS)。総expansions
  60,628,197/pass (range 611,783 q047 .. 17,661,456 u031)。WIN 0・
  WALL-INCONCLUSIVE 0・DIVERGENCE 0。
- anchors: k02a WIN (9,106,337 expansions / 4,991,527 ttHits)・l1a LOSS
  (7,660,602 / 3,951,175) ともpublished第三実装値に本hostで完全一致
  (a/b含む全起動で決定性フィールド同一)。negatives ng1/ng2は設計どおり
  fail-closed文言でGATE_FAIL。
- rules gate: verify_tbl replica quads 95,670 == third-impl quads 95,670・
  195,044 triples mismatch 0。
- maker: `make_inputs_ax.py` 全gate PASS・3回実行byte一致 (source pins:
  batch-keys `dfde0e90`/`db762175`・row-audit `6b40b131`/`c19e768f`・
  raw 26ファイルの2-pass node-exact + `# replay_done` + budget内 result 2・
  status.log PASS 3-way (AW: 10 PASS全result 2 + VAL-GATE 4/4 + WAVE-END
  stop=0。b17: EXECUTION-COMPLETE 52/52 LOSS + P2-TRUNCATED-RETRY 5件中
  u031/u033を含む・fired HARD-STOP 0)・probe_order 580..589 / 630/632/637・
  derived-vs-published input CSV byte-equality 10+3 target + 4 anchor/negative
  (anchor/negativeはpublished Part AR実験dirのCSVとbyte一致))。
- audit: `audit.py` **163/163 gates PASS**・2回実行byte一致 (schema
  `n11-centralreply-closure-b14res-b17edge-thirdimpl-audit-v1`, sha256
  `d1fc8999…`。G0 input CSV vs rows.json 17・script pins・rules gate・
  anchors a/b node-exact・negatives fail-closed・targets 13行 a/b determinism
  + verdict agreement)。
- 誠実記録 (status.log RUNNER-NOTE + READMEに開示): (1) anchors初回起動時の
  shell cwd groupingバグで k02a tag=a のみ単独起動した (RUN行重複・
  決定性フィールドは同一・k02a.bは未起動・絶対パスで即時再実行して現行a/bで
  上書き・Part ARのng1前例と同種)。(2) 2 solver並列時にhost CPU quotaで
  per-solver速度が半減する観測 (k02a solo wall 25.63s vs pair 53.03s) を受けて
  targetsは逐次実行 (1 solver逐次・宣言cap「最大2」以内・決定性フィールドは
  wall非依存)。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-b14res-b17edge-thirdimpl-20261122/`
  113ファイル+MANIFESTを5コミットでmainに反映: commit A `dbab0b9b`
  (scaffold: scripts pins + maker + audit.py + inputs 24ファイル) /
  A2 `b2867591` (source raws 26ファイル) / A3 `b826eebc` (sources rest 25
  ファイル) / B `db036985` (solver outputs 34ファイル: targets a/b 26・
  anchors 4・negative 2・rules-gate・status.log) / C `115c7ad3`
  (audit-summary + audit-run1/2 + README + MANIFEST 113行) = publication
  complete。**fetch-back全sha一致** (publication commit `115c7ad3` 固定rawで
  MANIFEST全行sha256照合113/113)。
- 意味 (route statement・閉鎖主張なし): batch-14 residual 10行 (Part AW) と
  batch-17 budget-edge 3行 (Part AU) が独立実装でも13/13 LOSSで再現された。
  これらはverdict-level補強文献であり、**verdict消費ゼロ**・Part AV
  (batch-17 adoption) と将来のclass 23101 residual LOSS adoption Partの採用判断
  は一切代行しない (scrutiny owner C++第二実装 gate pin `9193f5b6…`のまま)。
- 標準11×11空盤・19 central-reply roots・class 23101・class 10661・全13キーは
  本Partのどの時点でもUNKNOWNのまま。nodes数・expansions数を勝敗として読まない。

### Part AY status update (2026-11-22, execution host = 本レーンセッション)

宣言 (commit `6cde1b0b`) どおり、宣言後に本実行hostが最新mainで対抗宣言を確認
したうえで batch-18 (class 16131) を実行し、WIN-HALT時点まで出版した
(verdict不消費)。

- 実行: pinned replica `jsreplay.js` (`84585617…` byte-copy) 2-pass fresh
  cold・budget 15M・worker最大2 (published `runbatch.sh` (`f591f8c2…`) を
  2並列instanceで運転・status.log RUNNER-NOTE行とREADMEに開示)。
  最初のwaveで両workerの最初のキーがいずれも**WIN (result 1)**:
  **v001 (2-pass node-exact 5,656,151 nodes・legal 83・keys
  1154610354467115008/64)** と **v002 (7,898,204 nodes・legal 84・keys
  3459890413727387648/64)**。事前登録のWIN-HALT (rc=45) が発火しbatch停止。
  **51キーは未着手fresh** (一度も実行されておらず、15M再探索禁止規則に
  該当しない)。
- val-gate: 実行直前に本hostで4/4 node-exact再現 (at2m 0/2,000,000 x2・
  15m (2,3,651,923)/(2,5,040,200)・禁止四角95,670)。truncated pass 0。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-class16131-batch18-20261122/`:
  scaffold 70ファイル (commit `c36825c7`、53 CSV + batch-keys `1bb3ed41…` +
  scripts 5 + val-gate 8 + README + status.log header + MANIFEST) /
  raw 4ファイル + status.log (commit `3c07f51a`) / README結果節 +
  MANIFEST 73行 (commit `938e34f2`) = publication complete。
  **fetch-back byte一致 9/9** (raws 4 + status.log + README + MANIFEST +
  batch-keys + jsreplay + 一部CSV相当の内容照合)。
- verdict消費: **ゼロ**。unconsumed closure WIN候補は**17**
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/
  r002/q042 + **v001 + v002**)、すべてscrutiny owner (C++第二実装 gate
  pin `9193f5b6…`) 待ち。**v001/v002は本レーンでは採用しない。**
- route statement (条件付き・verdictではない): class 16131の費用子に
  WINが1つでも採用されれば、class 16131の全子LOSS閉包ルートは反駁される
  (16131は既probeのない最初のclean候補だったrank 15であり、rank 16
  class 16513が現行の次点clean候補)。**class 16131 (残51子)・次点候補・
  標準11×11空盤・19 central-reply rootsは本時点でUNKNOWNのまま。**
  nodes数を勝敗として読まない。
- 残51キーの列挙継続は将来の別宣言Partが行う。row-auditはbatch完走時点
  (`scripts/row_audit_batch18.py`) に全行機械検証する (現時点の2 WIN行は
  grepベース機械検証済み: p1==p2 node-exact・budget内・`# replay_done`・
  status.log整合)。


## Part AZ (verifier, declaration 2026-11-22): batch-18 closure WIN rows v001/v002 third-implementation cross-verification (宣言後に実行・verdict不消費)

batch 18 (Part AY, class 16131) は宣言どおりの実行で最初のwaveが両workerとも
WIN (result 1) に終わり、事前登録のWIN-HALT規則で停止した (**v001 WIN
5,656,151 nodes** / **v002 WIN 7,898,204 nodes**、いずれも2-pass fresh-cold
node-exact・budget 15M内・raws+status.log出版済み・publication commit
`938e34f2`)。これによりunconsumed closure WIN候補は17になった。前例
(Part G: closure WINs b018/d002/e002/f017 の第三実装再検証、および
Part K/O/P/T/W/AA/AD/AG/AL/AR のverifier battery约定) に従い、
**採用判断待ちのWIN行に第三実装verdict-level交叉検証の文献を追加する**。
verdict不消費・採用判断は引き続きscrutiny owner (C++第二実装 gate pin
`9193f5b6…`)。

- 対象: `research/experiments/n11-centralreply-closure-b18win-thirdimpl-20261122/`。
  published batch-18の2 WIN行 (v001/v002) の全行再検証 + Part G/ARと同一の
  anchor行 (k02a/l1a)・negative gate 2種 (ng1/ng2)・rules gate (verify_tbl
  quads 95,670 == third-impl・triples mismatch 0)。
- 入力: published batch-18 artifacts (publication commit `938e34f2`・
  MANIFEST 73行) から `scripts/make_inputs_az.py` で機械導出 (fail-closed・
  手転写ゼロ): batch-keys `1bb3ed41…` pin (53キー・class 16131・
  v001 s5 153671 / v002 s5 207534)、raw 4ファイルの2-pass node-exact +
  `# replay_done` + result 1 in-budget、status.logのPASS行・WIN-ROW-DETAIL行・
  WIN-HALT行との3-way一致、published input CSV (v001/v002) byte-equality、
  anchor/negative input CSVはpublished Part AR実験dirのCSVとbyte一致。
- 手法: pinned `third_impl.js` (`08ea958f…`)・1行=1 solver=1 process・
  cap 300,000,000拡張・wallcap 240s・`--memo-power=22`・全target/anchor
  a/b 2回のdeterminism gate (result/expansion/ttHits/reason同一必須)。
  wall到達 (240s) はhonest WALL-INCONCLUSIVE・clean不一致はDIVERGENCE
  として記録 (verdict書換え・隠蔽なし。anchorsのDOC/decision文言と同式)。
- 停止・消費規則: 本Partのverdict消費はゼロ。canonical cache (6,120行
  `be9cb24e…`・Part AV出版後は6,172行) に書込まない。17 unconsumed
  closure WIN候補 (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/
  p002/p003/r001/r002/q042/v001/v002) は採用判断scrutiny owner待ち・不変。
  本Part単体ではroot被覆・クラス閉鎖・第三手securedの主張をしない。
- 並走との不接触: 本Partはpublished batch-18 raw (AYの成果物) の読み取り
  のみで、AY宣言の残51キー (v003..v053) には一切触れない (15M再探索禁止
  規則にも触れない)。Part AV (batch-17 adoption, 宣言 `340abef3`,
  in flight) の成果物にも読み書きしない。AYレーンのbatch-18 continuation
  またはbatch-19 (class 16513) pivotの選択を本Partは妨げない。
  同一スコープ (batch-18 WIN行の第三実装交叉検証) の対抗宣言がmainに
  存在する場合は本宣言を破棄して着手しない。
- 標準11×11空盤・19 central-reply roots・class 16131 (残51子)・全53キーは
  本Partのどの時点でもUNKNOWNのまま。nodes数・expansions数を勝敗として
  読まない。
- 本amendment observed HEAD-before-push: 実行時の最新mainを
  コミットメッセージに記録する。push直前にnote blob sha1ロックを再照合し、
  競合時は再fetchして本節を追記し直す。

### Part AZ status update (2026-11-22, execution host = 本レーン continuing session)

宣言 (note amendment commit `a5ea2aa0`) どおり、宣言後に本hostが
published batch-18 WIN行 v001/v002をpinned第三実装で解き、出版まで完了した
(verdict不消費)。

- 実行: pinned `third_impl.js` (`08ea958f…`)・1行=1 solver=1 process・
  cap 300,000,000・wallcap 240s・`--memo-power=22`・全target/anchor
  a/b 2回。**targets 2/2 clean WIN (result 1)・replica verdict一致2/2**:
  **v001 WIN 6,558,484 expansions / 3,610,051 ttHits** (replica 5,656,151
  nodes・ratio 1.16)・**v002 WIN 9,204,329 / 5,027,672** (replica 7,898,204・
  ratio 1.17)。a/b pair全員result/expansion/ttHits/reason同一
  (determinism gate PASS)。総expansions 15,762,813/pass。
  LOSS 0・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
- battery順序 (RUNNER-NOTE開示どおり): negatives ng1/ng2が設計どおり
  fail-closed文言 (GATE_FAIL) → anchors k02a WIN 9,106,337/4,991,527・
  l1a LOSS 7,660,602/3,951,175 がpublished第三実装値にnode-exact再現
  (a/b同一) → targets逐次実行 (Part AXのCPU quota半減観測を継承し
  全行程逐次)。
- rules gate: verify_tbl replica quads 95,670 == third-impl quads 95,670・
  195,044 triples mismatch 0 (`output/rules-gate.txt`)。
- maker `make_inputs_az.py`: 全gate PASS・3回実行byte一致 (source pins:
  batch-18 batch-keys `1bb3ed41…` (53キー・class 16131・v001 s5 153671/
  v002 s5 207534/membership 2/3)・raw 4ファイル (published MANIFEST pins
  `24b45c8a`/`1fc367bd`/`41c10ec2`/`e9f578fc`)の2-pass node-exact + `# replay_done` + result 1 in-budget・status-b18.log `4b785add`の
  PASS行・WIN-HALT行・WIN-ROW-DETAIL行・VAL-GATE 4/4行・EXECUTION-HALTED行・
  51-unprobed行・17候補行の3-way一致・README `8b6a85b3`結果節照合・
  derived-vs-published input CSV byte-equality 2 target (`edee9be8`/
  `e8bbbaed`) + 4 anchor/negative (published Part AR CSVとbyte一致))。
- audit `audit.py`: **53/53 gates PASS**・2回実行byte一致 (schema
  `n11-centralreply-closure-b18win-thirdimpl-audit-v1`)。verdict
  agreements 2/2 (WIN=2)・inconclusive 0。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-b18win-thirdimpl-20261122/`
  43ファイル+MANIFESTを3コミットでmainに反映: A `2e6d14ee` (scaffold:
  scripts 6 + inputs 7 + sources 14) / B `9a997c21` (solver outputs 15:
  targets a/b 4・anchors 4・negative 2・rules-gate・status.log・
  audit-summary・audit-run1/2) / C `2f944d5d` (README + MANIFEST-sha256
  43行) = publication complete。**fetch-back 43/43 sha一致**
  (publication commit `2f944d5d` 固定rawでMANIFEST全行sha256照合)。
- 意味 (route statement・閉鎖主張なし): batch-18最初のwaveの2 WIN
  (v001/v002) が独立実装でもclean WINで再現された。verdict-level補強
  文献であり、**verdict消費ゼロ**・17 unconsumed closure WIN候補の採用
  判断は一切代行しない (scrutiny owner C++第二実装 gate pin `9193f5b6…`
  のまま)。canonical cache (6,120行 `be9cb24e…`) 不変・書込むいかなる
  cacheにも書込んでいない。AY宣言の残51キー (v003..v053・fresh) と
  Part AV (batch-17 adoption・in flight) には一切触れていない。
- 標準11×11空盤・19 central-reply roots・class 16131 (残51子)・全53キーは
  本Partのどの時点でもUNKNOWNのまま。nodes数・expansions数を勝敗として
  読まない。

## Part BA (verifier, declaration 2026-11-22): batch-18 closure WIN行 v001/v002 のif-adopted分解 (scrutiny owner向け事前計算・verdict不消費・実行前に宣言)

batch-18 (Part AY, class 16131) の最初のwaveで両worker WIN (v001 5,656,151
nodes / v002 7,898,204 nodes, 2-pass fresh-cold node-exact, 第三実装一致済み
(Part AZ, publication commit `2f944d5d`), batch-18 publication commit
`938e34f2`) により、unconsumed closure WIN候補は17になった。17候補のうち
15 (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/
r002/q042) は既存のif-adopted分解 (Part V/R/AB/AH/AI/AN/AO/AT等) を持つが、
**v001/v002はいまだif-adopted分解をもたない (機械可測のギャップ)**。採用判断
scrutiny owner (C++第二実装 gate pin `9193f5b6…`) のためのif-adopted分解を
双WIN precedent (p002p003/r001r002/n005n006) と同一形式で実行する。
**verdict不消費・本Partは採用を推奨も却下もしない・if-adopted投影を勝敗や
閉鎖主張として読まない。**

- 対象: `research/experiments/n11-centralreply-class16131-win-v001v002-ifadopted-20261122/`。
- BASE = 現行canonical 6,120行 (sha256 `be9cb24e…`, Part AS publication
  commit `8c42e44c` の `n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/`)。
  v001/v002のkeyはBASEに不在 (batch-18 makerのcanonical 0/53 gate済み)。
  Part AV (batch-17 adoption, 宣言 `340abef3`, in flight) の成果物は読み書き
  ともしない (Part ATと同様、BASE 6,120を凍結BASEとする非正典projectionで
  あることを明記)。
- 増分 = 双WIN行 v001 (s5_index 153671, key `[1154610354467115008, 64]`,
  legal 83, nodes 5,656,151) + v002 (s5_index 207534, key
  `[3459890413727387648, 64]`, legal 84, nodes 7,898,204) (published
  batch-18 raws 4ファイル `24b45c8a`/`1fc367bd`/`41c10ec2`/`e9f578fc`,
  publication commit `938e34f2`; maker `make_increment_v001v002_win.py`
  (Part AT版 `622ba795…` のadapt) が2-pass node-exact (result 1, nodes
  両pass一致) をrawから機械検証し、status.log (`4b785add…`) のPASS行・
  WIN-HALT行・WIN-ROW-DETAIL行・EXECUTION-HALTED行との3-way一致、
  batch-keys (`1bb3ed41…`) のlegal/(lo,hi)/s5_index一致、BASE不在 (6,120行)・
  quarantine不在・canonical-safe形式をgateしてから2行incrementを導出)。
- 手法: sha-pinned fail-closed union merger (`90711961…`, byte-copy pin)
  2回実行・byte一致 → **if-adopted cache 6,122行** (WIN 160 / LOSS 5,962・
  canonicalではなく投影)。merge後にBASE cache `be9cb24e…` byte不変を再検証。
  refresh script adapt版 `reaudit/scripts/refresh_v001v002_ifadopted.py`
  (Part AT版 `5f9810e6…` からcache path/sha・文言のみのadapt・sha期待値は
  cache自体から機械抽出) を2回直列実行・run間byte一致。delta extractor
  `compare_deltas_v001v002_ifadopted.py` (Part AT版 `207cfbcc…` を双WIN
  if-adopted用にadapt: flips == s5 153671/207534をcost childとして持つ
  unknown保持クラスの機械計算集合 (graph由来・hardcodeなし)、pure WIN採用の
  newly-free-classes空、per-root free/uncovered変更行0、class 16131 flip含有 +
  scenario-unknown 53→51、double-flipクラス (両WINをcost childにもつ) の
  台帳記録、update8 win_hit_groups変化の機械抽出、canonical BASE sha pin・
  BASE index_verdict不在gate、raw 2-pass再検証、manifest gate) を2回実行・
  byte一致・全gate PASS。
- 事前予想 (機械検証可能な範囲で事前登録・外れたら実測を優先して原因を記録):
  BASE (Part AS reaudit正本) のclass_status_counts/free_now/per-root coverage
  は本Partの再計算と完全一致しなければならない (equality gate)。class 16131は
  v001/v002の保有クラスとして必ずflipし、scenario-unknownは53→51。flipsの
  個数・peerクラス構成は台帳記録のみで予想しない (Part AJの30クラスjointと
  は条件が異なる)。joint greedy/worklistの変化は実測をそのまま記録し、
  加成性の主張はしない。
- 主張範囲: if-adopted投影上の分類delta (flip集合・win_hit_groups・被覆・
  worklist等の数表) のみ。canonical cacheは本Partで一切変更しない。
- verdict不消費: 本Partが消費するverdictはゼロ (if-adopted cacheはrepoの
  canonical chainではない)。v001/v002 (と他15候補) はcanonical上も未来の
  採用判断上もunconsumedのまま。
- 並走との不接触: AY宣言の残51キー (v003..v053・fresh) には一切触れない
  (probeも15M再探索もしない)。Part AVの成果物 (cache 6,172行・reaudit出力)
  には読み書きともに触れない。AYレーンのbatch-18 continuation / batch-19
  (class 16513) pivotの選択を本Partは妨げない。同一スコープ (batch-18 WIN行の
  if-adopted分解) の対抗宣言がmainに存在する場合は本宣言を破棄して着手しない。
- 標準11×11空盤・19 central-reply roots・class 16131 (残51子)・全53キーは
  本Partのどの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミットメッセージ
  に記録する。push直前にnote blob sha1ロックを再照合し、競合時は再fetchして
  本節を追記し直す。

### Part BA status update (2026-11-22, execution host = 本レーン continuing session)

宣言 (note amendment commit `607c876a`, observed HEAD-before-push
`f8cc6c9d`) どおり、宣言後に本hostがv001+v002同時採用のif-adopted
投影を計算・出版まで完了した (verdict不消費)。実行中に環境リセットが
1回発生したため、全pinned入力をmainから再取得・sha照合のうえ全工程を
再実行し、一次実行と再構築実行の出力が全てbyte一致した
(決定論的再現の追加検証になった)。

- maker `make_increment_v001v002_win.py` (3回実行byte一致): 2行
  increment sha256 `4f8fc29b…`・manifest sha256 `13736030…` (schema
  `batch18-win-v001v002-ifadopted-increment-manifest-v1`, rows 2/2/0,
  win_ids [v001, v002], win_s5_index [153671, 207534], win_nodes
  [5656151, 7898204], ifadopted_only, canonical untouched pin,
  base_cache_absent_hits 0, quarantine_hits 0)。raw 4ファイル
  (published pins `24b45c8a`/`1fc367bd`/`41c10ec2`/`e9f578fc`) の
  2-pass node-exact再検証・status-b18.log (`4b785add…`) との3-way
  一致・batch-keys legal一致はAT版と同一gate。
- merger (byte-copy pin `90711961…`, selftest PASS) 2回実行byte一致:
  **if-adopted cache 6,122行** (WIN 160 / LOSS 5,962, conflict 0,
  duplicates 0) sha256 `6bfa9faa…` (251,556 bytes)。merge-audit
  run1/run2 byte一致 sha256 `4cdad34b…`。merge後にBASE canonical
  6,120行 `be9cb24e…` byte不変を再検証 (verdict不消費の機械表明)。
- refresh adapt版 `refresh_v001v002_ifadopted.py` (AT版 `5f9810e6…`から
  2-hunk adapt) 2回直列実行 (~60s/回)・4出力ともbyte一致:
  summary `af95270b…` / closure-classes `e5a91e15…` / per-root-coverage
  `9f59ebf8…` / probe-worklist `18429b91…` (3.7MB・不出版・sha記録のみ)。
- extractor `compare_deltas_v001v002_ifadopted.py` (AT版 `207cfbcc…`の
  双WIN adapt・本レーン執筆) 3回実行byte一致 (delta json sha256
  `e3679aae…`)・全gate PASS。flips == s5 153671/207534のgraph保持
  クラス和集合のうちBASE-unknownのもの (v001 holders [4139, 16131] /
  v002 holders [5611, 6073, 16131] / double holders [16131] を機械
  計算・hardcodeなし)、**class 16131のBASE-unknown子53個 == batch-18
  53キーのs5 index集合** (新規の強い一致gate)、純WIN採用のnewly-free
  空集合・per-root被覆変更行0・新規free第三手空集合、verdict不消費
  (両s5のBASE index_verdict不在)、raw 2-pass・legal再検証。fail-closed
  改ざんテスト5種 (increment改ざん→INCR_SHA pin・summary改ざん→
  SCEN_SUMMARY_SHA pin・batch-keys改ざん→BATCH_KEYS_SHA pin・extractor
  定数v002 s5改ざん→manifest win gate・BATCH_CLASS改ざん→manifest
  class gate)、すべて即復元・復元byte一致を確認。
- 実測 (投影・schedule quantities): **flips = [4139, 5611, 6073, 16131]**
  すべてunknown→excluded_now 4 / unknown→unknown 34,496 /
  excluded→excluded 390 / excluded_now→excluded_now 23 /
  free_now→free_now 36、回帰0)。excluded_now 23→**27**・unknown
  34,500→**34,496**・free_now **36不変**。class 16131 (唯一のdouble
  holder) はBASE-unknown 53→**51**・closure候補表rank 15→**7**
  (unknown_now 51・groups_served 5、表はprobing-worklist view)。
  per-root free/uncovered変更行0 (root 27 baseline 119/119不変)。
  update8: resolved 79→**81** (新規 [153671, 207534]・両WINとも
  baseline requirement内)・win_hit_groups []→**5** (全てclass 16131の
  5 closure groups (12,50)/(12,70)/(48,20)/(48,72)/(48,100))・
  groups_free_now 127不変・remaining_now 31,780→31,729 (−51: 5つの
  win-hit groupがfrozen per-group unknown和集合から除外される.published
  refreshの機械計算・簿記)。joint greedy 36,726→**36,724**・probe
  worklist 64,941→**64,939** (movers: root 12 −2・root 48 −2)。
- 出版: 実験dir
  `research/experiments/n11-centralreply-class16131-win-v001v002-ifadopted-20261122/`
  15ファイル+不出版1 (worklist) を3コミットでmainに反映: A `603b4f4f`
  (if-adopted cache 6,122行・251,556 bytes) / B (maker `1e7865cb` +
  merger `00c3cdc6` + extractor `ce134e05` + refresh `94b00500` +
  increment `8e8c51d5` + manifest `1b8bc3c8` + merge-audits
  `19366a1e`/`b4e8e534`) / C (summary `2df84b96` + closure `26ef7844` +
  prc `e3abf46c` + delta json `f11677f3` + README `00c735de` +
  status.log `2cabe757` + MANIFEST-sha256 (15行) `333ef6d1`) =
  publication complete。**fetch-back 15/15 sha一致** (各publication
  commit固定rawでsha256照合)。
- 意味 (route statement・閉鎖主張なし): if-adopted投影は、scrutiny
  ownerがv001+v002を**同時に**採用した場合の分類台帳の変化を機械
  証明したもの。4クラス (4139 v001のみ / 5611・6073 v002のみ / 16131
  両WIN保有) の全LOSS閉包ルートは検証済みWIN子によって永久に反駁され、
  被覆は不変、update8は2つのpinned解決を得る。17個のunconsumed
  closure WIN全てのif-adopted分解が揃った (v001/v002が最後のギャップ
  だった)。本Partは採用を推奨も却下もしない・判断は一切代行しない
  (scrutiny owner C++第二実装 gate pin `9193f5b6…`のまま)。
- verdict不消費: canonical cache 6,120行 `be9cb24e…` はbyte不変
  (merge後再検証)。if-adopted cache 6,122行はrepoのcanonical chain
  ではない。v001/v002 (と他15候補) はcanonical上も未来の採用判断上も
  unconsumedのまま。AY宣言の残51キー (v003..v053・fresh) と Part AV
  (batch-17 adoption・in flight) の成果物には読み書きとも触れていない。
- 標準11×11空盤・19 central-reply roots・class 16131 (残51子)・全classは
  本Partのどの時点でもUNKNOWNのまま。nodes数・worklist数・greedy数を
  勝敗として読まない。

## Part BB (verifier, declaration 2026-11-22): 全17 unconsumed closure WIN行のjoint if-adopted分解 (scrutiny owner向け事前計算・verdict不消費・実行前に宣言)

Part BAの完了により、17個全部のunconsumed closure WIN (b018/d002/e002/
f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042/v001/v002) が
単独または小結合のif-adopted分解を持つ状態になった。ただし全17行を
**同時に**採用した場合のjoint投影は存在しない (Part AJのjoint10は旧
BASE 6,120ではなく**Part Y時代の6,027行**を用いた10 WIN版で、しかも
その後7 WIN (p002/p003/r001/r002/q042/v001/v002) が増えた・機械可測の
ギャップ)。scrutiny owner (C++第二実装 gate pin `9193f5b6…`) のための
全17行同時採用if-adopted分解を、**現行canonical BASE 6,120行**
(sha256 `be9cb24e…`, Part AS publication) の上で実行する。
**verdict不消費・本Partは採用を推奨も却下もしない・if-adopted投影を
勝敗や閉鎖主張として読まない。**

- 対象: `research/experiments/n11-centralreply-joint-17win-ifadopted-20261122/`。
- 入力は**全て出版済みのsha-pinned increment cache**のみ (raw再検証は
  各自の出版時に完了済み・ここではpinで連鎖させる):
  (1) Part AJ wins10 `fe2c6f68f49195b44e21c8d43998fccd965c868e08e49d8a1b3233f5daa4c15e`
  (10行: b018/d002/e002/f017/g018/h045/j033/z003/n005/n006)、
  (2) batch13 wins2 `bb238f67dbfcc3b9a05ac5542f783107366777f17149f7a5a5af64d4864b0f7c`
  (p002/p003, class 16930)、
  (3) batch15 wins2 `05c10e1ff17c2601b1fb4a0782af2543d302187ce6344df97d3c763947262b7d`
  (r001/r002, class 5830)、
  (4) Part AT q042 `b4958328270f11b24d3a638e1099a0c6047dbebb242e3116217b0473ef63f9b6`
  (class 23101)、
  (5) Part BA b18win v001/v002 `4f8fc29bfd00492aa9a983f20a121737d395b8f80d53e2b04c271fec068bc1ee`
  (class 16131)。resource pins: graph `54f9c364…`・update8 `b658290a…`・
  Board `954d3a10…`・policy `78655e94…`・quarantine `81d23160…`・
  BASE reaudit正本 3件 (Part AS: `f2008e70…`/`3ee1dbb6…`/`527c7e9a…`)。
- maker `make_increment_17win_joint.py`: 5つのpinned incrementから
  (行形式・WIN=1・nodes正・キー17個一意・BASE不在6,120行・quarantine
  不在・canonical-safe・各manifestのsha/行数/win構成との交差一致) を
  gateして17行joint increment + manifest (rows 17/17 WIN/0 LOSS) を導出。
- merger: byte-copy pin `90711961…` 2回実行・byte一致 → **if-adopted
  cache 6,137行** (WIN 175 / LOSS 5,962)。merge-audit 2回byte一致。
  merge後にBASE `be9cb24e…` byte不変再検証。
- refresh: AT/BA流のadapt (docstring + cache path + cache sha期待値は
  cache自体から機械抽出) を2回直列実行・4出力byte一致。
- extractor `compare_deltas_17win_ifadopted.py` (BA版 `c1c39b50…` の
  17-WIN拡張): flips == 17個のWIN s5 indexの全graph保持クラス和集合の
  うちBASE-unknownのもの (per-WIN holder台帳 + joint union機械計算・
  hardcodeなし)・純WIN採用のnewly-free空・per-root被覆変更行0・
  per-WIN s5のBASE index_verdict不在 (17/17不消費gate)・
  update8新規解決集合 == baseline requirement ∩ 17 s5 (機械)・
  excluded_now/unknownの加算整合。実測は台帳に記録するのみで
  事前予想しない (Part AJとの差分要因: BASE 6,027→6,120変化・
  10→17行拡大・その後のbatch-14 41 LOSS採用)。
- 並走との不接触: AY残51キー・Part AV (batch-17 adoption, in flight)・
  batch-19には一切触れない。同一スコープ (17-WIN joint if-adopted
  分解) の対抗宣言がmainに存在する場合は本宣言を破棄して着手しない
  (grep済み: 同名実験dirなし・note内に対抗宣言なし)。
- 標準11×11空盤・19 central-reply roots・17 WINの保有クラス (残る
  unknown子すべて)・全classは本Partのどの時点でもUNKNOWNのまま。
  nodes数を勝敗として読まない。
- 本amendment observed HEAD-before-push: 実行時の最新mainをコミット
  メッセージに記録する。push直前にnote blob sha1ロックを再照合し、
  競合時は再fetchして本節を追記し直す。

### Part BB status update (2026-11-22, execution host = 本レーン continuing session)

宣言 (note amendment commit `dafe9651`, observed HEAD-before-push
`53e7fae9`) どおり、宣言後に本hostが17行全同時採用のjoint if-adopted
投影を計算・出版まで完了した (verdict不消費)。入力は5つのpublished source
increment (AJ wins10 `fe2c6f68` / batch13 `bb238f67` / batch15 `05c10e1f`
/ Part AT q042 `b4958328` / Part BA v001+v002 `4f8fc29b`、各manifestも
pin `74fb877d`/`43143fd5`/`d6ed7b93`/`894e9420`/`13736030`) を
upstream正道からsha検証し、commit `0664482f` pinned rawで計8ファイルの
byte再検証も行った (誤配信なし)。full shaは実験dirの
MANIFEST-sha256.txt (16行・`8c361955…`) がpinする。

- maker `make_increment_17win_joint.py` sha256 `4585c416…` (3回実行
  byte一致): 17行joint increment sha256 `04003820…` + joint manifest
  `509cc941…` (schema `joint17win-ifadopted-increment-manifest-v1`,
  rows 17/17 WIN/0 LOSS、17キー一意・BASE不在 hits 0 (6,120行)・
  quarantine不在・canonical-safe・source manifestとのkey/s5/nodes機械
  交差・`win_s5_in_update8_baseline_requirement = 12`のupdate8 baseline
  31,859との機械交差) を導出。
- merger (byte-copy pin `90711961…`, selftest PASS) 2回実行byte一致:
  **joint if-adopted cache 6,137行** (WIN 175 / LOSS 5,962, conflict 0)
  sha256 `f8c2fd97…` (252,255 bytes・non-canonical投影)。merge-audit
  run1/run2 byte一致 sha256 `ae19b239…`。merge後にBASE canonical
  6,120行 `be9cb24e…` byte不変を再検証。
- refresh adapt版 `refresh_17win_ifadopted.py` (BA版 `d3fd8498…`から
  docstring文言 + projection cache path + cache sha期待値cache自体から
  の機械抽出の3-hunk adapt) sha256 `0365bf26…` 3回直列実行・4出力とも
  run間byte一致: summary `5cee4086…` / closure-classes `0c3c31f3…` /
  per-root-coverage `5ead108d…` / probe-worklist `4ca9e21b…`
  (3.7MB・不出版・sha記録のみ)。
- extractor `compare_deltas_17win_ifadopted.py` (BA版 `c1c39b50…`の
  17-WIN拡張・本レーン執筆) sha256 `1163b7c3…`: joint incrementを
  5 source incrementからbyte再構築してpublished行とbyte一致を保証、
  delta json (sha256 `115677e6…`, 39,648 bytes, schema
  `n11-joint17win-ifadopted-decomp-deltas-v1`) を3回実行byte一致・
  全gate PASS。INCR_SHA末尾pinの当初誤記 (`…d495485`) は作成中に
  fail-closed gateが捕捉し`…d497485cbe87`に修正した (検証済み3回は
  修正後)。fail-closed改ざんテスト7種 (joint increment nodes /
  if-adopted cache nodes / scenario summary / extractor baseline定数
  34500→34499 / extractor source-class pin 16930→16931 / upstream
  batch-13 increment / scenario closure CSV) すべて該当gateが捕捉・
  即復元・復元byte一致。
- 実測 (投影・schedule quantities): **flips = 42クラス**
  `[1518, 2634, 4139, 4843, 4864, 4889, 4892, 4903, 5007, 5011, 5255,
  5282, 5307, 5471, 5473, 5501, 5513, 5611, 5613, 5626, 5632, 5748,
  6030, 6073, 6147, 6166, 8106, 8785, 12264, 12327, 14776, 15640,
  16131, 16371, 16757, 16930, 20421, 23092, 23101, 23115, 23938,
  30345]` (17 WIN s5のgraph保持クラス**和集合**のうちBASE-unknownの
  もの・per-s5 holder台帳+joint union機械計算・hardcodeなし)。遷移
  台帳: unknown→excluded_now 42 / unknown→unknown 34,458 /
  excluded→excluded 390 / excluded_now→excluded_now 23 /
  free_now→free_now 36・回帰0 (gate)。excluded_now 23→**65**・unknown
  34,500→**34,458**・free_now **36不変**・excluded 390不変。
  **class 5830 (batch-15) は機械検証済みの例外**: BASEで既に別WIN子
  `[126017, 131631, 162106, 197665, 206386]` によりexcluded_now済み
  のためr001/r002採用はここに新規flipを作らない (13 source-class
  ledgerのうち唯一の非flip)。共有費用効果はclass 2634側 (r001/r002と
  の共有費用子 103558/103560/103561込みで51→48)。13 source classの
  BASE-unknown境界の和は17 WIN子**全て**を被覆 (gate)・13中12が
  flips内。class 16131 53→51 (BASE-unknown==batch-18 53キーの強い一致
  gate維持)。update8: resolved 79→**91** (newly 12 index
  `[103558, 103560, 103561, 153671, 184684, 188395, 197253, 198530,
  207534, 219608, 415095, 528497]` == baseline requirement ∩ 17 WIN
  s5 == manifest `in_baseline_req` 12・算術一致)・win_hit_groups
  []→**34** (34 groupすべてflip集合内のclassがserve・gate)・
  groups_free_now 127不変・remaining_now 31,780→**31,389** (−391:
  34 win-hit groupがfrozen per-group unknown和集合から除外)・lost
  resolutions [] (gate)。joint greedy 36,726→**36,727** (+1)・probe
  worklist 64,941→**64,917** (−24)。per-root free/uncovered変更行0
  (root 27 baseline 119/119不変)・新規free class/third空 (gate)。
  closure候補表churn: 退出 `[5746]`・新規 `[5748]`・class 16131 rank
  15→**14** (unknown_now 51)。
- 出版: 実験dir
  `research/experiments/n11-centralreply-joint-17win-ifadopted-20261122/`
  を3コミットでmainに反映: A `28acbbe9` (if-adopted cache 6,137行・
  252,255 bytes) / B `d86e33da` (maker `4585c416` + merger `90711961` +
  extractor `1163b7c3` + refresh `0365bf26` + increment `04003820` +
  manifest `509cc941` + merge-audits run1/run2 `ae19b239`) / C
  `78b4b8a1` (README `aed9994c` + status.log `871b3869` + reaudit
  summary `5cee4086` / closure-classes `0c3c31f3` / per-root-coverage
  `5ead108d` 3出力 + delta json `115677e6` + MANIFEST-sha256 `8c361955`)
  = publication complete。**fetch-back 16/16 sha一致** (各publication
  commit固定rawでsha256照合)。
- 意味 (route statement・閉鎖主張なし): joint if-adopted投影は、
  scrutiny ownerが17個のunconsumed closure WINを**全て同時に**採用した
  場合の分類台帳の変化を機械証明したもの。42クラスの全LOSS閉包ルートは
  検証済みWIN子によって永久に反駁され、被覆は不変、update8は12個の
  pinned解決を得る。これで17個すべてのunconsumed closure WINが単独・
  2行・10行・17行両極のif-adopted分解を持った (機械可測のギャップは
  消滅)。本Partは採用を推奨も却下もしない・判断は一切代行しない
  (scrutiny owner C++第二実装 gate pin `9193f5b6…`のまま)。
- verdict不消費: canonical cache 6,120行 `be9cb24e…` はbyte不変
  (merge後再検証)。if-adopted cache 6,137行はrepoのcanonical chain
  ではない。17 WIN行は全てcanonical上も未来の採用判断上もunconsumed
  のまま。AY宣言の残51キー (v003..v053・fresh)・Part AV (batch-17
  adoption・in flight)・batch-19 (class 16513) の成果物には読み書き
  とも触れていない。
- 標準11×11空盤・19 central-reply roots・17 WINの全保有クラス (残る
  unknown子すべて)・全classは本Partのどの時点でもUNKNOWNのまま。
  nodes数・worklist数・greedy数を勝敗として読まない。

## Part AV takeover (adoption, amendment 2026-11-22): batch-17 52-LOSS canonical adoptionのtakeover実行宣言（実行前に本amendmentを出版）

Part AV declaration (commit `340abef3`, observed HEAD-before-push `4741a92f`)
から7時間以上経過し、**~23:00Zのtakeover基準時刻** (AYレーンと共有・
session log Continuation 41 addendum `67b41c5a` が22:04Zにread-only
preflight済み・「dirがmainに現れない限りstandby」記録) を過ぎても、
Part AV対象dir
`research/experiments/n11-centralreply-class10661-loss52-adoption-reaudit-20261122/`
はmainに存在せず、AV採用のpublicationコミットも対抗takeover宣言も
存在しない (observed HEAD `432664f7` 時点でcommit stream・当note両方を
確認)。よってPart U / Part Z precedent に従い、本hostがPart AVを
takeoverし、declaration `340abef3` の範囲を**変更なく**そのまま実行する
単一オーナーとなる (本amendmentはscope変更ではなく所有権の移転のみ)。

- 本hostのtakeover前read-only preflight (本amendmentより前・verdict不消費・
  db書込ゼロ): (1) batch-17実験dir kit mirror 177ファイルをpublished
  MANIFEST-sha256 (main byte同一確認済み) に対しsha256全件再検証 0 bad
  (batch-keys `db762175…`・row-audit `c19e768f…`・raws 104含む)。
  (2) Part AS機材precedent kit 15ファイルを同様に全件再検証 0 bad
  (canonical 6,120行 `be9cb24e…`・AS reaudit 3出力 `f2008e70…`/
  `3ee1dbb6…`/`527c7e9a…`・maker `b6094f0b…`・merger `90711961…`・
  extractor `9e885ae0…`・refresh `5992738d…`)。
- 実行するpipeline (declaration `340abef3` の文言どおり・適応先はbatch-17):
  maker (Part AS `make_increments_batch14.py` のbatch-17 adapt・
  3-way p1/p2/status.log node-exact・batch-keys legal/(lo,hi)・
  row-audit 52行一致・WIN/exhaustion「不在」gate・52キーのBASE cache不在
  (0 hits)・quarantine 0・probed set=={u001..u052}+WAVE-END全体像) →
  fail-closed union merger (`90711961…` byte-copy・3回実行・byte一致・
  WIN/LOSS conflict 0) でcanonical 6,120行→**6,172行**を新pathに出版 →
  refresh adapt版 2回直列実行・run間byte一致 → delta extractor adapt版
  (BASE=Part AS reaudit 3出力・scenario=本reaudit出力) 3回実行・byte一致・
  全gate PASS。成果物は全てpublished正本のみからsha-pinで導出し、
  対象dir `n11-centralreply-class10661-loss52-adoption-reaudit-20261122/`
  に出版・fetch-back byte検証する。
- class 10661採用後のclass_status遷移 (free_now 36→37かどうかを含む) は
  宣言文言どおりreauditの機械計算に委ね、本amendment時点では一切断定しない。
- verdict不消費 (WIN側不変): batch-17にWIN行は存在しない (不在gate)。
  採用消費は52 LOSS行のみ。15 unconsumed closure WIN (宣言時点) は
  その後AY v001/v002を含む**17 unconsumed closure WIN**として増加したが、
  本Partはその全てに読み書きとも触れない (採用判断はscrutiny owner
  C++第二実装 gate pin `9193f5b6…` のまま)。
- 標準11×11空盤・19 central-reply roots・class 10661・全class・未知の全S5子
  は本Partのどの時点でもUNKNOWNのまま。nodes数を勝敗として読まない。
- 並走との不接触: batch-18 (AY残51キー)・batch-19選定・y=16 fastレーン・
  K1058レーンの成果物には読み書きとも触れない。**同一スコープの対抗
  takeover宣言/amendmentが本amendmentより先にmainに存在する場合
  (push時のnote blob sha1 lock `…` 衝突で検出) は本takeoverを破棄して
  着手しない。**
- 本amendment observed HEAD-before-push: `432664f7` (push直前にnote
  blob sha1 (`5022600953d25a02b4ae77da531f513c9ad4dea7`) を再照合し、
  競合時は再fetchして本節を追記し直す)。

### Part AV status update (2026-11-22, takeover実行host): execution complete, published, fetch-back verified

takeover amendment (上記・commit `d3ef2dc6`) どおり、本hostが単一
オーナーとしてbatch-17 (class 10661) 52-LOSS canonical採用+reauditを
宣言スコープ変更なく実行完了し、対象dir
`research/experiments/n11-centralreply-class10661-loss52-adoption-reaudit-20261122/`
をmainに3コミットで出版・fetch-back byte検証した (全16ファイル
MANIFEST-sha256照合一致・publication commit固定rawでcmp byte一致)。

- 出版コミット: A `3b1ed4d8` (observed HEAD-before-push `7eba0c4b`:
  increment 52行 `afcdad5b…` + manifest `e1d430a4…`
  (schema batch17-loss52-increments-manifest-v1, full==loss,
  win_scenario_exists false, row_counts 52/0/52/0) + merged canonical
  cache **6,172行** (WIN 158 / LOSS 6,014, conflict 0, `a5540811…`,
  253,898 bytes, 6,120+52 machine-checked) + merge-audit run1/2/3
  byte一致 `faf504ab…`) / B `96ee328a` (maker `04bde073…` +
  byte-pin merger `90711961…` + extractor `92d83671…` + refresh adapt
  `1b49cc07…`) / C `23bda9ba` (reaudit 3出力 `a0043c76…` /
  `e60c1088…` / `4c7ec5d7…` (2回実行byte一致) + delta
  `7d93613b…` (3回実行byte一致・全gate PASS) + README + status.log +
  MANIFEST-sha256)。probe-worklist `667dc815…` (3.7MB) は
  AH/AO/AP/AS先例どおり不出版・sha記録のみ。
- 実行機証: maker 3回・merger 3回・refresh 2回・extractor 3回とも
  byte一致。fail-closed改ざんテスト8種 (maker T1-T3: raw 2-pass
  ノード改ざん・row-audit sha pin・status.log PASS行不整合 /
  extractor T5-T8: increment sha・manifest row_counts・scenario
  cache sha・batch-keys sha) 全捕捉・復元byte一致・テスト後入力
  ミラー再検証 0 bad (batch-17 177ファイル・Part AS kit 15ファイル)。
- canonical上の機械確定 (分類の前進・reauditの機械gate・閉鎖主張なし):
  **class 10661が37番目のBoard検証free class** (BASE-unknown費用子
  52個全てが採用52行で解決・scenario-unknown 0・子境界の独立整数幾何
  再生成で全子exact LOSS)。free_now 36→**37**・unknown 34,500→
  **34,499** (unknown→free_now 1のみ・二方向gate)。**root 24 (central)
  free thirds 10→12 / uncovered 109→107** (新規free third 30・90)。
  update8 resolved 79→**80** (新規 s5 272756・LOSS・gate)・
  remaining 31,780→31,779・groups_free_now 127不変。簿記量 (勝敗ではない):
  joint greedy 36,726→35,645 (−1,081)・probe worklist 64,941→64,888
  (−53)・closure候補表 809→808 (class 10661退出・churnはbest-option
  簿記)。class 23101はrank 1 unknown 11のまま (非接触・不変)。
- verdict不消費 (WIN側不変): 消費はbatch-17 52 LOSS行のみ (fail-closed
  merger経由)。batch-17にWIN行・枯損行は存在しない (不在gate・manifest
  win_scenario_exists false)。**17 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/
  r002/q042 + AY v001/v002) は読み書きとも不接触・不変**。採用判断は
  scrutiny owner C++第二実装 gate pin `9193f5b6…` のまま。
- 並走との不接触: batch-18 (AY残51キー)・batch-19選定・y=16 fastレーン・
  K1058レーン・Part BB 17-WIN joint if-adopted成果物には読み書きとも
  触れていない (本3コミットは新規dir配下のみ)。
- 標準11×11空盤・19 central-reply roots・class 10661以外の全class・
  未知の全S5子は本Partのどの時点でもUNKNOWNのまま。nodes数・worklist数・
  greedy数を勝敗として読まない。
- 本status update observed HEAD-before-push: `23bda9ba` (push直前に
  note blob sha1 (`20bf1ecce776b4a4a7deac601613b8ede22c819e`) を再照合し、
  競合時は再fetchして本節を追記し直す)。


## Part BC (adoption, amendment 2026-11-22): batch-14residual (class 23101) 残余10-LOSS canonical adoptionの単一オーナー実行宣言

本hostが、batch-14residual (class 23101系譜・Part AW出版commit `cb94f808`由来)
の残余10 LOSS行 (2-pass node-exact・published raw/row-audit正本のみを入力とする
fail-closed makerによる机計算済み) のcanonical採用+reauditを、Part AS/AV
precedentどおりfail-closed pipelineで実行・出版する単一オーナーであることを
宣言する。**同一スコープの対抗宣言/amendmentが本amendmentより先にmainに存在
する場合は本宣言を破棄して着手しない。**

- 対象dir:
  `research/experiments/n11-centralreply-class23101-residualloss10-adoption-reaudit-20261122/`。
- pipeline (全成果物はpublished正本からsha-pinで導出・実行回数とbyte一致を
  status.logに記録): maker (increment 10行・3-way p1/p2/status.log node-exact・
  row-audit 10行一致・WIN不在gate・BASE cache不在gate) x3 → fail-closed union
  merger (byte-pin `90711961…`・3回実行・byte一致・WIN/LOSS conflict 0) で
  canonical 6,172行 (a5540811系) → 6,182行 (WIN 158 / LOSS 6,024) を新pathに
  出版 → refresh adapt版2回直列実行・run間byte一致 → delta extractor adapt版
  (closure候補表両world row-exact再構築gate・全class減算gate) x3・byte一致・
  全gate PASS → 3コミット出版 (A: output 6ファイル / B: scripts 3ファイル+
  reaudit refresh adapt / C: README+status.log+MANIFEST-sha256+reaudit 3出力+
  delta json。probe-worklist 3.75MBはAH/AO/AP/AS/AV先例どおり不出版・sha記録
  のみ) → 各publication commit固定rawでfetch-back byte検証。
- 主張の範囲: **class 23101の閉鎖は主張しない。** q042 WIN子 s5 745184
  (key `1152921505747697664:1032`) はunconsumedのままで、採用後も同クラスに
  unknownコスト子1個 (s5 745184) が残る。refresh後のfree_now (37不変想定)・
  unknown数の変化はreauditの機械計算結果としてのみ記録し、本amendment時点
  では断定しない。
- verdict不消費 (WIN側不変): 消費はbatch-14residual 10 LOSS行のみ
  (fail-closed merger経由)。**17 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042 +
  AY v001/v002) は読み書きとも不接触。** 採用判断はscrutiny owner C++
  第二実装 gate pin `9193f5b6…`のまま。
- 並走との不接触: batch-18 (AY残51キー)・batch-19選定・y=16 fastレーン・
  K1058レーン・Part BB 17-WIN joint if-adopted成果物には読み書きとも
  触れない (本出版は新規dir配下のみ)。
- 標準11×11空盤・19 central-reply roots・class 23101・全class・未知の全S5子は
  本Partのどの時点でもUNKNOWNのまま。nodes数・worklist数・greedy数を勝敗として
  読まない。
- 本amendment observed HEAD-before-push: `1867f01f` (push直前にnote blob sha1
  (`b6a5f231914ae0da8789542b5aa1ec4f01fc1adc`) を再照合し、競合時は再fetchして
  本節を追記し直す)。


### Part BC status update (2026-11-22, 単一オーナー実行host): execution complete, published, fetch-back verified

宣言amendment (上記・commit `9165ae39`) どおり、本hostが単一オーナーとして
batch-14residual (class 23101) 残余10-LOSS canonical採用+reauditを宣言スコープ
変更なく実行完了し、対象dir
`research/experiments/n11-centralreply-class23101-residualloss10-adoption-reaudit-20261122/`
をmainに3コミットで出版・fetch-back byte検証した (note宣言amendment・
publication計17ファイルがcommit固定rawでsha256/cmp全件一致)。

- 出版コミット: amendment `9165ae39` (observed HEAD-before-push `1867f01f`:
  push直前にnote blob sha1 `b6a5f231…`を再照合) / A `168a44ae`
  (observed HEAD `9165ae39`: increment 10行 `c3f201a6…` + manifest
  `f7287b7b…` + merged canonical cache **6,182行** (WIN 158 / LOSS 6,024,
  conflict 0, `0b594f7e…`, 254,396 bytes, 6,172+10 machine-checked) +
  merge-audit run1/2/3 byte一致 `6a9a53a3…`) / B `f2405c0e` (maker
  `6c57f2d0…` + byte-pin merger `90711961…` + extractor `48e88838…` +
  refresh adapt `d6bb2374…`) / C `1afbc6a7` (reaudit 3出力 `5f3a09c6…` /
  `52ec3d4b…` / `1f54065a…` + delta `62de8c16…` + README `53347371…` +
  status.log `df9ccfab…` + MANIFEST-sha256 `2c805371…`)。probe-worklist
  `fe71be60…` (3.75MB) はAH/AO/AP/AS/AV先例どおり不出版・sha記録のみ。
- 実行機証 (実行回数はstatus.log `df9ccfab…`が正): maker 3回・merger 3回
  (audits 3回込)・refresh **3回** (4出力それぞれbyte一致)・extractor 3回
  ともbyte一致。extractorはclosure候補表を両worldでrow-exact再構築する
  churn gate + 全class減算gate付き (AV版 `92d83671…`からのadapt)。
  commit B/Cメッセージ中のrefresh "x2" は本節記載時の誤記 (実行3回・
  byte一致はstatus.log・kit mirrorが正)。
- canonical上の機械確定 (分類の前進・閉鎖主張なし・delta `62de8c16…`全gate):
  採用はbatch-14residual 10 LOSS行 (q043..q052・full==loss: WIN不在gate・
  枯損行不在)。**class 23101は閉鎖しない**: unconsumed q042 WIN子
  s5 745184 (key `1152921505747697664:1032`) が唯一のscenario-unknown
  cost子として残り、同クラスのunknown cost子は11→**1** (leftover
  `[745184]`・gate)。free_now 37→**37不変** (unknown 34,499不変・
  unknown→unknown 34,499・excluded_now 23不変・free_now→free_now 37の
  二方向gate)。update8: resolved 80不変 (newly 0)・win_hit_groups 0不変。
  27の他holder class (23104..23966・各1 LOSS子) はunknownのまま (各クラス
  scenario-unknown −1の簿記のみ)。**probe worklist 64,888→64,872 (−16)**。
  closure候補表808不変・churn: 退出 `[22149]`・新規 `[23965]` (best-option
  簿記)。joint greedy 35,645→38,978 (+3,333): 6 improveパス局所探索の
  収束先差による**非単調性**で退行ではない (improveパス無し構成では
  49,361→49,351と正しく減少・delta json `joint_greedy_nonmonotonicity`
  に記録済み・plan estimateのみで被覆主張ではない)。
- verdict不消費 (WIN側不変): 消費はbatch-14residual 10 LOSS行のみ
  (fail-closed merger経由)。**17 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042 +
  AY v001/v002) は読み書きとも不接触・不変**。採用判断はscrutiny owner
  C++第二実装 gate pin `9193f5b6…`のまま。
- 並走との不接触: batch-18 (AY残51キー)・batch-19選定・y=16 fastレーン・
  K1058レーン・Part BB 17-WIN joint if-adopted成果物には読み書きとも
  触れていない (本出版コミットは新規dir配下のみ)。
- 標準11×11空盤・19 central-reply roots・class 23101・全class・未知の全S5子
  は本Partのどの時点でもUNKNOWNのまま。nodes数・worklist数・greedy数を
  勝敗として読まない。
- 本status update observed HEAD-before-push: `1afbc6a7` (push直前に
  note blob sha1 (`004d69a762e2ccdb028a726837dfcef9bb2170c1`) を再照合し、
  競合時は再fetchして本節を追記し直す)。

## Part BD (verifier, declaration 2026-11-22): Part BC (batch-14residual 10-LOSS採用) 全pipelineの独立host再実行検証 (実行前に宣言・verdict不消費)

Part BC (note宣言amendment commit `9165ae39`・publication commits `168a44ae`/`f2405c0e`/`1afbc6a7`・status update直前のnote blob lock `004d69a7…`) が出版した
batch-14residual (class 23101) 残余10-LOSS canonical採用+reauditの全pipelineを、
published正本bytesのみから独立host (本host) で再実行・機械検証する verifier Part
を宣言する。同一スコープの対抗宣言/amendmentが本amendmentより先にmainに存在
する場合は本宣言を破棄して着手しない。

- 対象: `research/experiments/n11-centralreply-class23101-residualloss10-adoption-second-verification-20261122/`。
- 再実行 (全入力はpublished byte・commit固定rawでfetch-back sha検証済みの読み取り
  のみ): maker `make_increments_residual10.py` (published `6c57f2d0…`) x3 →
  increment/manifestがpublished byte (`c3f201a6…`/`f7287b7b…`) と一致すること。
  byte-pin merger `90711961…` (AV/BC両出版でbyte同一確認済み) x3 + selftest →
  canonical 6,182行 (published `0b594f7e…`) byte一致・merge-audits 3回byte一致。
  `refresh_adoption_23101resid.py` (`d6bb2374…`) x3 → reaudit 3出力
  (`5f3a09c6…`/`52ec3d4b…`/`1f54065a…`) + worklist (`fe71be60…`) byte一致。
  `compare_deltas_batch14residual_adoption.py` (`48e88838…`) x3 → delta json
  (`62de8c16…`) byte一致・全gate PASS。本hostのpreflightとしてpublished Part AV
  refresh (`1b49cc07…`) を先行再実行しBASE 4出力 (`a0043c76…`/`e60c1088…`/
  `4c7ec5d7…`/`667dc815…`) がbyte再現したことを確認済み (環境一致・verdict不消費)。
- 独立解析 (published BC機材に依存しない自前minimal checker・BC出力の値は使わない):
  increment 10行のraw p1/p2 + status.log PASS行 + row-audit + batch-keys + input CSV
  の3-way再導出・merged cache == published BASE 6,172 (`a5540811…`) ∪ increment 10
  の集合演算検証 (WIN 158 / LOSS 6,024・conflict 0・重複0)・graph s4_cost + cache +
  update8 receiptからclass 23101のscenario-unknownがちょうど{s5 745184}
  (=未採用q042 WIN行・key `1152921505747697664:1032`) であること・holder classの
  減算 (23101: 11→1・他メンバークラス各−1)・update8 resolved 80不変の独立再計算・
  closure候補表churn (退出 `22149`/新規 `23965`) とper-root被覆全行不変
  (root 27 119/119) のBC/BASE published CSV間の独立照合・worklist総数
  `64,888→64,872` の再計算・joint greedy非単調性 (`35,645→38,978`) を1-pass値と
  improve-pass逐次軌道 (BASE/BC両world) で計測する計装コピーにより分解し、
  決定論性と局所探索収束点由来であることを機械記録する (plan estimate・勝敗ではない)。
- fail-closed改ざんbattery (5種: maker raw node改ざん捕捉・merger WIN/LOSS conflict
  捕捉・increment verdict反転merger捕捉・extractor manifest row_counts改ざん捕捉・
  refresh cache sha改ざん捕捉・復元byte一致の確認込み)。
- verdict不消費: 本Partは読み取りと再実行のみで canonical cache・refresh出力への
  書込みなし (本Partの出力は新規dir配下のみ)。17 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p002/p003の15 + q042 +
  AY v001/v002) は読み書きとも不接触・採用判断 scrutiny owner (C++第二実装 gate
  pin `9193f5b6…`) 不変。q042 WIN行は採用・却下ともにならない。
- 標準11×11空盤・19 central-reply roots・class 23101 (未採用q042 WIN 1子)・全キー
  は本Partのどの時点でもUNKNOWNのまま。nodes数・worklist数・greedy数を勝敗として
  読まない。
- 並走との不接触: AY batch-18 (残51キー)・batch-19選定・y16 fastレーン・K1058レー
  ン・Part BB/BC成果物 (読み取りのみ) に書込みなし。
- 本amendment observed HEAD-before-push: `b706b21448041c8d6788fd9803059ae675051595` (push直前にnote blob sha1
  (`a564e191ef9eb5b369dee4b1d1a7c25e9a47f73a`) を再照合し、競合時は再fetchして本節を追記し直す)。

### Part BD status update (2026-11-22, verifier host B): execution complete, published (12 files), fetch-back verified

宣言 (note amendment commit `269e7865`・observed HEAD-before-push `b706b214`・push直前note
blob lock `a564e191…`) どおり、 verifier単一オーナーとしてPart BC batch-14residual
(class 23101) 残余10-LOSS canonical採用の全pipelineを独立host Bで再実行検証し、
`research/experiments/n11-centralreply-class23101-residualloss10-adoption-second-verification-20261122/`
に12ファイルを出版・fetch-back byte検証した (最終HEAD `2a8060b8` 固定rawでcmp 12/12一致・
MANIFEST sha256全件一致)。

- 出版コミット (12ファイル): scripts x3 = `34356786` (check_bd_minimal.py `46a6cc51…`) /
  `331b26b0` (refresh_adoption_10661_instr.py `d922e6a6…`) / `05cf0106`
  (refresh_adoption_23101resid_instr.py `1fe2e67b…`) ・ outputs x6 = `a2cca96d`
  (bd-verification-summary.json `55e61eb5…`) / `9c0bee45` (bd-rerun-shas.txt
  `a4db0efc…`) / `fb341fde` (bd-minimal-check-result.json `68871285…`) /
  `4e6723a4` (bd-greedy-trace-base.json `3560aa0b…`) / `4005defd`
  (bd-greedy-trace-scen.json `339a8238…`) / `e9ac7e0d` (bd-tamper-battery.log
  `a57329b2…`) ・ docs x3 = `76288203` (README.md `1ddffed0…`) / `abbfa7cf`
  (status.log `38cc26d6…`) / `2a8060b8` (MANIFEST-sha256.txt `3581d46b…`)。
- pipeline再実行 (全入力はpublished byte・commit固定raw fetch-back検証済み):
  maker x3 (increment `c3f201a6` / manifest `f7287b7b`) → merger selftest (5-case
  PASS) + x3 (canonical 6,182行 `0b594f7e` + merge-audits `6a9a53a3`) →
  refresh x3 (`5f3a09c6` / `52ec3d4b` / `1f54065a` + worklist `fe71be60`,
  ~58s/run) → extractor x3 (`62de8c16`・全gate PASS)。3回実行すべてpublished byte一致。
- 自作minimal checker (Part BC機材非依存・BC出力の値は不使用): **43 checks /
  0 failures / rc=0**。raw 3-way再導出 (p1/p2/status.log/row-audit/batch-keys/input
  CSV・23,252,550 nodes/pass) ・ q042不在/batch-17 s5-disjoint/quarantine disjoint・
  cache集合演算 (BASE 6,172 ∪ increment 10 = 6,182・WIN 158 / LOSS 6,024・conflict 0・
  重複0) ・ class 23101 scenario-unknown == [745184] (未採用q042 WIN行
  key `1152921505747697664:1032`) ・ holder 28クラス (23101×10 + 27×1) 値一致・
  世界分類 excluded 390 / excluded_now 23 / free_now 37 / unknown 34,499・board検証
  free 37/37・update8 resolved 80不変 (両world)・closure候補表808行churn
  (退出 `22149` / 新規 `23965`・rank1=23101 with unknown_now 1) と全808行の
  unknown_now列の自前再計算一致・worklist 64,888→64,872 ((key,serving_class)行
  multiset差分: 削除123コピー {22149:108, 23101:10, holder singles 5}・追加107コピー
  {23965支配}・採用10キーはSCEN worklistから完全消滅・−16はbest-option
  bookkeepingで被覆変化ではない) ・ per-root coverageはindividual_greedy_union
  カラムのみ変化 (23行・被覆列は不変)。
- joint greedy非単調性の決定論的分解 (計装refreshコピー・両world全出力byte再現):
  1-pass値 BASE 49,361 → SCEN 49,351 (−10 = 採用10キー分・BC host記録と一致) ・
  6-pass打ち切りsnapshot 35,645 → 38,978 (+3,333)。両worldともJOINTはpass 6で
  improved=Trueのまま制限打ち切り = 収束しない非単調局所探索の決定論的snapshot、
  plan estimateであり被覆主張ではない。軌道: BASE [49361, 35697, 40555, 36770,
  35167, 36270, 35645] / SCEN [49351, 35694, 40555, 36767, 35158, 36127, 38978]
  (trace 2ファイル出版)。
- fail-closed改ざんbattery: 宣言の5種をT3のmerger単体 (T3a) とrefresh cache-sha pin
  捕捉 (T3b) に分離し計6種を実行 (全てスクラッチツリーのみ・現物はbattery後に
  Part BC MANIFEST 16/16で再検証): T1 maker raw nodes改ざん→3-way gate ABORT rc1 /
  T2 増分11行目WIN追加→merger GATE FAILED・no-output rc1 / T3a q043 verdict単独反転
  →merger単体は成功 (WIN 159・tamper-merged `855c8aa6`) = mergerだけではBASE不在
  キーの反転を捕捉できないgate-gap (T3bでrefresh cache-sha pinがrc1捕捉) /
  T4 manifest row_counts 10→9→extractor GATE FAILED rc1 / T5 scenario cache nodes
  1桁改ざん→cache sha drift rc1 / T6 policy末尾1行追加→evidence policy sha drift rc1。
- verdict不消費: 本Partは読み取りと再実行のみでcanonical cache・refresh出力への
  書込みなし (出力は新規dir配下のみ)。**17 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042 +
  AY v001/v002) は読み書きとも不接触・不変**。採用判断はscrutiny owner C++第二実装
  gate pin `9193f5b6…`のまま。q042 WIN行は採用・却下ともにならない。
- 並走との不接触: batch-18 (AY残51キー)・batch-19選定・y=16 fastレーン・K1058レー
  ン・Part BB/BC成果物 (読み取りのみ) に書込みなし。
- 標準11×11空盤・19 central-reply roots・class 23101・未知の全S5子は本Partの
  どの時点でもUNKNOWNのまま。nodes数・worklist数・greedy数を勝敗として読まない。
- 本status update observed HEAD-before-push: `2a8060b86f506786553344eae61674adc18d3064`
  (push直前にnote blob sha1 (`739e7fe2c8c3e4dd5f816f69b804e12b80e66fd5`) を再照合し、
  競合時は再fetchして本節を追記し直す)。

## Part BE (solver, amendment 2026-11-23): closure class 16513 exact-S5 probe batch 19 (宣言後に実行・verdict不消費・実行前に宣言)

長期レーン (n11 central-reply closure) のbatch-19として、graph class index 16513
(mask [1153202980657299456, 67108864]) の53個のunknown費用子をexact-S5 probeする
単一オーナー実行を宣言する (batch-19 / closure class 16513 probeというスコープに
対して本amendmentより先にmainに存在する対抗宣言/amendmentがある場合は本宣言を
破棄して着手しない)。

- 選定根拠 (全てpublished byteからの再導出・Part BD時点のresume指針「batch-19
  選定」を本hostが履行): baseはpublished canonical exact-S5 verdict cache
  6,182行 sha256 `0b594f7e…` (Part BC採用正本)。再ランクclosure候補表808クラスの
  うち rank 1..14 (23101/16757/20421/16371/30345/12264/5473/2634/8785/1518/8106/
  16930/5830/16131) は全て17 unconsumed closure WIN子と交差 (win-refuted) し、
  rank 1 class 23101 のunknown集合は {745184} (未採用q042 WIN行のみ・採用は
  scrutiny owner待ち)。よってrank 15 class 16513 (unknown 53・groups 5
  {(24,50),(24,70),(24,96),(48,30),(48,90)}・WIN交差0・prior 19パケット914位置と
  重複0) が首位のclean候補、runner-upはrank 16 class 5687 (unknown 53・WIN交差0)。
- 機材 (全てpublished byte): replica `jsreplay.js` sha256 `84585617…` byte-copy・
  `runbatch.sh` `f591f8c2…`・`runwave.sh` `8efd78c2…` (batch-17正本)・依存graph
  `54f9c364…`・update8 `b658290a…`・Board `954d3a10…`・policy `78655e94…`・
  quarantine `81d23160…`。scaffold keys maker `make_batch19_keys.py` (本Part作成・
  3回実行byte一致・全gate PASS: 53キー0/53 canonical hits・0 quarantine・
  914位置overlap 0・17-WIN再導出一致・rank 1..16 exact assert)。
- val-gate (実行前・本host): at2m 2アンカー → result 0 / nodes 2,000,000 x2
  node-exact・15m 2アンカー → (2, 3651923) / (2, 5040200) node-exact・禁止四角
  95,670 x4・`# replay_done` x4 (truncationなし) の4/4確認済み。
- protocol (事前登録): 2-pass fresh-cold node-exact、budget 15,000,000、
  1 solver / 1 row / 1プロセス、worker最大2 (2-core host)、publish=ALL
  (raw 2-pass全件出版)。stop rules: 決定論mismatch → HARD-STOP rc=42・
  WIN → HALT rc=45 (honest WIN labelのみで採用しない・verdict不消費)・
  budget枯損 → honest UNKNOWN label (同条件での再probe禁止)。
- verdict不消費: LOSS行は採用候補のみ (消費は別宣言adoption Partがpinned
  fail-closed mergerで行う)。17 unconsumed closure WIN行
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042 +
  v001/v002) は読み書きとも非接触・採用判定はscrutiny owner C++第二実装 gate pin
  `9193f5b6…`のまま。batch-18 (AY残51キー) とは非接触 (class 16513の53子と
  batch-18パケット53位置は重複0・機械確認済み)。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・class 16513・全キーは
  本Partのどの時点でもUNKNOWNのまま。nodes/legal/キー数は簿記で勝敗ではない。
  probe worklist抽出は行わない (キー導出はgraph+published cacheから)。
- 実験dir: `research/experiments/n11-centralreply-closure-class16513-batch19-20261123/`。
- 本amendment observed HEAD-before-push: `b546b56d1c4bccb0d2fbf6f150d9190649fc9627`
  (push直前にnote blob sha1 (`598b5f8494e1f0a0c74f6a1ae073fb6b0cf273f0`) を再照合し、競合時は再fetchして本節を追記し直す)。

## Part BF (verifier, declaration 2026-11-23): batch-19 closure WIN行 w001/w002 の第三実装交叉検証 (宣言後に実行・verdict不消費)

batch 19 (Part BE, class 16513) は宣言どおりの実行で最初のwaveで
**w001 WIN 6,639,780 nodes** (legal 84・s5 63802・2-pass fresh-cold
node-exact・budget 15M内)・**w002 WIN 7,738,714 nodes** (legal 89・
s5 109169・2-pass node-exact) に終わり、事前登録WIN-HALT規則で停止した
(publication commits A `49c3bea7` / B `51e73082` / C `9719e926`、
2/53 probed・51 UNPROBED・verdict消費ゼロ)。これによりunconsumed closure
WIN候補は19になった。前例 (Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AZ の
verifier battery 约定) に従い、**採用判断待ちのWIN行に第三実装
verdict-level交叉検証の文献を追加する**。verdict不消費・採用判断は
scrutiny owner (C++第二実装 gate pin `9193f5b6…`)。

- 対象: `research/experiments/n11-centralreply-closure-b19win-thirdimpl-20261123/`。
  published batch-19の2 WIN行 (w001/w002) の全行再検証 + Part G/AR/AZと同一の
  anchor行 (k02a/l1a)・negative gate 2種 (ng1/ng2)・rules gate (verify_tbl
  quads 95,670 == third-impl・triples mismatch 0)。
- 入力: published batch-19 artifacts (publication commits `49c3bea7`/
  `51e73082`/`9719e926`・MANIFEST-sha256 74行・remote byte一致確認済み)
  から `scripts/make_inputs_bf.py` で機械導出 (fail-closed・手転写ゼロ):
  batch-keys `9609aaf3…` pin (53キー・class 16513・w001 s5 63802/w002
  s5 109169・membership 2)、raw 4ファイル (w001 p1/p2 `8cf13d13` byte同一
  (wall_s 67/67)・w002 p1 `1faf8d15`/p2 `feb8475b` (wall_s 81/67のみ相違))
  の2-pass node-exact (比較はnodes/legal/result/keys等の決定性field) +
  `# replay_done` + result 1 in-budget、status-b19.log `e3a9e5b4` の
  PASS行・WIN-HALT行・WIN-ROW-DETAIL行 (s5 index・holder classes 1363/2901
  込み)・VAL-GATE 4/4行・EXECUTION-HALTED行・51-unprobed行・19候補行の
  3-way一致、README-b19 `29c7ea51` 結果節照合・derived-vs-published
  input CSV byte-equality (w001 `f232a593`/w002 `574a4124`) +
  anchor/negative 4件はpublished Part AR実験dir CSVとbyte一致。
- 手法: pinned `third_impl.js` (`08ea958f…`)・1行=1 solver=1 process・
  cap 300,000,000拡張・wallcap 240s・`--memo-power=22`・全target/anchor
  a/b 2回のdeterminism gate (result/expansion/ttHits/reason同一必須)。
  wall到達 (240s) はhonest WALL-INCONCLUSIVE・clean不一致はDIVERGENCE
  として記録 (verdict書換え・隠蔽なし)。
- 停止・消費規則: 本Partのverdict消費はゼロ。canonical cache (6,182行
  `0b594f7e…`) に書込まない。19 unconsumed closure WIN候補 (b018/d002/
  e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042/v001/
  v002/w001/w002) は採用判断scrutiny owner待ち・不変。本Part単体では
  root被覆・クラス閉鎖・第三手securedの主張をしない。
- 並走との不接触: 本Partはpublished batch-19 raw (BEの成果物) の読み取り
  のみで、BE宣言の残51キー (w003..w053) には一切触れない (15M再探索禁止
  規則にも触れない)。batch-20 (rank 16 class 5687) pivot・batch-19残キー
  継続のいずれの選択も本Partは妨げない。同一スコープ (batch-19 WIN行の
  第三実装交叉検証) の対抗宣言がmainに存在する場合は本宣言を破棄して
  着手しない。
- 標準11×11空盤・19 central-reply roots・class 16513 (残51子)・全53キーは
  本Partのどの時点でもUNKNOWNのまま。nodes数・expansions数を勝敗として
  読まない。
- 実験dir: `research/experiments/n11-centralreply-closure-b19win-thirdimpl-20261123/`。
- 本amendment observed HEAD-before-push: `9719e92606a09eaf4ebb283488e66215ac71f295`
  (push直前にnote blob sha1 (`eb6066e68244324136e8f9dfeadb6e543779c7e7`) を再照合し、
  競合時は再fetchして本節を追記し直す)。

### Part BF status update (2026-11-23, execution host = 本レーン continuing session)

宣言 (note amendment commit `511ae474`) どおり、宣言後に本hostが
published batch-19 WIN行 w001/w002をpinned第三実装で解き、出版まで完了した
(verdict不消費)。

- 実行: pinned `third_impl.js` (`08ea958f…`)・1行=1 solver=1 process・
  cap 300,000,000・wallcap 240s・`--memo-power=22`・全target/anchor
  a/b 2回・逐次実行。**targets 2/2 clean WIN (result 1)・replica verdict
  一致 2/2**: **w001 third-impl WIN 7,682,625 expansions / 4,336,161
  ttHits** (replica 6,639,780 nodes・ratio 1.16)・**w002 third-impl WIN
  8,988,730 expansions / 5,106,247 ttHits** (replica 7,738,714 nodes・
  ratio 1.16)。a/b pair全員result/expansion/ttHits/reason同一
  (determinism gate PASS)。pass-one総expansions 16,671,355。
  LOSS 0・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
- battery順序: negatives ng1/ng2が設計どおりfail-closed文言 (GATE_FAIL)
  → anchors k02a WIN 9,106,337/4,991,527・l1a LOSS 7,660,602/3,951,175
  がpublished第三実装値にnode-exact再現 (a/b同一) → targets逐次実行
  (Part AXのCPU quota半減観測を継承し全行程逐次) → rules gate → audit x2。
- rules gate: verify_tbl replica quads 95,670 == third-impl quads 95,670・
  195,044 triples mismatch 0 (`output/rules-gate.txt`)。
- maker `make_inputs_bf.py`: 全gate PASS・3回実行byte一致 (source pins:
  batch-19 batch-keys `9609aaf3…` (53キー・class 16513・w001 s5 63802/w002
  s5 109169/membership 2)・raw 4ファイル (MANIFEST pins
  `8cf13d13`×2・`1faf8d15`/`feb8475b`)の2-pass node-exact + `# replay_done`
  + result 1 in-budget・status-b19.log `e3a9e5b4`のPASS行・WIN-HALT行・
  WIN-ROW-DETAIL行 (s5 index・holder classes 1363/2901込み)・VAL-GATE 4/4行・
  EXECUTION-HALTED行・51-unprobed行・19候補行の3-way一致・README `29c7ea51`
  結果節照合・derived-vs-published input CSV byte-equality 2 target
  (`f232a593`/`574a4124`) + 4 anchor/negative (published Part AR CSVと
  byte一致))・batch-19 published MANIFEST remote byte一致確認。
- audit `audit.py`: **53/53 gates PASS**・2回実行byte一致 (schema
  `n11-centralreply-closure-b19win-thirdimpl-audit-v1`)。verdict
  agreements 2/2 (WIN=2)・inconclusive 0。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-b19win-thirdimpl-20261123/`
  43ファイル+MANIFESTを3コミットでmainに反映: A `98e5b3b1` (scaffold:
  scripts 6 + inputs 7 + sources 13) / B `6e31eb35` (solver outputs 16:
  targets a/b 4・anchors 4・negative 2・rules-gate・status.log・
  audit-summary・audit-run1/2) / C `55a75f38` (README + MANIFEST-sha256
  43行) = publication complete。**fetch-back 43/43 sha一致**
  (publication commit `55a75f38` 固定rawで全ファイルbyte照合)。
- session log: Continuation 45 (Part BE実行記録・compaction後の書き起こし
  でpublished bytesに再照合済み) + Continuation 46 (Part BF完了) を
  commit `578bcb05` で出版・fetch-back byte一致。
- 意味 (route statement・閉鎖主張なし): batch-19最初のwaveの2 WIN
  (w001/w002) が独立実装 (第三実装) でもclean WINで再現された
  (verdict-level補強文献)。**verdict消費ゼロ**・19 unconsumed closure
  WIN候補の採用判断は一切代行しない (scrutiny owner C++第二実装 gate pin
  `9193f5b6…` のまま)。canonical cache (6,182行 `0b594f7e…`) 不変・
  いかなるcacheにも書込んでいない。BE宣言の残51キー (w003..w053・fresh)
  とbatch-20 pivot (rank 16 class 5687) には一切触れていない。
- 標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 16513 (残51子)・全53キーは本Partのどの時点でも
  UNKNOWNのまま。nodes数・expansions数を勝敗として読まない。

## Part BG (solver, amendment 2026-11-23): closure class 12457 exact-S5 probe batch 20 (実行前に宣言・verdict不消費)

長期レーン (n11 central-reply closure) のbatch-20として、graph class index
12457 (mask [1152921504606847268, 0]) の53個のunknown費用子をexact-S5 probe
する単一オーナー実行を宣言する (batch-20 / closure class 12457 probeという
スコープに対して本amendmentより先にmainに存在する対抗宣言/amendmentが
ある場合は本宣言を破棄して着手しない)。

- 選定根拠とroute-alive訂正 (全てpublished byteからの再導出・Part BF時点の
  resume指針「batch-20選定 (rank 16 class 5687)」を履行する機械検査で
  rank 16指定に訂正が必要と判明した点を誠実記録): baseはpublished
  canonical exact-S5 verdict cache 6,182行 sha256 `0b594f7e…` (Part BC採用
  正本) + update8 receipts (`b658290a…`)。再ランクclosure候補表808クラスの
  うち rank 1..15 (23101/16757/20421/16371/30345/12264/5473/2634/8785/1518/
  8106/16930/5830/16131/16513) は再導出unknown費用子と**19 unconsumed
  closure WIN子** (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/
  p003/r001/r002/q042/v001/v002/**w001 s5 63802/w002 s5 109169**) の交差が
  非空 (win-refuted)。rank 16 class 5687 (unknown 53)はWIN候補との交差0
  だが、**base + update8 receipts上で費用子 s5 209644 が勝ち (verdict 1)
  で確定済み** (receipt `209644: 1`・update8正本)。published Part BC refresh機
  (`refresh_adoption_23101resid.py` sha256 `d6bb2374…`) の公開規則
  「any cost child that is a known WIN now marks the class excluded」により、
  class 5687は同refreshの **excluded_now 相当** (全子LOSS閉包ルートは
  反駁済み。仮に残53子すべてをLOSSで解決してもclass 5687はfreeにならない)。
  batch-19 READMEの「runner-up 5687 also clean」記述はunconsumed-WIN交差のみ
  の検査であってknown-WIN子検査を含まず、closure候補としての実行価値の点で
  不完全だった (published byteは不変のまま、本amendmentが訂正記録)。
  よって**rank 17 class 12457 (mask [1152921504606847268, 0]・cost size 54・
  unknown 53・known子は s5 126899 (LOSS確定) の1個のみ・WIN候補交差
  0・known WIN子なし) がpublished表順で最初のroute-alive候補** (現時点で
  全子LOSS閉包ルートへの反駁証拠が1つもない) として選定する。runner-upは
  rank 18 class 12643 (unknown 53・WIN交差0・known WIN子なし・route-alive)。
  rank 19 class 25835 / rank 20 class 31600も同様にroute-alive (backups)。
- 機材 (全てpublished byte): replica `jsreplay.js` sha256 `84585617…`
  byte-copy・`runbatch.sh` `f591f8c2…`・`runwave.sh` `8efd78c2…` (batch-17
  正本pin)・依存graph `54f9c364…`・update8 `b658290a…`・Board `954d3a10…`・
  policy `78655e94…`・quarantine `81d23160…`。scaffold keys maker
  `make_batch20_keys.py` (本Part作成・3回実行byte一致・全gate PASS:
  53キー0/53 canonical hits・0 quarantine・prior 20パケット981行/967位置と
  重複0・19-WIN再導出一致・rank 1..17 exact assert・rank 1..16 refutation
  evidence gate (19-WIN交差またはknown-WIN子・5687は s5 209644=1 を再現)・
  **route-alive gate: class 12457のknown子集合は{126899: LOSS}のみ**・
  全キーlegal/membership再導出・`x`接頭辞未使用gate)。
- val-gate (実行前・本host): batch-19と同一4アンカー。at2m 2 → result 0 /
  nodes 2,000,000 x2 node-exact・15m 2 → (2, 3651,923) / (2, 5,040,200)
  node-exact・禁止四角 95,670 x4・`# replay_done` x4 (truncationなし)。
- protocol (事前登録): 2-pass fresh-cold node-exact、budget 15,000,000、
  1 solver / 1 row / 1プロセス、worker最大2 (2-core host)、publish=ALL
  (raw 2-pass全件出版)。stop rules: 決定論 mismatch → HARD-STOP rc=42・
  WIN → HALT rc=45 (honest WIN labelのみで採用しない・verdict不消費)・
  budget枯損 → honest UNKNOWN label (同条件での再probe禁止)。本hostの実行は
  published runnerを上限付きforeground起動 (drive driverはbatch意味論を
  持たない・中断断片はpublished completeness guardがfresh-cold再実行)。
- verdict不消費: LOSS行は採用候補のみ (消費は別宣言adoption Partがpinned
  fail-closed mergerで実行)。19 unconsumed closure WIN行は読み書きとも
  非接触・採用判定はscrutiny owner C++第二実装 gate pin `9193f5b6…`のまま。
  batch-19残51キー (w003..w053・fresh) とは非接触。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・class 12457・全キーは
  本Partのどの時点でもUNKNOWNのまま。nodes/legal/キー数は簿記で勝敗ではない。
  probe worklist抽出は行わない (キー導出はgraph + published cache + receipts
  から機械再導出のみ)。
- 実験dir:
  `research/experiments/n11-centralreply-closure-class12457-batch20-20261123/`。
- 本amendment observed HEAD-before-push: 723eb637c1fcfbec8d04a40fa7f634de65615c79
  (push直前にnote blob sha1を再照合し、競合時は再fetchして本節を追記し直す)。

## Part BH (solver, amendment 2026-11-23): batch-19 residual w003..w053 continuation (class 16513 enumeration - WIN-CONTINUE事前登録)・verdict不消費・実行前に出版

Part BE (batch-19 class 16513) は事前登録のWIN-HALT規則により最初のwaveで停止した。
published batch-19 READMEの予約文言 (「将来のPartが同じbatchを継続できる」「row-audit
はbatch完走時点 (残51キーの継続Part) に全行機械検証する」) に従い、残51キー
w003..w053 (fresh・一度も実行されていない) の単一オーナー実行を宣言する
(本amendmentより先にmainに存在するbatch-19 residual continuationスコープの対抗宣言・
amendmentがある場合は本宣言を破棄して着手しない。branch / PRは作らない)。

- WIN-CONTINUE事前登録 (Part AW batch-14 residualの先例と同一の根拠): class 16513の
  全子LOSS閉包ルートはpublished w001/w002 WIN honest labelにより既に反駁済み。
  残余キーのprobeはunknown数最小化のための列挙であり、ここでのさらなるWIN-HALTに
  情報価値はない。よってresidual installmentでは、published runbatch.shのrc=45
  (WIN) が発火したキーはhonest WIN labelのみで記録し、続けてdrive driverを
  再起動して51キー完遂まで列挙を続ける。決定論mismatch -> 即HARD-STOP rc=42
  (以後のdrive起動も行わずbatch全体を停止)。budget枯渇 (result 0) ->
  honest UNKNOWN labelで次キーへ (同条件再probe禁止)。
- 新規scaffoldなし。published batch-19 dir
  `research/experiments/n11-centralreply-closure-class16513-batch19-20261123/`
  を正本としてそのまま使用する: input/batch-keys.json (sha256 `9609aaf3…`・53キー)・
  53枚input CSV (各MANIFEST pin)・scripts `jsreplay.js` `84585617…` /
  `runbatch.sh` `f591f8c2…` / `runwave.sh` `8efd78c2…` / `drive_batch19.sh`
  `35024890…` / `row_audit_batch19.py` `e6526f75…` / `make_batch19_keys.py`
  `2b672888…`。published MANIFEST-sha256.txt掲載の74ファイルを本hostで
  sha256再検証し74/74 byte一致を宣言前に機械確認済み。
- val-gate (実行前・本host): batch-19/20と同一の4アンカー。at2m 2行 ->
  result 0 / nodes 2,000,000 node-exact、15m 2行 -> result 2 (2,3,651,923) /
  (2,5,040,200) node-exact、禁止四角 95,670 x4、`# replay_done` x4
  (truncationなし)。published val-gate/*.this-host.out基準線とnode数完全一致を
  実行の前提条件とする。
- protocol: 2-pass fresh-cold node-exact、budget 15,000,000、
  1 solver / 1 row / 1プロセス、publish=ALL。実行はpublished drive driver
  (1回起動あたりtimeout 260秒有界・残キー奇偶分割 worker最大2 = 2-core host・
  drive自体はbatch意味論を持たない) を渡して反復起動する。完了済み行
  (w001/w002・published raws) は再実行しない。中断断片はpublished completeness
  guard (`# replay_done` 検査) がfresh-cold再実行する。
- row-audit: 列挙完遂後、`row_audit_batch19.py` (published byte) により53キー
  全行の機械検証を行う。これはBE READMEが予約した「継続Partで全行機械検証する」
  役割の履行である。
- verdict不消費: canonical exact-S5 verdict cache (6,182行 `0b594f7e…`) を含め
  cache書込みは一切しない。LOSS行は採用候補のみ (消費は別宣言adoption Partが
  pinned fail-closed mergerで実行)。新規WIN行はunconsumed closure WIN候補の
  追加のみで採用しない (scrutiny owner C++第二実装 gate pin `9193f5b6…`のまま)。
  19 unconsumed closure WIN行 (w001/w002含む) は読み書きとも非接触。
- 不接触: 並走中のbatch-20 (Part BG) には一切触れない。batch 1..18 + 各residual
  packet・{60,27}系レーンは非接触。batch-19スコープ内のw003..w053のみを扱う。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・class 16513 (残51子も含む)・
  全キーは本Partのどの時点でもUNKNOWNのまま。nodes数・legal数を勝敗として読まない。
  閉鎖・被覆・secured主張は一切しない。
- セッション制約: 本Partが1セッションで51キー全てを完了できない可能性がある。
  その場合は完了行のみを誠実出版 (verdictを出力していないtruncated断片は
  出版対象から除外し再実行に備える) し、残りはfreshのまま次の継続Partに
  引き継ぐ。
- 本amendment observed HEAD-before-push:
  `358cac13521bd9cd075c7128763147f7b2511447` (batch-20 Part BG scaffold直後のmain・push直前にnote blob sha `becd61ac…`を再照合し、競合時は再fetchして本節を追記し直す)

## Part BG 出版status update (2026-11-23, solver): batch 20 (class 12457) 完走 - 53/53 two-pass node-exact・honest LOSS 53ラベル・verdict不消費

batch 20 (Part BG, class 12457) は宣言 (`b4c4ac2d`) どおり完走した。

- 実行 (本host・drive 7起動・最終起動は両worker rc=0): 53/53キー
  **PASS (p1==p2 node-exact・budget 15,000,000内・`# replay_done` x106)**。
  53ラベルすべて**result=2 (LOSS, pinned contract)**。honest labels
  として記録したのみ (adoption candidates・消費は別宣言adoption Partが
  pinned fail-closed mergerで実行)。WIN 0・exhausted 0
  (WIN-HALT規則・exhaustion規則とも不発動)・mismatch 0。
- 途中中断: host timeoutによるtruncated-retry 14件を誠実記録
  (`output/raw/*.truncated.*.out` として断片保存 + published
  completeness guard (`# replay_done` 検査) によるfresh-cold再実行。
  完了行の再実行はゼロ)。
- row audit PASS (`row_audit_batch20.py` `3197c4dc…`・
  `output/row-audit.json` `1dcb7fb8…`: 53 pass rows・LOSS 53・WIN 0・
  exhausted 0・mismatches 0・input `efb40b1b…`照合済み)。
- 出版 (宣言と同一scaffold・実行前にpre-publishedだったもの):
  commit A `358cac13521bd9cd075c7128763147f7b2511447`
  (scaffold 69 files・val-gate 4/4 node-exact込み)・
  commit B `564cc66a4a5b0a48cc4bb7c4010d802f13014e83`
  (実行outputs 122 files: status.log・row-audit・raw 120)・
  commit C `928546dfea4b40a3873ddc559fa6082a25445847`
  (README `ad0c3eec…` + MANIFEST-sha256 `d0ef293b…`・191 entries)。
  全ファイルfetch-back byte-verified (git blob SHA-1: 69/69・122/122・
  2/2照合; trees API + local blob再計算の独立経路)。
- 並走記録: 本Partの実行中にmainへ K1058 knowledge commit (`74fa9731`)
  と**Part BH宣言** (`de1383a7`: batch-19 residual w003..w053継続・
  WIN-CONTINUE事前登録) がpushされた。本Partはいずれのパスにも
  触れていない (非接触維持)。
- verdict消費: **ゼロ**。canonical cache (6,182行 `0b594f7e…`) 書込み
  ゼロ。19 unconsumed closure WIN候補 (b018/d002/e002/f017/g018/j033/
  h045/z003/n005/n006/p002/p003/r001/r002/q042/v001/v002/w001 (s5 63802)/
  w002 (s5 109169)) は読み書きとも非接触 (scrutiny owner C++ gate
  `9193f5b6…`のまま)。
- route statement (条件付き・verdictではない): class 12457 (rank 17・
  route-alive) の費用子54すべてがラベルを持つ (既知子 {126899: LOSS} +
  probe 53・採用は一切行っていない)。53 LOSS行の採用が成立すれば
  class 12457の全子LOSS閉包ルートが確定するが、これは別宣言
  adoption Partの仕事。次のroute-alive closure候補はrank 18 class 12643
  (runner-up・backups 25835/31600もroute-alive機械検証済み)。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 12457・全53キーは本時点で
  **UNKNOWNのまま** (nodes数は簿記であり勝敗ではない)。
- 本status update observed HEAD-before-push: push直前に最新mainを
  再fetchし、note blob lock `0e0ec792ea3ee16ef700292f858e097078e9bcc3`
  を再照合する (競合時は本節を追記し直す)。

## Part BI (solver, amendment 2026-11-23): batch-20 (class 12457) 53-LOSS canonical adoption + reaudit（実行前に出版・verdict採用は53 LOSS行のみ）

長期レーン (n11 central-reply closure) のPart BIとして、published batch-20 (Part BG,
class 12457) の53 LOSS行をcanonical exact-S5 verdict cacheへ計上する単一オーナー実行を
宣言する (batch-20 53-LOSS adoptionというスコープに対して本amendmentより先にmainに
存在する対抗宣言/amendmentがある場合は本宣言を破棄して着手しない。branch / PRは作らない)。

- 引き継ぎ (published byteに基づく): Part BGはclass 12457 (rank 17・route-alive) の
  53 unknown費用子を2-pass node-exactで完走し、53/53 honest label result=2 (LOSS) を
  出版した (commit A 358cac13 scaffold 69 / B 564cc66a outputs 122 / C 928546df
  README ad0c3eec + MANIFEST d0ef293b 191行・row-audit 1dcb7fb8)。同READMEの消費規則は
  「53 LOSS行の採用は別宣言adoption Partがpinned fail-closed mergerで実行」であり、
  本Partがその役割を履行する。batch-20にWIN行は1行も存在しない (absence gate) なので、
  採用パケットは完全解決パケットと一致する (full == loss・機械主張)。
- 対象: `research/experiments/n11-centralreply-class12457-loss53-adoption-reaudit-20261123/`。
  BASE canonical exact-S5 verdict cache 6,182行 sha256 `0b594f7e…` (Part BC採用正本)
  + increment 53行 → 採用後canonical 6,235行 (予想: WIN 158 / LOSS 6,077・conflict 0)。
- 機材 (全てpublished byte・実行時にsha照合): union merger `s5_union_merge.py`
  sha256 `90711961…` byte-copy pin (WIN/LOSS conflict検出時の出力拒否gate込み・3回実行
  byte一致) / maker `make_increments_batch20.py` (Part AV版 04bde073のbatch-20 adapt・
  本宣言後に出版してから実行) / refresh `refresh_adoption_12457.py` (Part BC版
  d6bb2374のadapt・cache sha期待値はcache自体から機械抽出・graph 54f9c364 / update8
  b658290a / Board 954d3a10 / policy 78655e94 / quarantine 81d23160) / delta extractor
  `compare_deltas_batch20_adoption.py` (Part AV版 92d83671のadapt・本宣言後に出版して
  から実行) / batch-20 kit 191ファイル (MANIFEST d0ef293b・row-audit 1dcb7fb8・
  batch-keys efb40b1b) / BASE reaudit 3出力 (refresh-summary 5f3a09c6・closure-classes
  52ec3d4b 808行・per-root-coverage 1f54065a)。
- 本hostの事前preflight (read-only・宣言に先行して実施した点を誠実記録): published
  Part BC BASE refresh (d6bb2374) を本hostで再実行し3出力ともpublished byteとsha一致
  で再現済み (5f3a09c6 / 52ec3d4b / 1f54065a)。read-only機械検査で batch-20 key集合 ==
  class 12457のBASE-unknown費用子53個 (既知子は {126899: LOSS} のみ・update8 receipts
  不在) を確認済み。
- gate群 (fail-closed・全stage): 53行の2-pass raw独立再検証 (p1==p2 node-exact・
  `# replay_done`・result 2・budget 15M・stones 5・legal/(lo,hi)照合・WIN行不在
  absence gate・14 truncated断片はverdict行なし) / BASE不在53/53・quarantine 0 /
  increments manifest (53 resolved / 53 LOSS / 0 WIN / full==loss /
  win_scenario_exists false) / merge conflict 0・採用行は追加のみでBASE行はbyte不変 /
  refresh再実行 (class_status_counts・Board fail-closed子境界検証・root 27は119/119
  不変gate・per-root coverageはpublished BASEと一致して改善のみ) / delta extractor
  (status transition ledgerはunknown->{unknown, free_now}のみ・excluded_now flip空・
  newly free集合==機械計算集合かつ12457を含む・class 12457のBASE-unknown 53子==batch-20
  key集合で全行解決・holder classのunknown_now減少は自身のmembership分のみ・closure
  候補表churn: 12457退出) / 各stageのtamper battery (計5種以上・検出後復元byte一致)。
- route statement (条件付き・採用後のscheduling quantitiesに過ぎない): 53 LOSS行採用に
  よりclass 12457の費用子54個すべてがcanonical上LOSSとなる (既知子 126899 + 53行)。
  refresh再実行が54子すべてのBoard fail-closed検証にPASSすればclass 12457はunknown
  人口から退出しBoard検証free classとなる (37→38番目候補・機械判定待ち)。unknown class
  数34,499→34,498・closure候補表808→807の見込み・被覆の変化は機械実測で確定する。
  被覆・secured・root勝敗の主張はrefresh再実行とextractor gateが出す分類deltaのみ。
- 消費規則: 本Partは53 LOSS行のみをcanonical (6,182→6,235) として採用する。WIN行は
  batch-20に存在しないので採用場面はない。19 unconsumed closure WIN候補 (b018/d002/
  e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042/v001/v002/w001/w002)
  は読み書きとも非接触 (scrutiny owner C++第二実装 gate pin 9193f5b6のまま)。
  canonical chain外の投影は作らない。
- 不接触: Part BH (batch-19 residual w003..w053・宣言 de1383a7・別実行) には一切触れない。
  batch-21 (class 12643・将来の別宣言)・y=18/y=19 fast lane・K1058系は非接触。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4 は本Partのどの時点でもUNKNOWNのまま。nodes数・簿記量を
  勝敗として読まない。
- 実験dir: `research/experiments/n11-centralreply-class12457-loss53-adoption-reaudit-20261123/`。
- 本amendment observed HEAD-before-push: 1d46f883a1fea022128a1bb28d28713b75dcbcf6
  (push直前にnote blob sha1 4e09fd8374744fa9ce8adfafa4ad92c3ccaa0cfdを再照合し、
  競合時は再fetchして本節を追記し直す)。

## Part BI status update (2026-11-23, solver): batch-20 53-LOSS採用完了 - canonical 6,235行・class 12457は38番目のBoard検証free class (UNKNOWN担保不変)

Part BI (宣言 `879e898c`) どおり、batch-20 (class 12457) の53 LOSS行を
canonical exact-S5 verdict cacheへ採用し、refresh再監査・delta extractor全gate
を完走した。

- publish-then-execute順序の履行: 計算機材4 scriptを先にmainへ出版
  (commit `7bdf327a093670a24d04220c95b8495e452a9896`): maker `81a6b7ec…` /
  delta extractor `605e040a…` / union merger byte-copy pin `90711961…` /
  refresh `2f77a8bb…`。出版bytesをcommit-pinned raw fetchで本hostに取得・
  sha照合 (4/4 byte一致) の上、4段階すべてを出版後に再実行し、出版前実行
  (同一host・同一bytes) との出力byte一致を機械確認した。
- maker全gate PASS: increment 53行 (x001..x053全LOSS) sha256
  `554f726129cce48b09fcbc5edaf4b40fb6dd4332182e4c62594455c47bc0a163`・
  manifest `82a5f866…` (full==loss・WIN不在absence gate・枯損行不在
  absence gate・BASE (6,182行 `0b594f7e…`) 重複0・quarantine 0・kit 191/191・
  row-audit `1dcb7fb8` 一致・総ノード175,842,846/pass両pass一致)。
- merger (selftest PASS): BASE 6,182行 `0b594f7e…` + 53行 =
  **canonical 6,235行** (WIN 158 / LOSS 6,077・dup 0・conflict 0) sha256
  `f6649fe36425f9a4e959b058392746b73e655cda0fcfa223befafd8905d67d26`
  (256,885 bytes) を
  `output/merged-exact-s5-chain-…-plus-batch20loss53-20261123.cache`
  に出版。merge 3回byte一致 (audit run1=run2=run3 `06151e6d…`)・出版後
  再実行もbyte一致 (post-audit `d748bbbf…`、記録される入力path文字列
  以外はrun1と完全一致)。
- refresh再実行 (~60s) 4出力byte一致: refresh-summary `d9d18fc2…`・
  closure-classes `d57a7609…` (807行)・per-root-coverage `bc409e63…`・
  probe-worklist `3152855d…` (3.75MB・**Part AH/AO/AP/AS/AV/BC先例どおり
  不出版・sha記録のみ**)。
- delta extractor全gate PASS: decomp `31078669…`・flips=[]・
  new_free=[12457]厳密一致・class 12457のBASE-unknown 53子==batch-20
  key集合で全行解決・update8_resolved +53・changed_rows [central|2,
  central|5]・closure候補表の退出は[12457]のみ (closure gate)。
- 機械確定 (分類delta・勝敗ではない): **free_now 37→38** (class 12457
  は費用子54個すべてLOSS (既知子 {126899: LOSS} + 53行) かつBoard
  fail-closed子境界検証PASSで、38番目のBoard検証free classとしてunknown
  人口から退出)・**unknown 34,499→34,498**・closure候補表**808→807**・
  root 27 (known-loss-baseline) は**119/119不変**・class 23101は両表
  unknown_now 1のまま・class 12643はunknown 53のまま (**rank 18→17に
  繰り上げ**: 次のroute-alive closure候補・batch-21は別宣言が必要)。
  update8簿記: remaining 31,779→31,726・resolved 80→133・joint greedy
  38,978→38,415・worklist 64,872→64,808。nodes数・worklist数・greedy数
  を勝敗として読まない。被覆・secured・root勝敗の主張はしない。
- tamper battery 10種すべて出版前に検出 (increment verdict flip / raw行
  改変 / manifest WIN注入 / refresh-summary差し替え / batch-keys差し替え /
  scenario cache flip / merger cross-file conflict (出力拒否) / status.log
  最終行改変 / kit MANIFEST gate / extractor sha pin)・検出後復元byte一致。
- 誠実な修正記録: outputs commit `04a2335e…`のmessageはprobe-worklistを
  「直後の別commitで出版」と予告していたが、repo慣例 (3.7MB worklist
  不出版・sha記録のみ) に従い不出版とした (sha `3152855d…` はREADMEと
  本noteに記録)。
- verdict不消費: 採用は53 LOSS行のみ (fail-closed merger経由)。batch-20に
  WIN行は存在しない (absence gate) のでWIN採用場面はない。19 unconsumed
  closure WIN候補 (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/
  p002/p003/r001/r002/q042/v001/v002/w001 (s5 63802)/w002 (s5 109169)) は
  読み書きとも非接触 (scrutiny owner C++第二実装 gate pin `9193f5b6…`
  のまま)。
- 並走記録 (非接触維持): 本Partのscripts出版後にfast-lane 2コミット
  (`22dc3dd2`, `ecc96264`) とPart BI outputs A (`04a2335e`) がpushされた
  (`ecc96264` のmessageが本Part scripts commitを非接触と明記)。Part BH
  (batch-19 residual w003..w053・宣言 `de1383a7`) の採用コミットはまだ
  mainに無い。batch-21 (class 12643) は本Partでは着手していない。
- experiments dir: `research/experiments/n11-centralreply-class12457-loss53-adoption-reaudit-20261123/`
  (scripts `7bdf327a` / outputs A `04a2335e` / READMEは本status update
  commitで出版)。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 12643は本時点で
  **UNKNOWNのまま**。
- 本status update observed HEAD-before-push: push直前に最新mainを再fetch
  し、note blob lock `e398f02b2c7cabe20768944109e14dfbef432bc8` を再照合
  する (競合時は本節を追記し直す)。

## Part BJ (solver, amendment 2026-11-23): closure class 12643 exact-S5 probe batch 21 (実行前に宣言・verdict不消費)

長期レーン (n11 central-reply closure) の次のsolverバッチとして、batch-21
(class 12643) を宣言する (batch-21 / class 12643 probeというスコープに対して
本amendmentより先にmainに存在する対抗宣言・amendmentがある場合は本宣言を
破棄して着手しない。branch / PRは作らない)。

- 引き継ぎ (機械確定・Part BI status updateの分類delta): class 12457採用
  (canonical 6,235行 `f6649fe3`・free_now 38) の結果、closure候補表
  (`d57a7609…`, 807行) でclass 12643 (mask `[1152921504606847088, 0]`) は
  **rank 17に繰り上げ**られた (unknown 53・groups 4・first group first=4/
  third=5)。rank 1..16は反駁証拠保持または未着手を含む既知の状態であり、
  Part BG宣言 `b4c4ac2d` の選定規則 (既知WIN費用子を持つクラスは除外) を
  引き継ぐ。
- 対象: `research/experiments/n11-centralreply-closure-class12643-batch21-20261123/`。
  closure候補表rank 17クラス12643の未確定canonical S5子53キー
  (Part BI scenario probe-worklist `3152855d` のserving_class=12643行
  53行・probe_order順・Board再計算の合法手数74..96固定)。
- 本hostの事前preflight (read-only・宣言に先行して実施した点を誠実記録・
  2026-11-23実施): (1) 53行53キー一意 (キー重複なし機械確認)。(2) 採用後
  canonical cache 6,235行 (`f6649fe3`) に53キー **0 hits**。(3) quarantine
  registry (`81d23160…`) にlo文字列レベルで **0 hits**。(4) route-alive
  機械証拠: published Part BI closure候補表 (`d57a7609…`) にclass 12643が
  rank 17で残存していること自体が、refresh規則 (既知WIN費用子を持つクラス
  は除外される) による「既知WIN子不在」の機械帰結である。
- 機材 (全てpublished byte・実行時にsha照合): pinned replica `jsreplay.js`
  sha256 `84585617…` (batch-19/20正本からbyte-copy)・`runbatch.sh` `f591f8c2…`・
  `runwave.sh` `8efd78c2…`・drive driver (batch-20版 `0b1d6b38…`相当品を
  batch-21へadapt)・row audit (`3197c4dc…`相当品をbatch-21へadapt)・
  key maker (batch-20版 `1dceb05e…`相当品をbatch-21へadapt・canonical
  6,235行0-hit gate・quarantine gate・prior-packets overlap gate・
  route-alive gate込み)。
- val-gate (実行前・本host): batch-19/20と同一の4アンカー (at2m 2行 →
  result 0 / nodes 2,000,000 node-exact・15m 2行 → result 2 /
  (2,3651,923)/(2,5,040,200) node-exact・禁止四角 95,670 x4・
  `# replay_done` x4)。published val-gate基準線とnode数完全一致を実行の
  前提条件とする。
- protocol: 2-pass fresh-cold node-exact・budget 15,000,000・1 solver / 1 row /
  1プロセス・publish=ALL・worker最大2 (2-core host)・drive起動は260秒有界。
- 停止規則 (事前登録): 決定論mismatch → 即時HARD-STOP rc=42 (batch全体停止)。
  WIN (result 1) → 即時HALT rc=45・honest WIN labelで記録 (verdict不消費・
  採用はscrutiny owner C++第二実装 gate pin `9193f5b6…`のまま)。
  budget枯渇 (result 0) → honest UNKNOWN (同条件再probe禁止)。
- 消費規則: 2-pass一致かつresult 2 (LOSS) のキーのみincrement cache候補。
  採用は別宣言adoption Partがpinned fail-closed union merger (byte-copy pin
  `90711961…`) で実行する。本batch単体では閉鎖・被覆・secured・root勝敗の
  主張を一切しない。
- 不接触: Part BH (batch-19 residual w003..w053・宣言 `de1383a7`・別オーナー)
  には一切触れない。batch-20 (採用済み・Part BI完了) への追記もしない。
  y=18/y=19 fast lane・K1058系・sixth-cost系は非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 12643 (53キーすべて含む) は本Partのどの時点でも
  UNKNOWNのまま。nodes数・legal数・worklist数を勝敗として読まない。
- 本amendment observed HEAD-before-push: `e7c7595425442c3af35ad4dd74445b515dd071a7`
  (session log Continuation 48直後のmain・push直前にnote blob sha1
  `28a9c7b952e25537d77b15136463e06f5f1a75d4`を再照合し、競合時は再fetch
  して本節を追記し直す)。

- 2026-11-23 04:14Z Part BJ実行開始amendment（solver・execution start）: batch-21（class 12643・53キー）の宣言済みプロトコル `2bf5d529` に基づく2-pass fresh-cold probe実行を、本セッションを実行オーナーとして開始する。preflight（本amendment出版前・read-only・honest record）: published scaffold commit `85d0c4d7`（scripts 6・input 54・val-gate 12の72ファイル）をcommit-pinned rawで鏡像し、git blob sha1 18件照合＋pinned jsreplay SHA-256 `84585617…` 合致を機械確認。val-gate 4-anchorを本ホストで再実行し4/4 node-exact一致（budget/result/nodes比較・forbidden quadruples 95670 x4・wall_s除外: at2m 2本はresult 0/nodes 2000000、15m 2本はresult 2/nodes 3651923・5040200）。以降はpublished drive_batch21.sh（bounded invocation・2 worker max・2 solver process/host以下）を完走または事前登録STOP条件（mismatch rc=42・WIN-HALT rc=45・exhaustion honest UNKNOWN）まで実行し、outputs（status.log・raw 2-pass・row-audit）をpublishする。並走への留意: 本amendmentがmainに観測できる時点で本セッションが実行中である。実行成果の出版が観測されないまま本amendmentから長時間経過した場合（host消失等）は、takeover amendmentを先に出版したセッションが単一実行オーナーを引き継げる。標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 12643（53キー含む）はどの時点でもUNKNOWNのまま。本amendment observed HEAD-before-push: `6bc4d65865c53afa6d12f29299a7895fab864979`（inversive-plane lane commit・非接触）。push直前にnote blob sha1 `23ea8560bbd191d8c1ba0408a8dc5637d999e17b`を再照合し、競合時は再fetchして本節を追記し直す。
## Part BJ status update (2026-11-23, execution owner): batch-21 (class 12643) drive-1完了 - 事前登録WIN-HALTがa003で発火 (honest WIN label・verdict不消費)・49キー残留は新宣言待ち

Part BJ (宣言 `2bf5d529`) のプロトコルどおり、batch-21 (class 12643・
53キー) の2-pass fresh-cold probe drive-1を実行し、事前登録停止規則の
WIN-HALT rc=45が a003 のhonest WIN labelで発火したため、そこで停止した。
出版3コミットすべてfetch-back byte検証済み。

- drive-1 (status.log先頭行 2026-11-23T04:09:23Z・最終行 04:11:41Z・
  worker最大2・2番目workerはhost-timeout killで運用終了): 完走 two-pass
  node-exact行は4行。a001 LOSS 2,392,778 / a002 LOSS 6,755,079
  (p1==p2 byte一致・wall_s 67/67) / **a003 WIN (replay result 1) nodes
  5,021,280 two-pass node-exact** (key (10412339930666631168,4)・s5
  115192・wall_s 51/50) → 事前登録WIN-HALT rc=45発火・verdict不消費 /
  a004 LOSS 4,151,964。mismatch 0・exhaustion 0 (budget枯槍なし)。
- a006 はUNPROBED: 2番目workerが260秒有界driveのhost-timeoutでkillされた
  (p1: complete single-pass bookkeeping行 result 2 / nodes 8,008,743 は
  「NOT evidence」の簿記でありverdictではない。p2: truncated
  headers-only断片で `# replay_done` なし)。将来のcontinuationで
  fresh-cold再probeを実行するまで a006 は完了行として数えない。
- 残り49キー (a005..a053) は未着手fresh。batch-21 residualの追加probeには
  Part BH (batch-19 residual) と同型の新宣言 (preflight・scaffold再利用・
  val-gate再実行込み) が必要で、本status updateでは追加probeを一切しない。
- row audit (winhalt専用新script `scripts/row_audit_batch21_win_halt.py`
  sha256 `08fff912…` 同時出版): `output/row-audit-winhalt.json` sha256
  `5bb403ad…` 3回byte一致・全gate PASS (probed=4・loss_rows
  [a001,a002,a004]・win_rows [a003]・mismatches 0・exhausted []・
  fragment_key semantics: a006 evidence=false probed=false・
  unprobed_count 49)。scaffold同梱のfull-row auditは完走residual用の
  end-state auditとしてそのまま残存する。
- 出版 (全てcommit-pinned raw fetch-back byte一致): scaffold `85d0c4d7`
  (72ファイル・72/72) → outputs `0022c8c5` (raw 2-pass 8本 + status.log +
  row-audit json + audit script 併せ13ファイル・13/13) → README +
  MANIFEST-sha256.txt (85エントリ) `a38153a8` (README `27dd1abf…` /
  MANIFEST `548f25df…`)。experiments dir:
  `research/experiments/n11-centralreply-closure-class12643-batch21-20261123/`。
- verdict不消費ゼロ: a003 のWIN labelはhonest recordのみで採用しない
  (scrutiny owner C++第二実装 gate pin `9193f5b6…` 不変)。a001/a002/a004
  の3 LOSS行は採用候補のみで、採用は別宣言adoption Part (pinned
  fail-closed union merger byte-copy `90711961…`) が行う。canonical 6,235行
  (batch-20採用済みBASE `f6649fe3…`) はread-only・書き込みなし。19 unconsumed
  closure WIN候補も非接触。
- 条件付き書記 (closure・被覆・secured・root勝敗の主張ではない): a003
  (WIN honest label) はclosure候補class 12643の費用子であるため、このWIN
  行が将来採用された場合にのみ、closure selection route pointerはrunner-up
  rank 18 class 25835へ移動する (backup 31600)。class 12643のunknown人口は
  本時点では一切変化しない。
- 並走記録 (誠実・両方向): 本実行はstatus.log先頭行 04:09:23Zで開始済み
  (scaffold `85d0c4d7` の出版 04:08:04Z が先行・並走amendment自身が当
  scaffoldのcommit-pinned mirrorをpreflightに使用) のところ、並走セッション
  が 04:12:55Z に「Part BJ実行開始amendment」`2f6086dd` (本ノート直前の
  節・note blob lock `23ea8560…` を上書き) を出版し、同kitでの
  mirror/preflight・execution ownerの主張を記録した。同一scaffold・同一
  val-gate基準線に対する並走実行の成果がpublishされた場合は、独立
  cross-verification (期待される相違はwall_sのみ) として両方向記録に
  取り込む。first-completer規則 (y17 part2先例) に従い、本status update
  とoutputs出版 (`0022c8c5`, `a38153a8`) によりPart BJ executionを
  完結させる。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・**class 12643 (53キーすべて)**
  はどの時点でもUNKNOWNのまま。nodes数・worklist数・rank順位を勝敗として
  読まない。
- 本status update observed HEAD-before-push:
  `7055cb450fa9b2321f2e33300d2e8cdb3defce6a` (README/MANIFEST出版 `a38153a8`
  の後に対局外のinversive-plane laneがpushした非接触commit・noteは不変)。
  push直前に最新mainのnote blob sha1
  `83c59d9221e7a624ca81b8f876d903d54419aaa2` (並走amendment `2f6086dd`
  適用後) を再fetch・再照合し、競合時は本節を追記し直す。

## Part BJ addendum (2026-11-23): 第二ホスト同時再現の取り込み (両方向記録・status update並走節の履行)

並走セッション (実行開始amendment `2f6086dd` の出版者側) が本batch-21の
drive-1を第二ホストで 04:13:00Z..04:17:20Z に実行完了した。
**正本 (`0022c8c5`) と全10 rawファイルが wall_s フィールド以外で完全一致**
(a001 LOSS 2,392,778・a002 LOSS 6,755,079・**a003 WIN 5,021,280 →
同一キーで事前登録WIN-HALT発火**・a004 LOSS 4,151,964・a006 p1単一pass
簿記 8,008,743 同一・211 bytesのtruncated断片は正本とbyte完全一致)。
正本 `row_audit_batch21_win_halt.py` も第二ホスト出力に対してPASS・
`row-audit-winhalt.json` は正本とbyte完全一致 (`5bb403ad…`)。
詳細は `research/log/2026-11-23-b21-drive1-second-host-replication.md`
(commit `ad487a2f`)。verdict不消費・canonical 6,235行 (`f6649fe3…`) 不変。
閉鎖・被覆・secured主張なし。標準11×11空盤・19 central-reply roots・
二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 12643
(53キーすべて) はどの時点でもUNKNOWNのまま。

## Part BK (verifier, amendment 2026-11-23, 実行前に宣言): batch-21 a003 WIN行の第三実装交叉検証 (verdict不消費)

batch-21 (Part BJ) で出版されたWIN行 a003 (canonical `0022c8c5`・
2-pass fresh-cold node-exact・result 1・nodes 5,021,280) に対し、前例
(Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AZ/BF) と同じpinned第三実装
(non-df-pn AND/OR minimax) によるverdict-level交叉検証を、本セッションが
単一オーナーとして実行する (同一スコープの対抗宣言・amendmentが本
amendmentより先にmainにある場合は本宣言を破棄して着手しない)。

- 対象: `research/experiments/n11-centralreply-closure-b21win-thirdimpl-20261123/`。
  target 1行: **a003** (s5 115192・key (10412339930666631168, 4)・legal 82・
  replica_result 1・replica_nodes 5,021,280・holder class 12643 (unknown)・
  membership_class_count 3・published batch-21 batch-keys `1f9346a7…`)。
- 機材 (全てpublished byte・実行時にsha照合): third_impl.js `08ea958f…`・
  verify_tbl.js `c8c52528…`・jsreplay.js replica `84585617…`・runner
  `run_thirdimpl.sh` (BF正本byte-copy)・maker (BF `20d52c75…`をbatch-21
  正本sourcesへadapt)・audit gate battery (BF `fa7dd5e6…`を単一targetへ
  adapt)。
- 前提ゲート (fail-closed・全て機械検査): maker 3回実行byte一致・sources
  sha pin (batch-keys `1f9346a7…`・status-b21.log・README-b21・canonical
  a003 p1/p2 raw・published input CSV byte-equality (scaffold `85d0c4d7`)・
  BF published anchor/negative CSV byte-equality (provenance AR→BF→BK))、
  raw 2-pass node-exact (決定性field比較)・result 1 in-budget、
  status.log/README 3-way照合 (batch-21形式: a003 PASS行・WIN-HALT行・
  READMEのa003 WIN文言・nodes 5,021,280)。
- 実行protocol: anchors k02a (WIN 9,106,337/4,991,527)・l1a (LOSS
  7,660,602/3,951,175) の本ホストnode-exact再現、negatives ng1/ng2の
  GATE_FAIL確認、rules gate (replica quads 95,670 == third quads 95,670・
  triples mismatch 0)、target a003は1行=1solver=1プロセス・cap
  300,000,000・wallcap 240s・--memo-power=22・a/b 2回のdeterminism gate
  (result/expansions/ttHits/reason 同一必須)・逐次実行。wall超過は
  honest wall-inconclusiveとし検証主張としない。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・**verdict不消費**
  (a003の採用判断は引き続きscrutiny owner C++第二実装 gate pin
  `9193f5b6…` のまま)。第三実装verdictがcleanにreplica verdictと一致
  した場合は「一致した」事実のみ記録し、clean不一致はdivergence
  evidenceとして記録するが本レーンではverdictを書き換えない。
  開鎖・被覆・secured・root勝敗の主張をしない。
- 不接触: canonical cache (6,235行 `f6649fe3…`) への書き込みなし・
  19+1 unconsumed closure WIN候補 (既存19 + a003) の採用状態不変・
  Part BH (`de1383a7`)・batch-20採用済みBASE・batch-21 residual 49キー
  (fresh・未着手) に一切触れない・y18/y19 fast lane・K1058系・
  inversive-plane/k=8 lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 12643 (53キーすべて)
  は本Partのどの時点でもUNKNOWNのまま。nodes数・expansions数・ttHits数
  を勝敗として読まない。
- 本amendment observed HEAD-before-push: push直前に最新mainを再fetchし
  note blob lockを再照合する (競合時は本節を追記し直す)。

### Part BK status update (2026-11-23, execution host = 本レーン continuing session)

宣言 (note amendment commit `d93256ae`) どおり、宣言後に本hostが
published batch-21 WIN行 a003をpinned第三実装で解き、出版まで完了した
(verdict不消費)。

- 実行: pinned `third_impl.js` (`08ea958f…`)・1行=1 solver=1 process・
  cap 300,000,000・wallcap 240s・`--memo-power=22`・全target/anchor
  a/b 2回・逐次実行。**targets 1/1 clean WIN (result 1)・replica verdict
  一致 1/1**: **a003 third-impl WIN 5,806,719 expansions / 3,248,352
  ttHits** (replica 5,021,280 nodes・ratio 1.16・key
  (10412339930666631168, 4)・s5 index 115192・legal 82)。a/b pair
  result/expansions/ttHits/reason同一 (determinism gate PASS・
  16.55s/16.57s)。LOSS 0・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
  pass-one総expansions 5,806,719。
- battery順序: negatives ng1/ng2が設計どおりfail-closed文言
  (ng1 GATE_FAIL "legal count mismatch: derived=87 declared=88"・
  ng2 GATE_FAIL "stone count mismatch: bits=5 declared=6")
  → anchors k02a WIN 9,106,337/4,991,527・l1a LOSS 7,660,602/3,951,175
  がpublished第三実装値にnode-exact再現 (a/b同一)
  → target a003逐次実行 → rules gate → audit。
- rules gate: verify_tbl replica quads 95,670 == third-impl quads 95,670・
  195,044 triples mismatch 0 (`output/rules-gate.txt`)。
- maker `make_inputs_bk.py`: 全gate PASS・tamper battery 3/3検出
  (T1 maker sha-pin ABORT (status.log tamper)・T2 audit det-pair
  DIVERGENCE (verdict flip)・T3 audit G0 (input legal tamper)・
  scratch copyで実施・実験filesはrestore byte-verified)。
  source pins: batch-21 batch-keys (53キー・class 12643)・owner正本
  raw 10ファイル (outputs `0022c8c5`) + 本レーン第二ホスト再現raw
  10ファイル (log `ad487a2f`)・それぞれ2-pass node-exact +
  `# replay_done` + result 1 in-budget・status/README 3-way照合
  (batch-21形式: a003 PASS行・WIN-HALT行・nodes 5,021,280・README
  a003 WIN文言)。
- audit `audit.py`: **43/43 gates PASS**・3回実行byte一致 (schema
  `n11-centralreply-closure-b21win-thirdimpl-audit-v1`)。verdict
  agreement 1/1 (WIN=1)・wall_inconclusive 0
  (`output/audit-summary.json`)。
- 出版: 実験dir
  `research/experiments/n11-centralreply-closure-b21win-thirdimpl-20261123/`
  を3コミットでmainに反映: A `f15112a6` (scaffold: scripts 6 +
  inputs 6 + sources 10: README-b21・batch-keys-b21・status-b21・
  published-input・published-input-bf 4・raw 2) / B `7be47e99`
  (solver outputs 14: target a/b 2・anchors 4・negative 2・rules-gate・
  status.log・audit-summary・audit-run1.json/txt/2.txt) /
  C `4839be4b` (README `9faa30ca` + MANIFEST-sha256 36行 `56d5668b`)
  = publication complete。**fetch-back 38/38 byte一致**
  (publication commit `4839be4b` 固定rawで全ファイル照合)。
- 意味 (route statement・閉鎖主張なし): batch-21 drive-1のa003 WINが
  独立実装 (第三実装) でもclean WINで再現された (verdict-level補強
  文献)。a003はこれで (a) 二ホストで確認されたpinned df-pn replica
  2-pass node-exact rows・(b) 独立第三実装a/b determinism pairの
  双方で�付けられた**20番目のunconsumed closure WIN候補**となった。
  **verdict消費ゼロ**・採用判断は一切代行しない (scrutiny owner C++
  第二実装 gate pin `9193f5b6…` のまま)。canonical cache (6,235行
  `f6649fe3…`) 不変・いかなるcacheにも書込んでいない。batch-21
  residual 49キー (fresh・WIN-HALTにより未着手) ・Part BH
  (`de1383a7`)・batch-22候補 (class 25835) には本Partでは触れていない。
- 標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 12643 (53キーすべて・a003を含む)
  は本Partのどの時点でもUNKNOWNのまま。nodes数・expansions数を
  勝敗として読まない。

## Part BL (solver, amendment 2026-11-23, 実行前に宣言): closure class 25835 exact-S5 probe batch 22 (verdict不消費)

batch-22はclosure候補表の**rank 18 class 25835**（mask
[1152921504606982144, 8]・groups served (12,17)(12,67)(15,20)(15,75)・
cost 53子すべてunknown・known children {}・20-unconsumed-WIN交積0・
known WIN子なし）を最初のroute-alive候補として選定する。実行前に本
amendmentを出版する (publish-then-execute)。

- 選定根拠 (published baseから再導出・prose不使用): re-ranked closure
  候補表 = 807 classes (class 12457はPart BI採用で退出・closure表
  `d57a7609…` 807行と全行一致cross-check)。ranks 1..16 (23101/16757/
  20421/16371/30345/12264/5473/2634/8785/1518/8106/16930/5830/16131/
  16513/5687) は従来どおり反駁済み (19-WIN交積またはknown WIN子:
  5830はreceipt WIN 5子 {126017,131631,162106,197665,206386}・5687は
  receipt WIN子 {209644}・rank 1 class 23101のunknown集合は
  {745184}のみ)。**rank 17 class 12643 (batch-21対象) は今回の反駁
  証拠が確定**: unknown子集合と20-unconsumed-WIN集合の交積は厳密に
  {115192}、すなわちpublished Part BJ honest WIN行 a003 (key
  (10412339930666631168, 4)・Part BK第三実装で裏付け済み・verdict
  不消費のまま)。ranks 1..17がすべて反駁済みのため、**rank 18
  class 25835がpublished-table順で最初の全LOSS閉包ルート生存候補**。
  runner-up rank 19 class 31600 (mask
  [1152921505160495104, 32768]・cost 53子すべてunknown)・backup
  rank 20 class 10968 (mask
  [1152925919833292800, 0]・groups served 3) はともにroute-alive。
- preflight (fail-closed maker `make_batch22_keys.py` sha256
  `945ba254…`・全gate PASS・3回実行byte一致): 53キー k001..k053
  (s5昇順 91297..810380・legal 77..96・Board再計算53/53・membership
  分布 {2:1, 3:8, 4:44})。**canonical cache 6,235行 `f6649fe3…`
  hits 0/53・quarantine 0/53・prior 22 published packets
  (batches 1..21・1,087行・1,073一意) overlap 0・key id prefix "k"
  は22 packetすべてで未使用**。batch-keys.json sha256
  `b5f567bd…`・input CSV 53枚 (k001 = (10376293541461757952, 8)・
  legal 89・k053 = (1152921504606982144, 2056)・legal 91)。
  tamper battery 4/4検出 (T1 target rank pin 18->17→published表
  target行gate FAIL・T2 prior rows pin 1087->1086→gate FAIL・
  T3 a003 WIN行の除去→"WIN s5 set 19 != 20" gate FAIL・T4 rank-17
  evidence pin 115192->115193→20-WIN evidence gate FAIL)。
- val-gate (pinned `jsreplay.js` `84585617…`・本host): **4/4
  node-exact** (at2m 2キー result 0 nodes 2,000,000/2,000,000 budget
  exhausted・first-15m result 2 nodes 3,651,923・second-15m result 2
  nodes 5,040,200・禁止四角 95,670・wall_s比較外)。
- 実行protocol (batch-20/21流・publish-then-execute): scaffold
  (scripts 6: maker `945ba254` + drive_batch22.sh `df0ed0cd` +
  row_audit_batch22.py `c1ce40a6` + pinned jsreplay `84585617` /
  runbatch `f591f8c2` / runwave `8efd78c2`) を実験dir
  `n11-centralreply-closure-class25835-batch22-20261123/` に
  72ファイルでmainへ出版した後に実行する。2-pass fresh-cold replica・
  budget 15M・2 worker max・drive 260s有界・逐次はworker内のみ。
  事前登録stop rules: determinism mismatch rc=42 HARD-STOP・
  **WIN (replay result 1) は即時WIN-HALT rc=45 (honest WIN label・
  verdict不消費)**・budget exhaustion result 0はhonest UNKNOWN
  (15M同一条件での再probe禁止)。truncated pass filesは`# replay_done`
  なしはevidenceとせずfresh-cold再実行 (published completeness
  guard)。
- 採用規則: LOSS行のcanonical採用は**別宣言adoption Part**
  (pinned fail-closed merger `90711961`) でのみ。WIN行は20
  unconsumed closure WIN候補と同様にscrutiny owner C++第二実装
  gate `9193f5b6…` 待ちで本レーンは代行しない。
- 実行ownerの honesty: 本amendment出版後に本レーンがdriveを実行
  できない場合は、standard single-owner/takeover規則どおり次回以降
  の実行 (または並走実行のamendment先取) に委ね、重複実行・重複
  出版はしない。起動だけの成果扱いはしない。
- 不接触: canonical cache (6,235行 `f6649fe3…`) read-only・19+1
  unconsumed closure WIN候補 (a003込み) 不変・batch-21 residual
  49キー (fresh・a005..a053) 非接触・Part BH (batch-19 residual
  `de1383a7`) 別オーナーのまま・y18/y19 fast lane・K1058系・
  inversive-plane lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 25835 (53キー
  すべて)・class 12643は本Partのどの時点でもUNKNOWNのまま。
  nodes数・expansions数・legal数を勝敗として読まない。閉鎖・被覆・
  secured・root勝敗の主張はしない。
- 本amendment observed HEAD-before-push: `895ad14` (K1250
  inversive-plane item・非接触)。note blob lock `0fa1f479…` を
  push直前に再fetchして照合する (競合時は本節を追記し直す)。


## Part BL status update (2026-11-23): batch-22 (class 25835) drive-1 WIN-HALT at k002

- drive-1 (published declaration `8b27515b`の事前登録protocolどおり): 
  val-gate 4/4 node-exact (pinned jsreplay `84585617…`・本host)の後、
  k001・k002の順に2-pass fresh-cold・budget 15M・2 worker・drive 260s有界。
- **k002 WIN (honest label)**: key (1153484454560403456, 8)・s5 index
  150241・legal 87・membership 4。replay result 1・p1/p2 two-pass
  node-exact・nodes 10,542,704 (budget 15M内)・wall 113/112s。
  → 事前登録WIN-HALT rc=45でbatch停止。**verdict不消費** (本レーンは
  採用しない)。
- k001 fragment (UNPROBED): key (10376293541461757952, 8)。p1 complete
  single-pass bookkeeping result 0・nodes 15,000,000 budget exhaustion
  (honest UNKNOWN bookkeeping・**evidenceではない**)。p2はdrive
  260s timeoutによるtruncated断片 (`# replay_done`なし)。将来の
  continuationでfresh-cold再実行する (published completeness guard)。
  15M同一条件再probe禁止は完走行のみに binding。
- 残留UNPROBED: 51 freshキー (k003..k053) + k001再実行。
- 行監査: row-audit-winhalt (script sha256 `31e927e7…`): PASS・3回
  実行byte一致 (json `c6f7585c…`)・tamper battery 3/3検出 (p2 verdict
  反転 / status.log key-id改ざん / p1 key改ざん)。
- 意味 (route bookkeepingのみ): これにより**class 25835 (rank 18) の
  全LOSS閉包ルートも反駁証拠を持った** (class 12643・rank 17と同型)。
  k002は**21番目の unconsumed closure WIN 候補** (19旧 + a003 + k002)。
  採用判断はscrutiny owner C++第二実装 gate `9193f5b6…` 待ちで本レーン
  は代行しない。次batch選定は20+1-WIN交積の反駁簿記で行い、**rank 19
  class 31600 (mask [1152921505160495104, 32768]・cost 53子すべて
  unknown) がpublished-table順で次のroute-alive候補** (runner-up
  rank 20 class 10968)。被覆の閉鎖判定・secured主張はrefresh再実行+
  独立監査が行う。
- 出版: 宣言amendment `8b27515b`・scaffold commit A `106c469`
  (72ファイル・fetch-back 72/72 byte一致)・outputs commit B
  `2ed5b90` (7ファイル・fetch-back 7/7 byte一致)・commit C `a83da90`
  (README + MANIFEST-sha256 79行・fetch-back byte一致)。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 25835 (53キー
  すべて・k002を含む)・class 12643は本status update時点でもUNKNOWN
  のまま。nodes数・expansions数・legal数を勝敗として読まない。
- 本status update observed HEAD-before-push: `a83da90` (commit C)。
  note blob lock `eef9de1c…` をre-fetchして照合済み (競合時は本節を
  追記し直す)。

## Part BM (verifier, amendment 2026-11-23, 実行前に宣言): batch-22 k002 WIN行の第三実装交叉検証 + 本host pinned-replica再現 (verdict不消費)

batch-22 (Part BL) で出版されたWIN行 k002 (canonical outputs commit
`2ed5b90`・2-pass fresh-cold node-exact・replay result 1・nodes
10,542,704・budget 15M内) に対し、前例 (Part G/K/O/P/T/W/AA/AD/AG/AL/
AR/AZ/BF/BK) と同じpinned第三実装 (non-df-pn AND/OR minimax) による
verdict-level交叉検証を、本セッションが単一オーナーとして実行する
(同一スコープの対抗宣言・amendmentが本amendmentより先にmainにある
場合は本宣言を破棄して着手しない・本宣言時点でgrep cleanを確認)。

- 対象: `research/experiments/n11-centralreply-closure-b22win-thirdimpl-20261123/`。
  target 1行: **k002** (s5 150241・key (1153484454560403456, 8)・legal 87・
  replica_result 1・replica_nodes 10,542,704・holder class 25835 (unknown)・
  membership_class_count 4・published batch-22 batch-keys `b5f567bd…`)。
- 機材 (全てpublished byte・実行時にsha照合): third_impl.js `08ea958f…`・
  verify_tbl.js `c8c52528…`・jsreplay.js replica `84585617…`
  (batch-22正本byte-copy)・runner `run_thirdimpl.sh` (BF正本byte-copy
  `a0b77d83…`)・maker (Part BK `e664c4e6…`をbatch-22正本sourcesへ
  adapt)・audit gate battery (Part BK `f20d83b9…`をbatch-22向けadapt)。
- 前提ゲート (fail-closed・全て機械検査): maker 3回実行byte一致・sources
  sha pin (batch-keys-b22 `b5f567bd…`・status-b22.log `27dc7e7c…`・
  README-b22 `eab65d4f…`・row-audit-winhalt `c6f7585c…`・canonical
  k002 raw `baf468a3…`/`0ef25c4a…`・published input CSV byte-equality
  `2736d30a…` (scaffold `106c469`・MANIFEST `a83da90`行と一致)・BF
  published anchor/negative CSV byte-equality (provenance chain
  AR→BF→BK→BM))・raw 2-pass node-exact (決定性field比較)・result 1
  in-budget・status/row-audit/README 3-way照合 (batch-22形式: k002 PASS行
  `15000000,1,10542704`・k002 WIN-HALT行・row-audit win_rows [k002]・
  fragment k001 evidence=false・unprobed_count 52・READMEのk002 WIN文言・
  nodes 10,542,704)。
- 実行protocol (宣言時点で事前登録・順序も含め固定):
  1. **本host pinned-replica再現** (Part BJ第二ホスト再現 `ad487a2f`と
     同型の追加強化・Part BKにはなかった工程): pinned replica
     (jsreplay `84585617…`) でk002をbudget 15M・fresh-cold・逐次2回
     実行し、決定性fields (budget/result/nodes) のp1==p2・およびpublished
     raw fields (result 1・nodes 10,542,704) との一致をauditで機械検査
     する。exhaustion/mismatch/truncationはhonest記録のみとし検証主張
     としない (fail-closeした場合は実験を閉じdivergence evidenceとして
     記録する)。
  2. negatives ng1/ng2のGATE_FAIL確認 (fall-closed設計どおり) → anchors
     k02a (WIN 9,106,337 exp / 4,991,527 ttHits)・l1a (LOSS 7,660,602 /
     3,951,175) の本host node-exact再現 (a/b 2回)。
  3. rules gate: pinned `verify_tbl.js`でreplica quads 95,670 ==
     third-impl quads 95,670・triples checked mismatch 0。
  4. target k002は1行=1solver=1プロセス・cap 300,000,000・wallcap
     240s・`--memo-power=22`・a/b 2回のdeterminism gate
     (result/expansions/ttHits/reason同一必須)・逐次実行。wall超過は
     honest wall-inconclusiveとし検証主張としない。事前の機械予想は
     ない (expansions scaleについてはreplica nodes比から概算のみを
     宣言時に残さない・実測を待つ)。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・**verdict不消費**
  (k002の採用判断は引き続きscrutiny owner C++第二実装 gate pin
  `9193f5b6…` のまま)。第三実装verdictがcleanにreplica verdictと一致
  した場合は「一致した」事実のみ記録し、clean不一致はdivergence
  evidenceとして記録するが本レーンではverdictを書き換えない。閉鎖・
  被覆・secured・root勝敗の主張をしない。
- 不接触: canonical cache (6,235行 `f6649fe3…`) への書き込みなし・
  21 unconsumed closure WIN候補 (19旧 + a003 + k002) の採用状態不変・
  batch-22 residual 52キー (k001 fresh-cold再実行 + k003..k053 fresh) に
  一切触れない・batch-23選定 (rank 19 class 31600) は本Partの別工程
  ・Part BH (`de1383a7`)・batch-19/20/21系・fast lane (y18/y19)・
  K1058系・K1250-K1252 inversive-plane系・inversive-arc lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 12643・class 25835
  (53キーすべて・k002を含む) は本Partのどの時点でもUNKNOWNのまま。
  nodes数・expansions数・ttHits数を勝敗として読まない。WIN/LOSS採用は
  別宣言のadoption Part (pinned fail-closed merger `90711961`) でのみ。
- 本amendment observed HEAD-before-push: push直前に最新mainを再fetchし
  note blob lock (`94117f27…`・396,586B) を再照合する (競合時は本節を
  追記し直す)。

### Part BM status update (2026-11-23, execution host = 本レーン continuing session)

宣言 (note amendment commit `578638b3`・observed HEAD-before-push
`cc20473c4`) どおり、宣言後に本hostがpublished batch-22 WIN行 k002を
処理し、出版まで完了した (verdict不消費)。実験dir
`research/experiments/n11-centralreply-closure-b22win-thirdimpl-20261123/`。

- 実行 (宣言protocol順・逐次): pinned replica `jsreplay.js`
  (`84585617…`) でk002をfresh-cold budget 15M・逐次2回 → **p1/p2
  ともに result 1・nodes 10,542,704・two-pass node-exactかつpublished
  raw fields (result 1 / nodes 10,542,704) と完全一致** (wall 53s/54s・
  exhaustion/mismatch/truncationゼロ)。これでk002のreplica行はbatch-22
  実行hostと本hostの2ホストで同値再現。
- negatives ng1/ng2 GATE_FAIL文言どおり → anchors **k02a WIN
  9,106,337/4,991,527 (25.29s/25.51s)**・**l1a LOSS 7,660,602/3,951,175
  (21.68s/21.58s)** がpublished第三実装値にnode-exact再現 (a/b同一) →
  rules gate quads 95,670==95,670・triples 195,044 mismatch 0 →
  target **k002 third-impl clean WIN (result 1) 12,457,901 expansions /
  6,625,269 ttHits** (replica 10,542,704・ratio 1.18・a/b determinism
  PASS・34.04s/33.95s)・**replica verdict一致 1/1**・
  WALL-INCONCLUSIVE 0・DIVERGENCE 0。
- maker `make_inputs_bm.py` (`d560b8cd…`): 全gate PASS・4回実行byte
  一致・tamper 5/5検出 (T1a status-b22.log nodes改ざん→sha-pin ABORT・
  T1b README文言改ざん→sha-pin ABORT・T2 target raw verdict反転→audit
  det-pair DIVERGENCE rc=1・T3 input CSV legal改ざん→audit G0 rc=1・
  T4 replica両pass verdict反転→audit replica-verdict-vs-published
  rc=1・スクラッチcopyで実施・実験filesはbyte検証復元)。
- audit `audit.py` (`79f4b7e5…`): **50/50 gates PASS**・4回実行byte一致
  (schema `n11-centralreply-closure-b22win-thirdimpl-audit-v1`・
  gate内訳: input 5 + pins 3 + rows/count 2 + rules 2 +
  replica-thishost 7 + anchors 18 + negatives 2 + targets 10)。
- 出版 (全fetch-back byte一致): 実験dir 41ファイルを3コミットでmain
  に反映: A `5e3c180` scaffold 23ファイル (scripts 6 + inputs 6 +
  sources 11・fetch-back 23/23) → B `23d18c0` outputs 16ファイル
  (replica 2・targets 2・anchors 4・negative 2・rules-gate・status.log・
  audit 4・fetch-back 16/16) → C `32cf078` README + MANIFEST-sha256
  39行 (2/2)。
- 意味 (route statement・閉鎖主張なし): batch-22 drive-1のk002 WINが
  独立実装 (第三実装) でもclean WINで再現され、さらに本host fresh-cold
  replicaがpublished rawと完全一致した。k002 WIN labelはこれで
  (a) pinned df-pn replica 2-pass node-exact×2ホスト、(b) 独立第三実装
  a/b determinism pair の2系統で裏付けられた (**21番目のunconsumed
  closure WIN候補・verdict不消費**)。採用判断はscrutiny owner C++
  第二実装 gate pin `9193f5b6…` のまま。canonical cache (6,235行
  `f6649fe3…`) 不変。batch-22 residual 52キー・batch-23選定
  (rank 19 class 31600) には本Partでは触れていない。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 25835 (53キー
  すべて・k002を含む)・class 12643は本status update時点でもUNKNOWN
  のまま。nodes数・expansions数・ttHits数を勝敗として読まない。
- 本status update observed HEAD-before-push: `32cf078` (commit C)。
  push直前に最新mainを再fetchしnote blob lockを再照合する。


## Part BN (solver, amendment 2026-11-23, 実行前に宣言): closure class 31600 exact-S5 probe batch 23 (verdict不消費)

batch-23はclosure候補表の**rank 19 class 31600**（mask
[1152921505160495104, 32768]・groups served (24,29)(24,79)(25,30)(25,85)・
cost 53子すべてunknown・known children {}・21-unconsumed-WIN交積空・
known WIN子なし）を最初のroute-alive候補として選定する。実行前に本
amendmentを出版する (publish-then-execute)。

- 選定根拠 (published baseから再導出・prose不使用): re-ranked closure
  候補表 = 807 classes (closure表 `d57a7609…` 807行と全行一致
  cross-check)。ranks 1..16 (23101/16757/20421/16371/30345/12264/5473/
  2634/8785/1518/8106/16930/5830/16131/16513/5687) は従来どおり反駁済み
  (19-WIN交積またはknown WIN子: 5830はreceipt WIN 5子
  {126017,131631,162106,197665,206386}・5687はreceipt WIN子{209644}・
  rank 1 class 23101のunknown集合は{745184}のみ)。rank 17 class 12643
  (batch-21対象) はunconsumed-WIN交積 {115192} (Part BJ a003・Part BK
  第三実装裏付け済み)・**rank 18 class 25835 (batch-22対象) は今回の
  反駁証拠が確定**: unknown子集合と21-unconsumed-WIN集合の交積は厳密に
  {150241}、すなわちpublished Part BL honest WIN行 k002 (s5 150241・
  2ホストpinned-replica + Part BM第三実装で裏付け済み・verdict不消費
  のまま)。ranks 1..18がすべて反駁済みのため、**rank 19 class 31600が
  published-table順で最初の全LOSS閉包ルート生存候補**。
  runner-up rank 20 class 10968 (mask
  [1152925919833292800, 0]・cost 53子すべてunknown)・backup
  rank 21 class 16957 はともにroute-alive (maker内で機械検証)。
- preflight (fail-closed maker `make_batch23_keys.py` sha256
  `7b2c8e53…`・全gate PASS・**4回実行byte一致**): 53キー s001..s053
  (s5昇順 62435..924796・legal 78..95・Board再計算53/53・membership
  分布 {3:8, 4:45})。**canonical cache 6,235行 `f6649fe3…`
  hits 0/53・quarantine 0/53・prior 23 published packets
  (batches 1..22・1,140行・1,126一意) overlap 0・key id prefix "s"
  は23 packetすべてで未使用**。batch-keys.json sha256
  `2776acaf…`・input CSV 53枚 (s001 = (1152921505294712832, 32768)・
  legal 78・s053 = (1152921505160495104, 2129920)・legal 90)。
  **tamper battery 6/6検出** (T1 graph sha pin改ざん→drift ABORT・
  T2 CLASS_MASK 1bit反転→mask gate FAIL・T3 batch-22 prior packet
  pin 1bit反転→sha drift ABORT・T4 prior rows pin 1140→1141→gate
  FAIL・T5 rank-18 evidence pin {150241}→{150242}→21-WIN evidence
  gate FAIL・T6 graph実ファイル末尾1bit反転→sha drift ABORT・
  スクラッチcopyで実施)。
- val-gate (pinned `jsreplay.js` `84585617…`・本host): **4/4
  node-exact** (at2m 2キー result 0 nodes 2,000,000/2,000,000 budget
  exhausted・first-15m result 2 nodes 3,651,923・second-15m result 2
  nodes 5,040,200・禁止四角 95,670・wall_s比較外)。
- 実行protocol (batch-22流・publish-then-execute): scaffold
  (scripts 7: maker `7b2c8e53` + drive_batch23.sh `37bb126c` +
  row_audit_batch23.py `f45b124e` +
  **row_audit_batch23_win_halt.py `f55ae559` (汎用事前登録版・後述)** +
  pinned jsreplay `84585617` / runbatch `f591f8c2` / runwave
  `8efd78c2`) を実験dir
  `research/experiments/n11-centralreply-closure-class31600-batch23-20261123/`
  に出版してからdriveする。停止規則・消費規則はPart BLと同一
  (2-pass fresh cold budget 15M・mismatch→HARD-STOP・WIN→HALT rc=45
  (honest WIN label・verdict不消費・scrutiny owner待ち)・枯渇=UNKNOWN
  (15M同条件再探索禁止)・消費は別宣言adoption Part (pinned fail-closed
  merger `90711961`) 経由のみ・本batch単体では閉鎖・被覆・secured
  主張なし)。実行は次回以降のランが行う (起動だけは成果としない)。
- win-halt監査の事前登録 (batch-22からの構造改善): batch-22の
  win-halt row-auditはhalt後の事後スクリプトであった (k002/k001を
  固定記述)。batch-23では**汎用版 `row_audit_batch23_win_halt.py`
  をscaffoldに同梱して事前登録する**: completed/fragment/fileless
  の分類はすべてrawファイルの `# replay_done` 有無とstatus.logから
  導出し、haltするキーidは一切固定しない。WIN行が1つもcompleted
  に存在しない場合はGATE_FAIL (その場合はフル監査
  `row_audit_batch23.py` を使う)、fragmentキーの完全片側passは
  bookkeepingのみ (evidence=false・probed=false)、非completedキーへの
  verdict行は status.log上禁止、を機械検査する。
- 不接触: canonical cache (6,235行 `f6649fe3…`) read-only・
  21 unconsumed closure WIN候補 (19旧 + a003 + k002) の採用状態不変・
  batch-22 residual 52キー (k001 fresh-cold再実行 + k003..k053 fresh)
  に一切触れない・Part BM b22win-thirdimpl dir (`5e3c180..
  `32cf078`) 不変・Part BH (`de1383a7`)・batch-19/20/21系・fast lane
  (y19/y20)・K1058系・K1250-K1253 inversive-plane系・inversive-arc
  lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 12643・class 25835
  (53キーすべて)・**class 31600 (53キーすべて)** は本Partのどの時点でも
  UNKNOWNのまま。nodes数・legal数を勝敗として読まない。WIN/LOSS採用は
  別宣言のadoption Part (pinned fail-closed merger `90711961`) でのみ。
- 本amendment observed HEAD-before-push: `03e409d9`
  (inversive lane K1253後のmain)。push直前に最新mainを再fetchし
  note blob lock (`7a733e54…`・405,454B) を再照合する (競合時は本節を
  追記し直す)。


### Part BN status update (2026-11-23, execution host = 本レーン continuing session): scaffold published

宣言 (note amendment commit `bde1c7de`・observed HEAD-before-push
`03e409d9`・note blob lock `7a733e54…` を再照合のうえpush) に続いて、
scaffoldをmainに出版しfetch-back検証まで完了した (verdict不消費・
未実行)。

- scaffold commit A `52ff9a09` (observed HEAD-before-push `bde1c7de`):
  **73ファイル** = scripts 7 (maker `7b2c8e53` + drive `37bb126c` +
  row_audit `f45b124e` + **汎用事前登録win-halt監査 `f55ae559`** +
  pinned jsreplay `84585617` / runbatch `f591f8c2` / runwave
  `8efd78c2`) + input 54 (batch-keys.json `2776acaf…`・s001..s053 CSV)
  + val-gate 12 (published-baseline 8・this-host 4)。
- **fetch-back 73/73 byte一致** (commit `52ff9a09` pinned raw fetch +
  cmp全件)。
- 本host val-gate (this-host.out更新済み・出版済み): 4/4 node-exact
  (at2m 2キー result 0 nodes 2,000,000・first-15m result 2 nodes
  3,651,923・second-15m result 2 nodes 5,040,200・禁止四角 95,670・
  wall_s比較外)。
- maker: 全gate PASS・4回実行byte一致 (batch-keys.json sha256
  `2776acafbb638cb148661b3988b7eb36bc8519e5b7b75b415b01618bfcb85bf7`・
  tamper battery 6/6検出・T1-T6詳細は宣言節どおり)。
- batch-23 drive は未着手 (publish-then-execute・起動だけは成果と
  しない)。次回のランが宣言protocolどおりdriveする (2-pass fresh
  cold budget 15M・mismatch→HARD-STOP・WIN→HALT rc=45・枯渇=UNKNOWN)。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 12643・class 25835
  (53キーすべて)・class 31600 (53キーすべて・s001..s053のまま) は
  本status update時点でもUNKNOWNのまま。nodes数・legal数を勝敗として
  読まない。
- 本status update observed HEAD-before-push: push直前に最新mainを
  再fetchしnote blob lock (`1a9b85ea…`・411,288B) を再照合する。


### Part BN status update 2 (2026-11-23, execution host = 本レーン continuing session): batch-23 drive-1 WIN-HALT at s001・s002、出版完了

宣言 (`bde1c7de`)・scaffold (`52ff9a09`・status update `d95ca723`) の
後、宣言protocolどおりbatch-23のdrive-1を本hostで実行し、事前登録
WIN-HALT規則によりbatchが停止した (verdict不消費)。実験dirの全成果
をmainに出版しfetch-back検証まで完了した。

- drive-1 (2 worker・260s有界・2-pass fresh cold budget 15M・pinned
  replica `jsreplay.js` `84585617…`): **s001 WIN (honest label)**
  (key (1152921505294712832, 32768)・s5 index 62435・legal 78・
  membership 4・replay result 1・nodes 5,415,927・two-pass node-exact・
  wall 51/56s) → worker1 rc=45事前登録WIN-HALT。**s002 WIN (honest
  label)** (key (3458764514374189056, 32768)・legal 88・replay result
  1・nodes 9,329,444・two-pass node-exact・wall 94/52s) → worker2
  rc=45。両workerの最初のキーがともにWINであったため **fragment
  ゼロ** (batch-22のk001のようなmid-flight断片なし)。残り51キー
  (s003..s053) はfileless UNPROBED、15M同条件の再probe禁止は完走行
  のみにbinding。
- 行監査 (汎用事前登録版 `row_audit_batch23_win_halt.py`
  `f55ae559…`・schema `...batch23-rowaudit-winhalt-v1`): PASS・3回実行
  byte一致 (json `14aa7f63…`・probed 2・win_rows [s001, s002]・
  derived_state=true)・tamper battery 3/3検出 (s001 p1 verdict反転→
  p1/p2 mismatch GATE FAIL / 未probe s003への偽PASS行追加→非completed
  キーへのverdict行 GATE FAIL / s002のverdict行除去→completed欠落
  GATE FAIL・scratch copyで実施・実験filesはbyte検証復元)。
- 出版 (全fetch-back byte一致): 実験dir 81ファイルを3コミットでmain
  に反映: A `52ff9a09` scaffold 73ファイル (scripts 7 + input 54 +
  val-gate 12・73/73) → B `597d810` outputs 6ファイル (status.log・
  raw 4 (s001・s002のp1/p2)・row-audit-winhalt.json・6/6) → C
  `4dad105b` README + MANIFEST-sha256 79行 (2/2)。
- 意味 (route bookkeepingのみ・閉鎖主張なし): s001とs002は**22番目
  と23番目の unconsumed closure WIN 候補** (19旧 + a003 + k002 +
  s001 + s002)。採用された場合、**class 31600 (rank 19) の全LOSS
  閉包ルートは2つの独立WIN子で反駁証拠を持つ** (12643・25835と
  同型・同一クラス内2WINは初めてのパターン)。verdictは一切消費して
  いない: 採用判断はscrutiny owner C++第二実装 gate pin `9193f5b6…`
  待ちで本レーンは代行しない。canonical cache (6,235行 `f6649fe3…`)
  read-only・不変。次batch選定は次回のランが21+2-WIN交積の反駁簿記で
  行う (runner-up rank 20 class 10968・backup rank 21 class 16957は
  本batchでは触れていない)。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 12643・class 25835
  (53キーすべて)・class 31600 (53キーすべて・s001/s002を含む) は本
  status update時点でもUNKNOWNのまま。nodes数・legal数を勝敗として
  読まない。
- 本status update observed HEAD-before-push: `4dad105b` (commit C)。
  push直前に最新mainを再fetchしnote blob lock (`900004a0…`・
  413,325B) を再照合する。


## Part BO (solver, amendment 2026-11-23, 実行前に宣言): closure class 16957 exact-S5 probe batch 24 (verdict不消費)

batch-24は、batch-23 status update 2で予定したrunner-up rank 20 class 10968
から選定を開始したが、**fail-closed overlap gateが新事実を捕捉した**
(publish-then-execute規約どおり、まず本amendmentを出版する)。

- 機械発見 (selection実行中の生の失敗として記録・proze不使用):
  batch-23 maker `7b2c8e53`のbatch-24機械翻訳初稿 (KEY_PREFIX="y"・prior
  24 packets)でrank 20 class 10968 (mask
  [1152925919833292800, 0]・route-alive・cost 53子すべてunknown・known
  children {})のkey生成を試みたところ、**overlap gateが発火**:
  `GATE FAILED: key (1152926194711199744,0) already probed by a published
  packet`。当該位置はs5 index 273033で、published batch-12 packet (class
  8106)のkey id **n018**が宣言済み (batch-12はn008でWIN-HALT停止しており
  n018にrawは存在せず fileless UNPROBED、15M probeは一度も走っていない)。
  すなわち**class 10968はpublished-packet disjointness慣例の下では53キー
  fresh batch不能 (blocked・NOT route-dead)**: WIN反駁証拠ゼロ・known WIN子
  なし・unknown 53不変・採用判断・UNKNOWN担保はすべて不変のまま。同じ
  gateで機械掃引した結果、**rank 22 class 23964も2点交差を持つ**ことを
  将来の選定用に記録する: s5 495193 = batch-13 key p007 (p003でWIN-HALT・
  UNPROBED)・s5 550880 = batch-4 key e043 (e002でWIN-HALT・UNPROBED)。
  この2クラスのコリジョン簿記はbatch-24 makerにPKT_COLLISION gateとして
  組み込み、ピン改ざんにfail-closedする (T6電池で検出済み)。
- 選定続行 (すべて機械・published baseから再導出): rank 20 class 10968
  (blocked)とrank 22 class 23964 (blocked)を飛ばし、**rank 21 class
  16957** (mask [1152921504606978048, 264]・cost 53子すべてunknown・known
  children {}・groups served (15,70)(48,53)(48,103)・23-WIN交積空・
  packet交差ゼロ) がpublished-table順で最初の全key gate通過候補。
  runner-upは**rank 23 class 30565** (rank 22 23964がblockedのため飛び
  越し・route-alive・交差ゼロ)・backupは**rank 24 class 1849**
  (route-alive・交差ゼロ)。rank 19以前の反駁簿記 (ranks 1..18＋rank 19
  class 31600 via s001+s002 WIN pair) はPart BN宣言から不変で、batch-24
  makerで再検証済み。
- preflight (fail-closed maker `make_batch24_keys.py` sha256 `130b76dd…`・
  全gate PASS・**4回実行byte一致**): 53キー y001..y053 (s5昇順
  91296..561493・legal 75..95・Board再算出53/53・membership分布
  {2:3, 3:10, 4:40})。y001 = (10376293541461753856, 264)・legal 87・
  y053 = (1152921504606879744, 68719478848)・legal 90。canonical cache
  6,235行 `f6649fe3…` hits 0/53・quarantine 0/53・prior 24 published
  packets (batches 1..23・1,193行・1,179一意) overlap 0・key id prefix
  "y"は24 packetすべてで未使用 (使用済みはabcdefghjkmnpqrtuvwxzs・未使用
  はiloy)。batch-keys.json sha256 `486858d6…`。**tamper battery 7/7検出**
  (T1 graph sha pin 1bit→drift ABORT・T2 CLASS_MASK 1bit→mask gate
  FAIL・T3 batch-23 prior packet pin 1bit→sha drift ABORT・T4 prior rows
  pin 1193→1194→gate FAIL・T5 rank-19 WIN-pair evidence pin 1bit→selection
  gate FAIL・**T6 PKT-collision skip pin 1bit→新collision gate FAIL**・
  T7 graph実ファイル末尾1bit→sha drift ABORT・スクラッチcopyで実施)。
- val-gate (pinned `jsreplay.js` `84585617…`・本host): **4/4 node-exact**
  (at2m 2キー result 0 nodes 2,000,000/2,000,000 budget exhausted・
  first-15m result 2 nodes 3,651,923・second-15m result 2 nodes
  5,040,200・禁止四角 95,670・wall_s比較外)。
- 実行protocol (batch-22/23流・publish-then-execute): scaffold (scripts 7:
  maker `130b76dd` + drive_batch24.sh `031b6f38` + full row audit
  row_audit_batch24.py `722506eb` + **汎用事前登録win-halt監査
  row_audit_batch24_win_halt.py `fdebf219`** (batch-23の汎用版構造を踏襲・
  haltキーid固定なし・derived_state) + pinned jsreplay `84585617` /
  runbatch `f591f8c2` / runwave `8efd78c2`) + input 54 (batch-keys.json
  `2776acaf`…ではなくbatch-24正本 `486858d6…` + y001..y053 CSV) +
  val-gate 12 (published-baseline 8 byte-copy + 本host再生成4) を実験dir
  `research/experiments/n11-centralreply-closure-class16957-batch24-20261123/`
  に出版してからdriveする。停止規則・消費規則はPart BNと同一 (2-pass
  fresh cold budget 15M・mismatch→HARD-STOP rc=42・WIN→HALT rc=45 honest
  label・verdict不消費・枯渇=UNKNOWN・15M同条件再probe禁止は完走行のみ・
  採用は別宣言adoption Part (pinned fail-closed merger `90711961`) 経由
  のみ・本batch単体では閉鎖・被覆・secured主張なし)。起動だけは成果と
  しない。
- 不接触: canonical cache (6,235行 `f6649fe3…`) read-only・23 unconsumed
  closure WIN候補 (19旧 + a003 + k002 + s001 + s002) 不変・batch-21/22/23
  residuals非接触・batch-12/13/4のhalted packets (collision keysの宣言元)
  不変かつ本batchでは一切probeしない・Part BM/BN dirs不変・Part BH
  (`de1383a7`) 不変・fast lane・inversive-arc lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 31600・**class 10968
  (blocked・route-aliveのまま)**・**class 23964 (blocked)**・class 16957
  (53キーすべて・y001..y053) は本Partのどの時点でもUNKNOWNのまま。
  nodes数・legal数・membership数を勝敗として読まない。WIN/LOSS採用は
  別宣言のadoption Part (pinned fail-closed merger `90711961`) でのみ。
- 本amendment observed HEAD-before-push: `df870814` (three-token
  fast-lane宣言・新規noteファイルのみで非接触)。push直前に最新mainを
  再fetchしnote blob lock (`d8cf204b…`・416,711B) を再照合する (競合時は
  本節を追記し直す)。

## Part BO status update (batch-24 実行結果、2026-11-23)

(observed HEAD: 3c05b203・non-contact concurrent commits 7b62b8c2 (K1253)
・3c05b203 (K1251) を確認のうえ線形続行。fetch-back 済み出版状況に基づく追記)

- drive-1 は宣言commit 2c91e033 の事前登録stop ruleどおり **WIN-HALT
  rc=45 (両worker)** で完了 (2026-11-23T06:50:14Z..06:52:09Z・
  fragmentゼロ・truncated再実行ゼロ・budget 15M・2-pass fresh cold)。
- **y001 WIN (honest label)**: key (10376293541461753856, 264)・
  s5 91296・legal 87・membership 2・nodes 5,291,064 (budget 15M内)・
  two-pass node-exact (wall 53/53s)。**24番目の unconsumed closure WIN
  候補**。
- **y006 WIN (honest label)**: key (1152921504607043584, 264)・
  s5 368510・legal 84・membership 2・nodes 5,321,639 (budget 15M内)・
  two-pass node-exact (wall 51/45s)。**25番目の unconsumed closure WIN
  候補**。
- y002 LOSS (adoption candidateのみ): (1153484454560399360, 264)・
  s5 166253・nodes 217,944。y004 LOSS (adoption candidateのみ):
  (1152921779484884992, 264)・s5 272083・nodes 632,091。いずれも
  verdict不消費 (別宣言adoption Part・pinned fail-closed merger
  90711961 経由のみ)。
- 残り49キー (y003, y005, y007..y053) は fileless UNPROBED。
- row-audit-winhalt PASS (schema
  n11-centralreply-closure-class16957-batch24-rowaudit-winhalt-v1・
  json sha256 `9d073038…`): completed 4 (WIN 2・LOSS 2・exhausted 0)・
  3回実行byte一致・tamper battery 3/3検出 (p1 verdict反転 /
  未probeキー y010への偽verdict行 / verdict行 y006除去・scratch上で
  実施し実験filesは無改変)・clean control PASS。
- 出版3コミット (fetch-back byte照合済み): scaffold d7ee67c7 (73
  files・73/73 blob一致)・outputs 18420555 (10 files・10/10一致)・
  README+MANIFEST-sha256.txt 83行 d4c0074e (README blob 96f7b5d1…・
  MANIFEST blob 39660079…・raw sha256 8a8e30a8…)。
- 意味 (route statementのみ): y001/y006 の2独立WIN子により (採用
  された場合) **class 16957 の全LOSS閉包ルートは反駁証拠を持つ**
  (batch-21/22/23 と同型の反駁パターン)。ただし verdictは一切消費
  していない・採用判断は scrutiny owner C++第二実装 gate pin
  `9193f5b6…` 待ち (本レーンは代行しない)。class 10968・23964 は
  blocked (packet交差・NOT route-dead) のまま。canonical cache 6,235行
  f6649fe3… は read-only・不変。
- 次回 (batch-25) の選定は **25-WIN交積** (23旧 + s001/s002 +
  y001 (s5 91296)・y006 (s5 368510) の unconsumed set) の反駁簿記で
  maker内で機械選定する。rank 22 class 23964 は PKT-collision
  blocked継続・rank 23 class 30565 (runner-up)・rank 24 class 1849
  (backup) が当面のroute-alive候補だが、25-WIN交積の出現で反駁状況
  が変わるため EXPECTED_RANKS を拡張して再導出必須。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 16957
  (53キーすべて・y001/y006を含む) はどの時点でもUNKNOWNのまま。**
  nodes数・expansions数を勝敗として読まない。
- note blob lock chain: `d8cf204b…` (Part BN終了時 416,711B) →
  `c108a4df…` (Part BO宣言published 422,870B・fetch-back照合済み) →
  本status update追記後のblobはpush時にfetch-backして次回ラン用に
  記録する。

### Part BP宣言 (batch-25, class 30565 rank 23, 2026-11-23、実行前に出版)

本文は publish-then-execute 宣言。以下の選定・パケットはすべて機械再導出
(prose不使用) であり、実行はこの宣言の後に限る。

- **25-WIN集合確定**: 先の Part BO 結果 (y001 s5 91296・y006 s5 368510)
  を加えた unconsumed closure WIN 候補は25個。y001/y006 は published
  batch-24 packet (sha256 486858d6…) から再導出・canonical cache
  6,235行 (f6649fe3…) 未消費を機械確認。
- **rank 21 class 16957 は反駁に転落** (verdict不消費):
  unknown_now[16957] ∩ 25-WIN = {91296, 368510} (published Part BO
  honest WIN行 y001+y006 による2番目のWIN-PAIR反駁)。
- **rank 20 class 10968 と rank 22 class 23964 は blocked 継続**
  (NOT route-dead・WIN反駁証拠ゼロ): batch-24 packet を prior に加えても
  衝突ピンは不変 (10968 = {273033} = batch-12 n018 単独、23964 =
  {495193, 550880} = batch-13 p007 + batch-4 e043)。
- **新事実・rank 25 class 5690 は route-dead**: update8 receipt WIN子
  {209644} を持つ (rank 16 class 5687 と同一の既知WIN子)。known WIN子
  を持つため backup にはならない。よって batch-25 の backup は **rank 26
  class 13342** (mask [1188950301642588192, 0]・cost 54・unknown 54・
  25-WIN交積空・known_win空・packet交差ゼロ)。runner-up は rank 24
  class 1849 (mask [1152922672972169216, 0]・cost 53 unknown 53・交差ゼロ)。
- **対象選定: rank 23 class 30565** (mask [1152921505143717888, 1081344]・
  groups served (25,80)(36,41)(36,91)・cost 53子すべてunknown・known
  children {}・25-WIN交積空・packet交差ゼロ)。published候補表
  (d57a7609… 807行) との (rank→class) 全行一致を機械再確認。
- 53キー **i001..i053** (prefix "i" は25 published packets ですべて未使用。
  未使用文字は {i, l, o})。s5昇順 68580..903169・legal 76..94・Board再計算
  53/53・membership {4:45, 3:8}。canonical cache hits 0/53・quarantine
  0/53。prior 25 packets (1,246行・1,232一意・cross-packet重複14は
  membership由来) overlap ゼロ。batch-keys.json sha256
  `272c0c134e3be17838311d0d3f18f09340d09094d35e15197481c999892390a5`
  (schema `n11-centralreply-closure-class30565-batch25-input-v1`)。
- preflight maker `make_batch25_keys.py` `6b461049…`: 全gate PASS・
  4回実行byte一致・tamper battery 7/7検出 (T1 graph sha pin 1bit /
  T2 CLASS_MASK 1bit / T3 batch-24 packet sha pin 1bit / T4
  EXPECTED_PRIOR_ROWS 1246→1247 / T5 rank-21 evidence pin
  368510→368511 / T6 PKT-collision pin 273033→273034 / T7 rank-25
  route-dead known-win pin 209644→209645)・clean control PASS。
  新規gate: 25-WIN集合・rank-21反駁tie (== {91296, 368510})・
  rank-25 route-dead gate (ranked[24] == 5690・known_win == {209644})・
  EXPECTED_RANKS 25..28 拡張 (5690/13342/5343/13758)。
- val-gate 12ファイル: published-baseline 4組は batch-23/24 と同一の
  byte-copy、this-host 4つは本ホスト再生成 (node-exact一致・禁止四角
  95,670)。solver `jsreplay.js` `84585617…`・runner `runbatch.sh`
  `f591f8c2…`・`runwave.sh` `8efd78c2…` はいずれも byte-copy pin。
- 事前登録stop rules (batch-23/24 と同一): 2 worker・260s有界・
  2-pass fresh cold・budget 15M・WINは rc=45 で WIN-HALT (verdict不消費)・
  determinism mismatch は rc=42 HARD-STOP・budget不足は honest
  EXHAUSTED (UNKNOWN・同一条件での再probeなし)。監査script
  `row_audit_batch25_win_halt.py` `7b61123e…` (halt キーid固定なし)・
  `row_audit_batch25.py` `a81da5a5…` は scaffold に事前登録済み。
- 不接触確認: 本宣言時点の並走非接触コミットは finite-field-kyouen
  (K1251/K1253) のみ。observed HEAD は push 時に本文末尾の status update
  に記録する (競合時は本節を追記し直し、成立しない場合は簡潔に記録して
  次回へ回す)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 16957・
  class 30565 (53キーすべて) はどの時点でもUNKNOWNのまま。** nodes数・
  legal数を勝敗として読まない。WIN/LOSS採用は別宣言の adoption Part
  (pinned fail-closed merger 90711961) 経由のみ・scrutiny owner C++
  第二実装 gate 9193f5b6 待ちは代行しない。

## Part BP status update (batch-25 実行結果、2026-11-23)

(observed HEAD: 3b1a6283・concurrent non-contact commits fd2c12dd
(K1252) を確認のうえ線形続行。fetch-back済み出版状況に基づく追記)

- drive-1 は宣言commit `b54fbdd6` の事前登録stop ruleどおり
  **WIN-HALT rc=45 (両worker)** で完了 (2026-11-23T06:58:54Z..07:02:34Z・
  fragmentゼロ・truncated再実行ゼロ・budget 15M・2-pass fresh cold)。
- **i001 WIN (honest label)**: key (1152921505277935616, 1081344)・
  s5 68580・legal 88・membership 4・nodes 13,251,132 (budget 15M内)・
  two-pass node-exact (wall 150/68s)。**26番目の unconsumed closure
  WIN 候補**。
- **i002 WIN (honest label)**: key (3458764514357411840, 1081344)・
  s5 191299・legal 82・membership 4・nodes 7,207,180 (budget 15M内)・
  two-pass node-exact (wall 77/75s)。**27番目の unconsumed closure
  WIN 候補**。
- 残り51キー (i003..i053) は fileless UNPROBED。
- row-audit-winhalt PASS (schema
  n11-centralreply-closure-class30565-batch25-rowaudit-winhalt-v1・
  json sha256 `cc84d1b3…`): completed 2 (WIN 2・LOSS 0・exhausted 0)・
  3回実行byte一致・tamper battery 3/3検出 (p1 verdict反転 /
  未probeキー i010への偽verdict行 / verdict行 i002除去・scratch上で
  実施し実験filesは無改変)・clean control PASS。
- 出版3コミット (fetch-back byte照合済み): scaffold 2cc4a69a (73
  files・73/73 blob一致)・outputs 3b1a6283 (6 files・6/6一致)・
  README+MANIFEST-sha256.txt 79行 573099b4 (README blob 5c6fe73d…・
  MANIFEST blob 6b5a933c…・raw sha256 eb649458…)。
- 意味 (route statementのみ): i001/i002 の2独立WIN子により (採用
  された場合) **class 30565 の全LOSS閉包ルートは反駁証拠を持つ**
  (4batch連続の同型反駁パターン)。ただし verdictは一切消費してい
  ない・採用判断は scrutiny owner C++第二実装 gate pin `9193f5b6…`
  待ち (本レーンは代行しない)。class 10968・23964 はblocked
  (packet交差・NOT route-dead)・class 5690 は route-dead
  (receipt WIN子 209644) のまま。canonical cache 6,235行
  f6649fe3… は read-only・不変。
- 次回 (batch-26) の選定は **27-WIN交積** (25 + i001 (s5 68580)・
  i002 (s5 191299) の unconsumed set) の反駁簿記でmaker内で機械
  選定する。当面のroute-alive候補は rank 24 class 1849 (runner-up)・
  rank 26 class 13342 (backup)。rank 25 class 5690 はroute-dead
  (known WIN子 209644) のため選定対象外。PKT-collision blockedの
  10968・23964は継続。27-WIN交積の出現で反駁状況が変わるため
  EXPECTED_RANKS を再拡張して再導出必須。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 16957・
  class 30565 (53キーすべて・i001/i002を含む) はどの時点でもUNKNOWN
  のまま。** nodes数・expansions数を勝敗として読まない。
- note blob lock chain: `d8cf204b…` (Part BN) → `c108a4df…` (Part BO
  宣言) → `85fe6d79…` (Part BO status) → `79935c46…` (Part BP宣言)
  → 本status update追記後のblobはpush時にfetch-backして次回ラン用
  に記録する。
### Part BQ宣言 (batch-26, class 1849 rank 24, 2026-11-23、実行前に出版)

本文は publish-then-execute 宣言。以下の選定・パケットはすべて機械再導出
(prose不使用) であり、実行はこの宣言の後に限る。

- **27-WIN集合確定**: 先の Part BP 結果 (i001 s5 68580・i002 s5 191299)
  を加えた unconsumed closure WIN 候補は27個。i001/i002 は published
  batch-25 packet (sha256 272c0c13…) から再導出・canonical cache
  6,235行 (f6649fe3…) 未消費を機械確認。
- **rank 23 class 30565 は反駁に転落** (verdict不消費):
  unknown_now[30565] ∩ 27-WIN = {68580, 191299} (published Part BP
  honest WIN行 i001+i002 による3番目のWIN-PAIR反駁・同一クラス内
  2独立WIN子)。
- rank 17 class 12643 ({115192})・rank 18 class 25835 ({150241})・
  rank 19 class 31600 ({62435, 192809})・rank 21 class 16957
  ({91296, 368510}) の反駁は27-WIN簿記で不変。
- **rank 20 class 10968 と rank 22 class 23964 は blocked 継続**
  (NOT route-dead・WIN反駁証拠ゼロ): batch-25 packet を prior に加えても
  衝突ピンは不変 (10968 = {273033} = batch-12 n018 単独、23964 =
  {495193, 550880} = batch-13 p007 + batch-4 e043)。
- **rank 25 class 5690 は route-dead 継続**: update8 receipt WIN子
  {209644}。batch-26 候補から除外 (maker内で機械pin)。
- **対象選定: rank 24 class 1849** (mask [1152922672972169216, 0]・
  groups served (36,40)(36,80)・cost 53子すべてunknown・known children
  {}・27-WIN交積空・known WIN子ゼロ・packet交差ゼロ・canonical hits
  0/53・quarantine 0/53・53キーすべて canonical-safe)。published候補表
  (d57a7609… 807行) との (rank→class) 全行一致を機械再確認。
  runner-up: rank 26 class 13342 (mask [1188950301642588192, 0]・unknown
  54・route-alive・交差ゼロ)。backup: rank 27 class 5343 (unknown 54・
  route-alive・交差ゼロ)。
- 53キー **l001..l053** (prefix "l" は26 published packets ですべて未使用。
  未使用文字は {l, o} で今回は "l" を使用)。s5昇順 3170..81036・legal
  75..101・Board再計算 53/53・membership {4:44, 3:8, 2:1}。prior 26
  packets (1,299行・1,285一意・cross-packet重複14はmembership由来)
  overlap ゼロ。batch-keys.json sha256
  `f1ea43aef6ee06c918885a9007ad3f347d96aa198180e87bf3eb14d783304cdd`
  (schema `n11-centralreply-closure-class1849-batch26-input-v1`)。
- preflight maker `make_batch26_keys.py` `a74250d6…`: 全gate PASS・
  4回実行byte一致・tamper battery 8/8検出 (T1 graph sha pin 1bit /
  T2 CLASS_MASK 1bit / T3 batch-25 packet sha pin 1bit / T4
  EXPECTED_PRIOR_ROWS 1299→1300 / T5 rank-23 evidence pin
  191299→191300 / T6 PKT-collision pin 273033→273034 / T7 rank-25
  route-dead known-win pin 209644→209645 / T8 EXPECTED_RANKS rank-29
  pin 14103→14104)・clean control PASS。新規gate: 27-WIN集合・rank-23
  反駁tie (== {68580, 191299})・EXPECTED_RANKS rank-29拡張 (14103)。
- val-gate 12ファイル: published-baseline 4組は batch-23/24/25 と同一の
  byte-copy、this-host 4つは本ホスト再生成 (node-exact一致: at2m 2M
  exhaustion ×2・15m基準キー (2, 3,651,923)/(2, 5,040,200)・禁止四角
  95,670)。solver `jsreplay.js` `84585617…`・runner `runbatch.sh`
  `f591f8c2…`・`runwave.sh` `8efd78c2…` はいずれも byte-copy pin。
- 事前登録stop rules (batch-23/24/25 と同一): 2 worker・260s有界・
  2-pass fresh cold・budget 15M・WINは rc=45 で WIN-HALT (verdict不消費)・
  determinism mismatch は rc=42 HARD-STOP・budget不足は honest
  EXHAUSTED (UNKNOWN・同一条件での再probeなし)。監査script
  `row_audit_batch26_win_halt.py` `3bcf7857…` (halt キーid固定なし)・
  `row_audit_batch26.py` `33ffbce5…` は scaffold に事前登録済み。
- 不接触確認: 本宣言の執筆時点で n11 centralreply closure laneへの
  他セッションコミットは確認していない。observed HEAD は push 時に
  status update 側に記録する (競合時は本節を追記し直し、成立しない
  場合は簡潔に記録して次回へ回す)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 30565・
  class 1849 (53キーすべて) はどの時点でもUNKNOWNのまま。** nodes数・
  legal数を勝敗として読まない。WIN/LOSS採用は別宣言の adoption Part
  (pinned fail-closed merger 90711961) 経由のみ・scrutiny owner C++
  第二実装 gate 9193f5b6 待ちは代行しない。

## Part BQ status update (batch-26 実行結果、2026-11-23)

(observed HEAD: 9eda46af・concurrent non-contact commits 415e51f
(K1251)・ea1d674 (artifact-insertion log) を確認のうえ線形続行。
fetch-back済み出版状況に基づく追記。本節追記前の note blob lockは
`5135834e` 宣言版 438,761 bytes)

- drive-1 は宣言commit `8e64ba1c` の事前登録stop ruleどおり
  **WIN-HALT rc=45** で完了 (2026-11-23T07:55:53Z..08:22:06Z・
  bounded invocation 7回・budget 15M・2-pass fresh cold・
  determinism mismatch rc=42 は不発)。
- **l028 WIN (honest label)**: key (1153485622925590528, 0)・
  s5 81011・legal 88・membership 3・nodes 4,893,014 (budget 15M内)・
  two-pass node-exact (wall 52/52s)。**28番目の unconsumed closure
  WIN 候補**。worker2はWIN-HALT検知後に走行中だった l033
  (LOSS・nodes 8,571,040・2-pass一致) を最後まで完了させている。
- LOSS行 30 (l001..l027, l029, l031, l033) = 採用候補のみ・
  verdictは一切消費していない。UNPROBED 22キー: fragment l035
  (truncated p1・NOT evidence) + fileless 21キー (l030, l032,
  l034, l036..l053)。EXHAUSTED 0。
- 選定は **28-WIN交積** (27 + l028 (s5 81011)) の反駁簿記で
  maker内機械選定どおり: rank 23 class 30565 は batch-25
  WIN-PAIR (i001 s5 68580・i002 s5 191299) で反駁、rank 24
  **class 1849** (mask [1152922672972169216, 0]・groups (36,40)
  (36,80)・cost 53 unknown・27-WIN交積∅・packet交差 0) を選定。
  rank 25 class 5690 は route-dead (receipt WIN子 209644)・
  10968/23964 は PKT-collision blocked のまま。
- row-audit-winhalt PASS (schema
  n11-centralreply-closure-class1849-batch26-rowaudit-winhalt-v1・
  json sha256 `8c91b1342d82f99b…`): completed 31 (WIN 1・LOSS
  30・exhausted 0)・3回実行byte一致・tamper battery 3/3検出
  (p1 l028 verdict反転 / l028 verdict行除去 / 未probeキー l040
  への偽verdict行・scratch上で実施し実験filesは無改変)・clean
  control PASS。判定対象は raw outputs 75ファイル・status.log
  含む。
- 出版4コミット (fetch-back byte照合済み): 宣言 `8e64ba1c`
  (note amendment・note blob a014be5b→5135834e・438,761 bytes)・
  scaffold `309386d5` (73 files: scripts 7・input 54・val-gate
  12・73/73 blob一致)・outputs `32fbe3bb` (75 files:
  status.log + raw 73 + row-audit json・75/75一致)・README
  + MANIFEST-sha256.txt 148行 `9eda46af` (README raw sha256
  `602fb209…`)。
- 意味 (route statementのみ): 単独WIN子 l028 により (採用され
  た場合) **class 1849 の全LOSS閉包ルートは反駁証拠を持つ**
  (batch-21 a003単独・batch-22 k002単独・batch-23/24/25 pairに
  続く同型反駁・3回目の単独WIN子パターン)。ただし verdictは
  一切消費していない・採用判断は scrutiny owner C++第二実装
  gate pin `9193f5b6…` 待ち (本レーンは代行しない)。canonical
  cache 6,235行 f6649fe3… は read-only・不変。
- 次回 (batch-27) の選定は **28-WIN交積** (27 + i001・i002・
  l028 (s5 81011) の unconsumed set) の反駁簿記でmaker内で
  機械選定する。当面のroute-alive候補は rank 26 class 13342
  (runner-up)・rank 27 class 5343 (backup)・rank 28 class
  13758・rank 29 class 14103。rank 30..32 は要packet交差確認。
  class 10968・23964 は PKT-collision blocked・継続。prefix
  未使用文字は {o} のみ (次回選定時は "o" を使用)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 30565・
  class 1849 (53キーすべて・l028を含む) はどの時点でもUNKNOWNの
  まま。** nodes数・legal数を勝敗として読まない。WIN/LOSS採用は
  別宣言の adoption Part (pinned fail-closed merger 90711961)
  経由のみ・scrutiny owner C++ 第二実装 gate 9193f5b6 待ちは
  代行しない。

### Part BR宣言 (batch-27, class 13342 rank 26, 2026-11-23、実行前に出版)

本文は publish-then-execute 宣言。以下の選定・パケットはすべて機械再導出
(prose不使用) であり、実行はこの宣言の後に限る。

- **28-WIN集合確定**: 先の Part BQ 結果 (l028 s5 81011) を加えた
  unconsumed closure WIN 候補は28個。l028 は published batch-26 packet
  (sha256 f1ea43ae…) から再導出・canonical cache 6,235行 (f6649fe3…)
  未消費を機械確認。
- **rank 24 class 1849 は反駁に転落** (verdict不消費):
  unknown_now[1849] ∩ 28-WIN = {81011} (published Part BQ honest WIN行
  l028 単独による反駁・batch-21 a003・batch-22 k002 に続く3回目の
  単独WIN子パターン)。
- rank 17 class 12643 ({115192})・rank 18 class 25835 ({150241})・
  rank 19 class 31600 ({62435, 192809})・rank 21 class 16957
  ({91296, 368510})・rank 23 class 30565 ({68580, 191299}) の反駁は
  28-WIN簿記で不変。
- **rank 20 class 10968 と rank 22 class 23964 は blocked 継続**
  (NOT route-dead・WIN反駁証拠ゼロ): batch-26 packet を prior に加えても
  衝突ピンは不変 (10968 = {273033} = batch-12 n018 単独、23964 =
  {495193, 550880} = batch-13 p007 + batch-4 e043)。
- **rank 25 class 5690 は route-dead 継続**: update8 receipt WIN子
  {209644}。batch-27 候補から除外 (maker内で機械pin)。
- **対象選定: rank 26 class 13342** (mask [1188950301642588192, 0]・
  groups served (5,24)(5,30)(5,55)(5,65)(24,5)(24,55)・cost 54子すべて
  unknown・known children {}・28-WIN交積空・known WIN子ゼロ・packet交差
  ゼロ・canonical hits 0/54・quarantine 0/54・54キーすべて canonical-safe)。
  published候補表 (d57a7609… 807行) との (rank→class) 全行一致を機械再確認
  (rank 30まで: (30, 30484, 54) を拡張pin)。runner-up: rank 27 class 5343
  (unknown 54・route-alive・交差ゼロ)。backup: rank 28 class 13758
  (unknown 54・route-alive・交差ゼロ)。
- 54キー **o001..o054** (prefix "o" は27 published packets ですべて未使用。
  未使用文字は {o} のみで今回は "o" を使用)。s5昇順 98526..460214・legal
  74..100・Board再計算 54/54・membership {4:45, 3:8, 2:1}。prior 27
  packets (1,352行・1,338一意・cross-packet重複14はmembership由来)
  overlap ゼロ。batch-keys.json sha256
  `67814ed6287d68d6e97212c931dce2b7ee585219e20b4d43edb621632220a014`
  (schema `n11-centralreply-closure-class13342-batch27-input-v1`)。
- preflight maker `make_batch27_keys.py` `9ab4523a…`: 全gate PASS・
  4回実行byte一致・tamper battery 8/8検出 (T1 graph sha pin 1bit /
  T2 CLASS_MASK 1bit / T3 batch-26 packet sha pin 1bit / T4
  EXPECTED_PRIOR_ROWS 1352→1353 / T5 rank-24 evidence pin
  81011→81012 / T6 PKT-collision pin 273033→273034 / T7 rank-25
  route-dead known-win pin 209644→209645 / T8 EXPECTED_RANKS rank-30
  pin 30484→30485)・clean control PASS。新規gate: 28-WIN集合・rank-24
  反駁tie (== {81011})・prior 27 packets 拡張・EXPECTED_RANKS rank-30
  拡張 (30484)。batch-20 x-key pin をこのbatchのUNPROBED (54) から独立
  した固定53に分離 (batch-26 makerで暗黙に一致していた箇所の明示化)。
- val-gate 12ファイル: published-baseline 4組は batch-23/24/25 と同一の
  byte-copy、this-host 4つは本ホスト再生成 (node-exact一致: at2m 2M
  exhaustion ×2・15m基準キー (2, 3,651,923)/(2, 5,040,200)・禁止四角
  95,670)。solver `jsreplay.js` `84585617…`・runner `runbatch.sh`
  `f591f8c2…`・`runwave.sh` `8efd78c2…` はいずれも byte-copy pin。
- 事前登録stop rules (batch-23/24/25/26 と同一): 2 worker・260s有界・
  2-pass fresh cold・budget 15M・WINは rc=45 で WIN-HALT (verdict不消費)・
  determinism mismatch は rc=42 HARD-STOP・budget不足は honest
  EXHAUSTED (UNKNOWN・同一条件での再probeなし)。監査script
  `row_audit_batch27_win_halt.py` `7d920f2b…` (halt キーid固定なし)・
  `row_audit_batch27.py` `ed21debe…` は scaffold に事前登録済み。
  driver `drive_batch27.sh` `9114e211…`。
- 不接触確認: 本宣言の執筆時点で n11 centralreply closure laneへの
  他セッションコミットは確認していない (observed HEAD: Part BQ status
  update a2e1d76b 時点のものが本lane最後)。observed HEAD は push 時に
  status update 側に記録する (競合時は本節を追記し直し、成立しない
  場合は簡潔に記録して次回へ回す)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 30565・
  class 1849・class 13342 (54キーすべて) はどの時点でもUNKNOWNのまま。**
  nodes数・legal数を勝敗として読まない。WIN/LOSS採用は別宣言の adoption
  Part (pinned fail-closed merger 90711961) 経由のみ・scrutiny owner C++
  第二実装 gate 9193f5b6 待ちは代行しない。

## Part BS (verifier, amendment 2026-11-23, 実行前に宣言): batch-26 l028 WIN行の第三実装交叉検証 + 本host pinned-replica再現 (verdict不消費)

batch-26 (Part BQ) で出版されたWIN行 l028 (canonical outputs commit
`32fbe3bb`・scaffold `309386d5`・README+MANIFEST `9eda46af`・2-pass
fresh-cold node-exact・replay result 1・nodes 4,893,014・budget 15M内) に
対し、前例 (Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AZ/BF/BK/BM) と同じpinned
第三実装 (non-df-pn AND/OR minimax) によるverdict-level交叉検証を、
本セッションが単一オーナーとして実行する (同一スコープの対抗宣言・
amendmentが本amendmentより先にmainにある場合は本宣言を破棄して着手し
ない・本宣言時点でnote grep clean・`n11-centralreply-closure-b26win-
thirdimpl-20261123` dirの不存在を確認済み)。なお本レーンはbatch-26
drive-1を第二ホストとして同時実行しており、両ホストのl028 raw p1/p2・
全生値は機械照合で完全一致済み (第二ホスト再現記録 `e38a49f03` 出版
済み・verdict不消費)。本Partはその第三実装による追加裏付けである。

- 対象: `research/experiments/n11-centralreply-closure-b26win-thirdimpl-20261123/`。
  target 1行: **l028** (s5 81011・key (1153485622925590528, 0)・legal 88・
  replica_result 1・replica_nodes 4,893,014・holder class 1849 (unknown)・
  membership_class_count 3・published batch-26 batch-keys `f1ea43ae…`)。
- 機材 (全てpublished byte・実行時にsha照合): third_impl.js `08ea958f…`・
  verify_tbl.js `c8c52528…`・jsreplay.js replica `84585617…`・runner
  `run_thirdimpl.sh` (BF正本byte-copy `a0b77d83…`)・maker
  `make_inputs_bs.py` `313a8d71…` (BM maker `d560b8cd…`をbatch-26正本
  sourcesへhonest adapt)・audit gate battery `audit.py` `afc4da1d…`
  (BM audit `79f4b7e5…`の b26win版 adapt: EXP/SCHEMA/rows-schema・
  header文言のみ変更・gateロジック不変)。
- 前提ゲート (fail-closed・全て機械検査・宣言時点で実施済み): maker全
  gate PASS・4回実行byte一致 (`__pycache__`衛生)・tamper battery 5/5
  検出 (T1 raw pin 1bit・T2 row-audit pin 1bit・T3 README pin 1bit・
  T4 row-audit内容改変 (pass_rows 30→31)・T5 raw内容改変 (nodes
  4893014→4893015)・scratch上で実施し実験sources無改変)・clean control
  PASS。sources sha pin: batch-keys-b26 `f1ea43ae…`・status-b26.log
  `4e167469…` (42行 = PASS 31 + WIN-HALT 1 + P1/P2-TRUNCATED-RETRY 10・
  PASS key集合 == row-audit loss_rows∪win_rows (30+1) 機械交叉導出)・
  README-b26 `602fb209…` (l028 WIN honest label・nodes 4,893,014・
  28番目の unconsumed closure WIN 候補・batch-27 pointer rank 26
  class 13342)・row-audit-winhalt `8c91b134…` (probed 31・pass_rows 30・
  win_rows [l028]・fragment l035 evidence=false probed=false・
  unprobed_count 22・derived_state true・input_sha256 == batch-keys pin)・
  raw l028 p1/p2 `1e499c11…` (両方同一・2-pass node-exact + result 1
  in-budget + status/row-audit/README 3-way照合)・published input CSV
  byte-equality `52d79efc…`・BF anchor/negative CSV byte-equality
  (provenance chain AR→BF→BK→BM→BS)。
- 実行protocol (宣言時点で事前登録・順序も含め固定・逐次実行):
  1. rules gate: pinned `verify_tbl.js`でreplica quads 95,670 ==
     third-impl quads 95,670・triples checked mismatch 0。
  2. 本host pinned-replica再現: pinned replica (jsreplay `84585617…`) で
     l028をbudget 15M・fresh-cold・逐次2回 (p1/p2) 実行し、決定性
     fields p1==p2・published raw fields (result 1・nodes 4,893,014) との
     一致をauditで機械検査する。exhaustion/mismatch/truncationはhonest
     記録のみとし検証主張としない。
  3. negatives ng1/ng2のGATE_FAIL確認 (fail-closed設計どおり) → anchors
     k02a (WIN 9,106,337 exp / 4,991,527 ttHits)・l1a (LOSS 7,660,602 /
     3,951,175) の本host node-exact再現 (a/b 2回)。
  4. target l028は1行=1solver=1プロセス・cap 300,000,000・wallcap 240s・
     `--memo-power=22`・a/b 2回のdeterminism gate
     (result/expansions/ttHits/reason同一必須)・逐次実行。wall超過は
     honest wall-inconclusiveとし検証主張としない。事前の機械予想は
     宣言時に残さない (実測を待つ)。
- 監査: `audit.py` (G0 input/rows照合・G1 script pin 3種・G2 rules gate・
  G2b replica-thishost・G3 anchors・G4 negatives・G5 targets/verdict
  agreement) 3回実行byte一致・audit tamper battery 3種 (T1 maker pin
  反転→ABORT・T2 auditのtarget det-pair改ざん→DIVERGENCE検出・T3 G0の
  input改ざん→gate fail・scratch上で実施し実験files無改変)・clean
  control PASS。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・**verdict不消費**
  (l028の採用判断は引き続きscrutiny owner C++第二実装 gate pin
  `9193f5b6…` のまま)。第三実装verdictがcleanにreplica verdictと一致
  した場合は「一致した」事実のみ記録し、clean不一致はdivergence
  evidenceとして記録するが本レーンではverdictを書き換えない。閉鎖・
  被覆・secured・root勝敗の主張をしない。
- 不接触: canonical cache (6,235行 `f6649fe3…`) への書き込みなし・
  28 unconsumed closure WIN候補 (27 + l028 (s5 81011)) の採用状態不変・
  batch-26残留 (fragment l035再probe + fileless 21キー) に一切触れない・
  **batch-27 (Part BR) の54キー・scaffold・drive・outputsには一切触れな
  い (BRは並走所有)**・fast lane (y18/y19/y20/y21)・K1058/K125x系・
  inversive-arc lane・finite-field lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 1849 (53キーすべて・
  l028を含む) は本Partのどの時点でもUNKNOWNのまま。nodes数・expansions
  数・ttHits数を勝敗として読まない。WIN/LOSS採用は別宣言のadoption
  Part (pinned fail-closed merger `90711961`) でのみ。
- 本amendment observed HEAD-before-push: `efe21bd35` (2026-11-23T08:40:26Z
  時点・note blob lock `01bd66f8` 447,798 bytes と照合済み)。push直前に
  最新mainのnote blob lockを再照合する (batch-27 status update等の並走
  追記が挟まった場合は本節を追記し直し、成立しない場合は簡潔に記録して
  次回へ回す)。

### Part BS status update (2026-11-23, execution host = 本レーン continuing session)

宣言 (note amendment commit `c4dd29a6`・observed HEAD-before-push
`efe21bd35`) どおり、宣言後に本hostがpublished batch-26 WIN行 l028を
第三実装交叉検証し、出版まで完了した (verdict不消費)。実験dir
`research/experiments/n11-centralreply-closure-b26win-thirdimpl-20261123/`。
※運用記録: 宣言push時にプレースホルダ未置換の誤コミット `f4ada6a6`
("..."3文字追記) が一度成立したが、同一セッション内のfail-closed
検証で即時に検知し `c4dd29a6` が修正した (baseはblob `01bd66f8` 相当
329,972 charsと機械検証・誤コミットは履歴に残る・fetch-back blob
`0910a569` 454,355 bytes)。

- 実行 (宣言protocol順・逐次): rules gate `verify_tbl.js` 95,670==
  95,670・triples checked 195,044 mismatch 0 → 本host pinned-replica
  再現: p1/p2ともに **result 1・nodes 4,893,014・two-pass node-exact
  かつpublished raw fieldsと完全一致** (wall 24s/25s・exhaustion/
  mismatch/truncationゼロ) → negatives ng1/ng2 GATE_FAIL文言どおり →
  anchors **k02a WIN 9,106,337/4,991,527 (25.99s/26.15s)**・**l1a
  LOSS 7,660,602/3,951,175 (22.42s/22.75s)** がpublished第三実装値に
  node-exact再現 (a/b同一) → target **l028 third-impl clean WIN
  (result 1) 5,646,148 expansions / 3,187,475 ttHits** (replica
  4,893,014 nodes・ratio 1.15・a/b determinism PASS・16.65s/16.60s)・
  **replica verdict一致 1/1**・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
- maker `make_inputs_bs.py` (`313a8d71…`): 全gate PASS・4回実行byte
  一致・tamper 5/5検出 (T1 raw pin 1bit・T2 row-audit pin 1bit・
  T3 README pin 1bit・T4 row-audit内容改変 (pass_rows 30→31)・T5 raw
  内容改変 (nodes 4893014→4893015)・scratch上・sources無改変)・clean
  control PASS。
- audit `audit.py` (`afc4da1d…`): **50/50 gates PASS**・3回実行byte
  一致 (schema `n11-centralreply-closure-b26win-thirdimpl-audit-v1`・
  gate内訳: input 5 + pins 3 + rows/count 2 + rules 2 +
  replica-thishost 7 + anchors 18 + negatives 2 + targets 10)・
  audit tamper battery 3/3検出 (T1 maker README pin反転→ABORT /
  T2 target det-pair改ざん (l028.b result 1→2)→`target-l028-det-pair`
  DIVERGENCE検出 / T3 G0 input改ざん (legal 88→89)→`input-l028-
  matches-rows` gate fail・scratch上で実施し実験filesはbattery前後
  byte同一を検証)・clean control PASS。
- 出版 (fetch-back byte照合済み): 実験dir 41ファイルを宣言込みでmain
  に反映: 宣言 `c4dd29a6` (note amendment) → A `01851bc9` scaffold
  23ファイル (fetch-back 23/23) → B `77d3cadf` outputs 16ファイル
  (fetch-back 16/16) → C `b5008fb7` README (sha256 `6baa01f6…`) +
  MANIFEST-sha256 39行 (`e1138ae7…`・39ファイルすべてbyte一致・
  追記後の実験README文言どおり)。
- 意味 (route statement・閉鎖主張なし): **l028 WIN (honest label)
  は合計4系統で裏付けられた**: (a) batch-26 drive-1 第一ホストの
  pinned df-pn replica 2-pass node-exact・(b) drive-1 第二 ホスト再現
  (本レーン `e38a49f03`・byte同一)・(c) 宣言protocol step 2の本host
  fresh-cold replica再現・(d) 独立第三実装a/b determinism pair
  (**28番目のunconsumed closure WIN候補・verdict不消費**)。採用判断は
  scrutiny owner C++第二実装 gate pin `9193f5b6…` のまま。canonical
  cache (6,235行 `f6649fe3…`) 不変。batch-26残留 (fragment l035 +
  fileless 21キー)・batch-27 (Part BR) には本Partでは一切触れて
  いない (BRは並走所有)。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 1849 (53キー
  すべて・l028を含む)・class 13342 は本status update時点でも
  UNKNOWNのまま。nodes数・expansions数・ttHits数を勝敗として読ま
  ない。WIN/LOSS採用は別宣言のadoption Part (pinned fail-closed
  merger `90711961`) 経由のみ。
- 本status update observed HEAD-before-push: `b5008fb7` (commit C)。
  push直前に最新mainを再fetchしnote blob lockを再照合する (batch-27
  status update等の並走追記が挟まった場合は本節を追記し直し、成立し
  ない場合は簡潔に記録して次回へ回す)。
## Part BT (solver, amendment 2026-11-23): batch-26 residual l030..l053 continuation (class 1849 enumeration - WIN-CONTINUE事前登録)・verdict不消費・実行前に出版

Part BQ (batch-26 class 1849) は事前登録のWIN-HALT規則によりl028で停止し、
残22キー (fragment l035 truncated p1・NOT evidence + fileless 21キー
l030/l032/l034/l036..l053・fresh・一度もverdictを出していない) が残った。
published batch-26 READMEの予約文言 (「将来の continuation で fresh-cold
再実行」「row-auditはbatch完走時点 (残22キーの継続Part) に全行機械検証
する」) に従い、残22キーの単一オーナー実行を宣言する (本amendmentより
先にmainに存在するbatch-26 residual continuationスコープの対抗宣言・
amendmentがある場合は本宣言を破棄して着手しない。branch / PRは作らない)。

- WIN-CONTINUE事前登録 (Part AW batch-14 residual / Part BH batch-19
  residualの先例と同一の根拠): class 1849の全子LOSS閉包ルートはpublished
  l028 WIN honest label (Part BQ drive-1・Part BS第三実装交叉検証込み
  計4系統) により既に反駁済み。残余キーのprobeはunknown数最小化のための
  列挙であり、ここでのさらなるWIN-HALTに情報価値はない。よってresidual
  installmentでは、published runbatch.shのrc=45 (WIN) が発火したキーは
  honest WIN labelのみで記録し、drive driverを再起動して22キー完遂
  (または本セッション限界) まで列挙を続ける。決定論mismatch -> 即時
  HARD-STOP rc=42 (以後のdrive起動も行わず停止)。budget枯損 (result 0)
  -> honest EXHAUSTED (UNKNOWN・同一条件での再probeなし)。
- 残留キー集合の機械導出 (prose不使用): published batch-keys.json
  (sha256 `f1ea43ae…`・53キー l001..l053) とpublished output/status.log
  から PASS/WIN-HALT/EXHAUSTED 済み31キー {l001..l029, l031, l033} を
  除いた補集合 == {l030, l032, l034, l035, l036..l053} の22キー
  (fragment {l035} + fileless 21キー) であることを本hostで機械検証済み
  (published README記載のUNPROBED 22キー文言と一致)。published l035断片
  (output/raw/l035.p1.out・211 bytes・`# replay_done`なし) はrunbatchの
  completeness guardがfresh-cold再実行する。
- 新規scaffoldなし。published batch-26 dir
  `research/experiments/n11-centralreply-closure-class1849-batch26-20261123/`
  を正本としてそのまま使用する。本hostでpublished MANIFEST-sha256.txt
  掲載148ファイルのうち144ファイル (val-gate this-host 4ファイルを除く:
  scripts 7・input 54・val-gate 8・output/status.log・row-audit-winhalt
  .json・raw 73) をsha256再検証し**144/144 byte一致**を宣言前に機械確認
  済み。published README (sha256 `602fb209…`) もbyte一致再検証済み。
- val-gate (実行前・本host): batch-23/24/25/26と同一の4アンカー。
  at2m 2行 -> result 0 / nodes 2,000,000 node-exact、15m 2行 -> result 2 /
  nodes (2,3,651,923)/(2,5,040,200) node-exact、禁止四角 95,670 x4、
  `# replay_done` x4 (truncationなし)。published val-gate/*.this-host.out
  基準線とpublished-baseline 4組に対するnode数完全一致を実行の前提条件
  とする。本host再生成値は val-gate/*.bt-host.out としてoutputs出版に
  含める (published this-host 4ファイルは不変・byte-pin維持)。
- protocol: 2-pass fresh-cold node-exact、budget 15,000,000、
  1 solver / 1 row / 1プロセス、publish=ALL。実行はpublished drive driver
  (1回起動あたりtimeout 260秒有界・残キー奇偶分割 worker最大2 = 控えめ
  並列) を反復起動する。完了済み31キー (published raws) は再実行しない。
  中断断片はpublished completeness guard (`# replay_done` 検査) が
  fresh-cold再実行する。
- row-audit: 列挙完遂後、published `row_audit_batch26.py`
  (sha256 `33ffbce5…`・full-row監査としてscaffold事前登録済み) により
  53キー全行の機械検証を行う (batch-26 README予約文言の履行)。
  途中でセッションが終了する場合は完了行のみを誠実出版 (verdictを出力していない
  truncated断片は出版対象から除外し再実行に備え、残りはfreshのまま
  次の継続Partに引き継ぐ)。
- verdict不消費: canonical exact-S5 verdict cache (6,235行 `f6649fe3…`)
  への書込みは一切しない。LOSS行は採用候補のみ (消費は別宣言adoption
  Partがpinned fail-closed merger `90711961…`で実行)。新規WIN行は
  unconsumed closure WIN候補の追加のみで採用しない (28候補 (l028込み)
  は読み書きとも非接触・本PartのWIN行があれば29番目以降の候補として
  誠実記録)。採用判断はscrutiny owner C++第二実装 gate pin
  `9193f5b6…`のまま (本レーンは代行しない)。
- 不接触: **batch-27 (Part BR) の54キー・scaffold・drive・outputsには
  一切触れない (BRは並走所有)**。batch 1..25・各residual packet・
  fast lane (y18..y21)・inversive-arc lane・finite-field lane非接触。
  canonical cache read-only・scratch以外の既存filesは無改変。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 1849 (53キーすべて・
  l028・30 LOSS行を含む) は本Partのどの時点でもUNKNOWNのまま。nodes数を
  勝敗として読まない。被覆・secured・root勝敗の主張をしない。
- 本amendment observed HEAD-before-push: push直前に最新mainを再取得し
  noteのblob sha1ロック `7f19145a…` (458,762 bytes) を再照合する
  (競合時は再fetchして本節を追記し直し、成立しない場合は簡潔に記録して
  次回へ回す)。

### Part BT status update (2026-11-23, execution host = 本レーン continuing session)

宣言 (note amendment commit `135cc386`) どおり、push後に最新mainで
batch-26 residual continuationスコープの対抗宣言・amendmentがないことを
確認したうえ、宣言protocolを履行し出版まで完了した (verdict不消費)。

- 実行 (宣言protocol順・逐次): val-gate 4/4 node-exact (at2m 2行 result 0
  / nodes 2,000,000・15m 2行 result 2 / nodes (2,3,651,923)/(2,5,040,200)・
  禁止四角 95,670 x4・`# replay_done` x4・本host値は val-gate/*.bt-host.out
  4ファイル) → drive 4回の bounded invocation (同一published drive driver
  `1037cc5f`・2 worker・260s有界) で残留22キー完走: **22行すべて LOSS
  (採用候補のみ)** (合計 nodes 88,000,683・最小 l038 1,577,298・最大 l048
  9,304,668)・2-pass node-exact (mismatch 0)・EXHAUSTED 0・WIN 0
  (WIN-CONTINUE規則は不発動)。truncated-retry 7件を誠実記録 (l035 p1 /
  l036 p2 / l041 p1 / l045 p1 / l046 p2 / l049 p1 / l050 p1・断片7ファイル
  は output/raw/*.truncated.*.out として保存・published completeness
  guard (`# replay_done` 検査) がfresh-cold再実行・完了行の再実行ゼロ・
  status.log はpublished 42行 prefixとbyte一致 + 追記29行)。
- full-row row-audit (batch-26 README予約文言の履行): published
  pre-registered `row_audit_batch26.py` (sha256 `33ffbce5…`) はWIN行の
  status.log照合で**fail-closedした** (runbatch `f591f8c2…` がWINキーを
  「PASS (nodes付き) + WIN-HALT」の2行で書くのに対し監査側が単行
  (nodes付きWIN-HALT行) を想定・完全完走バッチでWIN行を含む監査の実行は
  今回が初で、これが潜在gateバグの初発火) → 最小派生版
  `row_audit_batch26_full.py` (sha256 `434025ba…`・pre-registered版との
  差分はWIN行の2行pair照合のみ・schema
  `n11-centralreply-closure-class1849-batch26-rowaudit-full-v2`) を本Partの
  outputsとして出版し **PASS: 53 rows / LOSS 52 / WIN 1 (l028) / exhausted
  0 / mismatches 0** (row-audit.json sha256 `cb4158d9…`・3回実行byte
  一致)・tamper battery 4/4検出 (T1 l044.p1 verdict反転→p1/p2 mismatch・
  T2 l028 WIN-HALT行除去→2行pair gate・T3 l035.p1 verdict反転→mismatch・
  T4 l049.p2 replay_done行除去→truncated gate。初回T1探針はsed pattern
  不一致のno-opで検出に至らず、anchor実効性assert付きで電池を設計し直し
  再実施・scratch上で実施し実験filesはbattery前後でbyte同一)・clean
  control PASS。
- 出版 (全fetch-back byte照合): outputs `a79c2a6f` (58 files: raw 51 =
  完了44 + 断片7・status.log・row-audit.json・bt-host 4・派生監査script・
  fetch-back 58/58 byte一致) → `d69c3a38` README + MANIFEST-sha256 204行
  (fetch-back 2/2・MANIFESTはpublished 148行を保持しstatus.log行のみsha
  更新・l035.p1.out行はfresh再実行版に更新・新規57行追記)。
- 意味 (route statementのみ・閉鎖主張なし): **class 1849の53子すべてに
  honest label (WIN 1 (l028・Part BSで4系統裏付け済み) + LOSS 52) が揃い、
  列挙ブックとして完結** (ただしverdictは一切不消費・閉包判定・free
  classificationの更新はadoption Partとrefresh再監査の仕事で本Partは
  代行しない)。52 LOSS行は採用候補のみ・採用は別宣言adoption Part
  (pinned fail-closed merger `90711961…`) 経由のみ。l028を含む28
  unconsumed closure WIN候補はscrutiny owner C++第二実装 gate pin
  `9193f5b6…` 待ちのまま。canonical cache 6,235行 `f6649fe3…` は
  read-only不変・batch-26 rowsはいかなるcacheにも未書込。
- 不接触確認: **batch-27 (Part BR・scaffold 93ef3f89・54キー) には本Partは
  一切触れていない** (BRは並走所有・本status update push直前の時点で
  batch-27のdrive outputsはまだmainに無いことを確認)。fast lane (y21宣言
  `a0519efe`)・finite-field/general-x-merge lane (K1252/K1254) 非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 1849 (53キーすべて・
  l028・52 LOSS行を含む)・class 13342 は本status update時点でもUNKNOWN
  のまま。nodes数・legal数を勝敗として読まない。被覆・secured・root勝敗
  の主張をしない。WIN/LOSS採用は別宣言のadoption Part (merger
  `90711961`) 経由のみ。
- 本status update observed HEAD-before-push: `d69c3a38` (Part BT
  commit B)。push直前に最新mainを再fetchし note blob lock `7bc5d800…`
  (464,656 bytes) を再照合する (batch-27 status update等の並走追記が
  挟まった場合は本節を追記し直し、成立しない場合は簡潔に記録して次回へ
  回す)。

## Part BU (solver, amendment 2026-11-23): batch-26 (class 1849) 52-LOSS canonical adoption + reaudit（実行前に出版・verdict採用は52 LOSS行のみ・l028 WINは不採用）

長期レーン (n11 central-reply closure) のPart BUとして、published batch-26
(Part BQ drive-1 + Part BT residual, class 1849) の52 LOSS行をcanonical
exact-S5 verdict cacheへ計上する単一オーナー実行を宣言する (batch-26
52-LOSS adoptionというスコープに対して本amendmentより先にmainに存在する対抗
宣言/amendmentがある場合は本宣言を破棄して着手しない。branch / PRは作らない)。

- 引き継ぎ (published byteに基づく): Part BQ (宣言 8e64ba1) はclass 1849
  (rank 24) の53 unknown費用子を2-pass fresh-cold node-exactで33キーまで
  探索し l028 WIN-HALT (rc=45・事前登録) で停止した (l028: 2-pass
  node-exact result 1, 4,893,014 nodes・Part BS第三実装交叉検証込み
  計4系統裏付け)。Part BT (宣言 135cc38・WIN-CONTINUE事前登録) が残り22
  キーを完走し (22行すべてLOSS・nodes計88,000,683)、**53/53 honest label
  (WIN 1 (l028) + LOSS 52)** が揃った (row-audit full-v2 `cb4158d9…`:
  53 rows / LOSS 52 / WIN 1 / mismatches 0・status.log `afc92e03…` 71行
  最終行 l053 PASS)。同READMEの消費規則は「52 LOSS行の採用は別宣言adoption
  Partがpinned fail-closed mergerで実行」であり、本Partがその役割を履行する。
- 対象: `research/experiments/n11-centralreply-class1849-loss52-adoption-reaudit-20261123/`。
  BASE canonical exact-S5 verdict cache 6,235行 sha256 `f6649fe3…` (Part BI
  採用正本) + increment 52行 → 採用後canonical 6,287行 (予想: WIN 158 /
  LOSS 6,129・conflict 0)。
- 機材 (全てpublished byte・実行時にsha照合): union merger `s5_union_merge.py`
  sha256 `90711961…` byte-copy pin (WIN/LOSS conflict検出時の出力拒否gate込み) /
  maker `make_increments_batch26.py` (Part BI版 04bde073のbatch-26 adapt・
  本宣言後に出版してから実行) / refresh `refresh_adoption_1849.py` (published
  Part BC版 `2f77a8bb…` byte-copyのbatch-26 adapt・cache sha期待値はcache
  自体から機械抽出・Board 954d3a10 / policy 78655e94 / quarantine 81d23160) /
  delta extractor `compare_deltas_batch26_adoption.py` (Part BI版 92d83671の
  adapt・本宣言後に出版してから実行) / batch-26 kit 204ファイル
  (MANIFEST af6da4ce・row-audit cb4158d9・batch-keys f1ea43ae) / BASE reaudit
  3出力 (refresh-summary d9d18fc2・closure-classes d57a7609 808行・
  per-root-coverage bc409e63)。
- 本hostの事前preflight (read-only・宣言に先行して実施した点を誠実記録):
  published Part BI BASE refresh (2f77a8bb) を本hostで再実行し3出力とも
  published byteとsha一致で再現済み (d9d18fc2 / d57a7609 / bc409e63・
  probe-worklist `3152855d…` 含む)。read-only機械検査で batch-26 key集合 ==
  class 1849のBASE-unknown費用子53個を確認済み (l028含む・quarantine 0・
  BASE不在53/53)。
- gate群 (fail-closed・全stage): 52 LOSS行の2-pass raw独立再検証 (p1==p2
  node-exact・`# replay_done`・result 2・budget 15M・stones 5・legal/(lo,hi)
  照合・pass-1/pass-2 総nodes 208,202,177/208,202,177)・l028 WIN行のraw再検証
  でincrement不採用 (unadopted_win_ids == [l028] gate) / increments manifest
  (53 resolved / 52 LOSS / 1 WIN unconsumed / exhausted 0 /
  full_packet_eq_loss_only false・win_scenario_exists true・batch-14residual
  q042先例と同一取り扱い) / merge conflict 0・採用行は追加のみでBASE行は
  byte不変 (merge-audit 3回byte一致) / refresh再実行 (class_status_counts
  はBASEと同一・class 1849 unknown_now 53→1・Board fail-closed子境界検証で
  残るunknownはl028 (s5 81011) のみ・per-root coverageはBASEと一致して改善
  のみ) / delta extractor (verdict flips空・new_free空・class 1849の
  BASE-unknown 53子==batch-26 key集合で52行解決・leftover==[81011]==l028・
  holder classのunknown_now減少は自身のmembership分のみ・closure候補表
  ranking churn: 1849 rank 24→2) / 各stageのtamper battery (maker 5種・
  refresh 2種・extractor 4種・計11 probe全検出+復元byte一致・検出後kit 204/204
  再検証)。
- route statement (条件付き・採用後のscheduling quantitiesに過ぎない): 52
  LOSS行採用によりclass 1849の費用子53個のうち52個がcanonical上LOSSとなり、
  l028 (s5 81011) のみunknownとして残る。**l028は28番目のunconsumed closure
  WIN候補 (4系統裏付け) のため、loss-only採用ではclass 1849は決して閉鎖
  しない** (閉鎖資格はl028の採用判断がscrutiny owner C++第二実装 gate を
  通過した後の別法律に依る)。closure候補表上のclass 1849 rankingは24→2
  (unknown_now 1)・joint greedy 38,415→38,301・probe worklist
  64,808→64,754 (いずれも簿記量・勝敗ではない)。被覆・secured・root勝敗の
  主張はrefresh再実行とextractor gateが出す分類deltaのみ。
- 消費規則: 本Partは52 LOSS行のみをcanonical (6,235→6,287) として採用する。
  l028 WIN行はhonest labelのみで読み書きとも非接触・不採用 (28 unconsumed
  closure WIN候補のまま・scrutiny owner C++第二実装 gate pin 9193f5b6のまま
  ・batch-14residual q042先例: Part AS manifest unadopted_win_ids==[q042] と
  同一取り扱い)。canonical chain外の投影は作らない。
- 不接触: batch-27 (Part BR・class 13342・54キー・drive outputsは未出版) に
  は一切触れない (BRは並走所有)。batch 1..25各dir・各residual packet・
  fast lane (y18..y21)・inversive-arc lane・finite-field lane・既存reaudit
  dirs不変。BASE canonical cache f6649fe3はread-only不変。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 1849 (53キーすべて・l028・52 LOSS行を含む)
  は本Partのどの時点でもUNKNOWNのまま。nodes数・簿記量を勝敗として読まない。
- 本amendment observed HEAD-before-push: `4ccf1630062944932654001622477ec6bcfebc67`
  (push直前にnote blob sha1 `86ab7300…` (469,554 bytes) を再照合し、競合時は
  再fetchして本節を追記し直し、成立しない場合は簡潔に記録して次回へ回す)。

## Part BU status update (2026-11-23, solver): batch-26 52-LOSS採用完了 - canonical 6,287行・class 1849はl028 (s5 81011) 1子を残しUNKNOWNのまま (UNKNOWN担保不変)

Part BU (宣言 publication commit `b299f42`・observed HEAD `4ccf1630`) どおり、
batch-26 (class 1849; Part BQ drive-1 l028 WIN-HALT停止 + Part BT residual完走
で53/53 honest label) の52 LOSS行のみをcanonical exact-S5 verdict cacheへ
採用し、refresh再監査・delta extractor全gateを完走した。**l028 WIN行は
不採用** (unadopted_win_ids == ["l028"]・batch-14residual q042先例と同一
取り扱い) を全stageのgateで機械担保した。

- publish-then-execute順序の履行: 計算機材4 scriptを先にmainへ出版
  (commit `33f942a`): maker `838a5c84…` / delta extractor `39606c48…` /
  union merger byte-copy pin `90711961…` / refresh `cf67ace7…`。出版bytesを
  commit-pinned raw fetchで本hostに取得・sha照合 (4/4 byte一致) の上、
  **出版bytesから全pipeline (maker → merger → refresh → extractor) を
  再実行しALL-OK** (maker 4回目 / merger 4回目 (run4 auditはinputのpath
  表記差のみでcache本体byte不変) / refresh 5回目 / extractor 4回目、
  いずれも出版前実行と出力byte一致)。
- tamper battery **14/14 PASS**: maker 5種・refresh 2種・extractor 4種の
  改竄入力を全検出+復元byte一致+検出後 kit 204/204 再検証、control 3件は
  正しく非検出・全出力sha再確認。
- maker全gate PASS: increment 52行 (l001..l027, l029..l053全LOSS) sha256
  `19f6306e6c15e11e4eb3ead4c7cd1189f24210a927dcf0a153c3fe5c26733217`・
  manifest `5db2410b…` (unadopted_win_ids==["l028"] gate・
  full_packet_eq_loss_only false・win_scenario_exists true・52キーのBASE
  (6,235行 `f6649fe3…`) 不在52/52・quarantine 0・総ノード208,202,177/pass
  両pass一致・l028 raw再検証でincrementから除外)。
- merger (selftest PASS): BASE 6,235行 `f6649fe3…` + 52行 =
  **canonical 6,287行** (WIN 158 / LOSS 6,129・dup 0・conflict 0) sha256
  `e32a2e442e77799ea36194f675baeb2424f3410a1d3e681b4c4fbb389f66fe93`
  (259,260 bytes) を
  `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-20261123.cache`
  に出版 (commit C `8f3e487`)。merge-audit run1=run2=run3 `faf6439b…`。
- refresh再実行 (~57s/回) 5回実行・出力byte一致: refresh-summary `51d6bf0d…`
  (worklist_total 64,754・joint greedy 38,301)・closure-classes `e54a0eb8…`
  (807行)・per-root-coverage `c1cb1bf5…`・probe-worklist `9ae1ca50…`
  (**Part AH/AO/AP/AS/AV/BC/BI先例どおり不出版・sha記録のみ**)。
- delta extractor全gate PASS: decomp `33a540c3…`・flips=[]・new_free=[]
  厳密一致 (loss-only packetがfree化できるclassの機械計算listは空)・
  class 1849のBASE-unknown 53子 == batch-26 key集合で52行解決・
  leftover == [81011] == l028・ranking churn gate: class 1849 rank 24→2
  (closure候補表のworklist best-option churnのみ: left [5213, 18933] /
  entered [1349, 1906]、各churned classのstatusは不変)・update8
  newly_resolved 0。
- 機械確定 (簿記量・勝敗ではない): **class 1849 unknown_now 53→1**
  (残るunknownはl028 (s5 81011) のみ・Board fail-closed子境界検証PASSで
  確認)・**class 1849は本採用では閉じない** (l028は28 unconsumed closure
  WIN候補 (Part BS第三実装交叉検証込み4系統裏付け) のためloss-only採用では
  閉鎖資格なし・採用判断はscrutiny owner C++第二実装 gate pin `9193f5b6…`
  通過後の別法律)・free_now 38不変・unknown 34,498不変・closure候補表807
  不変 (rank churn 24→2のみ)・root 27 (known-loss-baseline) 119/119不変・
  class 23101はrank 1 / unknown_now 1のまま・joint greedy 38,415→38,301
  (delta -114)・probe worklist 64,808→64,754 (delta -54)・update8 resolved
  133不変。
- verdict不消費: l028 WIN行 (2-pass node-exact result 1・4,893,014 nodes) は
  読み書きとも非接触のまま (**28 unconsumed closure WIN候補不变**)。
- publication series (各commitともfetch-back byte検証済み): `b299f42`
  (declaration note amendment) → `33f942a` (A: 実験dir scripts 4) →
  `694c816` (B1: increment + manifest + merge-audit×3) → `8dc3bd64`
  (B2: decomp-deltas + reaudit 3出力) → `8f3e487` (C: merged canonical
  cache 259,260 bytes) → `f613ded0` (D: README + MANIFEST-sha256・
  15ファイル明示列挙) → 本status update commit。実験dir:
  `research/experiments/n11-centralreply-class1849-loss52-adoption-reaudit-20261123/`。
- 不接触: batch-27 (Part BR・並走) のdrive outputsは本status update時点で
  mainに存在せず不接触のまま。並走 K1252 (Pfaffian訂正 `32d1d88…`)・
  y=22族パラメトリックfit単一オーナー宣言 (`c0baada6`) は別laneで本Partと
  無関係 (本Partの成果・読み書きに一切依存しない)。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・二石root {49,60}/
  {59,60}・S2 {59,60}・class 1/2/4・class 1849 (53キーすべて・l028・52 LOSS行
  を含む) は本status update時点でも**UNKNOWN**のまま。nodes数・worklist数・
  greedy union size等のscheduling quantities (簿記量) を勝敗・距離として
  読まない。
- 本status update observed HEAD-before-push:
  `292c408be8d1d73ed87d022f87c5bef47bd7c530` (並走finite-field laneの
  arc-bounds summary・本Partと無関係・note.md不変を確認済みで再取得した
  最新main HEAD。Part BU series上一番直近の本レーンcommitはcommit D
  `f613ded0`)。push直前に最新mainを再fetchし note blob lock
  `91aee50fdad63a7406ae0902ea7563313d514778` (476,026 bytes) を再照合する
  (batch-27 status update等の並走追記が挟まった場合は本節を追記し直し、
  成立しない場合は簡潔に記録して次回へ回す)。

## Part BV (verifier, amendment 2026-11-23, 実行前に宣言): batch-23 s001/s002 WIN行の第三実装交叉検証 + 本host pinned-replica再現 (verdict不消費)

batch-23 (Part BN) で出版されたWIN行 s001/s002 (canonical outputs commit
`597d810`・scaffold `52ff9a09`・README+MANIFEST `4dad105b`・2-pass
fresh-cold node-exact・replay result 1・nodes 5,415,927 / 9,329,444・
budget 15M内・両worker最初のキーでWIN-HALT) に対し、前例 (Part
G/K/O/P/T/W/AA/AD/AG/AL/AR/AZ/BF/BK/BM/BS) と同じpinned第三実装
(non-df-pn AND/OR minimax) によるverdict-level交叉検証を、本セッションが
単一オーナーとして実行する (同一スコープの対抗宣言・amendmentが本
amendmentより先にmainにある場合は本宣言を破棄して着手しない・本宣言時点
でnote grep clean・`n11-centralreply-closure-b23win-thirdimpl-20261123`
dirの不存在を確認済み)。誠実な相違点の開示: batch-23 drive-1はPart BN
執行hostの単一host出版であり Part BS 時のl028のような第二host同時再現
は出版されていない。よって本Partの「本host pinned-replica再現」は
s001/s002にとって最初の独立host再現である (rc=45 WIN-HALT時点の
51キー残留 (s003..s053) fileless UNPROBEDには一切触れない)。

- 対象: `research/experiments/n11-centralreply-closure-b23win-thirdimpl-20261123/`。
  target 2行: **s001** (key (1152921505294712832, 32768)・s5 62435・
  legal 78・replica_result 1・replica_nodes 5,415,927・holder class
  31600 (unknown)・membership_class_count 4・batch-keys `2776acaf…`)・
  **s002** (key (3458764514374189056, 32768)・s5 192809・legal 88・
  replica_result 1・replica_nodes 9,329,444・membership_class_count 4)。
- 機材 (全てpublished byte・実行時にsha照合): third_impl.js `08ea958f…`・
  verify_tbl.js `c8c52528…`・jsreplay.js replica `84585617…`・runner
  `run_thirdimpl.sh` (BF正本byte-copy `a0b77d83…`)・maker
  `make_inputs_bv.py` `a4031abe…` (BS maker `313a8d71…`のbatch-23正本
  sourcesへのhonest adapt: 対象2行・b23 pin群 (batch-keys/status/README/
  row-audit/raw 4/published-input 2)・status.log 4行電池 (PASS 2 +
  WIN-HALT 2・retry行なし)・row-audit電池 (win_rows 2行・pass_rows 0・
  fragment_keys {})・README文言gate・rows.json schema s/b26/b23/)・
  audit gate battery `audit.py` `08bdebce…` (BS audit `afc4da1d…`の
  b23win版 adapt: EXP/SCHEMA/rows-schema・target-count 1→2・header文言
  のみ変更・gateロジック不変)。
- 前提ゲート (fail-closed・全て機械検査・宣言時点で実施済み): maker全
  gate PASS (BV-SCAFFOLD)・4回実行byte一致 (`__pycache__`衛生)・input/
  rows.json再生成byte一致 (`61703c08…`)・tamper battery **6/6検出** (T1
  raw pin 1bit・T2 row-audit pin 1bit・T3 README pin 1bit・T4 row-audit
  内容改変 (win_rows ["s001","s002"]→["s003","s001","s002"])・T5 raw
  内容改変 (s001 p1 nodes 5415927→5415928)・T6 published-input pin 1bit・
  scratch上で実施し実験sources無改変byte検証・T4/T5はsha-pin層で検出
  (BS先例 T4/T5と同型))・clean control PASS。
- sources sha pin: batch-keys-b23 `2776acaf…` (53キー・class 31600)・
  status-b23.log `1e4ccea9…` (4行 = PASS 2 + WIN-HALT 2・PASS key集合 ==
  row-audit win_rows (s001,s002) 機械交叉導出・truncated-retry行ゼロ)・
  README-b23 `f38922ca…` (s001/s002 WIN honest label・5,415,927・
  9,329,444・22番目・23番目の unconsumed closure WIN 候補・Part BN識別
  文言)・row-audit-winhalt-b23 `14aa7f63…` (probed 2・pass_rows 0・
  win_rows [s001, s002]・fragment_keys {}・fileless_unprobed 51・
  derived_state true・input_sha256 == batch-keys pin)・raw s001 p1/p2
  `84463069…`/`cd7633fb…`・raw s002 p1/p2 `39664259…`/`8ce83037…`
  (各2-pass node-exact + result 1 in-budget + status/row-audit/README
  3-way照合・4ファイルは互いに非同一 (wall_s差))・published input CSV
  byte-equality `422161a1…`/`32257e8e…`・BF anchor/negative CSV
  byte-equality (provenance chain AR→BF→BK→BM→BS→BV)。
- val-gate (本host jsreplay健全性): batch-23 scaffold val-gate input 4 +
  published-baseline 4をbyte-copyし・本host再生成4件 (at2m budget 2M
  exhaustion ×2・15m基準キー budget 15M・published baseline (2,
  3,651,923)/(2, 5,040,200)・禁止四角 95,670) がpublished baselineと
  一致 (wall_s比較外) することを本Part実行の第0步として記録する。
  本host .out 4件を出版する。
- 実行protocol (宣言時点で事前登録・順序も含め固定・逐次実行):
  1. rules gate: pinned `verify_tbl.js`でreplica quads 95,670 ==
     third-impl quads 95,670・triples checked mismatch 0。
  2. val-gate this-host 4件。
  3. 本host pinned-replica再現: pinned replica (jsreplay `84585617…`) で
     s001・s002を各々budget 15M・fresh-cold・逐次2回 (p1/p2) 実行し、
     決定性 fields p1==p2・published raw fields (result 1・nodes
     5,415,927 / 9,329,444) との一致をauditで機械検査する。
     exhaustion/mismatch/truncationはhonest記録のみとし検証主張としない。
  4. negatives ng1/ng2のGATE_FAIL確認 (fail-closed設計どおり) → anchors
     k02a (WIN 9,106,337 exp / 4,991,527 ttHits)・l1a (LOSS 7,660,602 /
     3,951,175) の本host node-exact再現 (a/b 2回)。
  5. targets s001/s002は1行=1solver=1プロセス・cap 300,000,000・wallcap
     240s・`--memo-power=22`・a/b 2回のdeterminism gate
     (result/expansions/ttHits/reason同一必須)・逐次実行。wall超過は
     honest wall-inconclusiveとし検証主張としない。事前の機械予想は
     宣言時に残さない (実測を待つ)。
- 監査: `audit.py` (G0 input/rows照合・G1 script pin 3種・G2 rules gate・
  G2b replica-thishost・G3 anchors・G4 negatives・G5 targets/verdict
  agreement) 3回実行byte一致・audit tamper battery 3種 (T1 maker pin
  反転→ABORT・T2 auditのtarget det-pair改ざん→DIVERGENCE検出・T3 G0の
  input改ざん→gate fail・scratch上で実施し実験files無改変byte検証)・
  clean control PASS。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・**verdict不消費**
  (s001/s002の採用判断は引き続きscrutiny owner C++第二実装 gate pin
  `9193f5b6…` のまま)。第三実装verdictがcleanにreplica verdictと一致
  した場合は「一致した」事実のみ記録し、clean不一致はdivergence
  evidenceとして記録するが本レーンではverdictを書き換えない。閉鎖・
  被覆・secured・root勝敗の主張をしない。
- 不接触: canonical cache (Part BU採用後 6,287行 `e32a2e44…`) への書き
  込みなし・28 unconsumed closure WIN候補の採用状態不変・batch-21/22
  残留キー・batch-23残留51キー (s003..s053) に一切触れない・**batch-27
  (Part BR) の54キー・scaffold・drive・outputsには一切触れない (BRは並走
  所有・drive outputsは本宣言時点でmainに存在しない)**・batch-24/25
  (y001/y006・i001/i002) は本Partでは候補として非接触・fast lane
  (y18..y22族)・finite-field lane・inversive-arc lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 31600 (53キーすべて・
  s001/s002を含む) は本Partのどの時点でもUNKNOWNのまま。nodes数・
  expansions数・ttHits数を勝敗として読まない。WIN/LOSS採用は別宣言の
  adoption Part (pinned fail-closed merger `90711961` 経由) のみ。

## Part BV status update (2026-11-23, verifier): batch-23 s001/s002 第三実装交叉検証完了 - 本host pinned-replica初の独立host再現 + clean WIN一致2/2 (UNKNOWN担保不変)

Part BV (宣言 publication commit `d58afadd`・observed HEAD-before-push
`d2114935`〔並走finite-field lane docs・非接触〕・実行前に出版) どおり、
batch-23 (class 31600) WIN行 s001/s002 のpinned第三実装交叉検証と本host
pinned-replica再現を完遂し、全成果をmainに出版した (verdict不消費)。

- publish-then-execute順序の履行: 宣言 `d58afadd` → A `db195667`
  (scaffold 35ファイル = scripts 6 + input 7 + sources 14 + val-gate
  input/published-baseline 8・35/35 fetch-back byte一致) → B `8b6a1048`
  (outputs 24ファイル = output 20 + val-gate this-host 4・24/24一致) →
  C `6abf8097` (README + MANIFEST-sha256 59行・2/2一致) → 本status
  update。全出版bytesはcommit-pinned raw fetch-backでbyte検証済み。
- 実行 (宣言protocol順・逐次): (1) **rules gate PASS** (verify_tbl
  `c8c52528…`・replica quads 95,670 == third-impl quads 95,670・triples
  checked 195,044・mismatch 0)。(2) **val-gate this-host 4/4 node-exact**
  (jsreplay `84585617…`・published baselineと一致 (wall_s除外): at2m
  2M exhaustion ×2 (result 0, nodes 2,000,000)・15m基準キー budget 15M
  (2, 3,651,923)/(2, 5,040,200)・禁止四角 95,670)。(3) **本host
  pinned-replica再現 4/4 完全一致**: s001 p1/p2 = result 1・nodes
  5,415,927 (two-pass node-exact・wall 26/25s)・s002 p1/p2 = result 1・
  nodes 9,329,444 (two-pass node-exact・wall 46/48s)・published batch-23
  raw fieldsとの一致をaudit G2bで機械検査 (EXHAUSTED 0・mismatch 0・
  truncation 0)・**s001/s002にとって初の独立host再現** (Part BSのl028
  と違いbatch-23は単一host出版だった)。(4) **negatives 2/2 GATE_FAIL
  設計どおり** (ng1 legal count mismatch derived=87 declared=88・ng2
  stone count mismatch bits=5 declared=6)。(5) **anchors 2/2 本host
  node-exact** (a/b determinism PASS): k02a clean WIN 9,106,337 exp /
  4,991,527 ttHits・l1a clean LOSS 7,660,602/3,951,175 (published第三実装値
  と完全一致)。(6) **targets 2/2 clean WIN一致**: s001 clean WIN
  (result 1) 6,227,131 exp / 3,553,011 ttHits (wall 18.11/18.47s)・s002
  clean WIN (result 1) 11,072,137 / 6,076,075 (wall 32.06/32.49s)・
  cap 300,000,000・wallcap 240s・memo-power=22・**WALL-INCONCLUSIVE 0・
  DIVERGENCE 0** (pass-one合計 17,299,268・replica行との比率 1.150/
  1.187)。
- 監査: audit.py (BV版 `08bdebce…`・schema `n11-centralreply-closure-
  b23win-thirdimpl-audit-v1`) **ALL 67 GATES PASS**・3回実行byte一致
  (audit-run1=2=3)・audit-summary.jsonは決定的 (タイムスタンプ不読)・
  target det-pair改ざん/dir内pin反転/G0 input改ざんの**audit tamper
  battery 3/3検出** (scratch上・実験files無改変byte検証) + clean control
  PASS。宣言前に行った**maker全gate PASS** (BV-SCAFFOLD) + 4回byte一致 +
  **maker tamper battery 6/6検出** (raw pin 1bit・row-audit pin 1bit・
  README pin 1bit・row-audit内容改変・raw内容改変 (nodes 5415927→
  5415928)・published-input pin 1bit・T4/T5はsha-pin層で検出) +
  clean control PASS も確認済み。
- 意味 (route statementのみ・閉鎖/被覆/secured/root勝敗の主張なし):
  s001/s002 (22番目・23番目の unconsumed closure WIN候補) は (a) Part BN
  drive-1 published replica (b) 本host pinned-replica 2-pass node-exact
  (独立host) (c) 独立第三実装 clean WIN一致 の**3系統裏付け**となった
  (同一クラス内2WINペアの第三実装交叉検証は Part BF (batch-19 w001/w002)
  以来2例目・pair型ではa003/k002/l028に続く4,5,6番目の候補のクロス検証)
  。ただし **verdictは一切消費していない**・採用判断は scrutiny owner
  C++第二実装 gate pin `9193f5b6…` 待ちで本レーンは代行しない・
  canonical cache (Part BU採用後 6,287行 `e32a2e44…`) read-only不変・
  28 unconsumed closure WIN候補の採用状態・簿記は一切不変。
- 不接触: batch-21/22残留キー・batch-23残留51キー (s003..s053 fileless
  UNPROBEDのまま)・batch-27 (Part BR) の54キー/scaffold/drive/outputs
  (BRは並走所有・outputsは本status update時点でもmainに存在せず)・
  batch-24/25 (y001/y006・i001/i002 WIN行は本Part非接触・次のverifier
  候補)・fast lane (y=22 universal宣言 `e1e60cd4` は並走非接触)・
  finite-field lane非接触。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 31600 (53キーすべて・
  s001/s002を含む) は本status update時点でも**UNKNOWN**のまま。nodes数・
  expansions数・ttHits数を勝敗・距離として読まない。
- 本status update observed HEAD-before-push: `6abf8097…` (本Part
  commit Cそのもの。並走非接触コミットは y=22 universal single-owner宣言
  `e1e60cd4` のみ)。push直前に最新mainを再fetchし note blob lock
  `3c31aa353240c37cae7149bbce445b07e55e436f` (489,824 bytes = 宣言
  `d58afadd` 版) を再照合する (batch-27 status update等の並走追記が挟まった
  場合は本節を追記し直し、成立しない場合は簡潔に記録して次回へ回す)。

## Part BW (verifier, amendment 2026-11-23, 実行前に宣言): batch-24 y001/y006 WIN行の第三実装交叉検証 + 本host pinned-replica再現 (verdict不消費)

batch-24 (Part BO) で出版されたWIN行 y001/y006 (canonical outputs commit
`18420555`・scaffold `d7ee67c7`・README+MANIFEST `d4c0074e`・宣言 `2c91e033`・
2-pass fresh-cold node-exact・replay result 1・nodes 5,291,064 / 5,321,639・
budget 15M内・WIN-HALT rc=45 (worker1の最初のキー y001・worker2の3番目のキー
y006)) に対し、前例 (Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AZ/BF/BK/BM/BS/BV) と
同じpinned第三実装 (non-df-pn AND/OR minimax) によるverdict-level交叉検証を、
本セッションが単一オーナーとして実行する (同一スコープの対抗宣言・amendmentが
本amendmentより先にmainにある場合は本宣言を破棄して着手しない・本宣言時点で
note grep clean・`n11-centralreply-closure-b24win-thirdimpl-20261123` dirの
不存在を確認済み)。誠実な相違点の開示: batch-24 drive-1はPart BO執行hostの
単一host出版であり Part BS 時のl028のような第二host同時再現は出版されて
いない。よって本Partの「本host pinned-replica再現」はy001/y006にとって
最初の独立host再現である (rc=45 WIN-HALT時点の49キー残留 (y003, y005,
y007..y053) fileless UNPROBEDには一切触れない。同batchのLOSS行 y002/y004
(adoption candidatesのみ) も本Part対象外・出版正本は読み取りのみ)。

- 対象: `research/experiments/n11-centralreply-closure-b24win-thirdimpl-20261123/`。
  target 2行: **y001** (key (10376293541461753856, 264)・s5 91296・legal 87・
  replica_result 1・replica_nodes 5,291,064・holder class 16957 (unknown)・
  membership_class_count 2・batch-keys `486858d6…`)・**y006** (key
  (1152921504607043584, 264)・s5 368510・legal 84・replica_result 1・
  replica_nodes 5,321,639・membership_class_count 2)。
- 機材 (全てpublished byte・実行時にsha照合): third_impl.js `08ea958f…`・
  verify_tbl.js `c8c52528…`・jsreplay.js replica `84585617…`・runner
  `run_thirdimpl.sh` (BF正本byte-copy `a0b77d83…`)・maker
  `make_inputs_bw.py` `f94d6e4f…` (BV maker `a4031abe…`のbatch-24正本
  sourcesへのhonest adapt: 対象2行 y001/y006・b24 pin群 (batch-keys/status/
  README/row-audit/raw 4/published-input 2)・status.log 6行電池 (PASS 4 +
  WIN-HALT 2・retry行なし・loss-row gate新設: 各PASS行はtarget WIN行
  (result 1・published nodes) またはrow-audit loss_rows (y002/y004・
  result 2・published loss nodes 217,944/632,091) のいずれかでなければ
  ABORT)・row-audit電池 (win_rows 2行・loss_rows 2行・pass_rows 2・probed
  4・unprobed 49・stop_rule文言gate)・README文言gate・rows.json schema
  s/b23/b24/)・audit gate battery `audit.py` `3a2ce7ef…` (BV audit
  `08bdebce…`のb24win版 adapt: EXP/SCHEMA/rows-schema・target-count文言
  のみ変更・gateロジック不変)。
- 前提ゲート (fail-closed・全て機械検査・宣言時点で実施済み): maker全
  gate PASS (BW-SCAFFOLD)・4回実行byte一致 (`__pycache__`衛生)・input/
  rows.json再生成byte一致 (`92e9f999…`)・tamper battery **7/7検出** (T1
  raw pin 1bit・T2 row-audit pin 1bit・T3 README pin 1bit・T4 row-audit
  内容改変 (win_rows ["y001","y006"]→["y007","y001","y006"])・T5 raw
  内容改変 (y001 p1 nodes 5291064→5291065)・T6 published-input pin 1bit・
  **T7 status.log loss-row verdict反転 (y002 PASS result 2→1)**・scratch
  上で実施し実験sources無改変byte検証・T4/T5/T7はsha-pin層で検出)・
  clean control PASS。
- sources sha pin: batch-keys-b24 `486858d6…` (53キー・class 16957・schema
  `n11-centralreply-closure-class16957-batch24-input-v1`)・status-b24.log
  `dcba6b0e…` (6行 = PASS 4 + WIN-HALT 2・PASS key集合 == row-audit
  win_rows (y001,y006) ∪ loss_rows (y002,y004) 機械交叉導出・
  truncated-retry行ゼロ)・README-b24 `672d18cf…` (y001/y006 WIN honest
  label・5,291,064・5,321,639・y002/y004 LOSS adoption candidate文言・
  217,944・632,091・24番目・25番目の unconsumed closure WIN候補・Part BO
  識別文言)・row-audit-winhalt-b24 `9d073038…` (probed 4・pass_rows 2・
  win_rows [y001,y006]・loss_rows [y002,y004]・fragment_keys {}・
  unprobed_count 49・derived_state true・stop_rule事前登録文言)・
  input_sha256 == batch-keys pin)・raw y001 p1/p2 `03ae7d71…`(2ファイル
  同一bytes・wall 53/53s)・raw y006 p1/p2 `2c21a9e1…`/`1e2b6d13…`
  (2-pass node-exact + result 1 in-budget + status/row-audit/README 3-way
  照合)・published input CSV byte-equality `f746648e…`/`34db2f1f…`・BF
  anchor/negative CSV byte-equality (provenance chain AR→BF→BK→BM→BS→BV→BW)。
- val-gate (本host jsreplay健全性): batch-24 scaffold val-gate input 4 +
  published-baseline 4をbyte-copy (b23/BV実験の該当8ファイルと全byte同一
  であることをb24正本raw fetchで再確認済み)し・本host再生成4件 (at2m
  budget 2M exhaustion ×2・15m基準キー budget 15M・published baseline (2,
  3,651,923)/(2, 5,040,200)・禁止四角 95,670) がpublished baselineと一致
  (wall_s比較外) することを本Part実行の第0步として記録する。本host .out
  4件を出版する。
- 実行protocol (宣言時点で事前登録・順序も含め固定・逐次実行):
  1. rules gate: pinned `verify_tbl.js`でreplica quads 95,670 ==
     third-impl quads 95,670・triples checked mismatch 0。
  2. val-gate this-host 4件。
  3. 本host pinned-replica再現: pinned replica (jsreplay `84585617…`) で
     y001・y006を各々budget 15M・fresh-cold・逐次2回 (p1/p2) 実行し、
     決定性 fields p1==p2・published raw fields (result 1・nodes
     5,291,064 / 5,321,639) との一致をauditで機械検査する。
     exhaustion/mismatch/truncationはhonest記録のみとし検証主張としない。
  4. negatives ng1/ng2のGATE_FAIL確認 (fail-closed設計どおり) → anchors
     k02a (WIN 9,106,337 exp / 4,991,527 ttHits)・l1a (LOSS 7,660,602 /
     3,951,175) の本host node-exact再現 (a/b 2回)。
  5. targets y001/y006は1行=1solver=1プロセス・cap 300,000,000・wallcap
     240s・`--memo-power=22`・a/b 2回のdeterminism gate
     (result/expansions/ttHits/reason同一必須)・逐次実行。wall超過は
     honest wall-inconclusiveとし検証主張としない。事前の機械予想は
     宣言時に残さない (実測を待つ)。
  6. 監査: `audit.py` (G0/G1/G2/G2b/G3/G4/G5・BV版と同一gate構成・schema
     `n11-centralreply-closure-b24win-thirdimpl-audit-v1`) 3回実行byte
     一致・audit tamper battery 3種 (T1 maker pin反転→ABORT・T2 auditの
     target det-pair改ざん→DIVERGENCE検出・T3 G0のinput改ざん→gate
     fail・scratch上で実施し実験files無改変byte検証)・clean control PASS。
  7. 出版: A scaffold (scripts + input + sources + val-gate) → B outputs
     (rules-gate・val-gate this-host・replica p1/p2・negative・anchors a/b・
     targets a/b・audit 3回分・audit-summary・status.log) → C README +
     MANIFEST-sha256 → 本noteへのstatus update。全出版bytesはcommit-pinned
     raw fetch-backでbyte検証する。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・**verdict不消費**
  (y001/y006の採用判断は引き続きscrutiny owner C++第二実装 gate pin
  `9193f5b6…` のまま)。第三実装verdictがcleanにreplica verdictと一致
  した場合は「一致した」事実のみ記録し、clean不一致はdivergence
  evidenceとして記録するが本レーンではverdictを書き換えない。閉鎖・
  被覆・secured・root勝敗の主張をしない。
- 不接触: canonical cache (Part BU採用後 6,287行 `e32a2e44…`) への書き
  込みなし・28 unconsumed closure WIN候補の採用状態不変・batch-23/24
  残留キー (s003..s053・y003/y005/y007..y053 fileless UNPROBED) に一切
  触れない・batch-24の y002/y004 LOSS行 (adoption candidate) には本Part
  は出版正本の読み取りのみで一切書き込まない・batch-25 (i001/i002 WIN
  行)・**batch-27 (Part BR) の54キー・scaffold・drive・outputsには一切
  触れない (BRは並走所有・drive outputsは本宣言時点でmainに存在しない)**
  ・fast lane (y18..y22族・y=22 universal宣言 `e1e60cd4` 含む)・
  finite-field lane・inversive-arc lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 16957 (53キーすべて・
  y001/y006・y002/y004を含む) は本Partのどの時点でもUNKNOWNのまま。
  nodes数・expansions数・ttHits数を勝敗として読まない。WIN/LOSS採用は
  別宣言の adoption Part (pinned fail-closed merger `90711961` 経由)
  のみ。 scrutiny owner C++第二実装 gate `9193f5b6…` 待ちは本レーンは
  代行しない。
- 本宣言 observed HEAD-before-push: `cad4f7b4…` (並走q=13 arc laneの
  K1058・本Partと無関係・note.md不変を確認済みで再取得した最新main HEAD)。
  push直前に最新mainを再fetchし note blob lock
  `4d6694e7a04bab3115b627ceb5919d4448fe72ac` (495,245 bytes = Part BV
  status update `51a8be8d` 版) を再照合する (y=22 lane等の並走追記が
  夾まった場合は本節を追記し直し、成立しない場合は簡潔に記録して次回へ
  回す)。

## Part BR takeover amendment (solver, 2026-11-23, 実行前に出版): batch-27 (class 13342) drive-1実行のtakeover宣言 (publish-then-execute・verdict不消費)

本文はPart BR宣言 (commit `14ee1873`・scaffold `93ef3f89`、2026-11-23T08:35:59Z/08:36:23Z出版) の引継ぎ実行宣言である。takeover事由 (本amendment執筆直前の2026-11-23T12:29Z最新main再取得): (a) batch-27のdrive outputs・status update・row-auditはいずれもmainに存在しない (b) 宣言以降にPart BS/BT/BU/BV/BW (6abf8097・8b6a1048等) とfast lane・finite-field lane・inversive-arc laneの多数コミットが挟まり、いずれのセッションもBRを「並走所有・非接触」と明記したまま宣言から3時間以上drive成果が出版されていない (c) 対抗するBR実行開始宣言・第二のtakeover宣言はnote grep上存在しない。よって本セッションがdrive-1実行の単一オーナーとしてtakeoverする (成立しない場合は簡潔に記録して次回へ回す)。

- scaffold pin再照合 (本host・fetch-back bytes・sha256): drive_batch27.sh `9114e211…`・jsreplay.js `84585617…`・make_batch27_keys.py `9ab4523a…`・row_audit_batch27.py `ed21debe…`・row_audit_batch27_win_halt.py `7d920f2b…`・runbatch.sh `f591f8c2…`・runwave.sh `8efd78c2…`・input/batch-keys.json `67814ed6…` (schema `n11-centralreply-closure-class13342-batch27-input-v1`・54キー o001..o054・s5昇順 98526..460214・legal 74..100・membership)。54 input CSVの (id, lo, hi, legal) とbatch-keys全行一致を機械照合済み (bad 0)。実行は宣言済みプロトコルを1行も改変しない。
- 実行protocol (Part BR宣言 `14ee1873` の事前登録どおり): (1) val-gate this-host 4件 (published-baseline 4組: at2m budget 2M exhaustion ×2・15m基準キー budget 15M (2, 3,651,923)/(2, 5,040,200)・wall_s比較外・禁止四角 95,670)。 (2) drive_batch27.sh によるbounded invocation 260s×2worker (runbatch `f591f8c2` byte-pin)・2-pass fresh cold・budget 15M・WINは rc=45でWIN-HALT (honest label・verdict不消費)・determinism mismatchは rc=42 HARD-STOP・budget不足はhonest EXHAUSTED (同一条件での再probeなし)。 (3) row-audit 3回実行byte一致 + tamper battery (scratch上で実施・実験files無改変byte検証)。 (4) 出版: outputs (status.log・raw・val-gate this-host 4・row-audit json) → README + MANIFEST-sha256 → 本note status update。全出版bytesはcommit-pinned raw fetch-backでbyte検証する。
- 主張と消費規則: verdict不消費。WIN/LOSS採用は別adoption宣言 (pinned fail-closed merger `90711961`) 経由のみ・採用判断はscrutiny owner C++第二実装 gate pin `9193f5b6…` 待ち (本レーンは代行しない)。canonical cache (Part BU採用後 6,287行 `e32a2e44…`) read-only不変・28 unconsumed closure WIN候補の採用状態不変。閉鎖・被覆・secured・root勝敗の主張をしない。nodes数・expansions数を勝敗・距離として読まない。
- 不接触: Part BW (batch-24 verifier・並走所有) のscaffold/outputs・batch-23/24/25残留キー (s003..s053・y003/y005/y007..y053・i003..i053 fileless UNPROBED)・batch-26残留 (l028含む)・batch-25 i001/i002 WIN行の第三実装交叉検証 (次のverifier候補)・fast lane・finite-field lane・inversive-arc lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 13342 (54キーすべて) は本Partのどの時点でもUNKNOWNのまま。
- 本amendment observed HEAD-before-push: `855778a2…` (並走verifier lane Part BW commit B outputs・本lane非接触・note.md不変を確認済み)。push直前に最新mainを再fetchし note blob lock `b35ce499f72c39a5dccf4b0103bdd0d325077424` (504,869 bytes = Part BW宣言 `9f5b9b3c` 版) を再照合する (Part BWの更なるoutputsや他セッションのbatch-27実行成果が夾まった場合は本節を追記し直し、成立しない場合は簡潔に記録して次回へ回す)。

## Part BW status update (2026-11-23, verifier): batch-24 y001/y006 第三実装交叉検証完了 - 本host pinned-replica初の独立host再現 + clean WIN一致2/2 (UNKNOWN担保不変)

Part BW (宣言 publication commit `9f5b9b3c`・observed HEAD-before-push
`cad4f7b4`〔並走非接触〕・実行前に出版) どおり、batch-24 (class 16957)
WIN行 y001/y006 のpinned第三実装交叉検証と本host pinned-replica再現を完遂
し、全成果をmainに出版した (verdict不消費)。

- publish-then-execute順序の履行: 宣言 `9f5b9b3c` → A `ed77d6b6`
  (scaffold 35ファイル = scripts 6 + input 7 + sources 14 + val-gate
  input/published-baseline 8・35/35 fetch-back byte一致) → B `855778a2`
  (outputs 24ファイル = output 20 + val-gate this-host 4・24/24一致) →
  C `bfa533ca` (README + MANIFEST-sha256 59行・2/2一致) → 本status
  update。全出版bytesはcommit-pinned raw fetch-backでbyte検証済み。
- 実行 (宣言protocol順・逐次): (1) **rules gate PASS** (verify_tbl
  `c8c52528…`・replica quads 95,670 == third-impl quads 95,670・triples
  checked 195,044・mismatch 0)。(2) **val-gate this-host 4/4 node-exact**
  (jsreplay `84585617…`・published baselineと一致 (wall_s除外): at2m
  2M exhaustion ×2 (result 0, nodes 2,000,000)・15m基準キー budget 15M
  (2, 3,651,923)/(2, 5,040,200)・禁止四角 95,670)。(3) **本host
  pinned-replica再現 4/4 完全一致**: y001 p1/p2 = result 1・nodes
  5,291,064 (two-pass node-exact・wall 26/26s)・y006 p1/p2 = result 1・
  nodes 5,321,639 (two-pass node-exact・wall 26/25s)・published batch-24
  raw fieldsとの一致をaudit G2bで機械検査 (EXHAUSTED 0・mismatch 0・
  truncation 0)・**y001/y006にとって初の独立host再現** (Part BSのl028
  と違いbatch-24は単一host出版だった)。(4) **negatives 2/2 GATE_FAIL
  設計どおり** (ng1 legal count mismatch derived=87 declared=88・ng2
  stone count mismatch bits=5 declared=6)。(5) **anchors 2/2 本host
  node-exact** (a/b determinism PASS): k02a clean WIN 9,106,337 exp /
  4,991,527 ttHits・l1a clean LOSS 7,660,602/3,951,175 (published第三実装値
  と完全一致)。(6) **targets 2/2 clean WIN一致**: y001 clean WIN
  (result 1) 6,097,380 exp / 3,451,878 ttHits (wall 17.40/17.46s)・
  y006 clean WIN (result 1) 6,190,624 / 3,326,421 (wall 16.95/16.95s)・
  cap 300,000,000・wallcap 240s・memo-power=22・**WALL-INCONCLUSIVE 0・
  DIVERGENCE 0** (pass-one合計 12,288,004・replica行との比率 1.153/
  1.163)。
- 監査: audit.py (BW版 `3a2ce7ef…`・schema `n11-centralreply-closure-
  b24win-thirdimpl-audit-v1`) **ALL 67 GATES PASS**・3回実行byte一致
  (audit-run1=2=3)・audit-summary.jsonは決定的 (タイムスタンプ不読)・
  target det-pair改ざん/dir内pin反転/G0 input改ざんの**audit tamper
  battery 3/3検出** (scratch上・実験files無改変byte検証) + clean control
  PASS。宣言前に行った**maker全gate PASS** (BW-SCAFFOLD) + 4回byte一致 +
  **maker tamper battery 7/7検出** (raw pin 1bit・row-audit pin 1bit・
  README pin 1bit・row-audit内容改変・raw内容改変 (nodes 5291064→
  5291065)・published-input pin 1bit・**status.log loss-row verdict反転
  (y002 PASS result 2→1)**・T4/T5/T7はsha-pin層で検出) + clean control
  PASS も確認済み。
- 意味 (route statementのみ・閉鎖/被覆/secured/root勝敗の主張なし):
  y001/y006 (24番目・25番目の unconsumed closure WIN候補) は (a) Part BO
  drive-1 published replica (b) 本host pinned-replica 2-pass node-exact
  (独立host) (c) 独立第三実装 clean WIN一致 の**3系統裏付け**となった
  (同一クラス内2WINペアの第三実装交叉検証は Part BF (batch-19
  w001/w002)・Part BV (batch-23 s001/s002) に続く**3例目**)。ただし
  **verdictは一切消費していない**・採用判断は scrutiny owner C++
  第二実装 gate pin `9193f5b6…` 待ちで本レーンは代行しない・
  canonical cache (Part BU採用後 6,287行 `e32a2e44…`) read-only不変・
  28 unconsumed closure WIN候補の採用状態・簿記は一切不変。
- 不接触: batch-23/24残留キー (s003..s053 51キー・y003/y005/y007..y053
  49キー fileless UNPROBEDのまま)・batch-24の y002/y004 LOSS行
  (adoption candidate・本Partは出版正本の読み取りのみ)・batch-25
  (i001/i002 WIN行)・batch-27 (Part BR) の54キー/scaffold/drive/outputs
  (BRは本status update直前の12:31:32Zに並走がtakeover宣言 `d2e345e6`
  を出版済み・本Part BWとは非接触と同amendmentにも明記・outputsは本
  status update時点でもmainに存在せず)・
  fast lane (y=22 universal宣言 `e1e60cd4` は並走非接触)・finite-field
  lane・inversive-arc lane (K1254 `2489d763`・q=13 arc `cad4f7b4` 等
  並走非接触commit)非接触。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 16957 (53キーすべて・
  y001/y006・y002/y004を含む) は本status update時点でも**UNKNOWN**の
  まま。nodes数・expansions数・ttHits数を勝敗・距離として読まない。
- 本status update observed HEAD-before-push: `bfa533ca…` (本Part
  commit Cそのもの。commit B→Cの間に並走のPart BR takeover amendment
  `d2e345e6` (12:31:32Z・note追記・本Part BW宣言prefixは無改変を
  byte検証済み) が挟まった。その他の並走非接触コミットは q=13/有限体/
  inversive-arc laneの諸commitのみ)。push直前に最新mainを再fetchし
  note blob lock `f412fcc4f6030867598a66598d36f290c948b342`
  (508,970 bytes = Part BR takeover amendment `d2e345e6` 版) を再照合
  する (さらに並走追記が挟まった場合は本節を追記し直し、成立しない
  場合は簡潔に記録して次回へ回す)。

## Part BR status update (2026-11-23, solver・takeover実行host): batch-27 (class 13342) drive-1完了 - 事前登録WIN-HALTがo002で発火 (honest WIN label・**29番目の unconsumed closure WIN候補**・verdict不消費)

(takeover amendment 通り・publish-then-execute履行: amendment `d2e345e6` 出版後に
scaffold pins再照合 → val-gate this-host 4 → drive → audit/tamper → 出版 A
`28cf8c2f` outputs → C `a55813ee` README+MANIFEST → 本status update。全出版bytesは
commit-pinned raw fetch-backでbyte検証済み。observed HEAD: a55813ee (本Part
commit Cそのもの・併走Part BW status update `f687fa73` と fast lane
`6360bb32` は非接触・note.mdのBW status update以降の本lane追記なしを確認)。
本節追記前の note blob lock は `f412fcc4` (Part BW status update `f687fa73` 版
508,970 bytes) であるが、push直前の再fetchで最新mainの現blob
`4fa0fdffd…` (514,881 bytes) を再照合する。)

- 実行 (宣言 `14ee1873` + takeover amendment `d2e345e6` の事前登録どおり):
  (1) scaffold pins 8種再照合 byte一致 (drive `9114e211` / jsreplay `84585617`
  / make_batch27_keys `9ab4523a` / row_audit `ed21debe` / row_audit_win_halt
  `7d920f2b` / runbatch `f591f8c2` / runwave `8efd78c2` / batch-keys
  `67814ed6`)・54 input CSVの (id, lo, hi, legal) とbatch-keys全行一致
  (bad 0)。(2) **val-gate 4/4 node-exact** (takeover host・`*.takeover-host.out`
  4ファイル: at2m 2M exhaustion ×2 (result 0・nodes 2,000,000)・15m基準キー
  (2, 3,651,923)/(2, 5,040,200)・禁止四角 95,670・wall_s 19/19/36/44。
  published this-host 4 (宣言host preflight) は不変のまま別名overlay出版)。
  (3) drive invocation 1回のみで **worker2 rc=45 事前登録WIN-HALT**。
- **o002 WIN (honest label)**: key (3494793310856282144, 0)・s5 209134・legal
  79・membership 4・nodes 4,589,084 (budget 15M内)・two-pass node-exact (wall
  45/47s) → worker2の最初のキーで発火 (batch-21 a003・batch-22 k002・
  batch-26 l028 に続く4回目の単独WIN子パターン・**29番目の unconsumed
  closure WIN候補**)。status.log は PASS (nodes付き) + WIN-HALT の2行
  (runbatchの定式どおり・事前登録win-halt監査はpair照合を正しく実装済みで
  Part BTのような派生は不要)。
- worker1はworker2のWIN-HALT後に自workerの260s有界区間を継続し (driver wait
  設計・runbatchは他workerの停止を観測しない・batch-26 worker2/l033と同型)、
  o001/o003/o005/o007 **LOSS (採用候補のみ・verdict不消費)** (nodes
  2,829,495 / 2,400,082 / 2,093,259 / 6,644,942・2-pass node-exact) 完了後
  o009実行中に timeout 124 で打ち切り。**fragment o009 (UNPROBED)**:
  o009.p1.out は `# replay_done` 付き完全単一パス (bookkeepingのみ: result 2・
  nodes 9,082,839・証拠ではない)・o009.p2.out はtruncated断片 (verdict行なし)。
  truncated-retry行 0件 (retry再実行は未実施・continuationでfresh-cold再実行)。
- 残り48キー (o004, o006, o008, o010..o054) は fileless UNPROBED。EXHAUSTED 0・
  determinism mismatch (rc=42) 不発。
- **row-audit-winhalt PASS** (schema
  `n11-centralreply-closure-class13342-batch27-rowaudit-winhalt-v1`・事前登録
  `7d920f2b`・derived_state): completed 5 (WIN 1・LOSS 4)・fragment 1
  (o009)・fileless 48・unprobed 49・3回実行byte一致 (json sha256 `530fe947…`・
  status.log sha256 `50a4f407…`)・**tamper battery 3/3検出** (T1 o001 verdict
  反転→WIN-HALT pair照合gate / T2 未probeキー o010への偽PASS行→verdict-ish
  gate / T3 o002 verdict 2行除去→pair照合gate・scratch上で実施し実験filesは
  battery前後でbyte同一) + clean control PASS。誠実記録: T2の初回実行は
  scratch再利用ミス (T1汚染残存) でT1のgateメッセージでの検出となったため、
  クリーンscratchで再実施し正しいgate (verdict-ish lines for non-completed
  keys ['o010']) での検出を確認した。
- 出版 (全fetch-back byte照合): outputs `28cf8c2f` (18ファイル: status.log・
  raw 12・row-audit-winhalt.json・val-gate takeover-host 4) → README +
  MANIFEST-sha256 92行 `a55813ee` (実験dir `n11-centralreply-closure-class13342-
  batch27-20261123/`・MANIFESTはmain状態92ファイルのsha256・published
  this-host 4は宣言host版のまま)。
- 意味 (route statementのみ・閉鎖/被覆/secured/root勝敗の主張なし): 単独WIN子
  o002 により (採用された場合) **class 13342 の全LOSS閉包ルートは反駁証拠を
  持つ**。ただし verdictは一切消費していない・採用判断は scrutiny owner C++
  第二実装 gate pin `9193f5b6…` 待ち (本レーンは代行しない)・canonical cache
  (Part BU採用後 6,287行 `e32a2e44…`) read-only不変・class 10968/23964 は
  PKT-collision blocked・class 5690 は route-dead のまま。
- 次回 (batch-28) の選定は **29-WIN交積** (28 + o002 (s5 209134)) の反駁簿記で
  maker内で機械選定する。当面のroute-alive候補: rank 27 class 5343
  (runner-up)・rank 28 class 13758 (backup)・rank 29 class 14103 (rank 30..
  30484以降は要packet交差確認)。**prefix未使用単文字ゼロ** ({i, l, o} を
  batch-25/26/27で使用済み) なので次回選定時は2文字prefix等の新設計を要する。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 10968・class 23964・class 13342 (54キーすべて・
  o002を含む) はどの時点でもUNKNOWNのまま。** nodes数・expansions数を勝敗・
  距離として読まない。WIN/LOSS採用は別宣言のadoption Part (pinned fail-closed
  merger `90711961` 経由) のみ。
- 本status update observed HEAD-before-push: `a55813ee…` (本Part commit C)。
  push直前に最新mainを再fetchし note blob lock `4fa0fdffd…` (514,881 bytes =
  Part BW status update `f687fa73` 版) を再照合する (y=22 universal実行等の
  並走追記が挟まった場合は本節を追記し直し、成立しない場合は簡潔に記録して
  次回へ回す)。

## Part BX (verifier, amendment 2026-11-23, 実行前に宣言): batch-25 i001/i002 WIN行の第三実装交叉検証 + 本host pinned-replica再現 (verdict不消費)

batch-25 (Part BP) で出版されたWIN行 i001/i002 (canonical宣言 `b54fbdd6`・
scaffold `2cc4a69a` (73 files)・outputs `3b1a6283`・README+MANIFEST-sha256
79行 `573099b4`・2-pass fresh-cold node-exact・replay result 1・nodes
13,251,132 / 7,207,180・budget 15M内・WIN-HALT rc=45 (両worker・それぞれの
workerの最初のキーでhalt)) に対し、前例 (Part G/K/O/P/T/W/AA/AD/AG/AL/AR/
AZ/BF/BK/BM/BS/BV/BW) と同じpinned第三実装 (non-df-pn AND/OR minimax) に
よるverdict-level交叉検証を、本セッションが単一オーナーとして実行する
(同一スコープの対抗宣言・amendmentが本amendmentより先にmainにある場合は
本宣言を破棄して着手しない・本宣言時点でnote grep clean・
`n11-centralreply-closure-b25win-thirdimpl-20261123` dirの不存在を確認
済み)。誠実な相違点の開示: batch-25 drive-1はPart BP執行hostの単一host
出版であり第二host同時再現は出版されていない。よって本Partの「本host
pinned-replica再現」はi001/i002にとって最初の独立host再現である (WIN-
HALT時点の残り51キー i003..i053 fileless UNPROBEDには一切触れない。
batch-25にはLOSS行が存在しない (row-audit loss_rows空・PASS 2行のみ) の
で、batch-24 y002/y004のようなadoption候选行情報も本Partの対象外)。

- 対象: `research/experiments/n11-centralreply-closure-b25win-thirdimpl-20261123/`。
  target 2行: **i001** (key (1152921505277935616, 1081344)・s5 68580・
  legal 88・membership 4・replica_result 1・replica_nodes 13,251,132・
  holder class 30565 (unknown)・batch-keys `272c0c13…`)・**i002** (key
  (3458764514357411840, 1081344)・s5 191299・legal 82・replica_result 1・
  replica_nodes 7,207,180・membership 4)。
- 機材 (全てpublished byte・実行時にsha照合): third_impl.js `08ea958f…`・
  verify_tbl.js `c8c52528…`・jsreplay.js replica `84585617…`・runner
  `run_thirdimpl.sh` (BF正本byte-copy `a0b77d83…`)・maker
  `make_inputs_bx.py` `e1def905…` (BW maker `f94d6e4f…`のbatch-25正本
  sourcesへのhonest adapt: 対象2行 i001/i002・b25 pin群 (batch-keys/
  status/README/row-audit/raw 4/published-input 2)・status.log 4行電池
  (PASS 2 + WIN-HALT 2・truncated-retry行ゼロ・**loss行ゼロのため BW版の
  loss-row gateは除去**し「各PASS行はtarget WIN行 (result 1・published
  nodes) でなければABORT」gate・PASS key集合 == row-audit win_rows (i001,
  i002) の機械交叉導出)・row-audit電池 (win_rows 2行・loss_rows空・
  pass_rows 0・probed 2・unprobed 51・fragment_keys {}・mismatches 0・
  derived_state true・stop_rule文言gate・input_sha256機械照合)・README
  文言gate (i001/i002 WIN honest label・13,251,132・7,207,180・26番目・
  27番目の unconsumed closure WIN候補・scrutiny owner文言・class 30565・
  Part BP識別)・rows.json schema s/b24/b25/)・audit gate battery
  `audit.py` `19351ab5…` (BW audit `3a2ce7ef…`のb25win版 adapt: EXP/
  SCHEMA/rows-schema・target-count文言のみ変更・gateロジック不変)。
- 前提ゲート (fail-closed・全て機械検査・宣言時点で実施済み): maker全
  gate PASS (BX-SCAFFOLD)・4回実行byte一致 (`__pycache__`衛生)・tamper
  battery **7/7検出** (T1 raw i001.p1 nodes内容改変 13251132→13251133・
  T2 row-audit内容改変 probed 2→3・T3 README文言改変 i001 WIN→LOSS・
  T4 status.log i002 PASS verdict反転 1→2・T5 published-input i001 legal
  88→87・T6 BF anchor CSV k02a lo +1・T7 batch-keys s5_index 191299→191300・
  **全tamperに適用実効性assert (改変前後sha照合) を実施**・scratch (/tmp)
  上で実施し実験sources無改変byte検証・T1/T2/T3/T4/T7はsha-pin層・T5/T6は
  derived-vs-published byte等価層で検出)・clean control PASS。なお本host
  val-gate 4件 (jsreplay) は宣言前のhost健全性確認として取得済み
  (published baselineとのnode-exact一致 4/4・wall比較外) であり、protocol
  step 2で改めて取得し直したものを出版する (宣言前取得分は上書きされ、
  それも実験事実として記録する)。
- sources sha pin: batch-keys-b25 `272c0c13…` (53キー・class 30565・schema
  `n11-centralreply-closure-class30565-batch25-input-v1`)・status-b25.log
  `0b12b101…` (4行 = PASS 2 + WIN-HALT 2・PASS key集合 == row-audit
  win_rows 機械交叉導出・truncated-retry行ゼロ)・README-b25 `67ec6ef9…`・
  row-audit-winhalt-b25 `cc84d1b3…` (probed 2・pass_rows 0・win_rows
  [i001,i002]・loss_rows []・fragment_keys {}・unprobed_count 51・
  derived_state true・stop_rule事前登録文言・input_sha256 == batch-keys
  pin)・raw i001 p1/p2 `4e9e2de2…`/`bc6417d2…`・raw i002 p1/p2
  `da09e97a…`/`2730ee6d…` (2-pass node-exact + result 1 in-budget +
  status/row-audit/README 3-way照合)・published input CSV byte-equality
  `cba4b6cb…`/`1af3487a…`・BF anchor/negative CSV byte-equality
  (provenance chain AR→BF→BK→BM→BS→BV→BW→BX・k02a `b6174a3f…`・l1a
  `e13d2a6c…`・ng1 `8e64b9ad…`・ng2 `f19cd5a3…`)。
- val-gate (本host jsreplay健全性): batch-27 scaffold val-gate input 4 +
  published-baseline 4をbyte-copy (b23/BV系譜のpublished baselineと同一
  bytes・batch-27 val-gate正本からfetch-back照合済み) し・本host再生成4件
  (at2m budget 2M exhaustion ×2・15m基準キー budget 15M・published baseline
  (2, 3,651,923)/(2, 5,040,200)・禁止四角 95,670) がpublished baselineと
  node-exact一致 (wall_s比較外) することを本Part実行の protocol step 2と
  して取得する。本host .out 4件を出版する。
- 実行protocol (宣言時点で事前登録・順序も含め固定・逐次実行):
  1. rules gate: pinned `verify_tbl.js`でreplica quads 95,670 ==
     third-impl quads 95,670・triples checked mismatch 0。
  2. val-gate this-host 4件 (宣言前取得分の上書き再取得)。
  3. 本host pinned-replica再現: pinned replica (jsreplay `84585617…`) で
     i001・i002を各々budget 15M・fresh-cold・逐次2回 (p1/p2) 実行し、
     決定性 fields p1==p2・published raw fields (result 1・nodes
     13,251,132 / 7,207,180) との一致をauditで機械検査する。
     exhaustion/mismatch/truncationはhonest記録のみとし検証主張としない。
  4. negatives ng1 (legal+1)/ng2 (stones 6) のGATE_FAIL確認 (fail-closed
     設計どおり) → anchors k02a (WIN 9,106,337 exp / 4,991,527 ttHits)・
     l1a (LOSS 7,660,602 / 3,951,175) の本host node-exact再現 (a/b 2回)。
  5. targets i001/i002は1行=1solver=1プロセス・cap 300,000,000・wallcap
     240s・`--memo-power=22`・a/b 2回のdeterminism gate
     (result/expansions/ttHits/reason同一必須)・逐次実行。wall超過は
     honest wall-inconclusiveとし検証主張としない。事前の機械予想は
     宣言時に残さない (実測を待つ)。
  6. 監査: `audit.py` (G0/G1/G2/G2b/G3/G4/G5・BW版と同一gate構成・schema
     `n11-centralreply-closure-b25win-thirdimpl-audit-v1`) 3回実行byte
     一致・audit tamper battery 3種 (T1 maker pin反転→ABORT・T2 auditの
     target det-pair改ざん→DIVERGENCE検出・T3 G0のinput改ざん→gate
     fail・scratch上で実施・実験files無改変byte検証)・clean control PASS。
  7. 出版: A scaffold (scripts + input + sources + val-gate) → B outputs
     (rules-gate・val-gate this-host・replica p1/p2・negative・anchors a/b・
     targets a/b・audit 3回分・audit-summary・status.log) → C README +
     MANIFEST-sha256 → 本noteへのstatus update。全出版bytesはcommit-pinned
     raw fetch-backでbyte検証する。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・**verdict不消費**
  (i001/i002の採用判断は引き続きscrutiny owner C++第二実装 gate pin
  `9193f5b6…` のまま)。第三実装verdictがcleanにreplica verdictと一致
  した場合は「一致した」事実のみ記録し、clean不一致はdivergence
  evidenceとして記録するが本レーンではverdictを書き換えない。閉鎖・
  被覆・secured・root勝敗の主張をしない。
- 不接触: canonical cache (Part BU採用後 6,287行 `e32a2e44…`) への書き
  込みなし・29 unconsumed closure WIN候補の採用状態不変・batch-23/24/25
  残留キー (s003..s053・y003/y005/y007..y053・i003..i053 fileless
  UNPROBED) に一切触れない・batch-24の y002/y004 LOSS行 (adoption
  candidate)・batch-27の o001/o003/o005/o007 LOSS 4行 (adoption
  candidates) には本Partは出版正本の読み取りのみで一切書き込まない・
  batch-26/27 (Part BQ/BT/BR) のscaffold・drive・outputsには一切書き込ま
  ない・fast lane (y18..y22族・y=22 universal宣言 `e1e60cd4`・K1256/
  K1257・y=23宣言 `6f79c81f`)・finite-field lane・inversive-arc lane
  非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・
  class 16957・class 1849・class 13342・class 30565 (53キーすべて・
  i001/i002を含む) は本Partのどの時点でもUNKNOWNのまま。nodes数・
  expansions数・ttHits数を勝敗として読まない。WIN/LOSS採用は別宣言の
  adoption Part (pinned fail-closed merger `90711961` 経由) のみ。
  scrutiny owner C++第二実装 gate `9193f5b6…` 待ちは本レーンは代行
  しない。
- 本宣言 observed HEAD-before-push: `bf45c550…` (並走fast laneのK1256/
  K1257関連コミット・本Partと無関係・note grep clean・b25win dir不存在
  を確認済みで再取得した最新main HEAD)。push直前に最新mainを再fetchし
  note blob lock `74c6b4bc63c6060316bfc0b7632298f03ced35b5`
  (521,065 bytes = Part BR status update `bea59ed4` 版 + 並走fast lane
  無関係コミット時点) を再照合する (y=23宣言等の並走追記が挟まった
  場合は本節を追記し直し、成立しない場合は簡潔に記録して次回へ回す)。

### Part BX status update (2026-11-23, verifier): batch-25 i001/i002 第三実装交叉検証完了 - 本host pinned-replica初の独立host再現 + clean WIN一致2/2 (UNKNOWN担保不変)

(observed HEAD-before-push: `ef2ce618…` (本Part commit C)・並走非接触
コミット `7b64775a` (K1254・finite-field lane) を確認のうえ線形続行。
fetch-back済み出版状況に基づく追記)

- 宣言 `8b3aa95d` (publish-then-execute・protocol順どおり) の実行完了。
  **実行時に競合・対抗宣言は存在しなかった** (note grep clean・
  b25win dir不存在を宣言時に確認済み)。
- rules gate PASS: replica quads 95,670 == third-impl quads 95,670・
  triples checked 195,044・mismatches 0。
- val-gate this-host 4/4 node-exact (pinned `jsreplay.js`・published
  baseline (0, 2,000,000)×2・(2, 3,651,923)・(2, 5,040,200)・wall_s
  比較外・宣言前host健全性取得分の上書き再取得)。
- **本host pinned-replica再現 4/4 node-exact**: i001 p1/p2 = result
  1・nodes **13,251,132** (two-pass node-exact・wall 65/69s・published
  150/68s)・i002 p1/p2 = result 1・nodes **7,207,180** (two-pass
  node-exact・wall 36/36s・published 77/75s)。batch-25 (Part BP) が
  単一host出版だったため、**i001/i002 にとって最初の独立host再現**
  (audit G2b機械検査・EXHAUSTED 0・mismatch 0・truncation 0)。
- negatives 2/2 GATE_FAIL設計どおり (ng1 legal mismatch・ng2 stone
  mismatch)・anchors k02a/l1a本host node-exact (a/b determinism PASS・
  k02a WIN 9,106,337/4,991,527・l1a LOSS 7,660,602/3,951,175・published
  第三実装定数と完全一致)。
- **targets 2/2 clean WIN一致 (verdict agreement 2/2・DIVERGENCE 0・
  WALL-INCONCLUSIVE 0)**: **i001 clean WIN (result 1)** expansions
  15,723,649・ttHits 8,504,237 (a/b一致・wall 44.56/44.18s)・
  **i002 clean WIN (result 1)** expansions 8,292,120・ttHits 4,721,313
  (a/b一致・wall 23.96/24.25s)。cap 300M・wallcap 240s・memo-power=22。
  pass-one third-impl拡張数合計 24,015,769 (replica合計 20,458,312 との
  比率 1.187 / 1.151)。
- 監査 (`audit.py` `19351ab5…`): **ALL 67 GATES PASS**・3回実行byte
  一致 (audit-summary sha `7eb82c0d…`)・audit tamper battery 3/3検出
  (T1 maker pin反転→ABORT rc=1・T2 target det-pair改ざん→gate fail
  rc=1・T3 G0 input改ざん→gate fail rc=1・scratch上・実験files無改変
  byte検証)・clean control PASS。前提側 maker tamper battery 7/7検出
  (全tamperに適用実効性assert)・4回byte一致も宣言時に記録済み。
- 出版3コミット (fetch-back byte照合済み): scaffold `f1adc061`
  (35/35一致)・outputs `3e078e2a` (27/27一致)・README + MANIFEST-sha256
  63行 `ef2ce618` (README blob `54bccfce…`・MANIFEST blob
  `007572d9…`・実験dir `n11-centralreply-closure-b25win-thirdimpl-
  20261123/`・マニフェスト対象63ファイル)。
- 意味 (verdict-level文献のみ・verdict不消費): 第三実装 (non-df-pn
  AND/OR minimax) のclean WINがpublished replica WIN (honest label)
  と2/2一致した事実のみを記録する。i001/i002 (26番目・27番目の
  unconsumed closure WIN候補) の採用判断は引き続き scrutiny owner
  C++第二実装 gate pin `9193f5b6…` 待ち (本レーンは代行しない)・
  canonical cache (Part BU採用後 6,287行 `e32a2e44…`) read-only
  不変・採用は別宣言のadoption Part (pinned fail-closed merger
  `90711961` 経由) のみ。閉鎖・被覆・secured・root勝敗の主張は
  しない。
- 次回以降のverifier候補: batch-27 (Part BR) のo002 WIN行 (29番目
  候補・実験dir正本pinのfetch-back再取得から) が次点。adoption
  候補 (batch-24 y002/y004・batch-27 o001/o003/o005/o007 LOSS 6行) は
  別Part (BU前例・merger `90711961`) として将来回で宣言のみで着手。
  batch-28選定 (29-WIN交積・2文字prefix新設計) も次回レーン。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 16957・
  class 1849・class 13342・class 30565 (53キーすべて・i001/i002を
  含む) はどの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数
  を勝敗として読まない。
- 本status update observed HEAD-before-push: `ef2ce618…`。push直前に
  最新mainを再fetchし note blob lock `35c37e463066e845cdbee858aba01e0c
  8a59a7fe` (531,427 bytes = 本Part BX宣言 `8b3aa95d` 版) を再照合する
  (並走追記が挟まった場合は本節を追記し直し、成立しない場合は簡潔に
  記録して次回へ回す)。

## Part BY (verifier, amendment 2026-11-23, 実行前に宣言): batch-27 o002 WIN行の第三実装交叉検証 + 本host pinned-replica再現 (verdict不消費)

batch-27 (Part BR・takeover実行) で出版されたWIN行 o002 (canonical宣言
`14ee1873`・scaffold `93ef3f89`・takeover amendment `d2e345e6`・raws+status+
row-audit `28cf8c2f`・README+MANIFEST 92行 `a55813ee`・2-pass fresh-cold
node-exact・replay result 1・nodes 4,589,084・budget 15M内・WIN-HALT rc=45
(worker2の最初のキー・**29番目の unconsumed closure WIN候補**)) に対し、
前例 (Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AZ/BF/BK/BM/BS/BV/BW/BX) と同じ
pinned第三実装 (non-df-pn AND/OR minimax) によるverdict-level交叉検証を、
本セッションが単一オーナーとして実行する (同一スコープの対抗宣言・
amendmentが本amendmentより先にmainにある場合は本宣言を破棄して着手し
ない・本宣言時点でnote grep clean (Part BY文字は未使用)・
`n11-centralreply-closure-b27win-thirdimpl-20261123` dirの不存在を確認
済み)。誠実な相違点の開示: batch-27 drive-1はPart BR takeover実行host
の単一host出版であり第二host同時再現は出版されていない。よって本Part
の「本host pinned-replica再現」はo002にとって最初の独立host再現で
ある (残留キー・fragment o009 (UNPROBED・p1完全単一パスはbookkeeping
のみで証拠ではない) には一切触れない。同batchの o001/o003/o005/o007
の4 LOSS行はadoption候选のみで・本Partは出版正本の読み取りのみ)。

- 対象: `research/experiments/n11-centralreply-closure-b27win-thirdimpl-20261123/`。
  target 1行: **o002** (key (3494793310856282144, 0)・s5 209134・legal
  79・membership 4・replica_result 1・replica_nodes 4,589,084・holder
  class 13342 (unknown)・batch-keys `67814ed6…`)。
- 機材 (全てpublished byte・実行時にsha照合): third_impl.js `08ea958f…`・
  verify_tbl.js `c8c52528…`・jsreplay.js replica `84585617…`・runner
  `run_thirdimpl.sh` (BF正本byte-copy `a0b77d83…`)・maker
  `make_inputs_by.py` `359abebc…` (BX maker `e1def905…`のbatch-27正本
  sourcesへのhonest adapt: 対象1行 o002・b27 pin群 (batch-keys/status/
  README/row-audit/raw 2/published-input 1)・status.log 6行電池 (PASS 5 =
  LOSS 4行 (o001/o003/o005/o007・result 2・published nodes) + WIN 1行
  (o002・result 1・published nodes)・WIN-HALT 1・retry行ゼロ・**loss-row
  gate復元 (BX版の除去から戻し: 各PASS行はtarget WIN行またはrow-audit
  loss_rows のいずれかでなければABORT)**・PASS key集合 == row-audit
  win_rows ∪ loss_rows の機械交叉導出・**fragment gate新設**: fragment
  o009 はstatus行に一切出現してはならず・row-audit fragment_keys は
  {o009} (p1完全単一パス true・p2完全単一パス false・evidence false・
  probed false) 厳密照合)・row-audit電池 (win_rows [o002]・loss_rows
  4行・pass_rows 4・probed 5・unprobed_count 49・fileless 48・mismatches
  0・derived_state true・stop_rule文言gate・input_sha256機械照合)・
  README文言gate (o002 WIN honest label・4,589,084・29番目の
  unconsumed closure WIN候補・4 LOSS行のnode数文言・fragment o009
  UNPROBED文言・scrutiny owner文言・class 13342・Part BR識別)・rows.json
  schema s/b25/b27/)・audit gate battery `audit.py` `7f7fa3d1…` (BX audit
  `19351ab5…`のb27win版 adapt: EXP/SCHEMA/rows-schema・target-count文言
  (1 b27 WIN row) のみ変更・gateロジック不変)。
- 前提ゲート (fail-closed・全て機械検査・宣言時点で実施済み): maker全
  gate PASS (BY-SCAFFOLD)・4回実行byte一致 (`__pycache__`衛生)・input/
  o002.input.csv derived-vs-published byte-equality (published pin
  `d083f5c3…`)・tamper battery **7/7検出** (T1 raw o002.p1 nodes内容
  改変 4589084→4589085・T2 row-audit内容改変 probed 5→6・T3 README文言
  改変 o002 WIN→LOSS・T4 status.log o001 LOSS行 verdict反転 2→1・T5
  published-input o002 legal 79→78・T6 BF anchor CSV k02a lo +1・T7
  batch-keys s5_index 209134→209135・**全tamperに適用実効性assert**
  (改変前後sha照合)・scratch (/tmp) 上で実施し実験sources無改変byte
  検証・T1/T2/T3/T4/T7はsha-pin層・T5/T6はderived-vs-published byte
  等価層で検出)・clean control PASS。なお本host val-gate 4件 (jsreplay)
  は宣言前のhost健全性確認として取得済み (published baselineとの
  node-exact一致 4/4・wall比較外) であり、protocol step 2で改めて取得
  し直したものを出版する。
- sources sha pin: batch-keys-b27 `67814ed6…` (54キー・class 13342・
  schema `n11-centralreply-closure-class13342-batch27-input-v1`・published
  MANIFEST-sha256 92行 (commit `a55813ee` 時点) と全行一致照合)・
  status-b27.log `50a4f407…` (6行)・README-b27 `1ee2666e…`・row-audit-
  winhalt-b27 `530fe947…`・raw o002 p1/p2 `56fdf7a4…`/`cf1ce8ff…`
  (2-pass node-exact + result 1 in-budget + status/row-audit/README
  3-way照合)・published input CSV byte-equality `d083f5c3…`・BF
  anchor/negative CSV byte-equality (provenance chain AR→BF→BK→BM→BS→
  BV→BW→BX→BY・k02a `b6174a3f…`・l1a `e13d2a6c…`・ng1 `8e64b9ad…`・
  ng2 `f19cd5a3…`)。
- val-gate (本host jsreplay健全性): batch-27 scaffold val-gate input 4 +
  published-baseline 4をbyte-copy (b23/BV系譜のpublished baselineと同一
  bytes・batch-27 val-gate正本からfetch-back照合済み) し・本host再生成
  4件 (at2m budget 2M exhaustion ×2・15m基準キー budget 15M・published
  baseline (2, 3,651,923)/(2, 5,040,200)・禁止四角 95,670) がpublished
  baselineとnode-exact一致 (wall_s比較外) することを本Part実行の
  protocol step 2として取得する。本host .out 4件を出版する。
- 実行protocol (宣言時点で事前登録・順序も含め固定・逐次実行):
  1. rules gate: pinned `verify_tbl.js`でreplica quads 95,670 ==
     third-impl quads 95,670・triples checked mismatch 0。
  2. val-gate this-host 4件 (宣言前取得分の上書き再取得)。
  3. 本host pinned-replica再現: pinned replica (jsreplay `84585617…`) で
     o002をbudget 15M・fresh-cold・逐次2回 (p1/p2) 実行し、決定性
     fields p1==p2・published raw fields (result 1・nodes 4,589,084) との
     一致をauditで機械検査する。exhaustion/mismatch/truncationはhonest
     記録のみとし検証主張としない。
  4. negatives ng1 (legal+1)/ng2 (stones 6) のGATE_FAIL確認 (fail-closed
     設計どおり) → anchors k02a (WIN 9,106,337 exp / 4,991,527 ttHits)・
     l1a (LOSS 7,660,602 / 3,951,175)の本host node-exact再現 (a/b 2回)。
  5. target o002は1行=1solver=1プロセス・cap 300,000,000・wallcap 240s・
     `--memo-power=22`・a/b 2回のdeterminism gate (result/expansions/
     ttHits/reason同一必須)・逐次実行。wall超過はhonest
     wall-inconclusiveとし検証主張としない。事前の機械予想は宣言時に
     残さない (実測を待つ)。
  6. 監査: `audit.py` (G0/G1/G2/G2b/G3/G4/G5・BX版と同一gate構成・schema
     `n11-centralreply-closure-b27win-thirdimpl-audit-v1`) 3回実行byte
     一致・audit tamper battery 3種 (T1 maker pin反転→ABORT・T2 auditの
     target det-pair改ざん→DIVERGENCE検出・T3 G0のinput改ざん→gate
     fail・scratch上で実施・実験files無改変byte検証)・clean control
     PASS。
  7. 出版: A scaffold (scripts + input + sources + val-gate) → B outputs
     (rules-gate・val-gate this-host・replica p1/p2・negative・anchors
     a/b・target a/b・audit 3回分・audit-summary・status.log) → C README
     + MANIFEST-sha256 → 本noteへのstatus update。全出版bytesは
     commit-pinned raw fetch-backでbyte検証する。
- 主張と消費規則: 本検証はverdict-level文献作成のみ・**verdict不消費**
  (o002の採用判断は引き続きscrutiny owner C++第二実装 gate pin
  `9193f5b6…` のまま)。第三実装verdictがcleanにreplica verdictと一致
  した場合は「一致した」事実のみ記録し、clean不一致はdivergence
  evidenceとして記録するが本レーンではverdictを書き換えない。閉鎖・
  被覆・secured・root勝敗の主張をしない。
- 不接触: canonical cache (Part BU採用後 6,287行 `e32a2e44…`) への書き
  込みなし・29 unconsumed closure WIN候補の採用状態不変・batch-23/24/25
  残留キー (s003..s053・y003/y005/y007..y053・i003..i053 fileless
  UNPROBED)・batch-27残留キー (o004/o006/o008/o010..o054 fileless
  UNPROBED)・**fragment o009 (p1完全単一パスはbookkeepingのみ・証拠で
  ない)** に一切触れない・batch-24の y002/y004・batch-27の
  o001/o003/o005/o007 LOSS 6行 (adoption candidates) には本Partは出版
  正本の読み取りのみで一切書き込まない・batch-26/27 (Part BQ/BT/BR) の
  scaffold・drive・outputsには一切書き込まない・fast lane (y=22 universal
  宣言 `e1e60cd4`・K1256/K1257・y=23宣言 `6f79c81f`)・finite-field lane
  (K1254)・inversive-arc lane非接触。
- UNKNOWN担保: 標準11×11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・
  class 16957・class 1849・class 30565・class 13342 (54キーすべて・
  o002を含む) は本Partのどの時点でもUNKNOWNのまま。nodes数・expansions
  数・ttHits数を勝敗として読まない。WIN/LOSS採用は別宣言の adoption
  Part (pinned fail-closed merger `90711961` 経由) のみ。scrutiny owner
  C++第二実装 gate `9193f5b6…` 待ちは本レーンは代行しない。
- 本宣言 observed HEAD-before-push: `91b490c0…` (本レーン Part BX
  status更新・並走非接触コミットなしをlist_commitsで確認済み)。push
  直前に最新mainを再fetchし note blob lock
  `cb2c80d1aea1250be0cda9b8105f12b682812ec1` (536,124 bytes = Part BX
  status update `91b490c0` 版) を再照合する (並走追記が挟まった場合は
  本節を追記し直し、成立しない場合は簡潔に記録して次回へ回す)。

### Part BY status update (2026-11-23, verifier): batch-27 o002 第三実装交叉検証完了 - 本host pinned-replica初の独立host再現 + clean WIN一致1/1 (UNKNOWN担保不変)

(observed HEAD-before-push: `6bbacd91…` (本Part commit C)・並走非接触
コミット `df2b1cd6` (K1254・finite-field lane) を確認のうえ線形続行。
fetch-back済み出版状況に基づく追記)

- 宣言 `7a3a3f27` (publish-then-execute・protocol順どおり) の実行完了。
  **実行時に競合・対抗宣言は存在しなかった** (note grep clean・
  b27win dir不存在を宣言時に確認済み)。
- rules gate PASS: replica quads 95,670 == third-impl quads 95,670・
  triples checked 195,044・mismatches 0 (禁止四角 95,670)。
- val-gate this-host 4/4 node-exact (pinned `jsreplay.js`・published
  baseline (0, 2,000,000)×2・(2, 3,651,923)・(2, 5,040,200)・wall_s
  比較外・宣言前host健全性取得分の上書き再取得・walls 9/9/17/25s)。
- **本host pinned-replica再現 2/2 node-exact**: o002 p1/p2 = result
  1・nodes **4,589,084** (two-pass node-exact・wall 22/22s・published
  45/47s)。batch-27 (Part BR) はtakeover実行hostの単一host出版だった
  ため、**o002 にとって最初の独立host再現** (audit G2b機械検査・
  EXHAUSTED 0・mismatch 0・truncation 0)。
- negatives 2/2 GATE_FAIL設計どおり (ng1: legal count mismatch
  derived=87 declared=88・ng2: stone count mismatch bits=5 declared=6)・
  anchors k02a/l1a本host node-exact (a/b determinism PASS・k02a clean
  WIN 9,106,337/4,991,527・wall 26.39/26.22s・l1a clean LOSS
  7,660,602/3,951,175・wall 22.14/21.75s・published第三実装定数と
  完全一致)。
- **target 1/1 clean WIN一致 (verdict agreement 1/1・DIVERGENCE 0・
  WALL-INCONCLUSIVE 0)**: **o002 clean WIN (result 1)** expansions
  5,303,699・ttHits 2,988,749 (a/b一致・wall 15.13/15.15s)。cap
  300,000,000・wallcap 240s・memo-power=22。pass-one third-impl
  拡張数 5,303,699 (replica 4,589,084 との比率 1.156)。
- 監査 (`audit.py` `7f7fa3d1…`): **ALL 50 GATES PASS**・3回実行byte
  一致 (audit-summary-run json sha `2d05ccff…`)・audit tamper
  battery 3/3検出 (AT1 maker pin反転→ABORT rc=1・AT2 o002.b
  expansions +1→target-o002-det-pair gate fail rc=1・AT3 o002 CSV
  legal 79→80→input-o002-matches-rows gate fail rc=1・scratch (/tmp)
  上で実施・実験files無改変byte検証)・clean control PASS。前提側
  maker tamper battery 7/7検出 (全tamperに適用実効性assert)・4回
  byte一致も宣言時に記録済み (maker `359abebc…`・rows.json
  `cfd8bd06…`)。
- 実行事故のhonest記録: l1a anchor a-pass実行中に実行環境の同期
  エラーが発生し、空の `l1a.a.out` とstatus.logのRUN行欠落という
  不整合が生じた。当該部分成果物は破棄し、l1a a/bをクリーンに
  再実行してstatus.log整合を回復した (published出版bytesはすべて
  再実行後のもので、上記anchors実測値も再実行後)。
- 出版4コミット (fetch-back byte照合済み): 宣言 `7a3a3f27` (note
  blob `106a8abe…` fetch-back一致)・scaffold `5ed729d1` (31/31
  一致)・outputs `821b8a9e` (23/23一致)・README + MANIFEST-sha256
  55行 `6bbacd91` (README blob `32695f7a…`・MANIFEST blob
  `b37b97c7…`・実験dir `n11-centralreply-closure-b27win-thirdimpl-
  20261123/`・マニフェスト対象55ファイル = scaffold 31 + outputs
  23 + README)。
- 意味 (verdict-level文献のみ・verdict不消費): 第三実装 (non-df-pn
  AND/OR minimax) のclean verdictがpublished replica verdict
  (result 1 = WIN行) と1/1で一致した事実のみを記録する。o002
  (29番目の unconsumed closure WIN候補) の採用判断は引き続き
  scrutiny owner C++第二実装 gate pin `9193f5b6…` 待ち (本レーンは
  代行しない)・canonical cache (Part BU採用後 6,287行
  `e32a2e44…`) read-only不変・採用は別宣言のadoption Part
  (pinned fail-closed merger `90711961` 経由) のみ。閉鎖・被覆・
  secured・root勝敗の主張はしない。batch-27残留キー (o004/o006/
  o008/o010..o054 fileless UNPROBED)・fragment o009 (p1完全単一
  パスはbookkeepingのみで証拠ではない)・同batch4 LOSS行
  (o001/o003/o005/o007・adoption candidates) には本Partは一切
  触れていない。
- 次回以降の候補: batch-28選定 (29-WIN交積・2文字prefix新設計・
  rank 27 class 5343/13758/14103) が次点。adoption候補6行
  (batch-24 y002/y004・batch-27 o001/o003/o005/o007 LOSS) は別Part
  (BU前例・merger `90711961`) として将来回で宣言のみで着手。
  scrutiny owner C++ gate `9193f5b6…` 待ちは本レーンは代行しない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 10968・class 23964・class 16957・
  class 1849・class 30565・class 13342 (54キーすべて・o002を含む) は
  どの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数を
  勝敗として読まない。
- 本status update observed HEAD-before-push: `6bbacd91…`。push直前に
  最新mainを再fetchし note blob lock `106a8abee991f707708716baea702580
  825f98c5` (546,467 bytes = 本Part BY宣言 `7a3a3f27` 版) を再照合する
  (並走追記が挟まった場合は本節を追記し直し、成立しない場合は簡潔に
  記録して次回へ回す)。


### Part BZ宣言 (adoption, publish-then-execute, amendment 2026-11-23): batch-24 y002/y004 + batch-27 o001/o003/o005/o007 の6-LOSS canonical adoption

(observed HEAD-before-push: `ecd7387e…`。並走コミットはK1254/ status
page docs `12f6b2bd`・`009bb1f3` の非接触2件を確認済み。対抗宣言なし・
本noteに同一スコープのsectionなしをgrep確認済み。push直前にnote blob lock
`c0dcfe03471875bece2a946dc40fbd0b8e3db783` (551,976 bytes = Part BY status
update版) を再照合し、並走追記が挟まった場合は本節を追記し直す。)

単一オーナーとして着手する。スコープ: batch-24 (class 16957) のy002/y004と
batch-27 (class 13342) のo001/o003/o005/o007、計6行の2-pass node-exact
result 2 (LOSS) を、pinned fail-closed union merger (byte-copy
`907119610034…`) でPart BU正本cache (6,287行 `e32a2e44…`) に併合する
adoption Part (BU前例・preflightとしてBU refresh出力の本host byte再現を
含む)。**verdict不消費は不変**: 非採用WIN 3行 (y001/y006/o002) はhonest
labelのままunconsumed (scrutiny owner C++ gate `9193f5b6…` 待ち・本レーン
は代行しない)。fragment o009とfilelessキー (batch-24 49件・batch-27
48件・いずれもUNPROBED) は不接触。

実験dir:
`research/experiments/n11-centralreply-class16957-13342-loss6-adoption-reaudit-20261123/`。
本節の数値・shaはすべて事前取得の機械算出 (dry-run由来・この場合の「1回の
実行で」要素もdry-run; 宣言後にprotocol 1)-11)を逐次再実行し、下記shaと
byte一致しない場合は即時abort・honest記録とする)。

- 入力pins (全sha照合済み): BASE cache `e32a2e44…` (6,287行)・BASE refresh
  3出力 (Part BU reaudit: refresh-summary
  `51d6bf0dd6a7d73cc2824a692cf6b086849e5f7945509b9e72c6177ce7599101`・
  closure-classes `e54a0eb8…`・per-root-coverage `c1cb1bf5…`)・batch-24
  kit MANIFEST `8a8e30a8…` (83ファイル全sha照合)・batch-27 kit MANIFEST
  `eb4da2f7…` (92ファイル全sha照合)・merger byte-copy source
  `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`・
  dependency-graph.json.gz `54f9c364…`・repaired-joint-plan-update8.json・
  independent.py `954d3a10…`・s5_evidence_policy.py `78655e94…`・
  quarantine `81d23160…`。
- dry-run成果物 (sha固定済み・事前宣言数値):
  - maker `make_increments_b24b27.py`
    `eff939cdf98b928be78adf07b2fc95f7b4e814de6b0aaf95ac7ea132ab64c297c`:
    x4 byte-stable。increment (6行)
    `1d8556c128e09fa8d41a22d749af5a28dd4babf30c33d6317cb29af5cdd22074`
    (batch-24 y002/y004 nodes/pass 850,035・batch-27 o001/o003/o005/o007
    nodes/pass 13,967,778・計14,817,813/pass)。increments-manifest.json
    `818fb0c3e5e3bd8459bb4943218ab33c316ad45d8301d53badc235f584dcc00a`
    (row_counts: probed 9・adopted 6・WIN 3・fragment 1・fileless 97)。
  - merger `s5_union_merge.py` (byte-copy・selftest PASS・merge x3
    byte一致): merge-audit (全3run同一bytes)
    `cef05e36ed4d6c2ee48536744aff7645d48a7f85f4ac50596606c6d3e90e444c1`。
    scenario cache 6,293行 (WIN 158 / LOSS 6,135・259,527 bytes)
    `9115be9eca1e60828a90c50041f511b598ef79fc0be76d5e16821816e478e93e`。
  - refresh `reaudit/scripts/refresh_adoption_b24b27.py`
    `0677e6eb5321bb61ab5757687f4e192acc12447f4c8b642aa455f985a9ae57c3`:
    x3 byte一致 + 隔離実行 (env -i・PYTHONHASHSEED=random・cwd=/tmp)
    byte一致。refresh-summary
    `fca242cc767f4e30b1d450a3b10cbd524b18b96f28b4cc4ba83c8762f8bb2ff2`・
    closure-classes
    `14fc37c3a6f5c6753cac72a094d2c7693defb4a5e483558b3b87a42016b679d9`
    (class 16957 unknown_now 53→51・rank 22→10, class 13342 54→50・
    rank 26→6)・per-root-coverage
    `4218a6b49f8dd4df41f9bb3b746c7f2a32afeb3e22d175243e9319c8f46ca56a`・
    probe-worklist `7d9020d4…` (非出版・実行ごとに再生成)。
  - extractor `compare_deltas_b24b27_adoption.py`
    `a3adc0dafaa9ceafc159f0aa364859f4f80ff998abcc0f5daf5674a429f55a2a`:
    x4 + 隔離実行byte一致。decomp-deltas-b24b27-adoption.json (16,398B)
    `e0005d42a20998ba86d7a9f895e7e93bde01d1b0cf23bb56de0346dd6bd64d8d`:
    flips=[]・new_free=[]・free_now 38→38・update8 resolved +0 (133不変)・
    joint greedy 38,301→38,295・probe-worklist 64,754→64,747・closure churn
    left=[] entered=[]・individual greedy movers 4 roots ({5,16,24,48})・
    per-root free/uncovered不変。
- preflight (宣言前実施済み): 本hostでpublished Part BU refresh 3出力
  (refresh-summary・closure-classes・per-root-coverage・probe-worklist
  `9ae1ca50` 含む) をbyte再現。
- 準備段階のtamper battery (scratch tree /tmp/tb/kr = 別絶対pathで実施・
  **16/16検出 + 全probe復元byte検証**): T1-T5 (batch-24 raw y002.p2
  nodes 217944→217945・batch-27 status.log o002 WIN flip・batch-24
  batch-keys class id・batch-27 row-audit o007改変・BASE cache append →
  いずれも各sha-pin層でABORT)・T6 (maker定数のadopted setにWIN y001追加 →
  published row-audit loss_rows semantic gateでABORT)・T7 (maker定数の
  fragmentsからo009除去 → fileless/unprobed bookkeeping gateでABORT)・
  **T2d (3-level pin bypass: status.log o002 result 2に改変 + kit
  MANIFEST当該行再構築 + maker pin定数2件更新 → sha-pin層通過後にsemantic
  「WIN set [] != unadopted ['o002']」でABORT)**・T8 (merger同一キー
  verdict conflict (y002 2 vs 1) → GATE FAILED・出力未生成)・R1 (scenario
  cache y002 verdict反転 → refresh merged-cache pinでABORT)・R2
  (quarantine append → refresh quarantine pinでABORT)・E1/E2 (scenario
  closure-classes class 16957 unknown_now 51→50 / per-root-coverage
  baseline改変 → extractor sha-pinでABORT)・E3 (increments-manifest
  loss_idsからy004除去 → extractor semantic gate「manifest loss_ids !=
  the 6 adopted ids」でABORT)・CONTROL (scratch tree上でmaker→merger→
  refresh→extractorのfull chain再実行 → 出版sha全件byte一致)。
- 実行protocol (宣言時点で固定・逐次実行): 1) 本host preflight再確認 (BU
  refresh出力byte再現) 2) maker x4 3) merger selftest + merge x3
  4) refresh x3 + 隔離x1 5) extractor x4 + 隔離x1 (各stepでbyte一致検査) 
  6) tamper battery再実行 (16 probe・全検出+復元byte検証) 7) 出版A
  (scripts 4 = `scripts/` 3 + `reaudit/scripts/` 1) 8) 出版B (increment +
  increments-manifest + merge-audit x3) 9) 出版C (merged scenario cache) 
  10) 出版D (reaudit 3出力 + decomp-deltas json) 11) 出版E (README +
  MANIFEST-sha256) + 本noteへstatus update追記。全出版bytesはcommit-pinned
  raw URL fetch-backでbyte検証する (branch path CDN staleに注意)。
- 不接触: canonical BASE (Part BU `e32a2e44…`) read-only・非採用WIN
  y001/y006/o002 unconsumed・fragment o009 (p1完全単一パスはbookkeeping
  のみ・証拠ではない)・batch-24/27 filelessキー (49+48件ともUNPROBED)・
  batch-23/24/25/26/27の他scaffold/outputs・batch-28選定・fast lane
  (y=22/23宣言)・finite-field lane (K1254)・thirdimpl bank・29
  unconsumed closure WIN候補・inversive-arc lane。
- 消費規則: 本Partが消費するのは6 LOSS行のみ (merger WIN/LOSS conflict
  gate経由・BASEとのキー重複ゼロをmaker structural gateで担保済み)。本Part
  単体ではroot被覆・クラス閉鎖・secured・root勝敗の主張をしない (closure
  churn left=[]/entered=[] はクラス集合不変の機械記録であり閉鎖主張ではない)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 16957・class 13342 (全キー) は本Partの
  どの時点でもUNKNOWNのまま。** nodes数を勝敗として読まない。WIN採用は
  別adoption Part (pinned merger `90711961` 経由) のみで、scrutiny owner
  C++第二実装 gate `9193f5b6…` 待ちは本レーンは代行しない。joint greedy
  38,295・worklist 64,747はbookkeepingであり勝敗でも閉鎖でもない。


## Part CA (solver, amendment 2026-11-23): batch-27 residual o004..o054 continuation (class 13342 enumeration - WIN-CONTINUE事前登録)・verdict不消費・実行前に出版

Part BR (batch-27 class 13342) は事前登録のWIN-HALT規則によりo002で停止し、
残49キー (fragment o009 truncated p2・NOT evidence + fileless 48キー
o004/o006/o008/o010..o054・fresh・一度もverdictを出していない) が残った。
published batch-27 READMEの予約文言 (「published completeness guardが以降の
continuationでfresh-cold再実行する」) に従い、残49キーの単一オーナー実行を
宣言する (本amendmentより先にmainに存在するbatch-27 residual continuation
スコープの対抗宣言・amendmentがある場合は本宣言を破棄して着手しない。
branch / PRは作らない)。

- WIN-CONTINUE事前登録 (Part AW batch-14 residual / Part BH batch-19 residual /
  Part BT batch-26 residualの先例と同一の根拠): class 13342の全子LOSS閉包
  ルートはpublished o002 WIN honest label (Part BR drive-1 + Part BY第三実装
  交叉検証・独立host pinned-replica再現込み3系統) により既に反駁済み。
  残余キーのprobeはunknown数最小化のための列挙であり、ここでのさらなる
  WIN-HALTに情報価値はない。よってresidual installmentでは、published
  runbatch.shのrc=45 (WIN) が発火したキーはhonest WIN labelのみで記録し、
  drive driverを再起動して49キー完遂 (または本セッション限界) まで列挙を
  続ける。決定論mismatch -> 即時HARD-STOP rc=42 (以後のdrive起動も行わず
  停止)。budget枯損 (result 0) -> honest EXHAUSTED (UNKNOWN・同一条件での
  再probeなし)。
- 残留キー集合の機械導出 (prose不使用): published batch-keys.json (sha256
  `67814ed6287d68d6e97212c931dce2b7ee585219e20b4d43edb621632220a014`・54キー
  o001..o054・s5_index昇順 98526..460214) とpublished output/status.log
  (sha256 `50a4f407b369e06f9569238d1b0c35deb02dfad7d839cf57b2fc97a389512ca9`
  ・6行) から PASS/WIN-HALT/EXHAUSTED 済み5キー {o001, o002, o003, o005,
  o007} を除いた補集合 == {o004, o006, o008, o009, o010..o054} の49キー
  (fragment {o009} + fileless 48キー) であることを本hostで機械検証済み
  (published README記載のunprobed 49キー文言と一致)。**fragment o009**:
  published o009.p1.out は `# replay_done`付き完全単一パス (bookkeepingのみ・
  result 2 / nodes 9,082,839・証拠ではない) のためcompleteness guardは
  これを保持し、p2 truncated断片 (verdict行なし) のみをfresh-cold再実行する
  (よって将来のPASS行は、fresh p2とpublished p1の2-pass node-exact照として
  読まれる)。
- 新規scaffoldなし。published batch-27 dir
  `research/experiments/n11-centralreply-closure-class13342-batch27-20261123/`
  を正本としてそのまま使用する。本hostでpublished MANIFEST-sha256.txt掲載
  92ファイル (input 54+1・output/raw 12・output 2・scripts 8・val-gate 16)
  をcommit-pinned raw fetch + sha256再検証し **92/92 byte一致** を宣言前に
  機械確認済み (publish-then-executeの宣言先行preflight・read-only)。
- **実行場所と公開時序 (並走Part BZ非干渉の事前登録)**: 並走が同時刻に
  Part BZ (batch-24 y002/y004 + batch-27 o001/o003/o005/o007 6-LOSS
  canonical adoption・宣言 `8b7111be`・publish-then-execute) を宣言済みで
  あり、同Partはbatch-27 kit 92ファイルをsha pinで検証する。よって本Partの
  drive・val-gate・row-auditの実行は**(published dirのbyte-pinを一切更新
  しない) scratch copy** で行い、成果物 (raw・status.log追記・val-gate
  ca-host 4・派生監査script・row-audit json・MANIFEST更新) のpublished dir
  へのpublicationは **Part BZのstatus updateがmainに着地した後** に行う。
  Part BZが本セッション終了時点でも実行中の場合は成果物をscratchに保持し
  publicationを次回Runへ誠実繰越 (断片のままの出版は行わない)。どちらの
  場合も本宣言自体はBZと無関係 (BZの進行を一切待たない・結果に依存しない)。
- val-gate (実行前・本host): batch-23/24/25/26/27と同一の4アンカー。
  at2m 2行 -> result 0 / nodes 2,000,000 node-exact、15m 2行 -> result 2 /
  nodes (2,3,651,923)/(2,5,040,200) node-exact、禁止四角 95,670 x4、
  `# replay_done` x4 (truncationなし)。published val-gate/*.published-baseline.out
  基準線に対するnode数完全一致 (wall_s比較外) を実行の前提条件とする。
  本host再生成値は val-gate/*.ca-host.out としてoutputs出版に含める
  (published this-host 4・takeover-host 4ファイルは不変・byte-pin維持)。
- protocol: 2-pass fresh-cold node-exact、budget 15,000,000、
  1 solver / 1 row / 1プロセス、publish=ALL。実行はpublished drive driver
  (drive_batch27.sh sha256
  `9114e21142b1e0230eebc479b793dbdc1f0a2c994a52e7a924c3b2290cfe61bc`・
  1回起動あたりtimeout 260秒有界・残キー奇偶分割 worker最大2 = 控えめ並列・
  runbatch sha256
  `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84` byte-pin)
  をscratch copy上で反復起動する。完了済み5キー (published raws) は再実行
  しない。中断断片はpublished completeness guard (`# replay_done` 検査) が
  fresh-cold再実行する。
- row-audit: 列挙完遂後、published `row_audit_batch27.py` (sha256
  `ed21debece2939cccac76ebccd1c8450a81e8c7e9cb452da81aebe0b2392c2d6`・
  full-row監査としてscaffold事前登録済み) により54キー全行の機械検証を
  行う。**Part BT先例 (row_audit_batch26の潜在gateバグ) を踏まえた事前登録**:
  runbatchはWINキーを「PASS (nodes付き) + WIN-HALT」の2行構成で書くため、
  事前登録版がWIN行のstatus.log照合でfail-closedする場合は、差分がWIN行の
  2行pair照合のみの最小派生版を本Partのoutputsとして出版し全行監査に使用する
  (事前登録版のfail-closeも誠実記録・schemaはbatch-26 full-v2先例に倣い
  `n11-centralreply-closure-class13342-batch27-rowaudit-full-v2`)。監査は
  3回実行byte一致・tamper battery (verdict反転/WIN行pair除去/replay_done
  除去等・全tamperに適用実効性assert・実験files無改変byte検証) を実施する。
- verdict不消費: canonical exact-S5 verdict cache (Part BU採用時点 6,287行
  `e32a2e44…`・並走Part BZ採用後のどの状態にも) 書込みは一切しない。
  LOSS行は採用候補のみ (消費は別宣言adoption Partがpinned fail-closed
  merger `90711961…`で実行)。新規WIN行はunconsumed closure WIN候補の追加
  のみで採用しない (29候補 (o002込み) は読み書きとも非接触・本PartのWIN行が
  あれば30番目以降の候補として誠実記録)。採用判断はscrutiny owner C++第二実装
  gate pin `9193f5b6…`のまま (本レーンは代行しない)。
- 不接触: **Part BZ (6行adoption・並走所有・宣言 `8b7111be`)** の実験dir・
  outputs・canonical cache成果物には本Partは一切書き込まない (BZは本Partの
  batch-27 dir publicationを待たずに実行してよい・計算はscratchで独立)。
  batch 1..25各dir・各residual packet・batch-26残留 (l028含むadoption候補)・
  fast lane (y=23宣言 `6f79c81f`・K1256/K1257)・finite-field lane (K1254)・
  inversive-arc lane非接触。scratch以外のmain上の既存filesは無改変 (本Partの
  outputs publicationは本節の事前登録どおりBZ status update着地後のみ行う)。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・
  class 13342 (54キーすべて・o002・49残留キーを含む) は本Partのどの時点でも
  UNKNOWNのまま。nodes数を勝敗として読まない。被覆・secured・root勝敗の
  主張をしない。
- 本amendment observed HEAD-before-push: `b37117d97f1f6be91fb735fc36edb1afabd72220`
  (2026-11-23T13:41:31Z・Part BZ typo修正コミットを検知済み)。
  push直前に最新mainを再fetchし note blob sha1ロック
  `8dff57dd16d1148784d1fb0143995224a8e1e049` (560,088 bytes = Part BZ
  adoption宣言 typo修正 `b37117d9` 版) を再照合する (競合時は再fetchして
  本節を追記し直し、成立しない場合は簡潔に記録して次回へ回す)。


### Part BZ status update (2026-11-23, adoption): batch-24/27 6-LOSS canonical adoption 実行完了 - 全16ファイル出版byte検証済み・canonical cache 6,293行 (UNKNOWN担保不変)

(observed HEAD-before-push: 実行時の最新mainをコミットメッセージに記録。
実行window中の並走コミットは `f1d9e460` (K1254 order-32 arc gap・finite-field
lane) の1件のみで非接触を確認済み。push直前にnote blob lock
`8dff57dd16d1148784d1fb0143995224a8e1e049` (560,088 bytes = Part BZ宣言
typo-fix `b37117d9` 版) を再照合する。)

- 宣言 (`8b7111be` + typo-fix `b37117d9`, publish-then-execute) のprotocol
  1)-6) を逐次実行し、**全stepが宣言済みshaとbyte一致**:
  preflight (published Part BU refresh 3出力 `51d6bf0d`/`e54a0eb8`/`c1cb1bf5`
  を本hostでbyte再現)・maker x4 (increment `1d8556c1`・manifest `818fb0c3`)・
  merger selftest PASS + merge x3 (audit `cef05e36` x3同一bytes・scenario
  cache `9115be9e`)・refresh x3 + 隔離実行 (env -i・PYTHONHASHSEED=random・
  cwd=/tmp) (`fca242cc`/`14fc37c3`/`4218a6b4`/probe-worklist `7d9020d4`)・
  extractor x4 + 隔離実行 (decomp `e0005d42`)・tamper battery再実行
  **16/16検出 + 全probe復元byte検証** (T2d 3-level pin bypass→semantic
  「WIN set [] != unadopted ['o002']」・T8 merger同一キーverdict conflict
  →GATE FAILED出力未生成・CONTROL: scratch tree 別絶対pathでfull chain
  再実行・出版sha全件byte一致)。
- 出版5コミット ( fetch-back byte照合済み・全16ファイル ): A `92f67db1`
  (scripts 4: maker `eff939cd`・merger byte-copy `90711961`・extractor
  `a3adc0da`・refresh `0677e6eb`)・B `212136ef` (increment・
  increments-manifest・merge-audit x3計5ファイル)・C `d433323b`
  (merged scenario cache 6,293行・WIN 158 / LOSS 6,135・259,527 bytes
  `9115be9e`)・D (take 2) `1aba3f1f` (reaudit 3出力 + decomp計4ファイル)・
  E `a6f132d7` (README + MANIFEST-sha256 14行対象)。実験dir:
  `research/experiments/n11-centralreply-class16957-13342-loss6-adoption-reaudit-20261123/`。
- honest事故記録 (3件・いずれも検証層が捕捉): (1) 宣言sectionの
  unicode escape手打ち誤字3文字 (シ/丁/対) を宣言commit `8b7111be` の
  fetch-back byte検証が検出 → 修正commit `b37117d9` (数値・shaへの影響
  なし・fetch-back再検証byte一致)。(2) 出版D commit `aad298aa` が
  path誤り (dir名から `-reaudit-` 欠落) で4ファイルを誤locationに書込 →
  fetch-back 404が検出 → 正pathに再出版 `1aba3f1f` + 誤dirの4ファイル
  を掃除4 commits (`066e379e`/`5bb543da`/`cabe3ce4`/`3a38100`)・main
  HEADの誤dirは空。(3) protocol step 2のmaker run1が1回だけrc!=0
  (一過性・再現せず) → 即時再実行で x4 byte一致。
- 意味 (adopted facts only): canonical cacheはPart BU正本6,287行から
  6,293行へ (batch-24 y002/y004・batch-27 o001/o003/o005/o007の6-LOSS行
  をpinned fail-closed merger `90711961` 経由で採用・WIN/LOSS conflict
  gate・BASE重複ゼロのstructural gate込み)。scenario (adoption後) で
  class 16957 unknown_now 53→51・class 13342 54→50 (rank 26→6, 22→10)・
  closure churn left=[] entered=[]・free_now 38不変・update8 resolved
  +0 (133不変)・joint greedy 38,301→38,295・probe-worklist
  64,754→64,747・per-root free/uncovered不変 (individual greedy movers
  4 roots {5,16,24,48})。これらはすべてbookkeepingであり、root被覆・
  クラス閉鎖・secured・root勝敗の主張はしない。
- 不接触・未消費 (再確認): 非採用WIN 3行 (y001/y006/o002) はhonest
  labelのままunconsumed (29 unconsumed closure WIN候補に含まれ採用待ち・
  scrutiny owner C++第二実装 gate `9193f5b6…` 待ち・本レーンは代行しない)・
  fragment o009 (p1完全単一パスはbookkeepingのみ)・batch-24/27 fileless
  キー (49+48件ともUNPROBED)・canonical BASE (BU `e32a2e44…`) read-only
  (新正本は別filename `9115be9e` として出版・BASE書換なし)・fast lane・
  finite-field lane・inversive-arc lane非接触。
- 次回以降の候補: batch-28選定 (29-WIN交積・rank 27 class 5343/13758/
  14103) が次点。残るadoption候補なし (6行すべて採用完了)。knowledge
  folderの更新は次回実行時。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 16957・class 13342 (全キー) は本Part の
  実行・出版のどの時点でもUNKNOWNのまま。** nodes数を勝敗として読まない。
  WIN採用は別adoption Part (pinned merger `90711961` 経由) のみ。
- 事後注記 (本status updateのpush時・refit): push直前の再fetchで、本noteに並走による
  Part CA amendment (batch-27 residual continuation宣言・observed HEADはPart BZ typo-fix
  `b37117d9`) が追記済みであることが判明した。よって、事前登録のnote blob lock
  `8dff57dd16d1148784d1fb0143995224a8e1e049` (560,088 bytes版) は解消済みとして、
  本status sectionはPart CA追記後の最新正本 (568,693 bytes・fetch時点) 末尾に
  追記して出版した (observed HEAD-before-push・出版時に指定したnote blob shaは
  本commitのmessageに記録。本section本文の数値・sha・事故記録はPart BZ実行時点の
  記録であり不変・Part CAのoutputs publicationは本status update着地後という
  事前登録の条件どおり)。


## Part CB (solver, amendment 2026-11-23): batch-28 closure class 5343 exact-S5 probe (54キー aa001..aa054)・実行前に出版・verdict不消費

(batch-28選定を単一オーナーで着手するamendment。Part CA (batch-27 residual) の進行・outputsとは非接触・相互に進行を待たない。)

- 選定 (published factsのみから機械再導出): 実験dir
  `research/experiments/n11-centralreply-closure-class5343-batch28-20261123/`。
  対象は Part BZ正本 merged scenario cache 6,293行 (sha256
  `9115be9eca1e60828a90c50041f511b598ef79fc0be76d5e16821816e478e93e`) 上の
  closure順位 rank 27 class 5343 (mask `[1171516445255794688, 0]`・unknown 54・
  route-alive・29-WIN交積ゼロ・known WIN cost childゼロ・quarantine 0・
  54キーすべて canonical-safe)。rank→class対応は published BZ reaudit
  closure-classes.csv (sha256
  `14fc37c3a6f5c6753cac72a094d2c7693defb4a5e483558b3b87a42016b679d9`) と
  ranks 1..30 全行一致をmaker内で機械照合済み。rank 22 class 10968・rank 23
  class 23964 は PKT-collision blockedのまま。rank 28 class 13758
  (= unknown {459528} = batch-27 packet key o031)・rank 29 class 14103
  (= {460145} = o037) は batch-27 published packet (Part BR) と衝突するため
  本選定では除外 (両クラスはreaudit後の将来回)。runner-up: rank 35 class 2251・
  backup: rank 36 class 34269 (いずれも route-alive・29-WIN交積ゼロ・packet
  交差ゼロを zero-collision gateで機械確認済み)。
- 54キー aa001..aa054 (2文字prefix `aa` は新設計: 26単文字は published
  packets 1..27で使用済み。makerは prior 28 packets全key idが ^[a-z][0-9]{3}$
  形式であることをfail-closed gateで固定)。s5昇順 28037..199739・legal 64..96・
  membership {4:44, 3:9, 2:1}。
- input正本: `input/batch-keys.json` (sha256
  `af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5`・54キー)
  + 54 input CSV。maker `scripts/make_batch28_keys.py` (宣言時runtime sha256
  `d1ffe72f7a92c190db4982bbb59d10da9d1a967a6425fbc75cf745a255422f16`) を4回
  実行し全55ファイル byte-identicalを本セッションで機械確認済み。maker内
  fail-closed gate: prior 28 packets (1,406行・1,392 unique・14 shared
  positions・各packetのsha256埋込み) との交差ゼロ・quarantine 0・canonical
  重複ゼロ・29-WIN tie (28 + o002 (s5 209134))・ranks 1..26 (rank 22/23 skip)
  の反駁evidence (rank 6 class 13342 == {209134}・rank 10 class 16957 ==
  {91296, 368510}・rank 20 class 12643 == {115192}・rank 21 class 31600 ==
  {62435, 192809}・rank 24 class 25835 == {150241}・rank 25 class 30565 ==
  {68580, 191299})・rank 2 class 1849 unknown == {81011}・rank 19 class 5687・
  rank 26 class 5690 route-dead (known WIN == {209644})・BZ adoption tie
  (6 LOSS行 y002/y004/o001/o003/o005/o007がbase内LOSS(2)・class 16957 unknown
  51・class 13342 unknown 50)・published候補表807行一致・5830 receipt wins 5。
- 手法・停止規則・消費規則: Part B..BRと同一。pinned replica `jsreplay.js`
  (byte-copy sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`)・
  2-pass fresh cold・budget 15,000,000・1 solver / 1 row / 1プロセス・
  publish=ALL・exact-order=count・worker最大2。runbatch.sh byte-copy (sha256
  `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`) ・
  drive driver `drive_batch28.sh` (sha256
  `08dc059c55f4337d2c0a58c7e644a529af604a052a9137381345c3af6b6a2a5f`・1回起動
  あたりtimeout 260秒有界・残キー奇偶分割・worker最大2) を反復起動。
  determinism mismatch → 即時HARD-STOP (rc=42・以後のdrive起動も停止)。WIN
  (result 1) → 即時HALT (rc=45)・honest WIN label・verdict不消費 (29
  unconsumed closure WIN候補と書き込みとも非接触・本batchのWIN行は30番目
  以降の候補として誠実記録)。budget枯渇 (result 0) → honest EXHAUSTED
  (UNKNOWN・同一条件での再probe禁止)。
- val-gate (実行前・本host): batch-23..27と同一4アンカー (at2m 2行 →
  result 0 / nodes 2,000,000・15m 2行 → result 2 / nodes 3,651,923 /
  5,040,200・禁止四角 95,670 x4・`# replay_done` x4)。published-baseline 4組
  (batch-27 published kitのbyte-copy) に対するnode数完全一致が実行の前提
  条件。本host再生成は val-gate/*.cb-host.out としてoutputs出版に含める。
- row-audit: 列挙完遂後 `row_audit_batch28.py` (再適用版・sha256
  `656cac31fd95f7193c3df12efa05512cf2e746063740cfee7e5c574a5be66d56`) で
  54キー全行監査3回byte一致 + tamper battery (verdict反転・WIN行pair除去・
  replay_done除去等・全tamper検出assert)。WIN-HALT停止時はWIN行pair照合
  最小派生版 `row_audit_batch28_win_halt.py` (sha256
  `730ef5505deb9ea54c8a0c2986f88e9d071a1b76d138f4c26b9859208c637438`) を
  併用 (Part BT先例の事前登録と同一)。
- 消費規則: 2-pass一致かつ result 2 (LOSS) のキーのみ increment cache候補と
  して出版してよい (canonical採用は別adoption Partがpinned fail-closed merger
  `90711961…` で実施)。本batch単体ではroot被覆・クラス閉鎖・第三手securedの
  主張をしない (閉鎖判定は後続のreaudit + 独立監査が行う)。
- 不接触: Part CA (batch-27 residual continuation・並走所有) の実験dir・
  outputs・batch-27 dir byte-pinには本Partは一切書き込まない (相互に進行を
  待たない)。本Partの54キーはpublished 28 packetsと交差ゼロ (maker gate)・
  Part CA残留キー (o004..o054) ともprefix・s5集合でdisjoint。batch 1..27
  published dirs不変。fast lane (y=22/23宣言)・finite-field lane (K1254)・
  inversive/z19 lanes非接触。canonical BASE/正本 (`e32a2e44…` / `9115be9e`)
  read-only (本Partはverdict cacheへ書き込まない)。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・
  class 5343 (54キーすべて) は本Partの実行・出版のどの時点でもUNKNOWNの
  まま。nodes数・pass数を勝敗として読まない。
- 本amendment observed HEAD-before-push: `d6c37739cb478f18832e4d3edec8ffbacaec342b` (2026-11-23)。push直前に
  最新mainを再fetchしnote blob sha1ロック `94417ca8fd92b3a8975f2c4d3bc74eab456aa793` を再照合する
  (競合時は再fetchして本節を追記し直し、成立しなければ簡潔に記録して次回へ
  回す)。



### Part CB status update (2026-11-23, solver): batch-28 class 5343 WIN-HALT aa001/aa002 - 出版82ファイルfetch-back byte一致・verdict不消費 (UNKNOWN担保不変)

(observed HEAD-before-push: `4f9d2cef7e6b12bf52bf9ffd3bcba8869ffca194`。push直前にnote blob sha1ロック
`eb7e4454639406f36a8c182611080c5c301dde08` (fetch時点版) を再照合する。)

- 宣言 (`395219833f80a5d345c0acf999407b31e66832cb`, publish-then-execute・宣言host
  実行) どおり実行。preflight: maker x4 byte-identical (全55ファイル)・
  全gate PASS・push直前の対抗確認 (対抗batch-28宣言なし・実験dir不在を
  機械確認済み)。
- val-gate (本host): cb-host 4/4 node-exact (published-baseline byte-copy基準・
  禁止四角 95,670 x4・`# replay_done` x4・wall_s比較外)。
- drive-1: 1 invocation (drive_batch28.sh・2 worker・260s有界) で **両workerとも
  最初のキーで事前登録 WIN-HALT rc=45**。
  **aa002 WIN** (honest label・2-pass node-exact・result 1・nodes 6,527,041
  (budget 15M内)・key (1171516445390012416, 0)・s5 index 87306・legal 86・
  membership 2・wall 72/73s)・**aa001 WIN** (honest label・2-pass node-exact・
  result 1・nodes 13,183,855・key (1315631633331650560, 0)・s5 index 28037・
  legal 88・membership 4・wall 147/75s)。**30番目・31番目の候補**として誠実記録
  (29 unconsumed closure WIN候補と書き込みとも非接触・採用判断は scrutiny
  owner C++第二実装 gate pin `9193f5b6…` のまま・本レーンは代行しない)。
  残り52キー (aa003..aa054) は fileless UNPROBED・EXHAUSTED 0・MISMATCH 0
  (rc=42不発)・truncated断片 0。
- row-audit-winhalt (最小派生版 `96867282…`・schema
  `n11-centralreply-closure-class5343-batch28-rowaudit-winhalt-v1`): PASS 3回
  byte一致 (json sha256 `3f50b4f6…`)・completed 2 (WIN 2)・fragments []・
  fileless 52・unprobed 52。tamper battery **7/7検出** (verdict反転 / nodes改竄 /
  packet legal改竄 (batch-keys.json) / status WIN-pair除去 / replay_done strip /
  budget改竄 / nondigit nodes)・実験filesはbattery前後でbyte不変。
- 出版3コミット (commit-pinned raw URLでfetch-back **82/82 byte一致**):
  scaffold `a3dc8202953423620c94735e6345435734f1f63b` (scripts 7 + input 55 +
  val-gate 12)・outputs `84d495e8b4b42f57969994b071d6b4e3c28d923c` (raw 4 +
  status.log + row-audit json)・README+MANIFEST
  `4f9d2cef7e6b12bf52bf9ffd3bcba8869ffca194` (MANIFEST 81行)。実験dir:
  `research/experiments/n11-centralreply-closure-class5343-batch28-20261123/`。
- honest事故記録 (2件・いずれも検証層が捕捉): (1) 事前登録版
  `scripts/row_audit_batch28_win_halt.py` (宣言pin `730ef550…`) は batch-26版
  からのsed適用時に単文字前提のkey id gate (len 4・first letter・`o\d{3}`) が
  残っており、batch-28の2文字prefix `aa###` に対してfail-closeした (監査対象
  ファイルは無傷)。差分は当該gate 1箇所を `aa[0-9]{3}` 形式に修正するだけの
  最小派生版を出版し全行監査に使用 (fail-close自体も誠実記録)。(2) tamper
  battery初回構築の2件 (input CSV直接改竄・sedパターン不一致) はbattery側の
  構築ミスで監査のgapではない (実験files無改変・正規battery 7/7で裏どり)。
- 意味 (route statementのみ・verdict不消費): aa001/aa002 のいずれかが採用された
  場合、**class 5343 の全LOSS閉包ルートは反駁証拠を持つ** (batch-21 a003・
  batch-22 k002・batch-26 l028・batch-27 o002 に続く)。bookkeepingのみで閉鎖・
  被覆・secured・root勝敗の主張はしない。
- 次回以降の候補: (a) batch-28 WIN 2行 (aa001/aa002) の第三実装交叉検証
  (Part BY先例)・(b) aa001/aa002あるいは将来のLOSS行adoption (別Part・pinned
  merger `90711961…` 経由のみ)・(c) batch-29選定はreaudit再実行後 (rank 28
  class 13758 {459528} = batch-27 o031・rank 29 class 14103 {460145} = o037 は
  batch-27 packet衝突でreaudit待ち・rank 35 class 2251・rank 36 class 34269 が
  zero-collision clean候補)。Part CA (batch-27 residual) の進行とは非接触。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・
  aa001/aa002を含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
  nodes数・wall秒数を勝敗として読まない。

- 事後注記 (typo-fix・本commit): Part CB宣言sectionとPart CB status sectionは
  初回pushで行区切りが JSON escape起因の literal `\n` 2文字列として書き込まれる
  事故があった (数値・sha・published filesへの影響なし・fetch-back検証で検出)。
  本commitで該当2sectionのみ改行へ復元した (junction junk 2 個・section内 144 個)。
  observed HEAD-before-push: `e3c4cbc6b6fb3b2e18b11375e0e0809759872024`、修復時 note blob sha1ロック `b3e92fe8cb25b01bf7e90c7cf5886e16e3ca5542`。
  その他のsection・数値・shaは不変。

## Part CC (verifier, amendment 2026-11-23): batch-28 WIN rows aa001/aa002 third-implementation cross-verification・実行前に出版・verdict不消費

(Part CB (batch-28・class 5343) のWIN-HALT 2行に対するpinned第三実装交叉検証を単一オーナーで着手するamendment。Part BY (batch-27 o002) の手続きのbatch-28再適用。対抗宣言なしをpush直前に機械確認済み (note内に「Part CC」表記ゼロ)。)

- 対象: `research/experiments/n11-centralreply-closure-b28win-thirdimpl-20261123/`。
  batch-28 (Part CB・宣言 `395219833f80a5d345c0acf999407b31e66832cb`) で出版された
  WIN行 **aa001** (key (1315631633331650560, 0)・s5 28037・legal 88・membership 4・
  published replica result 1・nodes 13,183,855・**30番目の unconsumed closure WIN候補**) と
  **aa002** (key (1171516445390012416, 0)・s5 87306・legal 86・membership 2・
  published replica result 1・nodes 6,527,041・**31番目**)。いずれもhonest label・
  2-pass node-exact。残り52キー (aa003..aa054) はfileless UNPROBEDのまま本Partは
  一切触れない。
- 誠実な開示: batch-28 drive-1 は Part CB実行hostの単一環境出版物であり、
  aa001/aa002の第二実行環境同時再現は出版されていなかった。本Partのthis-host
  pinned-replica (fresh-cold 2-pass) はpublished source bytesのsha検証後に全工程を
  再実行するもので、node-exact一致が達成された場合はaa001/aa002に対して最初の
  「独立セッション再現」として記録する (実行hostの物理的相違までは主張しない)。
- 事前ゲート (宣言前・本host・すべて機械確認済み): maker
  `scripts/make_inputs_cc.py` (runtime sha256
  `8255d0adfe82ccc33d49c1339281fb18410748d165fa36e099529233249ab700`・Part BY maker
  359abebc…のbatch-28派生・2文字prefix aa### gate込み) を4回実行し全出力
  byte-identical・input/rows.json (sha256
  `b7222edf773c541fafac165d16355fd1f9469ec31bc233f78a35037fad542d39`・schema
  `n11-centralreply-closure-b28win-thirdimpl-input-v1`) 再生成byte一致。
  maker内fail-closed gate: sources 4ピン (batch-keys-b28 `af19208f…` /
  status-b28.log `e98b5d23…` / README-b28 `1b9f87b1…` /
  row-audit-winhalt-b28 `3f50b4f6…`) + raw 4ピン (aa001.p1 `b3f396bd…` /
  aa001.p2 `59a3e8a1…` / aa002.p1 `07d9d643…` / aa002.p2 `7d2d26a8…`) +
  published input CSV 2ピン (aa001 `8083b62e…` / aa002 `6310e641…`) + Part BF
  anchor/negative CSV 4ピン (b6174a3f… / e13d2a6c… / 8e64b9ad… / f19cd5a3…・
  provenance chain AR→BF→BK→BM→BS→BV→BW→BX→BY→CC)。status.log 4行
  (WIN PASS 2 + WIN-HALT 2・retry/fragment/loss行ゼロ)・row-audit
  (probed 2・win_rows [aa001, aa002]・loss_rows []・fileless_unprobed 52・
  fragment_keys {})・README文言 (両WIN honest label・nodes 2件・
  30番目・31番目候補・fileless UNPROBED・scrutiny owner継続・class 5343/Part CB)
  の各gate全PASS。tamper battery **7/7検出** (T1 raw aa001.p1 nodes+1 /
  T2 row-audit probed 2→3 / T3 README aa001 WIN→LOSS / T4 status aa001 verdict
  反転 1→2 / T5 published-input aa002 legal 86→85 / T6 BF anchor k02a lo+1 /
  T7 batch-keys s5_index 28037→28038・全tamperに適用実効性確認・scratch (/tmp)
  上で実施し実験sources無改変byte検証済み)・clean control PASS。
- 手法 (Part BYと同一のgate論理・1行1プロセス・逐次): (1) rules gate
  (pinned `verify_tbl.js` `c8c52528…`・replica quads 95,670 == third-impl quads
  95,670・triples mismatches 0)。(2) val-gate this-host 4行 (pinned
  `jsreplay.js` `84585617…`・published baseline 4組 (batch-28 kitのbyte-copy)
  に対するnode-exact一致が前提・wall_s比較外)。(3) negatives 2種
  (ng1 legal+1 / ng2 stones+1 → GATE_FAIL設計どおり)。(4) anchors 2行
  (k02a clean WIN expansions 9,106,337 / ttHits 4,991,527・l1a clean LOSS
  7,660,602 / 3,951,175・a/b determinism)。(5) 本host pinned-replica 2-pass
  fresh-cold (budget 15,000,000・aa001/aa002各p1/p2・determinism field一致 +
  published raw fields (result 1・nodes 13,183,855 / 6,527,041) 完全一致)。
  (6) 第三実装 (非df-pn AND/ORミニマックス `third_impl.js` pin `08ea958f…`)
  による対象行のverdict-level交叉検証 (driver `run_thirdimpl.sh` byte-copy
  sha256 `a0b77d8330c696a5a7da2883d49110ae8703dc1673be10d3a9972ea53c885a41`・
  cap 300,000,000・wallcap 240s・memo-power=22・1行2回 (a/b) determinism gate)。
  wall超過 (runlimit) はhonest wall-inconclusiveとして記録し検証主張としない。
  cleanな不一致はdivergence evidenceとして記録するが本レーンではverdictを
  書き換えない。
- 監査: `scripts/audit.py` (sha256
  `b7cfb0ce1fa2457ec7b4bfbb595aabcdd4303859800566104370b82d864d8b96`・Part BY
  audit 7f7fa3d1…のbatch-28派生・schema
  `n11-centralreply-closure-b28win-thirdimpl-audit-v1`)。G0 (input/rows整合)・G1
  (script pin 3種)・G2 (rules gate)・G2b (this-host replica p1/p2 determinism +
  published fields一致)・G3 (anchors node-exact)・G4 (negatives GATE_FAIL)・
  G5 (targets a/b determinism + verdict agreement) の全gate MUST PASS・3回実行
  byte一致 (audit-run1/2/3)・audit tamper battery 3種 (T1 script pin反転
  (PIN_THIRD末尾1桁反転) → pin gate fail ABORT / T2 targets a.out det-pair
  改ざん (expansions +1) → target-det-pair gate fail / T3 G0 input改ざん
  (CSV legal +1) → input-matches-rows gate fail・いずれもscratch copy上で実施し
  実験files無改変byte検証)。
- 主張と消費規則: 本検証はverdict-level文献 (three-implementation
  corroboration) のみ・**verdict不消費** (採用判断はscrutiny owner C++
  第二実装 gate pin `9193f5b6` 待ち・本レーンは代行しない)。aa001/aa002の
  採用された場合のroute statement: 単WIN子によりclass 5343の全LOSS閉包ルートは
  反駁証拠を持つ (Part CB READMEと同一文言)。閉鎖・被覆・secured・root勝敗の
  主張はしない。canonical cache (`9115be9e…` 6,293行) read-only・不変。
- 不接触: batch-28 fileless 52キー (aa003..aa054)・Part CA (batch-27 residual)・
  batch 1..28 published dirs (不変)・fast lane (y=22/23)・finite-field lane
  (K1254)・inversive/z19 lanes・19root計画。28 unconsumed closure WIN候補の
  採用状態にも非接触。
- UNKNOWN担保: 標準11x11空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・
  class 5343 (54キーすべて・aa001/aa002を含む) は本Partの実行・出版の
  どの時点でもUNKNOWNのまま。nodes数・expansions数・ttHits数・wall秒数を
  勝敗として読まない。
- 出版計画: A scaffold (scripts 6 + input 7 + sources 14 + val-gate 8 = 35
  files) → B outputs (rules-gate + this-host val-gate 4 + replica 4 +
  negatives 2 + anchors 4 + targets 4 + audit 3回分 + status.log) →
  C README + MANIFEST-sha256 (全published files分)。各コミットはcommit-pinned
  raw URLでfetch-back byte照合・push直前に必ず最新mainを再fetchして
  observed HEADを記録する。
- 本amendment observed HEAD-before-push: `59fababc6a49a077fbe03f3f1e25a359816f338a`
  (2026-11-23)。push直前に最新mainを再fetchしnote blob sha1ロック
  `fad849e99ffa4e460b6ca3605fbc0d885c30c828` (585,934 bytes版) を再照合する
  (競合時は再fetchして本節を追記し直し、成立しなければ簡潔に記録して次回へ回す)。

### Part CC status update (2026-11-23, verifier): batch-28 aa001/aa002 third-impl clean WIN 2/2・本host pinned-replica node-exact 2/2・出版全files fetch-back byte一致・verdict不消費 (UNKNOWN担保不変)

(observed HEAD-before-push: `29060369aa04e1d8f97d211bf455df8a63110d59`。push直前にnote blob sha1ロック
`9703ae8f742260d8eea2d675c60c216a22ec9b92` (593,538 bytes版・fetch時点) を再照合する。status section本文の数値は実行時点の記録で不変。)

- 宣言 (`0e2114913a593340c39a05a8fc4f4a6bbfe46937`, publish-then-execute) どおり実行
  (対抗宣言なし・実験dir 404事前確認済み)。
- 前提ゲート (宣言前): maker `make_inputs_cc.py` (`8255d0ad`) 4回実行全出力
  byte-identical・rows.json (`b7222edf`) 再生成byte一致・全sourceピン照合
  (published batch-28 MANIFEST 81行と全行一致)・maker tamper battery 7/7検出
  (T1..T7・適用実効性assert込み・scratch上・実験sources byte不変)・clean control PASS。
- 実行 (宣言protocol 1-6・逐次): (1) rules gate PASS (quads 95,670 == 95,670・
  triples checked 195,044・mismatches 0)。 (2) val-gate this-host 4/4 node-exact
  (at2m 2行 result 0/nodes 2,000,000 x2・15m 2行 result 2/nodes 3,651,923・
  5,040,200・`# replay_done` x4・wall_s比較外)。 (3) negatives 2/2 GATE_FAIL
  設計どおり (ng1 derived=87 declared=88・ng2 bits=5 declared=6)。 (4) anchors
  2/2 本host node-exact a/b determinism PASS (k02a clean WIN 9,106,337/4,991,527
  wall 32.90/32.49s・l1a clean LOSS 7,660,602/3,951,175 wall 28.36/28.89s・
  published第三実装値と同一)。 (5) **本host pinned-replica 2-pass fresh-cold
  2/2 node-exact**: aa001 result 1 nodes 13,183,855 (wall 84/91s)・aa002 result 1
  nodes 6,527,041 (wall 42/43s)・両行ともpublished batch-28 raw fieldsと完全一致・
  EXHAUSTED 0・mismatch 0 (**aa001/aa002に対する最初の独立セッション再現**)。
  (6) **targets 2/2 clean WIN一致 (verdict agreement 2/2・WALL-INCONCLUSIVE 0・
  DIVERGENCE 0)**: aa001 result 1 expansions 15,677,345 ttHits 8,277,865 (a/b
  完全一致・wall 56.97/55.07s)・aa002 result 1 expansions 7,624,309 ttHits
  4,113,380 (a/b完全一致・wall 27.22/27.08s)・cap 300M・wallcap 240s・
  memo-power=22・pass-one拡張数合計 23,301,654。
- 監査 (`audit.py` `b7cfb0ce`・schema
  `n11-centralreply-closure-b28win-thirdimpl-audit-v1`): **ALL 67 GATES PASS**
  3回実行byte一致 (audit-run1/2/3 `df402055`・audit-summary 4ファイル `9c22c1e7`)
  ・verdict_agreements 2/2 (aa001/aa002 third=1 replica=1 agree=true)・
  wall_inconclusive 0。audit tamper battery **3/3検出** (pin反転→
  pin-third_impl.js gate fail・aa002.a expansions +1→target-aa002-det-pair gate
  fail・aa002 CSV legal 86→87→input-aa002-matches-rows gate fail・scratch上で実施し
  実験files byte不変)・clean control PASS。
- 出版4コミット (commit-pinned raw URLでfetch-back **64/64 byte一致**): 宣言
  note amendment `0e211491` (note blob `9703ae8f`・prefix byte一致)・A scaffold
  `1f38deb8` (35 files = scripts 6 + input 7 + sources 14 + val-gate 8)・B outputs
  `31ddca98` (27 files = rules-gate + this-host val-gate 4 + replica 4 +
  negatives 2 + anchors 4 + targets 4 + audit 3回分 7 + status.log)・C README+
  MANIFEST `29060369` (63行)。実験dir:
  `research/experiments/n11-centralreply-closure-b28win-thirdimpl-20261123/`。
- 意味 (route statementのみ・verdict不消費): 第三実装 (非df-pn AND/OR minimax) の
  clean verdictがpublished replica verdictと2/2で一致した (three-implementation
  corroboration文献)。aa001 (30番目)・aa002 (31番目) の採用判断はscrutiny owner
  C++第二実装 gate pin `9193f5b6` のまま・本レーンは代行しない。canonical cache
  (`9115be9e` 6,293行) read-only不変。閉鎖・被覆・secured・root勝敗の主張はしない。
- 次回以降の候補: (a) aa001/aa002あるいは将来のLOSS行adoption (別adoption Part・
  pinned merger `90711961…` 経由のみ)・(b) batch-29選定はreaudit再実行後 (rank 28
  class 13758 {459528} = batch-27 o031・rank 29 class 14103 {460145} = o037 は
  batch-27 packet衝突でreaudit待ち・rank 35 class 2251・rank 36 class 34269 が
  zero-collision clean候補)・(c) batch-28 fileless 52キー (aa003..aa054) の将来
  probe (別宣言)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・
  aa001/aa002を含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
  nodes数・expansions数・ttHits数・wall秒数を勝敗として読まない。WIN/LOSS採用は
  別adoption Part (pinned merger `90711961…` 経由) のみ。

### Part CD 宣言 (2026-11-23): batch-28 fileless 52キー (aa003..aa054) drive-2 continuation — publish-then-execute

(observed HEAD-before-push: `9ea8ec121ebf…` (16:00:22Z・別projectの実験commit)。
push直前にnote blob sha1ロック `a2a159255055549d5b97e388a9f566061aaea1d9`
(598,374 bytes版) を再照合・fail-closed shaで更新する。対抗宣言なし
(note内 Part CD/drive2 記述ゼロを機械確認済み)・実験dir
`research/experiments/n11-centralreply-closure-class5343-batch28-drive2-20261123/` は404確認済み。)

- **目的**: batch-28 (Part CB・class 5343・54キー) の published kitを
  byte-clone継続し、UNPROBED fileless 52キー aa003..aa054 を pinned replica
  (jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`)
  で2-pass fresh-cold probeする drive-2 wave。**verdict不消費**。閉鎖・被覆・
  secured・root勝敗の主張をしない。
- **事前登録stop rules (published runner `runbatch.sh`
  `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84` 変更なし)**:
  各workerの最初のWIN行 (replay result 1) で rc=45 halt・そのinvocationでwave終了
  (次waveは別宣言)。EXHAUSTED (result 0) はhonest UNKNOWN bookkeeping
  (same-condition再probeなし)。MISMATCH rc=42 hard-stop。TRUNCATED pass
  (`# replay_done`なし) はevidenceでなくfresh-cold retry。
- **kit** (drive-2 dir = published batch-28 kitのbyte-clone・68 filesをpublished
  MANIFEST pinsと全件byte照合済み): scripts byte-pin再利用 (runner `f591f8c2…`・
  jsreplay `84585617…`・drive `08dc059c…`・row_audit full `656cac31…`・
  row_audit win-halt `96867282…`・maker `d1ffe72f…`・runwave `8efd78c2…`・一切変更なし)。
  input 55 files (54 CSV + batch-keys.json `af19208f…`・published pinsそのまま)。
  output seeds: published status.log `e98b5d23…` (drive-1の4行) + published raw
  outs aa001/aa002 (4 files・published pins)。**drive-1のcompleted行 (aa001/aa002)
  は再probeしない**。val-gate: sanctioned 4キー (at2m×2 budget 2M・15m×2
  budget 15M) input CSV + published baselines (published pins) + 本host fresh
  .cb-host.out。
- **実行protocol (宣言後・逐次)**: (1) val-gate 4/4 本host node-exact
  (published baseline比較・wall_s比較外) を確認。(2) waves: `bash
  scripts/drive_batch28.sh` 反復 (残りキーはpublished status.logから機械導出・
  odd/even 2 workers・各worker `timeout 260`・同時solver 2プロセス上限)。
  (3) rc=45観測でwave終了。(4) rc=42はhard-stop・即時honest記録。
  (5) 全52キー完了または時間切れで停止・部分完了もhonestに出版 (残りは
  fileless UNPROBEDのまま)。
- **監査**: win-halt状態なら `row_audit_batch28_win_halt.py` (`96867282…`)・
  54キー全部completedなら `row_audit_batch28.py` (`656cac31…`) をdrive-2 dirに
  対しそのまま実行 (kit構造同一のためbyte-pin再利用)。tamper batteryはscratch上
  で実施 (WIN行verdict反転 / status.log nodes改竄 / seed raw nodes+1 が該当
  gate failで検出されること)・実験dir byte不変を検証。
- **出版**: A scaffold (scripts 8 + input 55 + output seeds 5 + val-gate
  inputs/baselines 8 + README) → B outputs (fresh val-gate host outs・新probe
  raw outs・統合status.log・再生成row-audit json) → C MANIFEST-sha256 → note
  status update。全files commit-pinned raw URL fetch-back byte照合。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa001/aa002
  含む) は実行前後ともUNKNOWNのまま。** nodes数を勝敗として読まない。
  WIN/LOSS採用は別adoption Part (pinned merger `90711961…` 経由) のみ。

### Part CE 宣言 (2026-11-23): batch-23 fileless 51キー (s003..s053) drive-2 continuation — publish-then-execute

(observed HEAD-before-push: 最新mainをpush直前に再取得しコミットメッセージに記録する。
push直前にnote blob sha1ロックを再照合し、fail-closed shaで更新する。対抗宣言なし
(note内 Part CE / batch-23 drive-2 記述ゼロを機械確認済み)。実験dir
`research/experiments/n11-centralreply-closure-class31600-batch23-drive2-20261123/` は
push前に404を確認する。)

- **目的**: batch-23 (Part BN・class 31600 rank 19・54キーではなく53キー) の published kitを
  byte-clone継続し、UNPROBED fileless 51キー s003..s053 を pinned replica
  (jsreplay.js sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`)
  で2-pass fresh-cold probeする drive-2 wave。**verdict不消費**。閉鎖・被覆・
  secured・root勝敗の主張をしない。
- **WIN-CONTINUE事前登録 (Part BT batch-26 residual / Part CA batch-27 residual の
  先例と同一の根拠)**: class 31600の全子LOSS閉包ルートはpublished s001/s002 WIN
  honest label (Part BN drive-1 + Part BV第三実装交叉検証3系統・同一クラス内2WINは
  12643/25835と同型) により既に反駁済み。残余キーのprobeはunknown数最小化のための
  列挙であり、ここでのさらなるWIN-HALTに情報価値はない。よってresidual installmentでは、
  published runnerのrc=45 (WIN) が発火したキーはhonest WIN labelのみで記録し、
  drive driverを再起動して51キー完遂 (または本セッション限界) まで列挙を続ける
  (部分完了もhonestに出版・残りはfileless UNPROBEDのまま)。決定論mismatch →
  即時HARD-STOP rc=42 (以後のdrive起動も行わず停止)。budget枯渇 (result 0) →
  honest EXHAUSTED bookkeeping (UNKNOWN・15M同条件の再probeなし)。truncated pass
  (`# replay_done`なし) はevidenceでなく、published completeness guardが次の
  invocationでfresh-cold再実行する。
- **残留キー集合の機械導出 (prose不使用)**: published batch-keys.json (sha256
  `2776acafbb638cb148661b3988b7eb36bc8519e5b7b75b415b01618bfcb85bf7`・53キー) から
  published output/status.log (sha256 `1e4ccea9025cb11f38a05c7403a85a7d838398040506201738516bf46fa97e60`・
  4行: s001/s002 の PASS + WIN-HALT 2行ペア) のcompleted集合 {s001, s002} を除いた
  補集合 == {s003..s053} 51キー (fileless・fragmentゼロ) であることを本hostで機械検証済み
  (published README記載のunprobed 51キー文言と一致)。**drive-1のcompleted行
  (s001/s002) は再probeしない**。
- **kit** (drive-2 dir = published batch-23 dirのbyte-clone): published MANIFEST-sha256
  79行のうち本dirがcloneする75ファイル (scripts 8 + input 54 + output/status.log +
  output/raw 4 + output/row-audit-winhalt.json + val-gate input 4 + published-baseline 4)
  をcommit-pinned raw fetch + sha256再検証し **75/75 byte一致** を宣言前に機械確認済み
  (publish-then-executeの宣言先行preflight・read-only)。残る .this-host.out 4ファイルは
  published dir専用としてclone対象外 (drive-2では本host fresh `.ce-host.out` に置き換え)。
  scripts byte-pin再利用 (drive `37bb126c…`・runbatch `f591f8c2…`・runwave
  `8efd78c2…`・jsreplay `84585617…`・row_audit full `f45b125e…`・row_audit win-halt
  `f55ae559…`・make_batch23_keys `7b2c8e53…`・一切変更なし)。
- **val-gate (実行前・本host)**: batch-23..28と同一の4アンカー。at2m 2行 →
  result 0 / nodes 2,000,000 node-exact、15m 2行 → result 2 / nodes
  (2, 3,651,923)/(2, 5,040,200) node-exact、禁止四角 95,670 x4、`# replay_done` x4。
  published val-gate/*.published-baseline.out 基準線に対するnode数完全一致
  (wall_s比較外) をwave実行の前提条件とする。本host再生成値は val-gate/*.ce-host.out
  としてoutputs出版に含める。
- **実行protocol (宣言後・逐次)**: (1) val-gate 4/4 本host node-exactを確認。
  (2) waves: `bash scripts/drive_batch23.sh` 反復 (残りキーはpublished status.logから
  機械導出・odd/even 2 workers・各worker `timeout 260`・同時solver 2プロセス上限)。
  (3) rc=45観測でそのwave終了後にdriverを再起動する (WIN-CONTINUE)。(4) rc=42は
  hard-stop・即時honest記録。(5) 51キー完了またはセッション限界で停止。
- **row-audit**: 51キー完遂後、published `row_audit_batch23.py` (`f45b125e…`・full-row
  監査) をdrive-2 dirに対しそのまま実行 (kit構造同一のためbyte-pin再利用)。
  **Part BT先例 (row_audit潜在gateバグ) を踏まえた事前登録**: runbatchはWINキーを
  「PASS (nodes付き) + WIN-HALT」の2行構成で書くため、事前登録版がWIN行
  (s001/s002含む) のstatus.log照合でfail-closedする場合は、差分がWIN行の2行pair
  照合のみの最小派生版 `row_audit_batch23_full.py` (schema
  `n11-centralreply-closure-class31600-batch23-rowaudit-full-v2`) を本Partのoutputsとして
  出版し全行監査に使用する (事前登録版のfail-closeも誠実記録)。監査は3回実行byte一致・
  tamper battery (verdict反転 / status.log nodes改竄 / seed raw nodes+1 / replay_done除去
  等の該当gate fail検出・全tamperに適用実効性assert・scratch上・実験files無改変byte検証)
  を実施する。
- **verdict不消費**: canonical exact-S5 verdict cache (6,293行 `9115be9e…`) への書込みは
  一切しない。LOSS行は採用候補のみ (消費は別adoption Partがpinned fail-closed merger
  `90711961…`で実行)。新規WIN行はunconsumed closure WIN候補の追加のみ
  (aa001/aa002までの31候補に続き32番目以降として誠実記録・採用判断はscrutiny owner
  C++第二実装 gate pin `9193f5b6` のまま・本レーンは代行しない)。
- **不接触**: Part CD (batch-28 drive-2・並走所有) の実験dir・outputs、Part CA
  (batch-27 residual・並走所有) のprogress・outputs, batch 1..22各published dir,
  batch-24/25/26/27/28各published dir (不変)、batch-24 fileless 49キー・batch-25
  fileless 51キー (将来の別宣言対象)、fast lane (y=23)・finite-field lane (K1254)・
  inversive/z19 lanes、19root計画、28+3 unconsumed closure WIN候補の採用状態、
  canonical cache read-only不変。
- **出版**: A scaffold (scripts 8 + input 54 + output seeds 5 + val-gate 8 + README) →
  B outputs (fresh val-gate ce-host outs 4・新probe raw outs・統合status.log・
  再生成row-audit json 3回分) → C MANIFEST-sha256 → note status update。
  全files commit-pinned raw URL fetch-back byte照合・push直前に必ず最新mainを再fetchして
  observed HEADを記録する。
- **UNKNOWN担保**: 標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 31600 (53キーすべて・s001/s002を含む) は実行前後とも
  UNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。WIN/LOSS採用は別adoption Part
  (pinned merger `90711961…` 経由) のみ。

### Part CD status update (2026-11-23): batch-28 drive-2完遂 — aa003 LOSS行・aa004/aa005 EXHAUSTED・aa006/aa007 WIN-HALT行・val-gate 4/4・row-audit(winhalt) PASS・tamper battery 4/4・出版全files fetch-back byte一致・verdict不消費 (UNKNOWN担保不変)

(observed HEAD-before-push: `b3c6daf628f0c1b5059845ebe40ee6d42d6b9f0f` (Part CD C
commit)。push直前にnote blob sha1ロック
`9610c469352689c782d02ede25dbb809e6c81f07` (609,498 bytes版・Part CE宣言
amendmentを含むfetch時点) を再照合・fail-closed shaで更新する。並走のPart CE
(batch-23・class 31600) 宣言は本Partと非接触であることを確認済み。)

- 宣言 (`0ae99cf0e18b0487f47fbe2ad31dcd14237e58cc`, publish-then-execute) どおり
  実行 (対抗宣言なし・実験dir 404事前確認済み・kit clone 68 files published pins
  全件byte照合済み)。
- val-gate (宣言protocol (1)): 本host fresh 4/4 node-exact (published baselines
  比較・wall_s比較外・`.cd2-host.out` 4 files出版)。
- 実行 (宣言protocol (2)-(5)・ただし後述orchestration偏移を正直開示):
  wave-1 (drive_batch28.sh 1回 260s窓): aa003 **LOSS行 (result 2・nodes
  4,070,373・two-pass node-exact)**。aa004 p1完走後・aa004 p2・aa005 p1 は260s窓で
  truncated (TRUNCATED-RETRY行・sidecar 4 filesはevidenceでないbookkeepingとして
  出版)。
- **orchestration偏移 (正直開示)**: aa004 (legal 91) はbudget 15,000,000でEXHAUSTED
  207s/passであり、drive_batch28.shのworker当たりtimeout 260ではp2が永遠に完了
  しない。よってpinned runner `runbatch.sh` (`f591f8c2…`・変更なし) を「未完キー
  1個ずつ」`timeout 285`で直接起動するsession-local orchestration
  (`scripts/drive2_local_step.sh`・solver変更なし・2 solver並列上限・odd/even 2
  workers相当・runner内部guard・pre-registered stop rule変更なし) に切り替えた。
  verdict行はすべてrunner自身の記録。
- wave結果: aa004 **EXHAUSTED** (honest UNKNOWN・同条件再probeなし)・aa005
  **EXHAUSTED** (同) → **aa006 WIN (result 1・nodes 14,303,810)・aa007 WIN
  (result 1・nodes 13,483,540)**。両worker rc=45観測で事前登録stop ruleにより
  wave終了。残り47キー (aa008..aa054) はfileless UNPROBEDのまま。
- **row-audit(winhalt) PASS (機械導出)**: probed 7 (aa001..aa007) = WIN 4
  (aa001/aa002/aa006/aa007)・LOSS 1 (aa003)・EXHAUSTED 2 (aa004/aa005)・fragment 0・
  fileless 47・mismatch 0 (byte-pin `96867282…` をdrive-2 dirにそのまま実行・kit
  構造同一のため)。
- tamper battery **4/4検出** (scratch copy上・battery後実験dir全file sha256不変):
  T1' aa006 p1 result 1→2 → p1/p2 row mismatch gate fail (初回T1はsed置換不発動の
  無操作だったため実効性assert込みで再実施)・T2 status.log aa006 nodes+1 →
  WIN-HALT record incomplete fail・T3 seed aa001 status nodes+1 → 同fail・T4 aa003
  raw legal 86→87 → published packet legal不一致fail。
- 出版3コミット (commit-pinned raw URL fetch-back **96/96 byte一致 + MANIFEST
  byte一致**): A scaffold `43a0d55f` (71 files = scripts 8 (7 pinned再利用 +
  session-local orchestration記録) + input 55 + val-gate inputs/baselines 8)・
  B outputs `5c9ee6b3` (24 files = cd2-host outs 4・raw outs 14 (seed 4 + 新規10)・
  truncated sidecars 4・status.log・row-audit json)・C README+MANIFEST `b3c6daf6`。
  実験dir:
  `research/experiments/n11-centralreply-closure-class5343-batch28-drive2-20261123/`。
- 意味 (route statementのみ・verdict不消費): **unconsumed closure WIN候補は33キー**
  (31 prior + aa006/aa007・aa006は32番目・aa007は33番目候補としてhonest記録)。
  aa003 LOSS行はadoption候補のみ (消費は別adoption Part・pinned merger
  `90711961…` 経由のみ)。aa004/aa005 はhonest UNKNOWN (15M同条件再probeなし)。
  canonical cache (`9115be9e` 6,293行) read-only不変。閉鎖・被覆・secured・root
  勝敗の主張はしない。
- 次回以降の候補: (a) batch-28 fileless残り47キー (aa008..aa054) の将来probeは別
  宣言 (Part CF候補・**WIN-CONTINUE事前登録 (Part BT/CA/CE先例) の検討を推奨**:
  class 5343の全子LOSS閉包ルートはaa001/aa002 (第三実装交叉検証済み) で反駁済み
  であり、残余キーの列挙はunknown数最小化目的でWIN-HALT停止の情報価値は小さい)。
  (b) aa006/aa007の第三実装交叉検証 (verifier Part候補)。(c) aa001..aa007 WIN・
  LOSS行のadoption (別adoption Part・pinned merger `90711961…` 経由のみ)。
  (d) batch-29選定はreaudit再実行後 (rank 35 class 2251・rank 36 class 34269が
  zero-collision clean候補)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa001..aa007を
  含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・expansions
  数・wall秒数を勝敗として読まない。WIN/LOSS採用は別adoption Part (pinned merger
  `90711961…` 経由) のみ。
### Part CG 宣言 (2026-11-23): batch-28 drive-2 WIN行 aa006/aa007 第三実装交叉検証 — publish-then-execute

(observed HEAD-before-push: `a8772a049bd3…` (16:26:27Z・K1251 laneの検索実験commit・
noteには不触)。push直前にnote blob sha1ロック `5da4cecddac9bf8e5d6bd11f49e72d96c9825f11`
(614,692 bytes版・Part CD status update適用済み) を再照合し、fail-closed shaで更新する。
対抗宣言なし (note内 Part CG/thirdimpl-drive2win 記述ゼロを機械確認済み)。実験dir
`research/experiments/n11-centralreply-closure-b28drive2win-thirdimpl-20261123/` は
push直前に404を再確認済み。)

- **目的**: Part CD (batch-28 drive-2・class 5343) でpublishされた WIN行2件
  (aa006: replay result 1 nodes 14,303,810 / aa007: replay result 1 nodes
  13,483,540) を第三実装 (third_impl.js `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998`)
  で交叉検証し、本host pinned-replica 2-pass fresh-cold 再現と合わせて
  独立検証可能にする。**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張をしない。
- **事前登録stop rules**: replica MISMATCH (published raw fieldsとのresult/nodes
  不一致) はhard-stop・即時honest記録。third_impl DIVERGENCE (2-run非決定性) や
  WALL-INCONCLUSIVE (cap 300M/expansions wallcap 240 到達) もevidenceとして
  記録するがverdictには変換しない。EXHAUSTEDなし・全target行はfresh-cold 1回ずつ。
- **kit (scripts 6・全件byte-pin)**: third_impl.js `08ea958f…` (published Part CC
  からのpin再利用・一切変更なし)・verify_tbl.js `c8c52528…`・jsreplay.js
  `84585617…` (pinned replica)・run_thirdimpl.sh `a0b77d83…`・make_inputs_cg.py
  `d7155bd9…` (published sources byte-pin再利用・OUTPUT gate済み)・audit_cg.py
  `b326a292…` (published Part CC audit.py `b7cfb0ce…` からのdeltaは
  EXP/SCHEMA/rows-schema文字列とtarget-count gate明細のみ・gate logic不変・
  宣言内で開示)。audit_cg.pyのrules-gate依存はpinned jsreplay (inv path) 経由。
- **input (7 files)**: rows.json `3ef56043…` (schema
  `n11-centralreply-closure-b28drive2win-thirdimpl-input-v1`・targets aa006/aa007
  (lo/hi/legal/s5_index/replica_result 1/replica_nodes)・anchors k02a (expect win
  expansions 9,106,337 ttHits 4,991,527) l1a (expect loss expansions 7,660,602
  ttHits 3,951,175)・negatives ng1 (legal+1改竄) ng2 (stones改竄)) + input CSV 6件
  (make_inputs_cg.pyによるmachine-derived・published Part CD/BF sources byte-pin:
  aa006 `cdd84899…` aa007 `493e0a58…` k02a `b6174a3f…` l1a `e13d2a6c…` ng1
  `8e64b9ad…` ng2 `f19cd5a3…`)。
- **sources (13 files)**: published Part CD canonical outputs (status-cd.log
  `343097c2…`・row-audit-cd.json `3e86a32b…`・batch-keys-cd.json `af19208f…`・
  README-cd.md `338fc136…`・raw aa006.p1 `c9455882…` .p2 `e157a451…` aa007.p1
  `ad2870ea…` .p2 `bbacf3e3…`・published-input aa006 `cdd84899…` aa007
  `493e0a58…`) + published Part BF anchor/negative基底CSV 4件 (byte-pin) +
  published-rows-cc.json `b7222edf…`。
- **val-gate (8 files)**: sanctioned 4キー (at2m×2 budget 2M・15m×2 budget 15M)
  input CSV + published baselines (published pins)。本host fresh 4/4 node-exact
  を実行後確認。
- **実行protocol (宣言後・逐次・1 solver/1 row/1 process)**: (1) rules gate:
  `node scripts/verify_tbl.js` 期待「replica quads 95670 mine quads 95670 / triples
  checked 195044 mismatches 0」。失敗ならhard-stop。(2) val-gate fresh 4本
  (jsreplay --exact-replay・budget 2M/15M) → published baseline node-exact比較。
  (3) negatives: run_thirdimpl.sh ng1/ng2 → 期待GATE_FAIL (rc=1)。(4) anchors:
  k02a/l1a × (a,b) 計4 run → published expansions/ttHits一致。(5) targets
  pinned-replica 2-pass fresh-cold (aa006/aa007 × p1/p2・budget 15M・各~200s) →
  published raw fieldsとnode-exact。(6) targets third_impl 2-run pair
  (aa006/aa007 × (a,b)・cap 300M wallcap 240) → determinism (a==b) と
  published replica_result 1との verdict agreement。
- **監査**: `python3 scripts/audit_cg.py` 3回実行byte一致
  (audit-run1/2/3.txt + audit-summary-run1/2/3.json) と audit-summary.json。
  期待全gate PASS・verdict_agreements 2/2。tamper battery (scratch copy上:
  replica result反転 / raw nodes+1 / input CSV legal改竄 / third_impl pin反転)
  の各fail検出と実験dir byte不変を検証。
- **出版**: A scaffold (scripts 6 + input 7 + sources 13 + val-gate inputs/
  baselines 8) → B outputs (rules-gate.txt + val-gate this-host outs 4 + replica
  4 + negatives 2 + anchors 4 + targets 4 + audit 7 + status.log) → C README +
  MANIFEST-sha256 → note status update。全files commit-pinned raw URL fetch-back
  byte照合・branch path URL (CDN stale) は使わない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa006/aa007を
  含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・expansions
  数・wall秒数を勝敗として読まない。WIN/LOSS採用は別adoption Part (pinned merger
  `90711961…` 経由) のみ。

### Part CH 宣言 (2026-11-23): batch-28 (class 5343) 1-LOSS行 aa003 canonical adoption + re-audit — publish-then-execute

(observed HEAD-before-push: 336481d230aa082078cb2e8cae4318f3aa8edfd3 →
push直前に最新mainを再取得しコミットメッセージにHEADを記録する。push直前にnote
blob sha1ロック 7dbd917a6b392e19949f36aa8d2672651dcb4f0a (620,004 bytes版・Part CG
宣言適用済み) を再照合・fail-closedで更新する。対抗宣言なし (note内 Part CH /
batch-28 adoption / b28loss1 記述ゼロを機械grepで確認済み)。実験dir
`research/experiments/n11-centralreply-class5343-loss1-adoption-reaudit-20261123/` は
push直前に404を再確認済み。)

- **目的**: Part CD (batch-28 drive-2・class 5343) でpublishされた解決済み単一
  LOSS行 aa003 (key `(1152921504741064704, 4228)`, s5 index 104943, result 2,
  nodes 4,070,373, 2-pass node-exact @budget 15M) のみを、Part BZ canonical
  cache (6,293行 `9115be9e…`) に pinned byte-copy fail-closed union merger
  (`90711961…`) 経由で採用する。採用パケットはloss-only 1行であり
  **full != loss**: 同batchの WIN 4行 (aa001/aa002 はPart CC第三実装交叉検証済み・
  aa006/aa007 はPart CG交叉検証レーン宣言済み) はhonest labelのまま不採用
  (verdict不消費・scrutiny owner C++第二実装 gate pin `9193f5b6…` が唯一のWIN
  採用ルート・batch-14residual q042 / batch-26 l028 先例)、EXHAUSTED 2行
  (aa004/aa005・result 0 nodes==budget 15M) はhonest UNKNOWNのまま、fileless
  47キー (aa008..aa054) はUNPROBEDのまま。閉鎖・被覆・secured・root勝敗の主張を
  しない。
- **正直開示 (protocol偏移)**: 本セッションはdry-run準備から開始したため、
  本amendmentの出版前にadopted packet・gate定数・期待機械簿記の導出を本hostで
  実施済みである。publish-then-executeの実質 (スコープの事前固定・事後の
  cherry-pick不可能性) は、本宣言に固定する (a) 実験dir構成、(b) 入力sha pin群、
  (c) 採用行 (aa003単行) と不採用集合 (WIN 4・EXHAUSTED 2・fileless 47)、
  (d) 期待機械簿記 (下記) のすべてを事前登録することで担保する。出版される
  outputsはこれら宣言値とのbyte一致をfetch-back照合で機械検証する。宣言後に
  実行するのは、(A)-(E)出版とnote status updateである。
- **入力 (全件byte-pin)**: published batch-28 drive-2 kit 96 files (dir
  MANIFEST-sha256.txt `2811b577…`), status.log `343097c2…` (17行),
  row-audit-winhalt.json `3e86a32b…` (probed 7 = WIN 4 + LOSS 1 + EXHAUSTED 2
  + fileless 47), BASE cache 6,293行 `9115be9e…`, Part BZ reaudit outputs
  (refresh-summary `fca242cc…`, closure-classes.csv `14fc37c3…`,
  per-root-coverage.csv `4218a6b4…`), pinned merger `s5_union_merge.py`
  `90711961…` (Part BZ正本・変更なし), dependency-graph.json.gz `54f9c364…`,
  repaired-joint-plan-update8.json `b658290a…`, independent.py `954d3a10…`,
  s5_evidence_policy.py `78655e94…`, quarantine `81d23160…`。
- **実行protocol (本セッションで機械実施済み・出版は宣言後)**:
  (1) maker `make_increments_b28loss1.py` (kit 96/96 sha検証・status.log 17行
  構造gate (WIN-HALT 4ペア+EXHAUSTED 2ペア+TRUNCATED-RETRY 4行 sidecar
  absence gate)・aa003 2-pass node-exact・WIN 4行/EXHAUSTED 2行の
  NOT-emitted gate・zero BASE overlap・quarantine 0) → increment 1行
  `dc857bfd…` + manifest `017c7c30…` (schema `b28loss1-increments-manifest-v1`・
  `full_packet_eq_loss_only` false)。x4 byte-stable。
  (2) merger selftest PASS → BASE+increment merge x3 byte一致 (merge-audit
  run1/2/3同一 `5e8d6909…`) → merged 6,294行 `3124461b…` (WIN 158 /
  LOSS 6,136)。
  (3) refresh `refresh_adoption_b28loss1.py` (Part BZ版 `0677e6eb…` からのdeltaは
  CACHE path・CACHE_SHA_EXPECTED・docstringのみ) x3 + 隔離実行 (env -i・別tree)
  byte一致 → refresh-summary `76cad2a1…` / closure-classes `baa2db13…` /
  per-root-coverage `75e59441…` (+ probe-worklistはregenerateするが「worklist
  not published by design」(BZ先例) により出版しない)。
  (4) extractor `compare_deltas_b28loss1_adoption.py` (Part BZ版 `a3adc0da…`
  からのdeltaは1-batch/1-adopted-row/4-WIN/2-EXHAUSTED/0-fragment構造への適応
  のみ・gate logic設計はBZ先例継承・11 sha pin + manifest semantic gates +
  probed 7キー独立2-pass再検証 + closure churn rank機械宣言 CHURN_RANK_EXPECT +
  update8 delta=={104943} gate込み) x4 + 隔離実行 byte一致 →
  decomp-deltas `975a9cc6…`。
- **期待機械簿記 (事前登録)**: class 5343 unknown_now 54→53 (rank 27→19・
  rank 19..26クラス {5687, 12643, 31600, 10968, 23964, 25835, 30565, 5690} の
  +1シフトは純粋なranking bookkeeping。closure table membershipは不変
  left=[]/entered=[]・anchor 23101/1849 (unknown_now 1/1) rank不変)・
  excluded_now flips=[]・newly_free=[] (loss-only 1行はBASE未知コスト子全解決
  クラスのみfree化しうるが該当なし・**class 5343はWIN 4行不採用+EXHAUSTED 2行
  +fileless 47キーが残るためfree化しない**)・free_now 38→38・update8 resolved
  133→134 (新規解決集合=={104943}のみ)・joint greedy 38,295不変・probe worklist
  64,747→64,746・per-root free/uncovered不変 (root 27 baseline 119/119含む)・
  individual greedy union movers roots {4, 49} (root 4: 5978→5977, root 49:
  2811→2810)。
- **tamper battery (scratch tree上・12/12検出 + restoration green)**: pin層
  (increment sha / status.log sha (maker) / BASE cache sha / batch-keys sha /
  raw tamper→maker kit MANIFEST sha gate) と、攻撃者がpin定数を書き換えた場合の
  semantic層 (verdict反転 2→1→「non-LOSS verdict」gate・BASE append→
  「scenario cache row count != BASE + 1」gate・batch-keys class_index反転→
  row-audit picture disagreement gate・manifestはunpinnedのためWIN行nodes+1 /
  full!=loss反転 / resolved_ids欠落がsemantic gateで直接検出・extractorの独立
  2-pass raw mismatch表示を含む) の兩層を実効性assert込みで検証。battery後に
  pristine restoreでmaker/extractorともgreen。
- **出版 (宣言後・順次)**: A scripts (make_increments_b28loss1.py `1a79f5a6…` +
  s5_union_merge.py `90711961…` + compare_deltas_b28loss1_adoption.py
  `86fbc570…` + reaudit/scripts/refresh_adoption_b28loss1.py `729ef020…`) →
  B outputs (increment `dc857bfd…` + increments-manifest `017c7c30…` +
  merge-audit-run1/2/3 `5e8d6909…` ×3 + merged cache 6,294行 `3124461b…` +
  reaudit 3出力 + decomp-deltas `975a9cc6…`) → C README + MANIFEST-sha256 →
  note status update。全files commit-pinned raw URL fetch-back byte照合・
  branch path URL (CDN stale) は使わない。
- **不接触**: Part CG (batch-28 drive2win thirdimpl・並走所有) の実験dir・
  outputs・進行、batch-28 drive-2 published dir (不変)・batch 1..27各published
  dir (不変)、fast lane (y=23)・finite-field lane (K1254)・inversive/z19 lanes、
  19root計画、unconsumed closure WIN候補33キーの採用状態、BASE cache
  (`9115be9e…`) read-only不変 (merge先は新規別名cacheとしてのみ出版)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa001..aa007を
  含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数を勝敗として
  読まない。WIN採用は引き続きscrutiny owner C++第二実装 gate (`9193f5b6…`) のみ
  (本レーンは代行しない)。本Partはloss-only 1行のcanonical adoptionであり
  class 5343の閉鎖・root被覆・securedの主張を一切しない。
