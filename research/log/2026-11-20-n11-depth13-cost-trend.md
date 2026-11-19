# 2026-11-20 n11 depth-13第3差分コスト測定（最軽量2根・depths 10-13）

## 着手判断

単一オーナー宣言ノート（commit da4b167811・先行出版）に従い実施。K1081系列は
D10→D11倍率バンド1.0004〜1.0666（10根20 probe）、depth-12第2差分はD11→D12倍率
1.0000〜1.0802・非複利まで確認済み。**乗数が3手連続でどう振る舞うか**（D12→D13）が
逐次深化の費用見積で次に不足する情報だった。コスト測定のみであり、判定・行の閉鎖は行わない。

## 方法

depth-12トレンドと同じ最軽量2根（K1069 REFUTED-D10 idx0 `00000000000000003800000008001220`
bit 5・idx12 `00000000000000801202000000880100` bit 8）。runner v17固定コピー
（git blob c132cc64…）・cap 30M・timeout 280s・両AND順序・pilot_d6制御必須・逐次。
depth 10/11/12/13を自己完結的に再測定（計16 probe）。D10/D11/D12はd12trend正本
（10082aef…）とのnode一致をfail-closed gateで要求。

## 結果（16/16完走・capped 0・error 0・gate 7/7 PASS）

- **D12→D13倍率は全4 probeで1.0000（node数完全同一・728,062/905,121/333,456/445,323）**。
  idx0根が新たにフロンティア飽和に到達し、depth-12で既に飽和していたidx12根と同じく
  **depth 13の追加depthは追加nodeを生まない**ことが確定。
- D13/D10の最大は1.1105でD12/D10と同一。乗数系列（idx0 ac0: 1.0281→1.0802→1.0000、
  idx12 ac1: 1.0054→1.0000→1.0000）は複利にならず、rootごとに1.0へ収束する。
- D10/D11/D12再測定はd12trend正本の12値全てと厳密一致（拡張正本→d12trend正本→本実験で
  決定論の三重測定合意）。
- 供給判断への含意（提案のみ・実行はしない）: 逐次深化の費用見積ではrootごとの飽和深度を
  「連続するdepthでnode数が一致したらそれ以上のdepth延長は同コスト」と検出できる。
  軽量根の飽和はdepth 11-12に現れるが、大型rootの飽和深度は未知のまま（K1081の限界と同じ）。

## 成果物

- `research/experiments/n11-depth13-cost-trend-2root-20261120/`（README・scripts・output・
  runner固定コピー・生probe記録16行）
- 正本 `output/depth13-cost-trend-2root-20261120.json`（SHA-256
  573171e004b8b9d4e29590d9cc12be4ecbc144d1ae3a7b5aa0ca2893c6341c01）は別cwd・別プロセスの
  assembleでbyte-identical（2回確認）。

## 解釈規約

node数はcap内で決定的（機種非依存の費用単位）。capped/timeoutはいかなる方向の証拠にもならない
（本実験でcapped 0）。depth-13のloss=falseはREFUTED-D13分類でも行の閉鎖でもない。
REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 はすべて UNKNOWN のまま。**
