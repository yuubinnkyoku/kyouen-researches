# n11 長期レーン: depth-13第3差分コスト測定: 単一オーナー宣言ノート（2026-11-20）

depth-11倍率系列（K1081・パイロット1a2021979b・拡張d7d4ebbe1f・大型root標本1cdbe215da）で
D10→D11バンドは1.0004〜1.0666、depth-12第2差分（2db12bdcc0）でD11→D12は1.0000〜1.0802
（D12/D10最大1.1105・非複利）を得た。**1手延長あたりの乗数が3手連続で維持されるか**
（第3差分・depth-13）は、逐次深化の費用見積で次に不足している情報である。本レーンが以下を
単一オーナーとして実行することを宣言する。

- 対象: depth-12トレンドと同じ最軽量2根（K1069 REFUTED-D10 idx0
  `00000000000000003800000008001220`（bit 5）・idx12 `00000000000000801202000000880100`（bit 8））。
- プロトコル: runner v17固定コピー（git blob c132cc64…）・cap 30M・timeout 280s・両AND順序・
  pilot_d6制御必須・逐次。**depth 10・11・12・13の4深度を自己完結的に再測定**（計16 probe）。
  D10/D11/D12はdepth-12トレンド正本（10082aef…）の対応probeとnode一致することが決定論合意の
  三重測定追証になる。
- gate: K1069正本SHA pinとmembershi（assemble引数）・raw-child再導出・D10ラベル整合（両順序
  loss=false・uncapped）・D10/D11/D12のd12trend正本node一致crosscheck・pilot_d6全probe合格。
- 出力: `research/experiments/n11-depth13-cost-trend-2root-20261120/`。
- **depth-13での判定・分類・行の閉鎖は一切行わない。** depth-13でloss=falseが得られても
  REFUTED-D13分類でも行閉鎖でもない。36-root sweep本体は掃引オーナーレーン管轄のまま。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
REFUTED-D10 は LOSS 証明ではない。**（確認時HEAD: 541d0f6da4）
