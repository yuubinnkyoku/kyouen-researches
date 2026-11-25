# batch-30 EXH1 25M reprobe: ac013 (Part DK, 2026-11-24)

Part DK (宣言: research/log/2026-11-24-part-dk-batch30-exh1-25m-declaration.md・commit
`e411045b`・publish-then-execute・単一オーナー)。batch-30 (class 34269) 54キーで
唯一のEXHAUSTED残である **ac013** (15M EXH→20M EXH・Part DJ `41c9ede4`) を
**budget 25M で再probeする** (CS precedent・cross-invocation step design)。
**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張はしない。

## kit (fetch-back sha256照合後、本READMEに実測pin)

- scripts/jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
- scripts/runner_dk.sh `9048c3291d981d52c846bc177bb727f95827d88892c6fd44ae84c5a110b4ac1c` (runner_dj byte-clone・delta 1行: BUDGET 20000000→25000000)
- input/batch-keys.json `797467ec1009fc835c3fa9b92a29ebdbac6c3431777abbcde11a8a6fc1df88d5` (1キー)
- input/ac013.input.csv `edf4f6619bdf98208af758b19d03b454a9daa89b9e4bdcf214963b29848b0650` (batch-30 published CSV byte-clone)

## 実行設計

invocation A: jsreplay p1 (25M) 単独 → invocation B: jsreplay p2 (25M) 単独 →
invocation C: runner_dk.sh (両pass file存在 → pinned比較・status.log追記)。
PASS要件: p1==p2 node-exact。stop rules: WIN rc=45・MISMATCH rc=42・p1/p2 fail 43/44。

## val-gate (宣言後 host fresh 実行)

- VG1 first-25m: result=2 nodes=3,651,923 (published 15M baselineと node-exact) — PASS
- VG2 second-25m: result=2 nodes=5,040,200 (同上) — PASS

## 実行記録

**原lane (Part DK)**: 宣言 `e411045b` (08:11:41Z) → A scaffold `890e6186` (08:12:48Z) →
invocation A (P1 完走: result=2 nodes=21,954,135 wall_s=126) → invocation B (P2) 発行時の
実行環境outage (interim `2117ea737` = `output/INTERIM-P1-NOTE-20261124.md`) でP1 rawを
含むローカル作業状態が失われ、以降 3.5h 停滞。

**takeover lane** (takeover宣言 `6c92d945ca`・2026-11-24T11:43:17Z・原宣言の
earliest_takeover 11:41:41Z 経過後・対抗なし機械確認済み): published kit
(fetch-back sha pin 6/6 一致) から全工程を本host fresh で再実行:

- VG1 re-run (budget 25M): result=2 nodes=3,651,923 — published baseline
  `first-25m.dkvvg1-host.out` と node-exact (budget字段のみ25M) — PASS
  (`val-gate/first-25m.dkt-vg1-host.out`・wall_s=19)
- VG2 re-run (budget 25M): result=2 nodes=5,040,200 — baseline と node-exact — PASS
  (`val-gate/second-25m.dkt-vg2-host.out`・wall_s=27)
- invocation A: p1 fresh-cold (budget 25M): **result=2 (honest label)** nodes=21,954,135
  wall_s=126 (`output/raw/ac013.p1.out`・replay_done付)
- invocation B: p2 fresh-cold (同条件): result=2 nodes=21,954,135 wall_s=129
  (`output/raw/ac013.p2.out`・replay_done付)
- invocation C: runner_dk.sh ac013 (pinned byte-clone): **PASS 25000000,2,21954135
  (p1==p2 node-exact)** rc=0・`output/status.log` append (2026-11-24T11:49:57Z)
- 原host pre-wipe P1 観測 (nodes=21,954,135) と本host fresh 両pass が nodes 完全一致
  (3-way一致・wall_s は非比較字段)。

**ac013 の honest label は budget 25M 2-pass fresh-cold node-exact で result=2
(15M EXHAUSTED → 20M EXHAUSTED → 25M: 解決)。verdict不消費** (adoption は
scrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別 adoption Part・pinned
merger `90711961…` 経由のみ)。batch-30 (class 34269) 54キーに EXHAUSTED 行は
残っていない (honest label bookkeeping・閉鎖・被覆・root勝敗の主張ではない)。
nodes数・wall秒数を勝敗や距離として読まない。

## UNKNOWN担保

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・ac013を含む)**・class 5804・class 34948 は本Partの実行・出版の
どの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。
WIN/LOSS採用はscrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption Part
(pinned merger `90711961…` 経由) のみ。
