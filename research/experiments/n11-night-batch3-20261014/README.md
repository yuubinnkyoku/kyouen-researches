# n11 night batch 3: 206386 25M予算拡張でSOLVED(WIN)＋独立検証、未着手残5件から3件の初回2M probe

基準: main `cf2e7734` ＋ 未コミット先行実験 (adaptive系4件 / night-batch1 / night-batch2 /
night-plan-update3, 並行の night-plan-update4 は非接触)。
本実験は既存実験・K0423パイロット・全既存出力・night batch 1/2 成果物・履歴・
knowledge正本・生成物・共有solver論理を一切変更せず、
`research/experiments/n11-night-batch3-20261014/` に結果を分離保存する。
traceは `build/n11-night-batch3-traces/` (gitignore、使い捨て)。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
WIN/LOSS/UNKNOWNをそのまま保存し推定補完しない。UNKNOWNは証拠ではない。
全run逐次 (workers=1、上限2以下)・memo 20・cold TT (1行1プロセス、`--s5-cache`なし)・
capture (`--proof-dag`)・order count (mode 0)。check_traceは既存同一実体
(source SHA256 `0f890cb4…`、binary SHA256 `4e51efee…`) を読み取り専用で使用。
144019 / 144692 (UNKNOWN@10M) は同一条件で再探索していない。

## Task A: 206386 の予算拡張run (node予算25M、新規run)

night batch 2 の10M run (nightb10m-206386) は NODE_LIMIT で root 88子中82子WIN・残6子UNKNOWN。
これは同一条件の再実行ではなく、node予算のみ10M→25Mへ拡張した**新規run**である
(frozen 10M行は manifest 内に参照保存)。

| S5索引 | status | 先手結果 | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN | trace bytes |
|---:|---|---|---:|---:|---:|---:|---:|
| 206386 | SOLVED | **WIN (verdict=1)** | 11,024,416 | 262.2 | 1,483,052 | 88 / 0 / 0 | 1,413,445,629 |

11,024,416 nodesでSOLVED (25M予算は未消化)。残6子UNKNOWNは11.0M到達前に解けた。
terminal-only receipt (`nighta25m-206386-receipt.json`) を発行し、
Python dag_verifier 再検証と全フィールド一致を確認した:

- DAG: 1,592,383 nodes / 2,384,095 edges / 223,354 終局 / **trusted_leaves = 0**
- pruned roundtrip ✓ (replay orphan 0)、certificate json.gz 45,596,421 bytes、pruned 34,248,462 bytes
- checker wall 122.9s・peak RSS 1,708,632 KiB (OOMなし)、Python照合 wall 960.7s
  (verdict=1・nodes/edges/terminal_nodes/trusted_leaves 全一致 ✓)

これで206386はsolver-trustedから**独立終局証拠 (WIN)** へ昇格した。
126017・197665 に次ぐ、conflict-closure系の新規独立WIN証拠である
(ranking上 WIN時18分岐FREE・3選択invalidated・greedy Δ49)。
証明計画への反映 (plan-update系) は本バッチの範囲外。
具体DAGのLean内形式検査を意味しない。証拠への昇格は receipt のみが行い、
raw solver label は solver-trusted のまま保持している。

## Task B: 未着手残5件から3件を選択した初回2M probe

残poolは 131631 / 162106 / 193768 / 196002 / 211133。7観点
(①閉鎖S4数 ②第三手・応手寄与 ③両極情報量 ④S6正準子数と対称性 ⑤証拠共有 ⑥履歴 ⑦DAG見込み) を
`n11-conflict-ranking-20261013/output/ranking.tsv` と現行plan
`n11-night-plan-update3-20261014/output/effect-measurement3.json` (層別10件・unknown_candidates 20件・
unclosable [1,2,4,15,79,101]) で照合し、`output/selection-task-b.json` に記録した:

- **131631** (geometry 23位・99正準子): free=18 block。証拠共有 (197665と子2件・126017と子1件)。
  99子三兄弟 (131631/137043/162106) の最上位。batch2申送りの「206386 SOLVED後の再評価」条件が成立したため優先。
- **162106** (25位・99正準子): 同block。証拠共有最多 (197665と子2件・126017と子2件)。
- **211133** (22位・98正準子): free=3 の3件 (193768/196002/211133) は情報量小のため**代表1件のみ**採用。
  3件中 geometry順位最上位・正準子最少・choices invalidated 5 (3件中最大)。
- 除外: **193768 / 196002** (free=3 の2件目以降は情報量小)。
  確定集合・UNKNOWN@10M (144019, 144692) の同一条件再実行・K0423 (558600, 209644) は非接触。

### 2M結果 (3/3件 NODE_LIMIT = UNKNOWN、推定補完なし)

| S5索引 | status | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN |
|---:|---|---:|---:|---:|---|
| 131631 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 15.5 | 395,136 | 11 / 0 / 88 (計99) |
| 162106 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 15.6 | 393,532 | 11 / 0 / 88 (計99) |
| 211133 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 16.2 | 394,776 | 8 / 0 / 90 (計98) |

### 10M拡張 (有望件のみ・最大1件)

2Mの解決済みroot子比率が最大だった1件 (131631と162106が11/99で並び、geometry順位で131631) の
**1件のみ**を拡張した (他の2件は再実行しない)。batch2申送りの
「99子三兄弟は206386 SOLVED後に再評価」に従った判断である:

| S5索引 | status | 先手結果 | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN | receipt |
|---:|---|---|---:|---:|---:|---:|---|
| 131631 | NODE_LIMIT | UNKNOWN (10M) | 10,000,000 | 87.3 | 1,541,024 | 51 / 0 / 48 (僅差ではない) | — (UNKNOWNは検証しない) |

131631 は10Mで51/99まで進んだが残48子でNODE_LIMIT。UNKNOWNのまま保存し、
推定も同一条件 (10M) の再実行もしない。次回は25M以上の新規予算でのみ再開できる。

## Task C: 実行条件

- 極性: K0371絶対準拠 (S5=AND・後手手番・元先手固定視点)。判定はそのまま保存、推定なし。
- workers: 1 (逐次、上限2以下)。cold TT = 1行1プロセス。
- 144019 / 144692 の同一条件再探索: 未実施 (禁止遵守)。
- K0423 (558600, 209644)・night-batch1/2 出力・knowledge正本・生成物: 非接触・非上書き。
  `git status` は本ディレクトリ (未追跡) のみを追加し、追跡ファイルの変更は0件。

## 保存パス

| 内容 | パス |
|---|---|
| A 25M manifest (frozen 10M参照込み) | `output/nighta25m-manifest.json` |
| A 206386 receipt / terminal DAG / pruned / Python照合 | `output/nighta25m-206386-{receipt.json,terminal-dag.json.gz,pruned.csv.gz,python-comparison.json}` |
| A 206386 25M trace (gitignore・使い捨て) | `build/n11-night-batch3-traces/nighta25m-206386-proof.csv` |
| B 2M manifest (census込み) | `output/nightb2m-manifest.json` |
| B 10M拡張manifest | `output/nightb10m-manifest.json` |
| B 選定記録 (7観点) | `output/selection-task-b.json` |
| per-row csv/log | `output/nighta25m-206386.{csv,log}`・`output/nightb2m-{131631,162106,211133}.{csv,log}`・`output/nightb10m-131631.{csv,log}` |
| 入力 (frozen入力とバイト一致確認済) | `input/s5-{206386,131631,162106,211133}.csv` |

## 次バッチへの申送り

- **206386 (SOLVED・独立WIN証拠)**: 確定集合に追加してよい。ranking上 WIN時18分岐FREE・
  3選択invalidated・greedy Δ49。plan-update実験でWIN証人pool・上界側へ反映のこと
  (126017 → 197665 と同一経路。並行の night-plan-update4 は197665のみ層別済みで、
  206386は**未層別**)。
- **131631 (最有望)**: 10Mでroot 99子中51子WIN・残48子UNKNOWN。10Mの同一条件再探索は禁止のため、
  次回は25M以上の新規予算run。WINなら block同様 18分岐FREE。
- **162106**: 2Mで11/99。131631と同一プロファイル、証拠共有は3兄弟中最多。
  残poolで最初の10M拡張候補。20〜30M級の予算が必要。
- **211133**: 2Mで8/98。free=3代表として記録。情報量小のため深掘り優先度は低い。
- **未着手 pool 残り2件**: 193768, 196002 (free=3 で情報量小、見送り継続)。
  free=18 block の未着手は131631/162106の2件のみ (両方probe済み・UNKNOWN)。
- 144019 / 144692 は UNKNOWN@10M のまま据え置き (同一条件再探索禁止)。
- K0423 (558600, 209644) は本バッチ非接触。空盤 (11×11) は UNKNOWN のまま。
- 独立receipt総数: 13 (batch3まで) → 206386を加えて14件、うち新規WIN証拠は4件目。
- ディスク: D空き 約2.8GB。traceは batch1 2.6GB / batch2 1.3GB / batch3 1.4GB
  (receipt発行済みのため削除可、gitignore・使い捨て)。次のバッチは receipt済み trace から先に削除のこと。

## 再現 (repo root, WSL Linux Python)

```sh
python3 research/experiments/n11-night-batch3-20261014/scripts/prepare_inputs.py
python3 research/experiments/n11-night-batch3-20261014/scripts/select_task_b.py
python3 research/experiments/n11-night-batch3-20261014/scripts/probe_a25m.py
python3 research/experiments/n11-night-batch3-20261014/scripts/probe_b2m.py
python3 research/experiments/n11-night-batch3-20261014/scripts/probe_b2m.py --budget 10000000 --prefix nightb10m --indices 131631
python3 research/experiments/n11-night-batch3-20261014/scripts/verify_night3.py 206386 \
  --probe-manifest research/experiments/n11-night-batch3-20261014/output/nighta25m-manifest.json \
  --trace build/n11-night-batch3-traces/nighta25m-206386-proof.csv \
  --checker research/experiments/n11-adaptive-verify-20261013/output/check_trace --label nighta25m
python3 research/experiments/n11-night-batch3-20261014/scripts/compare_night3_dag.py 206386 --label nighta25m --rerun-python
```

check_trace は既存の同一実体 (source SHA256 `0f890cb4…`、binary SHA256 `4e51efee…`) を
読み取り専用で使用した。raw solver labelはsolver-trustedのまま;
証拠への昇格はterminal-only receipt のみが行う。UNKNOWNは昇格しない。
