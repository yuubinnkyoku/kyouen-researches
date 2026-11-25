# Part EH 単一オーナー宣言 (2026-11-25): batch-39 — closure class 30484 (rank 20) fresh 50キー probe (publish-then-execute)

単一オーナー: n11中央応答 長期レーン (本セッション・Part EE wave F検証と同一レーンの別hourly実行)。
対抗宣言なし: 着手前に最新mainを再取得し (observed HEAD `e8ff04e3` =
K0684 rooted-core same-K evidence update・2026-11-25T09:28:53Z)、機械検索で
batch-39 / Part EH / class 30484 の新規probe・宣言・実験dirを主張するcommitが
ないことを確認 (commit走査: "batch-39" 0件・"Part EH" 0件・"30484" を含む
commit 0件・code search "aj001" 0件)。push時にもHEADを再取得して同一チェックを
実施する。並走hourly実行との同時着手はpush競合チェックが防ぐ。

## 1. レジューム経緯と選定根拠

Part EF (batch-38, closure class 30345 rank 12) は別hourly実行が単一オーナーと
してin-flightである (inc1..inc5出版済み・ai001..ai043・本宣言時点でinc6待ち)。
Part EG (class 34908 b33-win-6 第三実装交叉検証) も別実行が宣言・kit出版済みで
所有中。本実行はこれらに触れず、**fresh frontierの次段 (rank 13..20 scan)** を
機械導出して最初の未所有fresh batchを開く。

本宣言前探査でrank 12まで (Part EF freshness-ranks1to12.csv `e5f51717…`) に
続く選定ゲートをrank 20まで機械拡張した (worklist regen × prior-probe universe
× canonical cache × quarantine の4方向交叉):

- **rank 13..19 (classes 12264, 5473, 16957, 2634, 8785, 1518, 8106) の残
  unknown 51..52子はすべて prior-probe universe内 (fresh 0・cache-hit 0・
  quarantine 0)**。よって rank 1..19 の残unknown子は (b38 claim-reserved 2子を
  除き) すべて既probe位置で、同一条件の新規probeでは開けない。
- **rank 20 class 30484** (`[1152922604135251968, 65536]`・unknown_now 52):
  50行がworklist probe_order 540..591連続。交叉の結果:
  - **52子はすべて universe外 (fresh 52・cache hit 0・quarantine 0)**。
  - **ただし2子が in-flight Part EF の宣言済み target と pair 同一**:
    worklist probe_order 585 = pair (1152922604135256064, 65536) = **batch-38
    ai044** (b38 probe_order 176) / probe_order 586 = pair (1152921573327372288,
    68157440) = **batch-38 ai048** (b38 probe_order 180)。いずれも dual-class
    (30345/30484) children・membership_class_count 3。batch-38 は別レーンの
    単一オーナー宣言による in-flight probe であり・その honest label は unconsumed・
    verdict は EF 実行→adoption 経路が所有する。**同一条件 (15M) の再probeは
    所有権侵害となるため batch-39 target から除外する (claim-reserved 2子)**。
    この交差は published batch-keys-b38.json (`29807104…`・49キー) と
    worklist extract の機械 set-intersection で導出し、maker G2/G6/G7 が実行時
    に再検証する。
  - **残50子が batch-39 targets aj001..aj050** (worklist probe_order 540..584,
    587..591・probe_order順 = aj id順)。

新規機械資産 (本session生成・kit sourcesに出版・maker G1/G3bがpin検証):
- `freshness-ranks13to20.csv` sha256
  `deea05b82a391f5e7d5809c08e2b8c77bc5007cc9ccefab55cee259f65d52b54` (239 bytes):
  rank 13..19 all-prior/fresh-0 行 + rank 20 (children 52 / prior 0 / cache_hit 0 /
  fresh 52)。EFの freshness-ranks1to12 と同一 schema・同一 pinned 入力基盤。
- `worklist-class30484-extract.csv` sha256
  `feda8c7295ec6d17562f786eae9f48c59e7d701fd13748ea655b8bbdb7ea33d0` (3,105 bytes):
  class 30484 の52行 (probe_order 540..591連続・全行serving_class 30484・
  class_unknown_now 52)。

## 2. 宣言前探査 (read-only・全開示・solver未実行)

1. **本環境でのrefresh原実行 byte再現 (Part EF宣言前探査と同一手法・同一入力)**:
   Part EE出版の refresh fork `refresh_adoption_ee.py` (`01937f23…`) と全pinned
   入力 (graph `54f9c364…` 16,114,706B / update8 receipts / independent.py
   `954d3a10…` / policy `78655e94…` / quarantine `81d23160…` / merged cache
   `fc3e4ac9…`) を本session環境にraw fetchして原実行し、**4出力すべて出版bytesと
   sha256完全一致** (probe-worklist.csv regen pin `b4933810` 3,724,115B (非出版)・
   closure-classes `27e00b0d` (35,951B)・refresh-summary `6af660a1` (32,765B)・
   per-root-coverage `6974299b`)。extract・freshness表はこの regen worklist から
   逐次生成した。
2. **universe交叉**: Part EF出版の prior-probe-universe.csv (`6deee846`・2,104
   pairs) をbyte再取得 (sha一致) して交叉に使用。batch-38 target 49 pair と
   class 30484 extract 52 pair の set-intersection がちょうど2件 (ai044/ai048)
   であることを機械確認 (G2で実行時再検証)。
3. **canonical cache pair-level parse**: 6,666 s5verdict行に対しclass 30484の
   52子の exact pair は0件 (creator b39 内の same-lo 文脈計数は aj007/aj008/
   aj012/aj014/aj016/aj020/aj023 の7行が same-lo 1 のみ)。
4. **quarantine registry** `81d23160`: active 2エントリ。52子のpairはいずれも
   非衝突。
5. **maker (make_batch39_keys.py・sha256 `425329c0…`・batch-38 published maker
   `9b117808…` からのfork・deltaはdocstring宣言どおり)**: lifecycle上、**宣言前に
   3回実行して全gates PASS・3回byte-identical** (inputs 51ファイル + batch-keys-b39.json
   `5e25b550…` 全sha一貫)。**tamper battery 10/10 fail-closed + control PASS**:
   T1 cache byte反転 (pin層G1) / T2b b38 packet ai044 lo drift + re-pin (G2) /
   T3b b38 packet ai048 legal drift + re-pin (G2) / T4 aj001 pair cache命中 +
   re-pin (G4) / T5 aj001 pair quarantine活性化 + re-pin (G5) / T6 closure rank 20行
   class drift + re-pin (G3) / T7 extract aj001 legal drift + re-pin (G6) /
   T8 universe aj001 pair追記 + count緩和 + re-pin (G7 semantic target-hit) /
   T9 freshness rank-20 fresh 52→50 + re-pin (G3b) / T10 extract claim-reserved行
   legal drift + re-pin (G6)・全ABORT rc=1・battery後に control rc=0・出版kit
   sourcesは事后 pristine 照合 (sha全一致)。
6. 本宣言時点で本セッションは **solver (jsreplay) を一度も実行していない**。
   (選定ゲート・makerはsolver不使用。val-gate fresh・probe は宣言後のみ。)
7. **key-id prefix衝突gate**: code search "aj001" 0件・既存発表済みpacketの
   key-id prefixは b/ad/af/ag/ah/d/e/ai 系のみで「aj」は未使用 (機械走査)。
   batch-39 key idsは **aj001..aj050**。

## 3. スコープ・手法

実験dir: `research/experiments/n11-centralreply-closure-class30484-batch39-20261125/`。

- 手法: pinned runner `runbatch.sh` (sha256 `f591f8c2…`・batch-31..38 kitとbyte-clone) +
  pinned replica `jsreplay.js` (sha256 `84585617…`・byte-clone)。2-pass fresh-cold
  replay・budget 15,000,000・1 solver / 1 row / 1 process・drive順 = worklist
  probe_order (= aj001..aj050) で逐次実行 (本環境は2-core・並列2 solverまで)。
- drive: `drive39_local_step.sh` (sha256 `49ec1dd5…`・batch-38 drive-38 `2bd91341…`
  からのfork・key-id regex ai→aj差し替え (4 spots) + batch-keys json b38→b39。
  WIN-CONTINUE設計・timeout 260 wrap・1 invocation最大2キー×2 workerはそのまま)。
- maker gates G1..G7 (fail-closed・宣言前検証済み・内容はdocstring・G2 = b38
  packet claim-reserved provenance・G3b = freshness ranks 13..20)。
- **停止規則 (事前登録・Part EFと同一)**:
  1. determinism mismatch → runner HARD-STOP (rc=42)、以後のキー着手不可。
  2. WIN (result 1) → per-key pre-registered honest WIN-HALT marker行 (rc=45)・
     drive-level WIN-CONTINUE: 残り全キーを継続。WIN行のverdictは一切不消費
     (scrutiny owner C++第二実装 gate `9193f5b6…` 通過後のみ採用可・本実行環境
     にC++コンパイラなし)。
  3. EXHAUSTED (result 0) → honest UNKNOWN・同一条件 (15M) の再探索は行わない。
     高budget再probeは別宣言・新runner sha必須。
  4. timeout・環境resetでTRUNCATEDになったpass fileはverdictでない・runnerの
     `# replay_done` guardでfresh再実行。
- val-gate (宣言後にfresh実行・published baseline 4 moleculeとnode-exact一致が必須):
  batch-38 kitと同一の4行 (input + published-baseline byte-clone出版・shaは
  batch-38 kitと同一): `at2m-s5-1152921504606851072-536870946` (budget 2,000,000・
  result 0・nodes 2,000,000) ・ `at2m-s5-1188950301626860544-536870912` (2,000,000・
  0・2,000,000) ・ `first-15m-s5-1152921504606851072-536870946` (15,000,000・2・
  3,651,923) ・ `second-15m-s5-1188950301626860544-536870912` (15,000,000・2・
  5,040,200)。本host fresh 4/4 (sidecar `.b39-host.out`・wall_s以外全field一致) を
  drive開始要件とする (不一致ならhard-stop)。
- 出版: raw 8キーごとのincrement wave・append-only status.log・batch-audit機械集計・
  README・MANIFEST-sha256 (self-exclusion規約)・完了log。本batch単独ではverdictを
  1行も消費しない (LOSS行のadoptionは別Part・pinned fail-closed merger `90711961…`
  専権・WIN行はscrutiny owner C++ gate待ち)。
- probe結果によって class 30484 の unknown_now 52から減算される (LOSS/EXHAUSTED
  いずれも・reaudit導出待ち)。claim-reserved 2子 (ai044/ai048) の結果はPart EFの
  側で報告され・class 30484 の子としての取扱はadoption reauditが導出する。本宣言は
  結果非予告であり、いかなる勝敗も宣言しない。EXHAUSTEDも出る可能性を事前登録する。
  nodes数はbookkeepingであり勝敗ではない。

## 4. UNKNOWN担保・不接触

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 30484 (batch-39の全キーを含む) は本Partの実行・出版のどの
時点でもUNKNOWNのまま。** nodes数・wall秒数を勝敗や距離として読まない。被覆・
閉鎖・secured coverage・root勝敗の主張は一切しない。

- canonical merged chain `fc3e4ac9…` (6,666行) はread-only不変 (本driveはcanonical
  cacheに一切書き込まない)。
- batch 1..38各published dir (不変)・Part EE/EF/EG出版物 read-only不接触。
  Part EF (batch-38 drive)・Part EG (第三実装交叉検証)・K1316 (z=12 predecl)・
  rooted-core lane は別オーナー・一切触れない。
- ai044/ai048 (claim-reserved dual-class children) の再probeは行わない。
  b018・rank 1..19のprior label群のadoption経路・19root計画・fast lane・
  finite-field lane・inversive lane。
