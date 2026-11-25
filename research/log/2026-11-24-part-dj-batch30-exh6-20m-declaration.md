# Part DJ 単一オーナー宣言: batch-30 (class 34269) EXHAUSTED 6行 (ac006/ac013/ac032/ac036/ac044/ac047) の20M high-budget再probe (publish-then-execute)

Part CP batch-30 は54キー全probe完了 (drive-3完了log `0db54f19`・2026-11-24T07:29:04Z)。
54キーのうち6行が15M budgetでEXHAUSTED (honest UNKNOWN) のまま残っている。
本宣言は batch-28 precedent (Part CQ 20M / CS 25M / CT 30M)・batch-31 precedent
(Part DI ad043 30M RESOLVED-WIN `1036c08e`) と同一形式の high-budget再probeを
**budget 20M (15Mは同条件でないため再probe可) で実行する**。**verdict不消費**。
閉鎖・被覆・secured・root勝敗の主張をしない。**標準11×11は本Partのどの時点でも
UNKNOWNのまま**。

## 対象6キー (published evidence: batch-30 status.log 79行・`88a474b5…`)

- ac006: 2026-11-24T01:48:05Z EXHAUSTED 15000000,0,15000000 (drive-2)
- ac013: 2026-11-24T01:56:44Z EXHAUSTED 15000000,0,15000000 (drive-2)
- ac032: 2026-11-24T06:55:12Z EXHAUSTED 15000000,0,15000000 (drive-3 takeover)
- ac036: 2026-11-24T07:03:43Z EXHAUSTED 15000000,0,15000000 (drive-3 takeover)
- ac044: 2026-11-24T07:15:13Z EXHAUSTED 15000000,0,15000000 (drive-3 takeover)
- ac047: 2026-11-24T07:20:11Z EXHAUSTED 15000000,0,15000000 (drive-3 takeover)

いずれも 2-pass fresh-cold (p1==p2 node-exact 15,000,000)。

## kit (事前登録pin・A scaffold出版後にfetch-back照合)

- scripts/jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` (batch-30 pinned byte-clone)
- scripts/runner_dj.sh `c5e86d49bc851f7e511e811bef5052d4634adfbbdf85a1224d101638db284a90`
  = pinned runbatch.sh `f591f8c2…` byte-clone・**deltaは1行のみ** (`BUDGET=15000000`
  → `BUDGET=20000000`)。run_key host-interruption guard・2-pass fresh-cold・
  node-exact PASS要件・EXHAUSTED honest label・WIN exit 45 すべて不変。
- scripts/dj_step.sh `6a67b83f196736a23e50a4219a1c71860127d05647ccbd0c8eaf5e1e0e47da2b`
  = drive3_local_step.sh `41c5719c…` からのdelta 3点のみ: (1) lock名 `.dj.lock`
  (2) worker/orphan pattern `runner_dj.sh` (3) **MISMATCH policyをSTRICT化**
  (本Partのstatus.logはfresh・single-writerのため、real divergence (両値非空) は
  当然、**空p2 MISMATCH 1行でも hard-stop rc=42**)。drive-3のincident許容 (index済み
  2行) は本Partには適用しない。それ以外 (done-set抽出・2キー x 2 worker wave・
  timeout 260 内側wrap・空キーガード・flock・orphan-liveness) は不変。
- input/batch-keys.json `a80f402befaf2e8cf7b0484b4c51a125b525ccfd536a31ad7dea52b555011068`
  (6キー・schema n11-centralreply-closure-class34269-batch30-exh6-20m-input-v1・
  budget 20000000・source batch-30 keys JSONからの機械抽出)
- input/ac006/013/032/036/044/047.input.csv 6 file (batch-30 published CSVの
  byte-clone・全件MANIFEST行 sha一致済み)

## 事前登録 stop rules (drive-1/2/3と同一・v3系)

WIN (result 1) rc=45・MISMATCH rc=42・p1/p2 fail rc=43/44・LOCK-BUSY rc=46 (retryable)・
ORPHAN-DETECTED rc=47 (retryable)・260s inner truncated rc=124 (retryable・次waveで
fresh-cold再実行)。**WIN-CONTINUE設計**: rc=45は当該キー単位のみでwave継続。
EXHAUSTED-at-20M (result 0) は honest UNKNOWN・本Part内では再probeしない
(25M段は別単一オーナー宣言)。**「1 bash invocation = 1 wave」厳守**。

## val-gate (宣言後・本host fresh実行・A scaffold出版)

budget引き上げが resolve済みキーの結果・節点数を変えないこと (budget capは
in-budget解には影響しないこと) を2本で担保する:

- VG1: first-15m input (`replay,0,5,98,0,...` published baseline: 15Mで
  result=2 nodes=3,651,923) を **budget 20M** で実行 → 期待: result=2・
  nodes=3,651,923 (15M published baselineと node-exact・budget字段のみ20M)。
- VG2: second-15m input (15Mで result=2 nodes=5,040,200) を budget 20Mで実行 →
  期待: result=2・nodes=5,040,200。

sidecar `.djvg1-host.out` / `.djvg2-host.out` をA scaffoldで出版。不一致なら
hard-stop (本Part実行取りやめ)。

## 出版計画

1. A scaffold: scripts 3 + input 7 + val-gate sidecar 2 + README (実行記録空欄)。
2. B outputs: waves完了分の raw p1/p2 + status.log (fresh・append-only)。
3. C: README最終 (実行記録) + MANIFEST-sha256 (全file)。
4. 完了log: research/log/2026-11-24-part-dj-batch30-exh6-20m.md。

実験dir: research/experiments/n11-centralreply-closure-class34269-batch30-exh6-20m-20261124/

## 対抗確認・observed HEAD

- observed HEAD-before-push: `0db54f1993767597c29caddf0211f50bc804d6f2`。
- 「Part DJ」宣言・batch-30 EXH6再probe宣言の throughput search 結果: 0件
  (単一オーナー)。

## UNKNOWN担保 (不変)

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・本Part対象6キーを含む)**・class 5804・class 34948 は本Partの
実行・出版のどの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。
被覆・secured・root勝敗の主張をしない。WIN/LOSS採用はscrutiny owner C++第二実装
gate `9193f5b6…` 通過後の別adoption Part (pinned merger `90711961…` 経由) のみで、
本レーンは行使しない。
