# 2026-11-20 n11 depth-11倍率の大型root標本測定（K1082台帳上位4根）

## 着手判断

単一オーナー宣言ノート（commit 0e9da3cb・先行出版）に従い実施。depth-11倍率系列
（K1081・pilot 1a2021979b・拡張 d7d4ebbe1f・d12 trend 2db12bdcc0）は「倍率はD10 node数が
大きいrootで高め」という残余リスクを明示したままだった。K1082台帳（76e2c4d2a6）により
root別D10 node数が出版されたので、大型root帯（両順序D10合計 8.7M〜13.0M nodes）での
倍率を追加標本で直接検証した。コスト測定のみであり、判定・行の閉鎖は行わない。

## 方法

K1082台帳 `by_root` sum_nodes降順で、pilot測定済みの最大probe根
`00000000010000809002000040000080`を除く上位4根（rank1 bit20・rank2 bit12・rank3 bit2・
rank4 bit18）。runner v17固定コピー（git blob c132cc64…）・cap 30M・timeout 280s・両AND順序・
pilot_d6制御必須・逐次。D10再測定はK1082台帳のnode値と厳密一致を要求（fail-closed gate）し、
D11を加えて計16 probe。assemble gate `ledger-selection-pin` で対象4根の再導出も検証。

## 結果（16/16完走・capped 0・error 0・gate 7/7 PASS）

- **大型root帯のD11/D10倍率は 1.0024〜1.0666**。最大は rank4 `00000000000000003800000009840000`
  ac0（D10 6,009,248 → D11 6,409,440 nodes）の 1.0666。最小は rank1 ac1 の 1.0024。
- **D10再測定8/8がK1082台帳のper-probe node値と厳密一致**（三度目の独立再測定による
  決定論合意。pilot拡張・台帳全数再実行に続き、本実験の短抜き型再測定でも同一）。
- **倍率系列は10根・20 probe（D10 node 0.12M〜14.2M）でバンド 1.0004〜1.0666 に拡張**。
  「+1手ごとおおむね+7%以内」の逐次深化の経験則は、大型root帯でも維持される。
- 大型rootで倍率が高めに振れる傾向は弱く確認される（上位2件のratio 1.0386/1.0666 は
  小型rootの分布上限付近）が、D10 node数との単調関係は成り立たない（rank1 ac1 は
  12.8M根でも 1.0024。フロンティア飽和の実例としてd12 trendのidx12根と整合）。
- 供給判断への含意: 全39根 depth-11再掃引を見積もる場合は 169.6M×1.0666 ≈ 181M nodes
  上限バンドで計画できる（提案のみ・実行はしない）。

## 成果物

- `research/experiments/n11-depth11-large-root-scaling-20261120/`（README・scripts・output・
  runner固定コピー・生probe記録16行）
- 正本 `output/depth11-large-root-scaling-20261120.json`（SHA-256
  c9927a2345edff7e6fe2e90ad1f3f255622aca7b35bb61d7876757d1fdbcecd0）は別cwd・別プロセスの
  assembleでbyte-identical（2回確認）。

## 解釈規約

node数はcap内で決定的（機種非依存の費用単位）。capped/timeoutはいかなる方向の証拠にも
ならない（本実験でcapped 0）。depth-11のloss=falseはREFUTED-D11分類でも行の閉鎖でもない。
REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 はすべて UNKNOWN のまま。**
