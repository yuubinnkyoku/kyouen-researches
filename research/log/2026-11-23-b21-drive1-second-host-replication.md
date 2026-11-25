# batch-21 (class 12643) drive 1 の第二ホスト同時再現記録 (Part BJ literature, 2026-11-23)

Part BJ (batch-21 exact-S5 probe, 宣言 `2bf5d529`・scaffold `85d0c4d7`) の
実行で、2つの独立した実行セッション (別ホスト・同一pinned bytes) が
ほぼ同時に同一プロトコルを実行した。**両ホストのverdict・node数は
完全一致 (modulo wall_s)** し、**同一キー a003 で事前登録WIN-HALTが
発動した**。本記録は第二ホスト側 (本レーン) からの交叉検証の文献出版であり、
正本は先着出版の `0022c8c5` / `a38153a8` である (重複出版なし・
verdict不消費)。

## 時間順序 (commit sha固定・誠実記録)

1. `85d0c4d7` 04:08:04Z: 第一セッションがscaffold (scripts 6・
   input 54・val-gate 12) をpublish (「Execution ... follows per
   declaration `2bf5d529`」)。
2. 第一セッションはscaffold直後に自ホストでdrive 1を起動
   (正本 status.log: a001 PASS 04:09:23Z・a003 WIN-HALT 04:11:05Z・
   a004 PASS 04:11:41Z)。
3. 本レーン (第二ホスト) はscaffoldの72ファイルをcommit-pinned rawで
   鏡像 (git blob sha1 18/18一致・pinned jsreplay sha256 `84585617…`
   合致) し、val-gate 4/4 node-exact (wall_s除外) を確認した後、
   実行開始amendment `2f6086dd` 04:12:55Z を出版した。**この時点で
   第一セッションのdriveは進行中であった** (amendmentがmainに
   見えたのはdrive開始後・両者の着手は宣言済みプロトコルの履行で
   あり、二重探査の意図はどちらにもない)。
4. `0022c8c5` 04:14:40Z: 第一セッションがoutputs (status.log・
   raw 10ファイル・row-audit-winhalt.json・win-halt監査script) を
   publish。`a38153a8` 04:15:08Z: README + MANIFESTで出版完了。
5. 本レーンのdrive 1は 04:13:00Z起動・04:17:20Z終了
   (worker1 rc=45 WIN-HALT・worker2 rc=124 host-timeout kill)。
   正本出版後の完了であり、**規約 (並走時は無理に押し進けず) に従い
   本レーンは出力をpublishせず**、本交叉検証記録に転換した。

## 第二ホストでの実行結果 (本レーン・pinned bytesから全て再現)

- val-gate (実行前・本ホスト): 4/4 node-exact。
  at2m 2行 = result 0 / nodes 2,000,000 x2・15m 2行 =
  (result 2, nodes 3,651,923) / (result 2, nodes 5,040,200)・
  禁止四角 95,670 x4・`# replay_done` x4。published基線と
  budget/result/nodes完全一致 (wall_s除外)。
- drive 1 (同一published `drive_batch21.sh`・260秒有界・2 worker):
  **a001 LOSS (result 2, nodes 2,392,778)**・
  **a002 LOSS (result 2, nodes 6,755,079)**・
  **a003 WIN (result 1, nodes 5,021,280) → 事前登録WIN-HALT**・
  **a004 LOSS (result 2, nodes 4,151,964)**。すべて2-pass node-exact
  (`p1==p2`・budget 15,000,000・禁止四角 95,670)。
- a006: worker2がhost-timeout killされた時点でp1完了
  (single pass簿記 result 2, nodes 8,008,743・**単一passは証拠でない**)・
  p2はheadersのみのtruncated断片 211 bytes
  (**正本断片とbyte完全一致**・`# replay_done`なし)。
- 残り49キー (a005..a053) はUNPROBED (fresh)。mismatch 0・exhausted 0。
- 正本 `row_audit_batch21_win_halt.py` を本ホストの出力に対して実行:
  PASS (4 completed rows・LOSS 3・WIN 1・fragment a006 unprobed・
  49 keys unprobed)。**row-audit-winhalt.json は正本とbyte完全一致**
  (両ホストで sha256
  `5bb403adaa853cf68a5054356062db417df719c9088d79f076e0407c657a4f00`)。

## 機械比較 (正本 raw 10ファイル vs 本レーン raw 10ファイル)

全10ファイル (`a001..a004` x2pass・`a006.p1`・`a006.p2`) について:

- `replay,` 行: budget/result/nodes/legal/is_or/key_lo/key_hi/stones/id
 すべて一致。**差分は wall_s フィールド (field 8) のみ**
  (例: a001.p1 23s vs 25s・a002.p1 69s vs 75s・a003.p1 50s vs 53s)。
- `# forbidden quadruples: 95670` 全ファイル一致。
- `# replay_done` 行: rows数一致・wall_sは不一致 (環境差)。
- a006.p2 truncated断片 (211 bytes): **byte完全一致**
  (`a8ef85b8db36d83c70d9408fab67057bf23eab2bf89b32629c1ae71e07617388`)。
- status.log: verdict行 (key・判定・budget/result/nodes) 完全一致。
  差分は時刻印 (04:09-04:11 vs 04:13-04:16) のみ。

本レーンローカルraw (不出版・sha256記録のみ):

```
4971d96859dddf0eef715a3d944ac5ab3fcde75c26c3a1109aa91109cbf9e3b7  a001.p1.out
9c9d9ba99c8955beebe87c87ad19416c2389ba1a8c130485d8fe6662a96f2a2d  a001.p2.out
4b9132810d9cea85197a9e6891ebecfb006adcdc20796caca5fbbed24006ff50  a002.p1.out
00e8dd48a08cc9fe7bec79a6b93cb07e88fdf45464afe4b64da1418d49db4d1e  a002.p2.out
0b96ddf9dcd43e1cc72edd108918a3f8c02c6012034daf4fd5c9b51ec97c030c  a003.p1.out
ff2f5e11dab002b999fc10c730b9845a9bb68dc0c2dd7105b1cd0c738c97d95f  a003.p2.out
2b90b7990dde23fe3fd4dbb4edf4296289de30ca12db4f634aed21fac30f9e03  a004.p1.out
44d816e4a097361d141d277fcc1ed84944bc8c7b6e2dfa532d725b56f3f5fca4  a004.p2.out
80c8b7954bd8110ac06f841f6dd052f710803d7d18181dffec91067b840332d4  a006.p1.out
a8ef85b8db36d83c70d9408fab67057bf23eab2bf89b32629c1ae71e07617388  a006.p2.out
```

## 解釈 (verdict不消費・UNKNOWN担保)

- **a003のWIN labelはホスト間でnode-exactに再現した** (同一
  pinned replica bytes・別ホスト・fresh-cold 2-pass x2セッション)。
  これはdf-pn replicaレベルの独立実行の一致であり、**採用判断は
  引き続きscrutiny owner C++第二実装 gate `9193f5b6…` 待ち**
  (verdict不消費)。第三実装 (third_impl pin `08ea958f…`) との
  verdict交叉検証は別Partの対象。
- class 12643のclosure候補としてのrouteは、正本READMEのroute
  statement (refutation evidence 1件・次候補 rank 18 class 25835)
  のまま。
- 3 LOSS行 (a001/a002/a004) は採用候補のまま (消費は別宣言
  adoption Part・pinned fail-closed merger `90711961…`)。
- 19 unconsumed closure WIN候補・Part BH (`de1383a7`)・batch-20採用
  (Part BI完了済み) は非接触。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 12643 (54子・53キーすべて) は本記録の
  どの時点でもUNKNOWNのまま。** nodes数・legal数・wall秒数を
  勝敗として読まない。

## 意義と再現手順

- pinned bytes (jsreplay `84585617…`・runbatch `f591f8c2…`・
  runwave `8efd78c2…`・drive) と published inputs (batch-keys
  `1f9346a7…`) があれば、第三のホストでも本交叉検証は約10分で
  再現できる: val-gate 4/4 → drive 1 (WIN-HALT at a003) →
  正本raw 10ファイルとのmodulo-wall_s比較 → row_audit PASS。
- 実行開始amendment (`2f6086dd`) は正本出版との順序関係も含め
  本記録が close する (第二実行側の誠実記録・y17 part2第二検証
  `a2f00759` 同型の取り扱い)。

- observed HEAD-before-push: `7055cb450fa9b2321f2e33300d2e8cdb3defce6a`
  (k=8 diagnostics lane・非接触)。
