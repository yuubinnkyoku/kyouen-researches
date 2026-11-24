# Part DK 単一オーナー宣言: batch-30 (class 34269) 最終EXHAUSTED残1行 ac013 の25M high-budget再probe (publish-then-execute)

Part DJ 完了log (`41c9ede4`) のとおり、batch-30 54キーのEXHAUSTED残は
**ac013 1行のみ** (15M EXHAUSTED → 20M EXHAUSTED・honest UNKNOWN)。本宣言は
batch-28 precedent (Part CS: 20M exhausted行の25M再probe) と同一形式で
**budget 25M (20Mは同条件でないため再probe可) でac013を再probeする**。
**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張をしない。
**標準11×11は本Partのどの時点でもUNKNOWNのまま**。

## 対象キー (published evidence)

- ac013: 15M EXHAUSTED (2026-11-24T01:56:44Z・batch-30 drive-2) → 20M EXHAUSTED
  (nodes 20,000,000・p1==p2 node-exact・Part DJ `bcd67982`) → 本Partは25M。

## kit (事前登録pin・A scaffold出版後にfetch-back照合)

- scripts/jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` (pinned byte-clone)
- scripts/runner_dk.sh `9048c3291d981d52c846bc177bb727f95827d88892c6fd44ae84c5a110b4ac1c`
  = runner_dj.sh `c5e86d49…` byte-clone・**deltaは1行のみ** (`BUDGET=20000000`
  → `BUDGET=25000000`・付随してrunbatch系 `f591f8c2` 由来の1行delta 2行分)。
  replay_done guard・2-pass比較・EXHAUSTED honest label・WIN exit 45不変
  (usage commentの旧称表記はcosmetic)。
- input/batch-keys.json `797467ec1009fc835c3fa9b92a29ebdbac6c3431777abbcde11a8a6fc1df88d5`
  (1キー・schema n11-centralreply-closure-class34269-batch30-exh1-25m-input-v1)
- input/ac013.input.csv `edf4f6619bdf98208af758b19d03b454a9daa89b9e4bdcf214963b29848b0650`
  (batch-30 published CSV byte-clone・batch-30 MANIFEST行とsha一致確認済み)

## 実行設計 (事前登録・cross-invocation step design)

ac013の20M passは2-worker併走下で222-229sを要した (Part DJ)・25M EXHAUSTED級は
1 passが260s内側timeoutを超過し得るため、**CS precedentのcross-invocation
step design**を採る:

1. invocation A: jsreplay p1 (budget 25M) を単独実行 (`output/raw/ac013.p1.out`)
   — 外側300s tool cap内。完了しない場合は誠実に記録して中止 (亏损passは
   runner replay_done guardのtruncated扱いで再実行可能)。
2. invocation B: jsreplay p2 (同条件fresh-cold) を単独実行
   (`output/raw/ac013.p2.out`)。
3. invocation C: runner_dk.sh を実行 (両pass fileはreplay_done付きで既存) →
   pinned runnerの比較・status.log追記 (PASS/EXHAUSTED/WIN-HALT) が走る。

stop rulesはrunner系不変: WIN rc=45・MISMATCH rc=42・p1/p2 fail 43/44。
PASS要件はp1==p2 node-exact (budget,result,nodes字段)。

## val-gate (宣言後・host fresh実行)

- VG1: first-15m input を budget 25M で実行 → 期待: result=2・nodes=3,651,923
  (published 15M baselineと node-exact・budget字段のみ25M)。
- VG2: second-15m input → 期待: result=2・nodes=5,040,200。

不一致ならhard-stop。

## 出版計画

1. A scaffold: scripts 2 + input 2 + val-gate 4 + README。
2. B outputs: raw p1/p2 + status.log。
3. C: README最終 + MANIFEST-sha256。
4. 完了log: research/log/2026-11-24-part-dk-batch30-exh1-25m.md。

実験dir: research/experiments/n11-centralreply-closure-class34269-batch30-exh1-25m-20261124/

## 対抗確認・observed HEAD

- observed HEAD-before-push: `41c9ede48c5ef9b13bc0c9e2ef5611530314b057` (Part DJ 完了log直後)。
- 「Part DK」宣言 throughput search: 0件 (単一オーナー)。

## UNKNOWN担保 (不変)

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・ac013を含む)**・class 5804・class 34948 は本Partの実行・出版の
どの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。被覆・secured・
root勝敗の主張をしない。WIN/LOSS採用はscrutiny owner C++第二実装 gate
`9193f5b6…` 通過後の別adoption Part (pinned merger `90711961…` 経由) のみで、
本レーンは行使しない。
