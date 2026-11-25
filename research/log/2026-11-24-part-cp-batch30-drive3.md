# Part CP batch-30 (closure class 34269) drive-3 完了log — 残25キー ac030..ac054 完走 (原宣言 6edbcf58 + takeover 3f0aeb55)

原宣言 `6edbcf58` (2026-11-24T02:27:43Z・Part CP batch-30 drive-3・publish-then-execute)
は scaffold A′ `cca29581` (02:29:06Z・session script v3 出版 + drive-3 host val-gate
sidecar `.d3t-host.out` 4) 以降、実験dirへのcommitゼロのまま4時間18分停滞した。
takeover規約 (宣言時刻+3.5h = earliest_takeover 05:57:43Z経過) と「対抗takeover宣言
なし」(research/log の02:29Z以降43 commit機械走査・該当0件) を機械確認し、
takeover宣言 `3f0aeb55` (observed HEAD `4948f19a`) で本レーンが継承した。
以下は両宣言分を併記した完了記録。**verdict不消費**。閉鎖・被覆・secured・
root勝敗の主張をしない。**標準11×11は本driveのどの時点でもUNKNOWNのまま**。

## 継承kit (takeover host fetch-back sha256照合済み・全値本host実測)

- scripts/runbatch.sh `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84` (pinned runner byte-clone)
- scripts/jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
- scripts/drive3_local_step.sh `41c5719c8253a9e199786e5fd87e70cc71ba85e22b3b80249df2082964a2f6c1` (v3宣言pin `41c5719c…` と完全一致)
- input/batch-keys.json `79fbd1664f4ad66ea62d9c8a8aa5aaff5d16bcdaa397895119ce4d8f47961232`
- input/ac030..ac054.input.csv 25 file 全件 MANIFEST-sha256 (139行版 `2b36d896…`) 行と一致
- output/status.log `07d839ab54a811b782cd79529c862c3827339e46e9942433012ae8378f790e2c` 44行 (drive-1 9行 + drive-2 35行) を append-only base として複製し使用

## takeover host val-gate (A `ce5cf7c9`)

published baselines 4 (at2m x2・first-15m・second-15m) に対し本host fresh 4走
(`.d3u-host.out` x4) を実行し node-exact 4/4 (wall_s除く):

- at2m (2M budget): result=0 n=2,000,000 x2
- 15M budget: result=2 n=3,651,923 / 5,040,200

fetch-back 4/4 byte一致 (A commit)。

## 実行 (v3 session scriptそのまま・「1 bash invocation = 1 wave」厳守)

13 waves + 最終 ALL-DONE 空キーガード確認 (rc=0・runbatch不)。flock単一
オーケストレータガード・orphan-livenessガード・incident-aware MISMATCH
pre-check (index済み2行では不発火) は宣言済みv3 deltaそのまま。2キー x 2 worker・
timeout 260 内側wrap (外側290s前に必ず発火)。

## 結果 — 25/25キー PASS (全行 2-pass fresh-cold p1==p2 node-exact・real_mismatch=0)

status.log 45-79行目 (drive-3分・append-only・最終44+35=79行)。

- **WIN 5行** (WIN-CONTINUE設計・wave継続・verdict不消費):
  - ac034 14,853,857 nodes (260s truncated retry込み: 初回wave 3でp2 truncated rc=124 → wave 4で fresh-cold 再実行)
  - ac041 10,959,413 / ac045 2,530,544 / ac048 4,701,704 / ac054 2,236,690 nodes
- **LOSS 16行** (nodes): ac030 7,072,780・ac031 10,125,646・ac033 5,912,106・
  ac035 8,904,715・ac037 3,818,788・ac038 5,018,863・ac039 11,367,923・
  ac040 3,119,506・ac042 3,007,885・ac043 6,210,354・ac046 5,216,563・
  ac049 3,095,290・ac050 8,586,185・ac051 9,625,374・ac052 5,349,962・
  ac053 4,251,146
- **EXHAUSTED 4行** (budget 15M nodes 15,000,000・honest UNKNOWN・同条件再probeなし):
  ac032 / ac036 / ac044 / ac047
- ac028/ac029 は原宣言の決定どおり出版済み incident-area pair をそのまま採用
  (fresh再probeなし・incident 2行 {MISMATCH p2空 x2・TRUNCATED-RETRY x2} は
  index済み・HARD-STOP不発火)。
- nodes合計 (resolve 21キー) 135,965,294/pass・EXHAUSTED 4キー 60,000,000/pass・
  計 195,965,294/pass (p1とp2それぞれ)。

## batch-30全体 (54キーすべて probe-level label 確定)

- drive-1: WIN 2 (ac002/ac003) / LOSS 2 (ac001/ac004)
- drive-2 (takeover): WIN 3 (ac020/ac026/ac027) / LOSS 20 / EXH 2 (ac006/ac013)
- drive-3 (takeover): WIN 5 / LOSS 16 / EXH 4
- **計: WIN 10 / LOSS 38 / EXHAUSTED 6** — いずれも verdict不消費 (probe-level
  label)。EXHAUSTED 6行は15M budgetでは未決着の honest UNKNOWN。

## 出版chain (全fetch-back byte一致)

1. takeover宣言 `3f0aeb55` (observed HEAD `4948f19a`・対抗宣言なし機械確認)
2. A `ce5cf7c9`: val-gate sidecar 4 (`.d3u-host.out`) — fetch-back 4/4
3. B checkpoint1 `c9e534f4`: ac030..ac040 raw 23 file (p1/p2 22 + ac034 truncated実行分 1) + status.log 59 行 — fetch-back 24/24
4. B checkpoint2 `092a655d`: ac041..ac054 raw 28 file + status.log 79行 — fetch-back 29/29
5. C `baf5136c`: README drive-3節追記 (178→228行) + MANIFEST-sha256 拡張
   (139→199行・.d3t/.d3u val-gate 8・drive3_local_step.sh・raw 51追加・README行
   /status.log行はdrive-3反映後shaに更新) — fetch-back 2/2 (commit-pin URL)
6. 完了log: 本file

実験dir: research/experiments/n11-centralreply-closure-class34269-batch30-20261123/

## 誠実記録・incident

1. **ac034 P2-TRUNCATED-RETRY 1件** (06:59:37Z status.log 行51): wave 3 (ac034+ac035)
   で ac034 の worker が 260s inner timeout で打ち切り (rc=124・retryable設計)。
   truncated file (`ac034.p2.truncated.065937.out`) は証拠として保存・出版済み。
   wave 4 で fresh-cold 再実行し PASS (nodes 14,853,857・p1==p2 node-exact)。
   truncated pass は一度も verdict を生成していない (`# replay_done` 不在のため
   runbatch host-interruption guard が再実行)。**値レベルのdivergenceなし**。
2. **real determinism MISMATCH 0件**・LOCK-BUSY 0回・ORPHAN-DETECTED 0回
   (v3ガード初の実運用で正常動作)。

## 運用知見 (今回new)

(a) **raw.githubusercontent.com のmain参照fetch-backはCDN lagで最大~5分 staleを
返す場合がある** (B1/B2は直後一致したがCでは旧版が返った)。**publish直後の
fetch-back検証は commit-pin URL** (raw/.../<commit sha>/path) を使えば確実
 (Cはcommit-pin URLでbyte一致を確認)。
(b) ac034のretryのように「timeout打ち切り→次waveでfresh-cold再実行」は
TRUNCATED-RETRY設計どおりに機能し、追加のdeclareなしでwave orchestration内で
解決した (260sは15M nodes EXHAUSTED級の重いキーの p1+p2 通しには厳しく、
WIN 14.85M nodes級でもp1完了・p2 truncatedになり得る)。

## UNKNOWN担保

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・EXHAUSTED行・incident-areaキー ac028/ac029・ac030..ac054を含む)**・
class 5804・class 34948 は本driveの実行・出版のどの時点でもUNKNOWNのまま。
nodes数・wall秒数を勝敗として読まない。被覆・secured・root勝敗の主張をしない。
WIN/LOSS採用はscrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption
Part (pinned merger `90711961…` 経由) のみで、本レーンは行使しない。

## レジューム (着手前に必ず最新main再取得・hourly並走注意)

- batch-30 (class 34269) は54キー全probe完了。次の候補:
  (a) **EXHAUSTED 6行 (ac006/ac013/ac032/ac036/ac044/ac047) の高budget (20M/25M/30M)
    再probeは別単一オーナー宣言** (Part CQ/CS/CT (batch-28)・DI (batch-31 ad043
    30M RESOLVED-WIN) のprecedent形式) ・**verdict不消費**。
  (b) **WIN 10行の第三実装交叉検証は別Part候補** (batch-28 b28-win46 queue
    registry形式のregistry注册を推奨) ・ただしadoptionはscrutiny owner C++ gate
    通過後の別adoption Part専権。
  (c) LOSS 38行のcanonical adoptionも同様にscrutiny gate後の別adoption Part
    (pinned merger経由・batch-29 CU/DB precedent)。
- 並走観察 (すべて非接触): Part DI (batch-31 ad043 30M再probe RESOLVED-WIN
  `1036c08e`)・Part CY drive-2 takeover (batch-31・checkpoint1 06:39:22Z)・
  K1283 z1面確定出版 (06:44-06:45Z・高速レーン)・Part DH/DF (b28 P4/P2
  thirdimpl・scaffold出版済み・outputsは本session開始時点で未出版) はいずれも
  本driveの領域に触れていない。
