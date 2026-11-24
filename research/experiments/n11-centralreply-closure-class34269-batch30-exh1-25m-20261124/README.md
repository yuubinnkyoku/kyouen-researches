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

(本セクションはB outputs/C工程後に更新)

## UNKNOWN担保

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・ac013を含む)**・class 5804・class 34948 は本Partの実行・出版の
どの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。
WIN/LOSS採用はscrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption Part
(pinned merger `90711961…` 経由) のみ。
