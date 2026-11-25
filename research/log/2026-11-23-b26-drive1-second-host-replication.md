# batch-26 (class 1849) drive 1 の第二ホスト同時再現記録 (Part BQ literature, 2026-11-23)

Part BQ (batch-26 exact-S5 probe, 宣言 `8e64ba1c`・scaffold `309386d578`) の
実行で、2つの独立した実行セッション (別ホスト・同一pinned bytes) が
ほぼ同時に同一プロトコルを実行した。**両ホストのverdict・node数は完全
一致 (modulo wall_s)** し、**同一キー l028 で事前登録WIN-HALTが発動した**。
本記録は第二ホスト側 (本レーン) からの交叉検証の文献出版であり、
正本は先着出版の `32fbe3bb99` (outputs) / `9eda46aff1` (README+MANIFEST)
/ `a2e1d76b43` (note status update) である (重複出版なし・verdict不消費)。

## 時間順序 (commit sha固定・誠実記録)

1. `8e64ba1c` 07:54:32Z: 宣言セッションがPart BQ宣言 (publish-then-execute)
   を出版。
2. `309386d578` 07:55:20Z: scaffold 73ファイル (scripts 7 + inputs 54 +
   val-gate 12) を出版。宣言セッションはscaffold直後に自ホストでdriveを
   起動 (正本status.logの最初のPASS行は 07:56:32Z l001)。**この実行開始
   はmain上には何も合流しない** (status.log は outputs と一緒に
   08:22:55Zまで出版されない)。
3. 本レーン (第二ホスト) は 08:01:37Z 時点のHEAD `300dd361` (07:58:30Z
   K1252・非接触) を観測し、batch-26のoutputs・実行開始を示すコミットが
   mainに存在しないことを確認のうえ、batch-22/24で確立したkit-takeover
   慣行 (Published scaffoldを使った後続実行・Part BL型) に従って執行を
   開始した: 73ファイルをcommit-pinned rawで鏡像 (git blob sha1 73/73
   一致・宣言記載sha256 pin全合致: batch-keys `f1ea43ae…`・maker
   `a74250d6…`・row audits `3bcf7857…`/`33ffbce5…`・runners
   `f591f8c2…`/`8efd78c2…`・jsreplay `84585617…`) → val-gate 4/4
   node-exact → **drive 1起動 08:04:20Z**。すなわち本レーン着手時点で
   第一セッションのdriveはすでに進行中であったが、それはmainからは
   観測不可能であった。両者の着手はいずれも宣言済みプロトコルの
   履行であり、二重探査の意図はどちらにもない (batch-21 `ad487a2f`
   と同型の同時並走)。
4. 第一セッションは outputs `32fbe3bb99` 08:22:55Z (status.log・raw・
   row-audit-winhalt.json) → `9eda46aff1` 08:23:49Z (README+MANIFEST)
   → `a2e1d76b43` 08:26:05Z (note Part BQ status update) で出版完了
   (drive終了 08:22:05Z頃・30 LOSS + l028 WIN + fragment l035 +
   21 fileless UNPROBED)。
5. 本レーンのdriveは 08:04:20Z起動・6回の260s有界invocationで
   08:30:38Z終了 (worker2 rc=45 WIN-HALT at l028・worker1 rc=124
   host-timeout kill)。HEAD取り直しで第一セッションの出版を検知した
   のは最終invocation直後。**規約 (並走時は無理に押し進めず) に従い
   本レーンはoutputs/README/MANIFEST/noteをpublishせず**、本交叉検証
   記録に転換した。

## 第二ホストでの実行結果 (本レーン・pinned bytesからすべて再現)

- val-gate (実行前・本ホスト): 4/4 node-exact。at2m 2行 = result 0 /
  nodes 2,000,000 ×2・15m 2行 = (result 2, nodes 3,651,923) /
  (result 2, nodes 5,040,200)・禁止四角 95,670 ×4・`# replay_done` ×4
  (published-baselineとbudget/result/nodes完全一致・wall_s比較外)。
- drive 1 (同一published `drive_batch26.sh`・260s有界・2 worker):
  **33完成行 = LOSS 32 + l028 WIN (result 1, nodes 4,893,014) → 事前登録
  WIN-HALT rc=45**。すべてtwo-pass node-exact (p1==p2・budget
  15,000,000・exhausted 0・mismatch 0)。
- l028 WIN (honest label): key (1153485622925590528, 0)・s5 81011・
  legal 88・membership 3・wall 53/50s・**正本と同一nodes**。
- fragment 2キー: l031 (p1は211 bytesのヘッダのみtruncated断片・p2なし)
  と l038 (p1完成単一passはbookkeeping result 2, nodes 1,577,298 のみ・
  p2は211 bytes truncated。単一passは証拠でない)。いずれもUNPROBED。
- fileless UNPROBED 18キー・truncated retry断片 9本 (いずれも211 bytes
  ヘッダのみ)。
- row-audit-winhalt (published `row_audit_batch26_win_halt.py`):
  PASS (33 completed rows・LOSS 32・WIN 1・fragment l031/l038・
  fileless 18)・3回実行byte一致 (json sha256 `0b2c5d24…`)・tamper
  battery 3/3検出 (l028 p1 verdict反転 1→2 / filelessキーへの偽PASS行
  / status.log key-id改ざん)・scratch上で実施し実験files無改変・
  clean control PASS。

## 機械比較 (正本 status.log 31行 vs 本レーン 33行)

- **共通完成行 29行 (l001..l029): verdict行 (key・判定・budget/result/
  nodes) は29/29完全一致・不一致ゼロ** (l028 WINを含む: `15000000,
  1,4893014`)。
- 正本のみの行: l031 PASS (2, 3,372,974)・l033 PASS (2, 3,117,894)。
- 本レーンのみの行: l030 PASS (2, 4,237,589)・l032 PASS (2, 1,753,293)・
  l034 PASS (2, 4,229,600)・l036 PASS (2, 4,286,829)。
- **共通29キー×2pass = 58生値ファイル全件: ヘッダ・禁止四角行
  (95,670)・replay行 (id/stones/legal/is_or/budget/result/nodes/
  key_lo/key_hi)・`# replay_done` marker すべて一致。差分はwall_s
  フィールドのみ** (正本host 19..107s・本ホスト 18..104s)。
- truncated断片 (211 bytesヘッダのみ) は**両ホストでbyte完全一致**
  (git blob sha1 `b4793b17…`・batch-21 a006.p2断片と同じ内容)。
- 両ホストとも**事前登録WIN-HALTが同一キー l028 (s5 index 81011) で
  発動**: l028 (28番目の unconsumed closure WIN候補) は two-host
  two-pass node-exact で相互補強された (第三実装交叉検証は別Partの
  宣言で行う)。

## 本レーンにしかない行の取り扱い (route statementのみ)

l030/l032/l034/l036 の4行は本レーンのtwo-pass完成行 (honest label
result 2) だが、**正本batch-26の行集合には含まれない**。正本の
row-audit (`ed721587…`) ではこの4キーはfileless UNPROBEDであり、
本記録はそれを書き換えない (K項目・closure表への反映も行わない)。
同様に正本のみの l031/l033 も本レーンでは未完成 (l031はfragment)。continuationがこれらのキーをprobeする場合はfresh-cold再導出が
 常に優先する。verdictは一切消費していない (どちらの行集合も)。
 採用判断は scrutiny owner C++第二実装 gate pin `9193f5b6…` 待ちで
 本レーンは代行しない。canonical cache 6,235行 `f6649fe3…` は
 read-only・不変 (batch-26 rowsは書込んでいない・両ホストとも)。

## 本レーンローカルraw (不出版・sha256記録のみ)

```
f54213288c84f78d28d90a920234199963258640817b876bc903c69af7035db4  output/raw/l028.p1.out
391110e82982105c111860f743fd52f08ef3ea48a8dfe05892c9fb757e1dcfc5  output/raw/l028.p2.out
baea9f56afb173ad42b39946dfb8aaf82f17c45cc2e763b0da62182c254f32f6  output/raw/l030.p1.out
a661f19c0dcd133e95afbdc32e44742918f54e541329f776188690cda695ec12  output/raw/l030.p2.out
9881f4500f5a3d100a6f88a073d9028cc217f13204d75503cc38caa113fac39b  output/raw/l032.p1.out
9881f4500f5a3d100a6f88a073d9028cc217f13204d75503cc38caa113fac39b  output/raw/l032.p2.out
9c5e40de543a9127f92d5cfb07fd318e2fa6173c55dea33bc10d433350b9128d  output/raw/l034.p1.out
9c5e40de543a9127f92d5cfb07fd318e2fa6173c55dea33bc10d433350b9128d  output/raw/l034.p2.out
539c32c35391bf95b4ebb84dfcca2dc2ee476c3db8dd3922543452857865d3aa  output/raw/l036.p1.out
539c32c35391bf95b4ebb84dfcca2dc2ee476c3db8dd3922543452857865d3aa  output/raw/l036.p2.out
a8ef85b8db36d83c70d9408fab67057bf23eab2bf89b32629c1ae71e07617388  output/raw/l031.p1.out (211 bytes truncated断片)
d4db39f89ae6e56b82321656a0106ff7ce6b4704de78cf40d84f4ade4b51507b  output/raw/l038.p1.out (完成単一pass・bookkeeping)
a8ef85b8db36d83c70d9408fab67057bf23eab2bf89b32629c1ae71e07617388  output/raw/l038.p2.out (211 bytes truncated断片)
e2698fae27a508c37ab8a6d9e73db788125952220d8c4fca8dc774bc2828e827  output/status.log
0b2c5d24fcc196a4599fda27748198b4b921ea5292f0cd59ae7ea9d0f9938596  output/row-audit-winhalt.json
26bf38a4c34b76748f692082a65f4ffe2b2d55e27176424ceaaed76535e099b4  output/val-gate-execution-host/at2m-s5-1152921504606851072-536870946.execution-host.out
11f84ee695b29fcd33b8b8a98fd98956b867992ab801911b6b903c3d973cfeb6  output/val-gate-execution-host/at2m-s5-1188950301626860544-536870912.execution-host.out
93073aa1a09092c51d85d4dd0acb039ba5c8bf60ddef6ba2eac08bce24f89956  output/val-gate-execution-host/first-15m-s5-1152921504606851072-536870946.execution-host.out
0d6f551d501e0dcf51e50e9dae7d8e249e97b622740df594e8770cb8dc57b20c  output/val-gate-execution-host/second-15m-s5-1188950301626860544-536870912.execution-host.out
```

## 運用知見 (今回new)

(a) **publish-then-execute宣言の実行開始は、outputsが出版されるまで
mainから観測できない**: 宣言+scaffold出版→outputs出版の間に第二
セッションがtakeoverしても衝突は原理的に検知できない。第二セッション
側の防衛としては (i) 実行開始前のHEAD・コミット確認だけでは不十分で
あること (今回は08:01:37Zの確認で文言上の実行中マーカーは存在しなかっ
た)、(ii) 同一kitの並走実行は決定論的であるため**衝突しても毀損は
なく交叉検証価値が残る**こと、の2点を運用正則として銘記する
(batch-21 `ad487a2f` と同型・2例目)。衝突後はfirst-completerの出版を
正本とし、後着側は重複出版せず文献記録に転換する (今回の行動)。

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 1849 (53キーすべて・l028を含む) は
どの時点でもUNKNOWNのまま。** nodes数・expansions数を勝敗として読ま
ない。WIN/LOSS採用は別宣言の adoption Part (pinned fail-closed merger
`90711961`) 経由のみ。
