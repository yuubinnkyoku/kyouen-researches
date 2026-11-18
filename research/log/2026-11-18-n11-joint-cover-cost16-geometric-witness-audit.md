# 2026-11-18 N11 5-parent joint cover: 幾何列挙による56-root witnessの独立監査

## 基準と背景

入力はmain上の固定blobを使用した。入力を取得した基準mainは `0ce32ace2dae155da1f2e49b95fe07ec0f08067d`。対象はcommit `3a04ca5b` の5-parent joint cover出力（112 target rows・minimum candidate-root cover 56）である。

同じ作業中にmainへ次の独立成果も着地したため、現行mainでは併せて参照する。

- `a76c4969`: Tutte行列rank（2素体）による全31 subsetのmax-matching第三実装照合、r≤18の2^r exact cover DP、全31 witness検査。19 checks PASS。
- `9b2747f0`: cost-16 parentのB型総数・全最小cover総数の確定。A16/B16/totalを出版し、31 sliceを二重実行で再現。

本監査はそれらのmatching計算を再利用せず、幾何候補を直接列挙して56-root witnessの下界・達成を検査する。

## 独立再導出

固定入力:

- head-1410 S6 worklist: blob `2fee1d0718547a62e346d35f5858d7913e37c097`
- K0865 sterile census: blob `9c251da3138c5cb0516e097be5e5d0427dfaf5f0`
- head-1410→1476 fold ledger: blob `e8785d509e8a11a37c0d03cc450455a14708c34d`
- 5-parent joint cover output: blob `40581746dc3304bdaff4b1934fd6f1d3d2981ea5`

worklist 6,438行から、ledgerで閉じた66行とK0865のSTERILE 35行を除き、open non-STERILE 6,337行を再構成した。5 parentへのD4包含関係を、6石行から1石を削除して正準化する方法で再計算した。

| parentの個別最小cover費用 | 対象S6行 |
|---:|---:|
| 6 | 11 |
| 9 | 18 |
| 12 | 23 |
| 15 | 29 |
| 16 | 31 |
| **合計** | **112** |

5集合は互いに素。候補root JSONLやblossom実装は読み込まず、各対象6石行について全空セルを走査し、既存6石の全20個の3点組に対するdet4がすべて非零となるセルだけを生残手として採用した。整数det4・D4正準化はこの監査内に独立実装した。

結果:

- 候補出現数: **8,199**
- 異なるD4正準7石root: **6,542**
- 被覆行数1のroot: **4,885**
- 被覆行数2のroot: **1,657**
- 最大span: **2**
- 6,542個の候補rootはすべて7石安全局面として再検査PASS

これらは5親の112 target rowsに限った候補宇宙である。

## 56-root witnessの直接検査

joint outputに収録された56 rootを、上記の独立再列挙結果へ照合した。

- 56 rootはすべて異なるD4正準形で、7石安全局面。
- 56 rootはすべて独立列挙した候補宇宙に存在。
- 各rootは対象112行のうちちょうど2行を覆う。
- 112行すべてがちょうど1回覆われる。
- witness中の親をまたぐrootは10本。候補宇宙全体の親またぎroot 49本とも一致。

したがって、任意の候補rootが覆える対象行は最大2行なので、112行のcoverには少なくとも56 rootが必要。一方、検査済みwitnessが56 rootで全行を分割する。よって**この112行のcandidate-root coverの最小値は56と決定的に確定**する。blossomのmatching値・Tutte rankの確率的評価には依存しない。

## 成果物と実行境界

- verifier: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/audit_joint_cover_cost16_five_parent_witness_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-cover-cost16-five-parent-independent-audit-20261118.json`

V8実行環境で同じ独立手順を実行し、23 checks all PASS。出力には56組のroot→被覆行の対応を全件収録した。公開Python verifierは再現用に追加したが、このrunではrepo checkout上でそのファイル自体を実行していない。実行済みのV8計算と未実行の再現用ファイルを混同しない。

## 解釈の境界

これは5 parentの112行に対する**候補root被覆計画**の厳密最小値である。56 rootのいずれについてもWIN7-D10証明書があるとは主張しない。したがってS6 manifestのfold、S5 parent閉鎖、二石rootの解決は起きていない。REFUTED-D10やSTERILEをLOSSとは扱わない。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。
