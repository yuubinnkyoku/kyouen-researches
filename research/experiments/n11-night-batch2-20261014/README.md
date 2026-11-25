# n11 night batch 2: 197665 25M予算拡張でSOLVED(WIN)、未着手pool 4件の初回2M probe

基準: main `cf2e7734` ＋ night batch 1 (`n11-night-batch1-20261014`, 未コミット)。
本実験は既存実験・K0423パイロット・全既存出力・night batch 1 成果物・knowledge正本・
生成物・共有solver論理を一切変更せず、`research/experiments/n11-night-batch2-20261014/`
に結果を分離保存する。traceは `build/n11-night-batch2-traces/` (gitignore、使い捨て)。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
WIN/LOSS/UNKNOWNをそのまま保存し推定補完しない。UNKNOWNは証拠ではない。
全run逐次 (workers=1)・memo 20・cold TT (1行1プロセス、`--s5-cache`なし)・capture (`--proof-dag`)・
order count (mode 0)。check_traceは既存同一実体 (source SHA256 `0f890cb4…`,
binary SHA256 `4e51efee…`) を読み取り専用で使用。

## Task A: 197665 の予算拡張run (node予算25M、新規run)

10M run (night batch 1) は NODE_LIMIT で root 87子中85子WIN・残2子UNKNOWNだった。
これは同一条件の再実行ではなく、node予算のみを10M→25Mへ拡張した**新規run**である。

| S5索引 | status | 先手結果 | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN | trace bytes |
|---:|---|---|---:|---:|---:|---|---:|
| 197665 | SOLVED | **WIN (verdict=1)** | 10,294,083 | 248.4 | 1,414,204 | 87 / 0 / 0 | 1,341,560,017 |

10,294,083 nodesでSOLVED (25M予算は未消化)。残2子UNKNOWNは10.3M到達前に解けた。
terminal-only receipt (`nighta25m-197665-receipt.json`) を発行し、
Python dag_verifier 再検証と全フィールド一致を確認した:

- DAG: 1,624,418 nodes / 2,433,495 edges / 227,142 終局 / **trusted_leaves = 0**
- pruned roundtrip ✓ (orphan 0)、certificate json.gz 46,527,697 bytes、pruned 34,948,259 bytes
- Python照合: verdict=1・nodes/edges/terminal_nodes/trusted_leaves 全一致 ✓ (wall 990.2s)

これで197665はsolver-trustedから**独立終局証拠 (WIN)** へ昇格した。
確定9件＋batch1 3件に次ぐ、conflict-closure系の新規独立WIN証拠である
(ranking上 WIN時18分岐FREE・3選択invalidated・greedy Δ49)。
証明計画への反映 (plan-update系) は本バッチの範囲外。
具体DAGのLean内形式検査を意味しない。OOMは発生していない
(run peak RSS 1,414,204 KiB、checker peak RSS 1,640,904 KiB)。

## Task B: 未着手9件から4件を選択した初回2M probe

選定は legal手数順ではなく、7観点 (閉鎖S4数・第三手/応手寄与・両極情報量・
S6正準子数と対称性・証拠共有・履歴・DAG見込み) を
`n11-conflict-ranking-20261013/output/ranking.tsv` と
`n11-adaptive-plan-update2-20261013/output/` (上界31,728・下界6,582・WIN証人1,846・
不能応手[1,2,101]、unknown_candidates 24件) で照合した:

- **206386** (幾何18位・88正準子): 未着手poolで正準子数最小・DAG見込み最大。
  free=18 block (WIN時18分岐FREE) の一員で、solved集合と子2件共有 (証拠共有)。
- **166171** (20位・91正準子): block内で次小。応手59の第三手クラス同一、子2件共有。
- **142283** (21位・92正準子): block内で3番目に小さい。応手59クラス同一、子1件共有。
- **137043** (24位・99正準子): 99正準子三兄弟 (131631/137043/162106) のうち
  rank最上位に近い上、solved集合と子2件共有 (証拠共有で131631に優位)。

除外: 確定12件・UNKNOWN@10M (144019, 144692) の同一条件再実行・K0423 (558600, 209644)。
free=3で情報量小の 196002 / 211133 / 193768 は今回見送り (batch1申送り準拠)。

### 2M結果 (4/4件 NODE_LIMIT = UNKNOWN、推定補完なし)

| S5索引 | status | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN |
|---:|---|---:|---:|---:|---|
| 206386 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 15.8 | 392,180 | 30 / 0 / 58 (計88) |
| 166171 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 17.2 | 393,008 | 22 / 0 / 69 (計91) |
| 142283 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 16.0 | 393,648 | 24 / 0 / 68 (計92) |
| 137043 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 16.3 | 394,860 | 15 / 0 / 84 (計99) |

### 10M拡張 (SOLVED目前の有望件のみ、最大1件)

2Mの解決済みroot子比率が最大だった1件のみ拡張した (他は再実行しない):

| S5索引 | status | 先手結果 | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN | receipt |
|---:|---|---|---:|---:|---:|---|---|
| 206386 | NODE_LIMIT | UNKNOWN (10M) | 10,000,000 | 86.0 | 1,387,596 | 82 / 0 / 6 (僅差) | — (UNKNOWNは検証しない) |

206386 は10Mで82/88まで進んだが残6子でNODE_LIMIT。UNKNOWNのまま保存し、
推定も同一条件の再実行もしない。

## 保存パス

| 内容 | パス |
|---|---|
| A 25M manifest (census・frozen 10M参照込み) | `output/nighta25m-manifest.json` |
| A 197665 receipt / terminal DAG / pruned / Python照合 | `output/nighta25m-197665-{receipt.json,terminal-dag.json.gz,pruned.csv.gz,python-comparison.json}` |
| A 197665 25M trace (gitignore・使い捨て) | `build/n11-night-batch2-traces/nighta25m-197665-proof.csv` |
| B 2M manifest (census込み) | `output/nightb2m-manifest.json` |
| B 10M拡張manifest | `output/nightb10m-manifest.json` |
| per-row csv/log | `output/nighta25m-197665.{csv,log}`・`output/nightb2m-{206386,166171,142283,137043}.{csv,log}`・`output/nightb10m-206386.{csv,log}` |
| 入力 (frozen入力とバイト一致確認済) | `input/s5-{197665,206386,166171,142283,137043}.csv` |

## 次バッチへの申送り

- **197665 (SOLVED・独立WIN証拠)**: 確定集合に追加してよい。ranking上 WIN時18分岐FREE・
  3選択invalidated・greedy Δ49。plan-update実験でWIN証人pool・上界側へ反映のこと
  (batch1の126017 WINと同一経路)。
- **206386 (最有望)**: 10Mでroot 88子中82子WIN・残6子UNKNOWN。197665と同じ「残り僅か」型。
  25M拡張または残6子の個別予算集中で SOLVED 到達見込みが高い。WINなら block同様 18分岐FREE。
- **166171 / 142283**: 2Mで22/91・24/92。応手59クラス同一、20〜30M級の予算が必要。
- **137043**: 2Mで15/99と遅い。131631/162106と同一プロファイルのため、
  3兄弟から1件だけ深掘りする場合は206386のSOLVED後の再評価が良い。
- **未着手 pool 残り5件**: 131631, 162106, 193768, 196002, 211133
  (193768/196002/211133 は free=3 で情報量小)。
- 144019 / 144692 は UNKNOWN@10M のまま据え置き (同一条件再探索禁止)。
- K0423 (558600, 209644) は本バッチ非接触。
- ディスク: trace 1.34GB を `build/n11-night-batch2-traces/` に保持中 (gitignore・使い捨て)。
  receipt発行済みのため削除可。D盤の空きが逼迫したら先にこちらを消す。

## 再現 (repo root, WSL Linux Python)

```sh
python3 research/experiments/n11-night-batch2-20261014/scripts/prepare_inputs.py
python3 research/experiments/n11-night-batch2-20261014/scripts/probe_b2m.py
python3 research/experiments/n11-night-batch2-20261014/scripts/probe_a25m.py
python3 research/experiments/n11-night-batch2-20261014/scripts/verify_night2.py 197665 \
  --probe-manifest research/experiments/n11-night-batch2-20261014/output/nighta25m-manifest.json \
  --trace build/n11-night-batch2-traces/nighta25m-197665-proof.csv \
  --checker research/experiments/n11-adaptive-verify-20261013/output/check_trace --label nighta25m
python3 research/experiments/n11-night-batch2-20261014/scripts/compare_night2_dag.py 197665 --label nighta25m --rerun-python
python3 research/experiments/n11-night-batch2-20261014/scripts/probe_b2m.py --budget 10000000 --prefix nightb10m --indices 206386
```

raw solver labelはsolver-trustedのまま; 証拠への昇格はterminal-only receipt のみが行う。
UNKNOWNは昇格しない。
