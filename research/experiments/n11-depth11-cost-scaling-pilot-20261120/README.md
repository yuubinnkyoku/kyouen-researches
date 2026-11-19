# n11 depth-11 probe コスト伸び測定パイロット（2026-11-20）

## 目的

出版済みdepth-10判定rootをdepth-11へ1手だけ延長したときのnodeコスト倍率を測定する。
**コスト測定のみ**であり、判定変更・行の閉鎖・depth-11掃引の着手宣言は一切行わない。
単一オーナー宣言ノート（`research/log/2026-11-20-n11-depth11-cost-scaling-pilot-single-owner-note.md`,
commit ec5b09c1）の下で実施した。

## プロトコル

- runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）。
- cap 30,000,000・timeout 280s・両AND順序（andclose 1/0）・pilot_d6制御必須（nodes 3,402・loss=false）。
- K1075掃引driverと同一の引数形式で、同一rootをdepth 10とdepth 11の両方で実行（逐次・逐次1 probe）。
- 生child hex規約（child = root − 最小セットビット）。bitはそのビット番号。
- 環境の遅さによるtimeoutは「当該環境で未検証」、値の不一致はfail-closed。

## 入力（出版済みレコードのみ）

| root | bit | label | 出版depth-10値 |
| --- | --- | --- | --- |
| `00000000010000809002000040000080` | 7 | K1069 39-live掃引の最大probe（REFUTED-D10） | andclose0 nodes 14,249,420・loss=false（K1069正本 `22953ae1…` の summary.max_probe） |
| `00004000000000821082000000000100` | 8 | K1069/K1070 第17証明書WIN7-D10 | andclose1 1,576,372 / andclose0 2,544,178・両順序loss=true・uncapped |

## 結果（8/8 probe完走・capped 0・error 0・gate 5/5 PASS）

| root | ordering | depth-10 nodes | depth-11 nodes | 倍率 (D11/D10) | loss (D10→D11) |
| --- | --- | --- | --- | --- | --- |
| max-probe root | andclose1 | 2,731,659 | 2,767,659 | 1.0132 | false→false |
| max-probe root | andclose0 | 14,249,420 | 14,562,762 | 1.0220 | false→false |
| WIN7-D10 root | andclose1 | 1,576,372 | 1,576,950 | 1.0004 | true→true |
| WIN7-D10 root | andclose0 | 2,544,178 | 2,546,836 | 1.0010 | true→true |

- depth-10側は3件の出版値とnode数・loss・capped全体で**厳密一致**（depth10-exact-reproduction gate PASS）。
  この測定で新たに得た値: max-probe rootのandclose1（D10 2,731,659・D11 2,767,659）はK1069で非出版のprobeであった。
- **depth-11への1手延長のコスト倍率は4/4 probeで+0.04%〜+2.2%**（node単位・機種非依存）。
  cap 30M・timeout 280sには全probeが余裕を持って完了（sandboxで最大43.6s）。
- 帰結: この2 rootの属するコスト帯では、depth-11掃引の計算量はdepth-10掃引とほぼ同額になる。
  ただし**標本は2 root（各クラス1根・4 probe）**であり、36 fresh witnessなど他コスト帯への外挿は
  保証しない。倍率のバンド（〜+2.2%）はdepth-11掃引事前コスト見積の参考値にすぎない。

## 再現性

- runner本体をgit blob SHA-1で固定（`c132cc64…`・検証器が起動時に再計算）。
- 正本 `output/depth11-cost-scaling-pilot-20261120.json`（SHA-256
  `44f1b875f71a8e35c4eca89a3277f1a10cbd3df51a8a26a43e5c95c2f65714ac7`）は
  生probe記録 `output/probe-records-d11pilot.jsonl` から assemble によってのみ生成され、
  別cwd・別プロセスからの再実行でbyte-identical（2回確認済み）。
- probeの再実行コマンド: `python3 scripts/depth11_cost_scaling_pilot_20261120.py run`
  （resume-safe: 完走済みの(root, depth, ordering)はskip）。
  assemble: `python3 scripts/depth11_cost_scaling_pilot_20261120.py assemble`（gate fail時exit 1）。

## 解釈規約

node数はcap内で決定的（機種非依存の費用単位）。capped/timeout probeはコストの下界であって
いかなる方向の証拠にもならない。depth-11でこの測定に付随するloss=falseは「当該rootの
当該sideのdepth-11内必勝不存在」のprobe事実の記録であって、REFUTED-D11の分類でも行の閉鎖でもない
（分類と閉鎖は掃引オーナーレーンの管轄）。REFUTED-D10はLOSS証明ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
