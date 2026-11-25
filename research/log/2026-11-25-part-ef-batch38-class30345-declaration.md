# Part EF 単一オーナー宣言 (2026-11-25): batch-38 — closure class 30345 (rank 12) fresh 49キー probe (publish-then-execute)

単一オーナー: n11中央応答 長期レーン (本セッション・Part EE wave Fと同一レーンの別hourly実行)。
対抗宣言なし: 着手前に最新mainを再取得し (observed HEAD `dda65bbb` =
Part EE wave F second-environment verification log・2026-11-25T06:18:03Z)、機械grepで
batch-38 / Part EF / class 30345 の新規probeを主張するcommit・宣言・実験dirがないことを確認
(search_commits: "batch-38" 0件・"Part EF" 0件・"class 30345" を含むcommitは Part EE wave F
docs/addendumの2件 `10fbf47e`/`d19b5ca4` (fresh frontier rank 12 の指摘と読み替え訂正) のみ)。
push時にもHEADを再取得して同一チェックを実施する。並走hourly実行との同時着手はpush競合
チェックが防ぐ。

## 1. レジューム経緯と選定根拠

Part EE (af034loss1 canonical adoption + wave F reaudit) は同一レーンの先行hourly実行で
完走済み (canonical merged chain 6,666 s5verdict行 `fc3e4ac9…`・closure表807行
`27e00b0d…`・refresh-summary `6af660a1…`・per-root-coverage `6974299b…`・probe-worklist
regen pin `b4933810…`)。Part EE wave F addendum (`d19b5ca4`) は closure rank 1..10 の残
81 unknown子が全部 prior-packet probe-level WIN行 (fresh 0) であることを機械確定し、
**fresh frontierはrank 12 class 30345から**と訂正出版した。本実行はその指摘どおりの
最初のfresh batchである。

本宣言前探査でrank 11までの選定ゲートを機械再確認した (worklist regen × prior-probe
universe × canonical cache の3方向交叉):

- **rank 11 class 13342の50 unknown子も全て prior-probe universe内** (fresh 0・cache-hit 0)。
  よって **rank 1..11 (classes 23101, 1849, 2251, 16371, 16757, 5804, 34908, 20421, 34269,
  5343, 13342) の残131 unknown子はすべて prior-probe universe内 (fresh 0)** で、
  同一条件の新規probeでは1行も開けない (既存honest labelは scrutiny/adoption経路専権)。
- **rank 12 class 30345** (`[1152922604118478848, 65536]`・unknown_now 50): 50子のうち
  - **1子は prior-packet**: pair (1153204079095189504, 65536) = s5 index 528497 =
    **batch-1 (class 16757 packet, 2026-11-22) の b018** (probed honest-label WIN
    PASS `15000000,1,3549602` + 事前登録WIN-HALT marker行)。verdictは未消費
    (canonical chain不在・機械照合済み)。batchにおけるprobe-level WINはscrutiny owner C++
    第二実装 gate (`9193f5b6…`) 通過後のみ採用可のため、同一条件 (15M) の再probeは禁止
    (2026-11-22の IF-ADOPTED分析 commit `aea7abcb` でも 16557/30345/15640 のブロッカー
    として言及済み)。**batch-38 targetから除外**する。
  - **49子は fresh**: canonical cache 0/50 (pair-level)・prior-probe universe 0/49・
    quarantine active 0/50 (いずれも機械照合)。

## 2. prior-probe universe (本batch固有の新規機械資産)

「fresh」判定の根拠を反復可能にするため、本セッションは**過去の全n11 probeが実際に
判定を与えた (lo,hi) 位置の全体集合**をpublished bytesから再構築した:

- 収集範囲: 発表済み keys-json/reprobe-keys 85ファイル (batch-1..37の全packet宇宙
  1,717 keys)・全n11実験dirのabstract input csv 3,474件 (うち `target,` 行から(lo,hi)抽出)、
  night-batch1..5・adaptive・conflict-closure系のearly-era inputs 24件、全n11パスの
  s5-index/lo-hi埋め込み掃引、s5-direct-15m.gz。
- **結果: 2,104 unique (lo,hi) pairs**。昇順 `"lo,hi\n"` 1行1pair・headerなしで直列化した
  **sha256 `6deee846a4e67778437cd052502535f4839f3fbe76d5e1ec9bc9b6c0036e942b`**
  (53,595 bytes) を `prior-probe-universe.csv` としてkitのsourcesに出版しmakerがpin検証する
  (再構築経路は上記収集範囲のpublished bytes限定・本実行のlogに手順を記録)。
- class 30345の50子との交差は**ちょうど1件** (b018 pair)。rank 1..12全部門の
  prior/fresh交叉表は `freshness-ranks1to12.csv` (sha256 `e5f51717…`) として出版し、
  maker G3bがfail-closed検証する。

## 3. 宣言前探査 (read-only・全開示・solver未実行)

1. **本環境でのrefresh原実行 byte再現 (Part DY宣言前探査と同一手法)**: Part EE出版の
   refresh fork `refresh_adoption_ee.py` (`01937f23…`) と全pinned入力 (graph
   `54f9c364…` / update8 receipts / independent.py `954d3a10…` / policy `78655e94…` /
   quarantine `81d23160…` / merged cache `fc3e4ac9…`) を本セッション環境に再fetchして
   原実行し、**4出力すべて出版bytesとsha256完全一致** (probe-worklist.csv regen pin
   `b4933810…`・closure-classes `27e00b0d…`・refresh-summary `6af660a1…`・
   per-root-coverage `6974299b…`)。
2. **worklist extract**: regen worklistから class 30345の50行を抽出 (probe_order 132..181
   連続・全行serving_class 30345・class_unknown_now 50)。`worklist-class30345-extract.csv`
   (sha256 `7fe55513…`・3,000 bytes) として出版。worklist本体 (~4MB) はregen pin
   `b4933810…` で再現を担保 (Part DW/DX/DYと同一運用)。
3. **batch-1 packet pins再取得**: batch-keys.json `2aaccc94…` (48キー b001..b048)・
   status.log `559a0884…` (b018 PASS `15000000,1,3549602` + b018 WIN-HALT行) を
   rawから再fetch・sha照合 (b018 rowのlo/hi/legal/s5/membershipはextract行140と全字段一致)。
4. **canonical cache pair-level parse**: 6,666 s5verdict行に対しclass 30345の50子の
   exact pairは0件 (same-lo行は文脈計数のみ・採用しない)。b018 pairも不在 (未消費WINの
   裏付け)。
5. **quarantine registry** `81d23160…`: active 2エントリ。50子のpairはいずれも非衝突。
6. **maker (make_batch38_keys.py・sha256 `9b117808…`・batch-37 published maker `2c2c8c3a…`
   からのfork)**: lifecycle上、**宣言前に3回実行して全gates PASS・3回byte-identical**
   (inputs 49ファイル + batch-keys-b38.json `29807104…` 全sha一貫)。**tamper battery
   10/10 fail-closed + control PASS**:
   T1 cache byte反転 (pin層G1) / T2b b018 lo drift + re-pin (G2) / T3b b018 nodes drift +
   re-pin (G2) / T4 ai001 pair cache命中 + re-pin (G4) / T5 ai001 pair quarantine活性化 +
   re-pin (G5) / T6 closure rank 12行class drift + re-pin (G3) / T7 extract ai001 legal drift +
   re-pin (G6) / T8 universe b018 1行削除 + re-pin (G7: 行数gateがfirst-fire) /
   T9 freshness rank-12 fresh 48化 + re-pin (G3b) / T10 extract prior b018 legal drift +
   re-pin (G6: 行構造崩れをG6行数gateが捕捉)・全ABORT・battery後にcontrol rc=0。
   batch-37のT2b/T4等の「変異適用を各stepでassert」規約はbattery.py内で実施。
7. 本宣言時点で本セッションは **solver (jsreplay) を一度も実行していない**。
   (選定ゲート・makerはsolver不使用。val-gate fresh・probe は宣言後のみ。)
8. **freshness gate (prefix衝突)**: 発表済み全packet 85 keys-jsonに key-id prefix
   「ai」は存在しない (機械走査・`ad001..ad055` (batch-31) / `af001..` (batch-32/33) /
   `ag001..` (batch-34) / `ah001..` (batch-35)/`d005..d049`(batch-36)/e系 (batch-37) 以外
   の新しいprefix)。batch-38 key idsは **ai001..ai049** (worklist probe_order順: 132..139,
   141..181・probe_order 140はb018のため欠番)。

## 4. スコープ・手法

実験dir: `research/experiments/n11-centralreply-closure-class30345-batch38-20261125/`。

- 手法: pinned runner `runbatch.sh` (sha256 `f591f8c2…`・batch-31..37 kitとbyte-clone) +
  pinned replica `jsreplay.js` (sha256 `84585617…`・byte-clone)。2-pass fresh-cold
  replay・budget 15,000,000・1 solver / 1 row / 1 process・drive順 = worklist probe_order
  (= ai001..ai049) で逐次実行 (本環境は2-core・並列2 solverまで)。
- maker gates G1..G7 (fail-closed・宣言前検証済み):
  - G1 sources sha pins (9ファイル: batch1-packet 2 + refresh-summary + closure-classes +
    canonical cache + quarantine + worklist extract + prior-probe-universe + freshness表)
  - G2 batch-1 packet完全性 (48キー b001..b048・b018行全字段照合・status PASS行
    `15000000,1,3549602` + WIN-HALT行)
  - G3 closure-classes rank 12 == class 30345・unknown_now 50 == 1 (prior) + 49 (fresh)
    accounting・mask照合
  - G3b freshness表 rank 1..11 fresh-0 + rank 12 (prior 1・fresh 49) とclosure表rank対応
  - G4 49 target pair + b018 pairがcanonical cacheに全て不在 (pair-level・same-lo文脈計数のみ)
  - G5 50 pairすべてquarantine activeでない
  - G6 worklist extract 50行 = probe_order 132..181連続・全字段一致・b018行はorder 140に
    在位・target probe_order単調増加 (legalはjsreplay実行時にも独立再導出され mismatchで
    hard-fail)
  - G7 prior-probe universe 2,104行昇順unique・49 targetは全てuniverse外 (freshness)・
    b018 pairはuniverse内
- **停止規則 (事前登録)**:
  1. determinism mismatch → runner HARD-STOP (rc=42)、以後のキー着手不可。
  2. WIN (result 1) → per-key pre-registered honest WIN-HALT marker行 (rc=45)・
     **drive-level WIN-CONTINUE**: 残り全キーを継続 (batch-35/36実績と同一運用・全49キーを
     honest labelする)。WIN行のverdictは一切不消費 (scrutiny owner C++第二実装 gate
     `9193f5b6…` 通過後のみ採用可・本実行環境にC++コンパイラなし・Part G/DU/DX/DYと同一の
     既知障害)。
  3. EXHAUSTED (result 0) → honest UNKNOWN・同一条件 (15M) の再探索は行わない。
     高budget再probeは別宣言・新runner sha (BUDGET変更) が必須。
  4. timeout・環境resetでTRUNCATEDになったpass fileはverdictでない・runnerの
     `# replay_done` guardでfresh再実行 (truncated passは完走EXHAUSTED行の
     no-re-search規則に触れない)。
- val-gate (宣言後にfresh実行・published baseline 4 moleculeとnode-exact一致が必須):
  batch-31 kit出版の4行 (input + published-baseline byte-clone出版):
  `at2m-s5-1152921504606851072-536870946` (budget 2,000,000・result 0・nodes 2,000,000) ・
  `at2m-s5-1188950301626860544-536870912` (2,000,000・0・2,000,000) ・
  `first-15m-s5-1152921504606851072-536870946` (15,000,000・2・3,651,923) ・
  `second-15m-s5-1188950301626860544-536870912` (15,000,000・2・5,040,200)。
  本host fresh 4/4 (sidecar `.b38-host.out`・wall_s以外全field一致) をdrive開始要件とする
  (不一致ならhard-stop)。
- drive: `drive38_local_step.sh` (sha256 `2bd91341…`・batch-31 drive-1 `26347816…` からの
  fork・key-id regex ad→ai差し替え + WIN-CONTINUE化 (WAVE-HALT 2 block削除)・worker設計
  `timeout 260` wrap・1 invocation最大2キー×2 worker・`if rem` empty-key guardはそのまま)。
- 出版: raw 8キーごとのincrement wave (Part DS ④(a)の教訓・sandbox reset耐性)・
  append-only status.log・batch-audit機械集計・README・MANIFEST-sha256 (self-exclusion規約)・
  完了log。本batch単独ではverdictを1行も消費しない (adoptionは別Part・pinned
  fail-closed merger `90711961…` 専権・WIN行はscrutiny owner C++ gate待ち)。
- probe結果によって class 30345 の unknown_now 50から減算される (LOSS/EXHAUSTED
  いずれも・reauditが導出)。closure table membership変動はprobe完了後のreauditが機械導出
  する。本宣言は結果非予告であり、いかなる勝敗も宣言しない。EXHAUSTEDも出る可能性を
  事前登録する。nodes数はbookkeepingであり勝敗ではない。

## 5. UNKNOWN担保・不接触

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 30345 (batch-38の全キーを含む) は本Partの実行・出版のどの時点でも
UNKNOWNのまま。** nodes数・wall秒数を勝敗や距離として読まない。被覆・閉鎖・secured
coverage・root勝敗の主張は一切しない。WIN採用は scrutiny owner C++ gate `9193f5b6…`
通過後の別adoption Part (pinned merger `90711961…` 経由) のみで、本レーンは代行しない。
b018 (probe-level unconsumed WIN) の採用可否は本batchのスコープ外。

- canonical merged chain `fc3e4ac9…` (6,666行) はread-only不変 (本driveはcanonical cacheに
  一切書き込まない)。
- batch 1..37各published dir (不変)・Part EE reaudit出版物 read-only不接触。
- b018行scrutiny (C++ `9193f5b6…` 専権)・rank 1..11のprior-packeted label群の
  adoption経路・19root計画・fast lane・finite-field lane・inversive lane。
