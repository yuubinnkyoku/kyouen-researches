# 2026-11-20 n11 depth-11 probeコスト伸び測定パイロット

## 着手判断

単一オーナー宣言ノート（commit ec5b09c1・先行出版）に従い実施。36-root depth-10 sweep本体は
掃引オーナーレーン実行中で結果未出版であり、本測定は出版済みrootのみを対象とし、どのレーンの
作業とも衝突しない。K1046レジューム以来の未着手課「depth>10コスト測定」に対応する。

## 入力と方法

- K1069 39-live掃引正本（SHA-256 22953ae1…・repo pin 53b07ebe16）の最大probe root
  `00000000010000809002000040000080`（bit 7・andclose0・nodes 14,249,420・REFUTED-D10）
- K1069/K1070 第17証明書WIN7-D10 root `00004000000000821082000000000100`（bit 8・
  両順序loss=true・nodes 1,576,372/2,544,178）

runner v17 repo原本固定コピー（git blob c132cc64…・起動時再検証）、cap 30M・timeout 280s・
両AND順序・pilot_d6制御必須・K1075掃引driverと同一引数形式で、同一rootをdepth 10とdepth 11の
両方で実行（逐次・計8 probe・並列1）。生child hex規約（child=root−最小セットビット）。

## 結果（8/8完走・capped 0・error 0・gate 5/5 PASS）

| root | ordering | D10 nodes | D11 nodes | 倍率 | loss |
| --- | --- | --- | --- | --- | --- |
| max-probe | ac1 | 2,731,659 | 2,767,659 | 1.0132 | F→F |
| max-probe | ac0 | 14,249,420 | 14,562,762 | 1.0220 | F→F |
| WIN7-D10 | ac1 | 1,576,372 | 1,576,950 | 1.0004 | T→T |
| WIN7-D10 | ac0 | 2,544,178 | 2,546,836 | 1.0010 | T→T |

- K1069出版値3件（max-probe ac0 14,249,420・WIN両順序）はnodes・loss・capped全体で厳密一致
  （depth10-exact-reproduction PASS・不一致時fail-closed）。
- **depth 10→11の1手延長コストは+0.04%〜+2.2%**（node単位・機種非依存・4/4）。全probe
  cap/timeoutまで余裕（sandbox最大43.6s）。
- 帰結: 測定したコスト帯ではdepth-11掃引はdepth-10掃引とほぼ同額。ただし**標本2 root・n=4 probe**
  であり、他コスト帯・36 fresh witnessへの外挿は保証しない。倍率バンドは事前見積の参考値。

## 供給判断への含意（提案・実行はしない）

36-root sweepが全REFUTEDで帰った場合、depth-11への再掃引はdepth-10とほぼ同じ計算量で実行可能
な可能性が高い（K1069 39-live類推: 総nodes 169.6M→概ね+2%程度）。ボトルネックは計算量ではなく
depth-saturation（永久判定）の意味論と、どのroot族をいつ延長するかのcoordinator判断になる。
max-probe rootのac1（D10 2,731,659）はK1069で非出版のprobe値であり、ac0（14,249,420）より
5.2倍小さい: 直近の掃引で最大probeは順序依存であることの追証。

## 成果物

- `research/experiments/n11-depth11-cost-scaling-pilot-20261120/`（README・scripts・output）
- 正本 `output/depth11-cost-scaling-pilot-20261120.json`（SHA-256
  44f1b875f71a8e35c4eca89a3277f1a10cbd3df51a8a26a43e5c95c2f65714ac7）は生probe記録からのみ
  assembleで生成され、別cwd・別プロセスでbyte-identical（2回確認）。

## 解釈規約

コスト測定のみ。本測定は行を閉じず、判定を変えず、depth-11掃引の着手宣言でもない。
本測定に付随するdepth-11のloss値はprobe事実の記録であって、REFUTED-D11分類ではない。
REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 はすべて UNKNOWN のまま。**
