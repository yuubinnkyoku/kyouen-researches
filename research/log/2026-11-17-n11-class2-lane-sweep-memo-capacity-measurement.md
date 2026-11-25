# 2026-11-17：v17 sweepエンジンのメモ容量測定（cost73i/73j全146 bit、verdict不変）

## 開始時点

最新main（`712c108e`時点）・`AGENTS.md`・`research/knowledge/README.md`・cost73i/73j関連のknowledge・experiments・logを確認した。73i（child `00000000000000403800400008000000`、12 WIN7-D10 + 61 REFUTED-D10、candidate nodes 131,402,821）と73j（child `00000000000000403800000408000000`、16 WIN7-D10 + 57 REFUTED-D10、168,445,380）は、fbt欠陥修復済みのv17エンジン `class4_child1_runner_v17.ts`（blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`、depth 10、cap 1e9、andclose 1、pilot_d6 = 3402）でsweep済み。並走レーンが全146 bitのnode-exact独立再実行（`verify_cost73ij_sweep_independent_rerun_20261117.py`）を出版済みである。

抽出側測定（同日band-memoエントリ）で、抽出器のMS=1<<18メモが抽出コストの支配因子であることが分かった。v17 runnerのline 54にも同一の `const MS = 1 << 18, MM = MS - 1;`（per-candidate freshEngine、64-probe線形探査、memoEntryは鎖切れ時に格納を黙ってスキップ、memoFindは不在扱い。健全だが再計算を生む）がある。そこでsweep側にも同じ容量問題があるかを、**146 bitすべてについてverdict不変性を検証しながら**測定した。

## 測定手順

生バッチ18本をcommit pin `712c108e` から取得し、並走rerunスクリプト記載のGit blob SHA-1で18/18検証した。MS変種はline 54の1行置換のみで生成（difflib検証済み）。測定実行はすべて `--nocontrol`（後述のpilotアボート対策）。並列は2 workerまで（cgroup 1.04 GB制約）。

## フィデリティとpilot容量プローブ

- verbatimエンジンで73i batch 1（9 bit）を再実行し、公開raw batch 1に**node-exact一致**（loss/nodes/capped/terminalStoneRange全bit、pilot_d6 = 3402）。
- MS=1<<24変種をデフォルト（pilot制御ON）で起動すると、runner自身のpilot制御がアボートした: **期待3402に対しnodes=3287**。このアボート自体が、MS=1<<18テーブルが負荷率~1%の3.4kノード探索でも既にメモエントリを落としていることの直接証拠である（飽和時だけの問題ではない）。

## 結果

| 対象 | 公開（MS=1<<18） | MS=1<<23 | 比 | MS=1<<24 | 比 | verdict不一致 |
|---|---:|---:|---:|---:|---:|---:|
| cost73i（73 bit） | 131,402,821 | 58,352,152 | **0.4441** | 58,334,444 | 0.4439 | 0（両方） |
| cost73j（73 bit） | 168,445,380 | 57,496,088 | **0.3413** | 未実施 | - | 0 |

- **146 bitすべてでloss/capped/terminalStoneRangeが完全一致**。WIN7-D10 bitリストも両childで公開と同一（73i: 1,9,11,18,29,38,54,82,97,100,110,111 / 73j: 0,1,6,29,44,49,52,69,74,82,87,91,98,100,110,118）。capped 0。
- **感度（fresh単一bit）**: 73i bit 78（最重、公開6,791,073）→ ms20: 1,917,186 → ms21: 1,733,674 → ms22: 1,703,113 → ms23: 1,701,662 → ms24: 1,701,638（約4.0倍削減、飽和は1<<22-1<<23）。軽いbit 101（公開184,771）も166,807→166,054で約10%削減。bit101は1<<22で飽和。
- **メモリ**: MS=1<<23は176 MB/engine、MS=1<<24は320 MB/engine。per-candidateのfreshEngine確保と旧engine回収の遅れでピークは約2倍になるため、MS=1<<24は4並列・2並列ともOOM-killされ、逐次のみ完走。MS=1<<23×2 workerは完走。cgroup上限1,090,519,040 bytes。

## 決定論上の注意（重要）

MS変種はノード数とpilot値（3402→3287）を変える。公開rawバッチ・audit・独立再実行はすべてverbatimエンジン（blob `c132cc64`、pilot 3402）にpinされているので、**公開記録は何も置き換えない**。MS>=1<<23は将来のsweep専用で、採用時は(i) pilot定数の再校正（例: MS=1<<24では3287）、(ii) 新engine blobのpin、(iii) 公開determinism体系からの明示的な切り離し記録が必要である。

## 処方

残りsweep作業（~50万候補）にMS=1<<23エンジンを使えば、今回の実測比（73i 0.4441、73j 0.3413）から**55-66%のノード削減**が見込め、verdictは不変である。ただし上記の決定論手続きを踏むこと。抽出側と異なりsweepはper-candidate freshEngineなので、並列数×engineフットプリントのメモリ管理が実運用の律速になる。

## 出版物

- `scripts/measure_sweep_memo_capacity_73ij_20261117.py`：再実行可能なorchestrator（engine/生バッチpin検証、1行MS変種生成検証、146 bit比較、pilot probe、感度、期待値定数の再検証）。resume対応。全チェック0 failureで検証済み。
- `output/class2-lane-sweep-memo-capacity-73ij-20261117.json`：per-bit全146エントリ、感度曲線、メモリ/OOM観測、決定論注意、解釈ガード入り。

## 解釈と次の作業

今回確かめたのは**既に出版済みsweepの計算コスト構成とverdict不変性**だけである。新しい探索verdictは1つも作っていない。cost73i/73jの各7石rootのWIN7-D10/REFUTED-D10は従来どおりで、S6 manifest行・S5 parentは1行も閉じていない。fold headの変更もない。

次の候補は、(i) 73i証明書の出版監視（出版されたらBigInt bytes再検証）、(ii) census v8 runner-up `00000000000000c09002000000400000`（cost 73、open 67）への着手（並走衝突リスクをmain再取得で確認してから）、(iii) 将来sweepレーンへのMS=1<<23処分の引継ぎ。

WIN7-D10は個別7石rootの深さ10以内の先手勝ちであり、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続きUNKNOWN。
