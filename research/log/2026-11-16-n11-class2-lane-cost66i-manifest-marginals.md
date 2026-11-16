# 2026-11-16：cost66i候補manifest marginals監査（bit19が最大marginal 4行、抽出順位確定）

開始時の最新mainは自commit `a1cbf6ca`（push直前に再取得して `74d9b4c8`（並走の76c claim更新）の上に載せた）。cost66i掃引の9 WIN7-D10候補について、出版済みhead-1450 projection tool（git blob `49fcd8ae...`、repo上の全basis 137ファイル＋MS5 manifest 6 partをblob pin検証のうえ取得）で候補別manifest marginalを測定した。

## 方法

`audit_cost66i_candidate_manifest_marginals_20261116.py`：76c版marginals監査（`audit_cost76c_candidate_manifest_marginals_20261117.py`）と同じ構成。head-1452 baseline（76d/77e foldの4 root）を0.6秒で完全再現（six-number summary `1452/174/6396/506144/4669/370058` 一致）した上で、9候補それぞれ単独、および昇順bit順で全9候補のprojectionを実行した。**両pending fold（64h prereg 20行・76c bit61行）は未着地のため**、候補marginalとpending fold閉鎖行の重複を別計上した。

## 結果（head-1452 baseline）

| bit | 単独marginal(manifest行) | pending 64h foldと重複 | 正味 | nodes |
|-----|------------------------|----------------------|------|-------|
| 19 | 4 | 1 | 3 | 2,645,084 |
| 28 | 3 | 1 | 2 | 4,429,373 |
| 88 | 2 | 0 | 2 | 2,662,456 |
| 99 | 2 | 0 | 2 | 1,812,502 |
| 103 | 2 | 0 | 2 | 1,033,614 |
| 29/58/90/112 | 1（自child行のみ） | 0 | 1 | − |

- bit 19が最大：4行 `00000000000000003801000000808000` / `00000000000000801206000000080000`（64h foldと重複）/ `00000000000000801222000000080000` / 自child行 `00000000000000801226000000000000`。
- 9候補のD4 cover orbit合計：63（9root×7）うちdistinct 55、manifest内20、うちhead-1452時点で未解決は9行。
- 全9候補fold時のprojection：head 1461/174/6387/505488/4660/369402（+9行）。
- **抽出推奨順位（正味marginal降順・nodes昇順）: [19, 103, 99, 88, 28, 29, 90, 58, 112]**。bit19の証明書抽出が最優先。bits 29/58/90/112は自child行のみで、他の候補が先にfoldされればmarginal 0になるため最後尾。
- 出力: `class2-lane-cost66i-candidate-manifest-marginals-20261116.json`（再実行で一貫）。

## 注意

- この監査はmanifest被覆projectionのみ。証明書の抽出・検証はまだ行っていない。foldは一切していない。
- marginalはhead-1452 baselineでの値。両pending fold着地後は共有行が落ちるため、66i foldの前に当時のcanonical headに対してprojectionを再導出する必要がある（recommendation.caveatに明記）。
- solved数はmanifest被覆の簿記であり勝敗ではない。**11x11空盤はUNKNOWNのまま**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4もすべてUNKNOWN。
