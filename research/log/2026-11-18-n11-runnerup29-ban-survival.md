# 2026-11-18 N11 runner-up parent（29行）最小coverの厳密ban生存曲線

## 成果

29行runner-up parent `00000000000000003800000009000000`（cost 15 exact）について、membership上位k本のpair rootを除外したときの**残存最小cover総数をk∈{0,1,2,3,4,5,6,7,8,10,12}の各点で完全再計算**し、厳密な生存曲線を決定した。各点で上位k rootのpair typeを重みから削除し（全type multiplicity 1なので削除と同値）、A型・B型総数を新規の共有memo anchored lazy matching DP（PmLazy）で最初から再計算する（各点約28秒・全11点311秒）。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/runnerup29_ban_survival_curve_20261118.py`
- endpoint検証script: 同dir `verify_runnerup29_k12_endpoint_20261118.py`
- output: 同dir `output/runnerup29-ban-survival-curve-20261118.json`（blob `92db40a2`）
- 15 checks all PASS。

## 主要数値

| k | kill（厳密） |
|---|---|
| 1 | 5.245% |
| 2 | 10.467% |
| 4 | 20.00% |
| 8 | 37.12% |
| 10 | 44.70% |
| 12 | **52.20%**（残 21,963,916,318,152,072） |

- **上位12本banでも全最小coverの47.8%が生存**。上位12本のmembership単純和は総数の60.54%だが、これは共同出現（joint）を二重計上する上限で、厳密なkillは52.20%（差8.34pt = joint重複の寄与）。
- 他parentとの比較（k=12 kill）: top parent（11行）95.9% > cost-12 parent（23行）62.5% > **runner-up（29行）52.2%** > cost-9 parent（18行）23.6%。行数・候補数が大きいparentほどcover計画が分散する傾向が4点で一貫。

## 検証

1. k=0の再計算総数が出版値 45,949,721,018,967,524 およびA/B内訳と完全一致。
2. **k=1は total − membership(top1)（= 2,410,014,432,522,432 を差し引いた値）と正確一致**、**k=2は 包含排除 total − (mem1 + mem2 − joint(top1,top2)) と正確一致**（出版membership・jointからの独立予測）で、ban再計算機構を二重に検証。
3. 単調減少・kill share単調増加・k=12のunion bound（生存 ≥ total − Σmembership）を機械検証。
4. **二重実行**: 出力は時間依存フィールドを含まない決定的JSON。本日の実行環境はbackground processが不安定で（既存の環境リセット2件に加え、nohup実行4回中3回が最終点直前で原因不明のSIGKILL）、完全走破は1回に留まったが、**3回の部分実行のk=0..10全11点が完全な点一致**し、さらに**k=12 endpoint専用検証scriptを2回実行してtotal/A/B/memo状態数/pm getsの全値が完全一致**した。実質的に全点が複数回独立計算で確定している。

## 解釈上の注意

生存曲線は「上位rootを除外した場合に何通りの最小cover計画が残るか」の組合せ論であり、除外rootのverdictや探索コストを主張しない。上位k本の集中度はcoordinatorの候補評価優先度の参考値にすぎない。REFUTED-D10・STERILE は LOSS 証明ではない。

## 環境の実験的事実

nohup + pollパターンで~5.5分を超えるbackground計算が本日は高頻度でkillされた（4回中3回・ログにtracebackなし・SIGKILL相当）。1コマンド（~70秒）に収まるendpoint検証scriptへの分割が確実な再検証手段。環境リセットでローカル作業dirが消失した場合も、出版済みblobのraw CDN pin検証再取得＋JSONL再生成（約40秒）で~5分以内に復旧可能なことを確認済み。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
