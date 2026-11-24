# Part CP batch-30 (closure class 34269) drive-3 declaration — 単一オーナー宣言 (publish-then-execute)

Part CP takeover drive-2 完了log (`d2bf9e74`・research/log/2026-11-24-part-cp-takeover-batch30-drive2.md)
のレジューム節どおり、**残25キー ac030..ac054 (fileless UNPROBED)** のprobeを
本宣言で開始する。**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張はしない。
**標準11×11は本driveのどの時点でもUNKNOWNのまま**。

## 対象・実行条件 (drive-1/2と同一)

- batch: research/experiments/n11-centralreply-closure-class34269-batch30-20261123/
  (input/batch-keys.json `79fbd166…`・54キー ac001..ac054・budget 15,000,000)。
- pinned runner不変: scripts/runbatch.sh `f591f8c2…` (byte-clone)・
  scripts/jsreplay.js `84585617…` (byte-clone)。2-pass fresh-cold・
  node-exact PASS要件・`# replay_done`ガード・TRUNCATED-RETRY設計すべて不変。
- WIN-CONTINUE (rc=45は当該キー単位のみでwave継続)・EXHAUSTED (result 0) は
  honest UNKNOWNで継続。pre-registered stop rules: WIN rc=45・MISMATCH rc=42・
  p1/p2 fail rc=43/44 (pinned runner内・drive-1宣言 `189a2e8e` と同一)。

## session script v3 (事前登録)

- scripts/drive3_local_step.sh sha256
  `41c5719c8253a9e199786e5fd87e70cc71ba85e22b3b80249df2082964a2f6c1`
  (本宣言のA′ commitで出版後にfetch-back照合する)。
- published drive-2 script `466f475f…` からの最小delta 3点のみ:
  1. **incident-aware MISMATCH check**: status.logに既に存在する drive-2の
     2 incident行 (後述) ではHARD-STOPしない。HARD-STOP発火条件は
     (a) p1・p2両値とも非空のMISMATCH行 (real determinism divergence) または
     (b) 空p2 MISMATCH行が3行以上 (新規racing artifact)。それ以外の行ではHARD-STOPせず継続する。
  2. **flock単一オーケストレータガード**: `.drive3.lock` を排他取得。
     他step実行中は rc=46 LOCK-BUSY (retryable・hard-stopではなく待機か再実行)。
  3. **orphan-livenessガード**: 実worker起動形
     `bash scripts/runbatch.sh acNNN` (timeout(1)背後含む) に一致する
     /proc/cmdlineを持つ存続プロセスがstep開始時に存在する場合
     rc=47 ORPHAN-DETECTED で何も起動せず終了 (retryable・hard-stopではない)。
     マッチパターンはbash-tool wrapperの自己マッチ (cmdlineに文言を含む)
     を排除するため意図的に狭い。unit test済み: flockガード rc=46動作・
     wrapper偽陽性0・現時点で孤立worker 0。
- それ以外 (done-set推に基づく残キー算出・2キー x 2 worker wave・
  `timeout 260`内側ラップ・外側290s前に必ず発火・空キーガード) は
  `466f475f…` から不変。

## drive-2 incident行のindex化 (事前登録・verdict不消費の維持)

status.log (44行・publish済み `9f754b3d`/C `8e1a0b9b`) のうち drive-2の
Koyeb zombie-race由来の4行を以下のとおりindex化する:

- incident行1: `2026-11-24T02:17:46Z ac028 MISMATCH p1=15000000,2,5087946 p2=`
  (p2空 = mid-write読取artifact)
- incident行2: `2026-11-24T02:19:25Z ac029 MISMATCH p1=15000000,2,9204933 p2=`
  (同上)
- artifact行1: `2026-11-24T02:16:52Z ac029 P1-TRUNCATED-RETRY`
- artifact行2: `2026-11-24T02:16:52Z ac028 P2-TRUNCATED-RETRY`

機械判定 (完了log§誠実記録2と同一): 3独立書込みattemptの節点数完全一致
(ac028: 5,087,946 x3 / ac029: 9,204,933 x3)・値レベルdivergence不在・
最終4 fileはcomplete pair (`# replay_done`付・p1/p2一致)。

**ac028/ac029の取り扱い (本宣言の決定)**: publish済みのcomplete pairをそのまま
incident-area evidenceとして採用 (verdict不消費のまま)・**fresh再probeは
行わない**。理由: (a) 3独立attemptの一致以上の情報を単一writerの再実行が
上回るのはlabel確定のみであり、採用はscrutiny owner C++ gate (`9193f5b6…`)
通過後の別adoption Part専権 (本レーンは行使しない)・(b) node一致が
既に3観測で確定しており、再計算は同じ条件下では同一結果しか生成しない
(pinned runnerの決定性)・(c) 計算資源は残25キーに集中する。

## val-gate (宣言後・本host fresh実行)

- published baselines 4 (at2m x2・first-15m・second-15m) に対し
  takeover-host fresh 4を実行し node-exact (4/4) を出発点とする
  (sidecar `.d3t-host.out` x4をA′ commitで出版)。不一致ならhard-stop
  (drive-1/2規約と同一)。

## 出版計画

1. A′: session script v3 + val-gate sidecar 4 (本宣言後)。
2. B checkpoints: waves完了分のraw p1/p2 + status.log (append-only)・
   適宜に分割出版 (2-3 checkpoint想定)。
3. C: README drive-3節追記 + MANIFEST-sha256拡張。
4. 完了log: research/log/2026-11-24-part-cp-batch30-drive3.md。

drive-2完了logに記載の失敗様式 (bash外側300s超過・Koyeb孤児) に対し、
本宣言の v3ガード (flock・orphan・incident-aware) で対処する。
**「1 bash invocation = 1 wave」を厳守**する。

## UNKNOWN担保 (不変)

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 10968・class 23964・class 5343・class 2251・
**class 34269 (54キーすべて・EXHAUSTED行・incident-areaキー
(ac028/ac029)・本driveで新たにprobeされるac030..ac054を含む)**・
class 5804・class 34948 は本driveの実行・出版のどの時点でもUNKNOWNのまま。
nodes数・wall秒数を勝敗として読まない。被覆・secured・root勝敗の主張を
しない。WIN/LOSS採用は scrutiny owner C++ gate `9193f5b6…` 通過後の
 別adoption Part (pinned merger `90711961…` 経由) のみで、本レーンは代行しない。
