# 2026-11-20 n11 大型4根のdepth-13飽和確認（K1082台帳上位4根・depths 10-13）

## 着手判断

単一オーナー宣言ノート（commit fed52e3f・先行出版）に従い実施。軽量2根の第3差分
（b231035d25）はD12→D13全probe 1.0000（飽和）だったが、**飽和深度の大型rootへの外挿は未知**が
K1081系列の明示済み限界だった。大型root標本（1cdbe215da）と同じ4根をdepth-13まで延長して
飽和の普遍性とdepthコストの挙動を測った。コスト測定のみであり、判定・行の閉鎖は行わない。

## 方法

K1082台帳by_root sum_nodes上位4根（bit 20/12/2/18）。runner v17固定コピー（git blob
c132cc64…）・cap 30M・timeout 280s・両AND順序・pilot_d6制御必須・逐次・depth 10/11/12/13の
自己完結フル再測定。**実施probe数は32**（宣言ノートの「計16 probe」は4深度×2順序×4根の
数え誤り。プロトコル内容は宣言通り。訂正として本ログに記録する）。D10/D11は大型root標本
正本（c9927a23…）と、D10はK1082台帳per-probe値ともnode一致をfail-closed gateで要求。

## 結果（32/32完走・capped 0・error 0・gate 8/8 PASS）

- **D12→D13倍率は全8 probeで1.0000（node数完全同一）**。軽量2根と合わせdepth-13まで測った
  全6根12ケースがすべてD12→D13で飽和。うちrank1 ac1・rank2 ac0・idx12両順序の4ケースは
  D11→D12で先行飽和。
- **depth非単調性を初観測**: rank1 ac0はD11→D12で0.9805（node数減少）、rank2 ac0が0.9974・
  rank4 ac1が0.9955。同じprobe内でもrank3 ac0は+11.8%増と方向が分かれる。node数の決定性は
  変わらず、増減はmemo化とカット構造の影響。
- 累積D13/D10の観測範囲は1.0024〜1.1424（最大はrank3 ac0の3,909,518/3,422,095）。
- D10/D11再測定は大型root標本正本と16値全て、D10はK1082台帳と8値全て厳密一致
  （決定論の多重測定合意）。

## 成果物

- `research/experiments/n11-depth13-largeroot-saturation-20261120/`（README・scripts・output・
  runner固定コピー・生probe記録32行）
- 正本 `output/depth13-largeroot-saturation-20261120.json`（SHA-256
  dca8abb2e92ecaa3a04042a5936eacaa0fabb107bf32751b4e93c12ada42beb9）は別cwd・別プロセスの
  assembleでbyte-identical（2回確認）。

## 解釈規約

node数はcap内で決定的（機種非依存の費用単位）。capped/timeoutはいかなる方向の証拠にもならない
（本実験でcapped 0）。depth-12/13のloss=falseはREFUTED-D12/D13分類でも行の閉鎖でもない。
D11→D12のnode減少は同エンジンのmemo化挙動の観察であってゲームの値に関する証拠ではない。
REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 はすべて UNKNOWN のまま。**
