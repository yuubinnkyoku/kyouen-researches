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

## 実行記録

(本セクションはB outputs/C工程後に更新)

## UNKNOWN担保

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・本Part対象6キーを含む)**・class 5804・class 34948 は本Partの
実行・出版のどの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。
WIN/LOSS採用はscrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption Part
(pinned merger `90711961…` 経由) のみ。
