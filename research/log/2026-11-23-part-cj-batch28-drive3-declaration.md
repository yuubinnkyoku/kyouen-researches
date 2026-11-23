# Part CJ 宣言 (2026-11-23): batch-28 (closure class 5343) drive-3 continuation — fileless 47キー aa008..aa054 probe (publish-then-execute)

単一オーナー: n11中央応答レーン (本セッション・Part CB/CD系drive継続)。対抗宣言なし
(push直前の最新main直近40コミットを機械grepし、batch-28 drive-3 / aa008..aa054 継続
probe / Part CJ / class 5343 drive継続 を主張するcommitなしを確認済み。Part CD (drive-2)
は2026-11-23T16:26Zに「残り47キー (aa008..aa054) はfileless UNPROBEDのまま」で完了、
Part CH (aa003 1-LOSS adoption) も完了済み・fileless 47キーのprobeは未着手)。

## 1. スコープ

Part CD (batch-28 drive-2) で残された fileless 47キー (aa008..aa054) を、published
batch-28 kitのbyte-clone (pinned runner) で2-pass fresh-cold probeする drive-3。
**verdict不消費** (probe結果のWIN/LOSSはhonest labelのまま、canonical adoptionは別
adoption Part (pinned merger `90711961…` 経由) のみ)。閉鎖・被覆・secured・root勝敗の
主張はしない。EXHAUSTED (budget 15M) はhonest UNKNOWN (same-condition再probeなし)。
session時間制約による誠実な打ち切りの場合、未probeキーはfileless UNPROBEDのまま
出版する (drive-1/2と同じwave設計・将来のdrive-4+で継続可能)。

## 2. 事前機械確認 (read-only・正直開示)

publish-then-execute規約に対する正直開示として、**read-only解析 (kit取得・sha検証・
残りキー導出) は本宣言の出版前に本hostで機械実施済み**である。probe実行・val-gate
fresh実行は宣言後のみ。

機械確認済み:

1. **kit byte-clone**: published batch-28 drive-2 dir
   `research/experiments/n11-centralreply-closure-class5343-batch28-drive2-20261123/`
   96ファイル (dir MANIFEST-sha256.txt `2811b577…`) をcommit-pinned raw URLから取得し
   sha256 96/96 OK。
2. **seed status**: published drive-2 status.log 17行 (`343097c2…`)・row-audit-winhalt
   (`3e86a32b…`: probed 7 = WIN 4 + LOSS 1 + EXHAUSTED 2 + fileless 47 + mismatch 0)。
   drive-1/2のcompleted行 (aa001..aa007) は再probeしない (残りキーはstatus.logから機械導出)。
3. **残りキー**: batch-keys.json (`af19208f…`) 54キーと status.log done集合(aa001..aa007)
   の差 = **47キー aa008..aa054** (機械導出・1個一致)。
4. **scripts pins** (published MANIFESTと一致・変更なし): runbatch.sh `f591f8c2…`・
   jsreplay.js `84585617…`・drive_batch28.sh `08dc059c…`・row_audit_batch28.py
   `656cac31…`・row_audit_batch28_win_halt.py `96867282…`・make_batch28_keys.py
   `d1ffe72f…`・runwave.sh `8efd78c2…`。
5. **正本cache不変**: Part CH merged canonical cache 6,294行 (`3124461b…`) はread-only
   不変 (本probeはfresh-cold 2-passでありcacheを読まない・書かない)。

## 3. val-gate (宣言後・要件)

published batch-28 drive-2 val-gate (sanctioned 4キー: at2m×2 budget 2M EXHAUSTED
2,000,000 x2・15m×2 budget 15M result 2 nodes 3,651,923 / 5,040,200) を本hostでfresh
実行し、**4/4 node-exact (wall_s比較外)・禁止四角 95,670・`# replay_done` x4** を
要件とする (published baselines `+ .cj-host.out` 4 files として出版)。

## 4. 実行protocol (宣言後に実施)

1. val-gate fresh 4/4 (上記)。
2. drive-3 wave反復: 各 invocationで未完キーを最大2個 (2 solver並列上限) `timeout 285`
   でpinned runbatch.shに直接渡す session-local orchestration
   (`scripts/drive3_local_step.sh`・Part CD `drive2_local_step.sh` と同型・pinned kit
   の一部ではない・実行tree pathの差のみでrunner/solver/stop rulesはbyte-identical)。
   solver・runner内部の変更は一切なし。
3. 完了ごとにstatus.log機械集計。row-auditはpinned `row_audit_batch28_win_halt.py`
   (`96867282…`・変更なし) x3 byte一致 + tamper battery (scratch tree上・drive-2の
   4 probesと同型: T1 完走行result反転→p1/p2 mismatch gate・T2 status.log nodes+1→
   WIN-HALT record incomplete gate・T3 seed行 (aa001..aa007) 改ざん→row picture
   disagreement gate・T4 raw行legal改ざん→published packet legal不一致gate。
   各probeに実効性assert (改ざん実際適用検査) + battery後pristine restoreで実験dir
   全file sha不変検証)。

## 5. stop rules (事前登録・pinned runner内蔵と同じ)

- **WIN rc=45** (result 1・2-pass node-exact): 本driveで**2 WIN行観測でwave halt**
  (batch-28 drive-1/2と同じ設計)。その時点で残キーはfileless UNPROBED。
- **MISMATCH rc=42**: 即時hard stop・誠実記録 (verdict不消費)。
- **P1/P2 fail rc=43/44**: stop (honest記録)。
- **EXHAUSTED**: 続行 (honest UNKNOWN)。
- **TRUNCATED pass** (timeout窓・`# replay_done`なし): evidenceでなくfresh-cold retry
  (completed行は不変・再実行しない)。
- **session時間制約打ち切り**: 誠実終了 (fileless残キーUNPROBED出版・将来drive-4+継続)。

## 6. 期待機械簿記 (事前登録)

- probed total: 7 + (drive-3で完走したキー数)。**結果非予告・いかなる勝敗も宣言しない**
  (WIN/LOSS/EXHAUSTEDの分布は実行後のhonest label)。
- class 5343のunknown_now (Part CH reauditで53) は本drive単体ではclosure tableに
  反映されない (canonical cacheへの反映はadoption Partのみ)。
- nodes数・wall秒数はbookkeepingであり勝敗ではない。
- 本driveはcanonical cacheに一切書き込まない (adoptionは別adoption宣言のみ)。

## 7. 実験dir・出版形態 (宣言後に順次)

- 実験dir: `research/experiments/n11-centralreply-closure-class5343-batch28-drive3-20261123/`
  (README・MANIFEST-sha256・scripts (7 pinned byte-clone + session-local 1)・input 55
  byte-clone・val-gate (published 12 + 本host fresh 4)・output (seed raw 18 + status.log
  (17行seed + drive-3追記) + row-audit json))。
- 宣言・実行記録はPart CH先例どおり `research/log/` に恒久化 (note運用は廃止済み・
  README generated領域は直接編集しない)。
- 出版は全files commit-pinned raw URL fetch-back byte照合 (branch path CDN staleは不使用)。

## 8. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
class 10968・class 23964・class 5343 (54キーすべて・本driveの全キーaa008..aa054を含む)・
class 2251 (Part CI所有・非接触) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
WIN採用は引き続きscrutiny owner C++第二実装 gate (`9193f5b6…`) のみ (本レーンは代行しない)。
nodes数を勝敗として読まない。

## 9. 不接触

- Part CI (batch-29・class 2251・17:27Z宣言済み・並走所有) のdir・outputs・進行。
- Part CG (batch-28 drive-2win aa006/aa007 thirdimpl・宣言済み・並走所有) のdir・outputs。
- Part CE (batch-23 fileless 51キー・宣言済み) と batch-24 fileless 49キー、batch 1..28の
  published各dir (不変・drive-3は新規dir)。
- BASE cache `3124461b…` (Part CH merged 6,294行) read-only不変。
- unconsumed closure WIN候補33キーの採用状態・scrutiny owner gate `9193f5b6…`。
- fast lane (y=23 universal verifier K1266宣言済み)・finite-field lane (K1254)・
  inversive/z19 lanes・19root計画。
