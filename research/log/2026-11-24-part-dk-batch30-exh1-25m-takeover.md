# Part DK takeover宣言: batch-30 (class 34269) 最終EXHAUSTED残1行 ac013 の25M high-budget再probe — 原宣言からの単一オーナーtakeover (publish-then-execute)

Part DK (原宣言 `e411045b`・2026-11-24T08:11:41Z) を、停滞3.5h基準の経過後に
takeoverする (本lane = n11長期レーン・takeover executor)。**verdict不消費**。
閉鎖・被覆・secured・root勝敗の主張はしない。**標準11×11は本Partのどの時点でも
UNKNOWNのまま。**

## takeover事由の機械確認 (事実のみ)

- 原宣言 `e411045b` (08:11:41Z) → A scaffold `890e6186` (08:12:48Z) →
  interim note `2117ea737` (08:21:58Z・P2 invocation中の実行環境outage・
  非PASS主張) 以降、**DK実験dirへの追commitなし・outputsなし**
  (list_commits path指定で機械確認: 実験dirのgit historyは上記2 commitのみ・
  `output/raw/` pass file・`status.log` は未出版のまま)。
  **earliest_takeover = 08:11:41Z + 3.5h = 11:41:41Z 経過後に本宣言を出版**。
- 対抗takeover宣言なし・原オーナー出版の再開なし (直前の最新main再取得・
  2026-11-24T11:4xZ時点で機械確認)。
- observed HEAD at push: `6bcbbc957bcc743f113572d667d383796137cfe3` (Part DM
  val-gate 11:04:39Z・並走中のPart DM batch-32 (class 8730) およびPart DH
  (b28 P4 第三実装交叉検証・takeover `a4e00aa3` + interim `076e05c1`) は
  いずれも非接触)。

## kit再取得・pin照合 (published bytesのみ・takeover前に実施済み)

原宣言の事前登録pinと、main published bytes (commit `890e6186` scaffold) の
fetch・sha256照合が**6/6 byte 一致**:

- scripts/jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
- scripts/runner_dk.sh `9048c3291d981d52c846bc177bb727f95827d88892c6fd44ae84c5a110b4ac1c`
- input/batch-keys.json `797467ec1009fc835c3fa9b92a29ebdbac6c3431777abbcde11a8a6fc1df88d5`
- input/ac013.input.csv `edf4f6619bdf98208af758b19d03b454a9daa89b9e4bdcf214963b29848b0650`
- val-gate input CSV 2本 `ecc0299b…` / `56aacb71…` (batch-28..31系のsanctioned
  val-gate input・batch-30/31 MANIFEST系と同一bytes)
- published baselines: `first-25m.dkvvg1-host.out` (replay row result=2
  nodes=3,651,923 wall=18・replay_done付) / `second-25m.dkvvg2-host.out`
  (result=2 nodes=5,040,200 wall=26) — 原hostによるVG1/VG2 PASS 出版済み。

## 実行設計 (原宣言のcross-invocation step designを継承・変更なし)

原hostのinterim note (`output/INTERIM-P1-NOTE-20261124.md`) のとおり、原hostの
P1 raw (観測: result=2 nodes=21,954,135 wall_s=126・**単pass観測で非PASS**) は
ローカル消失のおそれがあり、**本takeoverでは両passをpublished kitから
fresh-coldに再実行して出版する** (DJ precedent: pre-wipe観測との一致を照合記録する)。

1. VG re-run (hygiene・本host fresh): first/second-15m inputをbudget 25Mで実行
   → 期待 result=2 nodes=3,651,923 / 5,040,200 (published baselinesと
   node-exact・budget字段のみ25M)。不一致ならhard-stop。
   本hostの出力は `.dkt-vg1-host.out` / `.dkt-vg2-host.out` として出版
   (原host `.dkvvg1/dkvvg2-host.out` は不変)。
2. invocation A: jsreplay p1 (budget 25M) fresh-cold単独 → `output/raw/ac013.p1.out`。
3. invocation B: jsreplay p2 (同条件fresh-cold) → `output/raw/ac013.p2.out`。
4. invocation C: `runner_dk.sh ac013` (pinned byte-clone・replay_done guard +
   p1/p2 node-exact比較 + status.log append + STOP rules WIN rc=45 /
   MISMATCH rc=42 / p1,p2 fail rc=43,44・EXHAUSTED (result 0) はhonest
   UNKNOWN labelで継続)。

事前登録: probe結果は**非予告** (LOSS/EXHAUSTED/WINいずれも起こり得る)。
Nodes数はbookkeepingであり勝敗ではない。原interim観測 (21,954,135) との
一致は照合記録のみで、PASS判定は本host fresh p1==p2 node-exact +
pinned runner完了のみ。

## 出版計画 (原宣言のB-D工程をtakeoverとして実施)

1. B outputs: `output/raw/ac013.p1.out` / `output/raw/ac013.p2.out` /
   `output/status.log` / `val-gate/*.dkt-vg*-host.out` 2本。
2. C: READMEの実行記録更新 + MANIFEST-sha256 (本Part出版分の全file byte pin)。
3. 完了log: `research/log/2026-11-24-part-dk-batch30-exh1-25m-takeover-completion.md`
   (原宣言完了log名との衝突回避・takeoverであることを明記)。

## UNKNOWN担保 (不変・原宣言文言を継承)

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251・**class 34269
(54キーすべて・ac013を含む)**・class 5804・class 8730 は本Partの実行・出版の
どの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗や距離として読まない。
WIN/LOSS採用はscrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption
Part (pinned fail-closed merger `90711961…` 経由) のみで、本laneは行使しない。
