# Part DJ 完了log: batch-30 (class 34269) EXHAUSTED 6行の20M high-budget再probe — 5/6キー解決 (WIN 1・LOSS 4)・EXH残1行 (ac013)

宣言 `0b113ef3` (2026-11-24T07:31:xxZ・単一オーナー・publish-then-execute) →
A scaffold `81ae89f1` (15 file・fetch-back 15/15 byte一致) → **env reset (wave 2
invocationでKoyeb infra failure・ローカルtree全損)** → A scaffoldからkit再構成
(全pin sha一致) → 10 wave invocations + ALL-DONE → B outputs `bcd67982`
(19 file・fetch-back 19/19) → C `1d88aaa6` (README最終 + MANIFEST-sha256 34行・
fetch-back 2/2 commit-pin URL) → 完了log (本file)。**verdict不消費**。閉鎖・被覆・
secured・root勝敗の主張をしない。**標準11×11は本Partのどの時点でもUNKNOWNのまま**。

## 結果 (6/6キー 2-pass fresh-cold PASS・p1==p2 node-exact・real_mismatch 0・空p2 0)

- **ac006: WIN 18,182,847** (result=1・15M EXHAUSTED→20M WIN解決・WIN-HALT/
  WIN-CONTINUE) — batch-30 11行目のprobe-level WIN。
- **ac032: LOSS 19,707,272**・**ac036: LOSS 16,605,302**・**ac044: LOSS
  16,323,488**・**ac047: LOSS 17,394,041** (いずれも20M解決)。
- **ac013: EXHAUSTED at 20M** (nodes 20,000,000・honest UNKNOWN・同条件再probe
  なし)。**batch-30のEXHAUSTED残はこの1行のみ** (25M/30M段は別単一オーナー宣言。
  DI (ad043) precedentでは30Mで18.2M nodes解決が観測済み)。
- batch-30全体のprobe-level label: **WIN 11 / LOSS 42 / EXHAUSTED 1**。

## 実運用上の事実 (誠実記録)

1. **環境リセット1件** (~07:33Z・wave 2 invocation): Koyeb infra failure
   ("artifact files could not be saved・変更は破棄")。wave 1分 (ac006/ac013) の
   raw file・status.logは未出版だったため喪失。published A scaffold 15 fileから
   再構成し6キーを最初からfresh実行した。**pre-wipe観測** (ac006 p1 result=1
   nodes=18,182,847 205s・ac013 p1 result=0 nodes=20,000,000 222s) と
   **再実行** (18,182,847 217s・20,000,000 229s) が完全一致で、pinned solverの
   決定性がホスト間でも成立 (publish-then-execute設計の通りの回復)。
2. **260s内側timeoutとEXH級キーの相互作用**: 各キー p1 が175-229sを要するため、
   p1完了直後にp2開始→260s経過でp2 truncated (TRUNCATED-RETRY 6行・6 truncated
   file保存・出版済)。次invocationのreplay_done guardがp1を保持してp2のみ
   fresh-cold再実行 (設計どおり・1キーにつき2 invocationsで収束)。
   **値レベルdivergenceなし (全行p1==p2)**。
3. v2/v3系guard群 (flock・orphan-liveness・replay_done・strict MISMATCH) は
   MISMATCH 0・LOCK-BUSY 0・ORPHAN 0で完走。

## UNKNOWN担保

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・本Part対象6キーを含む)**・class 5804・class 34948 は本Partの
実行・出版のどの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗として読まない。
被覆・secured・root勝敗の主張をしない。WIN/LOSS採用はscrutiny owner C++第二実装
gate `9193f5b6…` 通過後の別adoption Part (pinned merger `90711961…` 経由) のみで、
本レーンは行使しない。

## レジューム (着手前に必ず最新main再取得・hourly並走注意)

- **ac013 (唯一のEXH残) の25M/30M再probeは別単一オーナー宣言** (Part DK候補。
  DI precedent: 30M resolving at 18.2M nodes)。
- batch-30 WIN 11行 (ac002/ac003/ac020/ac026/ac027/ac034/ac041/ac045/ac048/
  ac054/ac006) の第三実装交叉検証は別Part候補 (b28-win46 queue registry形式の
  registry登録を推奨)。
- LOSS 42行・WIN 11行のcanonical adoptionはscrutiny gate後の別adoption Part専権。
- 並走観察 (すべて非接触): Part DH/DF (b28 P4/P2 thirdimpl・scaffold出版済み・
  outputsは本session開始時点で未出版)・K1284 (z1ラダーδ4/δ5・高速レーン)。
