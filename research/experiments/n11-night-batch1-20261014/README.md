# n11 night batch 1: solver-trusted 3件の独立検証と新規7件の初回2M probe

基準: main `cf2e7734` ＋ 未コミット4実験 (adaptive-plan-update / update2 / probe / verify)。
本実験は既存実験・knowledge正本・生成物・共有solver論理・K0423パイロット・
全既存出力を一切変更せず、`research/experiments/n11-night-batch1-20261014/` に
結果を分離保存する。再生成traceは `build/n11-night-batch1-traces/` (gitignore、使い捨て)。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
WIN/LOSS/UNKNOWNをそのまま保存し推定補完はしない。UNKNOWNは証拠ではない。

## Task A: solver-trusted 3件の独立終局検証 (trace再生成、再求解ではない)

対象: `n11-conflict-closure-20261013/output/next10m-manifest.json` の
solver-trusted止まりだった3件 (すべて verdict=2 LOSS)。
frozen next10m と同一solver source・同一memo 20・同一order(count=0)・
同一node予算10M・cold TT・capture で trace を再生成し、
凍結 trace_sha256 と**バイト一致**を確認した上で、
`n11-native-terminal-checker-20261013/scripts/check_trace.cpp` と
同一チェックサムのチェックサム実体
(`n11-adaptive-verify-20261013/output/check_trace`, SHA256 `4e51efee…`,
source SHA256 `0f890cb4…`) で terminal-only receipt を発行した。
基準は focus検証済み3件・adaptive検証済み4件と同じ:
trusted_leaves=0 強制・root/verdict/trace SHA 結合・pruned roundtrip・
Python dag_verifier 再検証との全フィールド一致。

| S5索引 | 元先手結果 | 探索nodes | wall秒 | peak RSS (KiB) | trace bytes | frozen SHAバイト一致 | DAG nodes / edges / 終局 | trusted葉 | receipt | Python照合 |
|---:|---|---:|---:|---:|---:|---|---|---:|---|---|
| 137694 | LOSS (verdict=2) | 3,550,700 | 95.9 | 599,300 | 532,915,471 | `7722b1f9…` ✓ | 636,353 / 953,685 / 85,872 | 0 | ✓ | ✓ |
| 143240 | LOSS (verdict=2) | 4,774,013 | 131.1 | 775,924 | 711,692,603 | `d460d3de…` ✓ | 724,034 / 1,088,867 / 98,414 | 0 | ✓ | ✓ |
| 220231 | LOSS (verdict=2) | 3,570,981 | 102.4 | 714,180 | 542,280,034 | `a039058d…` ✓ | 483,525 / 741,330 / 58,329 | 0 | ✓ | ✓ |

3/3 が凍結traceとバイト一致 (探索nodes・verdictもraw runと一致)。
これで solver-trusted 3件は独立終局証拠へ昇格した。
既存の next10m/focus/adaptive 成果物は上書きしていない。
具体DAGのLean内形式検査を意味しない。

## Task B: 新規7件の初回2M probe (capture・solver-trusted保存)

候補pool 16件 (いずれもscreen2mでUNKNOWN@2M) から、
`n11-conflict-ranking-20261013/output/ranking.tsv` の影響表と
`n11-adaptive-plan-update2-20261013` (上界31,728・下界6,582・WIN証人1,846・
不能応手[1,2,101]) を参照して7件を選択した。選定は legal手数順ではなく:

- **120370** (impact/child 4位・Pareto): LOSS時14分岐欠落のハブ、WIN時20分岐FREE。両極情報量最大。
- **221294** (11位・Pareto): WIN時8選択 invalidated (残候補中最大)。
- **143718** (14位): 残り唯一の stabilizer=2 (51正準子)。確定9件と同じ対称性クラス。
- **181624 / 157861 / 126017 / 197665** (16〜19位): 統一プロファイル block (WIN時18分岐FREE、
  被覆不能4) の中で正準子数最小の4件。DAG取得見込みが良い。

除外: 確定9件 (115540,121263,126899,137694,143240,144095,144193,144311,220231)・
UNKNOWN@10M (144019,144692) の同一条件再探索禁止・K0423 2件 (558600,209644)。

条件: node予算2M・memo 20・cold TT (1行1プロセス)・capture・order count(=count-asc, mode 0)・
逐次実行 (workers=1、メモリ圧迫と同一root競合を回避)。
`--exact-replay-profile` で root 直接子の WIN/LOSS/UNKNOWN census を取得
(探索順・節点数は変えない計数のみ)。2MでNODE_LIMITのものは同条件で再実行せず
UNKNOWNのまま残した。

### 2M結果 (7/7件 NODE_LIMIT = UNKNOWN、推定補完なし)

| S5索引 | status | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN |
|---:|---|---:|---:|---:|---|
| 120370 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 17.2 | 394,104 | 17 / 0 / 83 (計100) |
| 126017 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 17.5 | 392,112 | 28 / 0 / 56 (計84) |
| 143718 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 17.7 | 397,908 | 10 / 0 / 41 (計51) |
| 157861 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 16.8 | 392,184 | 19 / 0 / 61 (計80) |
| 181624 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 16.7 | 391,436 | 12 / 0 / 67 (計79) |
| 197665 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 17.6 | 392,984 | 24 / 0 / 63 (計87) |
| 221294 | NODE_LIMIT (UNKNOWN) | 2,000,000 | 17.0 | 395,476 | 8 / 0 / 82 (計90) |

### 10M拡張 (SOLVED目前の有望件のみ、最大2件)

解決済みroot子比率の上位2件を拡張した (他は再実行しない):

| S5索引 | status | 元先手結果 | 節点 | wall秒 | peak RSS (KiB) | root子 WIN/LOSS/UNKNOWN | receipt |
|---:|---|---|---:|---:|---:|---|---|
| 126017 | SOLVED | **WIN (verdict=1)** | 7,151,480 | 182.8 | 1,039,360 | 84 / 0 / 0 | 独立検証 ✓ trusted葉0 |
| 197665 | NODE_LIMIT | UNKNOWN (10M) | 10,000,000 | 90.4 | 1,379,960 | 85 / 0 / 2 (僅差) | — (UNKNOWNは検証しない) |

126017 の WIN は terminal-only receipt (`nightb10m-126017-receipt.json`,
DAG 1,318,386 nodes / 1,984,060 edges / 178,988 終局 / trusted_leaves=0 /
pruned roundtrip ✓) と Python dag_verifier 全フィールド一致で独立証拠となった。
これは確定9件に次ぐ、conflict-closure系の初の新規独立WIN証拠である
(ranking上 WIN時18分岐FREE・3選択invalidated・greedy Δ49)。
証明計画への反映 (plan-update系) は本バッチの範囲外であり未実施。

## 保存パス

| 内容 | パス |
|---|---|
| A再生成manifest (frozen SHA比較込み) | `output/night-a-manifest.json` |
| A receipts (3件) | `output/night-a-{137694,143240,220231}-receipt.json` |
| A terminal DAG / pruned (3件) | `output/night-a-{index}-terminal-dag.json.gz` / `-pruned.csv.gz` |
| A Python照合 (3件) | `output/night-a-{index}-python-comparison.json` |
| A再生成trace (gitignore・使い捨て) | `build/n11-night-batch1-traces/night-a-{index}.csv` |
| B 2M manifest (census込み) | `output/nightb2m-manifest.json` |
| B 10M拡張manifest | `output/nightb10m-manifest.json` |
| B 126017 receipt / DAG / pruned / Python照合 | `output/nightb10m-126017-{receipt.json,terminal-dag.json.gz,pruned.csv.gz,python-comparison.json}` |
| B 126017 10M trace (gitignore) | `build/n11-night-batch1-traces/nightb10m-126017-proof.csv` |
| B per-row csv/log | `output/nightb2m-{index}.csv` / `output/nightb10m-{index}.csv` |
| 入力 (凍結入力とバイト一致確認済) | `input/s5-{index}.csv` |

## 次バッチへの申送り

- **197665 (最有望)**: 10M時点で root 87子中85子WIN・残りUNKNOWN 2子のみ。
  「残り僅か」の典型。20〜30M拡張、または残2子の個別 exact 予算集中で SOLVED
  到達見込みが高い。WINなら block同様 18分岐FREE。
- **143718**: 残り唯一の stabilizer=2 (51正準子)。2Mで10/51解決と浅いが、
  対称性クラスの完結価値が高く、DAGも小さい (証拠取得見込み良好)。
- **120370**: 影響表4位のParetoハブ (LOSS時14分岐欠落・WIN時20分岐FREE)。
  2Mで17/100。予算を注ぐ価値は残候補中最大だが到達は遠い。
- **221294**: WIN時8選択invalidatedのPareto片。2Mで8/90と遅い。
- **157861 / 181624**: 2Mで19/80・12/79。中程度。block内の次点。
- **未着手 pool 残り9件**: 131631, 137043, 142283, 162106, 166171, 193768,
  196002, 206386, 211133 (影響表の大半は block同一プロファイル、
  196002/211133/193768 は free=3 で情報量小)。
- 144019 / 144692 は UNKNOWN@10M のまま据え置き (同一条件再探索禁止)。
- 126017 WIN の plan反映 (WIN証人pool・上界側) は次回の plan-update 実験で実施のこと。

## 再現 (repo root, WSL Linux Python)

```sh
python3 research/experiments/n11-night-batch1-20261014/scripts/prepare_inputs.py
python3 research/experiments/n11-night-batch1-20261014/scripts/probe_night_a.py
for i in 137694 143240 220231; do
  python3 research/experiments/n11-night-batch1-20261014/scripts/verify_night.py $i --mode frozen \
    --probe-manifest research/experiments/n11-night-batch1-20261014/output/night-a-manifest.json \
    --trace build/n11-night-batch1-traces/night-a-$i.csv \
    --checker research/experiments/n11-adaptive-verify-20261013/output/check_trace --label night-a
  python3 research/experiments/n11-night-batch1-20261014/scripts/compare_night_dag.py $i --label night-a --rerun-python
done
python3 research/experiments/n11-night-batch1-20261014/scripts/probe_night_b.py
python3 research/experiments/n11-night-batch1-20261014/scripts/probe_night_b.py --budget 10000000 --prefix nightb10m --indices 126017 197665
python3 research/experiments/n11-night-batch1-20261014/scripts/verify_night.py 126017 --mode probe \
  --probe-manifest research/experiments/n11-night-batch1-20261014/output/nightb10m-manifest.json \
  --trace build/n11-night-batch1-traces/nightb10m-126017-proof.csv \
  --checker research/experiments/n11-adaptive-verify-20261013/output/check_trace --label nightb10m
python3 research/experiments/n11-night-batch1-20261014/scripts/compare_night_dag.py 126017 --label nightb10m --rerun-python
```

check_trace は既存の同一実体 (source SHA256 `0f890cb4…`, binary SHA256 `4e51efee…`)
を読み取り専用で使用した。raw solver labelはsolver-trustedのまま;
証拠への昇格は本実験の terminal-only receipt のみが行う。UNKNOWNは昇格しない。
