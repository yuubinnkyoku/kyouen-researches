# Part CY 完了 log (2026-11-24): batch-31 (closure class 5804) drive-1 — WIN-HALT 28/55 probeキー・WIN 2行

単一オーナー: n11中央応答レーン (長期レーン)。宣言
`research/log/2026-11-24-part-cy-batch31-class5804-drive1-declaration.md`
(commit `afc1bcc5`・2026-11-24T01:37:39Z・publish-then-execute規約遵守) に引き続き、
本セッションで scaffold → val-gate → drive-1 → 出版までを完遂した。
対抗宣言なし・並走レーン (Part CI batch-29 / Part CP batch-30 / Part CX batch-28 /
Part CZ batch-29-CQ) はいずれも非接触 (observed HEAD列で継続確認)。

## 出版コミット列 (いずれもpush直前最新main再取得・fetch-back検証実施)

1. 宣言 note: `afc1bcc5` (01:37:39Z)
2. scaffold A (scripts 4 + val-gate baselines 8 + README): `6197f658` (01:38:18Z)
3. scaffold B (input 56ファイル: batch-keys.json `d058fddc…` + ad001..ad055 CSV):
   `3f77a007` (01:38:40Z・fetch-back 4ファイル byte一致)
4. val-gate fresh 4 sidecar (`.b31-host.out`): `190820c7`
5. drive-1 outputs (raw 56 + status.log): `39f29652`
6. C: README result追記 + MANIFEST-sha256 (130行): `1b970d4d`

## val-gate fresh 4 (宣言後・drive開始要件)

published baselines (`6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`) に対し本host
fresh再実行 **4/4 node-exact** (budget/result/nodes完全一致:

- at2m #1: budget 2,000,000, result 0, nodes 2,000,000
- at2m #2: budget 2,000,000, result 0, nodes 2,000,000
- first-15m: budget 15,000,000, result 2, nodes 3,651,923
- second-15m: budget 15,000,000, result 2, nodes 5,040,200

不一致0のためhard-stop不発動・drive-1開始条件成立。

## drive-1 結果 (2026-11-24T01:42:23Z..02:05:32Z UTC)

- 対象 ad001..ad028 (probe 28/55キー)。**pre-registered WIN-HALT wave end: distinct
  WIN 2行で停止** (残27キー ad029..ad055 は UNPROBED・fileless のまま drive-2へ)。
- **WIN 2行** (15M budget内解決・result=1):
  - **ad024** (s5 198576・key_lo 6053401124017274880・legal 86・
    nodes 4,360,661)
  - **ad028** (s5 207094・key_lo 6053682324116078592・legal 82・nodes 12,803,283)
- **LOSS(2) 26行** (ad001..ad023, ad025..ad027)。
- **EXHAUSTED 0行・TRUNCATED 0行・MISMATCH 0**。全28キー56 raw出力の p1/p2は
  `replay,` 行 f1-8 完全一致を機械確認 (2-pass fresh-cold決定性検証PASS)。
- 合計 nodes 138,729,770 (WIN 2行 17,163,944 + LOSS 26行 121,565,826)。
  nodes数はbookkeepingであり勝敗ではない。

## 機械簿記上の効用 (勝敗主張なし)

- class 5804 (rank 38) の unknown_now 55 から **28キー分が減算対象**
  (26 LOSS確定行 + WIN 2行・いずれもverdict不消費のhonest label)。残27 unknown
  (残 unknown 27 == 未probe キー ad029..ad055 の27。closure table再導出はreauditが機械実施)。
- drive-1 WIN 2行 (ad024/ad028) は **WIN候補としてwin-listに追加される**事を
  除き、採用・closure・被覆・secured・root勝敗の主張は一切しない。WIN採用は
  scrutiny owner C++第二実装 gate (`9193f5b6…`) 通過後の別adoption Part
  (pinned fail-closed merger `90711961…` 経由) のみ (本レーンは代行しない)。

## UNKNOWN担保 (最優先・維持)

**標準11×11空盤・19 central-reply roots・二石root・S2・class 5804 (本batchの
55キーすべて・WIN/LOSS行を含む) は本Partの実行・出版のどの時点でもUNKNOWNの
まま。** nodes数・wall秒数を勝敗として読まない。

## 次wave (未実施・後続Part)

- drive-2: 残27キー ad029..ad055 (WIN-HALT wave設計同一・別宣言後に実施)。
- batch-31 WIN行 (ad024/ad028) の scrutiny C++ gate はscrutiny owner専権
  (本レーン非代行)。
