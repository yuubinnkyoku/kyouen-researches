# Part DK完了log (takeover): batch-30 (class 34269) 最終EXHAUSTED残1行 ac013 の25M再probe完結 — 2-pass fresh-cold node-exact PASS・nodes 21,954,135・honest label result=2・原host pre-wipe観測と3-way nodes一致・verdict不消費

実験dir: `research/experiments/n11-centralreply-closure-class34269-batch30-exh1-25m-20261124/`
(takeover宣言: `research/log/2026-11-24-part-dk-batch30-exh1-25m-takeover.md`・commit `6c92d945ca`)

## 出版chain (全fetch-back byte一致)

1. 原宣言 `e411045b` (08:11:41Z) — 原lane (publish-then-execute)。
2. 原lane A scaffold `890e6186` (08:12:48Z) — kit 9 file (jsreplay byte-clone
   `84585617…` / runner_dk `9048c329…` / inputs `797467ec…`/`edf4f661…` /
   val-gate 4) + 原host VG1/VG2 PASS 出版 (`.dkvvg1/dkvvg2-host.out`)。
3. 原lane interim `2117ea73` (08:21:58Z) — invocation A (P1 完走: result=2
   nodes=21,954,135 wall_s=126) 後、invocation B (P2) 発行時に実行環境outage
   (honest非PASS主張・`output/INTERIM-P1-NOTE-20261124.md` 出版)。以降3.5h停滞。
4. **takeover宣言 `6c92d945ca` (11:43:17Z)** — earliest_takeover
   (=原宣言08:11:41Z+3.5h=11:41:41Z) 経過後出版。対抗takeoverなし・原オーナー
   再開なし機械確認済み。kit 6/6 sha pin fetch-back一致を宣言前に実施。
5. **B outputs `3bb1e8d2b0`** — 本host fresh実行の
   `output/raw/ac013.p1.out` / `ac013.p2.out` / `output/status.log` /
   `val-gate/first-25m.dkt-vg1-host.out` / `val-gate/second-25m.dkt-vg2-host.out`
   (5 file・fetch-back sha256一致 5/5)。
6. **C `c8e4a6e6`** — README実行記録更新 + MANIFEST-sha256 (15 file)。
   commit-pinned raw sweep 15/15 sha256一致。

## 本host実行の全工程 (takeover lane・2026-11-24T11:43-11:50Z)

- **VG1 re-run** (budget 25M): result=2 nodes=3,651,923 — published baseline
  (`first-25m.dkvvg1-host.out`) と node-exact・budget字段のみ25M — PASS
  (wall_s=19)。VG2 re-run: result=2 nodes=5,040,200 — PASS (wall_s=27)。
  不一致0・hard-stop不発火。
- **invocation A (p1 fresh-cold, budget 25M)**: `replay,0,5,93,0,25000000,2,
  21954135,126,…` — result=2 (honest LOSS label)・nodes 21,954,135・wall_s=126
  ・replay_done付。
- **invocation B (p2 fresh-cold, 同条件)**: nodes 21,954,135・wall_s=129・
  replay_done付。
- **invocation C (pinned runner_dk.sh ac013)**: **PASS 25000000,2,21954135
  (p1==p2 node-exact)** rc=0・status.log 1行 (2026-11-24T11:49:57Z)。
  STOP rules (WIN 45 / MISMATCH 42 / 43,44) 不発火。
- **原host pre-wipe P1観測 (nodes=21,954,135) と本host fresh両pass が nodes
  完全一致 (3-way一致・wall_sは非比較字段)**。

## 何が確定したか (bookkeeping・主張の範囲)

- **ac013 の honest label: 2-pass fresh-cold node-exact PASS で result=2
  (budget 25M)**。supersede鎖: 15M EXHAUSTED (batch-30 drive-2・01:56:44Z) →
  20M EXHAUSTED (Part DJ `bcd67982`) → **25M PASS result=2 (本Part)**。
- Part DJ完了log (`41c9ede4`) のとおり batch-30 54キーのEXHAUSTED残はac013
  1行のみだったため、**batch-30 にEXHAUSTED行は残っていない** (54キーすべてが
  15M-31M-等何れかのbudgetでhonest labelを持つ)。これはprobe label bookkeeping
  であり、閉鎖・被覆・secured coverage・root勝敗の主張ではない。
- ac013のhonest label (result=2) は**どこにも消費していない** (canonical chain
  不変・DL base `60222707…` 6,405行への追記は別adoption Part専権)。
- verdict不消費。WIN/LOSS採用はscrutiny owner C++第二実装 gate `9193f5b6…`
  通過後の別adoption Part (pinned fail-closed merger `90711961…` 経由) のみ。

## honest記録

- C commit (`c8e4a6e6`) のcommit message文言に誤りがある (「MANIFEST自信を
  raitaiso外」=「MANIFEST自身をmapping対象外」の取り違え文字化け)。内容
  (README本文・MANIFEST全15行) はfetch-back byte一致で検証済み・実害なし。
- takeover宣言のローカル草稿段階でobserved HEAD shaを2文字分typoしたが、
  出版前にroundtrip照合 (fetch-back sha256比較) で検出し、出版bytesは正本
  (40文字) で確定した (ローカルtypoはrepoに入っていない)。当初README原案の
  括弧未閉鎖1箇所も出版前に機械修正済み。
- 本Partは原宣言の設計 (budget 25M・cross-invocation・VG期待値・出版計画) を
  1文字も変更していない (takeoverは実行継承のみ)。val-gate host出力のsuffixは
  宣言どおり `.dkt-vg1/2-host.out` (原hostの `.dkvvg1/2-host.out` は不変)。

## UNKNOWN担保 (不変)

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・ac013を含む)**・class 5804・class 8730 は本Partの実行・出版の
どの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗や距離として読まない。
被覆・secured・root勝敗の主張をしない。

## 次step (継承メモ・予約ではない)

- batch-30 (class 34269) のLOSS行群 (ac013含む) は canonical chain
  (`60222707…` 6,405行) に**まだ採用されていない** (DL chainの成分は
  b28loss1/b28loss7/b29loss16/b29loss37/b31loss51 = batch-28/29/31分のみ)。
  batch-30のLOSS行 (DJ 20M reprobe解決4行 + 本Part ac013 + drive-1..3の
  LOSS行) を FAIL-CLOSED merger (`90711961…`) で接続する別adoption Partが
  候補 (DL `c92959a8`-`405da370` と同じ工程構成)。WIN行 (ac006等) は
  scrutiny待ちで採用対象外。
- closure tableのclass 34269 unknown_now 54 は batch-30 adoption後に
  refresh reauditで機械更新される (unknown → WIN行数のみ)。
- Part DH (b28 P4 第三実装)・Part DM (batch-32 class 8730 drive-1) は
  他lane進行中・非接触継続。DH takeover (of-takeover) のearliestは
  09:40:53Z + 3.5h ≈ 13:10Z (先方のinterim以降の進行を最優先確認)。
