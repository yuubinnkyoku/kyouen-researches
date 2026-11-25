# n11 night batch 5 (最終探索候補): 162106 25M予算拡張でSOLVED(WIN)＋独立検証、free=3残2件の2M probe

基準: main `cf2e7734` ＋ 未コミット先行実験 (adaptive系4件 / night-batch1..4 /
night-plan-update3..6)。本実験は既存実験・K0423パイロット・全既存出力・
night batch 1..4 成果物・履歴・knowledge正本・生成物・共有solver論理を
変更せず、`research/experiments/n11-night-batch5-20261014/` に結果を分離保存する。
再生成traceは `build/n11-night-batch5-traces/` (gitignore、使い捨て)。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
WIN/LOSS/UNKNOWNをそのまま保存し推定補完しない。UNKNOWNは証拠ではない。
全run逐次 (workers=1、上限2以下)・memo 20・cold TT (1行1プロセス、`--s5-cache`なし)・
capture (`--proof-dag`)・order count (mode 0)。solver binary SHA256
`72f1da29…`・check_trace (source SHA256 `0f890cb4…`・binary SHA256 `4e51efee…`)
は先行batchと同一実体を読み取り専用で使用。
144019 / 144692 (UNKNOWN@10M) と確定集合・K0423は非接触。

## Task 0: receipt発行済み trace CSV の削除によるディスク確保

`build/n11-night-batch1..4-traces/` のうち、独立receipt (terminal-dag.json.gz ＋
receipt.json ＋ pruned roundtrip済み) が発行済みの使い捨て proof CSV のみ削除した。
receipt・DAG・pruned・manifest 本体は一切削除していない。削除前後で
tracked 差分0 (`git status --porcelain -uno` / `git diff` とも空) を確認。

| 削除ファイル | bytes | receipt |
|---|---:|---|
| `build/n11-night-batch4-traces/nighta25m-131631-proof.csv` | 2,834,089,071 | `n11-night-batch4-20261014/output/nighta25m-131631-receipt.json` (trace SHA256一致・pruned roundtrip ✓) |

batch1/2/3 traces は既に空。確保量 2,834,089,071 bytes (約2.64 GiB)。
本バッチの `nighta25m-162106-proof.csv` も receipt 発行後に同基準で削除済み
(2,310,149,527 bytes)。

## Task A: 162106 の予算拡張run (node予算25M、新規run)

night batch 4 の10M run (nightb10m-162106) は NODE_LIMIT で root 99子中58子WIN・
残41子UNKNOWNだった。これは同一条件の再実行ではなく、node予算のみ10M→25Mへ
拡張した**新規run**である (frozen 10M行は manifest 内に参照保存)。

| S5索引 | status | 先手結果 | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN | trace bytes |
|---:|---|---|---:|---:|---:|---|---:|
| 162106 | SOLVED | **WIN (verdict=1)** | 18,141,378 | 981.0 | 2,400,120 | 99 / 0 / 0 | 2,310,149,527 |

18,141,378 nodesでSOLVED (25M予算は未消化)。残41子UNKNOWNは18.1M到達前に解けた。
terminal-only receipt (`nighta25m-162106-receipt.json`) を発行し、
Python dag_verifier 再検証と全フィールド一致を確認した:

- DAG: 2,372,823 nodes / 3,500,917 edges / 352,077 終局 / **trusted_leaves = 0**
- pruned roundtrip ✓ (orphan 0、replay 17.7s)、certificate json.gz 67,966,581 bytes、
  pruned 51,140,441 bytes
- checker wall 281.2s・peak RSS 3,229,740 KiB (OOMなし)、Python照合 wall 2,015.1s
  (verdict=1・nodes/edges/terminal_nodes/trusted_leaves 全一致 ✓)

これで162106はsolver-trustedから**独立終局証拠 (WIN)** へ昇格した。
126017・197665・206386・131631 に次ぐ、conflict-closure系の新規独立WIN証拠である
(ranking上 WIN時18分岐FREE・3選択invalidated・greedy Δ49)。
証明計画への反映 (plan-update系) は本バッチの範囲外。
具体DAGのLean内形式検査を意味しない。証拠への昇格は receipt のみが行い、
raw solver label は solver-trusted のまま保持している。

## Task B: free=3 残2件の初回2M probe ＋ 193768 の10M拡張

night batch 3 の未着手pool 5件から3件を選択済みのため、残りは
**193768 / 196002** (いずれも free=3) の2件のみ。両件とも初回2M probeを1件ずつ実施し、
有望件 (root子WIN数が2件中最多の193768) に限り許可された10M拡張を1件適用した。
25M等の更なる拡張は本バッチでは行っていない。

| S5索引 | run | status | 先手結果 | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN |
|---:|---|---|---|---:|---:|---:|---|
| 196002 | 2M 初回 | NODE_LIMIT | UNKNOWN | 2,000,000 | 20.4 | 396,356 | 11 / 0 / 89 |
| 193768 | 2M 初回 | NODE_LIMIT | UNKNOWN | 2,000,000 | 19.7 | 395,664 | 21 / 0 / 81 |
| 193768 | 10M 拡張 (新規run) | NODE_LIMIT | UNKNOWN | 10,000,000 | 104.1 | 1,536,676 | 61 / 0 / 41 |

3/3件がNODE_LIMIT = UNKNOWN。推定補完はせず、証拠への昇格もない。
193768 10M時点の 61/102 WIN子は batch4 の162106 10M時 (58/99) と同程度の水準だが、
本バッチの拡張枠は1件のみで両件への適用はできず、25Mへの再拡張指示もなかったため
UNKNOWNのまま保存した。

## 保存物

- `output/nighta25m-manifest.json` / `output/nighta25m-162106.csv` / `.log`
- `output/nighta25m-162106-receipt.json` / `-terminal-dag.json.gz` / `-pruned.csv.gz` /
  `-python-comparison.json`
- `output/nightb2m-manifest.json` / `output/nightb2m-{193768,196002}.csv` / `.log`
- `output/nightb10m-manifest.json` / `output/nightb10m-193768.csv` / `.log`
- `input/s5-{162106,193768,196002}.csv` (凍結 pilots.json から再物質化、
  `n11-conflict-closure-20261013/input` とバイト一致)

## 申送り

- 162106 (WIN) は独立終局証拠済み。plan-update系でどう活用するかは次タスク。
- 193768 は 10M で 61/102 WIN子・残41 UNKNOWN。25M拡張で SOLVED 可能性が
  残るが、本バッチは「最終探索候補」枠を使い切った。再開する場合は
  node予算25Mの**新規run**として記録すること (10M行はNODE_LIMITのまま不変)。
- 196002 は 2M で 11/100 WIN子。情報量小 (free=3) が batch3 選定時との整合。
- 144019 / 144692 は指示通り同一条件で再探索していない。
- conflict-closure pool 5件 (131631/162106/193768/196002/211133) は本バッチで
  全員が何らかの探索済み状態になった (WIN独立証拠2件・UNKNOWN@25M 1件・
  UNKNOWN@2M 1件・UNKNOWN@10M 1件)。
