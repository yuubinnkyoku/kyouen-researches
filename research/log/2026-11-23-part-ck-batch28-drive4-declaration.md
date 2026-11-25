# Part CK 宣言 (2026-11-23): batch-28 (closure class 5343) drive-4 — fileless 45キー aa010..aa054 probe (WIN-CONTINUE・publish-then-execute)

単一オーナー: n11中央応答レーン (本セッション・Part CJ継続)。対抗宣言なし
(push直前の最新main直近15コミットを機械grepし、batch-28 drive-4 / aa010..aa054 /
Part CK を主張するcommitなしを確認済み。Part CJ (drive-3) 完了時点で「残り45キー
(aa010..aa054) はfileless UNPROBEDのまま」・並走のbatch-29 (Part CI) はclass 2251
所有で非接触)。

## 1. スコープ

Part CJ (batch-28 drive-3) で残された fileless 45キー (aa010..aa054) を、published
batch-28 kitのbyte-clone (pinned runner `f591f8c2…` 変更なし) で2-pass fresh-cold
probeする drive-4。**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張はしない。
EXHAUSTED (budget 15M) はhonest UNKNOWN。**WIN-CONTINUE (事前登録)**: WIN行
(runner rc=45) はhonest labelとしてstatus.log・rawに記録するが、driveは反復を継続
する (Part CE batch-23 continuation先例)。停止条件は (a) ALL-DONE (45キー完走)・
(b) MISMATCH rc=42 hard-stop・(c) session時間制約による誠実な打ち切り (その場合
未probeキーはfileless UNPROBEDのまま出版・将来drive-5+で継続)。drive-1/2/3の
2-WIN halt設計とは本宣言で明示的に置き換える (同一pinned runner・stop rulesは
runner内蔵のまま・wave継続判定のみorchestration層の相違)。

## 2. 事前機械確認 (read-only・正直開示)

- published batch-28 drive-3 dir 105ファイル (commit `eed9f348` でfetch-back 104/104
  sha OK + MANIFEST byte同一を本セッションで実施済み) がbyte-clone基礎。
- seed: drive-3 published status.log 21行 (Part CJ B `55fe0a81`・17行drive-2 seed +
  aa008/aa009の4行)・row-audit-winhalt.json (`eb1d1e98…` probed 9)。completed行
  (aa001..aa009) は再probeしない。
- 残りキー: batch-keys.json (`af19208f…`) とstatus.log done集合 (9キー) の差 =
  **45キー aa010..aa054** (機械導出)。
- val-gate: 本セッションでfresh 4/4 node-exact (Part CJ `at2m`/`15m`・`.cj-host.out`)
  を実施済みだが、drive-4 kit出版では同4ファイルを再掲する (再実行はしない・
  「fresh実行は宣言後」の規約に鑑み、本宣言後にもう一度fresh実行して掲載する)。

## 3. 実行protocol (宣言後)

1. val-gate fresh再実行 4/4 node-exact (同一4キー・wall_s比較外)。
2. wave反復: session-local orchestration (`scripts/drive4_local_step.sh`・Part CD/CJ
   と同型・未完キー最大2個ずつ `timeout 285` でpinned runbatch.shへ直接)。WIN rc=45は
   記録のみで次反復へ (WIN-CONTINUE)。
3. 終了後、row-audit: **batch-28にはWIN行とPASS/EXHAUSTED行が混在する完全走査型に
   なる可能性があるため、pinned `row_audit_batch28.py` (`656cac31…`) と pinned
   `row_audit_batch28_win_halt.py` (`96867282…`) の両方を通し、いずれかがPASSする
   ことを確認** (win_halt版は「fragment/fileless皆無」でGATE-FAILする設計・完全
   走査時はfull版が適用。部分終了時はwin_halt版)。x3 byte一致。
4. tamper battery (scratch上・実効性assertモデル・CJ T1'設計): 完走行result反転→
   p1/p2 mismatch gate・status.log nodes+1 (WIN行・LOSS行両probe)・raw legal反転→
   published packet legal不一致・battery後pristine全ファイルsha不変。

## 4. 期待機械簿記 (事前登録)

- probed total: 9 + (drive-4で完走したキー数)。**結果非予告・いかなる勝敗も宣言しない**
  (WIN/LOSS/EXHAUSTEDの分布は実行後のhonest label)。
- canonical cache (Part CH merged 6,294行 `3124461b…`) への書込なし (adoptionは別
  adoption Partのみ)。closure table不変。
- nodes数・wall秒数はbookkeepingであり勝敗ではない。

## 5. 実験dir・出版形態 (宣言後に順次)

- 実験dir: `research/experiments/n11-centralreply-closure-class5343-batch28-drive4-20261123/`
  (README・MANIFEST-sha256・scripts (7 pinned byte-clone + session-local 1)・input 55
  byte-clone・val-gate (published 12 + fresh `.cj-host.out` 4)・output (seed raw 22 +
  status.log (21行seed + drive-4追記) + row-audit json))。
- 宣言・完了記録は `research/log/` に恒久化。全files commit-pinned fetch-back byte照合。

## 6. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
class 10968・class 23964・class 5343 (54キーすべて・本driveの全キーを含む) は本Partの
実行・出版のどの時点でもUNKNOWNのまま。** WIN採用は引き続きscrutiny owner C++第二実装
gate (`9193f5b6…`) のみ (本レーンは代行しない)。

## 7. 不接触

- Part CI (batch-29・class 2251・並走所有) のdir・outputs・進行 (scaffold publish済)。
- Part CG (aa006/aa007 thirdimpl)・Part CE (batch-23 fileless)・batch-24 fileless 49キー、
  batch 1..28 published各dir (不変) と drive-3 published dir (不変)。
- BASE cache `3124461b…` read-only不変・unconsumed closure WIN候補35キーの採用状態・
  scrutiny owner gate `9193f5b6…`・fast lane (y=23)・finite-field lane・19root計画。
