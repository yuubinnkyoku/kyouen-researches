# n11 depth-12 第2差分コスト測定（2 root・depth 10/11/12、2026-11-20）

## 目的

depth-11コスト測定（パイロット commit 1a2021979b・標本拡張 d7d4ebbe1f）で得た
「D10→D11倍率バンド 1.0004〜1.0587」について、**1手延長あたりの乗数が次の手でも維持されるか**
（第2差分）をdepth 12で測る。**コスト測定のみ**で、判定変更・行の閉鎖・掃引は行わない。
単一オーナー宣言ノート
（`research/log/2026-11-20-n11-depth12-cost-trend-single-owner-note.md`・commit cd7b03fb51）の下で実施。

## 対象とプロトコル

- 対象: 標本拡張で最も軽い2根（K1069 REFUTED-D10分類、hex昇順 index {0, 12}）:
  `00000000000000003800000008001220`（bit 5）・`00000000000000801202000000880100`（bit 8）。
- runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）・
  cap 30M・timeout 280s・両AND順序・pilot_d6制御必須・逐次・**depth 10/11/12 の3深度を自己完結的に
  再測定**（計12 probe）。
- assembleは (i) K1069正本のパス、(ii) 標本拡張の出版済み正本のパスを引数に取り、
  membershi・SHA pin・D10/D11 node値の再測定一致をgate検証する。

## 結果（12/12完走・capped 0・error 0・gate 7/7 PASS）

| label | ordering | D10 nodes | D11 nodes | D12 nodes | r11/10 | r12/11 | r12/10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| idx0 | andclose1 | 671,421 | 684,989 | 728,062 | 1.0202 | 1.0629 | 1.0844 |
| idx0 | andclose0 | 815,057 | 837,946 | 905,121 | 1.0281 | 1.0802 | 1.1105 |
| idx12 | andclose1 | 331,659 | 333,456 | 333,456 | 1.0054 | **1.0000** | 1.0054 |
| idx12 | andclose0 | 443,007 | 445,323 | 445,323 | 1.0052 | **1.0000** | 1.0052 |

- **再測定したD10・D11の8 probeが標本拡張正本のnode値と全部一致**（`ext-determinism-crosscheck`
  gate PASS・別プロセス・別実行での node-exact 二重測定。決定論合意の追加証拠）。
- **D11→D12はidx0で+6.3%/+8.0%、idx12では node数が完全同一（ratio 1.0000）**。
  つまりdepth-11で探索が打ち切った境界ノードがdepth-12でも新たに展開されないrootでは、
  追加depthは追加nodeを全く生まない（idx12はD11で既にフロンティア飽和）。
- 総括: 2 root・4 ordering・3深度の観察では、**1手延長あたりの乗数は0%〜8%で、複利には
  ならない**（D12/D10 は最大1.1105）。測定標本2 rootは限られるが、逐次深化の費用見積に
  「各+1手ごと+10%未満」の経験則を与える。

## 再現性

- 正本 `output/depth12-cost-trend-2root-20261120.json`（SHA-256
  `10082aef033a34054b02c14eede10c2cd602466287750a05c2347f4852cbbd0a`）は生probe記録
  `output/probe-records-d12trend.jsonl` から assemble のみで生成され、別cwd・別プロセスで
  byte-identical（2回確認）。
- 再現: repoからK1069正本と拡張正本をraw取得し、
  `python3 scripts/depth12_cost_trend_20261120.py assemble <k1069.json> <ext.json>`。
  probe再実行は `run`（resume-safe）。

## 解釈規約

node数はcap内で決定的（機種非依存の費用単位）。capped/timeout probeはコスト下界であって
いかなる方向の証拠にもならない。depth-11/12で付随するloss=falseはREFUTED-D11/D12分類でも
行の閉鎖でもない（分類・閉鎖は掃引オーナーレーンの管轄）。REFUTED-D10はLOSS証明ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
