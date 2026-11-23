# 2026-11-24 反転平面研究の引き継ぎ（次セッション向け）

## 現在の到達点（すべて K項目に記録済み・検証済み）

| 項目 | 結果 | 項 |
|---|---|---|
| 主定理 | **`K(q) ≤ q`（すべての `q ≥ 7`、無条件、証明）** | K1252 |
| 定式化 | 弧 ⇔ `Q⁻` 上の一般位置集合 ⇔ `[k,4,k−3]` MDS 符号 | K1250 |
| 下界 | `(q+5)/2`（Sonnino 1999）＋探索の上積み | K1251 |
| 厳密値 | 反転平面 `K(3..9)=5,5,6,6,7,9,9`、`K(11)=9` | K1058/K1253 |
| AG 盤 | `K(7,8,9,11)=6,8,9,9` | K1058 |
| 非Miquelian | 位数8: `K=7`（同値）、位数32: `≈14`（Miquelian 22） | K1254 |
| ゲーム | q ≤ 9 の完全 Grundy、5盤比較（通常・misère・P局面・終局） | K1253/K1254 |
| 文献 | 反転平面の弧の上界は未発表（`K ≤ q` が新規） | K1251 |

## 使えるツール（`research/experiments/finite-field-kyouen-20261120/scripts/`）

| スクリプト | 用途 |
|---|---|
| `inversive_fast.py --q Q --export` | M(q) の円リスト生成（`output/circles_qQ.txt`） |
| `arc_census.c/.exe circles.txt DEPTH` | アークのみを DFS 列挙。層サイズと `#arcs(K+1)=0` から K の厳密性 |
| `arc_maxsearch.exe circles.txt --trials N --ils M --force` | 最大弧の探索（ILS＋強制挿入） |
| `arc_swapsearch.exe circles.txt --k K --iters N` | 固定サイズのスワップ探索（K の上積み検証） |
| `grundy_full128.c/.exe circles.txt` | 完全 Grundy（通常＋misère）と層別 P局面数 |
| `tits_build.py --q 8/32 --out ...` | Suzuki–Tits 反転平面の構成 |
| `casse_glynn_quadrics.py --q 8/16/32` | CG 弧を通る二次曲面の全数分類 |
| `nrc_quadrics.py --q 5..13` | NRC を通る二次曲面の全数分類 |
| `quadric_type_check.py --q ...` | 「双曲型 ⟺ det が平方」の二重分類 |
| `cg_hyperbolic_proof.py --q 8/16` | 偶数 q の代入連鎖の数値検証 |
| `ag_board_export.py --q Q --out ...` | AG(2,q) 盤のブロック書き出し |
| `ag_vs_inversive.py --q ...` | AG 盤と反転平面盤の円族比較（q≡3 mod 4 でのみ一致） |

## 残る未解決と次の一手

1. **`liminf K/q`**：証明済みの枠 `0.5 ≤ · ≤ 1`、実測 `≈0.65`。探索は2種独立＋大予算で収束しており、
   「0.65 が真値」の可能性が高いが証明なし。**次の一手**：K(13)=10 を仮定した上での
   構成的一般化（現状の最大弧は代数的にランダムで、構造が見えない）。
2. **q=9 特異性**：`K(9)=9=q` で上界が tight、極大アークが単一軌道、構造化族（F_3-線型写像・
   2次元 F_3-部分空間）が極大アークを与える唯一の位数。**次の一手**：F_3-構造と
   `Q⁻(3,9)` の自己同型の相互作用を群論的に解析。
3. **q=7 の反転機構**：3点局面の拡大の Grundy 値が {0,2} に分かれる理由。**次の一手**：
   4点局面の値の再帰（5点局面の値）を q=7 で完全に書き出し、値の分布を説明する不変量を探す。
4. **非Miquelian 盤の上界**：K1252 の証明は使えない。Suzuki–Tits(32) は ≈14 で ambient 上界 33 に対し
   大きな slack。**次の一手**：Tits ovoid の 4-アーク構造（`O` の 3-設計の交わり）から上界を導く。
5. **Suzuki–Tits 位数128**：円の構成が現手法では非現実的（平面の全数走査が必要）。
   **次の一手**：4点共円判定を設計の組み合わせ論（Tits ovoid の座標式から直接）で計算する。
6. **q=13 の #7**：深さ6 センサス（CPU 20,000秒規模）が未完了。`#7` が判明すれば
   q=11 の層サイズ分布との比較が完成する。

## このセッションで踏んだ落とし穴（再発防止）

- パイプラインの `Select-Object -First` は上流を止め、`Tee-Object` のファイルも切り詰める。
  長時間ジョブの出力は `> file 2>&1` のリダイレクトで取る。
- K項目の artifact を既存エントリの `path:` 行直後に挿入すると YAML の重複キーになる
  （直前エントリの note 行の後に入れ、`yaml.safe_load` で検証する）。
- ファイルは CRLF のことがある。パッチは改行コードを正規化してから置換し、最後に復元する。
- push は「最新コミットの差分を origin/main に再適用」する方式なので、**コミットごとに即 push**
  しないと途中のコミットがブランチから外れる。
- `git pull --rebase` は origin/main の NTFS 非対応ファイル名で失敗する。plumbing
  （`read-tree -c core.protectNTFS=false` → `apply --cached` → `commit-tree` → `update-ref`）で回避。
