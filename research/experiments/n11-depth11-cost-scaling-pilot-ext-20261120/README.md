# n11 depth-11 probe コスト伸び測定: 標本拡張（2026-11-20）

## 目的

depth-11コスト測定パイロット（`../n11-depth11-cost-scaling-pilot-20261120/`・commit 1a2021979b）の
標本（2 root・倍率バンド+0.04%〜+2.2%）を、K1069 REFUTED-D10分類38根から決定論的規則で選んだ
4根に拡張する。**コスト測定のみ**であり、判定変更・行の閉鎖・depth-11掃引の着手は行わない。
単一オーナー宣言ノート
（`research/log/2026-11-20-n11-depth11-cost-scaling-pilot-ext-single-owner-note.md`・commit 742bacf75a）
の下で実施。

## 対象選択規則

K1069正本（SHA-256 `22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc`・
`research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json`）
のclassificationで `REFUTED-D10` の38根をhex昇順に整列し、index {0, 12, 24, 36} の4根:

| index | root | bit | label |
| --- | --- | --- | --- |
| 0 | `00000000000000003800000008001220` | 5 | K1069-REFUTED-D10-idx0 |
| 12 | `00000000000000801202000000880100` | 8 | K1069-REFUTED-D10-idx12 |
| 24 | `00000000000000889042000080000000` | 31 | K1069-REFUTED-D10-idx24 |
| 36 | `00000010000000801202000000400400` | 10 | K1069-REFUTED-D10-idx36 |

membershi選択・SHA pinはassemble gate（`k1069-classification-pin`）で機械検証される
（assembleはK1069正本のパスを引数に取る）。

## プロトコル（パイロットと同一）

runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）・
cap 30M・timeout 280s・両AND順序・pilot_d6制御必須（nodes 3,402・loss=false）・逐次・
生child hex規約（child = root − 最小セットビット）。計16 probe。

## 結果（16/16完走・capped 0・error 0・gate 6/6 PASS）

| label | ordering | D10 nodes | D11 nodes | 倍率 | loss (D10→D11) |
| --- | --- | --- | --- | --- | --- |
| idx0 | andclose1 | 671,421 | 684,989 | 1.0202 | false→false |
| idx0 | andclose0 | 815,057 | 837,946 | 1.0281 | false→false |
| idx12 | andclose1 | 331,659 | 333,456 | 1.0054 | false→false |
| idx12 | andclose0 | 443,007 | 445,323 | 1.0052 | false→false |
| idx24 | andclose1 | 2,950,904 | 3,087,215 | 1.0462 | false→false |
| idx24 | andclose0 | 638,671 | 643,518 | 1.0076 | false→false |
| idx36 | andclose1 | 5,720,576 | 6,056,617 | 1.0587 | false→false |
| idx36 | andclose0 | 687,760 | 702,056 | 1.0208 | false→false |

- **depth-10側は8/8 probeがREFUTED-D10分類と整合**（両順序loss=false・uncapped・
  `d10-label-consistency` gate PASS）。ここで初めて測定されたD10 node数はK1069では非出版。
- **depth 10→11の1手延長コスト倍率: 拡張4根では+0.52%〜+5.87%**。パイロット（1 root最大
  14.2M既出版 + 1 root WIN既出版）と併せると、6 root・12 probe・D10 node数331k〜14.2Mの
  コスト帯で**倍率バンドは1.0004〜1.0587**（node単位・機種非依存）。
- 帰結: 帯域内ではdepth-11掃引の計算量はdepth-10掃引の+6%以内に収まる見込みが強まった。
  ただし標本はK1069 REFUTED-D10族から決定論的選択した4根+2根であり、36 fresh witness
  （非掃引root）への外挿は保証しない。倍率はややD10 node数と正相傾向（大きいprobeほど
  倍率が高め: 14.2M root 1.0220、5.7M root 1.0587、0.33M root 1.0054）があり、
  大型rootでのdepth-11はやや不利になる可能性を残余リスクとして残す。

## 再現性

- 正本 `output/depth11-cost-scaling-pilot-ext-20261120.json`（SHA-256
  `8a584be6a145665c6230169bdc7edb51d453e9429dafe0ab9fd8fc0e579c7aa1`）は生probe記録
  `output/probe-records-d11pilot-ext.jsonl` から assemble のみで生成され、別cwd・別プロセスで
  byte-identical（2回確認）。
- 再現手順: repoのK1069正本を直接raw取得して
  `python3 scripts/depth11_cost_scaling_ext_20261120.py assemble <k1069_sweep.json>`
  （membershi SHA pin gate含む・gate fail時exit 1）。probe再実行は `run`（resume-safe）。

## 解釈規約

node数はcap内で決定的（機種非依存の費用単位）。capped/timeout probeはコスト下界であって
いかなる方向の証拠にもならない。depth-11で付随するloss=falseはREFUTED-D11分類でも行の
閉鎖でもない（分類・閉鎖は掃引オーナーレーンの管轄）。REFUTED-D10はLOSS証明ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
