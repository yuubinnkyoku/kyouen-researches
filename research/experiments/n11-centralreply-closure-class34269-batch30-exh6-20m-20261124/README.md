# batch-30 EXH6 20M reprobe: closure class 34269 high-budget step (Part DJ, 2026-11-24)

Part DJ (宣言: research/log/2026-11-24-part-dj-batch30-exh6-20m-declaration.md・commit
`0b113ef3`・publish-then-execute・単一オーナー)。Part CP batch-30 (54キー全probe完了・
drive-3完了log `0db54f19`) のうち **15M budgetでEXHAUSTED (honest UNKNOWN) 残りの
6行 (ac006/ac013/ac032/ac036/ac044/ac047)** を **budget 20M で再probeする**
(batch-28 Part CQ/CS/CT・batch-31 Part DI precedent・同条件でないため再probe可)。
**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張はしない。

## kit (fetch-back sha256照合後、本READMEに実測pinを追記)

- scripts/jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` (batch-30 pinned byte-clone)
- scripts/runner_dj.sh `c5e86d49bc851f7e511e811bef5052d4634adfbbdf85a1224d101638db284a90` (runbatch `f591f8c2…` byte-clone・delta 1行: BUDGET 15000000→20000000)
- scripts/dj_step.sh `6a67b83f196736a23e50a4219a1c71860127d05647ccbd0c8eaf5e1e0e47da2b`
- input/batch-keys.json `a80f402befaf2e8cf7b0484b4c51a125b525ccfd536a31ad7dea52b555011068` (6キー)
- input/ac006/013/032/036/044/047.input.csv (batch-30 published CSV byte-clone)

## 事前登録 stop rules

WIN rc=45・MISMATCH rc=42 (STRICT・空p2 MISMATCH 1行でもhard-stop)・p1/p2 fail
rc=43/44・LOCK-BUSY rc=46・ORPHAN rc=47 (retryable)・260s truncated rc=124 (retryable)。
WIN-CONTINUE。EXHAUSTED-at-20M は honest UNKNOWN (25M段は別宣言)。
**1 bash invocation = 1 wave** (2キー x 2 worker・timeout 260 内側wrap)。

## val-gate (宣言後 host fresh 実行)

- VG1 first-20m: result=2 nodes=3,651,923 (15M published baselineと node-exact) — PASS
- VG2 second-20m: result=2 nodes=5,040,200 (同上) — PASS

budget cap 20M が in-budget resolve の値に影響しないことを機械担保。

## 実行記録 (2026-11-24T07:5x-08:1xZ ・10 wave invocations + ALL-DONE)

**結果: 6/6キー 2-pass fresh-cold PASS (p1==p2 node-exact・real_mismatch=0)**:

| key | 15M (published) | 20M再probe (本Part) |
|---|---|---|
| ac006 | EXHAUSTED | **WIN 18,182,847** (WIN-HALT・WIN-CONTINUE) |
| ac013 | EXHAUSTED | EXHAUSTED 20,000,000 (honest UNKNOWN・同条件再probeなし・残EXHはこの1行のみ) |
| ac032 | EXHAUSTED | **LOSS 19,707,272** |
| ac036 | EXHAUSTED | **LOSS 16,605,302** |
| ac044 | EXHAUSTED | **LOSS 16,323,488** |
| ac047 | EXHAUSTED | **LOSS 17,394,041** |

- batch-30全体: EXHAUSTED 6→1 (ac013のみ)・**WIN 11 / LOSS 42 / EXHAUSTED 1**
  (probe-level label・verdict不消費)。
- waves: 各キー p1 が175-229sを要するため260s内側timeoutでp2が打到ち切られ
  (TRUNCATED-RETRY 6行・truncated file 6件保存)、次invocationでp2のみfresh-cold
  再実行して完了 (rc=124 retryable設計どおり・値レベルdivergenceなし)。

## 誠実記録・incident (env reset 1件・pre-wipe観測との一致)

1. **環境リセット1件** (~07:33Z): wave 2 (ac032+ac036) invocationがKoyeb infra
   failure ("artifact files could not be saved・変更は破棄") で環境ごと棄却され、
   ローカル作業tree全損 (その時点でac006/ac013のwave 1分raw file・status.logは
   未出版で喪失)。**published A scaffold `81ae89f1` (fetch-back 15/15 byte一致) から
   kit再構成** (全pin sha一致) し、6キーを最初からfresh実行した。
   **決定性をCPU間で機械確認: pre-wipe観測** (ac006 p1: result=1, nodes=18,182,847
   205s / ac013 p1: result=0, nodes=20,000,000 222s) **とリセット後再実行**
   (ac006: nodes=18,182,847 217s / ac013: 20,000,000 229s) が完全一致。
2. drive-2 (batch-30) のKoyeb zombie-raceと異なり、本Partはguard群
   (flock・orphan-liveness・replay_done) で競合なし-MISMATCH未発生
   (real 0・空p2 0)。


## UNKNOWN担保

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・本Part対象6キーを含む)**・class 5804・class 34948 は本Partの
実行・出版のどの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。
WIN/LOSS採用はscrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption Part
(pinned merger `90711961…` 経由) のみ。
