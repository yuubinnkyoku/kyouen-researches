# 19残存初手の共同S5証明計画：必要未確定S5数の上界31,546・下界6,573（2026-10-12）

K0415の19未確定初手軌道について、各初手の中央応手（`f=60`）rootをLOSSにする証明が消費する未確定exact-S5数の、個別最適化の合計と19 root共同最適化を比較した。solver探索は行わず、有限の組合せ最適化と既存cache証拠だけを使う。

## 結果

| 対象 | 上界（実行可能計画） | 下界（有効） |
|---|---:|---:|
| 19 root個別の合計 | 63,118 | 16,662（個別element-only双対の合計、参考値） |
| 19 root共同 | **31,546** | **6,573**（element-only分数双対） |
| 削減 | 31,572（50.02%） | — |

- 共同計画は869個の相異なる有料third-move群を31,546個の未確定S5で覆う。各群は1個のS4応手を取り、その未知S5子集合の和集合が計画である。79群は既知LOSS S4で無料（122 third手）。
- 削減の主因は群の重複である。2261 third手の選択肢集合は948種に潰れ（79無料を含む）、相異なる有料群は869個だけになる。重複群は同一S4で追加費用なしに覆えるため、統合前重複除去は最適値を変えない（`build_instances` の `_dedup` と `Instance` のdocstringに理由を記録）。
- 最も安い単独新規LOSS軌道は初手49（上界2,055）。個別上界は2,055〜4,612、下界は581〜1,135。
- 下界の内訳（共同）：per-group-min-max 111、threshold 111、element-only双対 6,573.146（最強）、grouped分数双対 1,586.75、LP緩和双対 728.0。双対値は `solve_instance` の `LB <= UB` 表明で実行時検査した。
- 寄与統計：31,546個のS5のうち31,431個が複数群、31,374個が複数rootで使われる。1個のS5が担う群数は平均6.982、最大16。

## 方法

`scripts/build_dependency_graph.py` が20 root（既知LOSS基準1＋未確定19）の119 third手ずつについて、独立整数幾何 `Board` で正準S4応手クラスを再生成し、各S4のexact-S5子を現行cache照合で LOSS既知／WIN除外／未知に分ける。S4クラス総数34,949（LOSS 32、UNKNOWN 34,527、WIN除外390）、S5費用宇宙962,525。

`scripts/optimize_s5_selection.py` が各群1選択肢・和集合最小の有限問題を解く。上界は4種greedyのmulti-start＋和集合内再選択＋強制要素縮小（`--restarts 3` で16 start）。下界は上表の5種で、いずれも双対実行可能点または被覆しきい値であり、solver node数・実行時間・勝敗証明ではない。

`scripts/verify_plans.py` は独立再検証である。19 rootの全2,261 third手の合法応手集合、到達する全34,948 S4クラスのstatusと未知子集合、無料third手のゼロ費用証人、個別／共同プランの一致を再計算し、失敗0で通過した（`output/plan-verification.json`）。

## 再現と限界

```powershell
uv run --locked python research/experiments/n11-joint-s5-proof-planning-20261012/scripts/build_dependency_graph.py
uv run --locked python research/experiments/n11-joint-s5-proof-planning-20261012/scripts/optimize_s5_selection.py --restarts 3
uv run --locked python research/experiments/n11-joint-s5-proof-planning-20261012/scripts/verify_plans.py
```

- 上界は楽観的証明計画であり、列挙した未知S5が将来すべてLOSSになる仮定に依存する。1個でもWINになれば該当S4は使えず計画は組み直しになる。
- 下界と上界の差（6,573対31,546）は閉じていない。分枝限定による最適性証明はしていない。
- 中央応手（`f=60`）固定の評価であり、非中央応手の個別最適値比較（`--extra-replies`）は未実施。
- 初手をWIN証明する場合の費用（120応手すべてをWINにする必要）は本実験の対象外。LOSS側だけの片側評価である。
